"""
Module to implement a plugin to ensure all files end with a blank line.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd047(Plugin):
    """
    Class to implement a plugin to ensure all files end with a blank line.
    """

    def __init__(self):
        super().__init__()
        self.__last_line = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="single-trailing-newline",
            plugin_id="MD047",
            plugin_enabled_by_default=True,
            plugin_description="Each file should end with a single newline character.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md047.md",
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__last_line = None

    def next_line(self, context, line):
        """
        Event that a new line is being processed.
        """
        _ = context
        self.__last_line = line

    def completed_file(self, context):
        """
        Event that the file being currently scanned is now completed.
        """
        if self.__last_line:
            self.report_next_line_error(context, len(self.__last_line), -1)
