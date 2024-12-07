"""
Module to provide helper functions for containers.

These functions are typically needed in other modules than the two main
container modules.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.stack_token import ListStackToken

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-few-public-methods


class ContainerHelper:
    """
    Class to provide helper functions for containers.
    """

    @staticmethod
    def __reduce_containers_if_required_bq_list(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: str,
        new_tokens: List[MarkdownToken],
    ) -> Tuple[bool, str, str]:
        did_once = False
        whitespace_prefix = ""
        # list_indent_level = None
        if parser_state.token_stack[-1].is_list:
            # leading_space_length = (
            #     len(extracted_whitespace) + position_marker.index_indent
            # )
            assert parser_state.original_line_to_parse is not None
            leading_space_length = parser_state.original_line_to_parse.index(
                position_marker.text_to_parse
            ) + len(extracted_whitespace)
            search_index = len(parser_state.token_stack)
            while parser_state.token_stack[search_index - 1].is_list:
                list_token = cast(
                    ListStackToken, parser_state.token_stack[search_index - 1]
                )
                if list_token.indent_level <= leading_space_length:
                    break
                search_index -= 1
                did_once = True

            if did_once:
                last_token = cast(EndMarkdownToken, new_tokens[-1])
                last_token.set_extra_end_data(None)

            (
                container_level_tokens,
                _,
            ) = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=search_index,
                include_lists=True,
                caller_can_handle_requeue=False,
                requeue_reset=True,
            )
            new_tokens.extend(container_level_tokens)

            indent_delta = list_token.indent_level - position_marker.index_indent
            whitespace_prefix = extracted_whitespace[:indent_delta]
            extracted_whitespace = extracted_whitespace[indent_delta:]
        return did_once, extracted_whitespace, whitespace_prefix

    @staticmethod
    def __xx(parser_state: ParserState, extra_bqs: int) -> List[MarkdownToken]:
        until_index = len(parser_state.token_stack) - 1
        needed_bqs = extra_bqs
        while until_index > 0 and needed_bqs > 0:
            if parser_state.token_stack[until_index].is_block_quote:
                needed_bqs -= 1
            until_index -= 1
        x_tokens, _ = parser_state.close_open_blocks_fn(
            parser_state,
            include_block_quotes=True,
            include_lists=True,
            was_forced=True,
            until_this_index=until_index + 1,
        )
        POGGER.debug("x_tokens>>:$:<", x_tokens)
        return x_tokens

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __reduce_containers_if_required_bq(
        parser_state: ParserState,
        position_marker: PositionMarker,
        new_tokens: List[MarkdownToken],
        split_tab: bool,
        extracted_whitespace: str,
        grab_bag: ContainerGrabBag,
        extra_bqs: int,
    ) -> Tuple[bool, str, Optional[str]]:
        x_tokens = ContainerHelper.__xx(parser_state, extra_bqs)
        count_block_quotes = sum(bool(i.is_block_quote_end) for i in x_tokens)
        assert (
            count_block_quotes == extra_bqs
        ), "Should have generated the requested number of block quote tokens."

        first_new_token = cast(EndMarkdownToken, x_tokens[0])

        did_reduce_list, extracted_whitespace, whitespace_prefix = (
            ContainerHelper.__reduce_containers_if_required_bq_list(
                parser_state, position_marker, extracted_whitespace, x_tokens
            )
        )
        was_list_ended = (
            grab_bag.container_tokens[-1].is_list_end
            if grab_bag.container_tokens and grab_bag.container_tokens[-1].is_end_token
            else False
        )

        matching_start_token = cast(
            BlockQuoteMarkdownToken, first_new_token.start_markdown_token
        )
        POGGER.debug(
            "start_markdown_token.bleading>>:$:<",
            matching_start_token.bleading_spaces,
        )
        assert (
            matching_start_token.bleading_spaces is not None
        ), "Bleading spaces must be defined by this point."
        last_newline_index = matching_start_token.bleading_spaces.rfind("\n")
        # if last_newline_index == -1:
        #     last_newline_part =matching_start_token.leading_spaces
        # else:
        last_newline_part = matching_start_token.bleading_spaces[
            last_newline_index + 1 :
        ]
        # POGGER.debug("last_newline_part>>:$:<", last_newline_part)
        if split_tab:
            assert last_newline_part.endswith(
                " "
            ), "Bleading space part must end with a space character."
            last_newline_part = last_newline_part[:-1]
            # POGGER.debug("last_newline_part>>:$:<", last_newline_part)
            split_tab = False
        # POGGER.debug("split_tab>>:$:<", split_tab)
        last_newline_part += whitespace_prefix

        # POGGER.debug("extra_end_data>>:$:<", first_new_token.extra_end_data)
        assert (
            first_new_token.extra_end_data is None
        ), "Extra data must be defined by this point."

        was_paragraph_closed = (
            new_tokens[0].is_paragraph_end
            if new_tokens and new_tokens[0].is_end_token
            else False
        )
        if did_reduce_list or was_list_ended or not was_paragraph_closed:
            first_new_token.set_extra_end_data(None)
        else:
            first_new_token.set_extra_end_data(last_newline_part)

        new_tokens.extend(x_tokens)
        new_whitespace_prefix = ContainerHelper.__handle_whitespace_prefix(
            parser_state, whitespace_prefix, last_newline_part
        )
        return split_tab, extracted_whitespace, new_whitespace_prefix

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __handle_whitespace_prefix(
        parser_state: ParserState, whitespace_prefix: str, last_newline_part: str
    ) -> Optional[str]:
        if not whitespace_prefix:
            return None

        indent_level = 0
        stack_index = len(parser_state.token_stack) - 1
        while stack_index > 0:
            if parser_state.token_stack[stack_index].is_list:
                indent_level += cast(
                    ListStartMarkdownToken,
                    parser_state.token_stack[stack_index].matching_markdown_token,
                ).indent_level
                break
            bleading_spaces = cast(
                BlockQuoteMarkdownToken,
                parser_state.token_stack[stack_index].matching_markdown_token,
            ).bleading_spaces
            assert bleading_spaces is not None
            split_bleading_spaces = bleading_spaces.split("\n")
            last_split_bleading_spaces = len(split_bleading_spaces[-1])
            indent_level += last_split_bleading_spaces
            stack_index -= 1
        return last_newline_part[indent_level:]

    # pylint: disable=too-many-arguments
    @staticmethod
    def reduce_containers_if_required(
        parser_state: ParserState,
        position_marker: PositionMarker,
        block_quote_data: BlockQuoteData,
        new_tokens: List[MarkdownToken],
        split_tab: bool,
        extracted_whitespace: str,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Given a drop in the current count of block quotes versus what is actually
        specified, reduce the containers.
        """

        POGGER.debug(
            "block_quote_data.current_count>>:$:<", block_quote_data.current_count
        )
        POGGER.debug("block_quote_data.stack_count>>:$:<", block_quote_data.stack_count)
        POGGER.debug("new_tokens>>:$:<", new_tokens)
        POGGER.debug("split_tab>>:$:<", split_tab)
        POGGER.debug("parser_state.token_stack[-1]>>:$:<", parser_state.token_stack[-1])

        # TODO While? needs to take lists into account as well
        whitespace_prefix: Optional[str] = None
        if (
            block_quote_data.current_count >= 0
            and block_quote_data.stack_count > block_quote_data.current_count
            and parser_state.token_stack[-1].is_block_quote
        ):
            split_tab, extracted_whitespace, whitespace_prefix = (
                ContainerHelper.__reduce_containers_if_required_bq(
                    parser_state,
                    position_marker,
                    new_tokens,
                    split_tab,
                    extracted_whitespace,
                    grab_bag,
                    block_quote_data.stack_count - block_quote_data.current_count,
                )
            )

        return split_tab, extracted_whitespace, whitespace_prefix

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
