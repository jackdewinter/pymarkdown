"""
Module to implement a plugin that looks for text sequences that make
it appear like the author got the inline link syntax reversed.
"""
import re
from typing import List

from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd011(RulePlugin):
    """
    Class to implement a plugin that looks for text sequences that make
    it appear like the author got the inline link syntax reversed.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__reverse_link_syntax = re.compile(r"\(.*\)\[\s*[^\^].*\s*]")
        self.__leaf_tokens: List[MarkdownToken] = []
        self.__line_index = 0
        self.__leaf_token_index = 0

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-reversed-links",
            plugin_id="MD011",
            plugin_enabled_by_default=True,
            plugin_description="Reversed link syntax",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md011.md",
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__leaf_tokens = []
        self.__line_index = 1
        self.__leaf_token_index = 0

    def next_line(self, context: PluginScanContext, line: str) -> None:
        """
        Event that a new line is being processed.
        """
        if (
            self.__leaf_token_index + 1 < len(self.__leaf_tokens)
            and self.__line_index
            == self.__leaf_tokens[self.__leaf_token_index + 1].line_number
        ):
            self.__leaf_token_index += 1

        if (
            not self.__leaf_tokens[self.__leaf_token_index].is_code_block
            and not self.__leaf_tokens[self.__leaf_token_index].is_html_block
            and line
            and "(" in line
            and "[" in line
        ):
            if regex_search := self.__reverse_link_syntax.search(line):
                regex_span = regex_search.span()
                extra_error_information = line[regex_span[0] : regex_span[1]]
                self.report_next_line_error(
                    context,
                    regex_span[0] + 1,
                    extra_error_information=extra_error_information,
                )

        self.__line_index += 1

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        _ = context
        if token.is_blank_line or token.is_leaf:
            self.__leaf_tokens.append(token)
