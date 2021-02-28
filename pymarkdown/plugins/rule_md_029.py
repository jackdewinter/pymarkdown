"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd029(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # ol
            plugin_name="ol-prefix",
            plugin_id="MD029",
            plugin_enabled_by_default=True,
            plugin_description="Ordered list item prefix",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md029---ordered-list-item-prefix
        # Parameters: style ("one", "ordered", "one_or_ordered", "zero"; default "one_or_ordered")
