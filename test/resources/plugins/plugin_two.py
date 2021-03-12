"""
Module to implement a sample plugin that just reports that it has been called.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class PluginTwo(Plugin):
    """
    Class to implement a sample plugin that just reports that it has been called.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="debug-only-2",
            plugin_id="MD998",
            plugin_enabled_by_default=True,
            plugin_description="Debug plugin",
        )

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration.
        """
        print(self.get_details().plugin_id + ">>init_from_config")

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        print(self.get_details().plugin_id + ">>starting_new_file>>")

    def next_line(self, context, line):
        """
        Event that a new line is being processed.
        """
        print(self.get_details().plugin_id + ">>next_line:" + line)

    def completed_file(self, context):
        """
        Event that the file being currently scanned is now completed.
        """
        print(self.get_details().plugin_id + ">>completed_file")
