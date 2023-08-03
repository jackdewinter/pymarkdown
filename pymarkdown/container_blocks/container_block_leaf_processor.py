"""
Module to provide processing for the handling of leaf elements within container blocks.
"""
from __future__ import annotations

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.leaf_blocks.atx_leaf_block_processor import AtxLeafBlockProcessor
from pymarkdown.leaf_blocks.fenced_leaf_block_processor import FencedLeafBlockProcessor
from pymarkdown.leaf_blocks.indented_leaf_block_processor import (
    IndentedLeafBlockProcessor,
)
from pymarkdown.leaf_blocks.leaf_block_processor import LeafBlockProcessor
from pymarkdown.leaf_blocks.leaf_block_processor_paragraph import (
    LeafBlockProcessorParagraph,
)
from pymarkdown.leaf_blocks.setext_leaf_block_processor import SetextLeafBlockProcessor
from pymarkdown.leaf_blocks.thematic_leaf_block_processor import (
    ThematicLeafBlockProcessor,
)
from pymarkdown.links.link_reference_definition_helper import (
    LinkReferenceDefinitionHelper,
)
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import ListStackToken

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-few-public-methods


class ContainerBlockLeafProcessor:
    """
    Class to provide processing for the handling of leaf elements within container blocks.
    """

    @staticmethod
    def handle_leaf_tokens(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        """
        Handle the handoff between processing containers and the leaf tokens.
        """
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

        POGGER.debug("ttp>>:$:<", position_marker.text_to_parse)
        POGGER.debug("index_number>>:$:<", position_marker.index_number)
        POGGER.debug("index_indent>>:$:<", position_marker.index_indent)
        newer_position_marker = PositionMarker(
            position_marker.line_number,
            grab_bag.start_index,
            grab_bag.line_to_parse,
            index_indent=calculated_indent,
        )
        POGGER.debug("ttp>>:$:<", newer_position_marker.text_to_parse)
        POGGER.debug("index_number>>:$:<", newer_position_marker.index_number)
        POGGER.debug("index_indent>>:$:<", newer_position_marker.index_indent)
        parser_state.mark_for_leaf_processing(grab_bag.container_tokens)

        ContainerBlockLeafProcessor.__process_leaf_tokens(
            parser_state,
            newer_position_marker,
            grab_bag,
        )
        parser_state.clear_after_leaf_processing()

        grab_bag.extend_container_tokens_with_leaf_tokens()

    @staticmethod
    def __process_leaf_tokens(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        """
        Main entry point from the ContainerBlockProcessor for processing leaf tokens.
        """
        assert grab_bag.is_leaf_tokens_empty()
        POGGER.debug("parsing leaf>>")
        position_marker = PositionMarker(
            xposition_marker.line_number,
            0,
            xposition_marker.text_to_parse,
            index_indent=xposition_marker.index_indent,
        )
        # POGGER.debug("position_marker.text>>:$:<<", position_marker.text_to_parse)
        # POGGER.debug("position_marker.index>>:$:<<", position_marker.index_number)

        (
            new_index_number,
            extracted_leaf_whitespace,
        ) = ParserHelper.extract_spaces(position_marker.text_to_parse, 0)
        assert new_index_number is not None

        total_ws = new_index_number + position_marker.index_indent

        last_block_index = parser_state.find_last_block_quote_on_stack()
        last_list_index = parser_state.find_last_list_block_on_stack()

        ContainerBlockLeafProcessor.__handle_special_block_quote_reduction(
            parser_state,
            last_block_index,
            last_list_index,
            grab_bag,
        )
        if grab_bag.requeue_line_info:
            POGGER.debug("requeuing after __handle_special_block_quote_reduction")
            assert grab_bag.is_leaf_tokens_empty()
            return

        orig_text_removed_by_container = grab_bag.text_removed_by_container

        ContainerBlockLeafProcessor.__adjust_for_inner_list_container(
            parser_state,
            last_block_index,
            last_list_index,
            position_marker.line_number,
        )

        # POGGER.debug("position_marker.text>>:$:<<", position_marker.text_to_parse)
        # POGGER.debug("position_marker.index>>:$:<<", position_marker.index_number)
        (
            removed_leading_space,
            actual_removed_leading_space,
            position_marker,
        ) = ContainerBlockLeafProcessor.__adjust_for_list_container(
            parser_state,
            position_marker,
            last_block_index,
            last_list_index,
            extracted_leaf_whitespace,
            grab_bag,
        )

        # POGGER.debug("position_marker.text>>:$:<<", position_marker.text_to_parse)
        # POGGER.debug("position_marker.index>>:$:<<", position_marker.index_number)
        if (
            grab_bag.is_leaf_tokens_empty()
            and not grab_bag.do_skip_containers_before_leaf_blocks
            and not removed_leading_space
        ):
            position_marker = (
                ContainerBlockLeafProcessor.__adjust_containers_before_leaf_blocks(
                    parser_state,
                    position_marker,
                    last_block_index,
                    total_ws,
                    actual_removed_leading_space,
                    grab_bag,
                )
            )
            # POGGER.debug("position_marker.text>>:$:<<", position_marker.text_to_parse)
            # POGGER.debug("position_marker.index>>:$:<<", position_marker.index_number)

        ContainerBlockLeafProcessor.__parse_line_for_leaf_blocks(
            parser_state,
            position_marker,
            grab_bag,
        )

        ContainerBlockLeafProcessor.__post_leaf_block_adjustment(
            parser_state,
            orig_text_removed_by_container,
            position_marker.line_number,
        )

    @staticmethod
    def __parse_line_for_leaf_blocks(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        """
        Parse the contents of a line for a leaf block.

        Note: This is one of the more heavily traffic functions in the
        parser.  Debugging should be uncommented only if needed.
        """
        POGGER.debug("parsing leaf tokens")
        POGGER.debug("Leaf Line:$:", position_marker.text_to_parse)
        POGGER.debug("original_line:$:", grab_bag.original_line)
        detabified_original_line = TabHelper.detabify_string(grab_bag.original_line)
        detabified_original_start_index = detabified_original_line.find(
            position_marker.text_to_parse
        )
        assert detabified_original_start_index != -1
        POGGER.debug(
            "detabified_original_start_index:$:", detabified_original_start_index
        )

        (
            outer_processed,
            leaf_block_position_marker,
            leaf_token_whitespace,
        ) = ContainerBlockLeafProcessor.__handle_block_leaf_tokens(
            parser_state, position_marker, detabified_original_start_index, grab_bag
        )

        if not outer_processed:
            new_tokens = (
                AtxLeafBlockProcessor.parse_atx_headings(
                    parser_state,
                    leaf_block_position_marker,
                    leaf_token_whitespace,
                    grab_bag.block_quote_data,
                    grab_bag.original_line,
                )
                or IndentedLeafBlockProcessor.parse_indented_code_block(
                    parser_state,
                    leaf_block_position_marker,
                    leaf_token_whitespace,
                    grab_bag.removed_chars_at_start_of_line,
                    grab_bag.last_block_quote_index,
                    grab_bag.last_list_start_index,
                    grab_bag.original_line,
                )
                or SetextLeafBlockProcessor.parse_setext_headings(
                    parser_state,
                    leaf_block_position_marker,
                    leaf_token_whitespace,
                    grab_bag.block_quote_data,
                    grab_bag.original_line,
                )
                or ThematicLeafBlockProcessor.parse_thematic_break(
                    parser_state,
                    leaf_block_position_marker,
                    leaf_token_whitespace,
                    grab_bag.block_quote_data,
                    grab_bag.original_line,
                )
                or LeafBlockProcessorParagraph.parse_paragraph(
                    parser_state,
                    leaf_block_position_marker,
                    leaf_token_whitespace,
                    grab_bag.block_quote_data,
                    grab_bag.text_removed_by_container,
                    grab_bag.original_line,
                )
            )
            # POGGER.debug(">>leaf--adding>>$", new_tokens)
            grab_bag.extend_leaf_tokens(new_tokens)

    @staticmethod
    def __handle_block_leaf_tokens(
        parser_state: ParserState,
        incoming_position_marker: PositionMarker,
        detabified_original_start_index: int,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[bool, PositionMarker, Optional[str]]:
        POGGER.debug(
            "line>>$>>index>>$>>",
            incoming_position_marker.text_to_parse,
            incoming_position_marker.index_number,
        )
        remaining_line_to_parse = incoming_position_marker.text_to_parse[
            incoming_position_marker.index_number :
        ]
        (new_index_number, leaf_token_whitespace) = ParserHelper.extract_spaces(
            incoming_position_marker.text_to_parse,
            incoming_position_marker.index_number,
        )
        assert new_index_number is not None
        POGGER.debug(">>leaf_token_whitespace>>:$:<<", leaf_token_whitespace)

        position_marker = PositionMarker(
            incoming_position_marker.line_number,
            new_index_number,
            incoming_position_marker.text_to_parse,
            index_indent=incoming_position_marker.index_indent,
        )

        pre_tokens = LeafBlockProcessor.close_indented_block_if_indent_not_there(
            parser_state, leaf_token_whitespace
        )

        new_tokens: List[MarkdownToken] = []
        outer_processed = FencedLeafBlockProcessor.handle_fenced_code_block(
            parser_state,
            position_marker,
            leaf_token_whitespace,
            new_tokens,
            grab_bag.original_line,
            detabified_original_start_index,
            grab_bag.block_quote_data,
        )

        ignore_lrd_start = (
            grab_bag.do_ignore_link_definition_start
            or parser_state.token_stack[-1].is_html_block
        )

        (
            outer_processed,
            grab_bag.requeue_line_info,
        ) = LinkReferenceDefinitionHelper.handle_link_reference_definition_leaf_block(
            parser_state,
            outer_processed,
            position_marker,
            leaf_token_whitespace,
            remaining_line_to_parse,
            ignore_lrd_start,
            pre_tokens,
            grab_bag.original_line,
        )

        outer_processed = LeafBlockProcessor.handle_html_block(
            parser_state,
            position_marker,
            outer_processed,
            leaf_token_whitespace,
            new_tokens,
            grab_bag,
        )
        grab_bag.extend_leaf_tokens(pre_tokens)
        grab_bag.extend_leaf_tokens(new_tokens)
        return (
            outer_processed,
            position_marker,
            leaf_token_whitespace,
        )

    @staticmethod
    def __handle_special_block_quote_reduction(
        parser_state: ParserState,
        last_block_index: int,
        last_list_index: int,
        grab_bag: ContainerGrabBag,
    ) -> None:
        assert grab_bag.is_leaf_tokens_empty()
        real_stack_count = parser_state.count_of_block_quotes_on_stack()
        POGGER.debug(
            "stack_count>>:$:($)<",
            grab_bag.block_quote_data.stack_count,
            real_stack_count,
        )
        POGGER.debug("??? special_block_quote_reduction")
        if (
            grab_bag.block_quote_data.current_count < real_stack_count
            and not grab_bag.was_paragraph_continuation
            and last_block_index > last_list_index
            and not last_list_index
        ):
            POGGER.debug("yes special_block_quote_reduction")
            stack_delta = (
                grab_bag.block_quote_data.stack_count
                - grab_bag.block_quote_data.current_count
            )
            if parser_state.token_stack[-1].was_link_definition_started:
                stack_delta += 1
            (
                close_tokens,
                grab_bag.requeue_line_info,
            ) = parser_state.close_open_blocks_fn(
                parser_state,
                include_block_quotes=True,
                was_forced=True,
                requeue_reset=True,
                caller_can_handle_requeue=True,
                until_this_index=len(parser_state.token_stack) - stack_delta,
            )
            grab_bag.extend_leaf_tokens(close_tokens)
            if not grab_bag.requeue_line_info:
                POGGER.debug("parser_state.token_stack>>$", parser_state.token_stack)
                POGGER.debug(
                    "parser_state.token_document>>$", parser_state.token_document
                )
                grab_bag.block_quote_data = BlockQuoteData(
                    grab_bag.block_quote_data.current_count,
                    grab_bag.block_quote_data.stack_count - stack_delta,
                )

    @staticmethod
    def __adjust_for_inner_list_container(
        parser_state: ParserState,
        last_block_index: int,
        last_list_index: int,
        current_line_number: int,
    ) -> None:
        POGGER.debug("??? adjust_for_inner_list_container")
        if last_block_index > 0 and 0 < last_list_index < last_block_index:
            POGGER.debug("yes adjust_for_inner_list_container")
            list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[last_list_index].matching_markdown_token,
            )
            if list_token.line_number != current_line_number:
                POGGER.debug("plt-a>>last_block_token>>$", list_token)
                list_token.add_leading_spaces("")
                POGGER.debug(
                    "plt-a>>last_block_token>>$",
                    list_token,
                )
        else:
            POGGER.debug("not adjust_for_inner_list_container")

    @staticmethod
    def __adjust_for_list_container_after_block_quote(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        last_list_index: int,
        extracted_leaf_whitespace: str,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[Optional[ListStartMarkdownToken], Optional[str], Optional[str]]:
        list_token: Optional[ListStartMarkdownToken] = None
        POGGER.debug("yes adjust_for_list_container")
        removed_leading_space = None
        actual_removed_leading_space = None

        found_list_token = ContainerBlockLeafProcessor.__adjust_for_list_container_find(
            parser_state, xposition_marker
        )
        if not found_list_token:
            list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[last_list_index].matching_markdown_token,
            )
            calc_indent_level = list_token.indent_level
            if grab_bag.text_removed_by_container:
                calc_indent_level -= len(grab_bag.text_removed_by_container)
            if len(extracted_leaf_whitespace) > calc_indent_level:
                extracted_leaf_whitespace = extracted_leaf_whitespace[
                    :calc_indent_level
                ]
            list_token.add_leading_spaces(extracted_leaf_whitespace)
            actual_removed_leading_space = extracted_leaf_whitespace

            if not grab_bag.container_depth and not xposition_marker.index_indent:
                removed_leading_space = extracted_leaf_whitespace
        return list_token, removed_leading_space, actual_removed_leading_space

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_list_container(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        last_block_index: int,
        last_list_index: int,
        extracted_leaf_whitespace: Optional[str],
        grab_bag: ContainerGrabBag,
    ) -> Tuple[Optional[str], Optional[str], PositionMarker]:
        POGGER.debug("??? adjust_for_list_container")
        removed_leading_space = None
        actual_removed_leading_space = None
        assert extracted_leaf_whitespace is not None
        list_token: Optional[ListStartMarkdownToken] = None
        # pylint: disable=chained-comparison
        if (
            not grab_bag.was_indent_already_processed
            and last_block_index > 0
            and last_list_index > 0
            and last_list_index > last_block_index
        ):
            (
                list_token,
                removed_leading_space,
                actual_removed_leading_space,
            ) = ContainerBlockLeafProcessor.__adjust_for_list_container_after_block_quote(
                parser_state,
                xposition_marker,
                last_list_index,
                extracted_leaf_whitespace,
                grab_bag,
            )
        else:
            POGGER.debug("not adjust_for_list_container")
        # pylint: enable=chained-comparison
        if removed_leading_space:
            xposition_marker = PositionMarker(
                xposition_marker.line_number,
                len(removed_leading_space),
                xposition_marker.text_to_parse,
                index_indent=xposition_marker.index_indent,
            )
        # pylint: disable=too-many-boolean-expressions
        if (
            removed_leading_space is None
            and actual_removed_leading_space
            and list_token
            and grab_bag.block_quote_data.current_count
            == grab_bag.block_quote_data.stack_count
            and grab_bag.block_quote_data.stack_count > 1
            and grab_bag.is_para_continue
        ):
            assert grab_bag.text_removed_by_container is not None
            total_removed = len(grab_bag.text_removed_by_container) + len(
                actual_removed_leading_space
            )
            delta = list_token.indent_level - total_removed
            # assert t1 >= list_token.indent_level
            xposition_marker = PositionMarker(
                xposition_marker.line_number,
                xposition_marker.index_number,
                xposition_marker.text_to_parse[delta:],
                xposition_marker.index_indent,
            )
        # pylint: enable=too-many-boolean-expressions
        return removed_leading_space, actual_removed_leading_space, xposition_marker

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_for_list_container_find(
        parser_state: ParserState, xposition_marker: PositionMarker
    ) -> Optional[MarkdownToken]:
        found_list_token, document_index = (
            None,
            len(parser_state.token_document) - 1,
        )
        if (
            document_index >= 0
            and parser_state.token_document[document_index].line_number
            == xposition_marker.line_number
        ):
            assert (
                parser_state.token_document[document_index].is_list_start
                or parser_state.token_document[document_index].is_new_list_item
            )
            found_list_token = parser_state.token_document[document_index]
        return found_list_token

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_containers_before_leaf_blocks_adjust(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        last_block_index: int,
        total_ws: int,
        actual_removed_leading_space: Optional[str],
        grab_bag: ContainerGrabBag,
    ) -> Tuple[str, int, Optional[PositionMarker]]:
        if grab_bag.do_force_list_continuation:
            POGGER.debug(
                "actual_removed_leading_space=$=", actual_removed_leading_space
            )
            if not actual_removed_leading_space:
                actual_removed_leading_space = ""
            assert xposition_marker.text_to_parse.startswith(
                actual_removed_leading_space
            )
            position_marker = PositionMarker(
                xposition_marker.line_number,
                0,
                xposition_marker.text_to_parse[len(actual_removed_leading_space) :],
                xposition_marker.index_indent,
            )
            return "", -1, position_marker

        POGGER.debug("yes adjust_containers_before_leaf_blocks")
        (
            current_indent_level,
            close_tokens,
        ) = ContainerBlockLeafProcessor.__calculate_current_indent_level(
            parser_state,
            last_block_index,
            total_ws,
            xposition_marker.line_number,
            grab_bag,
        )
        if close_tokens:
            grab_bag.extend_container_tokens(close_tokens)

        assert parser_state.original_line_to_parse
        (
            new_index_indent,
            new_text_to_parse,
        ) = ContainerBlockLeafProcessor.__make_adjustments(
            parser_state,
            xposition_marker,
            current_indent_level,
            grab_bag,
        )
        ContainerBlockLeafProcessor.__val(parser_state, new_text_to_parse)
        return new_text_to_parse, new_index_indent, None

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_containers_before_leaf_blocks(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        last_block_index: int,
        total_ws: int,
        actual_removed_leading_space: Optional[str],
        grab_bag: ContainerGrabBag,
    ) -> PositionMarker:
        POGGER.debug("??? adjust_containers_before_leaf_blocks")
        if (
            xposition_marker.text_to_parse
            and not grab_bag.was_paragraph_continuation
            and not grab_bag.was_indent_already_processed
        ):
            (
                new_text_to_parse,
                new_index_indent,
                new_position_marker,
            ) = ContainerBlockLeafProcessor.__adjust_containers_before_leaf_blocks_adjust(
                parser_state,
                xposition_marker,
                last_block_index,
                total_ws,
                actual_removed_leading_space,
                grab_bag,
            )
            if new_position_marker:
                return new_position_marker
        else:
            POGGER.debug("not adjust_containers_before_leaf_blocks")
            new_text_to_parse = xposition_marker.text_to_parse
            new_index_indent = xposition_marker.index_indent

        indent_adjust = 0
        if actual_removed_leading_space and new_index_indent == len(
            actual_removed_leading_space
        ):
            indent_adjust += new_index_indent
            new_index_indent = 0

        return PositionMarker(
            xposition_marker.line_number,
            indent_adjust,
            new_text_to_parse,
            new_index_indent,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __calculate_current_indent_level_list(
        parser_state: ParserState, current_stack_index: int
    ) -> int:
        stack_token = cast(
            ListStackToken, parser_state.token_stack[current_stack_index]
        )
        if stack_token.last_new_list_token:
            return stack_token.last_new_list_token.indent_level
        list_token = cast(ListStartMarkdownToken, stack_token.matching_markdown_token)
        return list_token.indent_level

    @staticmethod
    def __post_leaf_block_adjustment(
        parser_state: ParserState,
        orig_text_removed_by_container: Optional[str],
        line_number: int,
    ) -> None:
        last_block_index = parser_state.find_last_block_quote_on_stack()
        POGGER.debug("last_block_index>>:$:", last_block_index)
        if not last_block_index:
            return

        last_block_token = cast(
            BlockQuoteMarkdownToken,
            parser_state.token_stack[last_block_index].matching_markdown_token,
        )

        if (
            not orig_text_removed_by_container
        ) and last_block_token.line_number != line_number:
            POGGER.debug(
                "plt-c>>last_block_token>>$",
                last_block_token,
            )
            POGGER.debug(
                "plt-c>>leading_text_index>>$", last_block_token.leading_text_index
            )
            last_block_token.add_bleading_spaces("")
            last_block_token.leading_text_index += 1
            POGGER.debug("plt-c>>last_block_token>>$", last_block_token)
            POGGER.debug(
                "plt-c>>leading_text_index>>$", last_block_token.leading_text_index
            )

    @staticmethod
    def __val(parser_state: ParserState, new_text_to_parse: str) -> None:
        assert parser_state.original_line_to_parse is not None
        if len(parser_state.original_line_to_parse) == len(new_text_to_parse):
            assert parser_state.original_line_to_parse.replace(
                ">", ParserHelper.space_character
            ) == new_text_to_parse.replace(">", ParserHelper.space_character), (
                "cheat=:"
                + ParserHelper.make_value_visible(parser_state.original_line_to_parse)
                + ":,new_text_to_parse=:"
                + ParserHelper.make_value_visible(new_text_to_parse)
                + ":"
            )
        else:
            is_valid = parser_state.original_line_to_parse.endswith(new_text_to_parse)
            assert is_valid, (
                "cheat=:"
                + ParserHelper.make_value_visible(parser_state.original_line_to_parse)
                + ":,new_text_to_parse=:"
                + ParserHelper.make_value_visible(new_text_to_parse)
                + ":"
            )

    @staticmethod
    def __make_adjustments(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        current_indent_level: int,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[int, str]:
        assert parser_state.original_line_to_parse is not None
        POGGER.debug(
            "parser_state.original_line_to_parse>>:$:($)",
            parser_state.original_line_to_parse,
            len(parser_state.original_line_to_parse),
        )
        POGGER.debug(
            "xposition_marker.text_to_parse>>:$:($)",
            xposition_marker.text_to_parse,
            len(xposition_marker.text_to_parse),
        )
        assert parser_state.original_line_to_parse
        if grab_bag.weird_adjusted_text:
            new_index_indent = len(grab_bag.weird_adjusted_text)
            grab_bag.text_removed_by_container = grab_bag.weird_adjusted_text
            new_text_to_parse = parser_state.original_line_to_parse[new_index_indent:]
        else:
            POGGER.debug("current_indent_level>>:$:<", current_indent_level)
            current_indent_level -= xposition_marker.index_indent
            POGGER.debug("current_indent_level>>:$:<", current_indent_level)
            assert current_indent_level >= 0

            prefix_text = xposition_marker.text_to_parse[:current_indent_level]
            new_text_to_parse = xposition_marker.text_to_parse[current_indent_level:]

            new_index_indent = len(parser_state.original_line_to_parse) - len(
                new_text_to_parse
            )

            POGGER.debug("new_text_to_parse>>:$:<", new_text_to_parse)
            POGGER.debug("new_index_indent>>:$:<", new_index_indent)
            grab_bag.text_removed_by_container = (
                grab_bag.text_removed_by_container + prefix_text
                if grab_bag.text_removed_by_container
                else prefix_text
            )
        return new_index_indent, new_text_to_parse

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_current_indent_level_loop(
        parser_state: ParserState,
        last_block_index: int,
        total_ws: int,
        line_number: int,
        current_stack_index: int,
        text_removed_by_container: Optional[str],
        current_indent_level: int,
        non_last_block_index: int,
        last_list_index: int,
        had_non_block_token: bool,
        did_hit_indent_level_threshold: bool,
    ) -> Tuple[int, int, int, bool, bool, bool]:
        proposed_indent_level: Optional[int] = 0
        POGGER.debug("token:$:", parser_state.token_stack[current_stack_index])
        continue_in_loop = True
        keep_processing = True
        if parser_state.token_stack[current_stack_index].is_block_quote:
            last_list_index = 0
            (
                new_indent_level,
                non_last_block_index,
            ) = ContainerBlockLeafProcessor.__calculate_current_indent_level_block_quote(
                parser_state,
                current_stack_index,
                non_last_block_index,
                last_block_index,
                line_number,
                current_indent_level,
                text_removed_by_container,
            )
            keep_processing = new_indent_level is not None
            if keep_processing:
                proposed_indent_level = new_indent_level
        elif parser_state.token_stack[current_stack_index].is_list:
            last_list_index = current_stack_index
            proposed_indent_level = (
                ContainerBlockLeafProcessor.__calculate_current_indent_level_list(
                    parser_state, current_stack_index
                )
            )
        else:
            had_non_block_token = True
            continue_in_loop = False
        POGGER.debug(
            "proposed_indent_level:$ <= total_ws:$<",
            proposed_indent_level,
            total_ws,
        )
        if continue_in_loop and keep_processing:
            assert proposed_indent_level is not None
            if proposed_indent_level > total_ws:
                did_hit_indent_level_threshold = True
                continue_in_loop = False
            else:
                current_indent_level = proposed_indent_level
                POGGER.debug("current_indent_level:$", current_indent_level)
        return (
            current_indent_level,
            non_last_block_index,
            last_list_index,
            had_non_block_token,
            did_hit_indent_level_threshold,
            continue_in_loop,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __calculate_current_indent_level(
        parser_state: ParserState,
        last_block_index: int,
        total_ws: int,
        line_number: int,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[int, List[MarkdownToken]]:
        text_removed_by_container = grab_bag.text_removed_by_container
        current_indent_level = 0
        non_last_block_index = 0
        last_list_index = 0
        had_non_block_token = False
        did_hit_indent_level_threshold = False
        POGGER.debug("token-stack:$:", parser_state.token_stack)
        for current_stack_index in range(1, len(parser_state.token_stack)):
            POGGER.debug("<<current_indent_level:$", current_indent_level)
            (
                current_indent_level,
                non_last_block_index,
                last_list_index,
                had_non_block_token,
                did_hit_indent_level_threshold,
                continue_in_loop,
            ) = ContainerBlockLeafProcessor.__calculate_current_indent_level_loop(
                parser_state,
                last_block_index,
                total_ws,
                line_number,
                current_stack_index,
                text_removed_by_container,
                current_indent_level,
                non_last_block_index,
                last_list_index,
                had_non_block_token,
                did_hit_indent_level_threshold,
            )
            POGGER.debug("<<current_indent_level:$", current_indent_level)
            if not continue_in_loop:
                break
        POGGER.debug("<<current_indent_level:$", current_indent_level)
        close_tokens: List[MarkdownToken] = []
        if last_list_index:
            POGGER.debug("<<had_non_block_token:$", had_non_block_token)
            POGGER.debug("<<grab_bag.is_para_continue:$", grab_bag.is_para_continue)
            if (
                not had_non_block_token
                and did_hit_indent_level_threshold
                and not grab_bag.is_para_continue
            ):
                POGGER.debug("<<last_list_index:$", last_list_index)
                (
                    close_tokens,
                    grab_bag.requeue_line_info,
                ) = parser_state.close_open_blocks_fn(
                    parser_state,
                    include_lists=True,
                    was_forced=True,
                    until_this_index=last_list_index,
                )
                POGGER.debug("<<close_tokens:$", close_tokens)
        return current_indent_level, close_tokens

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_current_indent_level_block_quote(
        parser_state: ParserState,
        current_stack_index: int,
        non_last_block_index: int,
        last_block_index: int,
        line_number: int,
        current_indent_level: int,
        text_removed_by_container: Optional[str],
    ) -> Tuple[Optional[int], int]:
        if current_stack_index != last_block_index:
            POGGER.debug("not last bq token, skipping")
            non_last_block_index = current_stack_index
            return None, non_last_block_index

        matching_token = parser_state.token_stack[
            current_stack_index
        ].matching_markdown_token
        assert matching_token is not None
        POGGER.debug("line_number=$", line_number)
        POGGER.debug(
            "matching_markdown_token.line_number=$", matching_token.line_number
        )
        POGGER.debug("non_last_block_index=$", non_last_block_index)

        valid_mark = non_last_block_index and non_last_block_index != (
            last_block_index - 1
        )
        POGGER.debug("current_indent_level=:$:", current_indent_level)
        base_indent_level = (
            current_indent_level
            if valid_mark and line_number == matching_token.line_number
            else 0
        )
        POGGER.debug("text_removed_by_container=:$:", text_removed_by_container)
        POGGER.debug("base_indent_level=:$:", base_indent_level)
        proposed_indent_level = (
            len(text_removed_by_container) if text_removed_by_container else 0
        ) + base_indent_level
        POGGER.debug("last bq token, processing:$", proposed_indent_level)
        return proposed_indent_level, non_last_block_index

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
