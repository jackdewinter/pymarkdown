"""
Module to provide helper functions for containers.

These functions are typically needed in other modules than the two main
container modules.
"""

import logging
from typing import List, Optional, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
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
        extracted_whitespace: Optional[str],
        new_tokens: List[MarkdownToken],
    ) -> bool:
        did_once = False
        if extracted_whitespace is not None and parser_state.token_stack[-1].is_list:
            search_index = len(parser_state.token_stack)
            leading_space_length = (
                len(extracted_whitespace) + position_marker.index_indent
            )
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
        return did_once

    # pylint: disable=too-many-arguments
    @staticmethod
    def __reduce_containers_if_required_bq(
        parser_state: ParserState,
        position_marker: PositionMarker,
        new_tokens: List[MarkdownToken],
        split_tab: bool,
        extracted_whitespace: Optional[str],
        grab_bag: ContainerGrabBag,
    ) -> bool:
        # TODO cyclic?
        x_tokens, _ = parser_state.close_open_blocks_fn(
            parser_state,
            include_block_quotes=True,
            was_forced=True,
            until_this_index=len(parser_state.token_stack) - 1,
        )
        POGGER.debug("x_tokens>>:$:<", x_tokens)
        assert len(x_tokens) == 1
        first_new_token = cast(EndMarkdownToken, x_tokens[0])

        did_reduce_list = ContainerHelper.__reduce_containers_if_required_bq_list(
            parser_state, position_marker, extracted_whitespace, x_tokens
        )
        was_list_ended = False
        if grab_bag.container_tokens and grab_bag.container_tokens[-1].is_end_token:
            end_token = cast(EndMarkdownToken, grab_bag.container_tokens[-1])
            was_list_ended = end_token.start_markdown_token.is_list_start

        matching_start_token = cast(
            BlockQuoteMarkdownToken, first_new_token.start_markdown_token
        )
        POGGER.debug(
            "start_markdown_token.bleading>>:$:<",
            matching_start_token.bleading_spaces,
        )
        assert matching_start_token.bleading_spaces is not None
        last_newline_index = matching_start_token.bleading_spaces.rfind("\n")
        # if last_newline_index == -1:
        #     last_newline_part =matching_start_token.leading_spaces
        # else:
        last_newline_part = matching_start_token.bleading_spaces[
            last_newline_index + 1 :
        ]
        POGGER.debug("last_newline_part>>:$:<", last_newline_part)
        if split_tab:
            assert last_newline_part.endswith(" ")
            last_newline_part = last_newline_part[:-1]
            POGGER.debug("last_newline_part>>:$:<", last_newline_part)
            split_tab = False
        POGGER.debug("split_tab>>:$:<", split_tab)

        POGGER.debug("extra_end_data>>:$:<", first_new_token.extra_end_data)
        assert first_new_token.extra_end_data is None

        was_paragraph_closed = False
        if new_tokens and new_tokens[0].is_end_token:
            end_token = cast(EndMarkdownToken, new_tokens[0])
            was_paragraph_closed = end_token.start_markdown_token.is_paragraph

        if did_reduce_list or was_list_ended or not was_paragraph_closed:
            first_new_token.set_extra_end_data(None)
        else:
            first_new_token.set_extra_end_data(last_newline_part)

        new_tokens.extend(x_tokens)
        return split_tab

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def reduce_containers_if_required(
        parser_state: ParserState,
        position_marker: PositionMarker,
        block_quote_data: BlockQuoteData,
        new_tokens: List[MarkdownToken],
        split_tab: bool,
        extracted_whitespace: Optional[str],
        grab_bag: ContainerGrabBag,
    ) -> bool:
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
        # assert block_quote_data.current_count != 0 or block_quote_data.stack_count <= 0
        POGGER.debug("parser_state.token_stack[-1]>>:$:<", parser_state.token_stack[-1])

        # TODO While? needs to take lists into account as well
        if (
            block_quote_data.current_count >= 0
            and block_quote_data.stack_count > block_quote_data.current_count
            and parser_state.token_stack[-1].is_block_quote
        ):
            split_tab = ContainerHelper.__reduce_containers_if_required_bq(
                parser_state,
                position_marker,
                new_tokens,
                split_tab,
                extracted_whitespace,
                grab_bag,
            )

        # if did_close_bq and extracted_whitespace is not None and parser_state.token_stack[-1].is_list:
        #     search_index = len(parser_state.token_stack)
        #     leading_space_length = len(extracted_whitespace)
        #     did_once = False
        #     while parser_state.token_stack[search_index - 1].is_list:
        #         list_token = cast(
        #             ListStackToken, parser_state.token_stack[search_index - 1]
        #         )
        #         if list_token.indent_level <= leading_space_length:
        #             break
        #         search_index -= 1
        #         did_once = True

        #     POGGER.debug("lsl $", parser_state.token_stack[search_index])

        #     if did_once:
        #         ff = cast(EndMarkdownToken, new_tokens[-1])
        #         ff.set_extra_end_data(None)

        #         (
        #             container_level_tokens,
        #             _,
        #         ) = parser_state.close_open_blocks_fn(
        #             parser_state,
        #             until_this_index=search_index,
        #             include_lists=True,
        #             caller_can_handle_requeue=False,
        #             requeue_reset=True,
        #         )
        #         new_tokens.extend(container_level_tokens)
        return split_tab

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
