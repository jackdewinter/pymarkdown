"""
Module to implement a plugin that
"""

from typing import List, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetailsV2,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.plugins.utils.container_token_manager import ContainerTokenManager
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RulePml101(RulePlugin):
    """
    Class to implement a plugin that
    """

    def __init__(self) -> None:
        super().__init__()
        self.__indent_basis = 0
        self.__container_manager = ContainerTokenManager()

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="list-anchored-indent",
            plugin_id="PML101",
            plugin_enabled_by_default=False,
            plugin_description="Anchored list indentation",
            plugin_version="0.6.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_pml101.md",
            plugin_configuration="indent",
            plugin_supports_fix=False,
            plugin_fix_level=3,
        )

    @classmethod
    def __validate_configuration_indent(cls, found_value: int) -> None:
        if found_value < 3 or found_value > 5:
            raise ValueError(
                "Allowable values are between 3 and 5."
            )  # pragma: no cover

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__indent_basis = (
            self.plugin_configuration.get_integer_property_with_default(
                "indent",
                4,
                valid_value_fn=self.__validate_configuration_indent,
            )
        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("indent", self.__indent_basis),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__container_manager.clear()

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_list_start or token.is_new_list_item:
            self.__check(context, token)

        self.__container_manager.manage_container_tokens(token)

    def __calculate_base_column_block_quote(
        self, stack_index: int, container_base_column: int, block_quote_base: int
    ) -> Tuple[int, int]:
        block_quote_token = cast(
            BlockQuoteMarkdownToken,
            self.__container_manager.container_token_stack[stack_index],
        )
        bq_index = self.__container_manager.bq_line_index[stack_index + 1]
        assert block_quote_token.bleading_spaces is not None
        split_leading_spaces = block_quote_token.bleading_spaces.split(
            ParserHelper.newline_character
        )
        if not block_quote_base:
            block_quote_base = container_base_column + len(
                split_leading_spaces[bq_index]
            )
        container_base_column += len(split_leading_spaces[bq_index])
        return container_base_column, block_quote_base

    def __calculate_base_column(self) -> Tuple[int, int, int]:
        container_base_column = 0
        block_quote_base = 0
        list_depth = 0
        if self.__container_manager.container_token_stack:
            stack_index = len(self.__container_manager.container_token_stack) - 1
            while (
                stack_index >= 0
                and self.__container_manager.container_token_stack[
                    stack_index
                ].is_list_start
            ):
                list_depth += 1
                stack_index -= 1
            while stack_index >= 0:
                if self.__container_manager.container_token_stack[
                    stack_index
                ].is_block_quote_start:
                    (
                        container_base_column,
                        block_quote_base,
                    ) = self.__calculate_base_column_block_quote(
                        stack_index, container_base_column, block_quote_base
                    )
                stack_index -= 1
        return container_base_column, block_quote_base, list_depth

    # def __check_apply_fix(
    #     self,
    #     context: PluginScanContext,
    #     token: MarkdownToken,
    #     adjusted_column_number: int,
    #     calculated_column_number: int,
    # ) -> None:
    #     list_token = cast(ListStartMarkdownToken, token)

    #     # column_delta is the space before the list start and follow_space_delta
    #     # is the space following the list start, before the list text commences.
    #     column_delta = adjusted_column_number - calculated_column_number
    #     follow_space_delta = (list_token.indent_level - list_token.column_number) - 1

    #     assert len(list_token.extracted_whitespace) >= column_delta
    #     adjusted_whitespace = list_token.extracted_whitespace[:-column_delta]

    #     self.register_fix_token_request(
    #         context,
    #         token,
    #         "next_token",
    #         "extracted_whitespace",
    #         adjusted_whitespace,
    #     )
    #     self.register_fix_token_request(
    #         context,
    #         token,
    #         "next_token",
    #         "indent_level",
    #         list_token.indent_level - column_delta - follow_space_delta,
    #     )
    #     if not token.is_new_list_item:
    #         self.register_fix_token_request(
    #             context,
    #             token,
    #             "next_token",
    #             "column_number",
    #             list_token.column_number - column_delta,
    #         )
    #         if list_token.leading_spaces:
    #             new_spaces = []
    #             total_delta = column_delta + follow_space_delta
    #             for i in list_token.leading_spaces.split("\n"):
    #                 if len(i) >= list_token.indent_level:
    #                     i = i[:-total_delta]
    #                 new_spaces.append(i)
    #             self.register_fix_token_request(
    #                 context,
    #                 list_token,
    #                 "next_token",
    #                 "leading_spaces",
    #                 "\n".join(new_spaces),
    #             )

    def __check(self, context: PluginScanContext, token: MarkdownToken) -> None:

        (
            container_base_column,
            block_quote_base,
            list_depth,
        ) = self.__calculate_base_column()

        if token.is_new_list_item:
            list_depth -= 1

        adjusted_column_number = token.column_number - 1 - container_base_column
        calculated_column_number = list_depth * self.__indent_basis
        if adjusted_column_number != calculated_column_number:
            # if context.in_fix_mode:
            #     self.__check_apply_fix(
            #         context, token, adjusted_column_number, calculated_column_number
            #     )
            # else:
            if block_quote_base:
                container_base_column -= block_quote_base
            # elif container_base_column:
            #     container_base_column += 1
            extra_error_information = (
                f"Expected: {calculated_column_number + container_base_column}, "
                + f"Actual={adjusted_column_number + container_base_column}"
            )
            self.report_next_token_error(
                context, token, extra_error_information=extra_error_information
            )
