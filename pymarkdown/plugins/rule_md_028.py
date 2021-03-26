"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd028(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # blockquote, whitespace
            plugin_name="no-blanks-blockquote",
            plugin_id="MD028",
            plugin_enabled_by_default=False,
            plugin_description="Blank line inside blockquote",
            plugin_version="0.0.0",
            plugin_interface_version=1
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md028---blank-line-inside-blockquote
