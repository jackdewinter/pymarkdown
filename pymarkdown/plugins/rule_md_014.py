"""
Module to implement a plugin that looks for code blocks for scripts that do not
look right.
"""
from typing import cast

from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.inline_markdown_token import TextMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd014(RulePlugin):
    """
    Class to implement a plugin that looks for code blocks for scripts that do not
    look right.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__in_code_block = False

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="commands-show-output",
            plugin_id="MD014",
            plugin_enabled_by_default=True,
            plugin_description="Dollar signs used before commands without showing output",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md014.md",
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__in_code_block = False

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_code_block:
            self.__in_code_block = True
        elif token.is_code_block_end:
            self.__in_code_block = False
        elif self.__in_code_block and token.is_text:
            text_token = cast(TextMarkdownToken, token)
            split_token_text = text_token.token_text.split(
                ParserHelper.newline_character
            )
            if all(next_line.strip().startswith("$") for next_line in split_token_text):
                self.report_next_token_error(context, token)
