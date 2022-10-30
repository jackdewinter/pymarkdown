"""
Module to implement a plugin that ensures that the indentation for List Items
are equivalent with each other.
"""
from enum import Enum
from typing import Dict, List, Optional, cast

from pymarkdown.container_markdown_token import (
    ListStartMarkdownToken,
    NewListItemMarkdownToken,
    OrderedListStartMarkdownToken,
    UnorderedListStartMarkdownToken,
)
from pymarkdown.markdown_token import EndMarkdownToken, MarkdownToken
# from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class OrderedListAlignment(Enum):
    """
    Enumeration to provide guidance on what alignment was used for ordered lists.
    """

    UNKNOWN = 0
    LEFT = 1
    RIGHT = 2


class RuleMd005(RulePlugin):
    """
    Class to implement a plugin that ensures that the indentation for List Items
    are equivalent with each other.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__list_stack: List[ListStartMarkdownToken] = []
        self.__unordered_list_indents: Dict[int, int] = {}
        self.__ordered_list_starts: Dict[int, OrderedListStartMarkdownToken] = {}
        self.__ordered_tokens: Dict[int, List[MarkdownToken]] = {}
        self.__ordered_list_alignment: Dict[int, OrderedListAlignment] = {}
        # self.__debug = False

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="list-indent",
            plugin_id="MD005",
            plugin_enabled_by_default=True,
            plugin_description="Inconsistent indentation for list items at the same level",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md005.md",
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__list_stack = []
        self.__unordered_list_indents = {}
        self.__ordered_list_starts = {}
        self.__ordered_tokens = {}
        self.__ordered_list_alignment = {}

    def __report_issue(
        self, context: PluginScanContext, token: MarkdownToken, expected_indent: int
    ) -> None:
        if expected_indent < 0:
            list_token = cast(NewListItemMarkdownToken, token)
            list_level = len(self.__list_stack)
            expected_indent = (
                self.__ordered_list_starts[list_level].indent_level
                - 2
                - len(list_token.list_start_content)
            )

        extra_data = f"Expected: {expected_indent}; Actual: {token.column_number - 1}"
        # if self.__debug:
        #     print(f"ERROR>>{extra_data}")
        self.report_next_token_error(context, token, extra_data)

    def __handle_ordered_list_item(
        self, context: PluginScanContext, token: OrderedListStartMarkdownToken
    ) -> None:
        list_level = len(self.__list_stack)
        list_alignment = self.__ordered_list_alignment[list_level]

        if list_alignment == OrderedListAlignment.RIGHT:
            assert self.__ordered_list_starts[list_level].extracted_whitespace
            original_text = (
                self.__ordered_list_starts[list_level].list_start_content
                + self.__ordered_list_starts[list_level].extracted_whitespace
            )
            original_text_length = len(original_text)
            current_prefix_length = len(
                f"{token.list_start_content}{token.extracted_whitespace}"
            )
            if original_text_length == current_prefix_length:
                assert (
                    token.indent_level
                    == self.__ordered_list_starts[list_level].indent_level
                )
            else:
                # if self.__debug:
                #     print("ri1")
                self.__report_issue(context, token, -1)
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
                    self.__ordered_list_alignment[
                        list_level
                    ] = OrderedListAlignment.LEFT
                    break
                last_total_length = len(last_token.extracted_whitespace) + len(
                    last_token.list_start_content
                )
                next_total_length = len(list_token.extracted_whitespace) + len(
                    list_token.list_start_content
                )
                if last_total_length == next_total_length:
                    self.__ordered_list_alignment[
                        list_level
                    ] = OrderedListAlignment.RIGHT
                    break

    def __handle_unordered_list_start(
        self, context: PluginScanContext, token: UnorderedListStartMarkdownToken
    ) -> None:
        self.__list_stack.append(token)
        list_level = len(self.__list_stack)
        if list_level not in self.__unordered_list_indents:
            self.__unordered_list_indents[list_level] = token.indent_level
        if self.__unordered_list_indents[list_level] != token.indent_level:
            # if self.__debug:
            #     print("ri3")
            self.__report_issue(
                context, token, self.__unordered_list_indents[list_level] - 2
            )

    def __handle_ordered_list_start(self, token: OrderedListStartMarkdownToken) -> None:
        self.__list_stack.append(token)
        list_level = len(self.__list_stack)
        self.__ordered_tokens[list_level] = [token]
        if list_level not in self.__ordered_list_starts:
            self.__ordered_list_starts[list_level] = token
            self.__ordered_list_alignment[list_level] = OrderedListAlignment.UNKNOWN

    def __handle_list_item(
        self, context: PluginScanContext, token: NewListItemMarkdownToken
    ) -> None:
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
        del self.__list_stack[-1]
        if not self.__list_stack:
            self.__unordered_list_indents = {}
            self.__ordered_list_starts = {}

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
