"""
Module to implement a plugin that looks for trailing spaces in the files.
"""

from typing import List, Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetails,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.container_markdown_token import ContainerMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


# pylint: disable=too-many-instance-attributes
class RuleMd009(RulePlugin):
    """
    Class to implement a plugin that looks for trailing spaces in the files.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__leaf_tokens: List[MarkdownToken] = []
        self.__leaf_owner_tokens: List[Optional[MarkdownToken]] = []
        self.__line_index = 0
        self.__leaf_token_index = 0
        self.__inline_token_index = 0
        self.__container_token_stack: List[ContainerMarkdownToken] = []
        self.__break_spaces = 0
        self.__strict_mode = False
        self.__list_item_empty_lines_mode = False

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="no-trailing-spaces",
            plugin_id="MD009",
            plugin_enabled_by_default=True,
            plugin_description="Trailing spaces",
            plugin_version="0.6.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md009.md",
            plugin_configuration="br_spaces,list_item_empty_lines,strict",
            plugin_supports_fix=True,
            plugin_fix_level=0,
        )

    @classmethod
    def __validate_break_spaces(cls, found_value: int) -> None:
        if found_value < 0:
            raise ValueError("Allowable values are greater than or equal to 0.")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__break_spaces = (
            self.plugin_configuration.get_integer_property_with_default(
                "br_spaces",
                2,
                valid_value_fn=self.__validate_break_spaces,
            )
        )
        if self.__break_spaces < 2:
            self.__break_spaces = 0

        self.__strict_mode = (
            self.plugin_configuration.get_boolean_property_with_default(
                "strict",
                False,
            )
        )

        self.__list_item_empty_lines_mode = (
            self.plugin_configuration.get_boolean_property_with_default(
                "list_item_empty_lines",
                False,
            )
        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("br_spaces", self.__break_spaces),
            QueryConfigItem("strict", self.__strict_mode),
            QueryConfigItem("list_item_empty_lines", self.__list_item_empty_lines_mode),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__leaf_tokens = []
        self.__leaf_owner_tokens = []
        self.__line_index = 1
        self.__leaf_token_index = 0
        self.__inline_token_index = 0
        self.__container_token_stack = []

    def next_line(self, context: PluginScanContext, line: str) -> None:
        """
        Event that a new line is being processed.
        """
        if (
            self.__leaf_token_index + 1 < len(self.__leaf_tokens)
            and self.__line_index
            == self.__leaf_tokens[self.__leaf_token_index + 1].line_number
            and self.__leaf_tokens[self.__leaf_token_index + 1].is_leaf
        ):
            self.__leaf_token_index = self.__inline_token_index + 1
            self.__inline_token_index = self.__leaf_token_index
        if (
            self.__inline_token_index + 1 < len(self.__leaf_tokens)
            and self.__line_index
            == self.__leaf_tokens[self.__inline_token_index + 1].line_number
        ):
            self.__inline_token_index += 1

        if (
            self.__leaf_token_index < len(self.__leaf_tokens)
            and not self.__leaf_tokens[self.__leaf_token_index].is_code_block
            and line
            and line[-1] == " "
        ):
            self.__next_line_check_for_error(line, context)
        self.__line_index += 1

    def __next_line_check_for_error(
        self, line: str, context: PluginScanContext
    ) -> None:
        (
            first_non_whitespace_index,
            extracted_whitespace,
        ) = ParserHelper.extract_spaces_from_end(line)
        extracted_whitespace_length = len(extracted_whitespace)

        is_within_list = False
        new_list_indent = -1
        expected_list_indent = -1
        if self.__list_item_empty_lines_mode and first_non_whitespace_index == 0:
            leaf_token = self.__leaf_owner_tokens[self.__leaf_token_index]
            if leaf_token is not None:
                is_within_list = True
                list_owner_token = cast(ListStartMarkdownToken, leaf_token)
                expected_list_indent = (
                    list_owner_token.indent_level + self.__break_spaces
                )
                if extracted_whitespace_length != expected_list_indent:
                    new_list_indent = expected_list_indent

        if (
            not is_within_list
            and (
                extracted_whitespace_length != self.__break_spaces or self.__strict_mode
            )
            or new_list_indent != -1
        ):
            if context.in_fix_mode:
                self.__report_fix(
                    context,
                    line,
                    new_list_indent,
                    extracted_whitespace_length,
                    first_non_whitespace_index,
                )
            else:
                self.__report_error(
                    context,
                    extracted_whitespace_length,
                    first_non_whitespace_index,
                    expected_list_indent,
                )

    # pylint: disable=too-many-arguments
    def __report_fix(
        self,
        context: PluginScanContext,
        line: str,
        new_list_indent: int,
        extracted_whitespace_length: int,
        first_non_whitespace_index: int,
    ) -> None:
        if new_list_indent != -1:
            line = " " * new_list_indent
        else:
            this_leaf_token = self.__leaf_tokens[self.__leaf_token_index]
            line = (
                line[:first_non_whitespace_index]
                if (
                    extracted_whitespace_length < self.__break_spaces
                    or this_leaf_token.is_atx_heading
                    or self.__strict_mode
                )
                else line[: first_non_whitespace_index + self.__break_spaces]
            )
        context.set_current_fix_line(line)

    # pylint: enable=too-many-arguments

    def __report_error(
        self,
        context: PluginScanContext,
        extracted_whitespace_length: int,
        first_non_whitespace_index: int,
        expected_list_indent: int,
    ) -> None:
        if expected_list_indent != -1:
            extra_error_information = str(expected_list_indent)
        elif self.__strict_mode or self.__break_spaces < 2:
            extra_error_information = "0"
        else:
            extra_error_information = f"0 or {self.__break_spaces}"
        extra_error_information = f"Expected: {extra_error_information}; Actual: {extracted_whitespace_length}"
        self.report_next_line_error(
            context,
            first_non_whitespace_index + 1,
            extra_error_information=extra_error_information,
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        _ = context

        if token.is_block_quote_start or token.is_list_start:
            container_token = cast(ContainerMarkdownToken, token)
            self.__container_token_stack.append(container_token)
        elif token.is_block_quote_end or token.is_list_end:
            del self.__container_token_stack[-1]
        elif token.is_blank_line or token.is_leaf or token.is_inline_hard_break:
            self.__leaf_tokens.append(token)
            if self.__container_token_stack:
                self.__leaf_owner_tokens.append(self.__container_token_stack[-1])
            else:
                self.__leaf_owner_tokens.append(None)


# pylint: enable=too-many-instance-attributes
