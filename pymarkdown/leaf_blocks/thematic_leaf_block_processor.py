"""
Module to provide processing for thematic break leaf blocks.
"""

import logging
from typing import List, Optional, Tuple

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.container_blocks.container_helper import ContainerHelper
from pymarkdown.leaf_blocks.leaf_block_helper import LeafBlockHelper
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.tab_helper import TabHelper
from pymarkdown.tokens.leaf_markdown_token import ThematicBreakMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import ParagraphStackToken, StackToken

POGGER = ParserLogger(logging.getLogger(__name__))


class ThematicLeafBlockProcessor:
    """
    Module to provide processing for thematic break leaf blocks.
    """

    __thematic_break_characters = "*_-"

    @staticmethod
    def is_thematic_break(
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        skip_whitespace_check: bool = False,
        whitespace_allowed_between_characters: bool = True,
    ) -> Tuple[Optional[str], Optional[int]]:
        """
        Determine whether or not we have a thematic break.
        """

        assert extracted_whitespace is not None
        thematic_break_character, end_of_break_index = None, None
        is_thematic_character = ParserHelper.is_character_at_index_one_of(
            line_to_parse,
            start_index,
            ThematicLeafBlockProcessor.__thematic_break_characters,
        )
        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        POGGER.debug("skip_whitespace_check>>$", skip_whitespace_check)
        POGGER.debug("is_thematic_character>>$", is_thematic_character)
        if (
            TabHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            or skip_whitespace_check
        ) and is_thematic_character:
            POGGER.debug("checking for thematic break")
            start_char, index, char_count, line_to_parse_size = (
                line_to_parse[start_index],
                start_index,
                0,
                len(line_to_parse),
            )

            while index < line_to_parse_size:
                if (
                    whitespace_allowed_between_characters
                    and ParserHelper.is_character_at_index_whitespace(
                        line_to_parse, index
                    )
                ):
                    index += 1
                elif line_to_parse[index] == start_char:
                    index += 1
                    char_count += 1
                else:
                    break  # pragma: no cover

            POGGER.debug("char_count>>$", char_count)
            POGGER.debug("index>>$", index)
            POGGER.debug("line_to_parse_size>>$", line_to_parse_size)
            if char_count >= 3 and index == line_to_parse_size:
                thematic_break_character, end_of_break_index = start_char, index

        return thematic_break_character, end_of_break_index

    @staticmethod
    def parse_thematic_break(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        block_quote_data: BlockQuoteData,
        original_line: str,
    ) -> List[MarkdownToken]:
        """
        Handle the parsing of a thematic break.
        """

        new_tokens: List[MarkdownToken] = []

        start_char, index = ThematicLeafBlockProcessor.is_thematic_break(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
        )
        if start_char:
            old_top_of_stack = parser_state.token_stack[-1]

            POGGER.debug(
                "parse_thematic_break>>start",
            )
            if parser_state.token_stack[-1].is_paragraph:
                force_paragraph_close_if_present = (
                    block_quote_data.current_count == 0
                    and block_quote_data.stack_count > 0
                )
                new_tokens, _ = parser_state.close_open_blocks_fn(
                    parser_state,
                    only_these_blocks=[ParagraphStackToken],
                    was_forced=force_paragraph_close_if_present,
                )

            token_text = position_marker.text_to_parse[
                position_marker.index_number : index
            ]
            # POGGER.debug("extracted_whitespace>>:$:<", extracted_whitespace)
            # POGGER.debug("token_text>>:$:<", token_text)
            # POGGER.debug("original_line>>:$:<", original_line)
            split_tab, split_tab_with_block_quote_suffix = False, False
            extra_whitespace_prefix: Optional[str] = None
            if ParserHelper.tab_character in original_line:
                (
                    token_text,
                    split_tab,
                    split_tab_with_block_quote_suffix,
                    extra_whitespace_prefix,
                    extracted_whitespace,
                ) = TabHelper.parse_thematic_break_with_tab(
                    original_line, token_text, extracted_whitespace
                )
                # POGGER.debug("extra_whitespace_prefix>>:$:<", extra_whitespace_prefix)
                # POGGER.debug("extracted_whitespace>>:$:<", extracted_whitespace)

            assert extracted_whitespace is not None
            ThematicLeafBlockProcessor.__perform_adjusts(
                parser_state,
                position_marker,
                extra_whitespace_prefix,
                extracted_whitespace,
                old_top_of_stack,
                new_tokens,
                start_char,
                token_text,
                block_quote_data,
                split_tab,
                split_tab_with_block_quote_suffix,
            )

            new_tokens.append(
                ThematicBreakMarkdownToken(
                    start_char,
                    extracted_whitespace,
                    token_text,
                    position_marker=position_marker,
                )
            )
        else:
            POGGER.debug(
                "parse_thematic_break>>not eligible",
            )
        return new_tokens

    @staticmethod
    def __perform_adjusts(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extra_whitespace_prefix: Optional[str],
        extracted_whitespace: str,
        old_top_of_stack: StackToken,
        new_tokens: List[MarkdownToken],
        start_char: str,
        token_text: str,
        block_quote_data: BlockQuoteData,
        split_tab: bool,
        split_tab_with_block_quote_suffix: bool,
    ) -> None:
        if split_tab and not split_tab_with_block_quote_suffix:
            assert extracted_whitespace is not None
            ThematicLeafBlockProcessor.__parse_thematic_break_with_suffix(
                parser_state,
                position_marker,
                extra_whitespace_prefix,
                extracted_whitespace,
                old_top_of_stack,
                new_tokens,
                start_char,
                token_text,
            )
        elif split_tab := ContainerHelper.reduce_containers_if_required(
            parser_state, block_quote_data, new_tokens, split_tab
        ):
            TabHelper.adjust_block_quote_indent_for_tab(parser_state)

    @staticmethod
    def __parse_thematic_break_with_suffix(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extra_whitespace_prefix: Optional[str],
        extracted_whitespace: str,
        old_top_of_stack: StackToken,
        new_tokens: List[MarkdownToken],
        start_char: str,
        token_text: str,
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

        POGGER.debug("start_char>>:$:<", start_char)
        POGGER.debug("extracted_whitespace>>:$:<", extracted_whitespace)
        POGGER.debug("token_text>>:$:<", token_text)
