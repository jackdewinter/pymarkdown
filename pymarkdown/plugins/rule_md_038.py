"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd038(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # whitespace, code
            plugin_name="no-space-in-code",
            plugin_id="MD038",
            plugin_enabled_by_default=True,
            plugin_description="Spaces inside code span elements",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md038---spaces-inside-code-span-elements
