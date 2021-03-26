"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd048(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # code
            plugin_name="code-fence-style",
            plugin_id="MD048",
            plugin_enabled_by_default=False,
            plugin_description="Code fence style",
            plugin_version="0.0.0",
            plugin_interface_version=1
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md048---code-fence-style
        # Parameters: style ("consistent", "tilde", "backtick"; default "consistent")
