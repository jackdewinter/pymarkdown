"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd039(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # whitespace, links
            plugin_name="no-space-in-links",
            plugin_id="MD039",
            plugin_enabled_by_default=True,
            plugin_description="Spaces inside link text",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md039---spaces-inside-link-text
