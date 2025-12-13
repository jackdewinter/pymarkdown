"""
Module to implement a plugin that looks for excessively long lines in the file.
"""

from typing import List, Optional, Tuple

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetails,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import MarkdownToken


# pylint: disable=too-many-instance-attributes
class RuleMd013(RulePlugin):
    """
    Class to implement a plugin that looks for excessively long lines in the file.
    """

    __maximum_line_length = 99999

    def __init__(self) -> None:
        super().__init__()
        self.__leaf_tokens: List[MarkdownToken] = []
        self.__line_index = 0
        self.__leaf_token_index = 0
        self.__line_length = 0
        self.__code_block_line_length = 0
        self.__heading_line_length = 0
        self.__minimum_line_length = 0
        self.__code_blocks_active = False
        self.__headings_active = False
        self.__strict_mode = False
        self.__stern_mode = False
        self.__last_line: Optional[str] = None

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="line-length",
            plugin_id="MD013",
            plugin_enabled_by_default=True,
            plugin_description="Line length",
            plugin_version="0.6.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md013.md",
            plugin_configuration="line_length,heading_line_length,code_block_line_length,"
            + "code_blocks,headings,strict,stern",
        )

    @classmethod
    def __validate_minimum(cls, found_value: int) -> None:
        if found_value < 1:
            raise ValueError("Allowable values are any integer greater than 0.")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__line_length = (
            self.plugin_configuration.get_integer_property_with_default(
                "line_length",
                80,
                valid_value_fn=self.__validate_minimum,
            )
        )
        self.__code_block_line_length = (
            self.plugin_configuration.get_integer_property_with_default(
                "code_block_line_length",
                80,
                valid_value_fn=self.__validate_minimum,
            )
        )
        self.__heading_line_length = (
            self.plugin_configuration.get_integer_property_with_default(
                "heading_line_length",
                80,
                valid_value_fn=self.__validate_minimum,
            )
        )
        self.__minimum_line_length = min(
            self.__line_length,
            self.__code_block_line_length,
            self.__heading_line_length,
        )

        self.__code_blocks_active = (
            self.plugin_configuration.get_boolean_property_with_default(
                "code_blocks",
                True,
            )
        )
        self.__headings_active = (
            self.plugin_configuration.get_boolean_property_with_default(
                "headings",
                True,
            )
        )
        self.__strict_mode = (
            self.plugin_configuration.get_boolean_property_with_default(
                "strict",
                False,
            )
        )
        self.__stern_mode = self.plugin_configuration.get_boolean_property_with_default(
            "stern",
            False,
        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("line_length", self.__line_length),
            QueryConfigItem("code_block_line_length", self.__code_block_line_length),
            QueryConfigItem("heading_line_length", self.__heading_line_length),
            QueryConfigItem("code_blocks", self.__code_blocks_active),
            QueryConfigItem("headings", self.__headings_active),
            QueryConfigItem("strict", self.__strict_mode),
            QueryConfigItem("stern", self.__stern_mode),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__leaf_tokens = []
        self.__line_index = 1
        self.__leaf_token_index = 0
        self.__last_line = None

    def __is_really_longer(
        self, line_length: int, compare_length: int
    ) -> Tuple[bool, int]:
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
        return line_length > compare_length, compare_length

    def next_line(self, context: PluginScanContext, line: str) -> None:
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
        if line_length > self.__minimum_line_length:
            is_actually_longer, compare_length = self.__is_really_longer(
                line_length, compare_length
            )
        else:
            is_actually_longer = False
        if is_actually_longer:
            # trigger_rule = False
            if self.__strict_mode:
                trigger_rule = True
            else:
                next_space_index, _ = ParserHelper.extract_until_spaces(
                    line, compare_length
                )
                # print("next_index=" + str(next_space_index))
                trigger_rule = (
                    line_length == next_space_index
                    if self.__stern_mode
                    else line_length != next_space_index
                )

            if trigger_rule:
                extra_error_information = (
                    f"Expected: {compare_length}, Actual: {line_length}"
                )
                override_is_error_token_prefaced_by_blank_line = (
                    self.__last_line is not None and not self.__last_line
                )
                self.report_next_line_error(
                    context,
                    1,
                    extra_error_information=extra_error_information,
                    override_is_error_token_prefaced_by_blank_line=override_is_error_token_prefaced_by_blank_line,
                )
        self.__line_index += 1
        self.__last_line = line.strip(" \t")

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        _ = context
        if token.is_blank_line or token.is_leaf:
            self.__leaf_tokens.append(token)


# pylint: enable=too-many-instance-attributes
