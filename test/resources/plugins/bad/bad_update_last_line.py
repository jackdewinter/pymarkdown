"""
Module to implement a sample plugin that always adds a newline to the
end of the file.  This is meant to clash with rule Md047
"""
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class BadUpdateLastLine(RulePlugin):
    """
    Class to implement a sample plugin that always adds a newline to the
    end of the file.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="bad-update-last-line",
            plugin_id="MDE003",
            plugin_enabled_by_default=True,
            plugin_description="Plugin that has always adds a newline.",
            plugin_version="0.0.0",
            plugin_supports_fix=True,
            plugin_fix_level=0,
        )

    def completed_file(self, context: PluginScanContext) -> None:
        """
        Event that the file being currently scanned is now completed.
        """
        if context.in_fix_mode and context.is_during_line_pass:
            context.set_current_fix_line("")
