"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd046(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # code
            plugin_name="code-block-style",
            plugin_id="MD046",
            plugin_enabled_by_default=False,
            plugin_description="Code block style",
            plugin_version="0.0.0",
            plugin_interface_version=1
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md045---images-should-have-alternate-text-alt-text
        # Parameters: style ("consistent", "fenced", "indented"; default "consistent")
