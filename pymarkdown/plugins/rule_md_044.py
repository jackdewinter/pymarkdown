"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd044(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # spelling
            plugin_name="proper-names",
            plugin_id="MD044",
            plugin_enabled_by_default=True,
            plugin_description="Proper names should have the correct capitalization",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md044---proper-names-should-have-the-correct-capitalization
        # Parameters: names, code_blocks (string array; default null, boolean; default true)
