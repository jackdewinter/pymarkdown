"""
Module to implement a plugin that looks for excessively long lines in the file.
"""
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


# pylint: disable=too-many-instance-attributes
class RuleMd013(RulePlugin):
    """
    Class to implement a plugin that looks for excessively long lines in the file.
    """

    __maximum_line_length = 99999

    def __init__(self):
        super().__init__()
        self.__leaf_tokens = None
        self.__line_index = None
        self.__leaf_token_index = None
        self.__line_length = None
        self.__code_block_line_length = None
        self.__heading_line_length = None
        self.__minimum_line_length = None
        self.__code_blocks_active = None
        self.__headings_active = None
        self.__strict_mode = None
        self.__stern_mode = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="line-length",
            plugin_id="MD013",
            plugin_enabled_by_default=True,
            plugin_description="Line length",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md013.md",
            plugin_configuration="line_length,heading_line_length,code_block_line_length,code_blocks,headings,strict,stern",
        )

    @classmethod
    def __validate_minimum(cls, found_value):
        if found_value < 1:
            raise ValueError("Allowable values are any integer greater than 0.")

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__line_length = self.plugin_configuration.get_integer_property(
            "line_length",
            default_value=80,
            valid_value_fn=self.__validate_minimum,
        )
        self.__code_block_line_length = self.plugin_configuration.get_integer_property(
            "code_block_line_length",
            default_value=80,
            valid_value_fn=self.__validate_minimum,
        )
        self.__heading_line_length = self.plugin_configuration.get_integer_property(
            "heading_line_length",
            default_value=80,
            valid_value_fn=self.__validate_minimum,
        )
        self.__minimum_line_length = min(
            self.__line_length,
            self.__code_block_line_length,
            self.__heading_line_length,
        )

        self.__code_blocks_active = self.plugin_configuration.get_boolean_property(
            "code_blocks",
            default_value=True,
        )
        self.__headings_active = self.plugin_configuration.get_boolean_property(
            "headings",
            default_value=True,
        )
        self.__strict_mode = self.plugin_configuration.get_boolean_property(
            "strict",
            default_value=False,
        )
        self.__stern_mode = self.plugin_configuration.get_boolean_property(
            "stern",
            default_value=False,
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__leaf_tokens = []
        self.__line_index = 1
        self.__leaf_token_index = 0

    def next_line(self, context, line):
        """
        Event that a new line is being processed.
        """
        if (
            self.__leaf_token_index + 1 < len(self.__leaf_tokens)
            and self.__line_index
            == self.__leaf_tokens[self.__leaf_token_index + 1].line_number
        ):
            self.__leaf_token_index += 1

        line_length = len(line)
        compare_length = self.__line_length
        is_actually_longer = False
        if line_length > self.__minimum_line_length:
            # print("line(" + str(self.__line_index) + ")->len=(" + str(line_length) + "):" + str(line))
            # print("-->" + str(self.__leaf_tokens[self.__leaf_token_index]))
            if (
                self.__leaf_tokens[self.__leaf_token_index].is_fenced_code_block
                or self.__leaf_tokens[self.__leaf_token_index].is_indented_code_block
            ):
                compare_length = (
                    self.__code_block_line_length
                    if self.__code_blocks_active
                    else RuleMd013.__maximum_line_length
                )
            elif (
                self.__leaf_tokens[self.__leaf_token_index].is_atx_heading
                or self.__leaf_tokens[self.__leaf_token_index].is_setext_heading
            ):
                compare_length = (
                    self.__heading_line_length
                    if self.__headings_active
                    else RuleMd013.__maximum_line_length
                )
            is_actually_longer = line_length > compare_length
            # print("is_actually_longer=" + str(is_actually_longer) + ", len=(" + str(line_length) + ", compare_length=" + str(compare_length))
        if is_actually_longer:

            trigger_rule = False
            if self.__strict_mode:
                trigger_rule = True
            else:
                next_space_index, _ = ParserHelper.extract_until_whitespace(
                    line, compare_length
                )
                # print("next_index=" + str(next_space_index))

                if self.__stern_mode:
                    trigger_rule = line_length == next_space_index
                else:
                    trigger_rule = line_length != next_space_index

            if trigger_rule:
                extra_error_information = (
                    f"Expected: {compare_length}, Actual: {line_length}"
                )
                self.report_next_line_error(
                    context, 1, extra_error_information=extra_error_information
                )
        self.__line_index += 1

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_blank_line or token.is_leaf:
            self.__leaf_tokens.append(token)


# pylint: enable=too-many-instance-attributes
