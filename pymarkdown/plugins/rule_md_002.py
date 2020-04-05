"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from plugin_manager import Plugin, PluginDetails


class RuleMd002(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers
            plugin_name="first-heading-h1,first-header-h1",
            plugin_id="MD002",
            plugin_enabled_by_default=False,
            plugin_description="First heading should be a top level heading",
        ) # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md002---first-heading-should-be-a-top-level-heading
        # Parameters: level (number; default 1)

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
