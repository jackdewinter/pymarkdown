"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd033(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # html
            plugin_name="no-inline-html",
            plugin_id="MD033",
            plugin_enabled_by_default=False,
            plugin_description="Inline HTML",
            plugin_version="0.0.0",
            plugin_interface_version=1,
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md033---inline-html
        # Parameters: allowed_elements (array of string; default empty)
