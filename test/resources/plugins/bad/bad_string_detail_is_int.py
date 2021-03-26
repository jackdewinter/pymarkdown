"""
Module to implement a sample plugin that has a bad string field from get_details.
"""
from plugin_manager import Plugin, PluginDetails


class BadStringDetailIsInt(Plugin):
    """
    Class to implement a sample plugin that has a bad string field from get_details.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="bad-string-detail-is-int",
            plugin_id="MDE007",
            plugin_enabled_by_default=True,
            plugin_description=123,
            plugin_version="0.0.0",
            plugin_interface_version=1
        )
