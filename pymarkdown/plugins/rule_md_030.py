"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd030(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # ol, ul, whitespace
            plugin_name="list-marker-space",
            plugin_id="MD030",
            plugin_enabled_by_default=False,
            plugin_description="Spaces after list markers",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md030---spaces-after-list-markers
        # Parameters: ul_single, ol_single, ul_multi, ol_multi (number; default 1)
