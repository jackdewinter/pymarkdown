"""
Module to implement a sample plugin that has a bad starting_new_file function.
"""
from plugin_manager import Plugin, PluginDetails


class BadCompletedFile(Plugin):
    """
    Class to implement a sample plugin that has a bad starting_new_file function.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="bad-starting-new-file",
            plugin_id="MDE002",
            plugin_enabled_by_default=True,
            plugin_description="Plugin that has a bad completed_file function.",
            plugin_version="0.0.0",
            plugin_interface_version=1
        )

    def completed_file(self, context):
        """
        Event that the file being currently scanned is now completed.
        """
        raise Exception("bad completed_file")
