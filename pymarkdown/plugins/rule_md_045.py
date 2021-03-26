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
            plugin_enabled_by_default=False,
            plugin_description="Images should have alternate text (alt text)",
            plugin_version="0.0.0",
            plugin_interface_version=1
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md045---images-should-have-alternate-text-alt-text
