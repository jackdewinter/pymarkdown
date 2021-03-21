"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd043(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers
            plugin_name="required-headings,required-headers",
            plugin_id="MD043",
            plugin_enabled_by_default=False,
            plugin_description="Required heading structure",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md043---required-heading-structure
