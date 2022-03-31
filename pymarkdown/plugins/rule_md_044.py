"""
Module to implement a plugin that ensures that specific proper names have
the correct capitalization.
"""
from typing import List, cast

from pymarkdown.constants import Constants
from pymarkdown.inline_markdown_token import (
    InlineCodeSpanMarkdownToken,
    LinkStartMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.leaf_markdown_token import LinkReferenceDefinitionMarkdownToken
from pymarkdown.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class RuleMd044(RulePlugin):
    """
    Class to implement a plugin that ensures that specific proper names have
    the correct capitalization.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__proper_name_list: List[str] = []
        self.__check_in_code_blocks: bool = False
        self.__is_in_code_block: bool = False

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="proper-names",
            plugin_id="MD044",
            plugin_enabled_by_default=True,
            plugin_description="Proper names should have the correct capitalization",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md044.md",
            plugin_configuration="names,code_blocks",
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__is_in_code_block = False

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__check_in_code_blocks = self.plugin_configuration.get_boolean_property(
            "code_blocks", default_value=True
        )
        self.__proper_name_list = []
        if names := self.plugin_configuration.get_string_property(
            "names",
            default_value="",
        ).strip():
            lower_list: List[str] = []
            for next_name in names.split(","):
                next_name = next_name.strip()
                if not next_name:
                    raise ValueError(
                        "Elements in the comma-separated list cannot be empty."
                    )
                if next_name.lower() in lower_list:
                    raise ValueError(
                        f"Element `{next_name}` is already present in the list as "
                        + f"`{self.__proper_name_list[lower_list.index(next_name.lower())]}`."
                    )
                lower_list.append(next_name.lower())
                self.__proper_name_list.append(next_name)

    # pylint: disable=too-many-arguments
    def __check_for_proper_match(
        self,
        original_source: str,
        found_index: int,
        required_capitalization: str,
        context: PluginScanContext,
        token: MarkdownToken,
        line_adjust: int,
        col_adjust: int,
    ) -> None:

        original_found_text = original_source[
            found_index : found_index + len(required_capitalization)
        ]
        after_found_index = found_index + len(required_capitalization)

        is_character_before_match = False
        if found_index > 0:
            is_character_before_match = original_source[found_index - 1].isalnum()

        is_character_after_match = False
        if after_found_index < len(original_source):
            is_character_after_match = original_source[after_found_index].isalnum()

        if not is_character_after_match and not is_character_before_match:
            assert len(original_found_text) == len(required_capitalization)
            if original_found_text != required_capitalization:
                extra_data = f"Expected: {required_capitalization}; Actual: {original_found_text}"
                self.report_next_token_error(
                    context,
                    token,
                    extra_error_information=extra_data,
                    line_number_delta=line_adjust,
                    column_number_delta=col_adjust,
                )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __search_for_possible_matches(
        self,
        string_to_check: str,
        string_to_check_lower: str,
        search_start: int,
        found_index: int,
        start_x_offset: int,
        start_y_offset: int,
        same_line_offset: int,
        next_name: str,
        context: PluginScanContext,
        token: MarkdownToken,
    ) -> None:
        col_adjust, line_adjust = ParserHelper.adjust_for_newlines(
            string_to_check_lower, search_start, found_index
        )
        if line_adjust == 0 and start_y_offset == 0:
            col_adjust -= same_line_offset
        line_adjust += start_y_offset
        if col_adjust == 0 and start_x_offset:
            col_adjust += (
                -start_x_offset if start_x_offset > 0 else -(-start_x_offset - 1)
            )
            col_adjust = -col_adjust
        elif col_adjust > 0 and start_x_offset:
            col_adjust += -start_x_offset - 1
            col_adjust = -col_adjust
        self.__check_for_proper_match(
            string_to_check,
            found_index,
            next_name,
            context,
            token,
            line_adjust,
            col_adjust,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __search_for_matches(
        self,
        string_to_check: str,
        context: PluginScanContext,
        token: MarkdownToken,
        same_line_offset: int = 0,
        start_x_offset: int = 0,
        start_y_offset: int = 0,
    ) -> None:

        string_to_check = ParserHelper.remove_all_from_text(string_to_check)
        string_to_check_lower = string_to_check.lower()
        for next_name in self.__proper_name_list:
            next_name_lower = next_name.lower()
            search_start = 0
            found_index = string_to_check_lower.find(next_name_lower, search_start)
            while found_index != -1:

                self.__search_for_possible_matches(
                    string_to_check,
                    string_to_check_lower,
                    search_start,
                    found_index,
                    start_x_offset,
                    start_y_offset,
                    same_line_offset,
                    next_name,
                    context,
                    token,
                )

                search_start = found_index + len(next_name)
                found_index = string_to_check_lower.find(next_name_lower, search_start)

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __adjust_for_newlines_and_search(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        link_body_text: str,
        full_link_text: str,
        string_to_check: str,
        same_line_offset: int,
    ) -> None:

        start_x_offset = 0
        start_y_offset = 0
        if ParserHelper.newline_character in link_body_text:
            start_x_offset, start_y_offset = ParserHelper.adjust_for_newlines(
                full_link_text, 0, len(full_link_text)
            )
        self.__search_for_matches(
            string_to_check,
            context,
            token,
            same_line_offset,
            start_x_offset,
            start_y_offset,
        )

    # pylint: enable=too-many-arguments

    def __handle_inline_link_end(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        end_token = cast(EndMarkdownToken, token)
        link_token = cast(LinkStartMarkdownToken, end_token.start_markdown_token)
        if link_token.label_type == Constants.link_type__inline:
            assert link_token.before_title_whitespace is not None
            assert link_token.inline_title_bounding_character is not None
            assert link_token.before_link_whitespace is not None
            link_body = "".join(
                [
                    link_token.before_link_whitespace,
                    link_token.active_link_uri,
                    link_token.before_title_whitespace,
                    link_token.inline_title_bounding_character,
                ]
            )
            full_link_text = "".join(
                [
                    "[",
                    link_token.text_from_blocks,
                    "](",
                    link_body,
                ]
            )
            same_line_offset = len(full_link_text) + 1
            assert link_token.active_link_title is not None
            self.__adjust_for_newlines_and_search(
                context,
                link_token,
                link_body,
                full_link_text,
                link_token.active_link_title,
                same_line_offset,
            )

    def __handle_inline_image(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        link_token = cast(LinkStartMarkdownToken, token)
        same_line_offset = -2
        self.__search_for_matches(
            link_token.text_from_blocks, context, token, same_line_offset
        )

        if link_token.label_type == Constants.link_type__inline:
            assert link_token.before_link_whitespace is not None
            assert link_token.before_title_whitespace is not None
            assert link_token.inline_title_bounding_character is not None
            link_body = "".join(
                [
                    link_token.before_link_whitespace,
                    link_token.active_link_uri,
                    link_token.before_title_whitespace,
                    link_token.inline_title_bounding_character,
                ]
            )
            full_link_text = f"![{link_token.text_from_blocks}]({link_body}"
            same_line_offset = len(full_link_text) + 1
            assert link_token.active_link_title is not None
            self.__adjust_for_newlines_and_search(
                context,
                token,
                link_body,
                full_link_text,
                link_token.active_link_title,
                same_line_offset,
            )

    def __handle_link_reference_definition(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        lrd_token = cast(LinkReferenceDefinitionMarkdownToken, token)
        link_name = lrd_token.link_name_debug or lrd_token.link_name
        same_line_offset = -1
        self.__search_for_matches(link_name, context, token, same_line_offset)

        assert lrd_token.link_destination_whitespace is not None
        assert lrd_token.link_destination is not None
        assert lrd_token.link_title_whitespace is not None
        full_link_text = "".join(
            [
                "[",
                link_name,
                "]:",
                lrd_token.link_destination_whitespace,
                lrd_token.link_destination,
                lrd_token.link_title_whitespace,
                "'",
            ]
        )
        same_line_offset = -(len(full_link_text) - 1)
        assert lrd_token.link_title_raw is not None
        self.__adjust_for_newlines_and_search(
            context,
            token,
            full_link_text,
            full_link_text,
            lrd_token.link_title_raw,
            same_line_offset,
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if not self.__proper_name_list:
            return
        if token.is_text:
            text_token = cast(TextMarkdownToken, token)
            if not self.__is_in_code_block or self.__check_in_code_blocks:
                self.__search_for_matches(text_token.token_text, context, token)
        elif token.is_inline_code_span:
            code_span_token = cast(InlineCodeSpanMarkdownToken, token)
            same_line_offset = len(code_span_token.extracted_start_backticks) + len(
                code_span_token.leading_whitespace
            )
            self.__search_for_matches(
                code_span_token.span_text, context, token, same_line_offset
            )
        elif token.is_inline_link_end:
            self.__handle_inline_link_end(context, token)
        elif token.is_inline_image:
            self.__handle_inline_image(context, token)
        elif token.is_link_reference_definition:
            self.__handle_link_reference_definition(context, token)
        elif token.is_code_block:
            self.__is_in_code_block = True
        elif token.is_code_block_end:
            self.__is_in_code_block = False
