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
            plugin_enabled_by_default=False,
            plugin_description="Horizontal rule style",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md035---horizontal-rule-style
        # Parameters: style ("consistent", "---", "***", or other string specifying the horizontal rule; default "consistent")
