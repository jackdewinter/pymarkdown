"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd012(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # whitespace, blank_lines
            plugin_name="no-multiple-blanks",
            plugin_id="MD012",
            plugin_enabled_by_default=True,
            plugin_description="Multiple consecutive blank lines",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md012---multiple-consecutive-blank-lines
        # Parameters: maximum (number; default 1)
