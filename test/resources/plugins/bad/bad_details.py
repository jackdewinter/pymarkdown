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
