"""
Module to provide detection of the list starts.
"""

import logging
import string
from typing import Optional, Tuple, cast

from pymarkdown.leaf_blocks.thematic_leaf_block_processor import (
    ThematicLeafBlockProcessor,
)
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.stack_token import ListStackToken
from pymarkdown.tab_helper import TabHelper
from pymarkdown.tokens.container_markdown_token import ListStartMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class ListBlockStartsHelper:
    """
    Class to provide detection of the list starts.
    """

    __ulist_start_characters = "-+*"
    __olist_start_characters = ".)"

    # pylint: disable=too-many-arguments
    @staticmethod
    def is_ulist_start(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        skip_whitespace_check: bool,
        adj_ws: Optional[str] = None,
    ) -> Tuple[bool, int, Optional[int], Optional[int]]:
        """
        Determine if we have the start of an un-numbered list.
        """
        POGGER.debug("is_ulist_start>>pre>>")
        POGGER.debug("is_ulist_start>>start_index>>$<<", start_index)
        POGGER.debug("is_ulist_start>>adj_ws>>$<<", adj_ws)
        POGGER.debug("is_ulist_start>>extracted_whitespace>>$<<", extracted_whitespace)
        (
            adj_ws,
            parent_indent,
        ) = ListBlockStartsHelper.__adjust_whitespace_for_nested_lists(
            parser_state,
            extracted_whitespace if adj_ws is None else adj_ws,
            line_to_parse,
            start_index,
        )

        assert adj_ws is not None
        POGGER.debug("skip_whitespace_check>>$", skip_whitespace_check)
        POGGER.debug("len(adj_ws)>>$", len(adj_ws))
        POGGER.debug("parent_indent>>$", parent_indent)

        if (
            TabHelper.is_length_less_than_or_equal_to(adj_ws, 3 + parent_indent)
            or skip_whitespace_check
        ):
            assert extracted_whitespace is not None
            adj_extracted_whitespace = extracted_whitespace
            if parent_indent:
                adj_extracted_whitespace = extracted_whitespace[parent_indent:]
            is_start = ListBlockStartsHelper.__is_start_ulist(
                line_to_parse, start_index, adj_extracted_whitespace
            )
        else:
            is_start = False
        if is_start:
            (
                is_start,
                after_all_whitespace_index,
            ) = ListBlockStartsHelper.__is_start_phase_one(
                parser_state, line_to_parse, start_index, False
            )
        else:
            after_all_whitespace_index = -1
        if is_start:
            is_start = ListBlockStartsHelper.__is_start_phase_two(
                parser_state,
                line_to_parse[start_index],
                True,
                False,
                after_all_whitespace_index,
                line_to_parse,
                start_index,
            )

        return is_start, after_all_whitespace_index, start_index, 0
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def is_olist_start(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        skip_whitespace_check: bool,
        adj_ws: Optional[str] = None,
    ) -> Tuple[bool, int, Optional[int], Optional[int]]:
        """
        Determine if we have the start of a numbered or ordered list.
        """

        POGGER.debug("is_olist_start>>pre>>")
        POGGER.debug("is_olist_start>>start_index>>$<<", start_index)
        POGGER.debug("is_olist_start>>adj_ws>>$<<", adj_ws)
        POGGER.debug("is_olist_start>>extracted_whitespace>>$<<", extracted_whitespace)
        (
            adj_ws,
            parent_indent,
        ) = ListBlockStartsHelper.__adjust_whitespace_for_nested_lists(
            parser_state,
            extracted_whitespace if adj_ws is None else adj_ws,
            line_to_parse,
            start_index,
        )
        POGGER.debug("after_adjust>>ws=$=", adj_ws)
        POGGER.debug("after_adjust>>parent_indent=$=", parent_indent)

        assert adj_ws is not None

        POGGER.debug("skip_whitespace_check>>$", skip_whitespace_check)
        POGGER.debug("len(adj_ws)>>$", len(adj_ws))

        if (
            TabHelper.is_length_less_than_or_equal_to(adj_ws, 3 + parent_indent)
            or skip_whitespace_check
        ):
            (
                is_start,
                index,
                number_of_digits,
                is_not_one,
            ) = ListBlockStartsHelper.__is_start_olist(line_to_parse, start_index)
        else:
            is_start, index, number_of_digits, is_not_one = False, None, None, False
        if is_start:
            assert index is not None
            assert is_not_one is not None
            (
                is_start,
                after_all_whitespace_index,
            ) = ListBlockStartsHelper.__is_start_phase_one(
                parser_state, line_to_parse, index, is_not_one
            )
        else:
            after_all_whitespace_index = -1
        if is_start:
            assert index is not None
            assert is_not_one is not None
            is_start = ListBlockStartsHelper.__is_start_phase_two(
                parser_state,
                line_to_parse[index],
                False,
                is_not_one,
                after_all_whitespace_index,
                line_to_parse,
                start_index,
            )

        return is_start, after_all_whitespace_index, index, number_of_digits

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_whitespace_for_nested_lists(
        parser_state: ParserState,
        adj_ws: Optional[str],
        line_to_parse: str,
        start_index: int,
    ) -> Tuple[Optional[str], int]:
        assert adj_ws is not None
        (
            child_list_token,
            parent_list_token,
        ) = ListBlockStartsHelper.__determine_child_and_parent_tokens(parser_state)
        POGGER.debug("len(adj_ws)>>$", len(adj_ws))

        if child_list_token and parent_list_token:
            parent_indent, child_indent = (
                parent_list_token.indent_level,
                child_list_token.indent_level,
            )
            POGGER.debug("parent_indent>>$", parent_indent)
            POGGER.debug("child_indent>>$", child_indent)
            if len(adj_ws) > parent_indent and len(adj_ws) < child_indent:
                adj_ws = adj_ws[parent_indent:]
        elif child_list_token:
            POGGER.debug("current_start>>$", child_list_token.matching_markdown_token)
            POGGER.debug(
                "current_start.last_new_list_token>>$",
                child_list_token.last_new_list_token,
            )
            POGGER.debug("line_to_parse>>:$:", line_to_parse)
            POGGER.debug("start_index>>$", start_index)

            indent_level = (
                child_list_token.last_new_list_token.indent_level
                if child_list_token.last_new_list_token
                else child_list_token.indent_level
            )
            parent_indent = (
                child_list_token.indent_level if start_index >= indent_level else 0
            )
        else:
            parent_indent = 0
        return adj_ws, parent_indent

    @staticmethod
    def __is_start_phase_one(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        is_not_one: bool,
    ) -> Tuple[bool, int]:
        start_index += 1
        line_to_parse_size = len(line_to_parse)
        after_all_whitespace_index, _ = ParserHelper.extract_spaces(
            line_to_parse, start_index
        )
        assert after_all_whitespace_index is not None
        POGGER.debug(
            "after_all_whitespace_index>>$>>len>>$",
            after_all_whitespace_index,
            line_to_parse_size,
        )
        at_end_of_line = after_all_whitespace_index == line_to_parse_size
        POGGER.debug("at_end_of_line>>$", at_end_of_line)

        is_in_paragraph = parser_state.token_stack[-1].is_paragraph
        is_paragraph_in_list = (
            parser_state.token_stack[-2].is_list if is_in_paragraph else False
        )

        is_block_within_list = False
        if (
            parser_state.token_stack[-1].is_fenced_code_block
            or parser_state.token_stack[-1].is_html_block
        ) and parser_state.token_stack[-2].is_list:
            POGGER.debug("start_index>>$", start_index)
            matching_list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[-2].matching_markdown_token,
            )
            POGGER.debug("matching_list_token>>$", matching_list_token)
            POGGER.debug(
                "matching_list_token.indent_level>>$", matching_list_token.indent_level
            )
            is_block_within_list = start_index > matching_list_token.indent_level
            POGGER.debug("is_block_within_list>>$", is_block_within_list)

        is_paragraph_continuation = (
            is_in_paragraph
            and not is_paragraph_in_list
            and (at_end_of_line or is_not_one)
        )
        is_start = (
            not is_paragraph_continuation
            and not is_block_within_list
            and (
                ParserHelper.is_character_at_index_whitespace(
                    line_to_parse, start_index
                )
                or ((start_index) == line_to_parse_size)
            )
        )
        return is_start, after_all_whitespace_index

    # pylint: disable=too-many-arguments
    @staticmethod
    def __is_start_phase_two(
        parser_state: ParserState,
        xx_seq: str,
        is_unordered_list: bool,
        is_not_one: bool,
        after_all_whitespace_index: int,
        line_to_parse: str,
        start_index: int,
    ) -> bool:
        (is_in_paragraph, at_end_of_line) = (
            parser_state.token_stack[-1].is_paragraph,
            (after_all_whitespace_index == len(line_to_parse)),
        )

        if is_in_paragraph:
            (
                is_first_item_in_list,
                is_sub_list,
            ) = ListBlockStartsHelper.__calculate_starts_within_paragraph(
                parser_state, line_to_parse, start_index, is_unordered_list, xx_seq
            )
        else:
            is_first_item_in_list, is_sub_list = False, False

        POGGER.debug(
            "is_in_para>>$(>>EOL>$>>is_not_one>$)>>is_first>$>>is_sub_list>$",
            is_in_paragraph,
            at_end_of_line,
            is_not_one,
            is_first_item_in_list,
            is_sub_list,
        )
        return not (
            is_in_paragraph
            and (at_end_of_line or is_not_one)
            and is_first_item_in_list
            and is_sub_list
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __is_start_ulist(
        line_to_parse: str, start_index: int, extracted_whitespace: Optional[str]
    ) -> bool:
        is_start = ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, ListBlockStartsHelper.__ulist_start_characters
        )

        # Thematic breaks have precedence, so stop a list start if we find one.
        if is_start:
            is_break, _ = ThematicLeafBlockProcessor.is_thematic_break(
                line_to_parse, start_index, extracted_whitespace
            )
            is_start = is_start and not is_break
        return is_start

    @staticmethod
    def __is_start_olist(
        line_to_parse: str, start_index: int
    ) -> Tuple[bool, Optional[int], Optional[int], Optional[bool]]:
        is_start = ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, string.digits
        )
        if is_start:
            index, olist_index_number = ParserHelper.collect_while_one_of_characters(
                line_to_parse, start_index, string.digits
            )
            assert olist_index_number is not None
            assert index is not None
            number_of_digits = len(olist_index_number)

            POGGER.debug("olist?$<<count>>$<<", olist_index_number, number_of_digits)
            is_not_one = olist_index_number != "1"
            is_start = (
                number_of_digits <= 9
                and ParserHelper.is_character_at_index_one_of(
                    line_to_parse, index, ListBlockStartsHelper.__olist_start_characters
                )
            )
        else:
            index, number_of_digits, is_not_one = None, None, None

        POGGER.debug("is_olist_start>>$", is_start)
        return is_start, index, number_of_digits, is_not_one

    @staticmethod
    def __determine_child_and_parent_tokens(
        parser_state: ParserState,
    ) -> Tuple[Optional[ListStackToken], Optional[ListStackToken]]:
        child_list_token, parent_list_token = None, None
        if parser_state.token_stack[-1].is_list:
            child_list_token = cast(ListStackToken, parser_state.token_stack[-1])
            if (
                len(parser_state.token_stack) > 1
                and parser_state.token_stack[-2].is_list
            ):
                parent_list_token = cast(ListStackToken, parser_state.token_stack[-2])
        elif len(parser_state.token_stack) > 1 and parser_state.token_stack[-2].is_list:
            child_list_token = cast(ListStackToken, parser_state.token_stack[-2])
            if (
                len(parser_state.token_stack) > 2
                and parser_state.token_stack[-3].is_list
            ):
                parent_list_token = cast(ListStackToken, parser_state.token_stack[-3])
        POGGER.debug("child_list_token>>$", child_list_token)
        POGGER.debug("parent_list_token>>$", parent_list_token)
        return child_list_token, parent_list_token

    @staticmethod
    def __calculate_starts_within_paragraph(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        is_unordered_list: bool,
        xx_seq: str,
    ) -> Tuple[bool, bool]:
        is_first_item_in_list = True
        if not parser_state.token_stack[-2].is_list:
            POGGER.debug("top of stack is not list>>$", parser_state.token_stack[-2])
        else:
            list_stack_token = cast(ListStackToken, parser_state.token_stack[-2])
            if is_unordered_list and list_stack_token.is_ordered_list:
                POGGER.debug("top of stack is ordered list>>$", list_stack_token)
            elif xx_seq != list_stack_token.list_character[-1]:
                POGGER.debug(
                    "xx>>$!=$",
                    line_to_parse[start_index],
                    list_stack_token.list_character,
                )
            else:
                is_first_item_in_list = start_index >= list_stack_token.indent_level
                POGGER.debug(
                    "start_index>>$>=$",
                    start_index,
                    list_stack_token.indent_level,
                )
        POGGER.debug("is_first_item_in_list>>$", is_first_item_in_list)

        is_sub_list = False
        if parser_state.token_stack[-2].is_list:
            list_token = cast(ListStackToken, parser_state.token_stack[-2])
            is_sub_list = start_index >= list_token.indent_level

        return is_first_item_in_list, is_sub_list
