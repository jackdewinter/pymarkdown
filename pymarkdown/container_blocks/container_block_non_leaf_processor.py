"""
Module to provide processing for the non-leaf scenarios that may contain container blocks.
"""

from __future__ import annotations

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_processor import BlockQuoteProcessor
from pymarkdown.container_blocks.container_block_nested_processor import (
    ContainerBlockNestedProcessor,
)
from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.container_blocks.container_indices import ContainerIndices
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.leaf_blocks.leaf_block_processor_paragraph import (
    LeafBlockProcessorParagraph,
)
from pymarkdown.list_blocks.list_block_processor import ListBlockProcessor
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class ContainerBlockNonLeafProcessor:
    """
    Class to provide processing for the non-leaf scenarios that may contain container blocks.
    """

    @staticmethod
    def handle_non_leaf_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        # POGGER.debug("ttp>>:$:<", position_marker.text_to_parse)
        # POGGER.debug("index_number>>:$:<", position_marker.index_number)
        # POGGER.debug("index_indent>>:$:<", position_marker.index_indent)
        ContainerBlockNonLeafProcessor.__handle_pre_processed_indent(
            parser_state,
            position_marker,
            grab_bag,
        )
        if ContainerBlockNonLeafProcessor.__look_for_override(
            parser_state,
            position_marker,
            grab_bag,
        ):
            ContainerBlockNonLeafProcessor.__handle_normal_containers(
                parser_state,
                position_marker,
                grab_bag,
            )

    @staticmethod
    def __handle_pre_processed_indent(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        assert (
            grab_bag.extracted_whitespace is not None
        ), "Extracted whitespace must be defined at this point."
        need_leading_whitespace_processing = (
            grab_bag.container_depth < (len(parser_state.token_stack) - 1)
            and len(grab_bag.extracted_whitespace) >= 4
            and not parser_state.token_stack[-1].is_html_block
            and not parser_state.token_stack[-1].is_fenced_code_block
        )
        need_trailing_indent_processing = (
            grab_bag.container_depth >= len(parser_state.token_stack) - 1
            and position_marker.index_number == -1
        )
        if need_trailing_indent_processing:
            POGGER.debug(">>trailing_indent_processing")
            ContainerBlockNonLeafProcessor.__handle_trailing_indent_with_block_quote(
                parser_state, grab_bag
            )
        elif need_leading_whitespace_processing:
            POGGER.debug(">>leading_whitespace_preprocessing")
            ContainerBlockNonLeafProcessor.__determine_leading_whitespace_preprocessing(
                parser_state,
                position_marker,
                grab_bag,
            )

    @staticmethod
    def __look_for_override(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> bool:
        if grab_bag.have_pre_processed_indent:
            (
                grab_bag.can_continue,
                grab_bag.line_to_parse,
                grab_bag.start_index,
                grab_bag.removed_chars_at_start_of_line,
            ) = (
                True,
                position_marker.text_to_parse[grab_bag.indent_already_processed :],
                grab_bag.indent_already_processed,
                grab_bag.indent_already_processed,
            )
        keep_processing = (
            not grab_bag.can_continue
            and not grab_bag.do_skip_containers_before_leaf_blocks
        )
        if keep_processing:
            last_container_stack_token = parser_state.token_stack[
                parser_state.find_last_container_on_stack()
            ]
            POGGER.debug("last_container_stack_token>>$", last_container_stack_token)
            if last_container_stack_token.is_block_quote:
                block_token = cast(
                    BlockQuoteMarkdownToken,
                    last_container_stack_token.matching_markdown_token,
                )
                assert (
                    block_token.bleading_spaces is not None
                ), "Bleading spaces must be defined by this point."
                split_spaces = block_token.bleading_spaces.split(
                    ParserHelper.newline_character
                )
                last_leading_space = split_spaces[-1]
                ex_ws_index, _ = ParserHelper.extract_spaces(last_leading_space, 0)
                assert (
                    grab_bag.adj_ws is not None
                ), "Adjusted whitespace must be defined by this point."
                if (
                    len(grab_bag.adj_ws) >= 4
                    and grab_bag.indent_used_by_container
                    and grab_bag.indent_used_by_container == ex_ws_index
                ):
                    keep_processing = False
                    grab_bag.indent_already_processed = len(last_leading_space)
                    grab_bag.weird_adjusted_text = last_leading_space
                    (
                        grab_bag.can_continue,
                        grab_bag.line_to_parse,
                        grab_bag.start_index,
                        grab_bag.removed_chars_at_start_of_line,
                    ) = (
                        True,
                        position_marker.text_to_parse[
                            grab_bag.indent_already_processed :
                        ],
                        grab_bag.indent_already_processed,
                        grab_bag.indent_already_processed,
                    )
        return keep_processing

    @staticmethod
    def __handle_normal_containers(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        (
            did_process,
            avoid_block_starts,
        ) = ContainerBlockNonLeafProcessor.__check_for_container_starts(
            parser_state,
            position_marker,
            grab_bag,
        )

        if grab_bag.requeue_line_info or grab_bag.did_blank:
            grab_bag.can_continue = False
            return

        nested_force_list_continuation = (
            ContainerBlockNonLeafProcessor.__handle_nested_blocks(
                parser_state,
                position_marker,
                did_process,
                avoid_block_starts,
                grab_bag,
            )
        )
        if grab_bag.do_force_list_continuation:
            POGGER.debug(
                "nested_force_list_continuation=$", nested_force_list_continuation
            )
            assert (
                not nested_force_list_continuation
            ), "This cannot be a nested and forced list continuation."
        if grab_bag.can_continue:
            did_process = ContainerBlockNonLeafProcessor.__handle_block_continuations(
                parser_state,
                position_marker,
                did_process,
                grab_bag,
            )

    @staticmethod
    def __handle_trailing_indent_with_block_quote(
        parser_state: ParserState,
        grab_bag: ContainerGrabBag,
    ) -> None:
        grab_bag.did_indent_processing = True
        assert (
            grab_bag.extracted_whitespace is not None
        ), "Extracted whitespace must be defined at this point."
        for stack_capture_index in range(1, len(parser_state.token_stack)):
            POGGER.debug(
                "$>stack:$:",
                stack_capture_index,
                parser_state.token_stack[stack_capture_index],
            )
            inner_token = parser_state.token_stack[
                stack_capture_index
            ].matching_markdown_token
            assert (
                inner_token is not None
            ), "All container and leaf tokens have a matching markdown token."
            POGGER.debug(
                "$>token:$:",
                stack_capture_index,
                inner_token,
            )
            if inner_token.is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, inner_token)
                assert (
                    block_quote_token.bleading_spaces is not None
                ), "Bleading spaces must be defined by this point."
                split_spaces = block_quote_token.bleading_spaces.split(
                    ParserHelper.newline_character
                )
                grab_bag.indent_already_processed = len(split_spaces[-1])
            else:
                assert (
                    inner_token.is_list_start
                ), "If it is not a block start, it must be a list start."
                list_token = cast(ListStartMarkdownToken, inner_token)
                grab_bag.indent_already_processed = list_token.indent_level
        delta = len(grab_bag.extracted_whitespace) - grab_bag.indent_already_processed
        POGGER.debug("len(ws)=$", len(grab_bag.extracted_whitespace))
        POGGER.debug("len(containers)=$", grab_bag.indent_already_processed)
        grab_bag.have_pre_processed_indent = (
            grab_bag.indent_already_processed != -1 and delta >= 4
        )

        grab_bag.do_skip_containers_before_leaf_blocks = (
            grab_bag.have_pre_processed_indent
        )

    @staticmethod
    def __determine_leading_whitespace_preprocessing(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        assert (
            grab_bag.extracted_whitespace is not None
        ), "Extracted whitespace must be defined at this point."
        grab_bag.indent_used_by_container = 0
        if grab_bag.is_para_continue and not grab_bag.container_depth:
            ContainerBlockNonLeafProcessor.__special_list_block_block(
                parser_state, position_marker, grab_bag
            )
        elif not grab_bag.is_para_continue:
            POGGER.debug(
                "position_marker.index_number:$:", position_marker.index_number
            )
            if position_marker.index_number == -1 and grab_bag.container_depth:
                leading_whitespace = (
                    ContainerBlockNonLeafProcessor.__calculate_indent_used_by_container(
                        parser_state,
                        position_marker,
                        grab_bag.extracted_whitespace,
                        grab_bag,
                    )
                )
            else:
                assert (
                    grab_bag.extracted_whitespace is not None
                ), "Extracted whitespace must be defined by this point."
                leading_whitespace = grab_bag.extracted_whitespace

            if len(leading_whitespace) >= 4:
                POGGER.debug(">>leading_whitespace_processing")
                ContainerBlockNonLeafProcessor.__handle_leading_whitespace(
                    parser_state,
                    position_marker,
                    leading_whitespace,
                    grab_bag,
                )
                (
                    grab_bag.did_indent_processing,
                    grab_bag.was_indent_already_processed,
                ) = (True, bool(grab_bag.container_depth))
            POGGER.debug("parser_state.token_document=$", parser_state.token_document)

    @staticmethod
    def __check_for_container_starts(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[bool, bool]:
        parser_state.nested_list_start = None
        ulist_index = -1
        olist_index = -1
        (
            did_process,
            block_index,
            avoid_block_starts,
        ) = ContainerBlockNonLeafProcessor.__get_block_start_index(
            parser_state,
            position_marker,
            grab_bag,
        )
        if grab_bag.can_continue:
            # POGGER.debug(">>avoid_block_starts>>$", avoid_block_starts)
            # POGGER.debug(">>did_process>>$", did_process)

            (
                did_process,
                ulist_index,
            ) = ContainerBlockNonLeafProcessor.__get_list_start_index(
                parser_state,
                position_marker,
                True,
                did_process,
                grab_bag,
            )

        if grab_bag.can_continue:
            # POGGER.debug("was_container_start>>$", was_container_start)
            (
                did_process,
                olist_index,
            ) = ContainerBlockNonLeafProcessor.__get_list_start_index(
                parser_state,
                position_marker,
                False,
                did_process,
                grab_bag,
            )

        grab_bag.end_container_indices = ContainerIndices(
            block_index=block_index, ulist_index=ulist_index, olist_index=olist_index
        )
        return (
            did_process,
            avoid_block_starts,
        )

    @staticmethod
    def __handle_nested_blocks(
        parser_state: ParserState,
        position_marker: PositionMarker,
        was_container_start: bool,
        avoid_block_starts: bool,
        grab_bag: ContainerGrabBag,
    ) -> bool:
        grab_bag.last_list_start_index = 0
        if grab_bag.end_container_indices.block_index != -1:
            assert grab_bag.last_block_quote_index in (
                grab_bag.end_container_indices.block_index - 1,
                grab_bag.end_container_indices.block_index,
            ), "Sanity check for block index failed."
        elif grab_bag.end_container_indices.olist_index != -1:
            grab_bag.last_list_start_index = grab_bag.end_container_indices.olist_index
        elif grab_bag.end_container_indices.ulist_index != -1:
            grab_bag.last_list_start_index = grab_bag.end_container_indices.ulist_index

        if not parser_state.token_stack[-1].is_fenced_code_block:
            new_position_marker = PositionMarker(
                position_marker.line_number,
                grab_bag.start_index,
                grab_bag.line_to_parse,
            )
            # POGGER.debug("was_container_start>>$", was_container_start)
            (
                nested_removed_text,
                was_indent_text_added,
                nested_force_list_continuation,
            ) = ContainerBlockNestedProcessor.handle_nested_container_blocks(
                parser_state,
                new_position_marker,
                was_container_start,
                avoid_block_starts,
                grab_bag,
            )
        else:
            (
                nested_removed_text,
                was_indent_text_added,
                nested_force_list_continuation,
            ) = (None, False, False)

        POGGER.debug_with_visible_whitespace(
            "nested_removed_text>>>:$:", nested_removed_text
        )
        if nested_removed_text is not None:
            grab_bag.text_removed_by_container = nested_removed_text
        grab_bag.can_continue = not (
            grab_bag.container_depth or grab_bag.did_blank or was_indent_text_added
        )
        POGGER.debug(
            ">>can_continue>>:$: = not(container_depth($) or "
            + "did_process_blank_line($) or was_indent_text_added($))",
            grab_bag.can_continue,
            grab_bag.container_depth,
            grab_bag.did_blank,
            was_indent_text_added,
        )
        return nested_force_list_continuation

    @staticmethod
    def __handle_block_continuations(
        parser_state: ParserState,
        position_marker: PositionMarker,
        did_process: bool,
        grab_bag: ContainerGrabBag,
    ) -> bool:
        if not did_process:
            did_process = ContainerBlockNonLeafProcessor.__process_list_in_progress(
                parser_state,
                position_marker.index_indent,
                grab_bag,
            )
            if not grab_bag.requeue_line_info:
                ContainerBlockNonLeafProcessor.__process_lazy_lines(
                    parser_state,
                    position_marker,
                    grab_bag,
                )
        else:
            is_paragraph_continuation = (
                bool(parser_state.token_stack)
                and parser_state.token_stack[-1].is_paragraph
            )
            list_index = parser_state.find_last_list_block_on_stack()
            block_index = parser_state.find_last_block_quote_on_stack()
            assert (
                not grab_bag.was_paragraph_continuation
            ), "This cannot be a paragraph continuation."
            grab_bag.was_paragraph_continuation = (
                is_paragraph_continuation and block_index > list_index
            )

        grab_bag.can_continue = not grab_bag.requeue_line_info
        return did_process

    @staticmethod
    def __special_list_block_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        if not (
            parser_state.token_stack[1].is_list
            and parser_state.token_stack[2].is_block_quote
            and parser_state.token_stack[3].is_block_quote
            and parser_state.token_stack[4].is_paragraph
            and parser_state.token_stack[1].matching_markdown_token
            and parser_state.token_stack[3].matching_markdown_token
            and parser_state.token_stack[1].matching_markdown_token.line_number
            == parser_state.token_stack[3].matching_markdown_token.line_number
        ):
            return
        list_token = cast(
            ListStartMarkdownToken,
            parser_state.token_stack[1].matching_markdown_token,
        )
        container_x_used_indent = list_token.indent_level
        assert (
            grab_bag.extracted_whitespace is not None
        ), "Extracted whitespace must be defined at this point."
        extracted_whitespace_length = len(grab_bag.extracted_whitespace)
        POGGER.debug("text_to_parse=:$:", position_marker.text_to_parse)
        POGGER.debug(
            "text_to_parse[rt($)]=:$:",
            extracted_whitespace_length,
            position_marker.text_to_parse[extracted_whitespace_length],
        )
        POGGER.debug("index_number=:$:", position_marker.index_number)
        if not (
            container_x_used_indent != extracted_whitespace_length
            and position_marker.text_to_parse[extracted_whitespace_length] == ">"
            and extracted_whitespace_length - container_x_used_indent >= 4
        ):
            return
        POGGER.debug("__special_list_block_block>>list_token>>$", list_token)
        list_token.add_leading_spaces(
            grab_bag.extracted_whitespace[:container_x_used_indent]
        )
        POGGER.debug("__special_list_block_block>>list_token>>$", list_token)
        (
            grab_bag.do_skip_containers_before_leaf_blocks,
            grab_bag.did_indent_processing,
            grab_bag.have_pre_processed_indent,
            grab_bag.do_force_leaf_token_parse,
            grab_bag.indent_already_processed,
        ) = (True, True, True, True, container_x_used_indent)

    @staticmethod
    def __calculate_indent_used_by_container(
        parser_state: ParserState,
        position_marker: PositionMarker,
        leading_whitespace: Optional[str],
        grab_bag: ContainerGrabBag,
    ) -> str:
        POGGER.debug("original_line_to_parse:$:", parser_state.original_line_to_parse)
        POGGER.debug("leading_whitespace:$:", leading_whitespace)
        POGGER.debug("text_to_parse=:$:", position_marker.text_to_parse)
        POGGER.debug("parser_state.token_stack=:$:", parser_state.token_stack)
        stack_search_index, current_indent = 1, 0
        assert (
            parser_state.original_line_to_parse is not None
        ), "Original line must be defined by this point."
        while stack_search_index <= grab_bag.container_depth:
            if parser_state.token_stack[stack_search_index].is_block_quote:
                current_indent = parser_state.original_line_to_parse.find(">")
                assert (
                    current_indent != -1
                ), "Since we have a block quote, there should be at least one block quote start character."
                assert (
                    parser_state.original_line_to_parse[current_indent + 1]
                    == ParserHelper.space_character
                ), "After the start character must be a space."
                current_indent += 1

                # TODO add tests with no space between `>` and next block
                assert (
                    current_indent < len(parser_state.original_line_to_parse)
                    and parser_state.original_line_to_parse[current_indent]
                    == ParserHelper.space_character
                ), "After the start character must be a space."
                current_indent += 1
            else:
                assert parser_state.token_stack[
                    stack_search_index
                ].is_list, "If not a block quote, this must be a list."
                list_token = cast(
                    ListStartMarkdownToken, parser_state.token_stack[stack_search_index]
                )
                delta = list_token.indent_level - current_indent
                POGGER.debug("delta=:$:", delta)
                current_indent += delta
            stack_search_index += 1
        assert (
            stack_search_index > grab_bag.container_depth
        ), "The new index must be more than the container depth."
        _, leading_whitespace = ParserHelper.extract_spaces_verified(
            parser_state.original_line_to_parse, current_indent
        )
        POGGER.debug("leading_whitespace=:$:", leading_whitespace)
        grab_bag.indent_used_by_container = current_indent
        return leading_whitespace

    @staticmethod
    def __handle_leading_whitespace(
        parser_state: ParserState,
        position_marker: PositionMarker,
        leading_whitespace: str,
        grab_bag: ContainerGrabBag,
    ) -> None:
        grab_bag.indent_already_processed, found_stack_index, remaining_whitespace = (
            0,
            0,
            leading_whitespace[:],
        )
        POGGER.debug(">remaining_whitespace:$:", remaining_whitespace)
        for i in range(grab_bag.container_depth + 1, len(parser_state.token_stack)):
            (
                do_break,
                found_stack_index,
                remaining_whitespace,
            ) = ContainerBlockNonLeafProcessor.__handle_leading_whitespace_loop(
                parser_state,
                i,
                remaining_whitespace,
                grab_bag,
            )
            if do_break:
                break
        POGGER.debug(">stack_index:$:", found_stack_index)
        if found_stack_index:
            grab_bag.have_pre_processed_indent = True
            close_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                include_lists=True,
                include_block_quotes=True,
                was_forced=True,
                until_this_index=found_stack_index,
            )
            grab_bag.extend_container_tokens(close_tokens)
            ind = parser_state.find_last_container_on_stack()
            if parser_state.token_stack[ind].is_list:
                ind2 = parser_state.find_last_block_quote_on_stack()
                block_quote_end_index = (
                    grab_bag.indent_used_by_container + 1 if ind2 else 0
                )
                extra_indent = 1 if grab_bag.container_depth else 0
                list_token = cast(
                    ListStartMarkdownToken,
                    parser_state.token_stack[ind].matching_markdown_token,
                )
                POGGER.debug("__handle_leading_whitespace>>list_token>>$", list_token)
                list_token.add_leading_spaces(
                    position_marker.text_to_parse[
                        block_quote_end_index : grab_bag.indent_already_processed
                        + extra_indent
                    ]
                )
                POGGER.debug("__handle_leading_whitespace>>list_token>>$", list_token)

    @staticmethod
    def __handle_leading_whitespace_loop(
        parser_state: ParserState,
        i: int,
        remaining_whitespace: str,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[bool, int, str]:
        # POGGER.debug(
        #     "$>remaining_whitespace:$:($)",
        #     i,
        #     remaining_whitespace,
        #     len(remaining_whitespace),
        # )
        # POGGER.debug("$>stack:$:", i, parser_state.token_stack[i])
        # POGGER.debug(
        #     "$>token:$:", i, parser_state.token_stack[i].matching_markdown_token
        # )
        inner_token, xx, found_stack_index, remaining_whitespace = (
            ContainerBlockNonLeafProcessor.__handle_leading_whitespace_loop_a(
                parser_state, i, remaining_whitespace
            )
        )
        if xx:
            return True, found_stack_index, remaining_whitespace
        list_token = cast(ListStartMarkdownToken, inner_token)
        assert (
            grab_bag.indent_used_by_container >= 0
        ), "If using a container, should have processed indent."
        remaining_indent = list_token.indent_level - (
            grab_bag.indent_already_processed + grab_bag.indent_used_by_container
        )
        # POGGER.debug("$>remaining_indent:$:", i, remaining_indent)
        left_whitespace = remaining_whitespace[:remaining_indent]
        # POGGER.debug("$>left_whitespace:$:", i, left_whitespace)
        if len(left_whitespace) < remaining_indent:
            if len(remaining_whitespace) >= 4:
                found_stack_index = i
            # POGGER.debug("3-->")
            return True, found_stack_index, remaining_whitespace
        remaining_whitespace = remaining_whitespace[remaining_indent:]
        grab_bag.indent_already_processed = list_token.indent_level
        return False, found_stack_index, remaining_whitespace

    @staticmethod
    def __handle_leading_whitespace_loop_a(
        parser_state: ParserState, i: int, remaining_whitespace: str
    ) -> Tuple[Optional[MarkdownToken], bool, int, str]:
        found_stack_index = 0
        if (inner_token := parser_state.token_stack[i].matching_markdown_token) is None:
            assert (
                parser_state.token_stack[i].was_link_definition_started
                or parser_state.token_stack[i].was_table_block_started
            ), "If there is no matching stack token, this must be a link definition or table."
            return inner_token, True, 0, remaining_whitespace
        if inner_token.is_block_quote_start:
            start_bq_index = remaining_whitespace.find(">")
            if start_bq_index < 0 or start_bq_index >= 4:
                # POGGER.debug("1-->$>start_bq_index:$:", i, start_bq_index)
                # POGGER.debug("$>remaining_whitespace:$:", i, remaining_whitespace)
                if len(remaining_whitespace) >= 4:
                    found_stack_index = i
                return inner_token, True, found_stack_index, remaining_whitespace
            raise AssertionError()
        if not inner_token.is_list_start:
            # POGGER.debug("2-->")
            if len(remaining_whitespace) >= 4:
                found_stack_index = (
                    i + 1 if parser_state.token_stack[i].is_indented_code_block else i
                )
            return inner_token, True, found_stack_index, remaining_whitespace
        return inner_token, False, found_stack_index, remaining_whitespace

    @staticmethod
    def __process_lazy_lines(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        assert grab_bag.is_leaf_tokens_empty(), "No leaf tokens should be present yet."
        POGGER.debug("clt>>lazy-check")

        after_ws_index, ex_whitespace = ParserHelper.extract_spaces_verified(
            grab_bag.line_to_parse, 0
        )
        remaining_line = grab_bag.line_to_parse[after_ws_index:]
        POGGER.debug("__process_lazy_lines>>mod->ltp>$<", remaining_line)
        POGGER.debug("__process_lazy_lines>>mod->ews>$<", ex_whitespace)

        (
            lazy_tokens,
            grab_bag.block_quote_data,
            grab_bag.was_paragraph_continuation,
        ) = BlockQuoteProcessor.check_for_lazy_handling(
            parser_state,
            position_marker,
            grab_bag.block_quote_data,
            remaining_line,
            ex_whitespace,
            grab_bag.was_paragraph_continuation,
            grab_bag.original_line,
        )
        grab_bag.extend_container_tokens(lazy_tokens)

    @staticmethod
    def __get_block_start_index(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[bool, int, bool]:
        POGGER.debug("text_to_parse>$<", position_marker.text_to_parse)
        POGGER.debug("index_number>$<", position_marker.index_number)
        POGGER.debug("index_indent>$<", position_marker.index_indent)
        new_position_marker = PositionMarker(
            position_marker.line_number,
            grab_bag.start_index,
            position_marker.text_to_parse,
        )
        POGGER.debug("text_to_parse>$<", new_position_marker.text_to_parse)
        POGGER.debug("index_number>$<", new_position_marker.index_number)
        POGGER.debug("container_start_bq_count>$<", grab_bag.container_start_bq_count)
        assert (
            grab_bag.container_start_bq_count is not None
        ), "If here, we should have a count of bq starts."
        (
            did_process,
            block_index,
            block_leaf_tokens,
            block_container_tokens,
            avoid_block_starts,
        ) = BlockQuoteProcessor.handle_block_quote_block(
            parser_state,
            new_position_marker,
            grab_bag,
        )
        grab_bag.extend_container_tokens(block_container_tokens)
        grab_bag.extend_leaf_tokens(block_leaf_tokens)

        if grab_bag.requeue_line_info:
            POGGER.debug(">>requeuing lines after looking for block start. returning.")

        if grab_bag.did_blank and not grab_bag.requeue_line_info:
            ContainerBlockNonLeafProcessor.__get_block_start_index_handle_blank_line(
                parser_state, grab_bag, block_leaf_tokens
            )

        grab_bag.can_continue = (
            not grab_bag.requeue_line_info and not grab_bag.did_blank
        )
        return (
            did_process,
            block_index,
            avoid_block_starts,
        )

    @staticmethod
    def __get_block_start_index_handle_blank_line(
        parser_state: ParserState,
        grab_bag: ContainerGrabBag,
        block_leaf_tokens: List[MarkdownToken],
    ) -> None:
        assert (
            block_leaf_tokens and block_leaf_tokens[-1].is_blank_line
        ), "should be a blank at the end"
        POGGER.debug(">>already handled blank line. returning.")
        grab_bag.extend_container_tokens_with_leaf_tokens()
        stack_index = len(parser_state.token_stack) - 1
        if (
            stack_index > 2
            and parser_state.token_stack[stack_index].is_block_quote
            and parser_state.token_stack[stack_index - 1].is_block_quote
            and parser_state.token_stack[stack_index - 2].is_list
        ):
            list_stack_index = stack_index - 2
            list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[list_stack_index].matching_markdown_token,
            )
            assert list_token is not None

            if list_token.line_number != block_leaf_tokens[-1].line_number:
                ContainerBlockNonLeafProcessor.__sdf(
                    parser_state, grab_bag, list_stack_index, list_token
                )

    @staticmethod
    def __sdf(
        parser_state: ParserState,
        grab_bag: ContainerGrabBag,
        list_stack_index: int,
        list_token: ListStartMarkdownToken,
    ) -> None:
        # do_add_leading_space = True
        # # for i in range(len(parser_state.block_copy)):
        # #     j = parser_state.block_copy[i]
        # #     if j.line_number == list_token.line_number and j.column_number == list_token.column_number:
        # #         break
        # # fg = parser_state.block_copy[i]
        # # fgg = fg.leading_spaces.count("\n") if fg.leading_spaces else 0
        # # list_tokeng = list_token.leading_spaces.count("\n")
        # # ww = (fgg == list_tokeng)
        # if do_add_leading_space:
        bq_count = grab_bag.block_quote_data.current_count
        last_active_block_quote_index = 0
        while bq_count > 0 and last_active_block_quote_index < len(
            parser_state.block_copy
        ):
            next_token = parser_state.block_copy[last_active_block_quote_index]
            assert next_token is not None
            if next_token.is_block_quote_start:
                bq_count -= 1
            last_active_block_quote_index += 1
        do_add_leading_space = list_stack_index < last_active_block_quote_index
        if do_add_leading_space:
            POGGER.debug(
                "__get_block_start_index_handle_blank_line>>list_token>>$",
                list_token,
            )
            list_token.add_leading_spaces("")
            POGGER.debug(
                "__get_block_start_index_handle_blank_line>>list_token>>$",
                list_token,
            )

    @staticmethod
    def __process_list_in_progress(
        parser_state: ParserState,
        index_indent: int,
        grab_bag: ContainerGrabBag,
    ) -> bool:
        did_process, ind = LeafBlockProcessorParagraph.check_for_list_in_process(
            parser_state
        )
        if did_process:
            assert (
                not grab_bag.container_tokens
            ), "Should not have any container tokens yet."
            POGGER.debug("clt>>list-in-progress")
            resultant_tokens = ListBlockProcessor.list_in_process(
                parser_state,
                ind,
                index_indent,
                grab_bag,
            )
            grab_bag.extend_container_tokens(resultant_tokens)

        return did_process

    @staticmethod
    def __get_list_start_index(
        parser_state: ParserState,
        position_marker: PositionMarker,
        is_ulist: bool,
        did_process: bool,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[bool, int]:
        """
        Note: This is one of the more heavily traffic functions in the
        parser.  Debugging should be uncommented only if needed.
        """
        new_position_marker = PositionMarker(
            position_marker.line_number, grab_bag.start_index, grab_bag.line_to_parse
        )

        POGGER.debug(
            "pre-list>>#$#$#$#",
            position_marker.index_number,
            position_marker.index_indent,
            position_marker.text_to_parse,
        )
        POGGER.debug(
            "pre-list>>#$#$#$#",
            new_position_marker.index_number,
            new_position_marker.index_indent,
            new_position_marker.text_to_parse,
        )
        new_list_index = -1
        if not did_process:
            assert (
                grab_bag.adj_ws is not None
            ), "If we have a list, we must have adjusted whitespace."
            assert (
                grab_bag.extracted_whitespace is not None
            ), "Extracted whitespace must be defined at this point."
            assert (
                grab_bag.removed_chars_at_start_of_line is not None
            ), "If we have a list, we must have removed characters."
            (
                did_process,
                new_list_index,
                new_line_to_parse,
                resultant_tokens,
            ) = ListBlockProcessor.handle_list_block(
                is_ulist,
                parser_state,
                new_position_marker,
                grab_bag,
            )
            # POGGER.debug_with_visible_whitespace("handle_list_block>$", resultant_tokens)
            if not grab_bag.requeue_line_info:
                assert (
                    new_line_to_parse is not None
                ), "If not requeuing, must have more line to parse."
                grab_bag.line_to_parse = new_line_to_parse
                grab_bag.extend_container_tokens(resultant_tokens)
        POGGER.debug(
            "post-ulist>>#$#$#$#",
            position_marker.index_number,
            position_marker.index_indent,
            position_marker.text_to_parse,
        )
        POGGER.debug(
            "post-ulist>>#$#$#$#",
            new_position_marker.index_number,
            new_position_marker.index_indent,
            new_position_marker.text_to_parse,
        )

        if grab_bag.requeue_line_info:
            POGGER.debug(
                ">>requeuing lines after looking for ordered list start. returning."
            )

        grab_bag.can_continue = not grab_bag.requeue_line_info
        return (
            did_process,
            new_list_index,
        )
