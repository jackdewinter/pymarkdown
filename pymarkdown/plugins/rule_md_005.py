"""
Module to implement a plugin that ensures that the indentation for List Items
are equivalent with each other.
"""

import copy
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.inline_code_span_markdown_token import (
    InlineCodeSpanMarkdownToken,
)
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.new_list_item_markdown_token import NewListItemMarkdownToken
from pymarkdown.tokens.ordered_list_start_markdown_token import (
    OrderedListStartMarkdownToken,
)
from pymarkdown.tokens.raw_html_markdown_token import RawHtmlMarkdownToken
from pymarkdown.tokens.reference_markdown_token import ReferenceMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken
from pymarkdown.tokens.unordered_list_start_markdown_token import (
    UnorderedListStartMarkdownToken,
)


class OrderedListAlignment(Enum):
    """
    Enumeration to provide guidance on what alignment was used for ordered lists.
    """

    UNKNOWN = 0
    LEFT = 1
    RIGHT = 2


@dataclass
class LeadingSpaceAdjustment:
    """
    Internal class to represent an adjustment to be made.
    """

    token: Any
    start_index: int
    end_index: int
    delta_indent: int


@dataclass
class DeferredAdjustmant:
    """
    Internal class to hold any deferred adjustments to the leading spaces.
    """

    token: MarkdownToken
    line_count: int
    delta_indent: int


# pylint: disable=too-many-instance-attributes,protected-access
class RuleMd005(RulePlugin):
    """
    Class to implement a plugin that ensures that the indentation for List Items
    are equivalent with each other.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__list_stack: List[ListStartMarkdownToken] = []
        self.__read_only_list_stack: List[ListStartMarkdownToken] = []

        self.__leading_space_adjustments: Dict[
            MarkdownToken, List[LeadingSpaceAdjustment]
        ] = {}
        self.__unordered_list_indents: Dict[int, int] = {}
        self.__unordered_current_indents: Dict[int, int] = {}
        self.__ordered_list_starts: Dict[int, OrderedListStartMarkdownToken] = {}
        self.__ordered_tokens: Dict[int, List[MarkdownToken]] = {}
        self.__ordered_list_alignment: Dict[int, OrderedListAlignment] = {}
        self.__line_count: Dict[int, int] = {}
        self.__deferred_adjustment: Dict[int, DeferredAdjustmant] = {}
        self.__list_start_indices: Dict[int, Dict[MarkdownToken, int]] = {}
        self.__list_end_indices: Dict[int, Dict[MarkdownToken, int]] = {}
        self.__current_list_tokens: Dict[int, MarkdownToken] = {}
        # self.__debug = False

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="list-indent",
            plugin_id="MD005",
            plugin_enabled_by_default=True,
            plugin_description="Inconsistent indentation for list items at the same level",
            plugin_version="0.5.1",
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md005.md",
            plugin_supports_fix=True,
            plugin_fix_level=2,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__list_stack = []
        self.__read_only_list_stack = []
        self.__leading_space_adjustments = {}
        self.__unordered_list_indents = {}
        self.__unordered_current_indents = {}
        self.__ordered_list_starts = {}
        self.__ordered_tokens = {}
        self.__ordered_list_alignment = {}
        self.__line_count = {}
        self.__deferred_adjustment = {}
        self.__list_start_indices = {}
        self.__list_end_indices = {}
        self.__current_list_tokens = {}

    def __report_issue_new_list_item(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        list_level: int,
        delta: Optional[int],
    ) -> None:
        list_token = cast(NewListItemMarkdownToken, token)
        base_token = self.__list_stack[-1]
        if base_token.is_unordered_list_start:
            expected_indent = self.__unordered_list_indents[list_level]
            expected_indent = self.__unordered_current_indents[list_level]
            delta_indent = list_token.indent_level - expected_indent
        else:
            expected_indent = base_token.indent_level - len(
                base_token.list_start_content
            )
            this_indent = list_token.indent_level - len(list_token.list_start_content)
            delta_indent = this_indent - expected_indent
            if delta and delta < 0:
                delta_indent -= delta

            expected_indent = list_token.indent_level - delta_indent

        adjusted_whitespace = (
            list_token.extracted_whitespace[:-delta_indent]
            if delta_indent > 0
            else list_token.extracted_whitespace + " " * (-delta_indent)
        )
        self.register_fix_token_request(
            context, token, "next_token", "indent_level", expected_indent
        )
        self.register_fix_token_request(
            context,
            token,
            "next_token",
            "extracted_whitespace",
            adjusted_whitespace,
        )
        if base_token.leading_spaces:
            self.__deferred_adjustment[list_level] = DeferredAdjustmant(
                token,
                self.__line_count[list_level],
                delta_indent,
            )

    def __report_issue_ordered_list(
        self, context: PluginScanContext, token: MarkdownToken, list_level: int
    ) -> None:
        list_copy_token = cast(OrderedListStartMarkdownToken, self.__list_stack[-1])
        list_token = cast(OrderedListStartMarkdownToken, token)
        base_token = self.__ordered_list_starts[list_level]
        expected_indent = base_token.column_number
        delta_indent = list_token.column_number - expected_indent
        adjusted_whitespace = (
            list_token.extracted_whitespace[:-delta_indent]
            if delta_indent > 0
            else list_token.extracted_whitespace + (" " * (-delta_indent))
        )
        self.register_fix_token_request(
            context,
            token,
            "next_token",
            "indent_level",
            list_token.indent_level - delta_indent,
        )
        list_copy_token._modify_token(
            "indent_level", list_token.indent_level - delta_indent
        )
        self.register_fix_token_request(
            context,
            token,
            "next_token",
            "extracted_whitespace",
            adjusted_whitespace,
        )
        list_copy_token._modify_token("extracted_whitespace", adjusted_whitespace)
        self.register_fix_token_request(
            context, token, "next_token", "column_number", expected_indent
        )
        list_copy_token._modify_token("column_number", expected_indent)
        if list_token.leading_spaces:
            self.__deferred_adjustment[list_level] = DeferredAdjustmant(
                token, self.__line_count[list_level], delta_indent
            )

    def __report_issue_unordered_list(
        self, context: PluginScanContext, token: MarkdownToken, list_level: int
    ) -> None:
        list_token = cast(UnorderedListStartMarkdownToken, token)
        expected_indent = self.__unordered_list_indents[list_level]
        delta_indent = list_token.indent_level - expected_indent

        previous_list_level = list_level - 1
        if previous_list_level in self.__ordered_tokens:
            previous_ordered_token = cast(
                OrderedListStartMarkdownToken,
                self.__ordered_tokens[previous_list_level][-1],
            )
            start_content_length = len(previous_ordered_token.list_start_content)
            previous_token = self.__ordered_list_starts[previous_list_level]
            indent_adjust = start_content_length - len(
                previous_token.list_start_content
            )
            delta_indent += indent_adjust
            expected_indent -= indent_adjust

            self.__unordered_current_indents[list_level] = (
                self.__unordered_current_indents[list_level] - indent_adjust
            )
        else:
            self.__unordered_current_indents[list_level] = expected_indent

        adjusted_whitespace = (
            list_token.extracted_whitespace[:-delta_indent]
            if delta_indent > 0
            else list_token.extracted_whitespace + (" " * (-delta_indent))
        )
        self.register_fix_token_request(
            context, token, "next_token", "indent_level", expected_indent
        )
        self.register_fix_token_request(
            context,
            token,
            "next_token",
            "extracted_whitespace",
            adjusted_whitespace,
        )
        self.register_fix_token_request(
            context,
            token,
            "next_token",
            "column_number",
            list_token.column_number - delta_indent,
        )
        if list_token.leading_spaces:
            self.__deferred_adjustment[list_level] = DeferredAdjustmant(
                token,
                self.__line_count[list_level],
                delta_indent,
            )

    def __report_issue(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        expected_indent: int,
        delta: Optional[int] = None,
    ) -> None:
        if context.in_fix_mode:
            list_level = len(self.__list_stack)
            if token.is_new_list_item:
                self.__report_issue_new_list_item(context, token, list_level, delta)
            elif token.is_unordered_list_start:
                self.__report_issue_unordered_list(context, token, list_level)
            else:
                self.__report_issue_ordered_list(context, token, list_level)
        else:
            if expected_indent < 0:
                list_token = cast(NewListItemMarkdownToken, token)
                list_level = len(self.__list_stack)
                expected_indent = (
                    self.__ordered_list_starts[list_level].indent_level
                    - 2
                    - len(list_token.list_start_content)
                )

            extra_data = (
                f"Expected: {expected_indent}; Actual: {token.column_number - 1}"
            )
            # if self.__debug:
            #     print(f"ERROR>>{extra_data}")
            self.report_next_token_error(context, token, extra_data)

    def __handle_ordered_list_item_right(
        self,
        list_level: int,
        context: PluginScanContext,
        token: OrderedListStartMarkdownToken,
    ) -> None:
        assert self.__ordered_list_starts[list_level].extracted_whitespace
        original_text = (
            self.__ordered_list_starts[list_level].list_start_content
            + self.__ordered_list_starts[list_level].extracted_whitespace
        )
        prefix_text = f"{token.list_start_content}{token.extracted_whitespace}"
        original_text_length = len(original_text)
        current_prefix_length = len(prefix_text)
        if delta := original_text_length - current_prefix_length:
            # if self.__debug:
            #     print("ri1")
            self.__report_issue(context, token, -1, delta)
        else:
            assert (
                token.indent_level
                == self.__ordered_list_starts[list_level].indent_level
            )

    def __handle_ordered_list_item(
        self, context: PluginScanContext, token: OrderedListStartMarkdownToken
    ) -> None:
        list_level = len(self.__list_stack)
        list_alignment = self.__ordered_list_alignment[list_level]

        self.__handle_leading_space_adjustments(context, token, False)

        if list_alignment == OrderedListAlignment.RIGHT:
            self.__handle_ordered_list_item_right(list_level, context, token)
        elif (
            self.__ordered_list_starts[list_level].column_number != token.column_number
        ):
            # if self.__debug:
            #     print("ri2")
            self.__report_issue(
                context, token, self.__ordered_list_starts[list_level].column_number - 1
            )

    def __compute_ordered_list_alignment(self) -> None:
        list_level = len(self.__list_stack)

        last_length = 0
        last_token: Optional[NewListItemMarkdownToken] = None

        for next_token in self.__ordered_tokens[list_level]:
            list_token = cast(NewListItemMarkdownToken, next_token)
            content_length = len(list_token.list_start_content)
            if not last_length:
                last_length = content_length
                last_token = list_token
            elif content_length != last_length:
                assert last_token is not None
                if last_token.column_number == list_token.column_number:
                    self.__ordered_list_alignment[list_level] = (
                        OrderedListAlignment.LEFT
                    )
                    break
                last_total_length = len(last_token.extracted_whitespace) + len(
                    last_token.list_start_content
                )
                next_total_length = len(list_token.extracted_whitespace) + len(
                    list_token.list_start_content
                )
                if last_total_length == next_total_length:
                    self.__ordered_list_alignment[list_level] = (
                        OrderedListAlignment.RIGHT
                    )
                    break

    def __handle_unordered_list_start(
        self, context: PluginScanContext, token: UnorderedListStartMarkdownToken
    ) -> None:
        self.__list_stack.append(token)
        self.__read_only_list_stack.append(token)
        list_level = len(self.__list_stack)
        self.__line_count[list_level] = 0

        if list_level not in self.__unordered_list_indents:
            self.__unordered_list_indents[list_level] = token.indent_level
        self.__unordered_current_indents[list_level] = token.indent_level
        if self.__unordered_list_indents[list_level] != token.indent_level:
            # if self.__debug:
            #     print("ri3")
            self.__report_issue(
                context, token, self.__unordered_list_indents[list_level] - 2
            )

    def __handle_ordered_list_start(self, token: OrderedListStartMarkdownToken) -> None:
        token_copy = copy.deepcopy(token)
        self.__list_stack.append(token_copy)
        self.__read_only_list_stack.append(token)
        list_level = len(self.__list_stack)
        self.__line_count[list_level] = 0

        new_map: Dict[MarkdownToken, int] = {}
        self.__list_start_indices[list_level] = new_map
        new_map[token] = self.__line_count[list_level]

        new_map = {}
        self.__list_end_indices[list_level] = new_map
        self.__current_list_tokens[list_level] = token

        self.__ordered_tokens[list_level] = [token]
        if list_level not in self.__ordered_list_starts:
            self.__ordered_list_starts[list_level] = token_copy
            self.__ordered_list_alignment[list_level] = OrderedListAlignment.UNKNOWN

    def __handle_deferred_adjustment(self) -> None:
        list_stack_length = len(self.__list_stack)
        current_deferred = self.__deferred_adjustment[list_stack_length]
        token = current_deferred.token
        delta_indent = current_deferred.delta_indent

        if list_stack_length in self.__list_start_indices:
            start_index = self.__list_start_indices[list_stack_length][token]
            end_index = self.__list_end_indices[list_stack_length][token]
        else:
            start_index = current_deferred.line_count
            end_index = self.__line_count[list_stack_length]

        owner = self.__read_only_list_stack[-1]
        owner_list: List[LeadingSpaceAdjustment] = []
        if owner in self.__leading_space_adjustments:
            owner_list = self.__leading_space_adjustments[owner]
        else:
            self.__leading_space_adjustments[owner] = owner_list

        owner_tuple = LeadingSpaceAdjustment(
            token, start_index, end_index, delta_indent
        )
        owner_list.append(owner_tuple)

    def __handle_leading_space_adjustments(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        do_leading_adjustments: bool,
    ) -> None:
        list_stack_length = len(self.__list_stack)
        if list_stack_length in self.__deferred_adjustment:
            self.__handle_deferred_adjustment()
            del self.__deferred_adjustment[list_stack_length]

        owner = self.__read_only_list_stack[-1]
        if do_leading_adjustments and owner in self.__leading_space_adjustments:
            end_token = cast(EndMarkdownToken, token)
            list_start_token = cast(
                ListStartMarkdownToken, end_token.start_markdown_token
            )
            assert list_start_token.leading_spaces is not None
            split_leading_spaces = list_start_token.leading_spaces.split("\n")
            owner_list = self.__leading_space_adjustments[owner]
            for next_adjustment in owner_list:
                for i in range(next_adjustment.start_index, next_adjustment.end_index):
                    split_leading_spaces[i] = (
                        split_leading_spaces[i][: -next_adjustment.delta_indent]
                        if next_adjustment.delta_indent > 0
                        else split_leading_spaces[i]
                        + (" " * -next_adjustment.delta_indent)
                    )
            self.register_fix_token_request(
                context,
                end_token.start_markdown_token,
                "next_token",
                "leading_spaces",
                "\n".join(split_leading_spaces),
            )

    def __handle_list_item(
        self, context: PluginScanContext, token: NewListItemMarkdownToken
    ) -> None:
        list_level = len(self.__list_stack)
        if list_level in self.__list_start_indices:
            current_list_token = self.__current_list_tokens[list_level]
            self.__current_list_tokens[list_level] = token

            self.__list_end_indices[list_level][current_list_token] = self.__line_count[
                list_level
            ]
            self.__list_start_indices[list_level][token] = self.__line_count[list_level]

        self.__handle_leading_space_adjustments(context, token, False)

        if self.__list_stack[-1].is_unordered_list_start:
            if (
                self.__unordered_list_indents[len(self.__list_stack)]
                != token.indent_level
            ):
                # if self.__debug:
                #     print("ri4")
                #     print("token.indent_level=" + str(token.indent_level))
                #     print("un_li=" + ParserHelper.make_value_visible(self.__unordered_list_indents))
                self.__report_issue(
                    context,
                    token,
                    self.__unordered_list_indents[len(self.__list_stack)] - 2,
                )
        else:
            self.__ordered_tokens[len(self.__list_stack)].append(token)

    def __handle_list_end(
        self, context: PluginScanContext, token: EndMarkdownToken
    ) -> None:
        list_level = len(self.__list_stack)
        if list_level in self.__list_start_indices:
            current_list_token = self.__current_list_tokens[list_level]
            self.__list_end_indices[list_level][current_list_token] = self.__line_count[
                list_level
            ]

        self.__handle_leading_space_adjustments(context, token, False)

        if token.is_ordered_list_end:
            list_level = len(self.__list_stack)
            if (
                self.__ordered_list_alignment[list_level]
                == OrderedListAlignment.UNKNOWN
            ):
                self.__compute_ordered_list_alignment()
            for next_token in self.__ordered_tokens[list_level]:
                next_list_token = cast(OrderedListStartMarkdownToken, next_token)
                self.__handle_ordered_list_item(context, next_list_token)
        self.__handle_leading_space_adjustments(context, token, True)
        del self.__line_count[len(self.__list_stack)]
        del self.__read_only_list_stack[-1]
        del self.__list_stack[-1]
        if list_level in self.__list_start_indices:
            del self.__list_start_indices[list_level]
            del self.__list_end_indices[list_level]
            del self.__current_list_tokens[list_level]
        if not self.__list_stack:
            self.__unordered_list_indents = {}
            self.__unordered_current_indents = {}
            self.__ordered_list_starts = {}

    def __count_newlines_in_token(self, current_token: MarkdownToken) -> int:
        newlines_in_text_token = 0
        if current_token.is_text:
            text_token = cast(TextMarkdownToken, current_token)
            newlines_in_text_token = ParserHelper.count_newlines_in_text(
                text_token.token_text
            )
        elif current_token.is_inline_image or current_token.is_inline_link:
            reference_token = cast(ReferenceMarkdownToken, current_token)
            newlines_in_text_token += ParserHelper.count_newlines_in_text(
                reference_token.text_from_blocks
            )
        elif current_token.is_inline_raw_html:
            raw_html_token = cast(RawHtmlMarkdownToken, current_token)
            newlines_in_text_token += ParserHelper.count_newlines_in_text(
                raw_html_token.raw_tag
            )
        elif current_token.is_inline_code_span:
            code_span_token = cast(InlineCodeSpanMarkdownToken, current_token)
            newlines_in_text_token += ParserHelper.count_newlines_in_texts(
                code_span_token.leading_whitespace,
                code_span_token.span_text,
                code_span_token.trailing_whitespace,
            )
        return newlines_in_text_token

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        # print(f"token>>{ParserHelper.make_value_visible(token)}")
        if token.is_unordered_list_start:
            unordered_list_start_token = cast(UnorderedListStartMarkdownToken, token)
            self.__handle_unordered_list_start(context, unordered_list_start_token)
        elif token.is_ordered_list_start:
            ordered_list_start_token = cast(OrderedListStartMarkdownToken, token)
            self.__handle_ordered_list_start(ordered_list_start_token)
        elif token.is_unordered_list_end or token.is_ordered_list_end:
            end_token = cast(EndMarkdownToken, token)
            self.__handle_list_end(context, end_token)
        elif token.is_new_list_item:
            new_list_item_token = cast(NewListItemMarkdownToken, token)
            self.__handle_list_item(context, new_list_item_token)
        elif list_stack_length := len(self.__list_stack):
            self.__line_count[list_stack_length] += self.__count_newlines_in_token(
                token
            )


# pylint: enable=too-many-instance-attributes,protected-access
