"""
Module to implement a sample plugin that has a bad starting_new_file function.
"""
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class BadNextToken(RulePlugin):
    """
    Class to implement a sample plugin that has a bad starting_new_file function.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="bad-next-token",
            plugin_id="MDE003",
            plugin_enabled_by_default=True,
            plugin_description="Plugin that has a bad next_token function.",
            plugin_version="0.0.0",
            plugin_interface_version=1,
        )

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        raise Exception("bad next_token")
