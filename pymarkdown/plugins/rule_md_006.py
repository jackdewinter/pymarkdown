"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd006(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # bullet, ul, indentation
            plugin_name="ul-start-left",
            plugin_id="MD006",
            plugin_enabled_by_default=False,
            plugin_description="Consider starting bulleted lists at the beginning of the line",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md006---consider-starting-bulleted-lists-at-the-beginning-of-the-line
