"""
Module to implement a plugin that ensures that nested Unordered List Items
start at predictable positions.
"""
from typing import Dict, List, Optional, Tuple, cast

from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.link_reference_definition_markdown_token import (
    LinkReferenceDefinitionMarkdownToken,
)
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class RuleMd007(RulePlugin):
    """
    Class to implement a plugin that ensures that nested Unordered List Items
    start at predictable positions.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__container_token_stack: List[MarkdownToken] = []
        self.__bq_line_index: Dict[int, int] = {}
        self.__last_leaf_token: Optional[MarkdownToken] = None
        self.__indent_basis = 0
        self.__start_indented = False

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="ul-indent",
            plugin_id="MD007",
            plugin_enabled_by_default=True,
            plugin_description="Unordered list indentation",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md007.md",
            plugin_configuration="indent,start_indented",
        )

    @classmethod
    def __validate_configuration_indent(cls, found_value: int) -> None:
        if found_value < 2 or found_value > 4:
            raise ValueError("Allowable values are between 2 and 4.")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__indent_basis = self.plugin_configuration.get_integer_property(
            "indent",
            default_value=2,
            valid_value_fn=self.__validate_configuration_indent,
        )
        self.__start_indented = self.plugin_configuration.get_boolean_property(
            "start_indented",
            default_value=False,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__container_token_stack = []

        self.__bq_line_index = {}
        self.__last_leaf_token = None

    @classmethod
    def __is_simple_delta(cls, token: MarkdownToken) -> bool:
        return (
            token.is_blank_line
            or token.is_thematic_break
            or token.is_atx_heading
            or token.is_paragraph_end
        )

    @classmethod
    def __is_remember_leaf_token(cls, token: MarkdownToken) -> bool:
        return bool(
            token.is_setext_heading
            or token.is_indented_code_block
            or token.is_html_block
        )

    @classmethod
    def __is_clear_leaf_token(cls, token: MarkdownToken) -> bool:
        return bool(
            token.is_indented_code_block_end
            or token.is_html_block_end
            or token.is_setext_heading_end
            or token.is_fenced_code_block_end
        )

    def __manage_leaf_tokens_text(self, token: MarkdownToken) -> int:
        assert self.__last_leaf_token is not None
        text_token = cast(TextMarkdownToken, token)
        if self.__last_leaf_token.is_setext_heading:
            assert text_token.end_whitespace is not None
            return text_token.end_whitespace.count(ParserHelper.newline_character) + 1
        assert (
            self.__last_leaf_token.is_html_block or self.__last_leaf_token.is_code_block
        )
        return text_token.token_text.count(ParserHelper.newline_character) + 1

    def __manage_leaf_tokens(self, token: MarkdownToken) -> None:
        bq_delta = 0
        if self.__is_simple_delta(token):
            bq_delta = 1
        elif self.__is_remember_leaf_token(token):
            self.__last_leaf_token = token
        elif self.__is_clear_leaf_token(token):
            self.__last_leaf_token = None
            if token.is_setext_heading_end or token.is_fenced_code_block_end:
                bq_delta = 1
        elif token.is_fenced_code_block:
            bq_delta = 1
            self.__last_leaf_token = token
        elif token.is_paragraph:
            paragraph_token = cast(ParagraphMarkdownToken, token)
            bq_delta = paragraph_token.extracted_whitespace.count(
                ParserHelper.newline_character
            )
        elif token.is_link_reference_definition:
            bq_delta = self.__manage_lrd_token(token)
        elif token.is_text and self.__last_leaf_token:
            bq_delta = self.__manage_leaf_tokens_text(token)
        self.__bq_line_index[len(self.__container_token_stack)] += bq_delta

    @classmethod
    def __manage_lrd_token(cls, token: MarkdownToken) -> int:
        lrd_token = cast(LinkReferenceDefinitionMarkdownToken, token)
        assert lrd_token.link_title_raw is not None
        assert lrd_token.link_title_whitespace is not None
        assert lrd_token.link_destination_whitespace is not None
        assert lrd_token.link_name_debug is not None
        return (
            1
            + lrd_token.link_name_debug.count(ParserHelper.newline_character)
            + lrd_token.link_destination_whitespace.count(
                ParserHelper.newline_character
            )
            + lrd_token.link_title_whitespace.count(ParserHelper.newline_character)
            + lrd_token.link_title_raw.count(ParserHelper.newline_character)
        )

    def manage_container_tokens(self, token: MarkdownToken) -> None:
        """
        Manage the container tokens, especially the block quote indices.
        """
        if token.is_block_quote_start:
            self.__container_token_stack.append(token)
            self.__bq_line_index[len(self.__container_token_stack)] = 0
        elif token.is_block_quote_end:
            del self.__bq_line_index[len(self.__container_token_stack)]
            del self.__container_token_stack[-1]
        elif token.is_list_start:
            self.__container_token_stack.append(token)
        elif token.is_list_end:
            del self.__container_token_stack[-1]
        elif (
            self.__container_token_stack
            and self.__container_token_stack[-1].is_block_quote_start
        ):
            self.__manage_leaf_tokens(token)

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        # print(f">>>{token}".replace(ParserHelper.newline_character, "\\n"))
        if token.is_unordered_list_start or (
            token.is_new_list_item
            and self.__container_token_stack[-1].is_unordered_list_start
        ):
            self.__check(context, token)

        self.manage_container_tokens(token)

    def __calculate_base_column_ordered_list(
        self, stack_index: int, ignore_list_starts: bool, container_base_column: int
    ) -> Tuple[bool, int]:
        if not ignore_list_starts:
            list_token = cast(
                ListStartMarkdownToken,
                self.__container_token_stack[stack_index],
            )
            container_base_column += list_token.indent_level
        ignore_list_starts = True
        return ignore_list_starts, container_base_column

    def __calculate_base_column_block_quote(
        self, stack_index: int, container_base_column: int, block_quote_base: int
    ) -> Tuple[bool, int, int]:
        block_quote_token = cast(
            BlockQuoteMarkdownToken,
            self.__container_token_stack[stack_index],
        )
        bq_index = self.__bq_line_index[stack_index + 1]
        assert block_quote_token.bleading_spaces is not None
        split_leading_spaces = block_quote_token.bleading_spaces.split(
            ParserHelper.newline_character
        )
        # print(f"bq_index={bq_index},split_leading_spaces={split_leading_spaces}")
        # print(f"split_leading_spaces[bq_index]={split_leading_spaces[bq_index]}=")
        if not block_quote_base:
            block_quote_base = container_base_column + len(
                split_leading_spaces[bq_index]
            )
        container_base_column += len(split_leading_spaces[bq_index])
        ignore_list_starts = False
        return ignore_list_starts, container_base_column, block_quote_base

    def __calculate_base_column(self) -> Tuple[int, int, int]:
        container_base_column = 0
        block_quote_base = 0
        list_depth = 0
        if self.__container_token_stack:
            stack_index = len(self.__container_token_stack) - 1
            while (
                stack_index >= 0
                and self.__container_token_stack[stack_index].is_unordered_list_start
            ):
                list_depth += 1
                stack_index -= 1
            # print(f"stack_index={stack_index}")
            ignore_list_starts = False
            while stack_index >= 0:
                # print(f"stack_index>{stack_index}," + \
                #   f"token={self.__container_token_stack[stack_index]}".replace(ParserHelper.newline_character, "\\n"))
                if self.__container_token_stack[stack_index].is_ordered_list_start:
                    (
                        ignore_list_starts,
                        container_base_column,
                    ) = self.__calculate_base_column_ordered_list(
                        stack_index, ignore_list_starts, container_base_column
                    )
                elif self.__container_token_stack[stack_index].is_block_quote_start:
                    (
                        ignore_list_starts,
                        container_base_column,
                        block_quote_base,
                    ) = self.__calculate_base_column_block_quote(
                        stack_index, container_base_column, block_quote_base
                    )
                # print(f"container_base_column>{container_base_column}")
                stack_index -= 1
        return container_base_column, block_quote_base, list_depth

    def __check(self, context: PluginScanContext, token: MarkdownToken) -> None:
        # print(f"{token}".replace(ParserHelper.newline_character, "\\n"))
        # print(f"{self.__container_token_stack}".replace(ParserHelper.newline_character, "\\n"))
        # print(f"{self.__bq_line_index}".replace(ParserHelper.newline_character, "\\n"))

        (
            container_base_column,
            block_quote_base,
            list_depth,
        ) = self.__calculate_base_column()
        # print(f"container_base_column={container_base_column}, block_quote_base={block_quote_base}, list_depth={list_depth}")

        # print(f"list_depth={list_depth}")
        if token.is_new_list_item:
            # print(f"list_depth={list_depth}")
            list_depth -= 1

        if self.__start_indented:
            # print(f"list_depth={list_depth}")
            list_depth += 1

        adjusted_column_number = token.column_number - 1 - container_base_column
        # print(f"adjusted_column_number={adjusted_column_number} = token.column_number({token.column_number}) -1 -container_base_column={container_base_column}")
        calculated_column_number = list_depth * self.__indent_basis
        # print(f"adjusted_column_number={adjusted_column_number}, calculated_column_number=" + \
        #   f"{calculated_column_number},block_quote_base={block_quote_base}")
        if adjusted_column_number != calculated_column_number:
            # print(f"container_base_column={container_base_column}")
            if block_quote_base:
                container_base_column -= block_quote_base
            elif container_base_column:
                container_base_column += 1
            extra_error_information = (
                f"Expected: {calculated_column_number+container_base_column}, "
                + f"Actual={adjusted_column_number+container_base_column}"
            )
            self.report_next_token_error(
                context, token, extra_error_information=extra_error_information
            )
