"""
Module to provide processing for the nested scenarios that may contain container blocks.
"""
from __future__ import annotations

import logging
from typing import Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_count_helper import BlockQuoteCountHelper
from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.container_blocks.container_indices import ContainerIndices
from pymarkdown.list_blocks.list_block_starts_helper import ListBlockStartsHelper
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.container_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.stack_token import ListStackToken

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods
class ContainerBlockNestedProcessor:
    """
    Class to provide processing for the nested scenarios that may contain container blocks.
    """

    @staticmethod
    def handle_nested_container_blocks(
        parser_state: ParserState,
        position_marker: PositionMarker,
        was_container_start: bool,
        avoid_block_starts: bool,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[Optional[str], bool, bool]:
        """
        Handle the processing of nested container blocks, as they can contain
        themselves and get somewhat messy.
        """
        adjusted_text_to_parse = position_marker.text_to_parse

        POGGER.debug("adjusted_text_to_parse>$<", adjusted_text_to_parse)
        POGGER.debug("index_number>$<", position_marker.index_number)
        POGGER.debug("index_indent>$<", position_marker.index_indent)
        POGGER.debug("parser_state.nested_list_start>$", parser_state.nested_list_start)
        POGGER.debug("was_container_start>$", was_container_start)

        if was_container_start and position_marker.text_to_parse:
            assert grab_bag.container_depth < 10
            nested_container_starts = (
                ContainerBlockNestedProcessor.__get_nested_container_starts(
                    parser_state,
                    position_marker.text_to_parse,
                    avoid_block_starts,
                )
            )
            POGGER.debug(
                "__handle_nested_container_blocks>nested_container_starts>>:$:<<",
                nested_container_starts,
            )

            grab_bag.adj_line_to_parse = position_marker.text_to_parse

            (
                indent_level_delta,
                already_adjusted,
                active_container_index,
            ) = ContainerBlockNestedProcessor.__check_for_nested_list_start(
                parser_state,
                nested_container_starts,
                grab_bag,
            )

            assert grab_bag.is_leaf_tokens_empty()
            adjusted_text_to_parse = ContainerBlockNestedProcessor.__do_nested_cleanup(
                parser_state,
                indent_level_delta,
                already_adjusted,
                active_container_index,
                adjusted_text_to_parse,
                grab_bag,
            )
            # POGGER.debug_with_visible_whitespace("adjusted_text_to_parse>>$>>", adjusted_text_to_parse)

            (
                adjusted_text_to_parse,
                nested_removed_text,
                was_indent_text_added,
                inner_force_list_continuation,
            ) = ContainerBlockNestedProcessor.__check_for_next_container(
                parser_state,
                position_marker,
                nested_container_starts,
                adjusted_text_to_parse,
                grab_bag,
            )
        else:
            (
                nested_removed_text,
                was_indent_text_added,
                inner_force_list_continuation,
            ) = (
                None,
                False,
                False,
            )

        # POGGER.debug_with_visible_whitespace("adjusted_text_to_parse>>$>>", adjusted_text_to_parse)
        grab_bag.line_to_parse = adjusted_text_to_parse
        return (
            nested_removed_text,
            was_indent_text_added,
            inner_force_list_continuation,
        )

    @staticmethod
    def __check_for_next_container(
        parser_state: ParserState,
        position_marker: PositionMarker,
        nested_container_starts: ContainerIndices,
        adjusted_text_to_parse: str,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[str, Optional[str], bool, bool]:
        POGGER.debug("check next container_start>stack>>$", parser_state.token_stack)
        POGGER.debug(
            "check next container_start>tokenized_document>>$",
            parser_state.token_document,
        )

        if (
            nested_container_starts.ulist_index
            or nested_container_starts.olist_index
            or nested_container_starts.block_index
        ):
            POGGER.debug(
                "check next container_start>nested_container",
            )
            (
                adjusted_text_to_parse,
                nested_removed_text,
                was_indent_text_added,
                inner_force_list_continuation,
            ) = ContainerBlockNestedProcessor.__look_for_container_blocks(
                parser_state,
                position_marker,
                grab_bag,
            )
        else:
            (
                nested_removed_text,
                was_indent_text_added,
                inner_force_list_continuation,
            ) = (None, False, False)
        parser_state.set_no_para_start_if_empty()

        return (
            adjusted_text_to_parse,
            nested_removed_text,
            was_indent_text_added,
            inner_force_list_continuation,
        )

    @staticmethod
    def __get_nested_container_starts(
        parser_state: ParserState,
        line_to_parse: str,
        avoid_block_starts: bool,
    ) -> ContainerIndices:
        POGGER.debug(
            "__handle_nested_container_blocks>stack>>:$:<<",
            line_to_parse,
        )

        POGGER.debug("check next container_start>")
        POGGER.debug("check next container_start>stack>>$", parser_state.token_stack)

        _, ex_ws_test = ParserHelper.extract_spaces(line_to_parse, 0)
        assert ex_ws_test is not None

        whitespace_scan_start_index = 0
        for token_stack_item in parser_state.token_stack:
            if token_stack_item.is_list:
                list_stack_token = cast(ListStackToken, token_stack_item)
                if list_stack_token.ws_before_marker <= len(ex_ws_test):
                    whitespace_scan_start_index = list_stack_token.ws_before_marker

        after_ws_index, ex_whitespace = ParserHelper.extract_spaces(
            line_to_parse, whitespace_scan_start_index
        )
        if not ex_whitespace:
            ex_whitespace = ""
            after_ws_index = whitespace_scan_start_index

        assert after_ws_index is not None

        nested_ulist_start, _, _, _ = ListBlockStartsHelper.is_ulist_start(
            parser_state, line_to_parse, after_ws_index, ex_whitespace, False
        )
        nested_olist_start, _, _, _ = ListBlockStartsHelper.is_olist_start(
            parser_state, line_to_parse, after_ws_index, ex_whitespace, False
        )
        nested_block_start = (
            False
            if avoid_block_starts
            else BlockQuoteCountHelper.is_block_quote_start(
                line_to_parse, after_ws_index, ex_whitespace
            )
        )

        POGGER.debug("check next container_start>stack>>$", parser_state.token_stack)

        return ContainerIndices(
            nested_ulist_start, nested_olist_start, nested_block_start
        )

    @staticmethod
    def __look_for_container_blocks(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[str, Optional[str], bool, bool]:
        """
        Look for container blocks that we can use.
        """
        POGGER.debug("check next container_start>recursing")
        adj_block, position_marker = (
            None
            if grab_bag.end_container_indices.block_index == -1
            else grab_bag.end_container_indices.block_index,
            PositionMarker(position_marker.line_number, -1, grab_bag.adj_line_to_parse),
        )
        new_container_depth = grab_bag.container_depth + 1

        POGGER.debug(
            "position_marker>:$:$:",
            position_marker.index_number,
            position_marker.text_to_parse,
        )
        POGGER.debug("adj_block>:$:", adj_block)
        POGGER.debug("\n\nRECURSING\n")
        # POGGER.debug("parser_state.token_document>$", parser_state.token_document)
        previous_document_length = len(parser_state.token_document)
        (
            produced_inner_tokens,
            adjusted_text_to_parse,
            current_bq_count_increment,
            grab_bag.requeue_line_info,
            grab_bag.did_blank,
            inner_force_list_continuation,
        ) = grab_bag.get_recurse_fn()(
            parser_state,
            position_marker,
            False,
            grab_bag.parser_properties,
            grab_bag.block_quote_data.current_count,
            new_container_depth,
            adj_block,
            grab_bag.block_quote_data.current_count,
            grab_bag.original_line,
        )
        assert (
            not grab_bag.requeue_line_info
            or not grab_bag.requeue_line_info.lines_to_requeue
        )
        assert adjusted_text_to_parse is not None

        POGGER.debug("\nRECURSED\n\n")

        # POGGER.debug("previous_document_length=$", previous_document_length)
        nested_removed_text = (
            ContainerBlockNestedProcessor.__calculate_nested_removed_text(
                parser_state, previous_document_length, grab_bag
            )
        )
        POGGER.debug("check next container_start>stack>>$", parser_state.token_stack)
        POGGER.debug(
            "check next container_start>tokenized_document>>$",
            parser_state.token_document,
        )
        POGGER.debug("check next container_start>line_parse>>$", adjusted_text_to_parse)
        if current_bq_count_increment:
            grab_bag.block_quote_data = BlockQuoteData(
                grab_bag.block_quote_data.current_count + current_bq_count_increment,
                parser_state.count_of_block_quotes_on_stack(),
            )

        POGGER.debug("produced_inner_tokens=$", produced_inner_tokens)
        was_indent_text_added = bool(
            parser_state.token_stack[-1].is_indented_code_block
            and produced_inner_tokens
            and len(produced_inner_tokens) == 1
            and produced_inner_tokens[0].is_text
        )
        POGGER.debug("was_indent_text_added=$", was_indent_text_added)

        # POGGER.debug("parser_state.token_document>$", parser_state.token_document)
        parser_state.token_document.extend(produced_inner_tokens)
        POGGER.debug("parser_state.token_document>$", parser_state.token_document)
        # POGGER.debug("did_process_blank_line>$", did_process_blank_line)

        return (
            adjusted_text_to_parse,
            nested_removed_text,
            was_indent_text_added,
            inner_force_list_continuation,
        )

    @staticmethod
    def __calculate_nested_removed_text(
        parser_state: ParserState,
        previous_document_length: int,
        grab_bag: ContainerGrabBag,
    ) -> Optional[str]:
        nested_removed_text = None
        POGGER.debug("__calculate_nested_removed_text")
        POGGER.debug(
            "__cnrt->token_doc($)",
            ParserHelper.make_value_visible(parser_state.token_document),
        )
        if previous_document_length != len(parser_state.token_document):
            POGGER.debug(
                "\ncheck next container_start>added tokens:$:",
                parser_state.token_document[previous_document_length:],
            )
            if parser_state.token_document[-1].is_block_quote_start:
                block_quote_token = cast(
                    BlockQuoteMarkdownToken, parser_state.token_document[-1]
                )
                nested_removed_text = ContainerBlockNestedProcessor.__calculate_nested_removed_text_block_quote(
                    parser_state, block_quote_token, grab_bag
                )
        if not nested_removed_text:
            POGGER.debug("__cnrt:nested_removed_text:$:", nested_removed_text)
            last_container_index = parser_state.find_last_container_on_stack()
            if (
                last_container_index > 0
                and parser_state.token_stack[last_container_index].is_block_quote
            ):
                block_quote_token = cast(
                    BlockQuoteMarkdownToken,
                    parser_state.token_stack[
                        last_container_index
                    ].matching_markdown_token,
                )
                assert block_quote_token.bleading_spaces is not None
                split_spaces = block_quote_token.bleading_spaces.split(
                    ParserHelper.newline_character
                )
                nested_removed_text = str(split_spaces[-1])
        POGGER.debug("__calculate_nested_removed_text<<:$:", nested_removed_text)
        return nested_removed_text

    @staticmethod
    def __calculate_nested_removed_text_block_quote(
        parser_state: ParserState,
        block_quote_token: BlockQuoteMarkdownToken,
        grab_bag: ContainerGrabBag,
    ) -> str:
        assert block_quote_token.bleading_spaces is not None
        split_spaces = block_quote_token.bleading_spaces.split(
            ParserHelper.newline_character
        )
        nested_removed_text = str(split_spaces[-1])
        POGGER.debug("nested_removed_text:$:", nested_removed_text)
        if (
            len(parser_state.token_document) > 1
            and parser_state.token_document[-2].is_new_list_item
            and parser_state.token_document[-2].line_number
            == parser_state.token_document[-1].line_number
        ):
            column_number_delta = (
                parser_state.token_document[-1].column_number
                - parser_state.token_document[-2].column_number
            )
            block_quote_character_index = nested_removed_text.index(">")
            nested_removed_text_length = len(nested_removed_text)
            POGGER.debug(
                "column_number_delta=$, block_quote_character_index=$, nested_removed_text_length=$",
                column_number_delta,
                block_quote_character_index,
                nested_removed_text_length,
            )
            adjusted_length = (
                parser_state.token_document[-2].column_number
                - 1
                + column_number_delta
                + (nested_removed_text_length - block_quote_character_index)
            )
            POGGER.debug("adjusted_length=$", adjusted_length)
            if adjusted_length != nested_removed_text_length:
                assert parser_state.original_line_to_parse
                nested_removed_text = parser_state.original_line_to_parse[
                    :adjusted_length
                ]
                POGGER.debug("previous:$:", nested_removed_text)
                grab_bag.weird_adjusted_text = nested_removed_text
        return nested_removed_text

    @staticmethod
    def __check_for_nested_list_start(
        parser_state: ParserState,
        nested_container_starts: ContainerIndices,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[int, bool, int]:
        active_container_index = max(
            grab_bag.end_container_indices.ulist_index,
            grab_bag.end_container_indices.olist_index,
            grab_bag.end_container_indices.block_index,
        )
        POGGER.debug(
            "check next container_start>max>>$>>bq>>$",
            active_container_index,
            grab_bag.end_container_indices.block_index,
        )
        indent_level_delta, already_adjusted = 0, False
        if (
            grab_bag.end_container_indices.block_index != -1
            and not nested_container_starts.ulist_index
            and not nested_container_starts.olist_index
        ):
            assert active_container_index == grab_bag.end_container_indices.block_index
            POGGER.debug(
                "parser_state.nested_list_start>>$<<",
                parser_state.nested_list_start,
            )
            POGGER.debug(
                "parser_state.token_document>>$<<", parser_state.token_document
            )
            if parser_state.nested_list_start and grab_bag.adj_line_to_parse.strip():
                (
                    grab_bag.start_index,
                    indent_level,
                    indent_was_adjusted,
                    indent_level_delta,
                ) = ContainerBlockNestedProcessor.__calculate_initial_list_adjustments(
                    parser_state,
                    grab_bag.adj_line_to_parse,
                    grab_bag.end_container_indices,
                )
                already_adjusted = ContainerBlockNestedProcessor.__adjust_line_2(
                    parser_state,
                    indent_level,
                    nested_container_starts,
                    indent_was_adjusted,
                    grab_bag,
                )
        return (
            indent_level_delta,
            already_adjusted,
            active_container_index,
        )

    @staticmethod
    def __adjust_line_2(
        parser_state: ParserState,
        indent_level: int,
        nested_container_starts: ContainerIndices,
        indent_was_adjusted: bool,
        grab_bag: ContainerGrabBag,
    ) -> bool:
        if (
            parser_state.token_document[-1].is_blank_line
            and (grab_bag.end_container_indices.block_index + grab_bag.start_index)
            < indent_level
        ):
            POGGER.debug("\n\nBOOM\n\n")

            y_tokens = []
            while parser_state.token_document[-1].is_blank_line:
                y_tokens.append(parser_state.token_document[-1])
                del parser_state.token_document[-1]

            x_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                include_lists=True,
            )
            parser_state.token_document.extend(x_tokens)
            parser_state.token_document.extend(y_tokens)
        elif (
            not nested_container_starts.block_index
            and grab_bag.adj_line_to_parse
            and grab_bag.adj_line_to_parse[0] == ParserHelper.space_character
            and indent_was_adjusted
            and parser_state.nested_list_start
        ):
            assert parser_state.nested_list_start is not None
        return False

    @staticmethod
    def __calculate_initial_list_adjustments(
        parser_state: ParserState,
        adj_line_to_parse: str,
        end_container_indices: ContainerIndices,
    ) -> Tuple[int, int, bool, int]:
        start_index, _ = ParserHelper.extract_spaces(adj_line_to_parse, 0)
        assert start_index is not None
        POGGER.debug("start_index>>$<<", start_index)

        assert parser_state.nested_list_start is not None
        assert parser_state.nested_list_start.matching_markdown_token is not None
        POGGER.debug(
            "parser_state.nested_list_start.matching_markdown_token>>$<<",
            parser_state.nested_list_start.matching_markdown_token,
        )
        list_start_token_index = parser_state.token_document.index(
            parser_state.nested_list_start.matching_markdown_token
        )
        POGGER.debug(
            "list_start_token_index>>$<<",
            list_start_token_index,
        )
        if list_start_token_index < (len(parser_state.token_document) - 1):
            token_after_list_start = parser_state.token_document[
                list_start_token_index + 1
            ]
            POGGER.debug(
                "token_after_list_start>>$<<",
                token_after_list_start,
            )
            assert (
                parser_state.nested_list_start.matching_markdown_token.line_number
                == token_after_list_start.line_number
            )
            column_number_delta = (
                token_after_list_start.column_number
                - parser_state.nested_list_start.matching_markdown_token.column_number
            )
        else:
            column_number_delta = 0
        POGGER.debug(
            "column_number_delta>>$<<",
            column_number_delta,
        )
        indent_level_delta, indent_level, adjusted_indent_level = (
            0,
            parser_state.nested_list_start.indent_level,
            column_number_delta + end_container_indices.block_index,
        )
        POGGER.debug(
            "adjusted_indent_level>>$<<  indent_level>$",
            adjusted_indent_level,
            indent_level,
        )
        indent_was_adjusted = indent_level != adjusted_indent_level
        if indent_level > adjusted_indent_level:
            indent_level_delta = indent_level - adjusted_indent_level
        indent_level = column_number_delta + end_container_indices.block_index

        return start_index, indent_level, indent_was_adjusted, indent_level_delta

    # pylint: disable=too-many-arguments
    @staticmethod
    def __do_nested_cleanup(
        parser_state: ParserState,
        delta: int,
        already_adjusted: bool,
        active_container_index: int,
        adjusted_text_to_parse: str,
        grab_bag: ContainerGrabBag,
    ) -> str:
        if delta or already_adjusted:
            adjusted_text_to_parse = grab_bag.adj_line_to_parse
        else:
            POGGER.debug("active_container_index<<$<<", active_container_index)
            adjustment_filler = ParserHelper.repeat_string(
                ParserHelper.space_character, active_container_index
            )
            grab_bag.adj_line_to_parse = (
                f"{adjustment_filler}{grab_bag.adj_line_to_parse}"
            )

        parser_state.token_document.extend(grab_bag.container_tokens)
        grab_bag.clear_container_tokens()
        return adjusted_text_to_parse

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
