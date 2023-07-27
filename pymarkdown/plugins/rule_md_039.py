"""
Module to implement a plugin that looks for spaces within link labels.
"""
from typing import cast

from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.inline_markdown_token import LinkStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd039(RulePlugin):
    """
    Class to implement a plugin that looks for spaces within link labels.
    """

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-space-in-links",
            plugin_id="MD039",
            plugin_enabled_by_default=True,
            plugin_description="Spaces inside link text",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md039.md",
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_inline_link or token.is_inline_image:
            link_token = cast(LinkStartMarkdownToken, token)
            if link_token.text_from_blocks != link_token.text_from_blocks.strip():
                self.report_next_token_error(context, token)
