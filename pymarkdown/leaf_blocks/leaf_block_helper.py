"""
Module to provide helpers for the processing of leaf blocks.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import ListStackToken, StackToken

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
        alt_removed_chars_at_start: Optional[int] = None,
        is_html: bool = False,
        original_line: Optional[str] = None,
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
            parser_state,
            removed_chars_at_start,
            html_tokens,
            delay_tab_match,
            alt_removed_chars_at_start,
            is_html,
            original_line,
        )

        if was_token_already_added_to_stack:
            assert (
                top_of_stack is not None
            ), "If token was added, top_of_stack should be defined."
            parser_state.token_stack.append(top_of_stack)
            POGGER.debug(
                ">>correct_for_leaf_block_start_in_list>>stack>>$>>",
                parser_state.token_stack,
            )
        html_tokens.append(end_of_list)
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens_to_add>>$>>", html_tokens
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_leaf_start_adjust_tab(
        parser_state: ParserState,
        original_line: str,
        leading_chars_at_start: str,
        indent_count: int,
        used_indent: str,
    ) -> str:
        after_index_index = len(leading_chars_at_start) + indent_count
        used_indent_text = leading_chars_at_start + used_indent
        assert (
            parser_state.original_line_to_parse is not None
        ), "Original line must be defined by now."
        reconstructed_line = (
            used_indent_text + parser_state.original_line_to_parse[after_index_index:]
        )
        detabified_original_line = TabHelper.detabify_string(original_line)
        assert (
            detabified_original_line == reconstructed_line
        ), "Detabified original must equal reconstructed."
        keep_going = True
        detab_index = 1
        while keep_going:
            orig_prefix = original_line[:detab_index]
            detab_orig_prefix = TabHelper.detabify_string(orig_prefix)
            keep_going = len(detab_orig_prefix) < len(used_indent_text)
            if keep_going:
                detab_index += 1
        assert len(detab_orig_prefix) == len(
            used_indent_text
        ), "Detab prefix must equal used indent."
        return orig_prefix[len(leading_chars_at_start) :]

    @staticmethod
    def __determine_removed_and_leading_characters(
        parser_state: ParserState, removed_chars_at_start: int
    ) -> Tuple[int, str]:
        leading_chars_at_start = ""
        last_bq_index = parser_state.find_last_block_quote_on_stack()
        if last_bq_index > 0:
            last_bq_token = cast(
                BlockQuoteMarkdownToken,
                parser_state.token_stack[last_bq_index].matching_markdown_token,
            )
            assert (
                last_bq_token.bleading_spaces is not None
            ), "Block quote tokens must have bleading spaces defined"
            leading_chars_at_start = last_bq_token.bleading_spaces
            last_newline_index = leading_chars_at_start.rfind("\n")
            assert (
                last_newline_index != -1
            ), "leading_chars_at_start must always have at least one newline character"
            leading_chars_at_start = leading_chars_at_start[last_newline_index + 1 :]
            removed_chars_at_start -= len(leading_chars_at_start)
        return removed_chars_at_start, leading_chars_at_start

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_leaf_start_adjust(
        parser_state: ParserState,
        delay_tab_match: bool,
        alt_removed_chars_at_start: Optional[int],
        is_html: bool,
        original_line: Optional[str],
        list_stack_token: ListStackToken,
        removed_chars_at_start: int,
    ) -> None:
        if LeafBlockHelper.__detect_list_already_added_to(parser_state):
            return

        if delay_tab_match:
            used_indent = ""
        else:
            leading_chars_at_start = ""
            if alt_removed_chars_at_start is not None:
                indent_count = alt_removed_chars_at_start
            else:
                if is_html:
                    removed_chars_at_start, leading_chars_at_start = (
                        LeafBlockHelper.__determine_removed_and_leading_characters(
                            parser_state, removed_chars_at_start
                        )
                    )
                indent_count = removed_chars_at_start
            used_indent = ParserHelper.repeat_string(" ", indent_count)
            if (
                is_html
                and original_line is not None
                and leading_chars_at_start
                and "\t" in original_line
            ):
                used_indent = LeafBlockHelper.__handle_leaf_start_adjust_tab(
                    parser_state,
                    original_line,
                    leading_chars_at_start,
                    indent_count,
                    used_indent,
                )
        assert (
            list_stack_token.matching_markdown_token is not None
        ), "Container stack tokens always have markdown tokens."
        list_markdown_token = cast(
            ListStartMarkdownToken, list_stack_token.matching_markdown_token
        )
        POGGER.debug("__handle_leaf_start_adjust>>list_token>>$", list_markdown_token)
        list_markdown_token.add_leading_spaces(used_indent)
        POGGER.debug("__handle_leaf_start_adjust>>list_token>>$", list_markdown_token)

    # pylint: enable=too-many-arguments

    @staticmethod
    def __detect_list_already_added_to(parser_state) -> bool:

        assert len(parser_state.block_copy) == len(parser_state.copy_of_token_stack) - 1
        copy_stack_index = len(parser_state.copy_of_token_stack) - 1
        while (
            copy_stack_index > 0
            and not parser_state.copy_of_token_stack[copy_stack_index].is_list
            and not parser_state.copy_of_token_stack[copy_stack_index].is_block_quote
        ):
            copy_stack_index -= 1
        stack_index = len(parser_state.token_stack) - 1
        assert parser_state.token_stack[stack_index].is_list or parser_state.token_stack[stack_index].is_block_quote
        # while (
        #     stack_index > 0
        #     and not parser_state.token_stack[stack_index].is_list
        #     and not parser_state.token_stack[stack_index].is_block_quote
        # ):
        #     stack_index -= 1
        bb_line = parser_state.token_stack[stack_index].matching_markdown_token.line_number
        bb_column = parser_state.token_stack[stack_index].matching_markdown_token.column_number
        aa_line = parser_state.copy_of_token_stack[copy_stack_index].matching_markdown_token.line_number
        aa_column = parser_state.copy_of_token_stack[copy_stack_index].matching_markdown_token.column_number
        new_stack_index = copy_stack_index
        while new_stack_index > 0 and bb_line != aa_line and bb_column != aa_column:
            new_stack_index -= 1
            aa_line = parser_state.copy_of_token_stack[new_stack_index].matching_markdown_token.line_number
            aa_column = parser_state.copy_of_token_stack[new_stack_index].matching_markdown_token.column_number

        original_removed_tokens = []
        removed_tokens = []
        add_index = new_stack_index + 1
        while add_index <= copy_stack_index:
            original_removed_tokens.append(parser_state.copy_of_token_stack[add_index].matching_markdown_token)
            removed_tokens.append(parser_state.block_copy[add_index-1])
            add_index+=1

        if original_removed_tokens:
            assert len(original_removed_tokens) == 1
            assert original_removed_tokens[0].is_list_start

            original_leading_spaces = original_removed_tokens[0].leading_spaces
            current_leading_spaces = removed_tokens[0].leading_spaces
            if original_leading_spaces and current_leading_spaces and original_leading_spaces != current_leading_spaces:
                return True
        return False

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_leaf_start(
        parser_state: ParserState,
        removed_chars_at_start: int,
        html_tokens: List[MarkdownToken],
        delay_tab_match: bool,
        alt_removed_chars_at_start: Optional[int],
        is_html: bool,
        original_line: Optional[str] = None,
    ) -> None:
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>stack>>$>>",
            parser_state.token_stack,
        )
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens_to_add>>$>>", html_tokens
        )

        assert parser_state.original_line_to_parse is not None
        ws_count, _ = ParserHelper.collect_while_spaces_verified(
            parser_state.original_line_to_parse[removed_chars_at_start:], 0
        )

        adjust_with_leading_spaces = False
        is_remaining_list_token = True
        while is_remaining_list_token:
            assert parser_state.token_stack[
                -1
            ].is_list, "Token at the end of the stack must be a list token."
            list_stack_token = cast(ListStackToken, parser_state.token_stack[-1])

            POGGER.debug(">>removed_chars_at_start>>$>>", removed_chars_at_start)
            POGGER.debug(">>stack indent>>$>>", list_stack_token.indent_level)
            if (removed_chars_at_start + ws_count) >= list_stack_token.indent_level:
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
            assert parser_state.token_stack[
                -1
            ].is_list, "Token at the end of the stack must be a list token."
            list_stack_token = cast(ListStackToken, parser_state.token_stack[-1])
            # delta_indent = removed_chars_at_start - list_stack_token.indent_level
            # POGGER.debug(
            #     ">>correct_for_leaf_block_start_in_list>>delta_indent>>$>>",
            #     delta_indent,
            # )
            # assert not delta_indent

            POGGER.debug(">>delay_tab_match>>$>>", delay_tab_match)
            if adjust_with_leading_spaces:
                LeafBlockHelper.__handle_leaf_start_adjust(
                    parser_state,
                    delay_tab_match,
                    alt_removed_chars_at_start,
                    is_html,
                    original_line,
                    list_stack_token,
                    removed_chars_at_start,
                )

    # pylint: enable=too-many-arguments

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

    @staticmethod
    def realize_leading_whitespace(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: str,
        original_line: str,
    ) -> str:
        """
        In cases where we "probably" have more than 3 spaces, we need to check to make
        sure that we actually have those once the containers are taken into account.
        """
        new_whitespace = extracted_whitespace
        if (
            extracted_whitespace
            and position_marker.index_indent
            # and len(extracted_whitespace) > 3
        ):
            indexed_original_line = original_line[: position_marker.index_indent]
            if indexed_original_line.endswith(">") or indexed_original_line.endswith(
                "> "
            ):
                bq_present = ParserHelper.count_characters_in_text(
                    indexed_original_line, ">"
                )
                stack_index = LeafBlockHelper.__find_nth_block_quote(
                    parser_state, bq_present
                )
                new_stack_index = stack_index + 1
                best_indent = None
                while (
                    new_stack_index < len(parser_state.token_stack)
                    and parser_state.token_stack[new_stack_index].is_list
                ):
                    inner_list_token = cast(
                        ListStackToken, parser_state.token_stack[new_stack_index]
                    )
                    indent_delta = (
                        inner_list_token.indent_level - position_marker.index_indent
                    )
                    # NOTE: this assert should be triggered by a currently disabled test
                    assert indent_delta > len(extracted_whitespace)
                    new_stack_index += 1
                new_whitespace = (
                    extracted_whitespace[best_indent:]
                    if best_indent is not None
                    else ""
                )
        return new_whitespace

    @staticmethod
    def __find_nth_block_quote(parser_state: ParserState, bq_present: int) -> int:
        bq_encountered = 0
        stack_index = 1
        while True:
            if parser_state.token_stack[stack_index].is_block_quote:
                bq_encountered += 1
                if bq_encountered == bq_present:
                    break
            stack_index += 1
        return stack_index
