"""
Module to implement a sample plugin that has a class name different than the file name.
"""
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class PluginTwo(RulePlugin):
    """
    Class to implement a sample plugin that has a class name different than the file name.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="class-name-mismatch",
            plugin_id="MD997",
            plugin_enabled_by_default=True,
            plugin_description="Plugin that has a mismatch between the module name and the class name.",
            plugin_version="0.0.0",
            plugin_interface_version=1,
        )

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration.
        """
        print(f"{self.get_id()}>>init_from_config")

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        print(f"{self.get_id()}>>starting_new_file>>")

    def next_line(self, context, line):
        """
        Event that a new line is being processed.
        """
        print(f"{self.get_id()}>>next_line:{line}")

    def completed_file(self, context):
        """
        Event that the file being currently scanned is now completed.
        """
        print(f"{self.get_id()}>>completed_file")
