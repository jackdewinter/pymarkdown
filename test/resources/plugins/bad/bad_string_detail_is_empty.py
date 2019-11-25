"""
Module to implement a sample plugin that has an empty string field from get_details.
"""
from plugin_manager import Plugin, PluginDetails


class BadStringDetailIsEmpty(Plugin):
    """
    Class to implement a sample plugin that has an empty string field from get_details.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="bad-string-detail-is-empty",
            plugin_id="MDE006",
            plugin_enabled_by_default=True,
            plugin_description="",
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
