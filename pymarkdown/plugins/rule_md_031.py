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
from pymarkdown.plugins.utils.leading_space_index_tracker import (
    LeadingSpaceIndexTracker,
)
from pymarkdown.tokens.blank_line_markdown_token import BlankLineMarkdownToken
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


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
        self.__container_adjustments: List[List[PendingContainerAdjustment]] = []
        self.__fix_count = 0
        self.__removed_container_stack_token: Optional[MarkdownToken] = None

        self.__leading_space_index_tracker = LeadingSpaceIndexTracker()

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
        self.__container_adjustments = []
        self.__fix_count = 0
        self.__leading_space_index_tracker.clear()

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
        leading_space_insert_index = self.__leading_space_index_tracker.get_tokens_block_quote_bleading_space_index(
            token
        )

        container_index = (
            self.__leading_space_index_tracker.get_container_stack_size() - 1
        )
        block_quote_token = cast(
            BlockQuoteMarkdownToken,
            self.__leading_space_index_tracker.get_container_stack_item(
                container_index
            ),
        )
        assert block_quote_token.bleading_spaces is not None
        split_leading_space = block_quote_token.bleading_spaces.split("\n")
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
            and not self.__leading_space_index_tracker.get_container_stack_item(
                container_index - 1
            ).is_list_start
        ):
            container_index -= 1

        if (
            container_index > 0
            and self.__leading_space_index_tracker.get_container_stack_item(
                container_index - 1
            ).is_list_start
        ):
            leading_space_insert_index = (
                LeadingSpaceIndexTracker.calculate_token_line_number(token)
                - self.__leading_space_index_tracker.get_container_stack_item(
                    container_index - 1
                ).line_number
            )
            self.__container_adjustments[container_index - 1].append(
                PendingContainerAdjustment(leading_space_insert_index, "")
            )

    def __fix_spacing_list(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        initial_index = container_index = (
            self.__leading_space_index_tracker.get_container_stack_size() - 1
        )
        while (
            container_index >= 0
            and self.__leading_space_index_tracker.get_container_stack_item(
                container_index - 1
            ).is_list_start
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
            self.__removed_container_stack_token is not None
            and not self.__removed_container_stack_token.is_block_quote_start
            # and container_index
        ):
            self.__fix_spacing_list_remove_list(context)
        else:
            self.__fix_spacing_list_not_remove_list(
                initial_index, container_index, token
            )

    def __fix_spacing_list_remove_list(self, context: PluginScanContext) -> None:
        removed_list_token = cast(
            ListStartMarkdownToken, self.__removed_container_stack_token
        )
        assert removed_list_token.leading_spaces is not None
        split_spaces = removed_list_token.leading_spaces.split("\n")
        split_spaces_length = len(split_spaces)
        if split_spaces_length > 1:
            split_spaces.insert(split_spaces_length - 1, "")
        else:
            split_spaces.append("")
        assert self.__removed_container_stack_token is not None
        self.register_fix_token_request(
            context,
            self.__removed_container_stack_token,
            "next_token",
            "leading_spaces",
            "\n".join(split_spaces),
        )

    def __fix_spacing_list_not_remove_list(
        self, initial_index: int, container_index: int, token: MarkdownToken
    ) -> None:
        last_closed_container_info = (
            self.__leading_space_index_tracker.get_closed_container_info(-1)
        )

        if last_closed_container_info.adjustment:
            adjust = 2 if container_index >= 0 else 1
        else:
            adjust = self.__calculate_adjust(initial_index, container_index)
        index = (
            LeadingSpaceIndexTracker.calculate_token_line_number(token)
            - self.__leading_space_index_tracker.get_container_stack_item(
                initial_index
            ).line_number
        )
        index -= last_closed_container_info.adjustment
        index -= adjust
        self.__container_adjustments[initial_index].append(
            PendingContainerAdjustment(index, "")
        )

    def __fix_spacing_list_prefix(
        self,
        token: MarkdownToken,
        container_index: int,
        initial_index: int,
    ) -> Tuple[BlockQuoteMarkdownToken, int, Optional[str]]:
        block_quote_index = cast(
            BlockQuoteMarkdownToken,
            self.__leading_space_index_tracker.get_container_stack_item(
                container_index - 1
            ),
        )

        current_closed_container_info = (
            self.__leading_space_index_tracker.get_closed_container_info(
                container_index - 1
            )
        )

        index = (
            LeadingSpaceIndexTracker.calculate_token_line_number(token)
            - block_quote_index.line_number
            - current_closed_container_info.adjustment
        )
        if current_closed_container_info.adjustment != 0:
            index += current_closed_container_info.count

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

        last_closed_container_info = (
            self.__leading_space_index_tracker.get_closed_container_info(-1)
        )
        assert (
            initial_index < 2
            or container_index
            or not last_closed_container_info.adjustment
        )
        return (
            0
            if initial_index >= 1
            and not container_index
            and last_closed_container_info.adjustment
            else 1
        )

    def __fix_spacing(
        self, context: PluginScanContext, token: MarkdownToken, special_case: bool
    ) -> None:
        if special_case:
            self.__fix_spacing_special_case(context, token)
            return
        if self.__leading_space_index_tracker.in_at_least_one_container():
            if self.__leading_space_index_tracker.get_container_stack_item(
                -1
            ).is_block_quote_start:
                self.__fix_spacing_block_quote(token)
            else:
                self.__fix_spacing_list(context, token)
        elif self.__removed_container_stack_token:
            if self.__removed_container_stack_token.is_list_start:
                removed_list_token = cast(
                    ListStartMarkdownToken, self.__removed_container_stack_token
                )
                assert removed_list_token.leading_spaces is None
                # if removed_list_token.leading_spaces is not None:
                #     split_spaces = removed_list_token.leading_spaces.split("\n")
                #     split_spaces.append("")
                # else:
                split_spaces = [""]
                self.register_fix_token_request(
                    context,
                    self.__removed_container_stack_token,
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
            if self.__leading_space_index_tracker.in_at_least_one_container()
            and self.__leading_space_index_tracker.get_container_stack_item(
                -1
            ).is_list_start
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
            self.__leading_space_index_tracker.in_at_least_one_container()
            and self.__leading_space_index_tracker.get_container_stack_item(
                -1
            ).is_list_start
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
        if self.__leading_space_index_tracker.get_container_stack_item(
            -1
        ).is_block_quote_start:
            token_part_name = "bleading_spaces"
            block_quote_token = cast(
                BlockQuoteMarkdownToken,
                self.__leading_space_index_tracker.get_container_stack_item(-1),
            )
            assert (
                block_quote_token.bleading_spaces is not None
            ), "Pending containers means this should at least have a newline in it."
            split_spaces = block_quote_token.bleading_spaces.split("\n")
        else:
            token_part_name = "leading_spaces"
            list_token = cast(
                ListStartMarkdownToken,
                self.__leading_space_index_tracker.get_container_stack_item(-1),
            )
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
            self.__leading_space_index_tracker.get_container_stack_item(-1),
            "next_token",
            token_part_name,
            "\n".join(split_spaces),
        )

    def __process_pending_container_end_tokens(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        while self.__leading_space_index_tracker.have_any_registered_container_ends():
            if context.in_fix_mode:
                if next_container_adjustment_list := self.__container_adjustments[-1]:
                    self.__process_pending_container_end_adjustment(
                        context, next_container_adjustment_list
                    )

            self.__removed_container_stack_token = (
                self.__leading_space_index_tracker.process_container_end(token)
            )
            del self.__container_adjustments[-1]

    def __calculate_special_case(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> bool:
        return bool(
            context.in_fix_mode
            and token.is_fenced_code_block
            and self.__leading_space_index_tracker.get_container_stack_size() >= 2
            and self.__leading_space_index_tracker.get_container_stack_item(
                -1
            ).is_block_quote_start
            and self.__leading_space_index_tracker.get_container_stack_item(
                -2
            ).is_block_quote_start
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

        if not token.is_end_token or token.is_end_of_stream:
            if not special_case:
                self.__process_pending_container_end_tokens(context, token)
            if self.__end_fenced_code_block_token:
                self.__handle_end_fenced_code_block(context, token)

        if token.is_block_quote_start or token.is_list_start:
            self.__container_adjustments.append([])
            self.__leading_space_index_tracker.open_container(token)
        elif token.is_block_quote_end or token.is_list_end:
            self.__leading_space_index_tracker.register_container_end(token)
        elif token.is_fenced_code_block:
            self.__handle_fenced_code_block(context, token, special_case)
            if special_case:
                self.__process_pending_container_end_tokens(context, token)
        elif token.is_fenced_code_block_end:
            self.__end_fenced_code_block_token = cast(EndMarkdownToken, token)

        self.__leading_space_index_tracker.track_since_last_non_end_token(token)

        if (
            not token.is_end_token
            and not token.is_block_quote_start
            and not token.is_list_start
        ):
            self.__last_non_end_token = token

        self.__second_last_token = self.__last_token
        self.__last_token = token
        self.__removed_container_stack_token = None


# pylint: enable=too-many-instance-attributes
