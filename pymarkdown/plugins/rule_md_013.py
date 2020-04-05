"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from plugin_manager import Plugin, PluginDetails


class RuleMd013(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # line_length
            plugin_name="line-length",
            plugin_id="MD013",
            plugin_enabled_by_default=True,
            plugin_description="Line length",
        ) # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md013---line-length
        # Parameters: line_length, heading_line_length, code_block_line_length, code_blocks, tables, headings, headers, strict (number; default 80, boolean; default true)

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
