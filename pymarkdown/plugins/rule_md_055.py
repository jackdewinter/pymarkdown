"""
Module to implement a plugin that looks for inconsistent use of leading and
trailing pipe characters in the rows of a table.
"""

import re
from typing import List, Optional, cast

from pymarkdown.plugin_manager.plugin_details import PluginDetailsV3, QueryConfigItem
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.table_markdown_tokens import (
    TableMarkdownHeaderToken,
    TableMarkdownRowToken,
)


class RuleMd055(RulePlugin):
    """
    Class to implement a plugin that looks for inconsistent use of leading and
    trailing pipe characters in the rows of a table.
    """

    __valid_styles = [
        "consistent",
        "leading_and_trailing",
        "leading_only",
        "no_leading_or_trailing",
        "trailing_only",
    ]
    # Matches a "|" cell divider that is not backslash-escaped.
    __unescaped_pipe = re.compile(r"(?<!\\)\|")
    # Matches an unescaped trailing "|" divider (ignoring trailing whitespace).
    __trailing_pipe = re.compile(r"(?<!\\)\|\s*$")

    def __init__(self) -> None:
        super().__init__()
        self.__style = "consistent"
        self.__expected_leading: Optional[bool] = None
        self.__expected_trailing: Optional[bool] = None
        self.__expected_style = "consistent"
        self.__row_leading = False
        self.__row_token: Optional[MarkdownToken] = None
        self.__last_item_whitespace = ""

    def get_details(self) -> PluginDetailsV3:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="table-pipe-style",
            plugin_id="MD055",
            plugin_enabled_by_default=True,
            plugin_description="Table pipe style",
            plugin_version="0.5.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md055.md",
            plugin_supports_fix=False,
            plugin_configuration="style",
        )

    @classmethod
    def __validate_style(cls, found_value: str) -> None:
        if found_value not in cls.__valid_styles:
            raise ValueError(f"Allowable values: {cls.__valid_styles}")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__style = self.plugin_configuration.get_string_property_with_default(
            "style",
            "consistent",
            valid_value_fn=RuleMd055.__validate_style,
        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [QueryConfigItem("style", self.__style)]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        if self.__style == "consistent":
            self.__expected_leading = None
            self.__expected_trailing = None
            self.__expected_style = "consistent"
        else:
            self.__expected_style = self.__style
            self.__expected_leading = self.__style not in (
                "no_leading_or_trailing",
                "trailing_only",
            )
            self.__expected_trailing = self.__style not in (
                "no_leading_or_trailing",
                "leading_only",
            )
        self.__row_token = None
        self.__last_item_whitespace = ""

    @staticmethod
    def __style_name(leading: bool, trailing: bool) -> str:
        if leading:
            return "leading_and_trailing" if trailing else "leading_only"
        return "trailing_only" if trailing else "no_leading_or_trailing"

    def __report(
        self,
        context: PluginScanContext,
        actual_style: str,
        detail: str,
        line_delta: int,
    ) -> None:
        assert self.__row_token is not None
        self.report_next_token_error(
            context,
            self.__row_token,
            line_number_delta=line_delta,
            extra_error_information=(
                f"Expected: {self.__expected_style}; Actual: {actual_style}; {detail}"
            ),
        )

    def __check_row(
        self,
        context: PluginScanContext,
        leading: bool,
        trailing: bool,
        line_delta: int = 0,
    ) -> None:
        actual_style = self.__style_name(leading, trailing)
        if self.__expected_leading is None:
            self.__expected_leading = leading
            self.__expected_trailing = trailing
            self.__expected_style = actual_style
            return
        assert self.__expected_trailing is not None
        if leading != self.__expected_leading:
            verb = "Missing" if self.__expected_leading else "Unexpected"
            self.__report(context, actual_style, f"{verb} leading pipe", line_delta)
        if trailing != self.__expected_trailing:
            verb = "Missing" if self.__expected_trailing else "Unexpected"
            self.__report(context, actual_style, f"{verb} trailing pipe", line_delta)

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_table_header:
            header_token = cast(TableMarkdownHeaderToken, token)
            self.__row_leading = header_token.did_header_row_start_with_separator
            self.__row_token = token
            self.__last_item_whitespace = ""
        elif token.is_table_row:
            row_token = cast(TableMarkdownRowToken, token)
            self.__row_leading = row_token.did_start_with_separator
            self.__row_token = token
            self.__last_item_whitespace = ""
        elif isinstance(token, EndMarkdownToken):
            start_token = token.start_markdown_token
            if start_token.is_table_header_item or start_token.is_table_row_item:
                self.__last_item_whitespace = token.extracted_whitespace
            elif start_token.is_table_header or start_token.is_table_row:
                # An over-full row emits item tokens only up to the header column
                # count and folds the excess cells (including the real row
                # terminator) into the end token's whitespace. When that is
                # present it carries the true trailing pipe; otherwise the last
                # emitted item's whitespace does.
                excess = token.extracted_whitespace
                if excess:
                    trailing = bool(self.__trailing_pipe.search(excess))
                else:
                    trailing = bool(
                        self.__unescaped_pipe.search(self.__last_item_whitespace)
                    )
                self.__check_row(context, self.__row_leading, trailing)
                if start_token.is_table_header:
                    # The delimiter row is not its own token; its pipe style is
                    # encoded in the header token's separator_line. Check it as a
                    # row in its own right (it sits one line below the header).
                    # ponytail: separator_line never contains escaped pipes, so a
                    # plain strip/startswith is enough; full per-cell column
                    # precision would need parser support.
                    separator = cast(
                        TableMarkdownHeaderToken, start_token
                    ).separator_line
                    self.__check_row(
                        context,
                        separator.lstrip().startswith("|"),
                        separator.rstrip().endswith("|"),
                        line_delta=1,
                    )
