"""
Module to implement a sample plugin that has a blank description.
"""
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class BlankDescription(RulePlugin):
    """
    Class to implement a sample plugin that has a blank description.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="blank-description",
            plugin_id="MDE007",
            plugin_enabled_by_default=True,
            plugin_description=" ",
            plugin_version="0.0.0",
            plugin_interface_version=1,
        )

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration.
        """
        print(f"{self.get_details().plugin_id}>>init_from_config")

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        print(f"{self.get_details().plugin_id}>>starting_new_file>>")

    def next_line(self, context, line):
        """
        Event that a new line is being processed.
        """
        print(f"{self.get_details().plugin_id}>>next_line:{line}")

    def completed_file(self, context):
        """
        Event that the file being currently scanned is now completed.
        """
        print(f"{self.get_details().plugin_id}>>completed_file")
