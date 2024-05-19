"""
Module to implement a plugin to ensure all files end with a blank line.
"""

from pymarkdown.plugin_manager.plugin_details import PluginDetails, PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class RuleMd047(RulePlugin):
    """
    Class to implement a plugin to ensure all files end with a blank line.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__last_line: str = ""

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="single-trailing-newline",
            plugin_id="MD047",
            plugin_enabled_by_default=True,
            plugin_description="Each file should end with a single newline character.",
            plugin_version="0.5.1",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md047.md",
            plugin_supports_fix=True,
            plugin_fix_level=0,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__last_line = ""

    def next_line(self, context: PluginScanContext, line: str) -> None:
        """
        Event that a new line is being processed.
        """
        _ = context
        self.__last_line = line

    def completed_file(self, context: PluginScanContext) -> None:
        """
        Event that the file being currently scanned is now completed.
        """
        if context.in_fix_mode:
            if (
                context.last_line_fixed is not None
                and not context.last_line_fixed.endswith("\n")
            ):
                context.set_current_fix_line("\n")
        elif self.__last_line:
            self.report_next_line_error(context, len(self.__last_line), -1)
