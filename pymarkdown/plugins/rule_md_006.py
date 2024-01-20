"""
Module to implement a plugin that ensures that all Unordered List Items
start at the beginning of the line.
"""
from typing import List, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd006(RulePlugin):
    """
    Class to implement a plugin that ensures that all Unordered List Items
    start at the beginning of the line.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__token_stack: List[MarkdownToken] = []

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="ul-start-left",
            plugin_id="MD006",
            plugin_enabled_by_default=False,
            plugin_description="Consider starting bulleted lists at the beginning of the line",
            plugin_version="0.5.1",
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md006.md",
            plugin_supports_fix=True,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__token_stack = []

    def __calculate_expected_indent(self) -> int:
        expected_indent = 0
        if len(self.__token_stack) > 1:
            if self.__token_stack[-2].is_block_quote_start:
                block_quote_token = cast(
                    BlockQuoteMarkdownToken, self.__token_stack[-2]
                )
                assert block_quote_token.bleading_spaces is not None
                split_spaces = block_quote_token.bleading_spaces.split(
                    ParserHelper.newline_character
                )
                expected_indent = len(split_spaces[0]) + (
                    block_quote_token.column_number - 1
                )
            else:
                list_token = cast(ListStartMarkdownToken, self.__token_stack[-2])
                expected_indent = list_token.indent_level
        return expected_indent

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_list_start or token.is_block_quote_start:
            self.__token_stack.append(token)
            if token.is_unordered_list_start:
                expected_indent = self.__calculate_expected_indent()
                if delta := (1 + expected_indent) - token.column_number:
                    self.__report_or_fix(context, token, delta)
        elif token.is_list_end or token.is_block_quote_end:
            del self.__token_stack[-1]
        elif token.is_new_list_item:
            if self.__token_stack[-1].is_unordered_list_start:
                expected_indent = self.__calculate_expected_indent()
                if delta := (1 + expected_indent) - token.column_number:
                    self.__report_or_fix(context, token, delta)

    def __report_or_fix(
        self, context: PluginScanContext, token: MarkdownToken, adjust_amount: int
    ) -> None:
        if context.in_fix_mode:
            list_start_token = cast(ListStartMarkdownToken, token)
            self.register_fix_token_request(
                context,
                token,
                "next_token",
                "indent_level",
                list_start_token.indent_level + adjust_amount,
            )
            if not token.is_new_list_item:
                self.register_fix_token_request(
                    context, token, "next_token", "extracted_whitespace", ""
                )
                self.register_fix_token_request(
                    context,
                    token,
                    "next_token",
                    "column_number",
                    list_start_token.column_number + adjust_amount,
                )
            else:
                self.register_fix_token_request(
                    context,
                    token,
                    "next_token",
                    "extracted_whitespace",
                    list_start_token.extracted_whitespace[:adjust_amount],
                )
        else:
            self.report_next_token_error(context, token)
