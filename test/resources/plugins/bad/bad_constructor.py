"""
Module to implement a sample plugin that has a bad constructor function.
"""
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class BadConstructor(RulePlugin):
    """
    Class to implement a sample plugin that has a bad constructor function.
    """

    def __init__(self):
        raise Exception("bad constructor")

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="bad-constructor",
            plugin_id="MDE004",
            plugin_enabled_by_default=True,
            plugin_description="Plugin that has a bad constructor function.",
            plugin_version="0.0.0",
            plugin_interface_version=1,
        )
