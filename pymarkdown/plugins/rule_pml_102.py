"""
Module to implement a plugin that
"""

from typing import List, Optional, cast

from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2, PluginDetailsV3
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.plugins.utils.container_token_manager import ContainerTokenManager
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken


class RulePml102(RulePlugin):
    """
    Class to implement a plugin that
    """

    def __init__(self) -> None:
        super().__init__()
        self.__container_manager = ContainerTokenManager()

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="disallow-lazy-list-indentation",
            plugin_id="PML102",
            plugin_enabled_by_default=False,
            plugin_description="Disallows lazy list indentation",
            plugin_version="0.5.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_pml102.md",
            plugin_supports_fix=False,
            plugin_fix_level=0,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__container_manager.clear()

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        self.__container_manager.premanage_container_tokens(token)

        if self.__container_manager.container_token_stack and token.is_paragraph:
            self.__check(context, token)

        self.__container_manager.manage_container_tokens(token)

    def __check(self, context: PluginScanContext, token: MarkdownToken) -> None:
        if self.__container_manager.container_token_stack[-1].is_block_quote_start:
            return

        top_list_token = cast(
            ListStartMarkdownToken, self.__container_manager.container_token_stack[-1]
        )
        current_paragraph_token = cast(ParagraphMarkdownToken, token)

        # if we do not have a multi-line paragraph, then we cannot have a lazy indent
        split_para_whitespace = current_paragraph_token.extracted_whitespace.split("\n")
        if len(split_para_whitespace) == 1:
            return

        # if we do not have leading spaces for the list, then we cannot have a lazy indent
        assert top_list_token.leading_spaces is not None
        split_list_whitespace = top_list_token.leading_spaces.split("\n")

        # self.__container_manager.get
        latest_block_quote_from_stack = None
        token_stack_index = len(self.__container_manager.container_token_stack) - 1
        ori_token_stack_index = token_stack_index + 1
        while token_stack_index >= 0:
            current_block_quote = self.__container_manager.container_token_stack[
                token_stack_index
            ]
            if current_block_quote.is_block_quote_start:
                latest_block_quote_from_stack = current_block_quote
                break
            token_stack_index -= 1

        list_adjust_value = self.__container_manager.list_adjust_map[
            ori_token_stack_index
        ]
        para_start_delta = (
            current_paragraph_token.line_number
            - top_list_token.line_number
            - (list_adjust_value - 1)
        )
        if list_adjust_value == 1:
            list_indent = top_list_token.indent_level
        else:
            assert top_list_token.last_new_list_token is not None
            list_indent = top_list_token.last_new_list_token.indent_level

        self.__xx(
            context,
            top_list_token,
            para_start_delta,
            split_para_whitespace,
            split_list_whitespace,
            latest_block_quote_from_stack,
            current_paragraph_token,
            list_indent,
            list_adjust_value,
            token_stack_index,
        )

        # never worry about it for the first line in a paragraph, as by definition, it cannot be continuing

    # pylint: disable=too-many-arguments,too-many-locals

    def __xx(
        self,
        context: PluginScanContext,
        top_list_token: ListStartMarkdownToken,
        para_start_delta: int,
        split_para_whitespace: List[str],
        split_list_whitespace: List[str],
        latest_block_quote_from_stack: Optional[MarkdownToken],
        current_paragraph_token: ParagraphMarkdownToken,
        list_indent: int,
        list_adjust_value: int,
        token_stack_index: int,
    ) -> None:
        paragraph_line_index = 1
        list_start_index = para_start_delta
        while paragraph_line_index < len(split_para_whitespace):
            split_para_ws = split_para_whitespace[paragraph_line_index]
            split_ws = len(split_list_whitespace[list_start_index])
            if latest_block_quote_from_stack:
                latest_block_stack = cast(
                    BlockQuoteMarkdownToken, latest_block_quote_from_stack
                )
                assert latest_block_stack.bleading_spaces is not None
                split_bleading_spaces = latest_block_stack.bleading_spaces.split("\n")
                split_bleading_spaces_index = (
                    current_paragraph_token.line_number
                    - latest_block_quote_from_stack.line_number
                    + paragraph_line_index
                    - self.__container_manager.bq_close_map.get(token_stack_index, 0)
                )
                split_ws_adjust = len(
                    split_bleading_spaces[split_bleading_spaces_index]
                )
                split_ws += split_ws_adjust
            if split_ws < list_indent:
                lnd = list_start_index + 1 + (list_adjust_value - 1)
                cnd = -(
                    split_ws + len(split_para_ws) + 1
                )  # maybe more for higher indented levels and bqs
                extra_data = (
                    f"Expected: {list_indent}; Actual: {split_ws + len(split_para_ws)}"
                )

                self.report_next_token_error(
                    context,
                    top_list_token,
                    extra_error_information=extra_data,
                    line_number_delta=lnd,
                    column_number_delta=cnd,
                )
            paragraph_line_index += 1


# pylint: enable=too-many-arguments,too-many-locals
