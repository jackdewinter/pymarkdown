"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd004(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # bullet, ul
            plugin_name="ul-style",
            plugin_id="MD004",
            plugin_enabled_by_default=True,
            plugin_description="Unordered list style",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md004---unordered-list-style
        # Parameters: style ("consistent", "asterisk", "plus", "dash", "sublist"; default "consistent")

