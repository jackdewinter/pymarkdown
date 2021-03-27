"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd027(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # blockquote, whitespace, indentation
            plugin_name="no-multiple-space-blockquote",
            plugin_id="MD027",
            plugin_enabled_by_default=False,
            plugin_description="Multiple spaces after blockquote symbol",
            plugin_version="0.0.0",
            plugin_interface_version=1,
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md027---multiple-spaces-after-blockquote-symbol
