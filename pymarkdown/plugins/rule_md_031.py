"""
Module to implement a plugin that ensures that blank lines surround fenced block quotes.
"""

import copy
from dataclasses import dataclass
from typing import List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetails,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.blank_line_markdown_token import BlankLineMarkdownToken
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.setext_heading_markdown_token import SetextHeadingMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


@dataclass
class ClosedContainerAdjustments:
    """
    Keep track of line space used by already closed containers.
    """

    adjustment: int = 0
    count: int = 0
    count2: int = 0


@dataclass(frozen=True)
class PendingContainerAdjustment:
    """
    Keep track of the adjustments we need to make on the container.
    """

    insert_index: int
    leading_space_to_insert: str
    do_insert: bool = True


# pylint: disable=too-many-instance-attributes
class RuleMd031(RulePlugin):
    """
    Class to implement a plugin that ensures that blank lines surround fenced block quotes.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__trigger_in_list_items: bool = True
        self.__end_fenced_code_block_token: Optional[EndMarkdownToken] = None
        self.__last_non_end_token: Optional[MarkdownToken] = None
        self.__last_token: Optional[MarkdownToken] = None
        self.__second_last_token: Optional[MarkdownToken] = None
        self.__container_token_stack: List[MarkdownToken] = []
        self.__pending_container_ends = 0
        self.__container_adjustments: List[List[PendingContainerAdjustment]] = []
        self.__closed_container_adjustments: List[ClosedContainerAdjustments] = []
        self.__end_tokens: List[EndMarkdownToken] = []
        self.__fix_count = 0
        self.__removed_container_token_stack: Optional[MarkdownToken] = None
        # self.__removed_container_adjustments = None
        # self.__removed_closed_container_adjustments = None

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="blanks-around-fences",
            plugin_id="MD031",
            plugin_enabled_by_default=True,
            plugin_description="Fenced code blocks should be surrounded by blank lines",
            plugin_version="0.7.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md031.md",
            plugin_configuration="list_items",
            plugin_supports_fix=True,
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__trigger_in_list_items = self.plugin_configuration.get_boolean_property(
            "list_items", default_value=True
        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("list_items", self.__trigger_in_list_items),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__last_non_end_token = None
        self.__last_token = None
        self.__end_fenced_code_block_token = None
        self.__container_token_stack = []
        self.__container_adjustments = []
        self.__closed_container_adjustments = []
        self.__end_tokens = []
        self.__pending_container_ends = 0
        self.__fix_count = 0

    def __fix_spacing_special_case(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        assert (
            self.__last_token is not None
        ), "Special case means at least a block token."
        new_token = copy.deepcopy(token)
        self.__fix_count += 1
        new_token.adjust_line_number(context, self.__fix_count)
        replacement_tokens = [
            BlankLineMarkdownToken(
                extracted_whitespace="", position_marker=PositionMarker(0, 0, "")
            ),
            self.__last_token,
            new_token,
        ]
        self.register_replace_tokens_request(
            context, self.__last_token, token, replacement_tokens
        )
        end_token = cast(EndMarkdownToken, self.__last_token)
        block_quote_start_token = cast(
            BlockQuoteMarkdownToken, end_token.start_markdown_token
        )
        assert (
            block_quote_start_token.bleading_spaces is not None
        ), "At least one line should have been processed."
        split_bleading_spaces = block_quote_start_token.bleading_spaces.split("\n")
        self.__container_adjustments[-1].append(
            PendingContainerAdjustment(
                len(split_bleading_spaces) - 1, split_bleading_spaces[-1].rstrip()
            )
        )

    def __fix_spacing_block_quote(self, token: MarkdownToken) -> None:
        container_index = len(self.__container_token_stack) - 1
        block_quote_token = cast(
            BlockQuoteMarkdownToken, self.__container_token_stack[container_index]
        )
        assert (
            block_quote_token.bleading_spaces is not None
        ), "At least one line should have been processed."
        split_leading_space = block_quote_token.bleading_spaces.split("\n")
        if token.is_setext_heading:
            setext_token = cast(SetextHeadingMarkdownToken, token)
            token_line_number = setext_token.original_line_number
        else:
            token_line_number = token.line_number

        leading_space_insert_index = (
            token_line_number - block_quote_token.line_number
        ) - (
            self.__closed_container_adjustments[-1].adjustment
            - self.__closed_container_adjustments[-1].count2
        )

        former_item_leading_space = split_leading_space[
            leading_space_insert_index
        ].rstrip()
        self.__container_adjustments[container_index].append(
            PendingContainerAdjustment(
                leading_space_insert_index, former_item_leading_space
            )
        )

        while (
            container_index > 0
            and not self.__container_token_stack[container_index - 1].is_list_start
        ):
            container_index -= 1

        if (
            container_index > 0
            and self.__container_token_stack[container_index - 1].is_list_start
        ):
            if token.is_setext_heading:
                setext_token = cast(SetextHeadingMarkdownToken, token)
                token_line_number = setext_token.original_line_number
            else:
                token_line_number = token.line_number
            leading_space_insert_index = (
                token_line_number
                - self.__container_token_stack[container_index - 1].line_number
            )
            self.__container_adjustments[container_index - 1].append(
                PendingContainerAdjustment(leading_space_insert_index, "")
            )

    def __fix_spacing_list(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        initial_index = container_index = len(self.__container_token_stack) - 1
        while (
            container_index >= 0
            and self.__container_token_stack[container_index - 1].is_list_start
        ):
            container_index -= 1
        if container_index >= 0:

            block_quote_index, index, ss = self.__fix_spacing_list_prefix(
                token, container_index, initial_index
            )

            assert block_quote_index.bleading_spaces is not None
            split_bleading_spaces = block_quote_index.bleading_spaces.split("\n")
            self.__container_adjustments[container_index - 1].append(
                PendingContainerAdjustment(index, split_bleading_spaces[index].rstrip())
            )
            # this may be due to a commented out test
            assert ss is None
            # self.__container_adjustments[container_index - 1].append(
            #     PendingContainerAdjustment(index, ss, do_insert=False)
            # )

        if (
            self.__removed_container_token_stack is not None
            and not self.__removed_container_token_stack.is_block_quote_start
            # and container_index
        ):
            self.__fix_spacing_list_remove_list(context)
        else:
            self.__fix_spacing_list_not_remove_list(
                initial_index, container_index, token
            )

    def __fix_spacing_list_remove_list(self, context: PluginScanContext) -> None:
        removed_list_token = cast(
            ListStartMarkdownToken, self.__removed_container_token_stack
        )
        assert removed_list_token.leading_spaces is not None
        split_spaces = removed_list_token.leading_spaces.split("\n")
        split_spaces_length = len(split_spaces)
        if split_spaces_length > 1:
            split_spaces.insert(split_spaces_length - 1, "")
        else:
            split_spaces.append("")
        assert self.__removed_container_token_stack is not None
        self.register_fix_token_request(
            context,
            self.__removed_container_token_stack,
            "next_token",
            "leading_spaces",
            "\n".join(split_spaces),
        )

    def __fix_spacing_list_not_remove_list(
        self, initial_index: int, container_index: int, token: MarkdownToken
    ) -> None:
        if self.__closed_container_adjustments[-1].adjustment:
            adjust = 2 if container_index >= 0 else 1
        else:
            adjust = self.__calculate_adjust(initial_index, container_index)
        if token.is_setext_heading:
            setext_token = cast(SetextHeadingMarkdownToken, token)
            token_line_number = setext_token.original_line_number
        else:
            token_line_number = token.line_number
        index = (
            token_line_number - self.__container_token_stack[initial_index].line_number
        )
        index -= self.__closed_container_adjustments[-1].adjustment
        self.__container_adjustments[initial_index].append(
            PendingContainerAdjustment(index - adjust, "")
        )

    def __fix_spacing_list_prefix(
        self,
        token: MarkdownToken,
        container_index: int,
        initial_index: int,
    ) -> Tuple[BlockQuoteMarkdownToken, int, Optional[str]]:
        block_quote_index = cast(
            BlockQuoteMarkdownToken,
            self.__container_token_stack[container_index - 1],
        )
        if token.is_setext_heading:
            setext_token = cast(SetextHeadingMarkdownToken, token)
            token_line_number = setext_token.original_line_number
        else:
            token_line_number = token.line_number
        index = (
            token_line_number
            - block_quote_index.line_number
            - self.__closed_container_adjustments[container_index - 1].adjustment
        )
        df = self.__closed_container_adjustments[container_index - 1].adjustment
        ff = df != 0
        if ff:
            index += self.__closed_container_adjustments[container_index - 1].count

        # ss = None
        # This may be due to a commented out test.
        assert not (
            container_index == initial_index
            and self.__last_token is not None
            and self.__last_token.is_block_quote_end
        )
        # x = cast(EndMarkdownToken, self.__last_token)
        # assert x.extra_end_data is not None
        # ss = x.extra_end_data
        # self.register_fix_token_request(
        #     context, x, "next_token", "extra_end_data", ""
        # )
        # self.__container_adjustments[container_index - 1].append(
        #     PendingContainerAdjustment(index, ss)
        # )
        return block_quote_index, index, None

    def __calculate_adjust(self, initial_index: int, container_index: int) -> int:
        if (
            initial_index >= 2
            and not container_index
            and self.__closed_container_adjustments[-1].adjustment
        ):
            return 1
        return (
            0
            if initial_index >= 1
            and not container_index
            and self.__closed_container_adjustments[-1].adjustment
            else 1
        )

    def __fix_spacing(
        self, context: PluginScanContext, token: MarkdownToken, special_case: bool
    ) -> None:
        if special_case:
            self.__fix_spacing_special_case(context, token)
            return
        if self.__container_token_stack:
            if self.__container_token_stack[-1].is_block_quote_start:
                self.__fix_spacing_block_quote(token)
            else:
                self.__fix_spacing_list(context, token)
        elif self.__removed_container_token_stack:
            if self.__removed_container_token_stack.is_list_start:
                removed_list_token = cast(
                    ListStartMarkdownToken, self.__removed_container_token_stack
                )
                if removed_list_token.leading_spaces is not None:
                    split_spaces = removed_list_token.leading_spaces.split("\n")
                    split_spaces.append("")
                else:
                    split_spaces = [""]
                self.register_fix_token_request(
                    context,
                    self.__removed_container_token_stack,
                    "next_token",
                    "leading_spaces",
                    "\n".join(split_spaces),
                )

        new_token = copy.deepcopy(token)
        self.__fix_count += 1
        new_token.adjust_line_number(context, self.__fix_count)
        assert self.__last_token is not None
        if token.is_fenced_code_block and self.__last_token.is_list_end:
            replacement_tokens: List[MarkdownToken] = [
                BlankLineMarkdownToken(
                    extracted_whitespace="",
                    position_marker=PositionMarker(new_token.line_number - 1, 0, ""),
                    column_delta=1,
                ),
                self.__last_token,
                new_token,
            ]
            self.register_replace_tokens_request(
                context, self.__last_token, token, replacement_tokens
            )
        else:
            replacement_tokens = [
                BlankLineMarkdownToken(
                    extracted_whitespace="",
                    position_marker=PositionMarker(new_token.line_number - 1, 0, ""),
                    column_delta=1,
                ),
                new_token,
            ]
            self.register_replace_tokens_request(
                context, token, token, replacement_tokens
            )

    def __handle_fenced_code_block(
        self, context: PluginScanContext, token: MarkdownToken, special_case: bool
    ) -> None:

        can_trigger = (
            self.__trigger_in_list_items
            if self.__container_token_stack
            and self.__container_token_stack[-1].is_list_start
            else True
        )
        if (
            self.__last_non_end_token
            and not self.__last_non_end_token.is_blank_line
            and can_trigger
        ):
            if context.in_fix_mode:
                self.__fix_spacing(context, token, special_case)
            else:
                self.report_next_token_error(context, token)

    def __calculate_end_deltas(self) -> Tuple[int, int]:
        line_number_delta = 0
        assert self.__last_non_end_token is not None
        if self.__last_non_end_token.is_text:
            text_token = cast(TextMarkdownToken, self.__last_non_end_token)
            line_number_delta = (
                text_token.token_text.count(ParserHelper.newline_character) + 2
            )
        else:
            assert self.__last_non_end_token.is_fenced_code_block
            line_number_delta = 1

        assert self.__end_fenced_code_block_token is not None
        column_number_delta = (
            self.__end_fenced_code_block_token.start_markdown_token.column_number
        )
        start_token = cast(
            EndMarkdownToken,
            self.__end_fenced_code_block_token.start_markdown_token,
        )
        if start_token.extracted_whitespace:
            column_number_delta -= len(start_token.extracted_whitespace)
        if (
            self.__end_fenced_code_block_token
            and self.__end_fenced_code_block_token.extracted_whitespace
        ):
            column_number_delta += len(
                self.__end_fenced_code_block_token.extracted_whitespace
            )
        column_number_delta = -(column_number_delta)

        return line_number_delta, column_number_delta

    def __handle_end_fenced_code_block(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:  # sourcery skip: extract-method
        can_trigger = not token.is_end_of_stream
        if (
            self.__container_token_stack
            and self.__container_token_stack[-1].is_list_start
        ):
            can_trigger = self.__trigger_in_list_items
        if (
            not token.is_blank_line
            and self.__end_fenced_code_block_token is not None
            and not self.__end_fenced_code_block_token.was_forced
            and can_trigger
        ):
            if context.in_fix_mode:
                self.__fix_spacing(context, token, False)
            else:
                assert self.__last_non_end_token
                line_number_delta, column_number_delta = self.__calculate_end_deltas()
                self.report_next_token_error(
                    context,
                    self.__end_fenced_code_block_token.start_markdown_token,
                    line_number_delta=line_number_delta,
                    column_number_delta=column_number_delta,
                )
        self.__end_fenced_code_block_token = None

    def __process_pending_container_end_adjustment(
        self,
        context: PluginScanContext,
        next_container_adjustment_list: List[PendingContainerAdjustment],
    ) -> None:
        if self.__container_token_stack[-1].is_block_quote_start:
            token_part_name = "bleading_spaces"
            block_quote_token = cast(
                BlockQuoteMarkdownToken, self.__container_token_stack[-1]
            )
            assert (
                block_quote_token.bleading_spaces is not None
            ), "Pending containers means this should at least have a newline in it."
            split_spaces = block_quote_token.bleading_spaces.split("\n")
        else:
            token_part_name = "leading_spaces"
            list_token = cast(ListStartMarkdownToken, self.__container_token_stack[-1])
            assert (
                list_token.leading_spaces is not None
            ), "Pending containers means this should at least have a newline in it."
            split_spaces = list_token.leading_spaces.split("\n")

        for next_container_adjustment in next_container_adjustment_list[::-1]:
            # this may be due to a commented out test
            assert next_container_adjustment.do_insert
            split_spaces.insert(
                next_container_adjustment.insert_index,
                next_container_adjustment.leading_space_to_insert,
            )
            # else:
            #     split_spaces[next_container_adjustment.insert_index] = (
            #         next_container_adjustment.leading_space_to_insert
            #     )

        self.register_fix_token_request(
            context,
            self.__container_token_stack[-1],
            "next_token",
            token_part_name,
            "\n".join(split_spaces),
        )

    def __process_pending_container_end_block_quote(self, token: MarkdownToken) -> None:
        for stack_index in range(len(self.__container_token_stack) - 2, -1, -1):
            current_stack_token = self.__container_token_stack[stack_index]
            if current_stack_token.is_block_quote_start:
                if token.is_setext_heading:
                    setext_token = cast(SetextHeadingMarkdownToken, token)
                    token_line_number = setext_token.original_line_number
                else:
                    token_line_number = token.line_number
                line_number_delta = (
                    token_line_number - self.__container_token_stack[-1].line_number
                )
                extra_end_data = self.__end_tokens[-1].extra_end_data
                if extra_end_data is not None:
                    line_number_delta += 1
                self.__closed_container_adjustments[
                    stack_index
                ].adjustment += line_number_delta
                self.__closed_container_adjustments[stack_index].count += 1
                if (
                    self.__container_token_stack[-1].is_block_quote_start
                    and cast(
                        BlockQuoteMarkdownToken, self.__container_token_stack[-1]
                    ).weird_kludge_six
                ):
                    self.__closed_container_adjustments[stack_index].count2 += 1
                break

    def __process_pending_container_end_list(self, token: MarkdownToken) -> None:
        for stack_index in range(len(self.__container_token_stack) - 2, -1, -1):
            current_stack_token = self.__container_token_stack[stack_index]
            if current_stack_token.is_list_start:
                if token.is_setext_heading:
                    setext_token = cast(SetextHeadingMarkdownToken, token)
                    token_line_number = setext_token.original_line_number
                else:
                    token_line_number = token.line_number
                line_number_delta = (
                    token_line_number - self.__container_token_stack[-1].line_number
                )
                self.__closed_container_adjustments[
                    stack_index
                ].adjustment += line_number_delta
                break

    def __process_pending_container_end(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        if context.in_fix_mode:
            if next_container_adjustment_list := self.__container_adjustments[-1]:
                self.__process_pending_container_end_adjustment(
                    context, next_container_adjustment_list
                )
            if self.__container_token_stack[-1].is_block_quote_start:
                self.__process_pending_container_end_block_quote(token)
            else:
                self.__process_pending_container_end_list(token)

        self.__removed_container_token_stack = self.__container_token_stack[-1]
        del self.__container_token_stack[-1]

        # self.__removed_container_adjustments = self.__container_adjustments[-1]
        del self.__container_adjustments[-1]

        # self.__removed_closed_container_adjustments = (
        #     self.__closed_container_adjustments[-1]
        # )
        del self.__closed_container_adjustments[-1]

        del self.__end_tokens[-1]
        self.__pending_container_ends -= 1

    def __calculate_special_case(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> bool:
        return bool(
            context.in_fix_mode
            and token.is_fenced_code_block
            and len(self.__container_token_stack) >= 2
            and self.__container_token_stack[-1].is_block_quote_start
            and self.__container_token_stack[-2].is_block_quote_start
            and self.__last_token
            and self.__second_last_token
            and self.__last_token.is_block_quote_end
            and self.__second_last_token.is_paragraph_end
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """

        special_case = self.__calculate_special_case(context, token)
        # special_case = False

        if not token.is_end_token or token.is_end_of_stream:
            while self.__pending_container_ends and not special_case:
                self.__process_pending_container_end(context, token)
            if self.__end_fenced_code_block_token:
                self.__handle_end_fenced_code_block(context, token)

        if token.is_block_quote_start or token.is_list_start:
            self.__container_token_stack.append(token)
            self.__container_adjustments.append([])
            self.__closed_container_adjustments.append(ClosedContainerAdjustments())
        elif token.is_block_quote_end or token.is_list_end:
            self.__pending_container_ends += 1
            self.__end_tokens.append(cast(EndMarkdownToken, token))
        elif token.is_fenced_code_block:
            self.__handle_fenced_code_block(context, token, special_case)
            while self.__pending_container_ends and special_case:
                self.__process_pending_container_end(context, token)
        elif token.is_fenced_code_block_end:
            self.__end_fenced_code_block_token = cast(EndMarkdownToken, token)

        if (
            not token.is_end_token
            and not token.is_block_quote_start
            and not token.is_list_start
        ):
            self.__last_non_end_token = token

        self.__second_last_token = self.__last_token
        self.__last_token = token
        self.__removed_container_token_stack = None
        # self.__removed_container_adjustments = None
        # self.__removed_closed_container_adjustments = None


# pylint: enable=too-many-instance-attributes
