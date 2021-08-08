"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd045(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # accessibility, images
            plugin_name="no-alt-text",
            plugin_id="MD045",
            plugin_enabled_by_default=True,
            plugin_description="Images should have alternate text (alt text)",
            plugin_version="0.5.0",
            plugin_interface_version=1,
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md045---images-should-have-alternate-text-alt-text

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_inline_image:
            if not token.text_from_blocks.strip():
                self.report_next_token_error(context, token)
