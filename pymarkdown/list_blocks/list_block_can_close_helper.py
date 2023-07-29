"""
Module to calculate whether to close a list when starting a new list.
"""

import logging
from typing import List, Tuple, cast

from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import ListStackToken, StackToken

POGGER = ParserLogger(logging.getLogger(__name__))


class ListBlockCanCloseHelper:
    """
    Class to calculate whether to close a list when starting a new list.
    """

    @staticmethod
    def calculate_can_remove_list(
        parser_state: ParserState, current_start_index: int
    ) -> bool:
        POGGER.debug_with_visible_whitespace(
            "parser_state.token_stack>$", parser_state.token_stack
        )
        POGGER.debug_with_visible_whitespace(
            "current_start_index>$", current_start_index
        )
        if len(parser_state.token_stack) <= 2:
            return False

        stack_index = len(parser_state.token_stack) - 1
        while stack_index and not parser_state.token_stack[stack_index].is_list:
            stack_index -= 1
        assert stack_index
        last_stack_index = stack_index
        assert parser_state.token_stack[stack_index].is_list
        stack_index -= 1
        while stack_index and not parser_state.token_stack[stack_index].is_list:
            stack_index -= 1
        if not stack_index:
            return False

        stack_index_token = cast(ListStackToken, parser_state.token_stack[stack_index])
        last_stack_index_token = cast(
            ListStackToken, parser_state.token_stack[last_stack_index]
        )
        POGGER.debug("parser_state.token_stack[i]>$", stack_index_token)
        previous_list_start_index = stack_index_token.indent_level
        previous_list_end_index = (
            previous_list_start_index
            + len(stack_index_token.list_character)
            + stack_index_token.ws_after_marker
        )
        POGGER.debug(
            "token_stack[i]:  previous_list_start_index=$,previous_list_end_index=$",
            previous_list_start_index,
            previous_list_end_index,
        )
        with_previous_list_bounds = (
            previous_list_start_index <= current_start_index < previous_list_end_index
        )

        adjusted_index = (
            last_stack_index_token.indent_level
            - last_stack_index_token.ws_before_marker
            if last_stack_index_token.is_ordered_list
            else last_stack_index_token.indent_level - 2
        )

        POGGER.debug(
            "adjusted_index>$ > parser_state.token_stack[stack_index].indent_level>$ ) "
            + "or not with_previous_list_bounds=$",
            adjusted_index,
            stack_index_token.indent_level,
            with_previous_list_bounds,
        )
        return (
            adjusted_index > stack_index_token.indent_level
            or not with_previous_list_bounds
        )

    @staticmethod
    def close_required_lists(
        parser_state: ParserState,
        allow_list_removal: bool,
        balancing_tokens: List[MarkdownToken],
        new_stack: StackToken,
    ) -> None:
        assert new_stack.matching_markdown_token is not None
        matching_column_number = new_stack.matching_markdown_token.column_number

        (
            list_count,
            parent_indent_level,
        ) = ListBlockCanCloseHelper.__close_required_lists_calc(parser_state)

        POGGER.debug(
            "matching_column_number=$ <= parent_indent_level=$ and allow_list_removal=$ and list_count=$ > 1",
            matching_column_number,
            parent_indent_level,
            allow_list_removal,
            list_count,
        )
        while (
            matching_column_number <= parent_indent_level
            and allow_list_removal
            and list_count > 1
        ):
            stack_index = len(parser_state.token_stack) - 2
            while stack_index and not parser_state.token_stack[stack_index].is_list:
                stack_index -= 1
            last_stack_index = parser_state.token_stack.index(
                parser_state.token_stack[-1]
            )
            POGGER.debug("parser_state.token_stack>>$", parser_state.token_stack)
            POGGER.debug("last_stack_index>>$", last_stack_index)
            POGGER.debug("stack_index>>$", stack_index)
            last_stack_index = stack_index + 1

            close_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=last_stack_index,
                include_lists=True,
                include_block_quotes=True,
            )
            assert close_tokens
            balancing_tokens.extend(close_tokens)
            POGGER.debug("close_tokens>>$", close_tokens)
            POGGER.debug("parser_state.token_stack>>$", parser_state.token_stack)
            assert parser_state.token_stack[-1].is_list

            (
                list_count,
                parent_indent_level,
            ) = ListBlockCanCloseHelper.__close_required_lists_calc(parser_state)
            POGGER.debug(
                "matching_column_number=$ < parent_indent_level=$ and "
                + "allow_list_removal=$ and list_count=$ > 1",
                matching_column_number,
                parent_indent_level,
                allow_list_removal,
                list_count,
            )

    @staticmethod
    def __close_required_lists_calc(parser_state: ParserState) -> Tuple[int, int]:
        token_stack_index = len(parser_state.token_stack) - 1
        found_list_tokens = []
        while token_stack_index:
            if parser_state.token_stack[token_stack_index].is_list:
                found_list_tokens.append(parser_state.token_stack[token_stack_index])
            token_stack_index -= 1

        parent_indent_level = -1
        if len(found_list_tokens) > 1:
            list_token = cast(
                ListStartMarkdownToken, found_list_tokens[1].matching_markdown_token
            )
            parent_indent_level = list_token.indent_level
        return len(found_list_tokens), parent_indent_level
