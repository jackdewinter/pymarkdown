"""
Module to implement a plugin that looks for image elements that do not specify alternate text.
"""

from typing import cast

from pymarkdown.general.constants import Constants
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.image_start_markdown_token import ImageStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd045(RulePlugin):
    """
    Class to implement a plugin that looks for image elements that do not specify alternate text.
    """

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-alt-text",
            plugin_id="MD045",
            plugin_enabled_by_default=True,
            plugin_description="Images should have alternate text (alt text)",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md045.md",
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_inline_image:
            image_token = cast(ImageStartMarkdownToken, token)
            if not image_token.text_from_blocks.strip(
                Constants.unicode_whitespace.value()
            ):
                self.report_next_token_error(context, token)
