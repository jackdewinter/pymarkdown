"""
Module to implement a plugin that looks for tables that are not surrounded by
blank lines.
"""

import copy
from typing import Optional

from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.blank_line_markdown_token import BlankLineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd058(RulePlugin):
    """
    Class to implement a plugin that looks for tables that are not surrounded by
    blank lines.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__previous_token: Optional[MarkdownToken] = None
        self.__last_row_token: Optional[MarkdownToken] = None
        self.__awaiting_below = False
        self.__container_depth = 0
        self.__table_is_fixable = False
        self.__fix_count = 0

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="blanks-around-tables",
            plugin_id="MD058",
            plugin_enabled_by_default=True,
            plugin_description="Tables should be surrounded by blank lines",
            plugin_version="0.5.1",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md058.md",
            plugin_supports_fix=True,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__previous_token = None
        self.__last_row_token = None
        self.__awaiting_below = False
        self.__container_depth = 0
        self.__table_is_fixable = False
        self.__fix_count = 0

    @staticmethod
    def __is_clear_above(previous_token: Optional[MarkdownToken]) -> bool:
        # The start of the file, a blank line, or the opening of a containing
        # block quote / list item all satisfy the "blank line above" rule.
        return (
            previous_token is None
            or previous_token.is_blank_line
            or previous_token.is_block_quote_start
            or previous_token.is_list_start
            or previous_token.is_new_list_item
        )

    @staticmethod
    def __is_clear_below(token: MarkdownToken) -> bool:
        # A blank line, the end of the file, or the close of a containing block
        # quote / list all satisfy the "blank line below" rule.
        return (
            token.is_blank_line
            or token.is_end_of_stream
            or token.is_block_quote_end
            or token.is_list_end
        )

    def __report_or_fix(
        self,
        context: PluginScanContext,
        error_token: MarkdownToken,
        insert_before_token: MarkdownToken,
    ) -> None:
        if not context.in_fix_mode:
            self.report_next_token_error(context, error_token)
            return
        # ponytail: only document-root tables are fixed; tables inside block
        # quotes / lists need container-prefix handling (see MD031) and are left
        # for a follow-up.
        if (
            context.is_during_line_pass
            or not self.__table_is_fixable
            or context.check_for_pragma_suppression(
                error_token.line_number, "MD058", False
            )
        ):
            return
        new_token = copy.deepcopy(insert_before_token)
        self.__fix_count += 1
        new_token.adjust_line_number(context, self.__fix_count)
        replacement_tokens = [
            BlankLineMarkdownToken(
                extracted_whitespace="",
                position_marker=PositionMarker(new_token.line_number - 1, 0, ""),
                column_delta=1,
            ),
            new_token,
        ]
        self.register_replace_tokens_request(
            context, insert_before_token, insert_before_token, replacement_tokens
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        # A table that just closed needs a blank line (or the end of the file /
        # containing block) immediately after it; this token is whatever
        # follows the table.
        if self.__awaiting_below:
            if not self.__is_clear_below(token):
                assert self.__last_row_token is not None
                self.__report_or_fix(context, self.__last_row_token, token)
            self.__awaiting_below = False

        if token.is_block_quote_start or token.is_list_start:
            self.__container_depth += 1
        elif token.is_block_quote_end or token.is_list_end:
            self.__container_depth -= 1

        if token.is_table:
            self.__table_is_fixable = self.__container_depth == 0
            if not self.__is_clear_above(self.__previous_token):
                self.__report_or_fix(context, token, token)
            self.__last_row_token = token
        elif token.is_table_header or token.is_table_row:
            self.__last_row_token = token
        elif token.is_table_end:
            self.__awaiting_below = True

        # A blank line at the end of a container is emitted before the token that
        # closes that container, so those closing tokens are skipped over to find
        # the token that actually precedes the table.
        if not token.is_container_end_token:
            self.__previous_token = token
