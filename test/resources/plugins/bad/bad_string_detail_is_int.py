"""
Module to implement a sample plugin that has a bad string field from get_details.
"""
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class BadStringDetailIsInt(RulePlugin):
    """
    Class to implement a sample plugin that has a bad string field from get_details.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="bad-string-detail-is-int",
            plugin_id="MDE007",
            plugin_enabled_by_default=True,
            plugin_description=123,
            plugin_version="0.0.0",
            plugin_interface_version=1,
        )
