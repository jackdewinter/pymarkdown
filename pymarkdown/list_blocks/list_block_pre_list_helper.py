"""
Module to provide for the initial process once we have decided to parse a list block.
"""

import logging
from typing import List, Tuple, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.leaf_blocks.leaf_block_processor_paragraph import (
    LeafBlockProcessorParagraph,
)
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods


class ListBlockPreListHelper:
    """
    Class to provide for the initial process once we have decided to parse a list block.
    """

    # pylint: disable=too-many-arguments
    @staticmethod
    def pre_list(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: str,
        marker_width_minus_one: int,
        block_quote_data: BlockQuoteData,
        adj_ws: str,
        position_marker: PositionMarker,
        container_depth: int,
    ) -> Tuple[int, int, int, int, int, List[MarkdownToken], BlockQuoteData]:
        """
        Handle the processing of the first part of the list.
        """
        (
            after_marker_ws_index,
            ws_after_marker,
            ws_before_marker,
            line_to_parse_size,
        ) = ListBlockPreListHelper.__calculate_whitespace_values(
            line_to_parse, start_index, extracted_whitespace
        )

        POGGER.debug("--$--$", start_index, start_index + 1)
        (
            indent_level,
            remaining_whitespace,
            ws_after_marker,
        ) = ListBlockPreListHelper.__calculate_indents(
            after_marker_ws_index,
            line_to_parse_size,
            marker_width_minus_one,
            ws_after_marker,
            ws_before_marker,
            adj_ws,
            container_depth,
        )

        return ListBlockPreListHelper.__check_for_list_nesting(
            parser_state,
            position_marker,
            indent_level,
            after_marker_ws_index,
            block_quote_data,
            remaining_whitespace,
            ws_after_marker,
            ws_before_marker,
        )
        # pylint: enable=too-many-arguments

    @staticmethod
    def __calculate_whitespace_values(
        line_to_parse: str, start_index: int, extracted_whitespace: str
    ) -> Tuple[int, int, int, int]:
        (
            after_marker_ws_index,
            after_marker_whitespace,
        ) = ParserHelper.extract_spaces_verified(line_to_parse, start_index + 1)
        ws_after_marker, ws_before_marker, line_to_parse_size = (
            TabHelper.calculate_length(
                after_marker_whitespace, start_index=start_index + 1
            ),
            TabHelper.calculate_length(extracted_whitespace),
            len(line_to_parse),
        )
        POGGER.debug(
            "after-marker>>$>>total=$", after_marker_whitespace, ws_after_marker
        )
        return (
            after_marker_ws_index,
            ws_after_marker,
            ws_before_marker,
            line_to_parse_size,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_indents(
        after_marker_ws_index: int,
        line_to_parse_size: int,
        marker_width_minus_one: int,
        ws_after_marker: int,
        ws_before_marker: int,
        adj_ws: str,
        container_depth: int,
    ) -> Tuple[int, int, int]:
        POGGER.debug(
            "--ws_before_marker>>$>>marker_width_minus_one>>$",
            ws_before_marker,
            marker_width_minus_one,
        )
        POGGER.debug("container_depth($)", container_depth)
        POGGER.debug(
            "after_marker_ws_index($) == line_to_parse_size($) and ws_after_marker($)",
            after_marker_ws_index,
            line_to_parse_size,
            ws_after_marker,
        )
        if (
            after_marker_ws_index == line_to_parse_size
            and ws_after_marker
            and not container_depth
        ):
            POGGER.debug("indent1")
            indent_level, remaining_whitespace, ws_after_marker = (
                2 + marker_width_minus_one + len(adj_ws),
                ws_after_marker,
                0,
            )
        else:
            POGGER.debug("indent2")
            if after_marker_ws_index == line_to_parse_size and ws_after_marker == 0:
                ws_after_marker += 1

            indent_level = (
                ws_before_marker + 1 + ws_after_marker + marker_width_minus_one
            )
            if ws_after_marker > 4:
                indent_level, remaining_whitespace, ws_after_marker = (
                    indent_level - ws_after_marker + 1,
                    ws_after_marker - 1,
                    1,
                )
            else:
                remaining_whitespace = 0

        POGGER.debug(
            "ws_after_marker>>$<<indent_level<<$<<rem<<$<<",
            ws_after_marker,
            indent_level,
            remaining_whitespace,
        )
        return indent_level, remaining_whitespace, ws_after_marker

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __check_for_list_nesting(
        parser_state: ParserState,
        position_marker: PositionMarker,
        indent_level: int,
        after_marker_ws_index: int,
        block_quote_data: BlockQuoteData,
        remaining_whitespace: int,
        ws_after_marker: int,
        ws_before_marker: int,
    ) -> Tuple[int, int, int, int, int, List[MarkdownToken], BlockQuoteData]:
        check_list_nesting = True
        if (
            parser_state.token_stack[-1].is_html_block
            or parser_state.token_stack[-1].is_fenced_code_block
        ):
            did_find, _ = LeafBlockProcessorParagraph.check_for_list_in_process(
                parser_state
            )
            if not did_find:
                indent_level = -1
                after_marker_ws_index = -1
                POGGER.debug("BAIL!")
        else:
            POGGER.debug("stack:$:", parser_state.token_stack)
            POGGER.debug("document:$:", parser_state.token_document)
            (
                did_find,
                last_list_index,
            ) = LeafBlockProcessorParagraph.check_for_list_in_process(parser_state)
            if did_find:
                POGGER.debug(
                    "stack[last_list_index]:$:",
                    parser_state.token_stack[last_list_index],
                )
                POGGER.debug(
                    "stack[last_list_index].mmt:$:",
                    parser_state.token_stack[last_list_index].matching_markdown_token,
                )
                check_list_nesting = False

        if check_list_nesting:
            (
                container_level_tokens,
                block_quote_data,
            ) = ListBlockPreListHelper.__handle_list_nesting(
                parser_state, block_quote_data, position_marker
            )
        else:
            container_level_tokens = []
        return (
            indent_level,
            remaining_whitespace,
            ws_after_marker,
            after_marker_ws_index,
            ws_before_marker,
            container_level_tokens,
            block_quote_data,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_list_nesting(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        position_marker: PositionMarker,
    ) -> Tuple[List[MarkdownToken], BlockQuoteData]:
        """
        Resolve any nesting issues with block quotes.
        """
        POGGER.debug(
            ">>block_quote_data.stack_count>>$>>block_quote_data.current_count>>$",
            block_quote_data.stack_count,
            block_quote_data.current_count,
        )
        container_level_tokens: List[MarkdownToken] = []
        adjusted_stack_count = block_quote_data.stack_count
        while block_quote_data.current_count < adjusted_stack_count:
            assert (
                not container_level_tokens
            ), "Container tokens cannot have been filled."
            last_block_index = parser_state.find_last_block_quote_on_stack()
            previous_last_block_token = cast(
                BlockQuoteMarkdownToken,
                parser_state.token_stack[last_block_index].matching_markdown_token,
            )
            POGGER.debug(
                "last_block_index>>$-->$", last_block_index, previous_last_block_token
            )
            container_level_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=last_block_index,
                include_block_quotes=True,
                include_lists=True,
            )
            POGGER.debug("container_level_tokens>>$", container_level_tokens)
            POGGER.debug("stack>>$", parser_state.token_stack)
            last_markdown_token = parser_state.token_stack[-1].matching_markdown_token
            POGGER.debug("last token>>$", last_markdown_token)
            POGGER.debug("position_marker.line_number>>$", position_marker.line_number)
            last_block_index = parser_state.find_last_block_quote_on_stack()
            POGGER.debug("last_block_index>>$", last_block_index)
            POGGER.debug(
                "parser_state.token_stack[-1]>>$", parser_state.token_stack[-1]
            )
            POGGER.debug(
                "last_markdown_token>>$",
                last_markdown_token,
            )

            first_conditional = not last_markdown_token
            second_conditional = (
                (not first_conditional)
                and last_markdown_token
                and (position_marker.line_number == last_markdown_token.line_number)
            )
            third_conditional = parser_state.token_stack[-1].is_block_quote

            secondary_conditionals = (
                first_conditional or second_conditional or third_conditional
            )
            POGGER.debug(
                "secondary_conditionals>>$ = first_conditional:$ or second_conditional:$ or "
                + "third_conditional:$",
                secondary_conditionals,
                first_conditional,
                second_conditional,
                third_conditional,
            )
            all_conditionals = last_block_index and secondary_conditionals
            POGGER.debug(
                "all_conditionals>>$ = last_block_index:$ or a2:$",
                all_conditionals,
                last_block_index,
                secondary_conditionals,
            )
            if all_conditionals:
                ListBlockPreListHelper.__handle_list_nesting_all_conditionals(
                    parser_state, last_block_index, previous_last_block_token
                )

            adjusted_stack_count -= 1

        if adjusted_stack_count != block_quote_data.stack_count:
            block_quote_data = BlockQuoteData(
                block_quote_data.current_count, adjusted_stack_count
            )
        return container_level_tokens, block_quote_data

    @staticmethod
    def __handle_list_nesting_all_conditionals(
        parser_state: ParserState,
        last_block_index: int,
        previous_last_block_token: BlockQuoteMarkdownToken,
    ) -> None:
        current_last_block_token = cast(
            BlockQuoteMarkdownToken,
            parser_state.token_stack[last_block_index].matching_markdown_token,
        )
        POGGER.debug(
            "last_block_index>>$-->$",
            last_block_index,
            current_last_block_token,
        )

        POGGER.debug(
            "prev>>$<<, current>>$<<",
            previous_last_block_token,
            current_last_block_token,
        )
        removed_leading_spaces = previous_last_block_token.remove_last_bleading_space()
        POGGER.debug("removed_leading_spaces>>$<<", removed_leading_spaces)
        assert removed_leading_spaces is not None, "Removed spaces cannot be None."
        POGGER.debug(
            "prev>>$<<, current>>$<<",
            previous_last_block_token,
            current_last_block_token,
        )
        POGGER.debug(
            "__handle_list_nesting_all_conditionals>>block_token>>$",
            current_last_block_token,
        )
        current_last_block_token.add_bleading_spaces(
            removed_leading_spaces, skip_adding_newline=True
        )
        POGGER.debug(
            "__handle_list_nesting_all_conditionals>>block_token>>$",
            current_last_block_token,
        )
        POGGER.debug(
            "prev>>$<<, current>>$<<",
            previous_last_block_token,
            current_last_block_token,
        )


# pylint: enable=too-few-public-methods
