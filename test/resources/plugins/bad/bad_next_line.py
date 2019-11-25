"""
Module to implement a sample plugin that has a bad starting_new_file function.
"""
from plugin_manager import Plugin, PluginDetails


class BadNextLine(Plugin):
    """
    Class to implement a sample plugin that has a bad starting_new_file function.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="bad-next-line",
            plugin_id="MDE003",
            plugin_enabled_by_default=True,
            plugin_description="Plugin that has a bad next_line function.",
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
        raise Exception("bad next_line")

    def completed_file(self):
        """
        Event that the file being currently scanned is now completed.
        """
        pass
