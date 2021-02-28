"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd007(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # bullet, ul, indentation
            plugin_name="ul-indent",
            plugin_id="MD007",
            plugin_enabled_by_default=True,
            plugin_description="Unordered list indentation",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md007---unordered-list-indentation
