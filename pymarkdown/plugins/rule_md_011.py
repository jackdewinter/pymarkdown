"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd011(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # links
            plugin_name="no-reversed-links",
            plugin_id="MD011",
            plugin_enabled_by_default=False,
            plugin_description="Reversed link syntax",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md011---reversed-link-syntax
