"""
Module to implement a sample plugin that has a bad starting_new_file function.
"""
from plugin_manager import Plugin, PluginDetails


class BadStartingNewFile(Plugin):
    """
    Class to implement a sample plugin that has a bad starting_new_file function.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="bad-starting-new-file",
            plugin_id="MDE001",
            plugin_enabled_by_default=True,
            plugin_description="Plugin that has a bad starting_new_file function.",
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
        raise Exception("bad starting_new_file")

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
