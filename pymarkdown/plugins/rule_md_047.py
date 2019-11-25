"""
Module to implement a sample plugin that just reports that it has been called.
"""
from plugin_manager import Plugin, PluginDetails


class RuleMd047(Plugin):
    """
    Class to implement a sample plugin that just reports that it has been called.
    """

    def __init__(self):
        super().__init__()
        self.last_line = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="single-trailing-newline",
            plugin_id="MD047",
            plugin_enabled_by_default=True,
            plugin_description="Files should end with a single newline character",
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.last_line = None

    def next_line(self, line):
        """
        Event that a new line is being processed.
        """
        self.last_line = line

    def completed_file(self):
        """
        Event that the file being currently scanned is now completed.
        """
        if self.last_line:
            # pylint: disable=too-many-function-args
            self.report_error(len(self.last_line), -1)
