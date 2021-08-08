"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd042(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # links
            plugin_name="no-empty-links",
            plugin_id="MD042",
            plugin_enabled_by_default=True,
            plugin_description="No empty links",
            plugin_version="0.5.0",
            plugin_interface_version=1,
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md042---no-empty-links

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_inline_link or token.is_inline_image:
            stripped_link_uri = token.active_link_uri.strip()
            if not stripped_link_uri or stripped_link_uri == "#":
                self.report_next_token_error(context, token)
