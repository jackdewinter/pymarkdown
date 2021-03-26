"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd010(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # whitespace, hard_tab
            plugin_name="no-hard-tabs",
            plugin_id="MD010",
            plugin_enabled_by_default=False,
            plugin_description="Hard tabs",
            plugin_version="0.0.0",
            plugin_interface_version=1
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md010---hard-tabs
        # Parameters: code_blocks (boolean; default true)
