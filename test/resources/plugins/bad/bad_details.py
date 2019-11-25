"""
Module to implement a sample plugin that has a bad constructor function.
"""
from plugin_manager import Plugin


class BadDetails(Plugin):
    """
    Class to implement a sample plugin that has a bad details function.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        raise Exception("bad details")

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
