"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd025(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers
            plugin_name="single-title,single-h1",
            plugin_id="MD025",
            plugin_enabled_by_default=False,
            plugin_description="Multiple top level headings in the same document",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md025---multiple-top-level-headings-in-the-same-document
        # Parameters: level, front_matter_title (number; default 1, string; default "^\s*title:")
