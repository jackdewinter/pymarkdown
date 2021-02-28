"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd037(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # whitespace, emphasis
            plugin_name="no-space-in-emphasis",
            plugin_id="MD037",
            plugin_enabled_by_default=True,
            plugin_description="Spaces inside emphasis markers",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md037---spaces-inside-emphasis-markers
