"""
Module to implement a plugin that ensures that locally aimed link fragments are valid.
"""

import re
import urllib
from enum import Enum
from html.parser import HTMLParser
from re import Pattern
from typing import Dict, List, Optional, Set, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetailsV2,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.email_autolink_markdown_token import EmailAutolinkMarkdownToken
from pymarkdown.tokens.inline_code_span_markdown_token import (
    InlineCodeSpanMarkdownToken,
)
from pymarkdown.tokens.link_reference_definition_markdown_token import (
    LinkReferenceDefinitionMarkdownToken,
)
from pymarkdown.tokens.link_start_markdown_token import LinkStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.raw_html_markdown_token import RawHtmlMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken
from pymarkdown.tokens.uri_autolink_markdown_token import UriAutolinkMarkdownToken


class RuleMd051States(Enum):
    """
    Enumeration to provide guidance on what to look for as the tokens come in.
    """

    LOOK_FOR_LINKS_OR_HEADINGS = 0
    LOOK_FOR_ATX_END = 1
    LOOK_FOR_SETEXT_END = 2
    LOOK_FOR_HTML_BLOCK_END = 3


class MyHTMLParser(HTMLParser):
    """
    Class to handle the parsing of an HTML document into its constituent parts
    to allow for tags and attributes to be extracted.
    """

    def __init__(self) -> None:
        self.valid_targets: List[str] = []
        super().__init__()

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        found_target = next(
            (
                value
                for attr, value in attrs
                if tag == "a" and attr in ["id", "name"] or tag != "a" and attr == "id"
            ),
            None,
        )
        if found_target is not None:
            self.valid_targets.append(found_target)


# pylint: disable=too-many-instance-attributes
class RuleMd051(RulePlugin):
    """
    Class to implement a plugin that ensures that locally aimed link fragments are valid.
    """

    __PUNCTUATION_REGEXP = re.compile(r"[^\w\- ]")
    __html_character_escape_map = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
        '"': "&quot;",
    }

    def __init__(self) -> None:
        """
        Initialize an instance of the RuleMd048 class.
        """
        super().__init__()
        self.__ignore_case = True
        self.__ignore_pattern_regex: Optional[str] = None
        self.__compiled_ignore_pattern_regex: Optional[Pattern[str]] = None
        self.__current_heading = ""
        self.__heading_state = RuleMd051States.LOOK_FOR_LINKS_OR_HEADINGS
        self.__present_headings: Dict[str, int] = {}
        self.__available_headings: Set[str] = set()
        self.__link_tokens: List[Tuple[str, MarkdownToken]] = []

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="link-fragments",
            plugin_id="MD051",
            plugin_enabled_by_default=True,
            plugin_description="Link fragments should be valid.",
            plugin_version="0.5.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md051.md",
            plugin_configuration="ignore_case",
            # plugin_supports_fix=True,
            # plugin_fix_level=2,
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__ignore_case = (
            self.plugin_configuration.get_boolean_property_with_default(
                "ignore_case", True
            )
        )
        self.__ignore_pattern_regex = (
            self.plugin_configuration.get_string_property_with_default(
                "ignore_pattern_regex", ""
            )
        )
        if self.__ignore_pattern_regex:
            try:
                self.__compiled_ignore_pattern_regex = re.compile(
                    self.__ignore_pattern_regex
                )
            except re.error as this_exception:
                raise ValueError(
                    "The value for property 'plugins.md051.ignore_pattern_regex' is not a valid regular expression."
                ) from this_exception

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("ignore_case", self.__ignore_case),
            QueryConfigItem("ignore_pattern_regex", self.__ignore_pattern_regex or ""),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__current_heading = ""
        self.__heading_state = RuleMd051States.LOOK_FOR_LINKS_OR_HEADINGS
        self.__present_headings = {}
        self.__available_headings = set()
        self.__link_tokens = []

    def completed_file(self, context: PluginScanContext) -> None:
        """
        Event that the file being currently scanned is now completed.
        """
        for link_text, link_token in self.__link_tokens:
            if link_text != "top" and link_text not in self.__available_headings:

                did_match = False
                if self.__compiled_ignore_pattern_regex is not None:
                    did_match = (
                        self.__compiled_ignore_pattern_regex.match(link_text)
                        is not None
                    )

                if not did_match:
                    self.report_next_token_error(
                        context, link_token, extra_error_information=None
                    )

    def __encode_uri_component(self, s: str) -> str:
        """
        Python equivalent of JavaScript's encodeURIComponent().
        Encodes all characters except: A-Z a-z 0-9 - _ . ! ~ * ' ( )
        """
        return urllib.parse.quote(s, safe="~-_.!~*'()")  # type: ignore

    def __ascii_downcase(self, text: str) -> str:
        return "".join(c.lower() if c.isascii() else c for c in text)

    def __resolve_special_case(self, converted_heading: str) -> str:
        """
        Due to the way PyMarkdown encodes backslash escapes, there is a weird
        case where replacing a backslash escape of a special html character,
        such as `\\<` returns `\\\x08\x07` + character + `\x07` + replacement
        + `\x07`. If resolved normally, it resolves to the replacement string,
        instead of the punctuation characters that the filter algorithm expects.
        Therefore, we handle it ourselves.
        """
        start_character_sequence = "\\\x08\x07"
        last_index = -1
        while start_character_sequence in converted_heading:
            start_index = converted_heading.index(start_character_sequence)
            assert last_index != start_index
            last_index = start_index
            character_after_start_index = start_index + len(start_character_sequence)
            next_character = converted_heading[character_after_start_index]
            assert next_character in RuleMd051.__html_character_escape_map
            mapped_next_character_sequence = (
                f"\x07{RuleMd051.__html_character_escape_map[next_character]}\x07"
            )
            end_index = (
                character_after_start_index + 1 + len(mapped_next_character_sequence)
            )
            replacement_text = converted_heading[
                character_after_start_index + 1 : end_index
            ]
            assert mapped_next_character_sequence == replacement_text
            converted_heading = (
                converted_heading[:start_index] + converted_heading[end_index:]
            )
        return converted_heading

    def __add_current_heading(self) -> None:
        """
        https://github.com/gjtorikian/html-pipeline/blob/f13a1534cb650ba17af400d1acd3a22c28004c09/lib/html/pipeline/toc_filter.rb#L30
        """

        converted_heading = (
            self.__ascii_downcase(self.__current_heading)
            if self.__ignore_case
            else self.__current_heading
        )
        converted_heading = self.__resolve_special_case(converted_heading)
        converted_heading = ParserHelper.resolve_all_from_text(converted_heading)
        converted_heading = RuleMd051.__PUNCTUATION_REGEXP.sub("", converted_heading)
        converted_heading = converted_heading.replace(" ", "-")

        count = self.__present_headings.get(converted_heading, 0)
        unique_suffix = f"-{count}" if count > 0 else ""
        unique_heading = self.__encode_uri_component(converted_heading + unique_suffix)

        self.__present_headings[converted_heading] = count + 1
        self.__available_headings.add(unique_heading)
        self.__current_heading = ""

    def __handle_raw_html(self, raw_token: RawHtmlMarkdownToken) -> None:
        parser = MyHTMLParser()
        parser.feed(f"<{raw_token.extra_data}>")
        parser.close()
        for i in parser.valid_targets:
            self.__current_heading = i
            self.__add_current_heading()

    def __handle_html_block(self) -> None:
        parser = MyHTMLParser()
        parser.feed(self.__current_heading)
        parser.close()
        for i in parser.valid_targets:
            self.__current_heading = i
            self.__add_current_heading()
        self.__current_heading = ""

    def __next_token_look(self, token: MarkdownToken) -> None:
        if token.is_atx_heading:
            self.__heading_state = RuleMd051States.LOOK_FOR_ATX_END
        elif token.is_setext_heading:
            self.__heading_state = RuleMd051States.LOOK_FOR_SETEXT_END
        elif token.is_inline_raw_html:
            self.__handle_raw_html(cast(RawHtmlMarkdownToken, token))
        elif token.is_html_block:
            self.__heading_state = RuleMd051States.LOOK_FOR_HTML_BLOCK_END
        elif token.is_inline_link:
            link_token = cast(LinkStartMarkdownToken, token)
            if link_token.label_type == "inline" and link_token.link_uri.startswith(
                "#"
            ):
                self.__link_tokens.append((link_token.link_uri[1:], link_token))
        elif token.is_link_reference_definition:
            link_reference_token = cast(LinkReferenceDefinitionMarkdownToken, token)
            assert link_reference_token.link_destination is not None
            if link_reference_token.link_destination.startswith("#"):
                self.__link_tokens.append(
                    (link_reference_token.link_destination[1:], link_reference_token)
                )

    def __next_token_look_for_atx_end(self, token: MarkdownToken) -> None:
        if token.is_atx_heading_end:
            self.__add_current_heading()
            self.__heading_state = RuleMd051States.LOOK_FOR_LINKS_OR_HEADINGS
        elif token.is_text:
            text_token = cast(TextMarkdownToken, token)
            self.__current_heading += text_token.token_text
        elif token.is_inline_code_span:
            code_span_token = cast(InlineCodeSpanMarkdownToken, token)
            self.__current_heading += code_span_token.span_text
        elif token.is_inline_uri_autolink:
            uri_autolink_token = cast(UriAutolinkMarkdownToken, token)
            self.__current_heading += uri_autolink_token.autolink_text
        elif token.is_inline_autolink:
            autolink_token = cast(EmailAutolinkMarkdownToken, token)
            self.__current_heading += autolink_token.autolink_text

    def __next_token_look_for_setext_end(self, token: MarkdownToken) -> None:
        if token.is_setext_heading_end:
            self.__add_current_heading()
            self.__heading_state = RuleMd051States.LOOK_FOR_LINKS_OR_HEADINGS
        elif token.is_text:
            text_token = cast(TextMarkdownToken, token)
            self.__current_heading += text_token.token_text
        elif token.is_inline_code_span:
            code_span_token = cast(InlineCodeSpanMarkdownToken, token)
            self.__current_heading += code_span_token.span_text
        elif token.is_inline_uri_autolink:
            uri_autolink_token = cast(UriAutolinkMarkdownToken, token)
            self.__current_heading += uri_autolink_token.autolink_text
        elif token.is_inline_autolink:
            email_autolink_token = cast(EmailAutolinkMarkdownToken, token)
            self.__current_heading += email_autolink_token.autolink_text

    def __next_token_look_for_html_block_end(self, token: MarkdownToken) -> None:
        if token.is_html_block_end:
            self.__handle_html_block()
            self.__heading_state = RuleMd051States.LOOK_FOR_LINKS_OR_HEADINGS
        elif token.is_text:
            text_token = cast(TextMarkdownToken, token)
            self.__current_heading += text_token.token_text

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if self.__heading_state == RuleMd051States.LOOK_FOR_LINKS_OR_HEADINGS:
            self.__next_token_look(token)
        elif self.__heading_state == RuleMd051States.LOOK_FOR_ATX_END:
            self.__next_token_look_for_atx_end(token)
        elif self.__heading_state == RuleMd051States.LOOK_FOR_SETEXT_END:
            self.__next_token_look_for_setext_end(token)
        else:
            assert self.__heading_state == RuleMd051States.LOOK_FOR_HTML_BLOCK_END
            self.__next_token_look_for_html_block_end(token)


# pylint: enable=too-many-instance-attributes
