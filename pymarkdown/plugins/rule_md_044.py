"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd044(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # spelling
            plugin_name="proper-names",
            plugin_id="MD044",
            plugin_enabled_by_default=True,
            plugin_description="Proper names should have the correct capitalization",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md044---proper-names-should-have-the-correct-capitalization
        # Parameters: names, code_blocks (string array; default null, boolean; default true)

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
