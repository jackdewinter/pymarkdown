"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from plugin_manager import Plugin, PluginDetails


class RuleMd005(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # bullet, ul, indentation
            plugin_name="list-indent",
            plugin_id="MD005",
            plugin_enabled_by_default=True,
            plugin_description="Inconsistent indentation for list items at the same level",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md005---inconsistent-indentation-for-list-items-at-the-same-level

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
