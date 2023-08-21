"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails, PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class RuleMd010(RulePlugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__allow_in_code_blocks: bool = False

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="no-hard-tabs",
            plugin_id="MD010",
            plugin_enabled_by_default=True,
            plugin_description="Hard tabs",
            plugin_version="0.5.0",
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md010.md",
            plugin_configuration="code_blocks",
            plugin_supports_fix=True,
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__allow_in_code_blocks = self.plugin_configuration.get_boolean_property(
            "code_blocks",
            default_value=True,
        )

    def next_line(self, context: PluginScanContext, line: str) -> None:
        """
        Event that a new line is being processed.
        """
        _ = self.__allow_in_code_blocks

        if "\t" in line:
            if context.in_fix_mode:
                context.set_current_fix_line(TabHelper.detabify_string(line))
            else:
                next_index = line.find("\t", 0)
                while next_index != -1:
                    self.report_next_line_error(
                        context,
                        next_index + 1,
                        extra_error_information=f"Column: {next_index + 1}",
                    )
                    next_index = line.find("\t", next_index + 1)
