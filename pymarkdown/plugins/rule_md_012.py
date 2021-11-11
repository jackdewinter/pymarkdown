"""
Module to implement a plugin that looks for multiple blank lines in the files.
"""
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class RuleMd012(RulePlugin):
    """
    Class to implement a plugin that looks for multiple blank lines in the files.
    """

    def __init__(self):
        super().__init__()
        self.__blank_lines_maximum = None
        self.__blank_line_count = None
        self.__last_blank_line = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-multiple-blanks",
            plugin_id="MD012",
            plugin_enabled_by_default=True,
            plugin_description="Multiple consecutive blank lines",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md012.md",
            plugin_configuration="maximum",
        )

    @classmethod
    def __validate_maximum(cls, found_value):
        if found_value < 0:
            raise ValueError("Allowable values are any non-negative integers.")

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__blank_lines_maximum = self.plugin_configuration.get_integer_property(
            "maximum",
            default_value=1,
            valid_value_fn=self.__validate_maximum,
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__blank_line_count = 0
        self.__last_blank_line = None

    def __check_for_excess_blank_lines(self, context):
        if self.__blank_line_count > self.__blank_lines_maximum:
            extra_data = f"Expected: {self.__blank_lines_maximum}, Actual: {self.__blank_line_count}"

            self.report_next_token_error(
                context, self.__last_blank_line, extra_error_information=extra_data
            )

    def completed_file(self, context):
        """
        Event that the file being currently scanned is now completed.
        """
        self.__check_for_excess_blank_lines(context)

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_blank_line:
            self.__last_blank_line = token
            self.__blank_line_count += 1
        else:
            self.__check_for_excess_blank_lines(context)
            self.__blank_line_count = 0
