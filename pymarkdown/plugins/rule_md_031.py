"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd031(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # code, blank_lines
            plugin_name="blanks-around-fences",
            plugin_id="MD031",
            plugin_enabled_by_default=True,
            plugin_description="Fenced code blocks should be surrounded by blank lines",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md031---fenced-code-blocks-should-be-surrounded-by-blank-lines
        # Parameters: list_items (boolean; default true)
