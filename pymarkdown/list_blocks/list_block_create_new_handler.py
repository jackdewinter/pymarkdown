"""
Module to provide for the creation of tokens for the new lists.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.requeue_line_info import RequeueLineInfo
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.leaf_blocks.leaf_block_processor_paragraph import (
    LeafBlockProcessorParagraph,
)
from pymarkdown.list_blocks.list_block_can_close_helper import ListBlockCanCloseHelper
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.new_list_item_markdown_token import NewListItemMarkdownToken
from pymarkdown.tokens.ordered_list_start_markdown_token import (
    OrderedListStartMarkdownToken,
)
from pymarkdown.tokens.stack_token import (
    BlockQuoteStackToken,
    ListStackToken,
    OrderedListStackToken,
    StackToken,
    UnorderedListStackToken,
)
from pymarkdown.tokens.unordered_list_start_markdown_token import (
    UnorderedListStartMarkdownToken,
)

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-few-public-methods


class ListBlockCreateNewHandler:
    """
    Class to provide for the creation of tokens for the new lists.
    """

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def create_new_list(
        parser_state: ParserState,
        position_marker: PositionMarker,
        indent_level: int,
        extracted_whitespace: Optional[str],
        ws_before_marker: int,
        ws_after_marker: int,
        index: int,
        container_level_tokens: List[MarkdownToken],
        remaining_whitespace: int,
        after_marker_ws_index: int,
        current_container_blocks: List[StackToken],
        container_depth: int,
        original_line: str,
        is_ulist: bool,
        alt_adj_ws: Optional[str] = None,
        forced_container_whitespace: Optional[str] = None,
    ) -> Tuple[bool, Optional[str], Optional[RequeueLineInfo]]:
        """
        Create a new list at the current location.
        """
        adj_ws = ListBlockCreateNewHandler.__calculate_create_adj_ws(
            alt_adj_ws, position_marker, parser_state
        )
        found_block_quote_before_list = (
            ListBlockCreateNewHandler.__find_block_quote_before_list(parser_state)
        )
        if found_block_quote_before_list and adj_ws is None and alt_adj_ws is not None:
            adj_ws = alt_adj_ws
        (
            whitespace_to_add,
            alt_adj_ws,
            ws_before_marker,
            indent_level,
        ) = ListBlockCreateNewHandler.__create_new_list_handle_whitespace(
            forced_container_whitespace,
            alt_adj_ws,
            ws_before_marker,
            indent_level,
            extracted_whitespace,
            adj_ws,
        )
        tabbed_whitespace_to_add = None
        tabbed_adjust = -1
        if "\t" in original_line:
            (
                tabbed_whitespace_to_add,
                tabbed_adjust,
            ) = ListBlockCreateNewHandler.__create_new_list_with_tab(
                position_marker, original_line, is_ulist, whitespace_to_add, index
            )

        other_create_token_fn = (
            ListBlockCreateNewHandler.__handle_list_block_unordered
            if is_ulist
            else ListBlockCreateNewHandler.__handle_list_block_ordered
        )
        new_token, new_stack = other_create_token_fn(
            position_marker,
            indent_level,
            tabbed_adjust,
            whitespace_to_add,
            tabbed_whitespace_to_add,
            ws_before_marker,
            ws_after_marker,
            index,
        )
        (
            new_container_level_tokens,
            adjusted_text_to_parse,
            requeue_line_info,
        ) = ListBlockCreateNewHandler.__post_list(
            parser_state,
            new_stack,
            new_token,
            position_marker.text_to_parse,
            remaining_whitespace,
            after_marker_ws_index,
            indent_level,
            current_container_blocks,
            position_marker,
            adj_ws,
            alt_adj_ws,
            container_depth,
        )
        assert new_container_level_tokens is not None
        container_level_tokens.extend(new_container_level_tokens)
        return True, adjusted_text_to_parse, requeue_line_info

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __calculate_create_adj_ws(
        adj_ws: Optional[str],
        position_marker: PositionMarker,
        parser_state: ParserState,
    ) -> Optional[str]:
        create_adj_ws = adj_ws
        POGGER.debug("adj_ws=>:$:<", create_adj_ws)
        if position_marker.index_number:
            POGGER.debug("adjusting for nested")
            POGGER.debug("afn>>$", parser_state.token_stack)
            search_index = parser_state.find_last_container_on_stack()
            if parser_state.token_stack[search_index].is_list:
                create_adj_ws = None
        POGGER.debug("create_adj_ws=$=", create_adj_ws)
        return create_adj_ws

    @staticmethod
    def __find_block_quote_before_list(
        parser_state: ParserState,
    ) -> Optional[BlockQuoteStackToken]:
        POGGER.debug_with_visible_whitespace(
            "parser_state.token_stack>$", parser_state.token_stack
        )
        found_block_quote_before_list = None
        token_stack_index = parser_state.find_last_container_on_stack()
        POGGER.debug_with_visible_whitespace("token_stack_index>$", token_stack_index)
        if parser_state.token_stack[token_stack_index].is_list:
            while token_stack_index > 0:
                if parser_state.token_stack[token_stack_index].is_block_quote:
                    found_block_quote_before_list = cast(
                        BlockQuoteStackToken,
                        parser_state.token_stack[token_stack_index],
                    )
                    break
                token_stack_index -= 1
        POGGER.debug_with_visible_whitespace(
            "found_block_quote_before_list>$", found_block_quote_before_list
        )
        return found_block_quote_before_list

    # pylint: disable=too-many-arguments
    @staticmethod
    def __create_new_list_handle_whitespace(
        forced_container_whitespace: Optional[str],
        alt_adj_ws: Optional[str],
        ws_before_marker: int,
        indent_level: int,
        extracted_whitespace: Optional[str],
        adj_ws: Optional[str],
    ) -> Tuple[Optional[str], Optional[str], int, int]:
        if forced_container_whitespace:
            whitespace_to_add: Optional[str] = forced_container_whitespace
            assert whitespace_to_add is not None
            if alt_adj_ws:
                whitespace_to_add += alt_adj_ws
            ws_before_marker += len(forced_container_whitespace)
            indent_level += len(forced_container_whitespace)
            assert alt_adj_ws is not None
            alt_adj_ws += forced_container_whitespace
        else:
            whitespace_to_add = extracted_whitespace if adj_ws is None else adj_ws
        return whitespace_to_add, alt_adj_ws, ws_before_marker, indent_level

    # pylint: enable=too-many-arguments
    @staticmethod
    def __create_new_list_with_tab(
        position_marker: PositionMarker,
        original_line: str,
        is_ulist: bool,
        whitespace_to_add: Optional[str],
        index: int,
    ) -> Tuple[Optional[str], int]:
        tabbed_whitespace_to_add = None
        tabbed_adjust = -1
        (
            tabbed_extract_spaces_index,
            tabbed_extract_spaces,
        ) = ParserHelper.extract_spaces(original_line, 0)
        POGGER.debug("tabbed_extract_spaces_index>:$:<", tabbed_extract_spaces_index)
        assert tabbed_extract_spaces_index is not None
        assert tabbed_extract_spaces is not None
        POGGER.debug("tabbed_extract_spaces>:$:<", tabbed_extract_spaces)
        POGGER.debug("text_to_parse>:$:<", position_marker.text_to_parse)
        POGGER.debug("index_number>:$:<", position_marker.index_number)
        detabbed_tabbed_extract_spaces = TabHelper.detabify_string(
            tabbed_extract_spaces
        )
        POGGER.debug(
            "detabbed_tabbed_extract_spaces>:$:<", detabbed_tabbed_extract_spaces
        )
        assert detabbed_tabbed_extract_spaces == whitespace_to_add
        if "\t" in tabbed_extract_spaces:
            tabbed_whitespace_to_add = tabbed_extract_spaces

        POGGER.debug("is_ulist>:$:<", is_ulist)

        # parse_index = position_marker.text_to_parse[position_marker.index_number]
        # POGGER.debug("parse_index>:$:<", parse_index)
        parse_index = 1 if is_ulist else index - position_marker.index_number + 1
        POGGER.debug("parse_index>:$:<", parse_index)

        new_index = position_marker.index_number + parse_index
        untabbed_marker = position_marker.text_to_parse[
            position_marker.index_number : new_index
        ]
        POGGER.debug("untabbed_marker>:$:<", untabbed_marker)
        tabbed_marker = original_line[
            tabbed_extract_spaces_index : tabbed_extract_spaces_index + parse_index
        ]
        POGGER.debug("tabbed_marker>:$:<", tabbed_marker)
        assert untabbed_marker == tabbed_marker

        tabbed_extract_spaces_index += len(tabbed_marker)
        POGGER.debug(
            "position_marker.text_to_parse[new_index:]>:$:<",
            position_marker.text_to_parse[new_index:],
        )
        POGGER.debug(
            "original_line[tabbed_extract_spaces_index:]>:$:<",
            original_line[tabbed_extract_spaces_index:],
        )
        if original_line[tabbed_extract_spaces_index] == "\t":
            POGGER.debug("new_index>:$:<", new_index)
            POGGER.debug(
                "tabbed_extract_spaces_index>:$:<", tabbed_extract_spaces_index
            )
            adj_string = TabHelper.detabify_string(
                original_line[tabbed_extract_spaces_index],
                additional_start_delta=new_index,
            )
            POGGER.debug("adj_string>:$:<", adj_string)
            tabbed_adjust = len(adj_string) - 1
            POGGER.debug("tabbed_adjust>:$:<", tabbed_adjust)

        return tabbed_whitespace_to_add, tabbed_adjust

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __post_list(
        parser_state: ParserState,
        new_stack: ListStackToken,
        new_token: ListStartMarkdownToken,
        line_to_parse: str,
        remaining_whitespace: int,
        after_marker_ws_index: int,
        indent_level: int,
        current_container_blocks: List[StackToken],
        position_marker: PositionMarker,
        adj_ws: Optional[str],
        alt_adj_ws: Optional[str],
        container_depth: int,
    ) -> Tuple[Optional[List[MarkdownToken]], Optional[str], Optional[RequeueLineInfo]]:
        """
        Handle the processing of the last part of the list.
        """
        (
            did_find,
            last_list_index,
        ) = LeafBlockProcessorParagraph.check_for_list_in_process(parser_state)
        if did_find:
            POGGER.debug(
                "list-in-process>>$",
                parser_state.token_stack[last_list_index],
            )
            (
                container_level_tokens,
                emit_li,
                requeue_line_info,
            ) = ListBlockCreateNewHandler.__close_required_lists_after_start(
                position_marker,
                parser_state,
                last_list_index,
                new_stack,
                new_token,
                current_container_blocks,
                container_depth,
            )
            if requeue_line_info:
                return [], None, requeue_line_info
        else:
            POGGER.debug(
                "NOT list-in-process>>$",
                parser_state.token_stack[last_list_index],
            )
            container_level_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state, was_forced=True
            )

        assert container_level_tokens is not None
        POGGER.debug("__post_list>>before>>$", container_level_tokens)
        if not did_find or not emit_li:
            POGGER.debug("__post_list>>adding>>$", new_token)
            parser_state.token_stack.append(new_stack)
            container_level_tokens.append(new_token)
        else:
            POGGER.debug("__post_list>>new list item>>")
            assert emit_li
            ListBlockCreateNewHandler.__post_list_use_new_list_item(
                parser_state,
                new_token,
                container_level_tokens,
                indent_level,
                position_marker,
                adj_ws,
                alt_adj_ws,
            )
        parser_state.set_no_para_start_if_empty()
        padded_spaces = ParserHelper.repeat_string(
            ParserHelper.space_character, remaining_whitespace
        )
        return (
            container_level_tokens,
            f"{padded_spaces}{line_to_parse[after_marker_ws_index:]}",
            None,
        )
        # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __post_list_use_new_list_item(
        parser_state: ParserState,
        new_token: ListStartMarkdownToken,
        container_level_tokens: List[MarkdownToken],
        indent_level: int,
        position_marker: PositionMarker,
        adj_ws: Optional[str],
        alt_adj_ws: Optional[str],
    ) -> None:
        POGGER.debug("instead of-->$", new_token)

        stack_index = len(parser_state.token_stack) - 1
        while stack_index and not parser_state.token_stack[stack_index].is_list:
            stack_index -= 1
        if stack_index != len(parser_state.token_stack) - 1:
            POGGER.debug("stack_index>$", stack_index)
            POGGER.debug("parser_state.token_stack>$", parser_state.token_stack)
            POGGER.debug(
                "len(parser_state.token_stack)>$", len(parser_state.token_stack) - 1
            )
            new_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=stack_index + 1,
                include_block_quotes=True,
            )
            POGGER.debug("new_tokens>$", new_tokens)
            POGGER.debug("parser_state.token_stack>$", parser_state.token_stack)
            POGGER.debug(
                "len(parser_state.token_stack)>$", len(parser_state.token_stack) - 1
            )
            container_level_tokens.extend(new_tokens)

        top_stack_item = parser_state.token_stack[-1]
        assert top_stack_item.is_list
        top_stack_list_token = cast(ListStackToken, top_stack_item)
        POGGER.debug("new_token>$", new_token)
        POGGER.debug("top_stack_item>$", top_stack_list_token)
        POGGER.debug(
            "top_stack_item.mmt>$", top_stack_list_token.matching_markdown_token
        )
        list_start_content = (
            new_token.list_start_content if new_token.is_ordered_list_start else ""
        )

        POGGER.debug("adj_ws-->:$:<", adj_ws)
        POGGER.debug("alt_adj_ws-->:$:<", alt_adj_ws)
        exws = (
            alt_adj_ws
            if adj_ws is None and alt_adj_ws is not None
            else new_token.extracted_whitespace
        )

        # Replace the "other" list start token with a new list item token.
        # The overwritting of the value of new_token is specifically called for.
        replacement_token = NewListItemMarkdownToken(
            indent_level,
            position_marker,
            exws,
            list_start_content,
        )
        top_stack_list_token.set_last_new_list_token(replacement_token)
        container_level_tokens.append(replacement_token)

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __close_required_lists_after_start(
        position_marker: PositionMarker,
        parser_state: ParserState,
        last_list_index: int,
        new_stack: ListStackToken,
        new_token: ListStartMarkdownToken,
        current_container_blocks: List[StackToken],
        container_depth: int,
    ) -> Tuple[
        Optional[List[MarkdownToken]], Optional[bool], Optional[RequeueLineInfo]
    ]:
        """
        After a list start, check to see if any others need closing.
        """
        POGGER.debug("list-in-process>>$", parser_state.token_stack[last_list_index])
        POGGER.debug(
            "list-in-process.token>>$",
            parser_state.token_stack[last_list_index].matching_markdown_token,
        )
        POGGER.debug("new_token>>$", new_token)
        (
            container_level_tokens,
            requeue_line_info,
        ) = parser_state.close_open_blocks_fn(
            parser_state,
            until_this_index=last_list_index + 1,
            caller_can_handle_requeue=True,
            requeue_reset=True,
        )
        if requeue_line_info:
            return None, None, requeue_line_info

        repeat_check, emit_li_token_instead_of_list_start_token = True, False

        POGGER.debug("token_stack>>$", parser_state.token_stack)
        if (
            not container_depth
            and len(parser_state.token_stack) > 1
            and parser_state.token_stack[1].is_block_quote
        ):
            extra_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=1,
                include_lists=True,
                include_block_quotes=True,
            )
            POGGER.debug("extra_tokens>>$", extra_tokens)
            container_level_tokens.extend(extra_tokens)
            POGGER.debug("token_stack>>$", parser_state.token_stack)
            repeat_check = False

        POGGER.debug("old-stack>>$<<", container_level_tokens)
        while repeat_check:
            (
                repeat_check,
                emit_li_token_instead_of_list_start_token,
                last_list_index,
            ) = ListBlockCreateNewHandler.__close_next_level_of_lists(
                position_marker,
                parser_state,
                new_stack,
                new_token,
                current_container_blocks,
                container_level_tokens,
                last_list_index,
                container_depth,
            )
        POGGER.debug("token_stack>>$", parser_state.token_stack)
        POGGER.debug("container_level_tokens>>$", container_level_tokens)
        POGGER.debug(
            "emit_li_token_instead_of_list_start_token>>$",
            emit_li_token_instead_of_list_start_token,
        )
        return container_level_tokens, emit_li_token_instead_of_list_start_token, None

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __close_next_level_of_lists(
        position_marker: PositionMarker,
        parser_state: ParserState,
        new_stack: ListStackToken,
        new_token: ListStartMarkdownToken,
        current_container_blocks: List[StackToken],
        container_level_tokens: List[MarkdownToken],
        last_list_index: int,
        container_depth: int,
    ) -> Tuple[bool, bool, int]:
        POGGER.debug("start")

        (
            do_not_emit,
            emit_li_token_instead_of_list_start_token,
            extra_tokens,
        ) = ListBlockCreateNewHandler.__are_list_starts_equal(
            position_marker,
            parser_state,
            last_list_index,
            new_stack,
            current_container_blocks,
            container_depth,
        )
        POGGER.debug("extra_tokens>>$", extra_tokens)
        POGGER.debug(
            "emit_li_token_instead_of_list_start_token>>$",
            emit_li_token_instead_of_list_start_token,
        )
        POGGER.debug("do_not_emit>>$", do_not_emit)
        container_level_tokens.extend(extra_tokens)
        repeat_check = False
        if do_not_emit:
            (
                last_list_index,
                repeat_check,
            ) = ListBlockCreateNewHandler.__close_next_level_of_lists_do_not_emit(
                parser_state,
                new_stack,
                new_token,
                current_container_blocks,
                emit_li_token_instead_of_list_start_token,
                container_level_tokens,
                container_depth,
            )
        else:
            POGGER.debug("post_list>>close open blocks and emit")
            (
                repeat_check,
                last_list_index,
            ) = ListBlockCreateNewHandler.__close_next_level_of_lists_do_emit(
                parser_state,
                last_list_index,
                container_level_tokens,
                new_stack,
                new_token,
            )
        return repeat_check, emit_li_token_instead_of_list_start_token, last_list_index

    @staticmethod
    def __close_next_level_of_lists_do_emit(
        parser_state: ParserState,
        last_list_index: int,
        container_level_tokens: List[MarkdownToken],
        new_stack: ListStackToken,
        new_token: ListStartMarkdownToken,
    ) -> Tuple[bool, int]:
        close_tokens, _ = parser_state.close_open_blocks_fn(
            parser_state,
            until_this_index=last_list_index,
            include_lists=True,
            include_block_quotes=True,
        )
        container_level_tokens.extend(close_tokens)

        (
            did_find,
            last_list_index,
        ) = LeafBlockProcessorParagraph.check_for_list_in_process(parser_state)
        POGGER.debug(
            "did_find>>$--last_list_index--$",
            did_find,
            last_list_index,
        )
        repeat_check = False
        if did_find:
            last_list_stack_token = cast(
                ListStackToken, parser_state.token_stack[last_list_index]
            )
            POGGER.debug(
                "ARE-EQUAL>>stack>>$>>new>>$",
                last_list_stack_token,
                new_stack,
            )
            POGGER.debug(
                "ARE-EQUAL>>stack>>$>>new>>$",
                last_list_stack_token.matching_markdown_token,
                new_token,
            )
            last_list_markdown_token = cast(
                ListStartMarkdownToken,
                last_list_stack_token.matching_markdown_token,
            )
            old_indent = 2
            if last_list_markdown_token.is_ordered_list_start:
                old_indent += len(last_list_markdown_token.list_start_content)
            POGGER.debug(
                "new_token.column_number($) <= old_indent($)",
                new_token.column_number,
                old_indent,
            )
            repeat_check = new_token.column_number <= last_list_stack_token.indent_level
            POGGER.debug(
                "repeat_check($) = new_token.column_number($) - last_list_stack_token.indent_level($)",
                repeat_check,
                new_token.column_number,
                last_list_stack_token.indent_level,
            )
        return repeat_check, last_list_index

    @staticmethod
    def __close_next_level_of_lists_do_not_emit(
        parser_state: ParserState,
        new_stack: ListStackToken,
        new_token: ListStartMarkdownToken,
        current_container_blocks: List[StackToken],
        emit_li_token_instead_of_list_start_token: bool,
        container_level_tokens: List[MarkdownToken],
        container_depth: int,
    ) -> Tuple[int, bool]:
        POGGER.debug("post_list>>don't emit")
        (
            did_find,
            last_list_index,
        ) = LeafBlockProcessorParagraph.check_for_list_in_process(parser_state)
        assert last_list_index > 0
        last_list_index_token = cast(
            ListStackToken, parser_state.token_stack[last_list_index]
        )
        POGGER.debug("parser_state.token_stack>>$", parser_state.token_stack)
        POGGER.debug(
            "did_find>>$--last_list_index--$",
            did_find,
            last_list_index,
        )
        assert did_find
        POGGER.debug(
            "ARE-EQUAL>>stack>>$>>new>>$",
            last_list_index_token,
            new_stack,
        )
        repeat_check = not (
            last_list_index_token.type_name == new_stack.type_name
            or new_stack.start_index > last_list_index_token.start_index
        )
        POGGER.debug("current_container_blocks>>$", current_container_blocks)
        POGGER.debug(
            "emit_li_token_instead_of_list_start_token>:$:  repeat_check:$:",
            emit_li_token_instead_of_list_start_token,
            repeat_check,
        )

        if not repeat_check and not emit_li_token_instead_of_list_start_token:
            ListBlockCreateNewHandler.__close_next_level_of_lists_do_not_emit_cleanup(
                parser_state,
                last_list_index_token,
                new_token,
                last_list_index,
                container_level_tokens,
                container_depth,
            )
        return last_list_index, repeat_check

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __close_next_level_of_lists_do_not_emit_cleanup(
        parser_state: ParserState,
        last_list_index_token: ListStackToken,
        new_token: ListStartMarkdownToken,
        last_list_index: int,
        container_level_tokens: List[MarkdownToken],
        container_depth: int,
    ) -> None:
        parent_list_indent = last_list_index_token.indent_level
        POGGER.debug("parent_list_indent>>$", parent_list_indent)
        new_token_column_number = new_token.column_number
        POGGER.debug("new_token_column_number>>$", new_token_column_number)
        assert parser_state.original_line_to_parse is not None
        intermediate_line_content = parser_state.original_line_to_parse[
            parent_list_indent : new_token_column_number - 1
        ]
        POGGER.debug("intermediate_line_content:$:", intermediate_line_content)
        if ">" not in intermediate_line_content:
            close_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=last_list_index,
                include_block_quotes=True,
            )
            if close_tokens:
                container_level_tokens.extend(close_tokens)
                assert not container_depth
                list_token = cast(
                    ListStartMarkdownToken,
                    last_list_index_token.matching_markdown_token,
                )
                delta = new_token.column_number - list_token.column_number
                new_token.set_extracted_whitespace(
                    "".rjust(delta, ParserHelper.space_character)
                )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __are_list_starts_equal(
        position_marker: PositionMarker,
        parser_state: ParserState,
        last_list_index: int,
        new_stack: ListStackToken,
        current_container_blocks: List[StackToken],
        container_depth: int,
    ) -> Tuple[bool, bool, List[MarkdownToken]]:
        """
        Check to see if the list starts are equal, and hence a continuation of
        the current list.
        """

        POGGER.debug(
            "ARE-EQUAL>>stack>>$>>new>>$",
            parser_state.token_stack[last_list_index],
            new_stack,
        )
        if parser_state.token_stack[last_list_index] == new_stack:
            balancing_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=last_list_index,
                include_block_quotes=True,
            )
            return True, True, balancing_tokens

        document_token_index = len(parser_state.token_document) - 1
        while document_token_index >= 0 and not (
            parser_state.token_document[document_token_index].is_any_list_token
        ):
            document_token_index -= 1
        assert document_token_index >= 0
        document_list_token = cast(
            ListStartMarkdownToken, parser_state.token_document[document_token_index]
        )
        last_list_stack_token = cast(
            ListStackToken, parser_state.token_stack[last_list_index]
        )

        POGGER.debug("parser_state.token_document=$", parser_state.token_document)
        POGGER.debug("parser_state.token_stack=$", parser_state.token_stack)
        POGGER.debug("ARE-EQUAL>>Last_List_token=$", document_list_token)
        old_start_index, old_last_marker_character, current_start_index = (
            document_list_token.indent_level,
            last_list_stack_token.list_character[-1],
            new_stack.ws_before_marker,
        )
        POGGER.debug(
            "old>>$>>$",
            last_list_stack_token.extra_data,
            old_last_marker_character,
        )
        POGGER.debug("new>>$>>$", new_stack.extra_data, new_stack.list_character[-1])
        return ListBlockCreateNewHandler.__implement_based_on_equality(
            parser_state,
            position_marker,
            last_list_stack_token,
            old_last_marker_character,
            new_stack,
            current_start_index,
            old_start_index,
            current_container_blocks,
            container_depth,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __implement_based_on_equality(
        parser_state: ParserState,
        position_marker: PositionMarker,
        last_list_stack_token: ListStackToken,
        old_last_marker_character: str,
        new_stack: ListStackToken,
        current_start_index: int,
        old_start_index: int,
        current_container_blocks: List[StackToken],
        container_depth: int,
    ) -> Tuple[bool, bool, List[MarkdownToken]]:
        ## Determine if the new start is within the range of the old stack.  If so
        ## AND some combination of the IF statement, then switch.
        ## i.e. a + at col 1 followed by a - at column 1 is a new list
        ## i.e. a + at col 1 followed by a - at column 3 is a new sublist
        last_list_indent = last_list_stack_token.indent_level
        if last_list_stack_token.last_new_list_token:
            last_list_indent = last_list_stack_token.last_new_list_token.indent_level

        POGGER.debug(
            "position_marker.index_number>>$ >= xx>>$",
            position_marker,
            last_list_indent,
        )
        is_indented_enough = position_marker.index_number >= last_list_indent
        POGGER.debug("is_indented_enough>>$", is_indented_enough)
        if (
            is_indented_enough
            or old_last_marker_character == new_stack.list_character[-1]
            and last_list_stack_token.type_name == new_stack.type_name
        ):
            balancing_tokens: List[MarkdownToken] = []
            POGGER.debug("new_stack>$<", new_stack)
            POGGER.debug("new_stack>$<", new_stack.matching_markdown_token)
            POGGER.debug("old_stack>$<", last_list_stack_token)
            POGGER.debug(
                "old_stack>$<",
                last_list_stack_token.matching_markdown_token,
            )
            emit_li_token_instead_of_list_start_token = (
                ListBlockCreateNewHandler.__process_eligible_list_start(
                    parser_state,
                    balancing_tokens,
                    current_start_index,
                    old_start_index,
                    current_container_blocks,
                    new_stack,
                    last_list_stack_token,
                )
            )
            return True, emit_li_token_instead_of_list_start_token, balancing_tokens

        POGGER.debug("SUBLIST WITH DIFFERENT")
        POGGER.debug("container_depth:$:", container_depth)
        POGGER.debug("are_list_starts_equal>>ELIGIBLE!!!")
        POGGER.debug(
            "are_list_starts_equal>>current_start_index>>$>>old_start_index>>$",
            current_start_index,
            old_start_index,
        )
        empty_balancing_tokens: List[MarkdownToken] = []
        return current_start_index >= old_start_index, False, empty_balancing_tokens

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_eligible_list_start(
        parser_state: ParserState,
        balancing_tokens: List[MarkdownToken],
        current_start_index: int,
        old_start_index: int,
        current_container_blocks: List[StackToken],
        new_stack: StackToken,
        last_list_stack_token: ListStackToken,
    ) -> bool:
        POGGER.debug("are_list_starts_equal>>ELIGIBLE!!!")
        POGGER.debug("current_container_blocks>>$", current_container_blocks)
        POGGER.debug(
            "are_list_starts_equal>>current_start_index>>$>>old_start_index>>$",
            current_start_index,
            old_start_index,
        )
        POGGER.debug("last_list_stack_token>>$", last_list_stack_token)
        assert last_list_stack_token is not None
        last_list_markdown_token = cast(
            ListStartMarkdownToken, last_list_stack_token.matching_markdown_token
        )
        POGGER.debug("last_list_markdown_token>>$", last_list_markdown_token)

        last_list_indent = last_list_markdown_token.indent_level
        if last_list_stack_token.last_new_list_token:
            last_list_indent = last_list_stack_token.last_new_list_token.indent_level

        POGGER.debug(
            "current_start_index>>$ >= last_list_indent>>$",
            last_list_stack_token,
            last_list_indent,
        )
        if current_start_index >= last_list_indent:
            return False

        POGGER.debug("current_container_blocks>>$", current_container_blocks)
        if len(current_container_blocks) > 1:
            POGGER.debug("current_container_blocks-->$", parser_state.token_stack)
            allow_list_removal = ListBlockCanCloseHelper.calculate_can_remove_list(
                parser_state, current_start_index
            )
            POGGER.debug("allow_list_removal-->$", allow_list_removal)
            ListBlockCanCloseHelper.close_required_lists(
                parser_state,
                allow_list_removal,
                balancing_tokens,
                new_stack,
            )

        return True

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_list_block_unordered(
        position_marker: PositionMarker,
        indent_level: int,
        tabbed_adjust: int,
        extracted_whitespace: Optional[str],
        tabbed_whitespace_to_add: Optional[str],
        ws_before_marker: int,
        ws_after_marker: int,
        index: int,
    ) -> Tuple[ListStartMarkdownToken, ListStackToken]:
        # This is done to allow for this function and __handle_list_block_ordered
        # to be called using the same pattern.
        _ = index

        assert extracted_whitespace is not None
        new_token = UnorderedListStartMarkdownToken(
            position_marker.text_to_parse[position_marker.index_number],
            indent_level,
            tabbed_adjust,
            extracted_whitespace,
            tabbed_whitespace_to_add,
            position_marker,
        )

        POGGER.debug("unordered-token-->$", new_token)

        return new_token, UnorderedListStackToken(
            indent_level,
            position_marker.text_to_parse[position_marker.index_number],
            ws_before_marker,
            ws_after_marker,
            position_marker.index_number,
            new_token,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_list_block_ordered(
        position_marker: PositionMarker,
        indent_level: int,
        tabbed_adjust: int,
        extracted_whitespace: Optional[str],
        tabbed_whitespace_to_add: Optional[str],
        ws_before_marker: int,
        ws_after_marker: int,
        index: int,
    ) -> Tuple[ListStartMarkdownToken, ListStackToken]:
        assert extracted_whitespace is not None
        new_token = OrderedListStartMarkdownToken(
            position_marker.text_to_parse[index],
            position_marker.text_to_parse[position_marker.index_number : index],
            indent_level,
            tabbed_adjust,
            extracted_whitespace,
            tabbed_whitespace_to_add,
            position_marker,
        )

        POGGER.debug("ordered-token-->$", new_token)

        return new_token, OrderedListStackToken(
            indent_level,
            position_marker.text_to_parse[position_marker.index_number : index + 1],
            ws_before_marker,
            ws_after_marker,
            position_marker.index_number,
            new_token,
        )

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
