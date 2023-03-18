"""
Module to provide helpers for the processing of leaf blocks.
"""
import logging
from typing import List, cast

from pymarkdown.container_markdown_token import ListStartMarkdownToken
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.stack_token import ListStackToken, StackToken

POGGER = ParserLogger(logging.getLogger(__name__))


class LeafBlockHelper:
    """
    Class to provide helpers for the processing of leaf blocks.
    """

    # pylint: disable=too-many-arguments
    @staticmethod
    def correct_for_leaf_block_start_in_list(
        parser_state: ParserState,
        removed_chars_at_start: int,
        old_top_of_stack_token: StackToken,
        html_tokens: List[MarkdownToken],
        was_token_already_added_to_stack: bool = True,
        delay_tab_match: bool = False,
    ) -> None:
        """
        Check to see that if a paragraph has been closed within a list and
        there is a leaf block token immediately following, that the right
        actions are taken.
        """

        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>removed_chars_at_start>$>>",
            removed_chars_at_start,
        )
        if not old_top_of_stack_token.is_paragraph:
            POGGER.debug("1")
            return

        statck_index, top_of_stack, end_of_list = (
            -2 if was_token_already_added_to_stack else -1,
            None,
            html_tokens[-1],
        )
        if not parser_state.token_stack[statck_index].is_list:
            POGGER.debug("2")
            return

        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>stack>>$>>",
            parser_state.token_stack,
        )
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens>>$>>",
            parser_state.token_document,
        )
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens_to_add>>$>>", html_tokens
        )

        if was_token_already_added_to_stack:
            top_of_stack = parser_state.token_stack[-1]
            del parser_state.token_stack[-1]
        del html_tokens[-1]

        LeafBlockHelper.__handle_leaf_start(
            parser_state, removed_chars_at_start, html_tokens, delay_tab_match
        )

        if was_token_already_added_to_stack:
            assert top_of_stack is not None
            parser_state.token_stack.append(top_of_stack)
            POGGER.debug(
                ">>correct_for_leaf_block_start_in_list>>stack>>$>>",
                parser_state.token_stack,
            )
        html_tokens.append(end_of_list)
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens_to_add>>$>>", html_tokens
        )
        # assert False

    # pylint: enable=too-many-arguments
    @staticmethod
    def __handle_leaf_start(
        parser_state: ParserState,
        removed_chars_at_start: int,
        html_tokens: List[MarkdownToken],
        delay_tab_match: bool,
    ) -> None:
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>stack>>$>>",
            parser_state.token_stack,
        )
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens_to_add>>$>>", html_tokens
        )

        adjust_with_leading_spaces = False
        is_remaining_list_token = True
        while is_remaining_list_token:
            assert parser_state.token_stack[-1].is_list
            list_stack_token = cast(ListStackToken, parser_state.token_stack[-1])

            POGGER.debug(">>removed_chars_at_start>>$>>", removed_chars_at_start)
            POGGER.debug(">>stack indent>>$>>", list_stack_token.indent_level)
            if removed_chars_at_start >= list_stack_token.indent_level:
                break  # pragma: no cover

            tokens_from_close, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=(len(parser_state.token_stack) - 1),
                include_lists=True,
            )
            adjust_with_leading_spaces = True
            POGGER.debug(
                ">>correct_for_leaf_block_start_in_list>>tokens_from_close>>$>>",
                tokens_from_close,
            )
            html_tokens.extend(tokens_from_close)

            is_remaining_list_token = parser_state.token_stack[-1].is_list

        if is_remaining_list_token:
            assert parser_state.token_stack[-1].is_list
            list_stack_token = cast(ListStackToken, parser_state.token_stack[-1])
            delta_indent = removed_chars_at_start - list_stack_token.indent_level
            POGGER.debug(
                ">>correct_for_leaf_block_start_in_list>>delta_indent>>$>>",
                delta_indent,
            )
            assert not delta_indent

            POGGER.debug(">>delay_tab_match>>$>>", delay_tab_match)
            # assert not delay_tab_match
            if adjust_with_leading_spaces:
                if delay_tab_match:
                    used_indent = ""
                else:
                    used_indent = ParserHelper.repeat_string(
                        " ", removed_chars_at_start
                    )
                assert list_stack_token.matching_markdown_token is not None
                list_markdown_token = cast(
                    ListStartMarkdownToken, list_stack_token.matching_markdown_token
                )
                list_markdown_token.add_leading_spaces(used_indent)

    @staticmethod
    def extract_markdown_tokens_back_to_blank_line(
        parser_state: ParserState, was_forced: bool
    ) -> List[MarkdownToken]:
        """
        Extract tokens going back to the last blank line token.
        """

        pre_tokens: List[MarkdownToken] = []
        while parser_state.token_document[-1].is_blank_line:
            last_element = parser_state.token_document[-1]
            if was_forced:
                pre_tokens.insert(0, last_element)
            else:
                pre_tokens.append(last_element)
            del parser_state.token_document[-1]
        return pre_tokens
