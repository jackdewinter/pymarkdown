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

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration.
        """
        pass

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        pass

    def next_line(self, line):
        """
        Event that a new line is being processed.
        """
        pass

    def completed_file(self):
        """
        Event that the file being currently scanned is now completed.
        """
        pass
