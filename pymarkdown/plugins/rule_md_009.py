"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd009(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # whitespace
            plugin_name="no-trailing-spaces",
            plugin_id="MD009",
            plugin_enabled_by_default=False,
            plugin_description="Trailing spaces",
            plugin_version="0.0.0",
            plugin_interface_version=1
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md007---unordered-list-indentation
        # Parameters: br_spaces, list_item_empty_lines, strict (number; default 2, boolean; default false, boolean; default false)
