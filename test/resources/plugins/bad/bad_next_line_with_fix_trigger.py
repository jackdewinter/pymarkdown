"""
Module to implement a sample plugin that has a bad next_line function.
"""

from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class BadNextLineWithFixTrigger(RulePlugin):
    """
    Class to implement a sample plugin that has a bad starting_new_file function.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="bad-next-line-with-trigger",
            plugin_id="MDE008",
            plugin_enabled_by_default=True,
            plugin_description="Plugin that has a bad next_line function.",
            plugin_version="0.0.0",
            plugin_fix_level=0,
            plugin_supports_fix=True,
        )

    def next_line(self, context, line):
        """
        Event that a new line is being processed.
        """
        if line == "throw_exception" and context.in_fix_mode:
            raise Exception("bad next_line")
