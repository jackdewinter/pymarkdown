"""
Module to provide processing for the setext heading leaf blocks.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.leaf_blocks.leaf_block_helper import LeafBlockHelper
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.tab_helper import TabHelper
from pymarkdown.tokens.leaf_markdown_token import (
    ParagraphMarkdownToken,
    SetextHeadingMarkdownToken,
)
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import ListStackToken, StackToken

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-few-public-methods


class SetextLeafBlockProcessor:
    """
    Class to provide processing for the setext heading leaf blocks.
    """

    __setext_characters = "-="

    @staticmethod
    def __parse_setext_headings_with_tab(
        original_line: str,
        line_to_parse: str,
        extracted_whitespace: str,
    ) -> Tuple[str, Optional[str], bool, bool, Optional[str]]:
        POGGER.debug("original_line>>:$:<", original_line)
        POGGER.debug("line_to_parse>>:$:<", line_to_parse)

        (
            token_text,
            split_tab,
            split_tab_with_block_quote_suffix,
            extra_whitespace_prefix,
            new_extracted_whitespace,
        ) = TabHelper.parse_thematic_break_with_tab(
            original_line, line_to_parse, extracted_whitespace
        )
        POGGER.debug("token_text>>:$:<", token_text)
        POGGER.debug("split_tab>>:$:<", split_tab)
        POGGER.debug(
            "split_tab_with_block_quote_suffix>>:$:<", split_tab_with_block_quote_suffix
        )
        POGGER.debug("extra_whitespace_prefix>>:$:<", extra_whitespace_prefix)
        POGGER.debug("new_extracted_whitespace>>:$:<", new_extracted_whitespace)

        return (
            token_text,
            new_extracted_whitespace,
            split_tab,
            split_tab_with_block_quote_suffix,
            extra_whitespace_prefix,
        )

    @staticmethod
    def parse_setext_headings(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        block_quote_data: BlockQuoteData,
        original_line: str,
    ) -> List[MarkdownToken]:
        """
        Handle the parsing of an setext heading.
        """

        new_tokens: List[MarkdownToken] = []
        assert extracted_whitespace is not None
        POGGER.debug("extracted_whitespace=>:$:<", extracted_whitespace)
        if (
            TabHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            and ParserHelper.is_character_at_index_one_of(
                position_marker.text_to_parse,
                position_marker.index_number,
                SetextLeafBlockProcessor.__setext_characters,
            )
            and parser_state.token_stack[-1].is_paragraph
            and (block_quote_data.current_count == block_quote_data.stack_count)
        ):
            POGGER.debug(
                "parse_setext_headings>>start",
            )
            is_paragraph_continuation = (
                SetextLeafBlockProcessor.__adjust_continuation_for_active_list(
                    parser_state, position_marker
                )
            )

            line_to_parse = position_marker.text_to_parse[
                position_marker.index_number :
            ]
            ex_ws_l = len(extracted_whitespace)
            POGGER.debug("line_to_parse=>:$:<", line_to_parse)
            POGGER.debug("original_line=>:$:<", original_line)
            split_tab = False
            split_tab_with_block_quote_suffix = False
            extra_whitespace_prefix = None
            if ParserHelper.tab_character in original_line:
                (
                    line_to_parse,
                    extracted_whitespace,
                    split_tab,
                    split_tab_with_block_quote_suffix,
                    extra_whitespace_prefix,
                ) = SetextLeafBlockProcessor.__parse_setext_headings_with_tab(
                    original_line,
                    line_to_parse,
                    extracted_whitespace,
                )

            assert extracted_whitespace is not None
            SetextLeafBlockProcessor.__prepare_and_create_setext_token(
                parser_state,
                position_marker,
                line_to_parse,
                is_paragraph_continuation,
                split_tab,
                new_tokens,
                extracted_whitespace,
                ex_ws_l,
                split_tab_with_block_quote_suffix,
                extra_whitespace_prefix,
            )
        else:
            POGGER.debug(
                "parse_setext_headings>>not eligible",
            )
        return new_tokens

    # pylint: disable=too-many-arguments
    @staticmethod
    def __prepare_and_create_setext_token(
        parser_state: ParserState,
        position_marker: PositionMarker,
        line_to_parse: str,
        is_paragraph_continuation: bool,
        split_tab: bool,
        new_tokens: List[MarkdownToken],
        extracted_whitespace: str,
        ex_ws_l: int,
        split_tab_with_block_quote_suffix: bool,
        extra_whitespace_prefix: Optional[str],
    ) -> Tuple[int, int, str]:
        _, collected_to_index = ParserHelper.collect_while_character(
            line_to_parse,
            0,
            position_marker.text_to_parse[position_marker.index_number],
        )
        POGGER.debug(
            ">>position_marker.index_number>:$:<", position_marker.index_number
        )

        POGGER.debug(">>collected_to_index>:$:<", collected_to_index)
        assert collected_to_index is not None
        (
            after_whitespace_index,
            extra_whitespace_after_setext,
        ) = ParserHelper.extract_spaces(line_to_parse, collected_to_index)
        assert after_whitespace_index is not None
        assert extra_whitespace_after_setext is not None

        if not is_paragraph_continuation and after_whitespace_index == len(
            line_to_parse
        ):
            old_top_of_stack = parser_state.token_stack[-1]

            if split_tab and split_tab_with_block_quote_suffix:
                TabHelper.adjust_block_quote_indent_for_tab(parser_state)
            SetextLeafBlockProcessor.__create_setext_token(
                parser_state,
                position_marker,
                collected_to_index + ex_ws_l,
                new_tokens,
                extracted_whitespace,
                extra_whitespace_after_setext,
            )
            if split_tab and not split_tab_with_block_quote_suffix:
                SetextLeafBlockProcessor.__prepare_and_create_setext_token_list_adjust(
                    parser_state,
                    position_marker,
                    extracted_whitespace,
                    extra_whitespace_prefix,
                    old_top_of_stack,
                    new_tokens,
                )
        return collected_to_index, after_whitespace_index, extra_whitespace_after_setext

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __prepare_and_create_setext_token_list_adjust(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: str,
        extra_whitespace_prefix: Optional[str],
        old_top_of_stack: StackToken,
        new_tokens: List[MarkdownToken],
    ) -> None:
        POGGER.debug("parser_state.token_stack[-1]>>:$:<", parser_state.token_stack[-1])
        POGGER.debug("parser_state.token_stack>>:$:<", parser_state.token_stack)
        POGGER.debug("parser_state.token_document>>:$:<", parser_state.token_document)
        assert parser_state.token_stack[-1].is_list
        modified_whitespace = (
            extra_whitespace_prefix + extracted_whitespace
            if extra_whitespace_prefix is not None
            else extracted_whitespace
        )
        TabHelper.adjust_block_quote_indent_for_tab(parser_state, modified_whitespace)
        POGGER.debug("parser_state.token_stack>>:$:<", parser_state.token_stack)
        POGGER.debug("parser_state.token_document>>:$:<", parser_state.token_document)
        LeafBlockHelper.correct_for_leaf_block_start_in_list(
            parser_state,
            position_marker.index_indent,
            old_top_of_stack,
            new_tokens,
            was_token_already_added_to_stack=False,
            delay_tab_match=True,
        )
        POGGER.debug("parser_state.token_stack>>:$:<", parser_state.token_stack)
        POGGER.debug("parser_state.token_document>>:$:<", parser_state.token_document)
        POGGER.debug("new_tokens>>:$:<", new_tokens)

    # pylint: enable=too-many-arguments
    @staticmethod
    def __adjust_continuation_for_active_list(
        parser_state: ParserState, position_marker: PositionMarker
    ) -> bool:
        is_paragraph_continuation: bool = (
            len(parser_state.token_stack) > 1 and parser_state.token_stack[-2].is_list
        )
        if is_paragraph_continuation:
            list_token = cast(ListStackToken, parser_state.token_stack[-2])
            POGGER.debug(
                "parser_state.original_line_to_parse>:$:<",
                parser_state.original_line_to_parse,
            )
            adj_text = position_marker.text_to_parse[position_marker.index_number :]
            assert parser_state.original_line_to_parse is not None
            assert parser_state.original_line_to_parse.endswith(adj_text)
            removed_text_length = len(parser_state.original_line_to_parse) - len(
                adj_text
            )
            POGGER.debug("removed_text_length>:$:<", removed_text_length)
            POGGER.debug("adj_text>:$:<", adj_text)
            POGGER.debug("indent_level>:$:<", list_token.indent_level)
            is_paragraph_continuation = (
                bool(adj_text) and removed_text_length < list_token.indent_level
            )
        return is_paragraph_continuation

    # pylint: disable=too-many-arguments
    @staticmethod
    def __create_setext_token(
        parser_state: ParserState,
        position_marker: PositionMarker,
        collected_to_index: int,
        new_tokens: List[MarkdownToken],
        extracted_whitespace: Optional[str],
        extra_whitespace_after_setext: Optional[str],
    ) -> None:
        token_index = len(parser_state.token_document) - 1
        while not parser_state.token_document[token_index].is_paragraph:
            token_index -= 1

        paragraph_token = cast(
            ParagraphMarkdownToken, parser_state.token_document[token_index]
        )
        assert paragraph_token.extra_data is not None
        replacement_token = SetextHeadingMarkdownToken(
            position_marker.text_to_parse[position_marker.index_number],
            collected_to_index - position_marker.index_number,
            paragraph_token.extra_data,
            position_marker,
            paragraph_token,
        )

        # This is unusual.  Normally, close_open_blocks is used to close off
        # blocks based on the stack token.  However, since the setext takes
        # the last paragraph of text (see case 61) and translates it
        # into a heading, this has to be done separately, as there is no
        # stack token to close.
        assert extra_whitespace_after_setext is not None
        assert extracted_whitespace is not None
        new_tokens.append(
            replacement_token.generate_close_markdown_token_from_markdown_token(
                extracted_whitespace, extra_whitespace_after_setext
            )
        )

        parser_state.token_document[token_index] = replacement_token
        del parser_state.token_stack[-1]

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
