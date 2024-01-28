"""
Module to implement a sample plugin that has a bad next_line function.
"""

from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import MarkdownToken


class BadEndTokens(RulePlugin):
    """
    Class to implement a sample plugin that reports an error on every end token.
    This is used to ensure that the "fixer" can suppress errors when needed.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="bad-end-tokens",
            plugin_id="MDE044",
            plugin_enabled_by_default=True,
            plugin_description="Plugin that triggers on end_tokens.",
            plugin_version="0.0.0",
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new line is being processed.
        """
        if token.is_end_token:
            self.report_next_line_error(context, token.column_number)
