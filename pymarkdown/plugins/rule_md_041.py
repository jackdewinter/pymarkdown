"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd041(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers
            plugin_name="first-line-heading,first-line-h1",
            plugin_id="MD041",
            plugin_enabled_by_default=False,
            plugin_description="First line in file should be a top level heading",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md041---first-line-in-file-should-be-a-top-level-heading
