"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from plugin_manager import Plugin, PluginDetails


class RuleMd032(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # bullet, ul, ol, blank_lines
            plugin_name="blanks-around-lists",
            plugin_id="MD032",
            plugin_enabled_by_default=True,
            plugin_description="Lists should be surrounded by blank lines",
        ) # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md032---lists-should-be-surrounded-by-blank-lines

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
