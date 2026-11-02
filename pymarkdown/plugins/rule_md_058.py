"""
Module to implement a plugin that looks for tables that are not surrounded by
blank lines.
"""

from typing import Dict, Optional

from pymarkdown.plugin_manager.plugin_details import PluginDetailsV3
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
        self.__in_html_block = False
        self.__last_table_line_number = 0
        self.__lines_to_fix: Dict[int, bool] = {}

    def get_details(self) -> PluginDetailsV3:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="blanks-around-tables",
            plugin_id="MD058",
            plugin_enabled_by_default=True,
            plugin_description="Tables should be surrounded by blank lines",
            plugin_version="0.5.1",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md058.md",
            plugin_supports_fix=True,
            plugin_fix_level=0,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__previous_token = None
        self.__last_row_token = None
        self.__awaiting_below = False
        self.__in_html_block = False
        self.__last_table_line_number = 0
        self.__lines_to_fix = {}

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
        fix_line_number: int,
        insert_below: bool,
    ) -> None:
        if not context.in_fix_mode:
            self.report_next_token_error(context, error_token)
            return
        # The blank line is inserted during the line pass, by copying the
        # container prefix (any `>` characters) of the table's own line, so
        # tables inside block quotes and list items are fixed the same way as
        # top-level ones.  A table the parser left inside an HTML block is
        # skipped: by CommonMark those lines belong to the HTML block, and a
        # blank line would turn them into a real table.
        if (
            context.is_during_line_pass
            and not self.__in_html_block
            and not context.check_for_pragma_suppression(
                error_token.line_number, "MD058", False
            )
        ):
            self.__lines_to_fix[fix_line_number] = insert_below

    def next_line(self, context: PluginScanContext, line: str) -> None:
        """
        Event that a new line is being processed.
        """
        insert_below = self.__lines_to_fix.get(context.line_number)
        if insert_below is None:
            return
        blank_line = line[: len(line) - len(line.lstrip(" \t>"))].rstrip()
        context.set_current_fix_line(
            f"{line}\n{blank_line}" if insert_below else f"{blank_line}\n{line}"
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
                self.__report_or_fix(
                    context,
                    self.__last_row_token,
                    self.__last_table_line_number,
                    True,
                )
            self.__awaiting_below = False

        if token.is_html_block:
            self.__in_html_block = True
        elif token.is_html_block_end:
            self.__in_html_block = False

        if token.is_table:
            if not self.__is_clear_above(self.__previous_token):
                self.__report_or_fix(context, token, token.line_number, False)
            self.__last_row_token = token
        elif token.is_table_header or token.is_table_row:
            self.__last_row_token = token
            # The delimiter row has no token of its own; it follows the header.
            self.__last_table_line_number = token.line_number + (
                1 if token.is_table_header else 0
            )
        elif token.is_table_end:
            self.__awaiting_below = True

        # A blank line at the end of a container is emitted before the token that
        # closes that container, so those closing tokens are skipped over to find
        # the token that actually precedes the table.
        if not token.is_container_end_token:
            self.__previous_token = token
