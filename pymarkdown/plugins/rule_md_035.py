"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd035(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # hr
            plugin_name="hr-style",
            plugin_id="MD035",
            plugin_enabled_by_default=True,
            plugin_description="Horizontal rule style",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md035---horizontal-rule-style
        # Parameters: style ("consistent", "---", "***", or other string specifying the horizontal rule; default "consistent")

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
