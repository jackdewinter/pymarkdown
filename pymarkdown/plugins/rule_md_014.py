"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd014(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # code
            plugin_name="commands-show-output",
            plugin_id="MD014",
            plugin_enabled_by_default=False,
            plugin_description="Dollar signs used before commands without showing output",
            plugin_version="0.0.0",
            plugin_interface_version=1,
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md014---dollar-signs-used-before-commands-without-showing-output
