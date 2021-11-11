"""
Module to implement a plugin that looks for spaces within link labels.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd039(Plugin):
    """
    Class to implement a plugin that looks for spaces within link labels.
    """

    def get_details(self):
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

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if (
            token.is_inline_link or token.is_inline_image
        ) and token.text_from_blocks != token.text_from_blocks.strip():
            self.report_next_token_error(context, token)
