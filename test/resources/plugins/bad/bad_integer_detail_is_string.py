"""
Module to implement a sample plugin that has a bad integer field from get_details.
"""
from plugin_manager import Plugin, PluginDetails


class BadIntegerDetailIsString(Plugin):
    """
    Class to implement a sample plugin that has a bad integer field from get_details.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="bad-int-detail-is-string",
            plugin_id="MDE005",
            plugin_enabled_by_default=True,
            plugin_description="Plugin that has a bad integer detail.",
            plugin_version="0.0.0",
            plugin_interface_version="I am a string",
        )
