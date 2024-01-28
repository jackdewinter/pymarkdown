"""
Module to implement a plugin that looks for trailing spaces in the files.
"""

from typing import List, Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails, PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.container_markdown_token import ContainerMarkdownToken
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
        return PluginDetailsV2(
            plugin_name="no-trailing-spaces",
            plugin_id="MD009",
            plugin_enabled_by_default=True,
            plugin_description="Trailing spaces",
            plugin_version="0.5.1",
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md009.md",
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
        self.__break_spaces = self.plugin_configuration.get_integer_property(
            "br_spaces",
            default_value=2,
            valid_value_fn=self.__validate_break_spaces,
        )
        if self.__break_spaces < 2:
            self.__break_spaces = 0

        self.__strict_mode = self.plugin_configuration.get_boolean_property(
            "strict",
            default_value=False,
        )

        self.__list_item_empty_lines_mode = (
            self.plugin_configuration.get_boolean_property(
                "list_item_empty_lines",
                default_value=False,
            )
        )

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

    def __report_error(
        self,
        context: PluginScanContext,
        extracted_whitespace_length: int,
        first_non_whitespace_index: int,
    ) -> None:
        if self.__strict_mode or self.__break_spaces < 2:
            extra_error_information = "0"
        else:
            extra_error_information = f"0 or {self.__break_spaces}"
        extra_error_information = f"Expected: {extra_error_information}; Actual: {extracted_whitespace_length}"
        self.report_next_line_error(
            context,
            first_non_whitespace_index + 1,
            extra_error_information=extra_error_information,
        )

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
            not self.__leaf_tokens[self.__leaf_token_index].is_code_block
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

        is_list_empty_line = False
        leaf_token = self.__leaf_owner_tokens[self.__leaf_token_index]
        if leaf_token is not None:
            is_list_empty_line = (
                self.__list_item_empty_lines_mode
                and leaf_token.is_list_start
                and first_non_whitespace_index == 0
            )

        if extracted_whitespace_length != self.__break_spaces or (
            self.__strict_mode and not is_list_empty_line
        ):
            if context.in_fix_mode:
                this_leaf_token = self.__leaf_tokens[self.__leaf_token_index]

                if (
                    extracted_whitespace_length < self.__break_spaces
                    or this_leaf_token.is_atx_heading
                ):
                    line = line[:first_non_whitespace_index]
                else:
                    line = line[: first_non_whitespace_index + self.__break_spaces]
                context.set_current_fix_line(line)
            else:
                self.__report_error(
                    context, extracted_whitespace_length, first_non_whitespace_index
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
