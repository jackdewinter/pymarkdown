"""
Module to implement a plugin that ensures that specific proper names have
the correct capitalization.
"""

from dataclasses import dataclass
from typing import List, Optional, cast

from pymarkdown.general.constants import Constants
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetailsV2,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.image_start_markdown_token import ImageStartMarkdownToken
from pymarkdown.tokens.inline_code_span_markdown_token import (
    InlineCodeSpanMarkdownToken,
)
from pymarkdown.tokens.link_reference_definition_markdown_token import (
    LinkReferenceDefinitionMarkdownToken,
)
from pymarkdown.tokens.link_start_markdown_token import LinkStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


@dataclass
class FoundReplacement:
    """
    Class containing replacements found.
    """

    found_index: int
    required_capitalization: str
    part_context: str


class RuleMd044(RulePlugin):
    """
    Class to implement a plugin that ensures that specific proper names have
    the correct capitalization.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__proper_name_list: List[str] = []
        self.__check_in_code_blocks: bool = False
        self.__check_in_code_spans: bool = False
        self.__is_in_code_block: bool = False
        self.__names: str = ""
        self.__replacement_items: List[FoundReplacement] = []

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="proper-names",
            plugin_id="MD044",
            plugin_enabled_by_default=True,
            plugin_description="Proper names should have the correct capitalization",
            plugin_version="0.7.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md044.md",
            plugin_configuration="names,code_blocks",
            plugin_supports_fix=True,
            plugin_fix_level=2,
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
        self.__check_in_code_blocks = (
            self.plugin_configuration.get_boolean_property_with_default(
                "code_blocks", True
            )
        )
        self.__check_in_code_spans = (
            self.plugin_configuration.get_boolean_property_with_default(
                "code_spans", True
            )
        )
        self.__proper_name_list = []
        self.__names = self.plugin_configuration.get_string_property_with_default(
            "names",
            "",
        ).strip(" ")
        if self.__names:
            lower_list: List[str] = []
            for next_name in self.__names.split(","):
                next_name = next_name.strip(" ")
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

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("code_blocks", self.__check_in_code_blocks),
            QueryConfigItem("code_spans", self.__check_in_code_spans),
            QueryConfigItem("names", self.__names),
        ]

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
        part_context: str,
    ) -> None:
        original_found_text = original_source[
            found_index : found_index + len(required_capitalization)
        ]
        after_found_index = found_index + len(required_capitalization)

        is_character_before_match = (
            original_source[found_index - 1].isalnum() if found_index > 0 else False
        )
        is_character_after_match = (
            original_source[after_found_index].isalnum()
            if after_found_index < len(original_source)
            else False
        )
        if (
            not is_character_after_match
            and not is_character_before_match
            and original_found_text != required_capitalization
        ):
            assert len(original_found_text) == len(required_capitalization)
            if context.in_fix_mode:
                # d1 = max(0,found_index-5)
                # d2 = min(len(original_source), found_index+5)
                # dd  = original_source[d1:d2]
                self.__replacement_items.append(
                    FoundReplacement(found_index, required_capitalization, part_context)
                )
            else:
                extra_data = f"Expected: {required_capitalization}; Actual: {original_found_text}"
                self.report_next_token_error(
                    context,
                    token,
                    extra_error_information=extra_data,
                    line_number_delta=line_adjust + context.calc_pragma_offset(token, line_adjust),
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
        part_context: str,
    ) -> None:
        col_adjust, line_adjust = ParserHelper.adjust_for_newlines(
            string_to_check_lower, search_start, found_index
        )
        if line_adjust == 0 and start_y_offset == 0:
            assert col_adjust >= 0
            col_adjust -= same_line_offset
            assert same_line_offset <= 0
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
            part_context,
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
        part_context: str = "",
        keep_text_with_markers: bool = False,
    ) -> None:
        if not keep_text_with_markers:
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
                    part_context,
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
        part_context: str,
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
            part_context,
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
            same_line_offset = -(len(full_link_text))
            assert link_token.active_link_title is not None
            self.__adjust_for_newlines_and_search(
                context,
                link_token,
                link_body,
                full_link_text,
                link_token.active_link_title,
                same_line_offset,
                "x",
            )

    def __handle_inline_link_fix(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        link_token = cast(LinkStartMarkdownToken, token)
        assert link_token.link_title is not None
        self.__search_for_matches(
            link_token.link_title, context, token, 0, part_context="link_title"
        )
        self.__search_for_matches(
            link_token.text_from_blocks,
            context,
            token,
            0,
            part_context="text_from_blocks",
        )
        if (
            link_token.label_type == Constants.link_type__inline
            and link_token.pre_link_title
        ):
            self.__search_for_matches(
                link_token.pre_link_title,
                context,
                token,
                0,
                part_context="pre_link_title",
            )

    def __handle_inline_image(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:  # sourcery skip: extract-method
        link_token = cast(LinkStartMarkdownToken, token)
        same_line_offset = -2
        self.__search_for_matches(
            link_token.text_from_blocks, context, token, same_line_offset
        )

        if (
            link_token.label_type == Constants.link_type__inline
            and not context.in_fix_mode
        ):
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
            same_line_offset = -(len(full_link_text))
            assert link_token.active_link_title is not None
            self.__adjust_for_newlines_and_search(
                context,
                token,
                link_body,
                full_link_text,
                link_token.active_link_title,
                same_line_offset,
                "y",
            )
        elif context.in_fix_mode:
            image_token = cast(ImageStartMarkdownToken, token)
            assert image_token.link_title is not None
            self.__search_for_matches(
                image_token.link_title, context, token, 0, part_context="link_title"
            )
            self.__search_for_matches(
                image_token.text_from_blocks,
                context,
                token,
                0,
                part_context="text_from_blocks",
            )

    def __handle_link_reference_definition(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        lrd_token = cast(LinkReferenceDefinitionMarkdownToken, token)
        link_name = lrd_token.link_name_debug or lrd_token.link_name
        same_line_offset = -1
        if context.in_fix_mode:
            if lrd_token.link_name_debug:
                self.__search_for_matches(
                    lrd_token.link_name_debug,
                    context,
                    token,
                    same_line_offset,
                    part_context="link_name_debug",
                )
            self.__search_for_matches(
                lrd_token.link_name,
                context,
                token,
                same_line_offset,
                part_context="link_name",
            )
        else:
            self.__search_for_matches(
                link_name, context, token, same_line_offset, part_context="link_name"
            )

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
        if context.in_fix_mode:
            self.__adjust_for_newlines_and_search(
                context,
                token,
                full_link_text,
                full_link_text,
                lrd_token.link_title_raw,
                same_line_offset,
                "link_title_raw",
            )
            if lrd_token.link_title:
                self.__adjust_for_newlines_and_search(
                    context,
                    token,
                    full_link_text,
                    full_link_text,
                    lrd_token.link_title,
                    same_line_offset,
                    "link_title",
                )
        else:
            self.__adjust_for_newlines_and_search(
                context,
                token,
                full_link_text,
                full_link_text,
                lrd_token.link_title_raw,
                same_line_offset,
                "link_title_raw",
            )

    def __handle_inline_code_span(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        if not self.__check_in_code_spans:
            return
        code_span_token = cast(InlineCodeSpanMarkdownToken, token)
        same_line_offset = -(
            len(code_span_token.extracted_start_backticks)
            + len(code_span_token.leading_whitespace)
        )
        self.__search_for_matches(
            code_span_token.span_text,
            context,
            token,
            same_line_offset,
            keep_text_with_markers=context.in_fix_mode,
        )

    def __handle_text(self, context: PluginScanContext, token: MarkdownToken) -> None:
        text_token = cast(TextMarkdownToken, token)
        if not self.__is_in_code_block or self.__check_in_code_blocks:
            self.__search_for_matches(
                text_token.token_text,
                context,
                token,
                keep_text_with_markers=context.in_fix_mode,
            )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if not self.__proper_name_list:
            return
        self.__replacement_items.clear()
        if token.is_text:
            self.__handle_text(context, token)
        elif token.is_inline_code_span:
            self.__handle_inline_code_span(context, token)
        elif token.is_inline_link_end and not context.in_fix_mode:
            self.__handle_inline_link_end(context, token)
        elif token.is_inline_image:
            self.__handle_inline_image(context, token)
        elif token.is_link_reference_definition:
            self.__handle_link_reference_definition(context, token)
        elif token.is_code_block:
            self.__is_in_code_block = True
        elif token.is_code_block_end:
            self.__is_in_code_block = False
        elif context.in_fix_mode:
            if token.is_inline_link:
                self.__handle_inline_link_fix(context, token)

        if self.__replacement_items:
            self.__apply_replacement_items(context, token)

    def __apply_replacement_items(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        if token.is_text:
            text_token = cast(TextMarkdownToken, token)
            self.__apply_normal_replacement(
                context, token, text_token.token_text, "token_text"
            )
        elif token.is_inline_code_span:
            code_span_token = cast(InlineCodeSpanMarkdownToken, token)
            self.__apply_normal_replacement(
                context, token, code_span_token.span_text, "span_text"
            )
        elif token.is_link_reference_definition:
            lrd_token = cast(LinkReferenceDefinitionMarkdownToken, token)
            self.__apply_matching_replacement(
                context, token, lrd_token.link_name, "link_name"
            )
            if lrd_token.link_name_debug:
                self.__apply_matching_replacement(
                    context, token, lrd_token.link_name_debug, "link_name_debug"
                )
            self.__apply_matching_replacement(
                context, token, lrd_token.link_title_raw, "link_title_raw"
            )
            if lrd_token.link_title:
                self.__apply_matching_replacement(
                    context, token, lrd_token.link_title, "link_title"
                )
        elif token.is_inline_link:
            link_token = cast(LinkStartMarkdownToken, token)
            self.__apply_matching_replacement(
                context, token, link_token.link_title, "link_title"
            )
            self.__apply_matching_replacement(
                context, token, link_token.pre_link_title, "pre_link_title"
            )
            self.__apply_matching_replacement(
                context, token, link_token.text_from_blocks, "text_from_blocks"
            )
        else:
            assert (
                token.is_inline_image
            ), "If not anything else, must be an inline image."
            image_token = cast(ImageStartMarkdownToken, token)
            self.__apply_matching_replacement(
                context, token, image_token.link_title, "link_title"
            )
            self.__apply_matching_replacement(
                context, token, image_token.text_from_blocks, "text_from_blocks"
            )

    def __apply_normal_replacement(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        text_to_check: Optional[str],
        name_to_check: str,
    ) -> None:
        assert text_to_check is not None
        new_text = text_to_check
        for replacement_item in self.__replacement_items:
            new_text = (
                new_text[: replacement_item.found_index]
                + replacement_item.required_capitalization
                + new_text[
                    replacement_item.found_index
                    + len(replacement_item.required_capitalization) :
                ]
            )
        assert new_text != text_to_check, "The new text must always be different."
        self.register_fix_token_request(
            context, token, "next_token", name_to_check, new_text
        )

    def __apply_matching_replacement(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        text_to_check: Optional[str],
        name_to_check: str,
    ) -> None:
        assert text_to_check is not None
        new_text = text_to_check
        for replacement_item in self.__replacement_items:
            if replacement_item.part_context == name_to_check:
                new_text = (
                    new_text[: replacement_item.found_index]
                    + replacement_item.required_capitalization
                    + new_text[
                        replacement_item.found_index
                        + len(replacement_item.required_capitalization) :
                    ]
                )
        if new_text != text_to_check:
            self.register_fix_token_request(
                context, token, "next_token", name_to_check, new_text
            )
