"""
Module to provide processing for the container blocks.
"""
from __future__ import annotations

import copy
import logging
from typing import TYPE_CHECKING, List, Optional, Tuple, cast

from pymarkdown.block_quote_data import BlockQuoteData
from pymarkdown.block_quote_processor import BlockQuoteProcessor
from pymarkdown.container_block_leaf_processor import ContainerBlockLeafProcessor
from pymarkdown.container_grab_bag import ContainerGrabBag
from pymarkdown.container_indices import ContainerIndices
from pymarkdown.container_markdown_token import (
    BlockQuoteMarkdownToken,
    ListStartMarkdownToken,
)
from pymarkdown.extensions.pragma_token import PragmaExtension
from pymarkdown.leaf_block_processor_paragraph import LeafBlockProcessorParagraph
from pymarkdown.list_block_processor import ListBlockProcessor
from pymarkdown.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.requeue_line_info import RequeueLineInfo
from pymarkdown.stack_token import ListStackToken
from pymarkdown.tab_helper import TabHelper

if TYPE_CHECKING:  # pragma: no cover
    from pymarkdown.parse_block_pass_properties import ParseBlockPassProperties

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines
# pylint: disable=too-few-public-methods


class ContainerBlockProcessor:
    """
    Class to provide processing for the container blocks.
    """

    @staticmethod
    def __setup(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[PositionMarker, bool, bool]:

        POGGER.debug(">>")
        POGGER.debug(">>")
        if ContainerBlockProcessor.__look_for_pragmas(
            position_marker,
            grab_bag,
        ):
            return position_marker, True, False

        position_marker = ContainerBlockProcessor.__prepare_container_start_variables(
            parser_state,
            position_marker,
            grab_bag,
        )

        ContainerBlockProcessor.__prepare_container_start_variables2(
            parser_state, position_marker, grab_bag
        )

        is_not_in_root_list = not (
            parser_state.token_stack
            and len(parser_state.token_stack) >= 2
            and parser_state.token_stack[1].is_list
        )

        POGGER.debug(
            "position_marker>:$:$:",
            position_marker.index_number,
            position_marker.text_to_parse,
        )
        return (
            position_marker,
            False,
            is_not_in_root_list,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_line_for_container_blocks(
        parser_state: ParserState,
        position_marker: PositionMarker,
        ignore_link_definition_start: bool,
        parser_properties: ParseBlockPassProperties,
        container_start_bq_count: int,
        container_depth: int = 0,
        adjusted_block_index: Optional[int] = None,
        initial_block_quote_count: Optional[int] = None,
    ) -> Tuple[
        List[MarkdownToken],
        Optional[str],
        Optional[int],
        Optional[RequeueLineInfo],
        bool,
        bool,
    ]:
        """
        Parse the line, taking care to handle any container blocks before deciding
        whether or not to pass the (remaining parts of the) line to the leaf block
        processor.

        Note: This is one of the more heavily traffic functions in the
        parser.  Debugging should be uncommented only if needed.
        """

        grab_bag = ContainerGrabBag(
            parser_state,
            container_depth,
            initial_block_quote_count,
            adjusted_block_index,
            container_start_bq_count,
            parser_properties,
            ignore_link_definition_start,
            position_marker.text_to_parse,
        )
        (
            position_marker,
            did_find_pragma,
            is_not_in_root_list,
        ) = ContainerBlockProcessor.__setup(
            parser_state,
            position_marker,
            grab_bag,
        )
        if did_find_pragma:
            return [], None, None, None, False, False
        # POGGER.debug("position_marker.index_number>>$", position_marker.index_number)

        # POGGER.debug(">>parser_state.token_stack:$", parser_state.token_stack)
        # POGGER.debug(">>is_not_in_root_list=:$:", is_not_in_root_list)
        assert grab_bag.extracted_whitespace is not None
        if (
            not grab_bag.container_depth
            and len(grab_bag.extracted_whitespace) >= 4
            and is_not_in_root_list
        ):
            POGGER.debug("indent")
            ContainerBlockProcessor.__handle_indented_block_start(
                parser_state, position_marker, grab_bag
            )
        else:
            ContainerBlockProcessor.__handle_non_leaf_block(
                parser_state,
                position_marker,
                grab_bag,
            )

        if (
            grab_bag.can_continue
            and not grab_bag.do_skip_containers_before_leaf_blocks
            and not grab_bag.did_blank
        ) or grab_bag.do_force_leaf_token_parse:
            ContainerBlockProcessor.__handle_leaf_tokens(
                parser_state,
                position_marker,
                grab_bag,
            )

        return (
            grab_bag.container_tokens,
            grab_bag.line_to_parse,
            grab_bag.block_quote_data.current_count,
            grab_bag.requeue_line_info,
            grab_bag.did_blank,
            grab_bag.do_force_list_continuation,
        )
        # pylint: enable=too-many-arguments

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
            # POGGER.debug("parser_state.token_document=$", parser_state.token_document)
            last_container_stack_token = parser_state.token_stack[
                parser_state.find_last_container_on_stack()
            ]
            POGGER.debug("last_container_stack_token>>$", last_container_stack_token)
            if last_container_stack_token.is_block_quote:
                block_token = cast(
                    BlockQuoteMarkdownToken,
                    last_container_stack_token.matching_markdown_token,
                )
                assert block_token.leading_spaces is not None
                split_spaces = block_token.leading_spaces.split(
                    ParserHelper.newline_character
                )
                # POGGER.debug("split_spaces>>$", split_spaces)
                last_leading_space = split_spaces[-1]
                # POGGER.debug(
                #     "last_leading_space>:$:($)",
                #     last_leading_space,
                #     len(last_leading_space),
                # )
                ex_ws_index, _ = ParserHelper.extract_spaces(last_leading_space, 0)
                # POGGER.debug("ex_ws_index>:$", ex_ws_index)
                assert grab_bag.adj_ws is not None
                if (
                    len(grab_bag.adj_ws) >= 4
                    and grab_bag.indent_used_by_container
                    and grab_bag.indent_used_by_container == ex_ws_index
                ):
                    keep_processing = False
                    grab_bag.indent_already_processed = len(last_leading_space)
                    grab_bag.weird_adjusted_text = last_leading_space
                    # POGGER.debug(
                    #     "position_marker.text_to_parse>:$:($)",
                    #     position_marker.text_to_parse,
                    #     len(position_marker.text_to_parse),
                    # )
                    # POGGER.debug("used_pre_indent>:$:", used_pre_indent)
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
    def __handle_non_leaf_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        # POGGER.debug("ttp>>:$:<", position_marker.text_to_parse)
        # POGGER.debug("index_number>>:$:<", position_marker.index_number)
        # POGGER.debug("index_indent>>:$:<", position_marker.index_indent)
        ContainerBlockProcessor.__handle_pre_processed_indent(
            parser_state,
            position_marker,
            grab_bag,
        )
        # POGGER.debug("position_marker.index_number>>$", position_marker.index_number)
        # assert grab_bag.extracted_whitespace is not None
        if ContainerBlockProcessor.__look_for_override(
            parser_state,
            position_marker,
            grab_bag,
        ):
            ContainerBlockProcessor.__handle_normal_containers(
                parser_state,
                position_marker,
                grab_bag,
            )

    @staticmethod
    def __calculate_indent_used_by_container(
        parser_state: ParserState,
        position_marker: PositionMarker,
        leading_whitespace: Optional[str],
        grab_bag: ContainerGrabBag,
    ) -> Optional[str]:
        POGGER.debug("original_line_to_parse:$:", parser_state.original_line_to_parse)
        POGGER.debug("leading_whitespace:$:", leading_whitespace)
        POGGER.debug("text_to_parse=:$:", position_marker.text_to_parse)
        POGGER.debug("parser_state.token_stack=:$:", parser_state.token_stack)
        stack_search_index, current_indent = 1, 0
        assert parser_state.original_line_to_parse is not None
        while stack_search_index <= grab_bag.container_depth:
            if parser_state.token_stack[stack_search_index].is_block_quote:
                current_indent = parser_state.original_line_to_parse.find(">")
                assert current_indent != -1
                assert (
                    parser_state.original_line_to_parse[current_indent + 1]
                    == ParserHelper.space_character
                )
                current_indent += 1

                # TODO add tests with no space between `>` and next block
                assert (
                    current_indent < len(parser_state.original_line_to_parse)
                    and parser_state.original_line_to_parse[current_indent]
                    == ParserHelper.space_character
                )
                current_indent += 1
            else:
                assert parser_state.token_stack[stack_search_index].is_list
                list_token = cast(
                    ListStartMarkdownToken, parser_state.token_stack[stack_search_index]
                )
                delta = list_token.indent_level - current_indent
                POGGER.debug("delta=:$:", delta)
                current_indent += delta
            stack_search_index += 1
        assert stack_search_index > grab_bag.container_depth
        _, leading_whitespace = ParserHelper.extract_spaces(
            parser_state.original_line_to_parse, current_indent
        )
        POGGER.debug("leading_whitespace=:$:", leading_whitespace)
        grab_bag.indent_used_by_container = current_indent
        return leading_whitespace

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
        assert grab_bag.extracted_whitespace is not None
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
        list_token.add_leading_spaces(
            grab_bag.extracted_whitespace[:container_x_used_indent]
        )
        (
            grab_bag.do_skip_containers_before_leaf_blocks,
            grab_bag.did_indent_processing,
            grab_bag.have_pre_processed_indent,
            grab_bag.do_force_leaf_token_parse,
            grab_bag.indent_already_processed,
        ) = (True, True, True, True, container_x_used_indent)

    @staticmethod
    def __determine_leading_whitespace_preprocessing(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:

        assert grab_bag.extracted_whitespace is not None
        grab_bag.indent_used_by_container = 0
        if grab_bag.is_para_continue and not grab_bag.container_depth:
            ContainerBlockProcessor.__special_list_block_block(
                parser_state, position_marker, grab_bag
            )
        elif not grab_bag.is_para_continue:
            POGGER.debug(
                "position_marker.index_number:$:", position_marker.index_number
            )
            leading_whitespace: Optional[str] = grab_bag.extracted_whitespace
            if position_marker.index_number == -1 and grab_bag.container_depth:
                leading_whitespace = (
                    ContainerBlockProcessor.__calculate_indent_used_by_container(
                        parser_state, position_marker, leading_whitespace, grab_bag
                    )
                )
            assert leading_whitespace is not None
            if len(leading_whitespace) >= 4:
                POGGER.debug(">>leading_whitespace_processing")
                ContainerBlockProcessor.__handle_leading_whitespace(
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
    def __handle_pre_processed_indent(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        # POGGER.debug("normal")
        # POGGER.debug(
        #     "container_depth=$ == len(containers)=$ - 1",
        #     container_depth,
        #     len(parser_state.token_stack) - 1,
        # )
        # POGGER.debug("token-stack:$", parser_state.token_stack)
        # POGGER.debug("text_to_parse=:$:", position_marker.text_to_parse)
        # POGGER.debug("index_number=:$:", position_marker.index_number)
        # POGGER.debug("index_indent=:$:", position_marker.index_indent)
        assert grab_bag.extracted_whitespace is not None
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
            ContainerBlockProcessor.__handle_trailing_indent_with_block_quote(
                parser_state, grab_bag
            )
        elif need_leading_whitespace_processing:
            POGGER.debug(">>leading_whitespace_preprocessing")
            ContainerBlockProcessor.__determine_leading_whitespace_preprocessing(
                parser_state,
                position_marker,
                grab_bag,
            )

    @staticmethod
    def __handle_trailing_indent_with_block_quote(
        parser_state: ParserState,
        grab_bag: ContainerGrabBag,
    ) -> None:

        grab_bag.did_indent_processing = True
        assert grab_bag.extracted_whitespace is not None
        for stack_capture_index in range(1, len(parser_state.token_stack)):
            POGGER.debug(
                "$>stack:$:",
                stack_capture_index,
                parser_state.token_stack[stack_capture_index],
            )
            inner_token = parser_state.token_stack[
                stack_capture_index
            ].matching_markdown_token
            assert inner_token is not None
            POGGER.debug(
                "$>token:$:",
                stack_capture_index,
                inner_token,
            )
            if inner_token.is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, inner_token)
                assert block_quote_token.leading_spaces is not None
                split_spaces = block_quote_token.leading_spaces.split("\n")
                grab_bag.indent_already_processed = len(split_spaces[-1])
            else:
                assert inner_token.is_list_start
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
    def __handle_leading_whitespace_loop(
        parser_state: ParserState,
        i: int,
        remaining_whitespace: str,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[bool, int, str]:
        found_stack_index = 0
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
        inner_token = parser_state.token_stack[i].matching_markdown_token
        assert inner_token is not None
        if inner_token.is_block_quote_start:
            start_bq_index = remaining_whitespace.find(">")
            if start_bq_index < 0 or start_bq_index >= 4:
                # POGGER.debug("1-->$>start_bq_index:$:", i, start_bq_index)
                # POGGER.debug("$>remaining_whitespace:$:", i, remaining_whitespace)
                if len(remaining_whitespace) >= 4:
                    found_stack_index = i
                return True, found_stack_index, remaining_whitespace
            raise AssertionError()
        if not inner_token.is_list_start:
            # POGGER.debug("2-->")
            if len(remaining_whitespace) >= 4:
                found_stack_index = (
                    i + 1 if parser_state.token_stack[i].is_indented_code_block else i
                )
            return True, found_stack_index, remaining_whitespace
        assert inner_token.is_list_start
        list_token = cast(ListStartMarkdownToken, inner_token)
        assert grab_bag.indent_used_by_container >= 0
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
    def __handle_leading_whitespace(
        parser_state: ParserState,
        position_marker: PositionMarker,
        leading_whitespace: Optional[str],
        grab_bag: ContainerGrabBag,
    ) -> None:
        assert leading_whitespace is not None
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
            ) = ContainerBlockProcessor.__handle_leading_whitespace_loop(
                parser_state,
                i,
                remaining_whitespace,
                grab_bag,
            )
            # POGGER.debug(">do_break:$:", do_break)
            # POGGER.debug(">remaining_whitespace:$:", remaining_whitespace)
            if do_break:
                # POGGER.debug(">break!")
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
                # POGGER.debug(">ind2:$:", ind2)
                extra_indent = 1 if grab_bag.container_depth else 0
                list_token = cast(
                    ListStartMarkdownToken,
                    parser_state.token_stack[ind].matching_markdown_token,
                )
                list_token.add_leading_spaces(
                    position_marker.text_to_parse[
                        block_quote_end_index : grab_bag.indent_already_processed
                        + extra_indent
                    ]
                )

            # POGGER.debug(">text_to_parse:$:", position_marker.text_to_parse)
            # POGGER.debug(
            #     ">text_to_parse[grab_bag.indent_already_processed:]:$:",
            #     position_marker.text_to_parse[grab_bag.indent_already_processed:],
            # )

    @staticmethod
    def __handle_indented_block_start(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        (
            grab_bag.can_continue,
            grab_bag.line_to_parse,
            grab_bag.start_index,
            grab_bag.text_removed_by_container,
            grab_bag.removed_chars_at_start_of_line,
        ) = (
            True,
            position_marker.text_to_parse,
            position_marker.index_number,
            "",
            0,
        )
        POGGER.debug("parser_state.token_stack>>$", parser_state.token_stack)
        is_paragraph_continuation = (
            parser_state.token_stack and parser_state.token_stack[-1].is_paragraph
        )
        list_index = parser_state.find_last_list_block_on_stack()
        block_index = parser_state.find_last_block_quote_on_stack()
        POGGER.debug("list_index>>$", list_index)
        POGGER.debug("block_index>>$", block_index)
        if is_paragraph_continuation and block_index > list_index:
            grab_bag.was_paragraph_continuation = True
        # if is_paragraph_continuation and block_index < list_index:
        #     grab_bag.was_other_paragraph_continuation = True
        if (
            not is_paragraph_continuation
            and parser_state.token_stack
            and len(parser_state.token_stack) >= 2
            and parser_state.token_stack[1].is_block_quote
        ):
            x_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                include_lists=True,
                include_block_quotes=True,
            )
            # POGGER.debug("x_tokens=:$:", x_tokens)
            grab_bag.extend_container_tokens(x_tokens)

    @staticmethod
    def __handle_normal_containers(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        (
            did_process,
            avoid_block_starts,
        ) = ContainerBlockProcessor.__check_for_container_starts(
            parser_state,
            position_marker,
            grab_bag,
        )

        if grab_bag.requeue_line_info or grab_bag.did_blank:
            grab_bag.can_continue = False
            return

        nested_force_list_continuation = ContainerBlockProcessor.__handle_nested_blocks(
            parser_state,
            position_marker,
            did_process,
            avoid_block_starts,
            grab_bag,
        )
        if grab_bag.do_force_list_continuation:
            POGGER.debug(
                "nested_force_list_continuation=$", nested_force_list_continuation
            )
            assert not nested_force_list_continuation
        if grab_bag.can_continue:
            did_process = ContainerBlockProcessor.__handle_block_continuations(
                parser_state,
                position_marker,
                did_process,
                grab_bag,
            )
        return

    @staticmethod
    def __prepare_container_start_variables(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> PositionMarker:
        # POGGER.debug("Stack Depth:$:", parser_state.original_stack_depth)
        # POGGER.debug("Document Depth:$:", parser_state.original_document_depth)
        if grab_bag.container_depth:
            return position_marker

        if ParserHelper.tab_character in position_marker.text_to_parse:
            detabified_line = TabHelper.detabify_string(position_marker.text_to_parse)
            POGGER.debug("Before tab replacement:$:", position_marker.text_to_parse)
            POGGER.debug("After tab replacement :$:", detabified_line)
            position_marker = PositionMarker(
                position_marker.line_number,
                position_marker.index_number,
                detabified_line,
                position_marker.index_indent,
            )

        parser_state.mark_start_information(position_marker)

        parser_state.copy_of_token_stack = []
        parser_state.copy_of_token_stack.extend(parser_state.token_stack)

        parser_state.block_copy = [
            copy.deepcopy(i.matching_markdown_token)
            for i in parser_state.token_stack
            if not i.is_document
        ]

        return position_marker

    @staticmethod
    def __prepare_container_start_variables2(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        # Debug to be used for block quotes if needed.
        # POGGER.debug(
        #    "Last Block Quote:$:",
        #    parser_state.last_block_quote_stack_token,
        # )
        # POGGER.debug(
        #    "Last Block Quote:$:",
        #    parser_state.last_block_quote_markdown_token_index,
        # )
        # POGGER.debug(
        #    "Last Block Quote:$:", parser_state.copy_of_last_block_quote_markdown_token
        # )

        (
            new_start_index,
            grab_bag.extracted_whitespace,
        ) = ParserHelper.extract_spaces(position_marker.text_to_parse, 0)
        assert new_start_index is not None
        grab_bag.start_index = new_start_index
        ContainerBlockProcessor.__calculate_for_container_blocks(
            parser_state,
            grab_bag,
        )

    @staticmethod
    def __handle_block_continuations(
        parser_state: ParserState,
        position_marker: PositionMarker,
        did_process: bool,
        grab_bag: ContainerGrabBag,
    ) -> bool:
        if not did_process:
            did_process = ContainerBlockProcessor.__process_list_in_progress(
                parser_state,
                grab_bag,
            )
            if not grab_bag.requeue_line_info:
                ContainerBlockProcessor.__process_lazy_lines(
                    parser_state,
                    position_marker,
                    grab_bag,
                )
        else:
            is_paragraph_continuation = (
                parser_state.token_stack and parser_state.token_stack[-1].is_paragraph
            )
            list_index = parser_state.find_last_list_block_on_stack()
            block_index = parser_state.find_last_block_quote_on_stack()
            # POGGER.debug("is_paragraph_continuation($) and block_index($) > list_index($)",
            #     is_paragraph_continuation, block_index, list_index)
            if is_paragraph_continuation and block_index > list_index:
                grab_bag.was_paragraph_continuation = True

        grab_bag.can_continue = not grab_bag.requeue_line_info
        return did_process

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
        ) = ContainerBlockProcessor.__get_block_start_index(
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
            ) = ContainerBlockProcessor.__get_list_start_index(
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
            ) = ContainerBlockProcessor.__get_list_start_index(
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

        # POGGER.debug("was_container_start>>$", was_container_start)

        grab_bag.last_list_start_index = 0
        if grab_bag.end_container_indices.block_index != -1:
            assert grab_bag.last_block_quote_index in (
                grab_bag.end_container_indices.block_index - 1,
                grab_bag.end_container_indices.block_index,
            )
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
            ) = ContainerBlockProcessor.__handle_nested_container_blocks(
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
    def __handle_leaf_tokens(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        assert parser_state.original_line_to_parse is not None
        calculated_indent = len(parser_state.original_line_to_parse) - len(
            grab_bag.line_to_parse
        )
        # POGGER.debug(">>indent>>$", calculated_indent)

        assert not (
            grab_bag.indent_used_by_list
            and ">" in grab_bag.indent_used_by_list
            and parser_state.token_stack[-1].is_paragraph
            and parser_state.token_stack[-2].is_block_quote
        )

        # POGGER.debug("ttp>>:$:<", position_marker.text_to_parse)
        # POGGER.debug("index_number>>:$:<", position_marker.index_number)
        # POGGER.debug("index_indent>>:$:<", position_marker.index_indent)
        newer_position_marker = PositionMarker(
            position_marker.line_number,
            grab_bag.start_index,
            grab_bag.line_to_parse,
            index_indent=calculated_indent,
        )
        # POGGER.debug("ttp>>:$:<", newer_position_marker.text_to_parse)
        # POGGER.debug("index_number>>:$:<", newer_position_marker.index_number)
        # POGGER.debug("index_indent>>:$:<", newer_position_marker.index_indent)
        parser_state.mark_for_leaf_processing(grab_bag.container_tokens)

        ContainerBlockLeafProcessor.process_leaf_tokens(
            parser_state,
            newer_position_marker,
            grab_bag,
        )
        parser_state.clear_after_leaf_processing()

        grab_bag.extend_container_tokens_with_leaf_tokens()

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
        assert grab_bag.container_start_bq_count is not None
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
        # POGGER.debug("did_process>>$", did_process)

        if grab_bag.requeue_line_info:
            POGGER.debug(">>requeuing lines after looking for block start. returning.")

        if grab_bag.did_blank:
            POGGER.debug(">>already handled blank line. returning.")
            grab_bag.extend_container_tokens_with_leaf_tokens()

        grab_bag.can_continue = (
            not grab_bag.requeue_line_info and not grab_bag.did_blank
        )
        return (
            did_process,
            block_index,
            avoid_block_starts,
        )

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
            assert grab_bag.adj_ws is not None
            assert grab_bag.extracted_whitespace is not None
            assert grab_bag.removed_chars_at_start_of_line is not None
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
                assert new_line_to_parse is not None
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

    @staticmethod
    def __calculate_for_container_blocks(
        parser_state: ParserState,
        grab_bag: ContainerGrabBag,
    ) -> None:
        """
        Perform some calculations that will be needed for parsing the container blocks.
        """
        grab_bag.current_container_blocks = [
            ind for ind in parser_state.token_stack if ind.is_list
        ]
        grab_bag.block_quote_data = BlockQuoteData(
            0
            if grab_bag.initial_block_quote_count is None
            else grab_bag.initial_block_quote_count,
            parser_state.count_of_block_quotes_on_stack(),
        )

        ContainerBlockProcessor.__calculate_adjusted_whitespace(
            parser_state,
            grab_bag,
        )

    @staticmethod
    def __look_back_in_document_for_block_quote(
        parser_state: ParserState, token_index: int
    ) -> Optional[BlockQuoteMarkdownToken]:

        # TODO Look back on stack instead?
        other_block_quote_token, other_token_index = None, token_index
        while other_token_index >= 0:
            if parser_state.token_document[other_token_index].is_block_quote_start:
                block_quote_token = cast(
                    BlockQuoteMarkdownToken,
                    parser_state.token_document[other_token_index],
                )
                if not ContainerBlockProcessor.__does_block_quote_token_have_end(
                    parser_state, block_quote_token
                ):
                    other_block_quote_token = block_quote_token
                    break
            other_token_index -= 1
        POGGER.debug_with_visible_whitespace(
            "PLFCB>>other_block_quote_token>>$",
            other_block_quote_token,
        )
        return other_block_quote_token

    @staticmethod
    def __calculate_adjusted_whitespace_kludge_without_found(
        parser_state: ParserState, token_index: int, grab_bag: ContainerGrabBag
    ) -> Tuple[bool, int]:
        other_block_quote_token = (
            ContainerBlockProcessor.__look_back_in_document_for_block_quote(
                parser_state, token_index
            )
        )

        # Check to see if out first block token is the same as our first.
        # if not, do not use it as a base.
        #
        # Note; may need to be tweaked for extra levels.
        if not grab_bag.container_depth and other_block_quote_token:
            POGGER.debug(
                "parser_state.token_stack[1]>>:$:", parser_state.token_stack[1]
            )
            if (
                parser_state.token_stack[1].matching_markdown_token
                != other_block_quote_token
            ):
                other_block_quote_token = None

        if other_block_quote_token:
            POGGER.debug("PLFCB>>other_block_quote_token>>:$:", other_block_quote_token)
            POGGER.debug(
                "PLFCB>>other_block_quote_token.leading_text_index>>:$:",
                other_block_quote_token.leading_text_index,
            )
            leading_spaces = other_block_quote_token.calculate_next_leading_space_part(
                increment_index=False, delta=-1
            )
            POGGER.debug("PLFCB>>leading_spaces>>:$:", leading_spaces)
            POGGER.debug("PLFCB>>other_block_quote_token>>:$:", other_block_quote_token)
            POGGER.debug(
                "PLFCB>>other_block_quote_token.leading_text_index>>:$:",
                other_block_quote_token.leading_text_index,
            )
            force_reline = True
            old_start_index = len(leading_spaces)
        else:
            force_reline = False
            list_token = cast(
                ListStartMarkdownToken, parser_state.token_document[token_index]
            )
            old_start_index = list_token.indent_level
        return force_reline, old_start_index

    @staticmethod
    def __does_block_quote_token_have_end(
        parser_state: ParserState,
        found_block_quote_token: Optional[BlockQuoteMarkdownToken],
    ) -> bool:
        assert found_block_quote_token
        POGGER.debug(
            "PLFCB>>found_block_quote_token>>:$:",
            ParserHelper.make_value_visible(found_block_quote_token),
        )
        found_token_index = parser_state.token_document.index(found_block_quote_token)
        POGGER.debug("PLFCB>>found_token_index>>:$:", found_token_index)
        found_token_index += 1
        while found_token_index < len(parser_state.token_document):
            if parser_state.token_document[found_token_index].is_end_token:
                end_token = cast(
                    EndMarkdownToken, parser_state.token_document[found_token_index]
                )
                if end_token.start_markdown_token == found_block_quote_token:
                    break
            found_token_index += 1
        POGGER.debug(
            "PLFCB>>found_token_index>>:$:max:$",
            found_token_index,
            len(parser_state.token_document),
        )
        return found_token_index < len(parser_state.token_document)

    @staticmethod
    def __calculate_adjusted_whitespace_kludge(
        parser_state: ParserState,
        token_index: int,
        found_block_quote_token: Optional[BlockQuoteMarkdownToken],
        grab_bag: ContainerGrabBag,
    ) -> None:

        assert grab_bag.extracted_whitespace is not None
        previous_ws_len = 0
        force_reline, ws_len = (
            False,
            TabHelper.calculate_length(grab_bag.extracted_whitespace) + previous_ws_len,
        )
        if (
            found_block_quote_token
            and ContainerBlockProcessor.__does_block_quote_token_have_end(
                parser_state, found_block_quote_token
            )
        ):
            found_block_quote_token = None
        if found_block_quote_token:
            POGGER.debug(
                "PLFCB>>found_block_quote_token>>:$:",
                ParserHelper.make_value_visible(found_block_quote_token),
            )
            leading_spaces = found_block_quote_token.calculate_next_leading_space_part(
                increment_index=False, delta=-1, allow_overflow=True
            )
            POGGER.debug("PLFCB>>leading_spaces>>:$:", leading_spaces)
            old_start_index = len(leading_spaces)
        else:
            (
                force_reline,
                old_start_index,
            ) = ContainerBlockProcessor.__calculate_adjusted_whitespace_kludge_without_found(
                parser_state, token_index, grab_bag
            )
        POGGER.debug(
            "old_start_index>>$>>ws_len>>$>>force_reline>>$",
            old_start_index,
            ws_len,
            force_reline,
        )
        if force_reline or ws_len >= old_start_index:
            POGGER.debug("RELINE:$:", grab_bag.line_to_parse)
            grab_bag.adj_ws = grab_bag.extracted_whitespace[old_start_index:]
            POGGER.debug(
                "adj_ws:$: old_start_index:$:", grab_bag.adj_ws, old_start_index
            )

    @staticmethod
    def __look_for_any_list_start(
        parser_state: ParserState,
    ) -> Tuple[int, Optional[BlockQuoteMarkdownToken]]:
        found_block_quote_token: Optional[BlockQuoteMarkdownToken] = None
        token_index = len(parser_state.token_document) - 1
        while token_index >= 0 and not (
            parser_state.token_document[token_index].is_any_list_token
        ):
            if (
                not found_block_quote_token
                and parser_state.token_document[token_index].is_block_quote_start
            ):
                found_block_quote_token = cast(
                    BlockQuoteMarkdownToken,
                    parser_state.token_document[token_index],
                )
            token_index -= 1
        POGGER.debug(
            "PLFCB>>Started list-last token>>$",
            parser_state.token_document[token_index],
        )

        POGGER.debug(
            "CAW>>found_block_quote_token>>:$:",
            ParserHelper.make_value_visible(found_block_quote_token),
        )
        if found_block_quote_token:
            POGGER.debug(
                "PLFCB>>leading_text_index>>$",
                found_block_quote_token.leading_text_index,
            )
        assert token_index >= 0
        return token_index, found_block_quote_token

    @staticmethod
    def __calculate_adjusted_whitespace(
        parser_state: ParserState,
        grab_bag: ContainerGrabBag,
    ) -> None:
        """
        Based on the last container on the stack, determine what the adjusted whitespace is.
        """

        grab_bag.adj_ws = grab_bag.extracted_whitespace
        assert grab_bag.adj_ws is not None

        last_block_stack_index = parser_state.find_last_list_block_on_stack()
        if last_block_stack_index <= 0:
            assert not grab_bag.current_container_blocks
            POGGER.debug("PLFCB>>No Started lists")
            if grab_bag.adjusted_block_index is None:
                POGGER.debug("PLFCB>>No Started Block Quote")
            else:
                POGGER.debug("PLFCB>>Started Block Quote")
                assert grab_bag.extracted_whitespace is not None
                grab_bag.adj_ws = grab_bag.extracted_whitespace[
                    grab_bag.adjusted_block_index :
                ]
        else:
            assert grab_bag.current_container_blocks
            POGGER.debug(
                "PLFCB>>Started list-last stack>>$",
                parser_state.token_stack,
            )
            POGGER.debug(
                "PLFCB>>Started list-last stack>>$",
                parser_state.token_stack[last_block_stack_index],
            )

            (
                token_index,
                found_block_quote_token,
            ) = ContainerBlockProcessor.__look_for_any_list_start(parser_state)

            assert grab_bag.adj_ws is not None
            ContainerBlockProcessor.__calculate_adjusted_whitespace_kludge(
                parser_state,
                token_index,
                found_block_quote_token,
                grab_bag,
            )
            assert grab_bag.adj_ws is not None

    @staticmethod
    def __handle_nested_container_blocks(
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
                ContainerBlockProcessor.__get_nested_container_starts(
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
            ) = ContainerBlockProcessor.__check_for_nested_list_start(
                parser_state,
                nested_container_starts,
                grab_bag,
            )

            assert grab_bag.is_leaf_tokens_empty()
            adjusted_text_to_parse = ContainerBlockProcessor.__do_nested_cleanup(
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
            ) = ContainerBlockProcessor.__check_for_next_container(
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
                ) = ContainerBlockProcessor.__calculate_initial_list_adjustments(
                    parser_state,
                    grab_bag.adj_line_to_parse,
                    grab_bag.end_container_indices,
                )
                already_adjusted = ContainerBlockProcessor.__adjust_line_2(
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
            ) = ContainerBlockProcessor.__look_for_container_blocks(
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

        nested_ulist_start, _, _, _ = ListBlockProcessor.is_ulist_start(
            parser_state, line_to_parse, after_ws_index, ex_whitespace, False
        )
        nested_olist_start, _, _, _ = ListBlockProcessor.is_olist_start(
            parser_state, line_to_parse, after_ws_index, ex_whitespace, False
        )
        nested_block_start = (
            False
            if avoid_block_starts
            else BlockQuoteProcessor.is_block_quote_start(
                line_to_parse, after_ws_index, ex_whitespace
            )
        )

        POGGER.debug("check next container_start>stack>>$", parser_state.token_stack)

        return ContainerIndices(
            nested_ulist_start, nested_olist_start, nested_block_start
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
                nested_removed_text = (
                    ContainerBlockProcessor.__calculate_nested_removed_text_block_quote(
                        parser_state, block_quote_token, grab_bag
                    )
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
                assert block_quote_token.leading_spaces is not None
                split_spaces = block_quote_token.leading_spaces.split(
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
        assert block_quote_token.leading_spaces is not None
        split_spaces = block_quote_token.leading_spaces.split(
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
        ) = ContainerBlockProcessor.parse_line_for_container_blocks(
            parser_state,
            position_marker,
            False,
            grab_bag.parser_properties,
            grab_bag.block_quote_data.current_count,
            container_depth=new_container_depth,
            adjusted_block_index=adj_block,
            initial_block_quote_count=grab_bag.block_quote_data.current_count,
        )
        assert (
            not grab_bag.requeue_line_info
            or not grab_bag.requeue_line_info.lines_to_requeue
        )
        assert adjusted_text_to_parse is not None

        POGGER.debug("\nRECURSED\n\n")

        # POGGER.debug("previous_document_length=$", previous_document_length)
        nested_removed_text = ContainerBlockProcessor.__calculate_nested_removed_text(
            parser_state, previous_document_length, grab_bag
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
    def __process_list_in_progress(
        parser_state: ParserState,
        grab_bag: ContainerGrabBag,
    ) -> bool:

        did_process, ind = LeafBlockProcessorParagraph.check_for_list_in_process(
            parser_state
        )
        if did_process:
            assert not grab_bag.container_tokens
            POGGER.debug("clt>>list-in-progress")
            resultant_tokens = ListBlockProcessor.list_in_process(
                parser_state,
                ind,
                grab_bag,
            )
            grab_bag.extend_container_tokens(resultant_tokens)

        return did_process

    @staticmethod
    def __process_lazy_lines(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:

        assert grab_bag.is_leaf_tokens_empty()
        POGGER.debug("clt>>lazy-check")

        after_ws_index, ex_whitespace = ParserHelper.extract_spaces(
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
        )
        grab_bag.extend_container_tokens(lazy_tokens)

    @staticmethod
    def __look_for_pragmas(
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> bool:

        _, pragma_whitespace = ParserHelper.extract_spaces(
            position_marker.text_to_parse, 0
        )
        return (
            PragmaExtension.look_for_pragmas(
                position_marker,
                position_marker.text_to_parse,
                grab_bag.container_depth,
                pragma_whitespace,
                grab_bag.parser_properties,
            )
            if grab_bag.parser_properties.is_pragmas_enabled
            else False
        )


# pylint: enable=too-few-public-methods
