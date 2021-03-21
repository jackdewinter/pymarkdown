"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd034(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # links, url
            plugin_name="no-bare-urls",
            plugin_id="MD034",
            plugin_enabled_by_default=False,
            plugin_description="Bare URL used",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md034---bare-url-used
