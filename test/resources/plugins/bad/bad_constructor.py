"""
Module to implement a sample plugin that has a bad constructor function.
"""
from plugin_manager import Plugin, PluginDetails


class BadConstructor(Plugin):
    """
    Class to implement a sample plugin that has a bad constructor function.
    """

    def __init__(self):
        raise Exception("bad constructor")

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="bad-constructor",
            plugin_id="MDE004",
            plugin_enabled_by_default=True,
            plugin_description="Plugin that has a bad constructor function.",
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
