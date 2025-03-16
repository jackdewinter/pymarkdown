"""
Module to implement a plugin that ensures that blank lines surround fenced block quotes.
"""

import copy
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
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

# pylint: disable=too-many-lines


@dataclass(frozen=True)
class PendingContainerAdjustment:
    """
    Keep track of the adjustments we need to make on the container.
    """

    insert_index: int
    leading_space_to_insert: str
    do_insert: bool = True
    do_special: bool = False


@dataclass
class Fixer:
    """
    Keep track of fixes that need to be applied.
    """

    token: MarkdownToken
    plugin_action: str
    field_name: str
    field_value: Union[str, int]


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
        self.__container_x: List[int] = []

        self.__fix_count = 0
        self.__removed_container_stack_token: Optional[MarkdownToken] = None
        self.__x1: List[MarkdownToken] = []
        self.__x2: List[List[PendingContainerAdjustment]] = []
        self.__x3: List[int] = []
        self.__x4: List[EndMarkdownToken] = []
        self.__x5: List[EndMarkdownToken] = []
        self.__removed_container_adjustments: Optional[
            List[PendingContainerAdjustment]
        ] = None
        self.__last_end_container_tokens: List[MarkdownToken] = []

        self.__fix_requests: List[Fixer] = []

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
        self.__container_x = []
        self.__fix_count = 0
        self.__leading_space_index_tracker.clear()
        self.__removed_container_adjustments = None
        self.__removed_container_stack_token = None
        self.__x1.clear()
        self.__x2.clear()
        self.__x3.clear()
        self.__x4.clear()
        self.__x5.clear()

    def __xabc(self, context: PluginScanContext, token: MarkdownToken) -> None:
        assert (
            self.__last_token is not None
        ), "Special case means at least a block token."
        new_token = copy.deepcopy(token)
        self.__fix_count += 1
        new_token.adjust_line_number(context, self.__fix_count)
        last_token_before_code_block = self.__last_token

        # because this is the special handling, from __calculate_special_case, we know that
        # we must have 2 block quotes.
        search_index = self.__leading_space_index_tracker.get_container_stack_size() - 3
        while search_index >= 0:
            stack_token = self.__leading_space_index_tracker.get_container_stack_item(
                search_index
            )
            if stack_token.is_list_start:
                self.__container_adjustments[search_index].append(
                    PendingContainerAdjustment(0, "")
                )
                assert self.__last_token.is_end_token
                old_end_token = cast(EndMarkdownToken, self.__last_token)
                last_token_before_code_block = EndMarkdownToken(
                    old_end_token.type_name,
                    old_end_token.extracted_whitespace,
                    "",
                    old_end_token.start_markdown_token,
                    old_end_token.was_forced,
                    old_end_token.line_number,
                    old_end_token.column_number,
                )
                break
            search_index -= 1

        replacement_tokens = [
            BlankLineMarkdownToken(
                extracted_whitespace="",
                position_marker=PositionMarker(new_token.line_number - 1, 0, ""),
            ),
            last_token_before_code_block,
            new_token,
        ]
        self.register_replace_tokens_request(
            context, self.__last_token, token, replacement_tokens
        )

    def __fix_spacing_special_case(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:

        self.__xabc(context, token)
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

    def __fix_spacing_special_case2(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        """
        This is another special case where we have to do things long-form.
        """
        assert (
            self.__last_token is not None
        ), "Special case means at least a block token."
        assert (
            self.__last_token is not None
        ), "Special case means at least a block token."
        new_token = copy.deepcopy(token)
        self.__fix_count += 1
        new_token.adjust_line_number(context, self.__fix_count)

        assert self.__second_last_token is not None
        replacement_tokens = [
            BlankLineMarkdownToken(
                extracted_whitespace="",
                position_marker=PositionMarker(new_token.line_number - 1, 0, ""),
            ),
            self.__second_last_token,
            self.__last_token,
            new_token,
        ]
        self.register_replace_tokens_request(
            context, self.__second_last_token, token, replacement_tokens
        )

        end_token = cast(EndMarkdownToken, self.__second_last_token)
        stack_token = self.__leading_space_index_tracker.get_container_stack_item(-1)
        assert stack_token == end_token.start_markdown_token
        list_start_token = cast(ListStartMarkdownToken, stack_token)
        assert (
            list_start_token.leading_spaces is not None
        ), "At least one line should have been processed."
        split_leading_spaces = list_start_token.leading_spaces.split("\n")
        self.__container_adjustments[-1].append(
            PendingContainerAdjustment(
                len(split_leading_spaces) - 1,
                split_leading_spaces[-1].rstrip(),
                do_insert=False,
            )
        )

        end_token = cast(EndMarkdownToken, self.__last_token)
        stack_token = self.__leading_space_index_tracker.get_container_stack_item(-2)
        assert stack_token == end_token.start_markdown_token
        block_quote_start_token = cast(
            BlockQuoteMarkdownToken, end_token.start_markdown_token
        )
        assert (
            block_quote_start_token.bleading_spaces is not None
        ), "At least one line should have been processed."
        split_bleading_spaces = block_quote_start_token.bleading_spaces.split("\n")
        self.__container_adjustments[-2].append(
            PendingContainerAdjustment(
                len(split_bleading_spaces) - 1,
                split_bleading_spaces[-1].rstrip(),
                do_insert=False,
            )
        )

        stack_token = self.__leading_space_index_tracker.get_container_stack_item(-3)
        list_start_token = cast(ListStartMarkdownToken, stack_token)
        assert (
            list_start_token.leading_spaces is not None
        ), "At least one line should have been processed."
        split_leading_spaces = list_start_token.leading_spaces.split("\n")
        self.__container_adjustments[-3].append(
            PendingContainerAdjustment(
                len(split_bleading_spaces) - 1, split_leading_spaces[-1]
            )
        )

        stack_token = self.__leading_space_index_tracker.get_container_stack_item(-4)
        block_quote_start_token = cast(BlockQuoteMarkdownToken, stack_token)
        assert (
            block_quote_start_token.bleading_spaces is not None
        ), "At least one line should have been processed."
        split_bleading_spaces = block_quote_start_token.bleading_spaces.split("\n")
        self.__container_adjustments[-4].append(
            PendingContainerAdjustment(
                len(split_bleading_spaces) - 1,
                split_bleading_spaces[-1],
                do_special=True,
            )
        )

    def __abc(self, context: PluginScanContext) -> Tuple[bool, int]:
        apply_rstrip = True
        delayed_container_x_adjustment = 0
        if (
            len(self.__x1) >= 3
            and self.__x1[0].is_list_start
            and self.__x1[1].is_block_quote_start
        ):
            self.__apply_tailing_block_quote_fix(1, context)
            apply_rstrip = False
            if self.__x1[2].is_block_quote_start:
                delayed_container_x_adjustment = -1
        elif (
            len(self.__x1) >= 3
            and self.__x1[0].is_list_start
            and self.__x1[1].is_list_start
            and self.__x1[2].is_block_quote_start
        ):
            self.__apply_tailing_block_quote_fix(2, context)
            apply_rstrip = False
            delayed_container_x_adjustment = -1
        elif (
            len(self.__x1) >= 3
            and self.__x1[0].is_block_quote_start
            and self.__x1[1].is_list_start
            and self.__x1[2].is_list_start
        ):
            self.__apply_tailing_block_quote_fix(0, context)
            apply_rstrip = False
            delayed_container_x_adjustment = -1
        elif len(self.__x1) >= 2 and self.__x1[0].is_block_quote_start:
            self.__apply_tailing_block_quote_fix(0, context)
        return apply_rstrip, delayed_container_x_adjustment

    def __fix_spacing_block_quote(
        self, context: PluginScanContext, token: MarkdownToken, upgrade_kludge: bool
    ) -> None:
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

        leading_space_insert_index = self.__leading_space_index_tracker.get_tokens_block_quote_bleading_space_index(
            token
        )
        former_item_leading_space = split_leading_space[leading_space_insert_index]
        apply_rstrip = True
        delayed_container_x_adjustment = 0
        if (
            leading_space_insert_index == len(split_leading_space) - 1
            and not former_item_leading_space
            and leading_space_insert_index
        ):
            former_item_leading_space = split_leading_space[
                leading_space_insert_index - 1
            ]
        elif (
            leading_space_insert_index == -1
            and len(self.__x1) >= 2
            and self.__x1[0].is_block_quote_start
            and self.__container_x
        ):
            leading_space_insert_index, upgrade_kludge, former_item_leading_space = (
                self.__fix_spacing_block_quote_1()
            )
        else:
            apply_rstrip, delayed_container_x_adjustment = self.__abc(context)

        if not upgrade_kludge and apply_rstrip:
            former_item_leading_space = former_item_leading_space.rstrip()
        self.__container_adjustments[container_index].append(
            PendingContainerAdjustment(
                leading_space_insert_index + self.__container_x[container_index],
                former_item_leading_space,
                do_special=upgrade_kludge,
            )
        )
        self.__fix_spacing_block_quote_end(token, container_index)
        self.__container_x[-1] += delayed_container_x_adjustment

    def __fix_spacing_block_quote_1(self) -> Tuple[int, bool, str]:
        end_token = self.__x4[0]
        assert end_token.start_markdown_token == self.__x1[0]
        assert end_token.extra_end_data
        self.__fix_requests.append(
            Fixer(
                end_token,
                "next_token",
                "extra_end_data",
                end_token.extra_end_data.rstrip(),
            )
        )
        leading_space_insert_index = 0
        former_item_leading_space = end_token.extra_end_data

        block_quote_token = cast(
            BlockQuoteMarkdownToken, end_token.start_markdown_token
        )
        assert block_quote_token.bleading_spaces is not None
        xxx = block_quote_token.bleading_spaces.split("\n")
        xxx[-1] = xxx[-1].rstrip()

        self.__fix_requests.append(
            Fixer(
                end_token.start_markdown_token,
                "next_token",
                "bleading_spaces",
                "\n".join(xxx),
            )
        )

        upgrade_kludge = True
        self.__container_x[-1] += 1
        return leading_space_insert_index, upgrade_kludge, former_item_leading_space

    def __fix_spacing_block_quote_end(
        self, token: MarkdownToken, container_index: int
    ) -> None:

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

    def __fix_spacing_list_special(
        self,
        context: PluginScanContext,
        list_token_mod_index: int,
        previous_block_quote_index: int,
    ) -> None:
        _ = context
        end_adj = self.__removed_container_adjustments
        assert not end_adj

        outer_block_quote_token = cast(
            BlockQuoteMarkdownToken, self.__removed_container_stack_token
        )
        assert outer_block_quote_token.bleading_spaces is not None
        assert (
            outer_block_quote_token.bleading_spaces[-1] == " "
            and outer_block_quote_token.bleading_spaces[-2] == ">"
        )
        stripped_bleading_spaces = outer_block_quote_token.bleading_spaces[:-1]
        self.__fix_requests.append(
            Fixer(
                outer_block_quote_token,
                "next_token",
                "bleading_spaces",
                stripped_bleading_spaces,
            )
        )

        current_list_token = (
            self.__leading_space_index_tracker.get_container_stack_item(-1)
        )
        inner_block_quote_token = (
            self.__leading_space_index_tracker.get_container_stack_item(
                previous_block_quote_index
            )
        )
        adjusted_indent_level = cast(
            ListStartMarkdownToken, current_list_token
        ).indent_level - (inner_block_quote_token.column_number + 1)

        self.__container_adjustments[-1].append(
            PendingContainerAdjustment(list_token_mod_index, "")
        )
        self.__container_adjustments[-1].append(
            PendingContainerAdjustment(
                list_token_mod_index, " " * adjusted_indent_level, do_insert=False
            )
        )

        leading_space_to_insert = "> "
        remaining_index = previous_block_quote_index - 1
        if remaining_index >= 0:
            assert remaining_index == 0
            container_stack_token = (
                self.__leading_space_index_tracker.get_container_stack_item(
                    remaining_index
                )
            )
            if container_stack_token.is_list_start:
                list_start_token = cast(ListStartMarkdownToken, container_stack_token)
                leading_space_to_insert = (
                    " " * list_start_token.indent_level
                ) + leading_space_to_insert
            else:
                # block_quote_token = cast(BlockQuoteMarkdownToken, container_stack_token)
                leading_space_to_insert = f"> {leading_space_to_insert}"
        block_quote_mod_index = (
            outer_block_quote_token.line_number
            - inner_block_quote_token.line_number
            + 1
        )
        self.__container_adjustments[previous_block_quote_index].append(
            PendingContainerAdjustment(block_quote_mod_index, leading_space_to_insert)
        )

    def __fix_spacing_list_detect_special(
        self, token: MarkdownToken
    ) -> Tuple[bool, int, int]:
        if (
            self.__removed_container_stack_token
            and self.__removed_container_stack_token.is_block_quote_start
        ):

            initial_index = (
                self.__leading_space_index_tracker.get_container_stack_size() - 1
            )

            list_token = self.__leading_space_index_tracker.get_container_stack_item(
                initial_index
            )
            assert list_token.is_list_start
            leading_spaces = cast(ListStartMarkdownToken, list_token).leading_spaces
            assert leading_spaces is not None
            split_spaces = leading_spaces.split("\n")

            # last_closed_container_info = (
            #     self.__leading_space_index_tracker.get_closed_container_info(-1)
            # )

            # if last_closed_container_info.adjustment:
            adjust = 1
            # else:
            #     adjust = self.__calculate_adjust(initial_index, container_index)
            index = (
                LeadingSpaceIndexTracker.calculate_token_line_number(token)
                - self.__leading_space_index_tracker.get_container_stack_item(
                    initial_index
                ).line_number
            )
            # index -= last_closed_container_info.adjustment
            index -= adjust
            # SNAFU6?
            xx = self.__leading_space_index_tracker.get_tokens_list_leading_space_index(
                token
            )
            selected_leading_space = split_spaces[xx]
            if selected_leading_space.endswith(ParserLogger.blah_sequence):
                stack_index = initial_index - 1
                while (
                    stack_index >= 0
                    and not self.__leading_space_index_tracker.get_container_stack_item(
                        stack_index
                    ).is_block_quote_start
                ):
                    stack_index -= 1
                assert stack_index >= 0
                return True, stack_index, xx
        return False, -1, -1

    def __fix_spacing_list(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> Tuple[bool, bool]:
        is_special, stack_index, index = self.__fix_spacing_list_detect_special(token)
        if is_special:
            self.__fix_spacing_list_special(context, index, stack_index)
            return True, False

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

            block_quote_index, index, _ = self.__fix_spacing_list_prefix(
                context, token, container_index, initial_index
            )

            assert block_quote_index.bleading_spaces is not None
            split_bleading_spaces = block_quote_index.bleading_spaces.split("\n")
            self.__container_adjustments[container_index - 1].append(
                PendingContainerAdjustment(index, split_bleading_spaces[index].rstrip())
            )
            # this may be due to a commented out test
            # Above, __fix_spacing_list_prefix has a third return value of ss
            # assert ss is None
            # self.__container_adjustments[container_index - 1].append(
            #     PendingContainerAdjustment(index, ss, do_insert=False)
            # )

        kludge_alpha = False
        if (
            self.__removed_container_stack_token is not None
            and not self.__removed_container_stack_token.is_block_quote_start
            # and container_index
        ):
            kludge_alpha = self.__fix_spacing_list_remove_list(context, token)
        else:
            self.__fix_spacing_list_not_remove_list(
                initial_index, container_index, token
            )
        return False, kludge_alpha

    def __xxabc(self, split_spaces: List[str]) -> bool:
        xxxxx = split_spaces.pop(-1)
        split_spaces.append("")
        search_index = 0
        self.__container_adjustments[search_index].append(
            PendingContainerAdjustment(0, xxxxx)
        )
        return True

    # pylint: disable=too-many-boolean-expressions
    def __fix_spacing_list_remove_list_kludge(self, token: MarkdownToken) -> bool:
        if (
            len(self.__x1) == 2
            and self.__x1[0].is_list_start
            and self.__x1[1].is_list_start
            and self.__leading_space_index_tracker.get_container_stack_size() == 2
            and self.__leading_space_index_tracker.get_container_stack_item(
                0
            ).is_block_quote_start
            and self.__leading_space_index_tracker.get_container_stack_item(
                1
            ).is_list_start
        ):
            list_token = cast(ListStartMarkdownToken, self.__x1[0])
            assert list_token.leading_spaces is not None
            split_leading_spaces = list_token.leading_spaces.split("\n")
            split_leading_spaces.insert(self.__x3[0] - 1, "")
            self.__leading_space_index_tracker.nudge_list_container(
                token, nudge_positive=False
            )
            self.__fix_requests.append(
                Fixer(
                    self.__x1[0],
                    "next_token",
                    "leading_spaces",
                    "\n".join(split_leading_spaces),
                )
            )
            return False
        return True

    # pylint: enable=too-many-boolean-expressions

    def __fix_spacing_list_remove_list(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> bool:
        _ = context
        if not self.__fix_spacing_list_remove_list_kludge(token):
            return False

        xx = self.__removed_container_stack_token
        removed_list_token = cast(ListStartMarkdownToken, xx)
        if removed_list_token.leading_spaces is None:
            return False

        kludge_alpha = False
        split_spaces = removed_list_token.leading_spaces.split("\n")
        split_spaces_length = len(split_spaces)
        if split_spaces_length > 1:

            if len(self.__x3) > 1 and self.__x3[-1] < split_spaces_length:
                assert self.__x3[-1] == split_spaces_length - 1
                kludge_alpha = self.__xxabc(split_spaces)
            else:
                split_spaces.insert(split_spaces_length - 1, "")
        else:
            if (
                len(self.__x1) == 3
                and self.__x1[0].is_list_start
                and self.__x1[1].is_block_quote_start
                and self.__x1[2].is_list_start
            ):
                assert self.__x3[-1] == split_spaces_length
                kludge_alpha = self.__xxabc(split_spaces)
            split_spaces.append("")
        assert removed_list_token is not None
        self.__fix_requests.append(
            Fixer(
                removed_list_token,
                "next_token",
                "leading_spaces",
                "\n".join(split_spaces),
            )
        )
        return kludge_alpha

    def __xx(self, container_index: int, initial_index: int) -> Tuple[bool, int, int]:
        continue_processing = True
        adjust = 0
        adj2 = 0
        if container_index == -1:
            if (
                len(self.__x1) == 2
                and self.__x1[0].is_list_start
                and self.__x1[1].is_block_quote_start
            ):
                adjust = 1
                adj2 = 1
                continue_processing = False
            elif (
                len(self.__x1) == 3
                and self.__x1[0].is_list_start
                and self.__x1[1].is_block_quote_start
                and self.__x1[2].is_block_quote_start
            ):
                adjust = 1
                adj2 = 1
                continue_processing = False
            elif (
                len(self.__x1) == 3
                and self.__x1[0].is_block_quote_start
                and self.__x1[1].is_list_start
                and self.__x1[2].is_block_quote_start
            ):
                self.__xx1(initial_index)
                continue_processing = False
                adjust = 1
        return continue_processing, adjust, adj2

    def __xx1(self, initial_index: int) -> None:
        gh = cast(ListStartMarkdownToken, self.__x1[1]).leading_spaces
        assert gh is not None
        split_spaces = gh.split("\n")
        assert self.__x3[1] == len(split_spaces) - 1
        sdf = split_spaces[-1]
        del split_spaces[-1]
        # split_spaces.append("")
        self.__fix_requests.append(
            Fixer(
                self.__x1[1],
                "next_token",
                "leading_spaces",
                "\n".join(split_spaces),
            )
        )
        self.__container_adjustments[initial_index].append(
            PendingContainerAdjustment(0, sdf, do_special=True)
        )

    def __fix_spacing_list_not_remove_list(
        self, initial_index: int, container_index: int, token: MarkdownToken
    ) -> None:
        last_closed_container_info = (
            self.__leading_space_index_tracker.get_closed_container_info(-1)
        )

        continue_processing, adjust, adj2 = self.__xx(container_index, initial_index)
        if continue_processing:
            if last_closed_container_info.adjustment:
                adjust = 2 if container_index >= 0 else 1
            else:
                adjust = self.__calculate_adjust(initial_index, container_index)
        if not continue_processing:
            last_closed_container_info.adjustment += adj2
        index = (
            LeadingSpaceIndexTracker.calculate_token_line_number(token)
            - self.__leading_space_index_tracker.get_container_stack_item(
                initial_index
            ).line_number
        )
        index -= (
            last_closed_container_info.adjustment
            + last_closed_container_info.list_nudge_count
        )
        index -= adjust
        if index < 0:
            index = 0
            self.__leading_space_index_tracker.nudge_list_container(
                token, nudge_positive=False
            )
        self.__container_adjustments[initial_index].append(
            PendingContainerAdjustment(index, "")
        )

    def __fix_spacing_list_prefix(
        self,
        context: PluginScanContext,
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
        #             # SNAFU6?

        # IF
        assert not (
            container_index == initial_index
            and self.__last_token is not None
            and self.__last_token.is_block_quote_end
        )
        _ = context
        ss = None
        # if (
        #     container_index == initial_index
        #     and self.__last_token is not None
        #     and self.__last_token.is_block_quote_end
        # ):
        #     x = cast(EndMarkdownToken, self.__last_token)
        #     if x.extra_end_data is not None:
        #         ss = x.extra_end_data
        #         self.register_fix_token_request(
        #             context, x, "next_token", "extra_end_data", ""
        #         )
        #         self.__container_adjustments[container_index - 1].append(
        #             PendingContainerAdjustment(index, ss)
        #         )
        return block_quote_index, index, ss

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

    def __fix_spacing_one_container(
        self, context: PluginScanContext, token: MarkdownToken, upgrade_kludge: bool
    ) -> Tuple[bool, bool]:
        did_special_list_fix = False
        kludge_alpha = False
        if self.__leading_space_index_tracker.get_container_stack_item(
            -1
        ).is_block_quote_start:
            self.__fix_spacing_block_quote(context, token, upgrade_kludge)
        else:
            did_special_list_fix, kludge_alpha = self.__fix_spacing_list(context, token)
        return did_special_list_fix, kludge_alpha

    def __fix_spacing_removed_container(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        _ = (token, context)
        assert self.__removed_container_stack_token is not None
        if self.__removed_container_stack_token.is_list_start:
            removed_list_token = cast(
                ListStartMarkdownToken, self.__removed_container_stack_token
            )
            if removed_list_token.leading_spaces is not None:
                split_spaces = removed_list_token.leading_spaces.split("\n")
                split_spaces.append("")
            else:
                split_spaces = [""]
            self.__fix_requests.append(
                Fixer(
                    self.__removed_container_stack_token,
                    "next_token",
                    "leading_spaces",
                    "\n".join(split_spaces),
                )
            )

    def __fix_spacing_with_fenced_and_list_end(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        new_token: MarkdownToken,
        kludge_alpha: bool,
    ) -> None:
        end_container_index = len(self.__last_end_container_tokens) - 1
        while (
            end_container_index >= 0
            and self.__last_end_container_tokens[end_container_index].is_list_end
        ):
            end_container_index -= 1
        first_token = self.__last_end_container_tokens[end_container_index + 1]
        replacement_tokens: List[MarkdownToken] = []
        if end_container_index >= 0:
            if not kludge_alpha:
                replacement_tokens.extend(
                    self.__last_end_container_tokens[end_container_index + 1 :]
                )
            replacement_tokens.append(
                BlankLineMarkdownToken(
                    extracted_whitespace="",
                    position_marker=PositionMarker(new_token.line_number - 1, 0, ""),
                    column_delta=1,
                )
            )
            if kludge_alpha:
                replacement_tokens.extend(
                    self.__last_end_container_tokens[end_container_index + 1 :]
                )
        else:
            replacement_tokens.append(
                BlankLineMarkdownToken(
                    extracted_whitespace="",
                    position_marker=PositionMarker(new_token.line_number - 1, 0, ""),
                    column_delta=1,
                )
            )
            replacement_tokens.extend(
                self.__last_end_container_tokens[end_container_index + 1 :]
            )
        replacement_tokens.append(new_token)
        self.register_replace_tokens_request(
            context, first_token, token, replacement_tokens
        )

    def __fix_spacing_with_special_list_fix(
        self, context: PluginScanContext, token: MarkdownToken, new_token: MarkdownToken
    ) -> None:
        assert self.__last_token and self.__last_token.is_block_quote_end
        new_end_token = cast(EndMarkdownToken, copy.copy(self.__last_token))
        new_end_token.set_extra_end_data(None)
        replacement_tokens = [
            BlankLineMarkdownToken(
                extracted_whitespace="",
                position_marker=PositionMarker(new_token.line_number - 1, 0, ""),
                column_delta=1,
            ),
            new_end_token,
            new_token,
        ]
        self.register_replace_tokens_request(
            context, self.__last_token, token, replacement_tokens
        )

    def __fix_spacing_with_else(
        self, context: PluginScanContext, token: MarkdownToken, new_token: MarkdownToken
    ) -> None:
        replacement_tokens = [
            BlankLineMarkdownToken(
                extracted_whitespace="",
                position_marker=PositionMarker(new_token.line_number - 1, 0, ""),
                column_delta=1,
            ),
            new_token,
        ]
        self.register_replace_tokens_request(context, token, token, replacement_tokens)

    def __calc_kludge_one(self, at_least_one_container: bool) -> bool:
        if not at_least_one_container:
            return False
        last_stack_token = self.__leading_space_index_tracker.get_container_stack_item(
            -1
        )
        return (
            not any(i.is_block_quote_start for i in self.__x1[:-1])
            if last_stack_token.is_list_start and self.__x1[-1].is_block_quote_start
            else False
        )

    def __calc_3(
        self,
        context: PluginScanContext,
        did_process_removals: bool,
        at_least_one_container: bool,
        upgrade_kludge: bool,
    ) -> Tuple[bool, bool]:
        # This will most likely need rewriting for deeper nestings.
        if not did_process_removals and at_least_one_container:
            last_stack_token_index = (
                self.__leading_space_index_tracker.get_container_stack_size() - 1
            )
            found_block_quote_token = None
            assert last_stack_token_index >= 0
            token_at_index = (
                self.__leading_space_index_tracker.get_container_stack_item(
                    last_stack_token_index
                )
            )
            if token_at_index.is_block_quote_start:  # pragma: no cover
                found_block_quote_token = token_at_index
                while last_stack_token_index >= 0:
                    if (
                        token_at_index := self.__leading_space_index_tracker.get_container_stack_item(
                            last_stack_token_index
                        )
                    ).is_block_quote_start:
                        found_block_quote_token = token_at_index
                        break
                    last_stack_token_index -= 1

                if (
                    found_block_quote_token
                    and len(self.__x1) == 2
                    and self.__x1[0].is_list_start
                    and self.__x1[1].is_block_quote_start
                ):
                    # dd = 0
                    # while dd < len(self.__x1) and not self.__x1[dd].is_block_quote_start:
                    #     dd += 1
                    # assert dd < len(self.__x1)
                    dd = 1
                    did_process_removals = upgrade_kludge = True
                    self.__apply_tailing_block_quote_fix(dd, context)
        return did_process_removals, upgrade_kludge

    def __apply_tailing_block_quote_fix(
        self, modify_index: int, context: PluginScanContext
    ) -> None:
        _ = context

        assert self.__x1[modify_index].is_block_quote_start
        block_quote_token = cast(BlockQuoteMarkdownToken, self.__x1[modify_index])
        assert block_quote_token.bleading_spaces is not None
        split_spaces = block_quote_token.bleading_spaces.split("\n")
        assert self.__x3[modify_index] == len(split_spaces) - 1
        split_spaces[-1] = split_spaces[-1].rstrip()
        self.__fix_requests.append(
            Fixer(
                self.__x1[modify_index],
                "next_token",
                "bleading_spaces",
                "\n".join(split_spaces),
            )
        )

    def __fix_spacing(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        special_case: bool,
        special_case_2: bool,
    ) -> None:
        if special_case:
            self.__fix_spacing_special_case(context, token)
            return
        if special_case_2:
            self.__fix_spacing_special_case2(context, token)
            return
        at_least_one_container = (
            self.__leading_space_index_tracker.in_at_least_one_container()
        )
        upgrade_kludge = False
        if len(self.__x1) > 1:
            # These circumstances are already handled by the zero and single level removals.
            # all_removals_are_block_quotes = all(
            #     f.is_block_quote_start for f in self.__x1
            # )
            all_removals_are_lists = all(f.is_list_start for f in self.__x1)
            was_kludge_one = self.__calc_kludge_one(at_least_one_container)
            did_process_removals = (
                # all_removals_are_block_quotes or
                all_removals_are_lists
                or was_kludge_one
                or not at_least_one_container
            )

            # did_process_removals = self.__calc_2(context, did_process_removals)
            did_process_removals, upgrade_kludge = self.__calc_3(
                context, did_process_removals, at_least_one_container, upgrade_kludge
            )
            # assert did_process_removals

        did_special_list_fix = False
        kludge_alpha = False
        if at_least_one_container:
            did_special_list_fix, kludge_alpha = self.__fix_spacing_one_container(
                context, token, upgrade_kludge
            )
        elif self.__removed_container_stack_token:
            self.__fix_spacing_removed_container(context, token)

        new_token = copy.deepcopy(token)
        self.__fix_count += 1
        new_token.adjust_line_number(context, self.__fix_count)
        assert self.__last_token is not None
        if token.is_fenced_code_block and self.__last_token.is_list_end:
            self.__fix_spacing_with_fenced_and_list_end(
                context, token, new_token, kludge_alpha
            )
        elif did_special_list_fix:
            self.__fix_spacing_with_special_list_fix(context, token, new_token)
        else:
            self.__fix_spacing_with_else(context, token, new_token)

    def __handle_fenced_code_block(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        special_case: bool,
        special_case_2: bool,
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
            if context.in_fix_mode and not context.is_during_line_pass:
                self.__fix_spacing(context, token, special_case, special_case_2)
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
                self.__fix_spacing(context, token, False, False)
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
        _ = context
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

        for i, next_container_adjustment in enumerate(next_container_adjustment_list):
            if next_container_adjustment.do_special:
                split_spaces.insert(
                    0, next_container_adjustment.leading_space_to_insert
                )
                del next_container_adjustment_list[i]
                break

        for next_container_adjustment in next_container_adjustment_list[::-1]:
            assert not next_container_adjustment.do_special
            if next_container_adjustment.do_insert:
                split_spaces.insert(
                    next_container_adjustment.insert_index,
                    next_container_adjustment.leading_space_to_insert,
                )
            else:
                split_spaces[next_container_adjustment.insert_index] = (
                    next_container_adjustment.leading_space_to_insert
                )

        self.__fix_requests.append(
            Fixer(
                self.__leading_space_index_tracker.get_container_stack_item(-1),
                "next_token",
                token_part_name,
                "\n".join(split_spaces),
            )
        )

    def __process_pending_container_end_tokens(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        # is_first = True
        while self.__leading_space_index_tracker.have_any_registered_container_ends():
            if context.in_fix_mode:
                if next_container_adjustment_list := self.__container_adjustments[-1]:
                    self.__process_pending_container_end_adjustment(
                        context, next_container_adjustment_list
                    )

            if self.__leading_space_index_tracker.get_container_stack_item(
                -1
            ).is_block_quote_start:
                leading_space_insert_index = self.__leading_space_index_tracker.get_tokens_block_quote_bleading_space_index(
                    token
                )
            else:
                leading_space_insert_index = self.__leading_space_index_tracker.get_tokens_list_leading_space_index(
                    token
                )
            self.__x3.append(leading_space_insert_index)

            # xxxxxxx = self.__leading_space_index_tracker.since_last_non_end_token()
            # fgg = (
            #     is_first
            #     and len(xxxxxxx) >= 3
            #     and xxxxxxx[-1].is_list_end
            #     and xxxxxxx[-2].is_block_quote_end
            #     and xxxxxxx[-3].is_list_end
            # )

            self.__removed_container_stack_token, xx = (
                self.__leading_space_index_tracker.process_container_end(token)
            )
            assert xx.start_markdown_token == self.__removed_container_stack_token
            self.__x1.append(self.__removed_container_stack_token)
            self.__x4.append(xx)

            self.__removed_container_adjustments = self.__container_adjustments[-1]
            self.__x2.append(self.__removed_container_adjustments)
            del self.__container_adjustments[-1]
            del self.__container_x[-1]
            # is_first = False

    def __calculate_special_case(self) -> bool:
        return bool(
            self.__leading_space_index_tracker.get_container_stack_size() >= 2
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

    def __calculate_specials(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> Tuple[bool, bool]:

        special_case = False
        special_case_2 = False
        if context.in_fix_mode and token.is_fenced_code_block:
            special_case = self.__calculate_special_case()
            if not special_case:
                special_case_2 = (
                    len(self.__x5) >= 3
                    and self.__x5[-1].is_block_quote_end
                    and self.__x5[-2].is_list_end
                    and self.__x5[-3].is_paragraph_end
                )
                if special_case_2:
                    special_case_2 = (
                        self.__leading_space_index_tracker.get_container_stack_size()
                        >= 4
                        and self.__leading_space_index_tracker.get_container_stack_item(
                            -3
                        ).is_list_start
                        and self.__leading_space_index_tracker.get_container_stack_item(
                            -4
                        ).is_block_quote_start
                    )

        return special_case, special_case_2

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """

        special_case, special_case_2 = self.__calculate_specials(context, token)
        if not token.is_end_token or token.is_end_of_stream:
            if not (special_case or special_case_2):
                self.__process_pending_container_end_tokens(context, token)
            if self.__end_fenced_code_block_token:
                self.__handle_end_fenced_code_block(context, token)

        if token.is_block_quote_start or token.is_list_start:
            self.__container_adjustments.append([])
            self.__container_x.append(0)
            self.__leading_space_index_tracker.open_container(token)
        elif token.is_block_quote_end or token.is_list_end:
            self.__leading_space_index_tracker.register_container_end(token)
        elif token.is_fenced_code_block:
            self.__handle_fenced_code_block(
                context, token, special_case, special_case_2
            )
            if special_case or special_case_2:
                self.__process_pending_container_end_tokens(context, token)
        elif token.is_fenced_code_block_end:
            self.__end_fenced_code_block_token = cast(EndMarkdownToken, token)

        if token.is_end_token:
            self.__x5.append(cast(EndMarkdownToken, token))
        else:
            self.__x5.clear()
        self.__leading_space_index_tracker.track_since_last_non_end_token(token)

        self.__next_token_after(context, token)

    def __next_token_after(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:

        if (
            not token.is_end_token
            and not token.is_block_quote_start
            and not token.is_list_start
        ):
            self.__last_non_end_token = token

        if token.is_block_quote_end or token.is_list_end:
            self.__last_end_container_tokens.append(token)
        else:
            self.__last_end_container_tokens.clear()

        self.__second_last_token = self.__last_token
        self.__last_token = token
        self.__removed_container_stack_token = None
        self.__x1.clear()
        self.__x4.clear()
        self.__removed_container_adjustments = None
        self.__x2.clear()
        self.__x3.clear()

        while self.__fix_requests:
            ff = self.__fix_requests[0]
            del self.__fix_requests[0]
            self.register_fix_token_request(
                context, ff.token, ff.plugin_action, ff.field_name, ff.field_value
            )


# pylint: enable=too-many-instance-attributes
