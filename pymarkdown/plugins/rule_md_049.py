"""
Module to implement a plugin that validates uris fo links and images.
"""
import os.path
import re
import urllib.parse
from typing import Callable, Dict, Generator, List, Optional, Pattern, Tuple, cast

from pymarkdown.inline_markdown_token import ReferenceMarkdownToken, TextMarkdownToken
from pymarkdown.leaf_markdown_token import SetextHeadingMarkdownToken
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin

NOT_A_VALID_HEADING = "Wrong reference: # anchor not a valid heading"

FILE_DOES_NOT_EXIST = "Dangling reference: file does not exist!"

TriggeredRuleParams = Tuple[str, int, int, str, str, str, Optional[str]]


class RuleMd049(RulePlugin):
    """
    Class to implement a plugin that looks for link and images elements that have an invalid uri.
    """

    EXTERNAL_LINK_REGEX = re.compile("^(.+):.*$")

    def __init__(self) -> None:
        super().__init__()
        self.heading_processor = HeadingProcessor()
        self.anchor_validator = AnchorValidator(
            self.report_next_token_error, self._create_triggered_rule_params
        )

    def completed_file(self, context: PluginScanContext) -> None:
        """
        Event that the file being currently scanned is now completed.
        """
        scan_file = os.path.realpath(context.scan_file)

        self.heading_processor.completed_file(scan_file)
        current_file_headings = self.heading_processor.get_headings(scan_file)
        triggers = self.anchor_validator.complete_file(
            scan_file, current_file_headings
        )
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

        link_uri, link_anchor = self._extract_link_uri(token)
        if self.EXTERNAL_LINK_REGEX.match(link_uri):
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
        line_number_delta: int = 0,
        column_number_delta: int = 0,
        use_original_position: bool = False,
    ) -> TriggeredRuleParams:
        """
        Prepare parameters to create an invalid heading reference report later.
        """
        if use_original_position:
            leaf_token = cast(SetextHeadingMarkdownToken, token)
            line_number = leaf_token.original_line_number
            column_number = leaf_token.original_column_number
        else:
            line_number = token.line_number
            column_number = token.column_number

        return (
            context.scan_file,
            line_number + line_number_delta,
            column_number + column_number_delta
            if column_number_delta >= 0
            else -column_number_delta,
            self.get_details().plugin_id,
            self.get_details().plugin_name,
            self.get_details().plugin_description,
            extra_error_information,
        )

    @staticmethod
    def _resolve_to_filesystem_path(context: PluginScanContext, link_uri: str) -> str:
        if not link_uri:
            path = context.scan_file
        elif link_uri.startswith("/"):
            path = link_uri[1:]
        else:
            path = os.path.join(os.path.dirname(context.scan_file), link_uri)
        return os.path.realpath(path)

    @staticmethod
    def _extract_link_uri(token: MarkdownToken) -> Tuple[str, Optional[str]]:
        ref_token = cast(ReferenceMarkdownToken, token)
        link_uri_split = ref_token.link_uri.split("#", 1)
        if len(link_uri_split) == 2:
            return link_uri_split[0], link_uri_split[1]
        return link_uri_split[0], None


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
            self.__heading_text += text_token.token_text

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


KEBAB2REGEX_REGEX = re.compile(r"([^A-Za-z0-9]+)")


def anchor2regex(anchor: str) -> Pattern[str]:
    """
    Converts a kebab-case anchor into a regex.
    """
    return re.compile(
        KEBAB2REGEX_REGEX.sub(r".*", urllib.parse.unquote_plus(anchor)),
        re.ASCII | re.IGNORECASE,
    )


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
            link_regex = anchor2regex(link_anchor)
            if not [heading for heading in headings if link_regex.match(heading)]:
                # Report invalid heading reference
                self.__report_error(context, token, NOT_A_VALID_HEADING)
        else:
            # Case B: we did not process the referenced file and need to store this reference check until we
            #         finished the referenced file.

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
            link_regex = anchor2regex(link_anchor)
            if not [heading for heading in headings if link_regex.match(heading)]:
                for trigger_params in anchors[link_anchor]:
                    yield trigger_params
