"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class RuleMd010(RulePlugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def __init__(self):
        super().__init__()
        self.__allow_in_code_blocks = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-hard-tabs",
            plugin_id="MD010",
            plugin_enabled_by_default=True,
            plugin_description="Hard tabs",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md010.md",
            plugin_configuration="code_blocks",
        )

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__allow_in_code_blocks = self.plugin_configuration.get_boolean_property(
            "code_blocks",
            default_value=True,
        )

    def next_line(self, context, line):
        """
        Event that a new line is being processed.
        """
        _ = self.__allow_in_code_blocks

        if "\t" in line:
            next_index = line.find("\t", 0)
            while next_index != -1:
                extra_data = f"Column: {next_index + 1}"
                self.report_next_line_error(
                    context, next_index + 1, extra_error_information=extra_data
                )
                next_index = line.find("\t", next_index + 1)
