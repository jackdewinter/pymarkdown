"""
Module to implement a plugin that looks for multiple blank lines in the files.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, cast

from pymarkdown.plugin_manager.plugin_details import (
    PluginDetails,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.plugins.utils.leading_space_index_tracker import (
    LeadingSpaceIndexTracker,
)
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken


@dataclass
class PendingContainerFixes:
    """Class to hold the pending fixes to be made when the container is closed."""

    leading_space_index: int
    repeat_count: int


class RuleMd012(RulePlugin):
    """
    Class to implement a plugin that looks for multiple blank lines in the files.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__blank_lines_maximum = 0
        self.__blank_line_count = 0
        self.__last_blank_line: Optional[MarkdownToken] = None
        self.__captured_blank_line: List[MarkdownToken] = []
        self.__leading_space_index_tracker = LeadingSpaceIndexTracker()
        self.__container_fix_map: Dict[MarkdownToken, List[PendingContainerFixes]] = {}

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="no-multiple-blanks",
            plugin_id="MD012",
            plugin_enabled_by_default=True,
            plugin_description="Multiple consecutive blank lines",
            plugin_version="0.7.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md012.md",
            plugin_configuration="maximum",
            plugin_supports_fix=True,
            plugin_fix_level=1,
        )

    @classmethod
    def __validate_maximum(cls, found_value: int) -> None:
        if found_value < 0:
            raise ValueError("Allowable values are any non-negative integers.")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__blank_lines_maximum = self.plugin_configuration.get_integer_property(
            "maximum",
            default_value=1,
            valid_value_fn=self.__validate_maximum,
        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [QueryConfigItem("maximum", self.__blank_lines_maximum)]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__blank_line_count = 0
        self.__last_blank_line = None
        self.__captured_blank_line.clear()
        self.__leading_space_index_tracker.clear()
        self.__container_fix_map.clear()

    def __append_to_container_fix_map(
        self, key: MarkdownToken, value: PendingContainerFixes
    ) -> None:
        if key in self.__container_fix_map:
            value_list = self.__container_fix_map[key]
        else:
            value_list = []
            self.__container_fix_map[key] = value_list
        value_list.append(value)

    def __fix_containers(self) -> None:
        outer_container_index = (
            self.__leading_space_index_tracker.get_container_stack_size() - 1
        )
        container_token = self.__leading_space_index_tracker.get_container_stack_item(
            outer_container_index
        )
        line_number_delta = (
            self.__captured_blank_line[-1].line_number
            - self.__captured_blank_line[0].line_number
        )
        if container_token.is_block_quote_start:
            leading_space_index = self.__leading_space_index_tracker.get_tokens_block_quote_bleading_space_index(
                self.__captured_blank_line[-1]
            )
            self.__append_to_container_fix_map(
                container_token,
                PendingContainerFixes(
                    leading_space_index - (line_number_delta - 1), line_number_delta
                ),
            )
            inner_container_index = outer_container_index - 1
            while (
                inner_container_index >= 0
                and self.__leading_space_index_tracker.get_container_stack_item(
                    inner_container_index
                ).is_block_quote_start
            ):
                inner_container_index -= 1
            if inner_container_index >= 0:
                leading_space_index = self.__leading_space_index_tracker.get_tokens_list_leading_space_index(
                    self.__captured_blank_line[-1], inner_container_index
                )
                container_token = (
                    self.__leading_space_index_tracker.get_container_stack_item(
                        inner_container_index
                    )
                )
                self.__append_to_container_fix_map(
                    container_token,
                    PendingContainerFixes(
                        leading_space_index - (line_number_delta - 1), line_number_delta
                    ),
                )
        else:
            leading_space_index = (
                self.__leading_space_index_tracker.get_tokens_list_leading_space_index(
                    self.__captured_blank_line[-1], outer_container_index
                )
            )
            self.__append_to_container_fix_map(
                container_token,
                PendingContainerFixes(
                    leading_space_index - (line_number_delta - 1), line_number_delta
                ),
            )
            inner_container_index = outer_container_index - 1
            while (
                inner_container_index >= 0
                and self.__leading_space_index_tracker.get_container_stack_item(
                    inner_container_index
                ).is_list_start
            ):
                inner_container_index -= 1
            if inner_container_index >= 0:
                leading_space_index = self.__leading_space_index_tracker.get_tokens_block_quote_bleading_space_index(
                    self.__captured_blank_line[-1], inner_container_index
                )
                container_token = (
                    self.__leading_space_index_tracker.get_container_stack_item(
                        inner_container_index
                    )
                )
                self.__append_to_container_fix_map(
                    container_token,
                    PendingContainerFixes(
                        leading_space_index - (line_number_delta - 1), line_number_delta
                    ),
                )

    def __check_for_excess_blank_lines(self, context: PluginScanContext) -> None:
        if self.__blank_line_count > self.__blank_lines_maximum:
            if context.in_fix_mode:
                if self.__leading_space_index_tracker.in_at_least_one_container():
                    self.__fix_containers()

                replacement_tokens = self.__captured_blank_line[:1]
                self.register_replace_tokens_request(
                    context,
                    self.__captured_blank_line[0],
                    self.__captured_blank_line[-1],
                    replacement_tokens,
                )
            else:
                assert self.__last_blank_line is not None
                extra_data = f"Expected: {self.__blank_lines_maximum}, Actual: {self.__blank_line_count}"
                self.report_next_token_error(
                    context, self.__last_blank_line, extra_error_information=extra_data
                )
        self.__captured_blank_line.clear()

    def __process_pending_container_end_fixes(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        end_token = cast(EndMarkdownToken, token)
        if end_token.start_markdown_token in self.__container_fix_map:
            value_list = self.__container_fix_map[end_token.start_markdown_token]
            if end_token.start_markdown_token.is_block_quote_start:
                block_token = cast(
                    BlockQuoteMarkdownToken, end_token.start_markdown_token
                )
                assert block_token.bleading_spaces is not None
                split_spaces = block_token.bleading_spaces.split("\n")
                token_part_name = "bleading_spaces"
            else:
                list_token = cast(
                    ListStartMarkdownToken, end_token.start_markdown_token
                )
                assert list_token.leading_spaces is not None
                split_spaces = list_token.leading_spaces.split("\n")
                token_part_name = "leading_spaces"

            while value_list:
                pending_container_fixes: PendingContainerFixes = value_list[-1]
                for _ in range(pending_container_fixes.repeat_count):
                    del split_spaces[pending_container_fixes.leading_space_index]
                del value_list[-1]

            self.register_fix_token_request(
                context,
                end_token.start_markdown_token,
                "next_token",
                token_part_name,
                "\n".join(split_spaces),
            )

    def completed_file(self, context: PluginScanContext) -> None:
        """
        Event that the file being currently scanned is now completed.
        """
        self.__check_for_excess_blank_lines(context)

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_blank_line:
            if (
                self.__last_blank_line is not None
                and (token.line_number - self.__last_blank_line.line_number) != 1
            ):
                self.__check_for_excess_blank_lines(context)
                self.__blank_line_count = 0
            self.__captured_blank_line.append(token)
            self.__last_blank_line = token
            self.__blank_line_count += 1
        else:
            if self.__blank_line_count:
                self.__check_for_excess_blank_lines(context)
            self.__blank_line_count = 0

        if token.is_block_quote_end or token.is_list_end:
            self.__process_pending_container_end_fixes(context, token)

        if token.is_block_quote_start or token.is_list_start:
            self.__leading_space_index_tracker.open_container(token)
        elif token.is_block_quote_end or token.is_list_end:
            self.__leading_space_index_tracker.register_container_end(token)
        self.__leading_space_index_tracker.track_since_last_non_end_token(token)
