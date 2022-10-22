"""
Module to provide processing for the leaf blocks.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quote_data import BlockQuoteData
from pymarkdown.constants import Constants
from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.leaf_markdown_token import (
    BlankLineMarkdownToken,
    ParagraphMarkdownToken,
)
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.stack_token import (
    BlockQuoteStackToken,
    ListStackToken,
    ParagraphStackToken,
)

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


class LeafBlockProcessorParagraph:
    """
    Class to provide processing for the leaf blocks.
    """

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def parse_paragraph(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        block_quote_data: BlockQuoteData,
        text_removed_by_container: Optional[str],
        original_line: str,
    ) -> List[MarkdownToken]:
        """
        Handle the parsing of a paragraph.
        """
        POGGER.debug(">>text_removed_by_container>>:$:<<", text_removed_by_container)
        assert extracted_whitespace is not None
        POGGER.debug(">>extracted_whitespace>>:$:<<", extracted_whitespace)
        POGGER.debug("position_marker.text_to_parse=:$:", position_marker.text_to_parse)
        POGGER.debug("position_marker.index_number=:$:", position_marker.index_number)
        POGGER.debug("position_marker.index_indent=:$:", position_marker.index_indent)

        if parser_state.no_para_start_if_empty and position_marker.index_number >= len(
            position_marker.text_to_parse
        ):
            POGGER.debug("Escaping paragraph due to empty w/ blank")
            return [
                BlankLineMarkdownToken(
                    extracted_whitespace, position_marker, len(extracted_whitespace)
                )
            ]

        POGGER.debug(
            "parse_paragraph>block_quote_data.stack_count>$>block_quote_data.current_count>$<",
            block_quote_data.stack_count,
            block_quote_data.current_count,
        )

        container_index, adjusted_whitespace_length = (
            parser_state.find_last_container_on_stack(),
            0,
        )
        if container_index > 0:
            adjusted_whitespace_length = (
                LeafBlockProcessorParagraph.__adjust_paragraph_for_containers(
                    parser_state,
                    container_index,
                    extracted_whitespace,
                    adjusted_whitespace_length,
                )
            )

        POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
        POGGER.debug("adjusted_whitespace_length=:$:", adjusted_whitespace_length)
        (
            new_tokens,
            extracted_whitespace,
            did_add_paragraph_token,
        ) = LeafBlockProcessorParagraph.__handle_paragraph_prep(
            parser_state,
            block_quote_data,
            position_marker,
            extracted_whitespace,
        )

        adjusted_index = position_marker.index_number
        if did_add_paragraph_token and ParserHelper.is_character_at_index_one_of(
            position_marker.text_to_parse, adjusted_index, Constants.ascii_whitespace
        ):
            new_index, end_string = ParserHelper.extract_ascii_whitespace(
                position_marker.text_to_parse, adjusted_index
            )
            assert new_index is not None and end_string
            assert not extracted_whitespace
            adjusted_index = new_index
            extracted_whitespace = end_string

        text_to_parse = position_marker.text_to_parse[adjusted_index:]
        POGGER.debug("--add-text-token--")
        POGGER.debug("text_to_parse=:$:", text_to_parse)
        POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
        POGGER.debug("original_line=:$:", original_line)
        assert extracted_whitespace is not None

        (
            corrected_tab_text,
            corrected_extracted_whitespace,
        ) = LeafBlockProcessorParagraph.__calculate_corrected_tab_text(
            original_line, text_to_parse, extracted_whitespace
        )

        new_tokens.append(
            TextMarkdownToken(
                text_to_parse,
                corrected_extracted_whitespace,
                position_marker=position_marker,
                tabified_text=corrected_tab_text,
            )
        )
        return new_tokens

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __calculate_corrected_tab_text(
        original_line: str, text_to_parse: str, extracted_whitespace: str
    ) -> Tuple[str, str]:
        corrected_tab_text = ""
        corrected_extracted_whitespace = extracted_whitespace
        if "\t" in original_line:

            if corrected_extracted_whitespace:
                first_non_whitespace_character = text_to_parse[0]
                first_non_whitespace_character_index = original_line.find(
                    first_non_whitespace_character
                )
                corrected_extracted_whitespace = original_line[
                    :first_non_whitespace_character_index
                ]
                original_line = original_line[first_non_whitespace_character_index:]

            corrected_index = -1
            ends_without_modification = original_line.endswith(text_to_parse)
            POGGER.debug("ends_without_modification=:$:", ends_without_modification)
            if ends_without_modification:
                corrected_index = len(original_line) - len(text_to_parse)
                corrected_tab_text = original_line[corrected_index:]
                assert corrected_tab_text == text_to_parse
            else:
                POGGER.debug("original_line=:$:", original_line)
                POGGER.debug("text_to_parse=:$:", text_to_parse)
                adj_text_to_parse, _ = ParserHelper.find_detabify_string(
                    original_line, text_to_parse
                )
                POGGER.debug("adj_text_to_parse=:$:", adj_text_to_parse)
                assert adj_text_to_parse is not None
                corrected_index = 0
                corrected_tab_text = adj_text_to_parse
            assert corrected_index != -1
        return corrected_tab_text, corrected_extracted_whitespace

    @staticmethod
    def __adjust_paragraph_for_containers(
        parser_state: ParserState,
        container_index: int,
        extracted_whitespace: Optional[str],
        adjusted_whitespace_length: int,
    ) -> int:
        if not parser_state.token_stack[container_index].is_block_quote:
            top_list_token = cast(
                ListStackToken, parser_state.token_stack[container_index]
            )
            POGGER.debug(">>list-owners>>$", top_list_token)
            adjusted_whitespace_length = (
                LeafBlockProcessorParagraph.__adjust_paragraph_for_list(
                    top_list_token, extracted_whitespace
                )
            )
        POGGER.debug(">>adjusted_whitespace_length>>$", adjusted_whitespace_length)
        return adjusted_whitespace_length

    @staticmethod
    def __adjust_paragraph_for_list(
        top_list_token: ListStackToken, extracted_whitespace: Optional[str]
    ) -> int:
        assert extracted_whitespace is not None
        ex_ws_length = len(extracted_whitespace)
        POGGER.debug(">>owners-indent>>$", top_list_token.indent_level)
        POGGER.debug(">>ws_before_marker>>$", top_list_token.ws_before_marker)
        POGGER.debug(">>ws_after_marker>>$", top_list_token.ws_after_marker)
        POGGER.debug(">>last_new_list_token>>$", top_list_token.last_new_list_token)
        POGGER.debug(">>extracted_whitespace>>$", ex_ws_length)

        dominant_indent, original_list_indent, indent_delta = (
            (
                top_list_token.last_new_list_token.indent_level
                if top_list_token.last_new_list_token
                else top_list_token.indent_level
            ),
            top_list_token.indent_level - 2,
            (
                top_list_token.ws_after_marker - 1
                if top_list_token.ws_after_marker > 1
                else 0
            ),
        )
        POGGER.debug(">>dominant_indent>>$>>", dominant_indent)
        original_text_indent = (
            ex_ws_length
            + top_list_token.indent_level
            - top_list_token.ws_before_marker
            - indent_delta
        )
        POGGER.debug(">>original_list_indent>>$>>", original_list_indent)
        POGGER.debug(">>original_text_indent>$>>", original_text_indent)
        return (
            dominant_indent - original_text_indent
            if dominant_indent > original_text_indent >= 4
            else 0
        )

    @staticmethod
    def __handle_paragraph_prep(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
    ) -> Tuple[List[MarkdownToken], Optional[str], bool]:

        # In cases where the list ended on the same line as we are processing, the
        # container tokens will not yet be added to the token_document.  As such,
        # make sure to construct a "proper" list that takes those into account
        # before checking to see if this is an issue.
        adjusted_document = parser_state.token_document[:]
        assert parser_state.same_line_container_tokens is not None
        adjusted_document.extend(parser_state.same_line_container_tokens)
        did_add_paragraph_token = False

        if (
            len(adjusted_document) >= 2
            and adjusted_document[-1].is_blank_line
            and adjusted_document[-2].is_any_list_token
        ):

            (
                did_find,
                last_list_index,
            ) = LeafBlockProcessorParagraph.check_for_list_in_process(parser_state)
            assert did_find
            new_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state, until_this_index=last_list_index
            )
        elif block_quote_data.stack_count != 0 and block_quote_data.current_count == 0:
            new_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[BlockQuoteStackToken],
                include_block_quotes=True,
            )
        else:
            new_tokens = []

        if not parser_state.token_stack[-1].is_paragraph:
            assert extracted_whitespace is not None
            new_paragraph_token = ParagraphMarkdownToken(
                extracted_whitespace, position_marker
            )
            parser_state.token_stack.append(ParagraphStackToken(new_paragraph_token))
            new_tokens.append(new_paragraph_token)
            extracted_whitespace = ""
            did_add_paragraph_token = True
        return new_tokens, extracted_whitespace, did_add_paragraph_token

    @staticmethod
    def check_for_list_in_process(parser_state: ParserState) -> Tuple[bool, int]:
        """
        From the end of the stack, check to see if there is already a list in progress.
        """

        stack_index = len(parser_state.token_stack) - 1

        while stack_index >= 0 and not parser_state.token_stack[stack_index].is_list:
            stack_index -= 1

        return stack_index >= 0, stack_index
