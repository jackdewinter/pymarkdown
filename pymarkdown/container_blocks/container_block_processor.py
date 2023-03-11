"""
Module to provide processing for the container blocks.
"""
from __future__ import annotations

import copy
import logging
from typing import TYPE_CHECKING, List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.container_blocks.container_block_leaf_processor import (
    ContainerBlockLeafProcessor,
)
from pymarkdown.container_blocks.container_block_non_leaf_processor import (
    ContainerBlockNonLeafProcessor,
)
from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.container_markdown_token import (
    BlockQuoteMarkdownToken,
    ListStartMarkdownToken,
)
from pymarkdown.extensions.pragma_token import PragmaExtension
from pymarkdown.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.requeue_line_info import RequeueLineInfo
from pymarkdown.tab_helper import TabHelper

if TYPE_CHECKING:  # pragma: no cover
    from pymarkdown.container_blocks.parse_block_pass_properties import (
        ParseBlockPassProperties,
    )

POGGER = ParserLogger(logging.getLogger(__name__))


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
        original_line: Optional[str] = None,
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
            original_line
            if original_line is not None
            else position_marker.text_to_parse,
            ContainerBlockProcessor.parse_line_for_container_blocks,
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
            ContainerBlockNonLeafProcessor.handle_non_leaf_block(
                parser_state,
                position_marker,
                grab_bag,
            )

        if (
            grab_bag.can_continue
            and not grab_bag.do_skip_containers_before_leaf_blocks
            and not grab_bag.did_blank
        ) or grab_bag.do_force_leaf_token_parse:
            ContainerBlockLeafProcessor.handle_leaf_tokens(
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
            leading_spaces = other_block_quote_token.calculate_next_bleading_space_part(
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
            leading_spaces = found_block_quote_token.calculate_next_bleading_space_part(
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
