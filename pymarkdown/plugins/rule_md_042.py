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
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md042---no-empty-links
