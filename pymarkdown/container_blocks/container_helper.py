"""
Module to provide helper functions for containers.

These functions are typically needed in other modules than the two main
container modules.
"""

import logging
from typing import List, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.tokens.container_markdown_token import BlockQuoteMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-few-public-methods


class ContainerHelper:
    """
    Class to provide helper functions for containers.
    """

    @staticmethod
    def reduce_containers_if_required(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        new_tokens: List[MarkdownToken],
        split_tab: bool,
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
        assert block_quote_data.current_count != 0 or block_quote_data.stack_count <= 0
        POGGER.debug("parser_state.token_stack[-1]>>:$:<", parser_state.token_stack[-1])
        # While? needs to take lists into account as well
        if (
            block_quote_data.current_count > 0
            and block_quote_data.stack_count > block_quote_data.current_count
            and parser_state.token_stack[-1].is_block_quote
        ):
            x_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                include_block_quotes=True,
                was_forced=True,
                until_this_index=len(parser_state.token_stack) - 1,
            )
            POGGER.debug("x_tokens>>:$:<", x_tokens)
            assert len(x_tokens) == 1
            first_new_token = cast(EndMarkdownToken, x_tokens[0])

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

            assert last_newline_part is not None
            first_new_token.set_extra_end_data(last_newline_part)

            new_tokens.extend(x_tokens)
        return split_tab


# pylint: enable=too-few-public-methods
