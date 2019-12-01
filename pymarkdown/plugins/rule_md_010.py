"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from plugin_manager import Plugin, PluginDetails


class RuleMd010(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    # def __init__(self):
    #    super().__init__()

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="single-trailing-newline",
            plugin_id="MD010",
            plugin_enabled_by_default=True,
            plugin_description="Files should end with a single newline character",
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """

    def next_line(self, line):
        """
        Event that a new line is being processed.
        """

    def completed_file(self):
        """
        Event that the file being currently scanned is now completed.
        """
