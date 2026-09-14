"""
Module to implement a plugin that looks for table rows whose column count
does not match the table's header row.
"""

import re
from typing import cast

from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.table_markdown_tokens import TableMarkdownRowToken


class RuleMd056(RulePlugin):
    """
    Class to implement a plugin that looks for table rows whose column count
    does not match the table's header row.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__header_item_count = 0

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="table-column-count",
            plugin_id="MD056",
            plugin_enabled_by_default=True,
            plugin_description="Table column count",
            plugin_version="0.5.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md056.md",
            plugin_supports_fix=False,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__header_item_count = 0

    # Matches a "|" cell divider that is not backslash-escaped.
    __unescaped_pipe = re.compile(r"(?<!\\)\|")

    @classmethod
    def __count_excess_cells(cls, excess_text: str) -> int:
        # Excess columns are folded into the row-end token as
        # "{leading}{text}{trailing}" per column, separated by "|" dividers,
        # with a trailing "|" only if the source row ended with one. Split on
        # unescaped dividers (an escaped "\|" stays inside its cell); the
        # final segment is empty/blank only when a trailing divider was
        # present, otherwise it is the last cell's content.
        # ponytail: handles "\|" but not "\\|" (escaped backslash before a
        # real divider); the upgrade path is exposing the parser's
        # excess-column count on the token if that ever matters.
        segments = cls.__unescaped_pipe.split(excess_text.rstrip())
        divider_count = len(segments) - 1
        return divider_count if not segments[-1].strip() else divider_count + 1

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_table:
            self.__header_item_count = 0
        elif token.is_table_header_item:
            self.__header_item_count += 1
        elif token.is_table_row:
            row_token = cast(TableMarkdownRowToken, token)
            if row_token.delta > 0:
                actual = self.__header_item_count - row_token.delta
                self.report_next_token_error(
                    context,
                    token,
                    extra_error_information=(
                        f"Expected: {self.__header_item_count}; "
                        f"Actual: {actual}; "
                        "Too few cells, row will be missing data"
                    ),
                )
        elif isinstance(token, EndMarkdownToken):
            if token.start_markdown_token.is_table_row and token.extracted_whitespace:
                actual = self.__header_item_count + self.__count_excess_cells(
                    token.extracted_whitespace
                )
                self.report_next_token_error(
                    context,
                    token.start_markdown_token,
                    extra_error_information=(
                        f"Expected: {self.__header_item_count}; "
                        f"Actual: {actual}; "
                        "Too many cells, extra data will be missing"
                    ),
                )
