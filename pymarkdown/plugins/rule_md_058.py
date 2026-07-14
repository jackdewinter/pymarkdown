"""
Module to implement a plugin that looks for tables that are not surrounded by
blank lines.
"""

from typing import Optional

from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
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

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="blanks-around-tables",
            plugin_id="MD058",
            plugin_enabled_by_default=True,
            plugin_description="Tables should be surrounded by blank lines",
            plugin_version="0.5.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md058.md",
            plugin_supports_fix=False,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__previous_token = None
        self.__last_row_token = None
        self.__awaiting_below = False

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
                self.report_next_token_error(context, self.__last_row_token)
            self.__awaiting_below = False

        if token.is_table:
            if not self.__is_clear_above(self.__previous_token):
                self.report_next_token_error(context, token)
            self.__last_row_token = token
        elif token.is_table_header or token.is_table_row:
            self.__last_row_token = token
        elif token.is_table_end:
            self.__awaiting_below = True

        self.__previous_token = token
