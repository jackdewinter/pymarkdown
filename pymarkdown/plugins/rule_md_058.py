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

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        # A table that just closed needs a blank line (or the end of the file)
        # immediately after it; this token is whatever follows the table.
        if self.__awaiting_below:
            if not (token.is_blank_line or token.is_end_of_stream):
                assert self.__last_row_token is not None
                self.report_next_token_error(context, self.__last_row_token)
            self.__awaiting_below = False

        if token.is_table:
            # The table must be preceded by a blank line or the start of the file.
            if (
                self.__previous_token is not None
                and not self.__previous_token.is_blank_line
            ):
                self.report_next_token_error(context, token)
            self.__last_row_token = token
        elif token.is_table_header or token.is_table_row:
            self.__last_row_token = token
        elif token.is_table_end:
            self.__awaiting_below = True

        self.__previous_token = token
