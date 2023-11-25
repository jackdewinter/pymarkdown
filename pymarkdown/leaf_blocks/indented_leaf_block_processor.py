"""
Module to provide processing for indented leaf blocks.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.indented_code_block_markdown_token import (
    IndentedCodeBlockMarkdownToken,
)
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import IndentedCodeBlockStackToken, ListStackToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods


class IndentedLeafBlockProcessor:
    """
    Class to provide processing for indented leaf blocks.
    """

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def parse_indented_code_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        removed_chars_at_start: Optional[int],
        last_block_quote_index: int,
        original_line: str,
    ) -> List[MarkdownToken]:
        """
        Handle the parsing of an indented code block
        """

        new_tokens: List[MarkdownToken] = []

        assert extracted_whitespace is not None
        assert removed_chars_at_start is not None
        if (
            TabHelper.is_length_greater_than_or_equal_to(
                extracted_whitespace, 4, start_index=removed_chars_at_start
            )
            and not parser_state.token_stack[-1].is_paragraph
        ):
            # POGGER.debug(
            #     "parse_indented_code_block>>start",
            # )
            # POGGER.debug("removed_chars_at_start>:$:<", removed_chars_at_start)
            # POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
            # POGGER.debug(
            #     "position_marker.text_to_parse>:$:<", position_marker.text_to_parse
            # )
            # POGGER.debug(
            #     "position_marker.text_to_parse[index_number=$]>:$:<",
            #     position_marker.index_number,
            #     position_marker.text_to_parse[position_marker.index_number :],
            # )
            # POGGER.debug("original_line>:$:<", original_line)

            indented_text = position_marker.text_to_parse[
                position_marker.index_number :
            ]

            last_block_stack_index = parser_state.find_last_block_quote_on_stack()
            is_in_block_quote = last_block_stack_index > 0
            POGGER.debug("is_in_block_quote>:$:<", is_in_block_quote)

            last_list_stack_index = parser_state.find_last_list_block_on_stack()
            is_in_list = last_list_stack_index > 0
            POGGER.debug("is_in_list>:$:<", is_in_list)

            tabified_extracted_space: Optional[str] = None
            xx_extracted_space, xx_left_over, adjust_block_quote_indent = (
                None,
                None,
                False,
            )
            if ParserHelper.tab_character in original_line:
                (
                    tabified_extracted_space,
                    xx_extracted_space,
                    xx_left_over,
                    adjust_block_quote_indent,
                ) = IndentedLeafBlockProcessor.__parse_indented_code_block_with_tab(
                    parser_state,
                    position_marker,
                    is_in_list,
                    is_in_block_quote,
                    original_line,
                    last_block_stack_index,
                    last_list_stack_index,
                )

            IndentedLeafBlockProcessor.__process_indented_code_block(
                parser_state,
                position_marker,
                new_tokens,
                tabified_extracted_space,
                original_line,
                xx_extracted_space,
                xx_left_over,
                adjust_block_quote_indent,
                last_block_quote_index,
                extracted_whitespace,
                indented_text,
            )
        else:
            POGGER.debug(
                "parse_indented_code_block>>not eligible",
            )
        return new_tokens

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __parse_indented_code_block_with_tab_list_list(
        parser_state: ParserState, original_line: str, last_list_index: int
    ) -> Tuple[ListStartMarkdownToken, str, int]:
        last_list_token = cast(
            ListStartMarkdownToken,
            parser_state.token_stack[last_list_index].matching_markdown_token,
        )
        last_list_lead_spaces = last_list_token.leading_spaces
        assert last_list_lead_spaces is not None
        POGGER.debug("last_list_lead_spaces>:$:<", last_list_lead_spaces)
        POGGER.debug("original_line>:$:<", original_line)
        lead_space_last_line_index = last_list_lead_spaces.rfind("\n")
        if lead_space_last_line_index != -1:
            last_list_lead_spaces = last_list_lead_spaces[
                lead_space_last_line_index + 1 :
            ]
            POGGER.debug("last_block_quote_lead_spaces>:$:<", last_list_lead_spaces)

        lead_space_len = len(last_list_lead_spaces)
        POGGER.debug("lead_space_len>:$:<", lead_space_len)
        return last_list_token, last_list_lead_spaces, lead_space_len

    # pylint: disable=too-many-locals
    @staticmethod
    def __parse_indented_code_block_with_tab_list(
        parser_state: ParserState,
        position_marker: PositionMarker,
        original_line: str,
        last_list_index: int,
    ) -> Tuple[Optional[str], Optional[str], Optional[str], bool]:
        (
            last_list_token,
            last_list_lead_spaces,
            lead_space_len,
        ) = IndentedLeafBlockProcessor.__parse_indented_code_block_with_tab_list_list(
            parser_state, original_line, last_list_index
        )

        _, ex_space = ParserHelper.extract_spaces(position_marker.text_to_parse, 0)
        # POGGER.debug("after_space_index>:$:<", after_space_index)
        # POGGER.debug("ex_space>:$:<", ex_space)
        assert ex_space is not None
        assert len(ex_space) >= 4
        was_indented = not parser_state.token_stack[-2].is_document
        fex_space, fex_space_index, split_tab = TabHelper.find_tabified_string(
            original_line,
            position_marker.text_to_parse,
            use_proper_traverse=True,
            reconstruct_prefix=last_list_lead_spaces,
            was_indented=was_indented,
        )

        indent_used = 0
        extra_index = 0
        if split_tab:
            extra_index = lead_space_len
            while (
                indent_used < len(last_list_lead_spaces)
                and fex_space[indent_used] != "\t"
            ):
                indent_used += 1
        else:
            detab_fex_space = TabHelper.detabify_string(fex_space, fex_space_index)
            assert detab_fex_space == position_marker.text_to_parse

        keep_going = True
        search_index = 1
        while keep_going:
            ex_part = fex_space[indent_used : indent_used + search_index]
            detabbed_ex_part = TabHelper.detabify_string(
                ex_part, fex_space_index + extra_index
            )
            keep_going = (
                len(detabbed_ex_part) < len(fex_space) and len(detabbed_ex_part) < 4
            )
            if keep_going:
                search_index += 1
        xx_extracted_space = ex_part
        xx_left_over = fex_space[indent_used + search_index :]
        assert original_line.endswith(fex_space)
        xx_dd = (
            original_line[:indent_used]
            if split_tab
            else original_line[: -(len(fex_space))]
        )
        last_list_token.remove_last_leading_space()
        last_list_token.add_leading_spaces(xx_dd)
        return None, xx_extracted_space, xx_left_over, False

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __parse_indented_code_block_with_tab(
        parser_state: ParserState,
        position_marker: PositionMarker,
        is_in_list: bool,
        is_in_block_quote: bool,
        original_line: str,
        last_block_quote_index: int,
        last_list_index: int,
    ) -> Tuple[Optional[str], Optional[str], Optional[str], bool]:
        if not is_in_list and not is_in_block_quote:
            next_character = position_marker.text_to_parse[position_marker.index_number]
            next_character_index = original_line.find(next_character)
            assert next_character_index != -1
            return (
                original_line[:next_character_index],
                None,
                None,
                False,
            )

        # Note not handling lists yet
        # assert is_in_block_quote

        if last_list_index > last_block_quote_index:
            return IndentedLeafBlockProcessor.__parse_indented_code_block_with_tab_list(
                parser_state, position_marker, original_line, last_list_index
            )
        (
            last_block_quote_lead_spaces,
            adj_lead_space_len,
            adjust_block_quote_indent,
        ) = IndentedLeafBlockProcessor.__get_indented_block_with_tab_quote_properties(
            parser_state, last_block_quote_index, original_line
        )

        lead_space_len = len(last_block_quote_lead_spaces)
        POGGER.debug("lead_space_len>:$:<", lead_space_len)
        after_space_index, ex_space = ParserHelper.extract_spaces(
            original_line, lead_space_len + adj_lead_space_len
        )
        return IndentedLeafBlockProcessor.__parse_indented_code_block_with_tab_complete(
            after_space_index,
            ex_space,
            lead_space_len,
            original_line,
            adjust_block_quote_indent,
        )

    # pylint: enable=too-many-arguments
    @staticmethod
    def __parse_indented_code_block_with_tab_complete(
        after_space_index: Optional[int],
        ex_space: Optional[str],
        lead_space_len: int,
        original_line: str,
        adjust_block_quote_indent: bool,
    ) -> Tuple[Optional[str], Optional[str], Optional[str], bool]:
        POGGER.debug("after_space_index>:$:<", after_space_index)
        POGGER.debug("ex_space>:$:<", ex_space)
        assert ex_space is not None
        detabified_ex_space = TabHelper.detabify_string(
            ex_space, additional_start_delta=lead_space_len
        )
        POGGER.debug("detabified_ex_space>:$:<", detabified_ex_space)
        # assert detabified_ex_space == extracted_whitespace
        # last_good_space_index = -1
        # space_index = 1
        # detabified_ex_space = ""
        # while space_index < len(ex_space) + 1 and len(detabified_ex_space) < 4:
        #     POGGER.debug("space_index>:$:<", space_index)
        #     last_good_space_index = space_index
        #     space_prefix = ex_space[:space_index]
        #     POGGER.debug("sdf>:$:<", space_prefix)
        #     POGGER.debug("lead_space_len>:$:<", lead_space_len)
        #     detabified_ex_space = TabHelper.detabify_string(
        #         space_prefix, additional_start_delta=lead_space_len
        #     )
        #     POGGER.debug("detabified_ex_space>:$:<", detabified_ex_space)
        #     space_index += 1
        # assert len(detabified_ex_space) >= 4

        (
            detabified_ex_space,
            last_good_space_index,
            space_prefix,
        ) = TabHelper.search_for_tabbed_prefix(ex_space, 4, lead_space_len)
        assert space_prefix is not None

        if len(detabified_ex_space) == 4:
            xx_extracted_space = space_prefix
            xx_left_over = ex_space[last_good_space_index:]
        else:
            xx_extracted_space = space_prefix[:-1]
            xx_left_over = ParserHelper.create_replacement_markers(
                space_prefix[-1], detabified_ex_space[4:]
            )

        POGGER.debug("xx_extracted_space>:$:<", xx_extracted_space)
        POGGER.debug("xx_left_over>:$:<", xx_left_over)
        xx_left_over += original_line[after_space_index:]
        POGGER.debug("xx_left_over>:$:<", xx_left_over)
        return None, xx_extracted_space, xx_left_over, adjust_block_quote_indent

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_indented_code_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        new_tokens: List[MarkdownToken],
        tabified_extracted_space: Optional[str],
        original_line: str,
        xx_extracted_space: Optional[str],
        xx_left_over: Optional[str],
        adjust_block_quote_indent: bool,
        last_block_quote_index: int,
        extracted_whitespace: str,
        indented_text: str,
    ) -> None:
        # adj_ws: Optional[str] = ""
        # POGGER.debug("tabified_extracted_space>:$:<", tabified_extracted_space)
        if not parser_state.token_stack[-1].is_indented_code_block:
            # POGGER.debug("xx_extracted_space>:$:<", xx_extracted_space)
            # POGGER.debug("xx_left_over>:$:<", xx_left_over)
            (
                last_block_quote_index,
                xextracted_whitespace,
                indented_text,
            ) = IndentedLeafBlockProcessor.__create_indented_block(
                parser_state,
                last_block_quote_index,
                position_marker,
                extracted_whitespace,
                new_tokens,
                tabified_extracted_space,
                original_line,
                indented_text,
                xx_extracted_space,
                xx_left_over,
            )
            assert xextracted_whitespace is not None
            extracted_whitespace = xextracted_whitespace
        elif tabified_extracted_space:
            (_, adj_ws, _) = IndentedLeafBlockProcessor.__recalculate_whitespace(
                extracted_whitespace, 0, tabified_extracted_space
            )
            extracted_whitespace = adj_ws

            adj_ws_length = len(adj_ws)
            indented_text = original_line[adj_ws_length:]
        elif xx_extracted_space is not None:
            extracted_whitespace = xx_extracted_space
            assert xx_left_over is not None
            indented_text = xx_left_over

        # POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        # POGGER.debug("indented_text>:$:<", indented_text)

        if adjust_block_quote_indent:
            TabHelper.adjust_block_quote_indent_for_tab(parser_state)

        assert extracted_whitespace is not None
        new_tokens.append(
            TextMarkdownToken(
                indented_text,
                extracted_whitespace,
                position_marker=position_marker,
            )
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __get_indented_block_with_tab_quote_properties(
        parser_state: ParserState, last_block_quote_index: int, original_line: str
    ) -> Tuple[str, int, bool]:
        adjust_block_quote_indent = False

        POGGER.debug(
            "token_stack[last_block_quote_index]>:$:<",
            parser_state.token_stack[last_block_quote_index],
        )
        last_block_quote_token = cast(
            BlockQuoteMarkdownToken,
            parser_state.token_stack[last_block_quote_index].matching_markdown_token,
        )
        last_block_quote_lead_spaces = last_block_quote_token.bleading_spaces
        assert last_block_quote_lead_spaces is not None
        POGGER.debug("last_block_quote_lead_spaces>:$:<", last_block_quote_lead_spaces)
        lead_space_last_line_index = last_block_quote_lead_spaces.rfind("\n")
        POGGER.debug("original_line>:$:<", original_line)
        adj_lead_space_len = 0
        if lead_space_last_line_index != -1:
            last_block_quote_lead_spaces = last_block_quote_lead_spaces[
                lead_space_last_line_index + 1 :
            ]
            POGGER.debug(
                "last_block_quote_lead_spaces>:$:<", last_block_quote_lead_spaces
            )
        assert last_block_quote_lead_spaces[-1] == " "
        last_part_minus_tailing_space = last_block_quote_lead_spaces[:-1]
        POGGER.debug(
            "last_part_minus_tailing_space>:$:<", last_part_minus_tailing_space
        )
        assert original_line.startswith(last_part_minus_tailing_space)
        trailing_char_in_original = original_line[len(last_part_minus_tailing_space)]
        POGGER.debug("trailing_char_in_original>:$:<", trailing_char_in_original)
        if trailing_char_in_original == ParserHelper.tab_character:
            adjust_block_quote_indent = True
            adj_lead_space_len = -1
            assert original_line.startswith(last_part_minus_tailing_space)
        POGGER.debug("last_block_quote_lead_spaces>:$:<", last_block_quote_lead_spaces)
        # if not adjust_block_quote_indent:
        #     assert original_line.startswith(last_block_quote_lead_spaces)
        return (
            last_block_quote_lead_spaces,
            adj_lead_space_len,
            adjust_block_quote_indent,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __create_indented_block(
        parser_state: ParserState,
        last_block_quote_index: int,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        new_tokens: List[MarkdownToken],
        tabified_extracted_space: Optional[str],
        original_line: str,
        indented_text: str,
        xx_extracted_space: Optional[str],
        xx_left_over: Optional[str],
    ) -> Tuple[int, Optional[str], str]:
        assert extracted_whitespace is not None
        column_number = (
            position_marker.index_number
            + position_marker.index_indent
            - len(extracted_whitespace)
            + 1
        )
        POGGER.debug("last_block_quote_index>:$:<", last_block_quote_index)
        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        POGGER.debug("tabified_extracted_space>:$:<", tabified_extracted_space)
        POGGER.debug("xx_extracted_space>:$:<", xx_extracted_space)
        (
            last_block_quote_index,
            actual_whitespace_index,
            adj_ws,
            extracted_whitespace,
        ) = IndentedLeafBlockProcessor.__prepare_for_indented_block(
            parser_state,
            last_block_quote_index,
            extracted_whitespace,
            tabified_extracted_space,
        )
        POGGER.debug("last_block_quote_index>:$:<", last_block_quote_index)
        POGGER.debug("actual_whitespace_index>:$:<", actual_whitespace_index)
        POGGER.debug("adj_ws>:$:<", adj_ws)
        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        if xx_extracted_space is not None:
            adj_ws = xx_extracted_space
        POGGER.debug("adj_ws>:$:<", adj_ws)

        column_number += actual_whitespace_index
        POGGER.debug("column_number>>$", column_number)

        new_token = IndentedCodeBlockMarkdownToken(
            adj_ws, position_marker.line_number, column_number
        )
        parser_state.token_stack.append(IndentedCodeBlockStackToken(new_token))
        new_tokens.append(new_token)
        POGGER.debug("left_ws>>$<<", extracted_whitespace)

        POGGER.debug("xx_left_over>:$:<", xx_left_over)
        POGGER.debug("tabified_extracted_space>:$:<", tabified_extracted_space)
        if xx_left_over:
            extracted_whitespace = ""
            indented_text = xx_left_over
        if tabified_extracted_space:
            extracted_whitespace = ""
            adj_ws_length = len(adj_ws)
            indented_text = original_line[adj_ws_length:]

        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        POGGER.debug("indented_text>:$:<", indented_text)
        return last_block_quote_index, extracted_whitespace, indented_text

    # pylint: enable=too-many-arguments

    @staticmethod
    def __prepare_for_indented_block(
        parser_state: ParserState,
        last_block_quote_index: int,
        extracted_whitespace: Optional[str],
        tabified_extracted_space: Optional[str],
    ) -> Tuple[int, int, str, str]:
        POGGER.debug(">>>>$", parser_state.token_stack[-1])
        if parser_state.token_stack[-1].is_list:
            list_token = cast(ListStackToken, parser_state.token_stack[-1])
            POGGER.debug(
                ">>indent>>$",
                list_token.indent_level,
            )
            last_block_quote_index = 0

        POGGER.debug(
            "__recalculate_whitespace>>$>>$",
            extracted_whitespace,
            0,
        )
        (
            actual_whitespace_index,
            adj_ws,
            left_ws,
        ) = IndentedLeafBlockProcessor.__recalculate_whitespace(
            extracted_whitespace, 0, tabified_extracted_space
        )
        return (
            last_block_quote_index,
            actual_whitespace_index,
            adj_ws,
            left_ws,
        )

    @staticmethod
    def __recalculate_whitespace(
        whitespace_to_parse: Optional[str],
        offset_index: int,
        tabified_extracted_space: Optional[str],
    ) -> Tuple[int, str, str]:
        """
        Recalculate the whitespace characteristics.
        """
        assert whitespace_to_parse is not None
        POGGER.debug("whitespace_to_parse>>$>>", whitespace_to_parse)
        POGGER.debug("offset_index>>$>>", offset_index)
        POGGER.debug("tabified_extracted_space>>$>>", tabified_extracted_space)

        actual_whitespace_index = 4 + offset_index
        adj_ws = whitespace_to_parse[:actual_whitespace_index]
        left_ws = whitespace_to_parse[actual_whitespace_index:]
        if tabified_extracted_space:
            additional_start_delta = 0
            length_so_far = 0
            last_index = 0
            next_character_index = 0
            while (
                next_character_index < len(tabified_extracted_space)
                and length_so_far < 4
            ):
                next_character = tabified_extracted_space[next_character_index]
                POGGER.debug("next_character>:$:<", next_character)
                if next_character == ParserHelper.tab_character:
                    length_so_far = (1 + (length_so_far // 4)) * 4
                else:
                    length_so_far += 1
                last_index += 1
                POGGER.debug("length_so_far>:$:<", length_so_far)
                next_character_index += 1
            POGGER.debug("length_so_far>:$:<", length_so_far)
            assert length_so_far == 4
            POGGER.debug("last_index>:$:<", last_index)
            tabbed_prefix = tabified_extracted_space[:last_index]
            POGGER.debug("tabbed_prefix>:$:<", tabbed_prefix)
            err = TabHelper.detabify_string(
                tabbed_prefix,
                additional_start_delta=additional_start_delta,
            )
            POGGER.debug("tabbed_prefix>:$:<", tabbed_prefix)
            POGGER.debug("err>:$:<", err)
            assert len(err) == 4
            adj_ws = tabbed_prefix
            left_ws = tabified_extracted_space[last_index:]

        POGGER.debug("actual_whitespace_index>>$", actual_whitespace_index)
        POGGER.debug("adj_ws>>$<<", adj_ws)
        POGGER.debug("left_ws>>$<<", left_ws)
        return actual_whitespace_index, adj_ws, left_ws


# pylint: enable=too-few-public-methods
