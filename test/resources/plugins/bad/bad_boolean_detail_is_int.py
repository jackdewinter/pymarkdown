"""
Module to implement a sample plugin that has a bad boolean field from get_details.
"""
from plugin_manager import Plugin, PluginDetails


class BadBooleanDetailIsInt(Plugin):
    """
    Class to implement a sample plugin that has a bad boolean field from get_details.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="bad-boolean-detail-is-int",
            plugin_id="MDE005",
            plugin_enabled_by_default=123,
            plugin_description="Plugin that has a bad boolean detail.",
        )
