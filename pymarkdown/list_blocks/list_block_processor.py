"""
Module to provide processing for the list blocks.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.requeue_line_info import RequeueLineInfo
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.html.html_helper import HtmlHelper
from pymarkdown.leaf_blocks.atx_leaf_block_processor import AtxLeafBlockProcessor
from pymarkdown.leaf_blocks.fenced_leaf_block_processor import FencedLeafBlockProcessor
from pymarkdown.leaf_blocks.leaf_block_processor import LeafBlockProcessor
from pymarkdown.leaf_blocks.leaf_block_processor_paragraph import (
    LeafBlockProcessorParagraph,
)
from pymarkdown.leaf_blocks.thematic_leaf_block_processor import (
    ThematicLeafBlockProcessor,
)
from pymarkdown.list_blocks.list_block_create_new_handler import (
    ListBlockCreateNewHandler,
)
from pymarkdown.list_blocks.list_block_pre_list_helper import ListBlockPreListHelper
from pymarkdown.list_blocks.list_block_starts_helper import ListBlockStartsHelper
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import ListStackToken, StackToken

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


class ListBlockProcessor:
    """
    Class to provide processing for the list blocks.
    """

    @staticmethod
    def __handle_list_with_leading_indent_loop(
        acceptable_indent_stack_index: int,
        parser_state: ParserState,
        stack_index: int,
        extracted_whitespace: str,
    ) -> int:
        box_start = 1 if stack_index == 1 else ((stack_index + 1) * 4) + stack_index
        box_end = (stack_index * 4) + (stack_index - 1)

        is_in_this_box = box_start <= len(extracted_whitespace) + 1 <= box_end
        can_promote_to_next_box = (stack_index + 1) < len(
            parser_state.token_stack
        ) and parser_state.token_stack[stack_index + 1].is_list

        if is_in_this_box or can_promote_to_next_box:
            acceptable_indent_stack_index = stack_index
        return acceptable_indent_stack_index

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_list_with_leading_indent(
        parser_state: ParserState,
        container_depth: int,
        removed_chars_at_start: int,
        extracted_whitespace: str,
        indent_already_processed: bool,
        adj_ws: str,
    ) -> Tuple[int, Optional[str], str, str, bool]:
        indent_already_used, forced_container_whitespace = 0, None
        is_in_root_list = (
            not container_depth
            and parser_state.token_stack
            and len(parser_state.token_stack) >= 2
            and parser_state.token_stack[1].is_list
        )

        if (
            not removed_chars_at_start
            and is_in_root_list
            and adj_ws == extracted_whitespace
            and len(extracted_whitespace) >= 4
            and not indent_already_processed
        ):
            stack_index = 1
            acceptable_indent_stack_index = 0
            while (
                stack_index < len(parser_state.token_stack)
                and parser_state.token_stack[stack_index].is_list
            ):
                acceptable_indent_stack_index = (
                    ListBlockProcessor.__handle_list_with_leading_indent_loop(
                        acceptable_indent_stack_index,
                        parser_state,
                        stack_index,
                        extracted_whitespace,
                    )
                )
                stack_index += 1

            if acceptable_indent_stack_index:
                list_stack_token = parser_state.token_stack[
                    acceptable_indent_stack_index
                ]
                assert list_stack_token.is_list, "Token must be a list token."
                list_token = cast(
                    ListStartMarkdownToken, list_stack_token.matching_markdown_token
                )
                indent_already_used = list_token.indent_level
                forced_container_whitespace = extracted_whitespace[:indent_already_used]
                extracted_whitespace = extracted_whitespace[indent_already_used:]
                adj_ws = adj_ws[indent_already_used:]
                indent_already_processed = True
        return (
            indent_already_used,
            forced_container_whitespace,
            extracted_whitespace,
            adj_ws,
            indent_already_processed,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_list_block_init(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: str,
        adj_ws: str,
        is_ulist: bool,
        container_depth: int,
        removed_chars_at_start: int,
        indent_already_processed: bool,
    ) -> Tuple[
        bool,
        int,
        Optional[int],
        Optional[int],
        int,
        Optional[str],
        str,
        str,
        bool,
    ]:
        POGGER.debug(
            "hlb>>parser_state.nested_list_start>$", parser_state.nested_list_start
        )
        POGGER.debug("hlb>>extracted_whitespace>$<", extracted_whitespace)
        POGGER.debug("hlb>>adj_ws>$<", adj_ws)
        POGGER.debug("hlb>>removed_chars_at_start>$<", removed_chars_at_start)
        POGGER.debug(
            "text_to_parse[index=$:]>:$:<",
            position_marker.index_number,
            position_marker.text_to_parse[position_marker.index_number :],
        )

        (
            indent_already_used,
            forced_container_whitespace,
            extracted_whitespace,
            adj_ws,
            indent_already_processed,
        ) = ListBlockProcessor.__handle_list_with_leading_indent(
            parser_state,
            container_depth,
            removed_chars_at_start,
            extracted_whitespace,
            indent_already_processed,
            adj_ws,
        )

        if is_ulist:
            (
                started_ulist,
                end_of_ulist_start_index,
                index,
                number_of_digits,
            ) = ListBlockStartsHelper.is_ulist_start(
                parser_state,
                position_marker.text_to_parse,
                position_marker.index_number,
                extracted_whitespace,
                False,
                adj_ws,
            )
        else:
            (
                started_ulist,
                end_of_ulist_start_index,
                index,
                number_of_digits,
            ) = ListBlockStartsHelper.is_olist_start(
                parser_state,
                position_marker.text_to_parse,
                position_marker.index_number,
                extracted_whitespace,
                False,
                adj_ws,
            )
        return (
            started_ulist,
            end_of_ulist_start_index,
            index,
            number_of_digits,
            indent_already_used,
            forced_container_whitespace,
            extracted_whitespace,
            adj_ws,
            indent_already_processed,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __create_new_list_if_indented(
        parser_state: ParserState,
        position_marker: PositionMarker,
        indent_level: int,
        ws_before_marker: int,
        ws_after_marker: int,
        extracted_whitespace: str,
        forced_container_whitespace: Optional[str],
        adj_ws: str,
        adjusted_text_to_parse: Optional[str],
        index: int,
        container_level_tokens: List[MarkdownToken],
        remaining_whitespace: int,
        after_marker_ws_index: int,
        current_container_blocks: List[StackToken],
        container_depth: int,
        original_line: str,
        is_ulist: bool,
    ) -> Tuple[bool, Optional[str], Optional[RequeueLineInfo]]:
        POGGER.debug(
            "total=$;ws-before=$;ws_after=$;start_index=$",
            indent_level,
            ws_before_marker,
            ws_after_marker,
            position_marker.index_number,
        )
        POGGER.debug("extracted_whitespace=$=", extracted_whitespace)
        if indent_level >= 0:
            POGGER.debug("indent_level=$=", indent_level)
            POGGER.debug("ws_before_marker=$=", ws_before_marker)
            POGGER.debug("forced_container_whitespace=$=", forced_container_whitespace)
            return ListBlockCreateNewHandler.create_new_list(
                parser_state,
                position_marker,
                indent_level,
                extracted_whitespace,
                ws_before_marker,
                ws_after_marker,
                index,
                container_level_tokens,
                remaining_whitespace,
                after_marker_ws_index,
                current_container_blocks,
                container_depth,
                original_line,
                is_ulist,
                adj_ws,
                forced_container_whitespace,
            )
        return (
            False,
            adjusted_text_to_parse,
            None,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __handle_list_block_pull_from_grab_bag(
        grab_bag: ContainerGrabBag,
    ) -> Tuple[
        str,
        str,
        BlockQuoteData,
        int,
        List[StackToken],
        int,
        bool,
        str,
    ]:
        assert (
            grab_bag.extracted_whitespace is not None
        ), "extracted_whitespace must be defined by now"
        assert (
            grab_bag.removed_chars_at_start_of_line is not None
        ), "Characters must have been removed by this point."
        assert grab_bag.adj_ws is not None, "adj_ws must be defined by now"

        extracted_whitespace = grab_bag.extracted_whitespace
        removed_chars_at_start: int = grab_bag.removed_chars_at_start_of_line
        adj_ws = grab_bag.adj_ws

        block_quote_data: BlockQuoteData = grab_bag.block_quote_data

        current_container_blocks: List[StackToken] = grab_bag.current_container_blocks
        container_depth: int = grab_bag.container_depth

        indent_already_processed: bool = grab_bag.was_indent_already_processed
        original_line = grab_bag.original_line

        return (
            extracted_whitespace,
            adj_ws,
            block_quote_data,
            removed_chars_at_start,
            current_container_blocks,
            container_depth,
            indent_already_processed,
            original_line,
        )

    # pylint: disable=too-many-locals
    @staticmethod
    def handle_list_block(
        is_ulist: bool,
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[bool, int, Optional[str], List[MarkdownToken]]:
        """
        Handle the processing of a ulist block.
        """
        (
            extracted_whitespace,
            adj_ws,
            block_quote_data,
            removed_chars_at_start,
            current_container_blocks,
            container_depth,
            indent_already_processed,
            original_line,
        ) = ListBlockProcessor.__handle_list_block_pull_from_grab_bag(grab_bag)

        (
            did_process,
            requeue_line_info,
            old_extracted_whitespace,
            old_indent_already_processed,
        ) = (
            False,
            None,
            extracted_whitespace,
            indent_already_processed,
        )
        adjusted_text_to_parse: Optional[str] = position_marker.text_to_parse
        container_level_tokens: List[MarkdownToken] = []

        (
            started_ulist,
            end_of_ulist_start_index,
            index,
            number_of_digits,
            indent_already_used,
            forced_container_whitespace,
            extracted_whitespace,
            adj_ws,
            indent_already_processed,
        ) = ListBlockProcessor.__handle_list_block_init(
            parser_state,
            position_marker,
            extracted_whitespace,
            adj_ws,
            is_ulist,
            container_depth,
            removed_chars_at_start,
            indent_already_processed,
        )
        POGGER.debug("clt>>list-start=$", started_ulist)
        if started_ulist:
            POGGER.debug("clt>>ulist-start")
            removed_chars_at_start = indent_already_used
            assert (
                index is not None and number_of_digits is not None
            ), "If started_ulist, both index and number_of_digits must be valid."
            (
                indent_level,
                remaining_whitespace,
                ws_after_marker,
                after_marker_ws_index,
                ws_before_marker,
                container_level_tokens,
                block_quote_data,
            ) = ListBlockPreListHelper.pre_list(
                parser_state,
                position_marker.text_to_parse,
                index,
                extracted_whitespace,
                number_of_digits,
                block_quote_data,
                adj_ws,
                position_marker,
                container_depth,
            )

            (
                did_process,
                adjusted_text_to_parse,
                requeue_line_info,
            ) = ListBlockProcessor.__create_new_list_if_indented(
                parser_state,
                position_marker,
                indent_level,
                ws_before_marker,
                ws_after_marker,
                extracted_whitespace,
                forced_container_whitespace,
                adj_ws,
                adjusted_text_to_parse,
                index,
                container_level_tokens,
                remaining_whitespace,
                after_marker_ws_index,
                current_container_blocks,
                container_depth,
                original_line,
                is_ulist,
            )
        else:
            extracted_whitespace = old_extracted_whitespace
            indent_already_processed = old_indent_already_processed

        ListBlockProcessor.__handle_list_block_push_to_grab_bag(
            grab_bag,
            removed_chars_at_start,
            block_quote_data,
            requeue_line_info,
            indent_already_processed,
            extracted_whitespace,
        )

        return (
            did_process,
            end_of_ulist_start_index,
            adjusted_text_to_parse,
            container_level_tokens,
        )

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_list_block_push_to_grab_bag(
        grab_bag: ContainerGrabBag,
        removed_chars_at_start: int,
        block_quote_data: BlockQuoteData,
        requeue_line_info: Optional[RequeueLineInfo],
        indent_already_processed: bool,
        extracted_whitespace: Optional[str],
    ) -> None:
        grab_bag.removed_chars_at_start_of_line = removed_chars_at_start
        grab_bag.block_quote_data = block_quote_data
        grab_bag.requeue_line_info = requeue_line_info
        grab_bag.was_indent_already_processed = indent_already_processed
        grab_bag.extracted_whitespace = extracted_whitespace

    # pylint: enable=too-many-arguments
    # pylint: disable=too-many-arguments
    @staticmethod
    def __list_in_process_update_containers(
        parser_state: ParserState,
        ind: int,
        used_indent: Optional[str],
        was_paragraph_continuation: bool,
        start_index: int,
        grab_bag: ContainerGrabBag,
    ) -> None:
        stack_index = parser_state.find_last_list_block_on_stack()
        if stack_index > 0:
            list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[stack_index].matching_markdown_token,
            )
            POGGER.debug(
                "lip>>last_block_token>>$",
                list_token,
            )

        POGGER.debug(">>used_indent>>$<<", used_indent)
        POGGER.debug(">>was_paragraph_continuation>>$<<", was_paragraph_continuation)
        if used_indent is not None:
            list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[ind].matching_markdown_token,
            )
            POGGER.debug(
                "__list_in_process_update_containers>>list_token>>$", list_token
            )
            list_token.add_leading_spaces(used_indent)
            POGGER.debug(
                "__list_in_process_update_containers>>list_token>>$", list_token
            )
        else:
            stack_index = parser_state.find_last_list_block_on_stack()
            need_to_add_leading_spaces = False
            if stack_index > 0:
                assert (
                    parser_state.original_line_to_parse is not None
                ), "Original line must be defined by this point."

                last_container_index = parser_state.find_last_container_on_stack()
                consumed_text = parser_state.original_line_to_parse[:start_index]
                back_index = stack_index
                while back_index and parser_state.token_stack[back_index].is_list:
                    back_index -= 1
                need_to_add_leading_spaces = (
                    back_index <= 0
                    or not consumed_text
                    or ">" in consumed_text
                    or stack_index != last_container_index
                )
            if need_to_add_leading_spaces:
                ListBlockProcessor.__list_in_process_update_containers_part_2(
                    parser_state, stack_index, consumed_text, grab_bag
                )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __list_in_process_update_containers_part_2(
        parser_state: ParserState,
        stack_index: int,
        consumed_text: str,
        grab_bag: ContainerGrabBag,
    ) -> None:
        list_stack_token = cast(ListStackToken, parser_state.token_stack[stack_index])
        list_token = cast(
            ListStartMarkdownToken,
            parser_state.token_stack[stack_index].matching_markdown_token,
        )
        if lists_new_list_token := list_stack_token.last_new_list_token:
            lists_indent_level = lists_new_list_token.indent_level
        else:
            lists_indent_level = list_token.indent_level
        assert not consumed_text or len(consumed_text) < lists_indent_level
        grab_bag.bogus = consumed_text
        POGGER.debug("__list_in_process_update_containers2>>list_token>>$", list_token)
        list_token.add_leading_spaces("")
        POGGER.debug("__list_in_process_update_containers2>>list_token>>$", list_token)

    # pylint: disable=too-many-locals
    @staticmethod
    def list_in_process(
        parser_state: ParserState,
        ind: int,
        index_indent: int,
        grab_bag: ContainerGrabBag,
    ) -> List[MarkdownToken]:
        """
        Handle the processing of a line where there is a list in process.
        """
        assert (
            grab_bag.extracted_whitespace is not None
        ), "Extracted whitespace must be defined by this point."
        assert parser_state.token_stack[
            ind
        ].is_list, "Index must point to a valid list."
        extracted_whitespace = grab_bag.extracted_whitespace
        assert (
            extracted_whitespace is not None
        ), "extracted_whitespace must be defined by now"

        line_to_parse = grab_bag.line_to_parse
        start_index = grab_bag.start_index
        list_stack_token = cast(ListStackToken, parser_state.token_stack[ind])
        before_ws_length = list_stack_token.ws_before_marker
        leading_space_length = TabHelper.calculate_length(extracted_whitespace)
        requested_list_indent = (
            list_stack_token.last_new_list_token.indent_level
            if list_stack_token.last_new_list_token
            else list_stack_token.indent_level
        )

        allow_list_continue = ListBlockProcessor.__can_list_continue(
            parser_state,
            line_to_parse,
            start_index,
            extracted_whitespace,
            leading_space_length,
        )
        POGGER.debug(
            "leading_space_length>>$>>requested_list_indent>>$>>is_in_paragraph>>$",
            leading_space_length,
            requested_list_indent,
            parser_state.token_stack[-1].is_paragraph,
        )
        used_indent = None
        if (
            was_paragraph_continuation := leading_space_length >= requested_list_indent
            and allow_list_continue
        ):
            POGGER.debug("list-in-progress: was_paragraph_continuation")
            container_level_tokens: List[MarkdownToken] = []
            (
                line_to_parse,
                used_indent,
            ) = ListBlockProcessor.__adjust_line_for_list_in_process(
                line_to_parse,
                start_index,
                extracted_whitespace,
                leading_space_length,
                requested_list_indent,
                grab_bag.original_line,
            )
        else:
            POGGER.debug("list-in-progress: not was_paragraph_continuation")
            (
                container_level_tokens,
                line_to_parse,
                used_indent,
                ind,
                requeue_line_info,
                was_paragraph_continuation,
            ) = ListBlockProcessor.__process_list_non_continue(
                parser_state,
                requested_list_indent,
                leading_space_length,
                before_ws_length,
                line_to_parse,
                start_index,
                extracted_whitespace,
                allow_list_continue,
                ind,
                grab_bag.original_line,
                index_indent,
            )
            if requeue_line_info:
                grab_bag.line_to_parse = line_to_parse
                grab_bag.indent_used_by_list = None
                grab_bag.requeue_line_info = requeue_line_info
                grab_bag.was_paragraph_continuation = False
                return []
        ListBlockProcessor.__list_in_process_update_containers(
            parser_state,
            ind,
            used_indent,
            was_paragraph_continuation,
            start_index,
            grab_bag,
        )

        grab_bag.line_to_parse = line_to_parse
        grab_bag.indent_used_by_list = used_indent
        grab_bag.requeue_line_info = None
        grab_bag.was_paragraph_continuation = was_paragraph_continuation

        return container_level_tokens

    # pylint: enable=too-many-locals

    @staticmethod
    def __can_list_continue(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: str,
        leading_space_length: int,
    ) -> bool:
        started_ulist, _, _, _ = ListBlockStartsHelper.is_ulist_start(
            parser_state, line_to_parse, start_index, extracted_whitespace, True, None
        )
        started_olist, _, _, _ = ListBlockStartsHelper.is_olist_start(
            parser_state, line_to_parse, start_index, extracted_whitespace, True, None
        )
        return (
            (not parser_state.token_document[-1].is_blank_line)
            if leading_space_length >= 4 and (started_ulist or started_olist)
            else True
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __check_for_paragraph_break(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: str,
        original_line: str,
        index_indent: int,
    ) -> bool:
        POGGER.debug("is_theme_break>>?")
        is_theme_break, _ = ThematicLeafBlockProcessor.is_thematic_break(
            line_to_parse,
            start_index,
            extracted_whitespace,
            skip_whitespace_check=True,
        )
        POGGER.debug("is_theme_break>>$", is_theme_break)
        POGGER.debug("is_atx_heading>>?")
        is_atx_heading, _, _, _ = AtxLeafBlockProcessor.is_atx_heading(
            line_to_parse, start_index, extracted_whitespace, skip_whitespace_check=True
        )
        POGGER.debug("is_atx_heading>>$", is_atx_heading)
        POGGER.debug("is_fenced_start>>?")
        is_fenced_start, _, _, _, _ = FencedLeafBlockProcessor.is_fenced_code_block(
            parser_state,
            line_to_parse,
            start_index,
            extracted_whitespace,
            original_line,
            index_indent,
            skip_whitespace_check=True,
        )
        POGGER.debug("is_fenced_start>>$", is_fenced_start)
        POGGER.debug("is_html_start>>?")
        is_html_start, _ = HtmlHelper.is_html_block(
            line_to_parse,
            start_index,
            extracted_whitespace,
            parser_state.token_stack,
            parser_state.parse_properties,
            skip_whitespace_check=True,
        )
        POGGER.debug("is_html_start>>$", is_html_start)
        return (
            bool(is_theme_break)
            or is_atx_heading
            or is_fenced_start
            or bool(is_html_start)
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments,too-many-locals
    @staticmethod
    def __process_list_non_continue(
        parser_state: ParserState,
        requested_list_indent: int,
        leading_space_length: int,
        before_ws_length: int,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: str,
        allow_list_continue: bool,
        ind: int,
        original_line: str,
        index_indent: int,
    ) -> Tuple[
        List[MarkdownToken],
        str,
        Optional[str],
        int,
        Optional[RequeueLineInfo],
        bool,
    ]:
        POGGER.debug(
            "requested_list_indent>>$<<",
            requested_list_indent,
        )
        requested_list_indent -= before_ws_length

        POGGER.debug(
            "leading_space_length>>$>>adj requested_list_indent>>$>>$<<",
            leading_space_length,
            requested_list_indent,
            parser_state.token_stack[-1].is_paragraph,
        )

        was_breakable_leaf_detected = ListBlockProcessor.__check_for_paragraph_break(
            parser_state,
            line_to_parse,
            start_index,
            extracted_whitespace,
            original_line,
            index_indent,
        )

        if was_paragraph_continuation := (
            parser_state.token_stack[-1].is_paragraph
            and leading_space_length >= requested_list_indent
            and allow_list_continue
            and not was_breakable_leaf_detected
        ):
            container_level_tokens: List[MarkdownToken] = []
            POGGER.debug(
                "1>>line_to_parse>>$>>",
                line_to_parse,
            )
            (
                line_to_parse,
                used_indent,
            ) = ListBlockProcessor.__adjust_line_for_list_in_process(
                line_to_parse,
                start_index,
                extracted_whitespace,
                leading_space_length,
                requested_list_indent + before_ws_length,
                original_line,
            )
            was_paragraph_continuation = used_indent is None
            POGGER.debug(
                ">>line_to_parse>>$>>",
                line_to_parse,
            )
            POGGER.debug(">>used_indent>>$>>", used_indent)
        else:
            POGGER.debug(
                "2>>line_to_parse>>$>>",
                line_to_parse,
            )
            (
                container_level_tokens,
                requeue_line_info,
            ) = ListBlockProcessor.__check_for_list_closures(
                parser_state,
                line_to_parse,
                start_index,
                extracted_whitespace,
                ind,
                leading_space_length,
                original_line,
                index_indent,
            )
            POGGER.debug(
                "2>>requeue_line_info>>$>>",
                requeue_line_info,
            )
            if requeue_line_info:
                return [], line_to_parse, None, -1, requeue_line_info, False

            (
                line_to_parse,
                used_indent,
                ind,
            ) = ListBlockProcessor.__adjust_for_nested_list(
                parser_state,
                container_level_tokens,
                ind,
                line_to_parse,
                extracted_whitespace,
                start_index,
                before_ws_length,
                leading_space_length,
                original_line,
            )

        # POGGER.debug(">>line_to_parse>>$>>",line_to_parse)
        return (
            container_level_tokens,
            line_to_parse,
            used_indent,
            ind,
            None,
            was_paragraph_continuation,
        )

    # pylint: enable=too-many-arguments,too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_nested_list(
        parser_state: ParserState,
        container_level_tokens: List[MarkdownToken],
        ind: int,
        line_to_parse: str,
        extracted_whitespace: str,
        start_index: int,
        before_ws_length: int,
        leading_space_length: int,
        original_line: str,
    ) -> Tuple[str, Optional[str], int]:
        POGGER.debug(
            "2>>__check_for_list_closures>>$>>",
            container_level_tokens,
        )
        POGGER.debug(
            "2>>parser_state.token_stack>>$>>",
            parser_state.token_stack,
        )
        POGGER.debug(
            "2>>ind>>$>>",
            ind,
        )

        found_owning_list: Optional[ListStackToken] = None
        if container_level_tokens:
            (
                did_find,
                last_list_index,
            ) = LeafBlockProcessorParagraph.check_for_list_in_process(parser_state)
            POGGER.debug(
                "2>>did_find>>$>>$>>",
                did_find,
                last_list_index,
            )
            if did_find:
                ind = last_list_index
                found_owning_list = cast(ListStackToken, parser_state.token_stack[ind])
        else:
            assert parser_state.token_stack[ind].is_list, "Token must be a list token."
            found_owning_list = cast(ListStackToken, parser_state.token_stack[ind])

        if found_owning_list:
            POGGER.debug(">>in list>>")
            requested_list_indent = (
                (found_owning_list.last_new_list_token.indent_level)
                if found_owning_list.last_new_list_token
                else found_owning_list.indent_level
            )
            POGGER.debug(">>line_to_parse>>$>>", line_to_parse)
            POGGER.debug(">>extracted_whitespace>>$<<", extracted_whitespace)
            POGGER.debug(">>start_index>>$", start_index)
            POGGER.debug(">>requested_list_indent>>$", requested_list_indent)
            POGGER.debug(">>before_ws_length>>$", before_ws_length)
            (
                line_to_parse,
                used_indent,
            ) = ListBlockProcessor.__adjust_line_for_list_in_process(
                line_to_parse,
                start_index,
                extracted_whitespace,
                leading_space_length,
                requested_list_indent,
                original_line,
            )
            POGGER.debug(">>line_to_parse>>$", line_to_parse)
            POGGER.debug(">>used_indent>>$<<", used_indent)
        else:
            used_indent = None
        return line_to_parse, used_indent, ind

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_line_for_list_in_process_with_tab(
        original_line: str, remaining_indent: int, removed_whitespace: str
    ) -> str:
        _, ex_ws = ParserHelper.extract_spaces_verified(original_line, 0)
        POGGER.debug("ex_ws($)", ex_ws)
        if "\t" in ex_ws:
            detabified_ws = TabHelper.detabify_string(ex_ws, 0)
            POGGER.debug("detabified_ws($)", detabified_ws)
            assert (
                len(detabified_ws) >= remaining_indent
            ), "Length must be greater than the indent."

            sub_ws = None
            i = -1
            do_loop = True
            # for i in range(len(ex_ws)):
            while do_loop:
                i += 1
                assert i < len(ex_ws), "Index must be within the string."
                sub_ws = ex_ws[: i + 1]
                POGGER.debug("sub_ws($)", sub_ws)
                detabified_ws = TabHelper.detabify_string(sub_ws, 0)
                POGGER.debug("detabified_ws($)", detabified_ws)
                POGGER.debug(
                    "detabified_ws($),removed_whitespace($)",
                    len(detabified_ws),
                    len(removed_whitespace),
                )
                if len(detabified_ws) >= len(removed_whitespace):
                    do_loop = False
            if len(detabified_ws) <= len(removed_whitespace):
                assert sub_ws is not None, "Subws must have been defined."
                removed_whitespace = sub_ws
        return removed_whitespace

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_line_for_list_in_process(
        line_to_parse: str,
        start_index: int,
        leading_space: str,
        leading_space_length: int,
        requested_list_indent: int,
        original_line: str,
    ) -> Tuple[str, Optional[str]]:
        """
        Alter the current line to better represent the current level of lists.
        """
        remaining_indent = leading_space_length - requested_list_indent
        POGGER.debug("original_line($)", original_line)
        POGGER.debug(
            "enough ws to continue; line($),start_index($),leading_space($)",
            line_to_parse,
            start_index,
            leading_space,
        )
        if remaining_indent < 0:
            padded_spaces = ""
            start_index = 0
            removed_whitespace = None
        else:
            POGGER.debug("requested_list_indent($)", requested_list_indent)
            POGGER.debug("leading_space($)", leading_space)
            padded_spaces = ParserHelper.repeat_string(
                ParserHelper.space_character, remaining_indent
            )
            removed_whitespace = leading_space[:requested_list_indent]
            if "\t" in original_line:
                removed_whitespace = (
                    ListBlockProcessor.__adjust_line_for_list_in_process_with_tab(
                        original_line, remaining_indent, removed_whitespace
                    )
                )
        POGGER.debug("padded_spaces($)", padded_spaces)
        POGGER.debug("line_to_parse[start_index:]($)", line_to_parse[start_index:])
        POGGER.debug("removed_whitespace($)", removed_whitespace)
        return (
            f"{padded_spaces}{line_to_parse[start_index:]}",
            removed_whitespace,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __check_for_list_closures(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: str,
        ind: int,
        leading_space_length: int,
        original_line: str,
        index_indent: int,
    ) -> Tuple[List[MarkdownToken], Optional[RequeueLineInfo]]:
        """
        Check to see if the list in progress and the level of lists shown require
        the closing of some of the sublists.
        """
        POGGER.debug("ws(naa)>>line_to_parse>>$<<", line_to_parse)
        POGGER.debug("ws(naa)>>stack>>$", parser_state.token_stack)
        POGGER.debug("ws(naa)>>tokens>>$", parser_state.token_document)

        is_leaf_block_start = LeafBlockProcessor.is_paragraph_ending_leaf_block_start(
            parser_state,
            line_to_parse,
            start_index,
            extracted_whitespace,
            original_line,
            index_indent,
        )
        if not parser_state.token_stack[-1].is_paragraph or is_leaf_block_start:
            POGGER.debug("ws (normal and adjusted) not enough to continue")

            POGGER.debug("lsl $", leading_space_length)
            POGGER.debug("lsl $", parser_state.token_stack[ind])
            search_index = ind
            POGGER.debug(
                "lsl $>$",
                search_index,
                parser_state.token_stack[search_index - 1],
            )
            while parser_state.token_stack[search_index - 1].is_list:
                list_token = cast(
                    ListStackToken, parser_state.token_stack[search_index - 1]
                )
                if list_token.indent_level <= leading_space_length:
                    break
                search_index -= 1

            POGGER.debug("lsl $", parser_state.token_stack[search_index])

            (
                container_level_tokens,
                requeue_line_info,
            ) = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=search_index,
                include_lists=True,
                caller_can_handle_requeue=True,
                requeue_reset=True,
            )
        else:
            container_level_tokens, requeue_line_info = [], None

        return container_level_tokens, requeue_line_info

    # pylint: enable=too-many-arguments
