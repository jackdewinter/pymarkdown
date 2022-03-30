"""
Module to implement a plugin that looks for fenced code blocks without a language specified.
"""
from typing import cast

from pymarkdown.leaf_markdown_token import FencedCodeBlockMarkdownToken
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class RuleMd040(RulePlugin):
    """
    Class to implement a plugin that looks for fenced code blocks without a language specified.
    """

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="fenced-code-language",
            plugin_id="MD040",
            plugin_enabled_by_default=True,
            plugin_description="Fenced code blocks should have a language specified",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md040.md",
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_fenced_code_block:
            fenced_token = cast(FencedCodeBlockMarkdownToken, token)
            if not fenced_token.extracted_text.strip():
                self.report_next_token_error(context, token)
