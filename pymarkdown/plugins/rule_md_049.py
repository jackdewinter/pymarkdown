"""
Module to implement a plugin that validates uris fo links and images.
"""
import html
import os.path
import re
import urllib.parse
from typing import Callable, Dict, Generator, List, Optional, Pattern, Tuple, cast
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.tokens.inline_code_span_markdown_token import (
    InlineCodeSpanMarkdownToken,
)
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken

from pymarkdown.tokens.reference_markdown_token import ReferenceMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin

NOT_A_VALID_HEADING = "Wrong reference: # anchor not a valid heading"

DUPLICATE_HEADING = "Multiple headings found"

FILE_DOES_NOT_EXIST = "Dangling reference: file does not exist!"

TriggeredRuleParams = Tuple[str, int, int, str, str, str, Optional[str], bool]


class RuleMd049(RulePlugin):
    """
    Class to implement a plugin that looks for link and images elements that have an invalid uri.
    """

    def __init__(self) -> None:
        super().__init__()
        self.heading_processor = HeadingProcessor()
        self.anchor_validator = AnchorValidator(
            self.report_next_token_error, self._create_triggered_rule_params
        )
        self.__whitelist_regex: Optional[Pattern[str]] = None

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        regex_string = self.plugin_configuration.get_string_property(
            "regex", default_value=""
        )
        self.__whitelist_regex = re.compile(regex_string) if regex_string else None

    def completed_file(self, context: PluginScanContext) -> None:
        """
        Event that the file being currently scanned is now completed.
        """
        scan_file = os.path.realpath(context.scan_file)

        self.heading_processor.completed_file(scan_file)
        current_file_headings = self.heading_processor.get_headings(scan_file)
        triggers = self.anchor_validator.complete_file(scan_file, current_file_headings)
        for trigger_params in triggers:
            context.add_triggered_rule(*trigger_params)

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="validate-refs",
            plugin_id="MD049",
            plugin_enabled_by_default=False,
            plugin_description="Local URIs should be valid",
            plugin_version="0.0.2",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md049.md",
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        self.heading_processor.next_token(token)
        self._validate_references(context, token)

    def _validate_references(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        if not token.is_inline_image and not token.is_inline_link:
            # Not a reference so nothing to do here
            return
        uri = self._extract_link_uri(token)

        if self.__whitelist_regex and self.__whitelist_regex.match(uri):
            return

        link_scheme, link_uri, link_anchor = self._split_link_uri(uri)

        if link_scheme != "":
            # External link so nothing to do here
            return

        filesystem_path = self._resolve_to_filesystem_path(context, link_uri)
        # Check that referenced file exists
        if os.path.exists(filesystem_path):
            headings = self.heading_processor.get_headings(filesystem_path)
            self.anchor_validator.next_anchor(
                context, token, headings, filesystem_path, link_anchor
            )
        else:
            # Report invalid file reference
            self.report_next_token_error(
                context, token, extra_error_information=FILE_DOES_NOT_EXIST
            )

    # pylint: disable=too-many-arguments
    def _create_triggered_rule_params(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        extra_error_information: Optional[str] = None,
    ) -> TriggeredRuleParams:
        """
        Prepare parameters to create an invalid heading reference report later.
        """
        return (
            context.scan_file,
            token.line_number,
            token.column_number,
            self.get_details().plugin_id,
            self.get_details().plugin_name,
            self.get_details().plugin_description,
            extra_error_information,
            False,
        )

    @staticmethod
    def _resolve_to_filesystem_path(context: PluginScanContext, link_uri: str) -> str:
        if not link_uri:
            path = context.scan_file
        elif link_uri.startswith("/"):
            path = urllib.parse.unquote(link_uri[1:])
        else:
            path = os.path.join(
                os.path.dirname(context.scan_file), urllib.parse.unquote(link_uri)
            )
        return os.path.realpath(path)

    @staticmethod
    def _extract_link_uri(token: MarkdownToken) -> str:
        ref_token = cast(ReferenceMarkdownToken, token)
        return ref_token.link_uri

    @staticmethod
    def _split_link_uri(link_uri: str) -> Tuple[str, str, Optional[str]]:
        parsed_uri = urllib.parse.urlparse(link_uri)
        return parsed_uri.scheme, parsed_uri.path, parsed_uri.fragment


class HeadingProcessor:
    """
    Processor to handle found headings
    """

    def __init__(self) -> None:
        super().__init__()
        self.__start_token: Optional[MarkdownToken] = None
        self.__heading_text: str = ""
        self.__current_file_headings: List[str] = []
        self.__headings_map: Dict[str, List[str]] = {}

    def next_token(self, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_setext_heading or token.is_atx_heading:
            self.__heading_text = ""
            self.__start_token = token
        elif token.is_setext_heading_end or token.is_atx_heading_end:
            self.__current_file_headings.append(self.__heading_text)
            self.__heading_text = ""
            self.__start_token = None
        elif self.__start_token and token.is_text:
            text_token = cast(TextMarkdownToken, token)
            self.__heading_text += html.unescape(
                ParserHelper.resolve_all_from_text(text_token.token_text)
            )
        elif self.__start_token and token.is_inline_code_span:
            inline_code_token = cast(InlineCodeSpanMarkdownToken, token)
            # Restore inline code element to create correct github link_fragment
            self.__heading_text += inline_code_token.extracted_start_backticks
            self.__heading_text += html.unescape(
                ParserHelper.resolve_all_from_text(inline_code_token.span_text)
            )
            self.__heading_text += inline_code_token.extracted_start_backticks

    def completed_file(self, filename: str) -> None:
        """
        Event that the file being currently scanned is now completed.
        """
        self.__headings_map[filename] = self.__current_file_headings
        self.__start_token = None
        self.__heading_text = ""
        self.__current_file_headings = []

    def get_headings(self, filename: str) -> List[str]:
        """
        Return found headlines of the given filename
        """
        return self.__headings_map.get(filename, [])


SPECIAL_CHAR_REGEX: Pattern[str] = re.compile(r"[^\w\s-]")
SPACE_REGEX: Pattern[str] = re.compile(r"[ \t\n\r\f\v]+")
SPECIAL_SPACE_REGEX: Pattern[str] = re.compile(r"[\s]")


def compare_anchor(anchor: str, headline: str) -> bool:
    """
    Converts a kebab-case anchor into a regex.
    """
    cleaned = headline.lower()
    # cleaned = SPACE_REGEX.sub('-', cleaned)
    cleaned = SPECIAL_SPACE_REGEX.sub("-", cleaned)
    cleaned = SPECIAL_CHAR_REGEX.sub("", cleaned)
    cleaned = urllib.parse.quote(cleaned)
    return cleaned == anchor


class AnchorValidator:
    """
    Class to validate found anchors
    """

    def __init__(
        self,
        report_error: Callable[[PluginScanContext, MarkdownToken, str], None],
        create_trigger_params: Callable[
            [PluginScanContext, MarkdownToken, str], TriggeredRuleParams
        ],
    ):
        self.__anchor_map: Dict[str, Dict[str, List[TriggeredRuleParams]]] = {}
        self.__report_error = report_error
        self.__create_trigger_params = create_trigger_params

    def get_anchor_map(self, filename: str) -> Dict[str, List[TriggeredRuleParams]]:
        """
        Return anchors that need to be validated for the given filename
        """
        if filename not in self.__anchor_map:
            self.__anchor_map[filename] = {}
        return self.__anchor_map[filename]

    def _insert_anchor_validation(
        self, filename: str, heading: str, trigger: TriggeredRuleParams
    ) -> None:
        path_anchor_map = self.get_anchor_map(filename)
        link_anchor_list = path_anchor_map.get(heading, [])
        link_anchor_list.append(trigger)
        path_anchor_map[heading] = link_anchor_list

    # pylint: disable=too-many-arguments
    def next_anchor(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        headings: List[str],
        filesystem_path: str,
        link_anchor: Optional[str],
    ) -> None:
        """
        Event that a new anchor is being processed.
        """
        if not link_anchor:
            return
        if headings:
            # Case A: we already processed the referenced file and know the headlines
            headings_count = len(
                [
                    heading
                    for heading in headings
                    if compare_anchor(link_anchor, heading)
                ]
            )
            if headings_count == 0:
                # Report invalid heading reference
                self.__report_error(context, token, NOT_A_VALID_HEADING)
            elif headings_count > 1:
                # Report invalid heading reference
                self.__report_error(context, token, DUPLICATE_HEADING)
        else:
            # Case B: we did not process the referenced file and need to store
            #         this reference check until we finished the referenced file.

            self._insert_anchor_validation(
                filesystem_path,
                link_anchor,
                self.__create_trigger_params(context, token, NOT_A_VALID_HEADING),
            )

    def complete_file(
        self, scan_file: str, headings: List[str]
    ) -> Generator[TriggeredRuleParams, None, None]:
        """
        Event that the file being currently scanned is now completed.
        """
        anchors = self.get_anchor_map(scan_file)
        for link_anchor in anchors.keys():
            headings_count = len(
                [
                    heading
                    for heading in headings
                    if compare_anchor(link_anchor, heading)
                ]
            )
            if headings_count == 0:
                yield from anchors[link_anchor]
            elif headings_count > 1:
                for trigger_params in anchors[link_anchor]:
                    yield (*trigger_params[:-1], DUPLICATE_HEADING)
