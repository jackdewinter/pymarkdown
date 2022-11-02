"""
Module to provide processing for the leaf blocks.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quote_data import BlockQuoteData
from pymarkdown.constants import Constants
from pymarkdown.container_markdown_token import BlockQuoteMarkdownToken
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
            original_line,
        )
        POGGER.debug("new_tokens=:$:", new_tokens)
        POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
        POGGER.debug("did_add_paragraph_token=:$:", did_add_paragraph_token)
        POGGER.debug(
            "position_marker.text_to_parse=:$:",
            position_marker.text_to_parse[position_marker.index_number :],
        )

        adjusted_index = position_marker.index_number
        if did_add_paragraph_token and ParserHelper.is_character_at_index_one_of(
            position_marker.text_to_parse, adjusted_index, Constants.ascii_whitespace
        ):
            POGGER.debug(
                "position_marker.text_to_parse=:$:", position_marker.text_to_parse
            )
            POGGER.debug("adjusted_index=:$:", adjusted_index)
            new_index, end_string = ParserHelper.extract_ascii_whitespace(
                position_marker.text_to_parse, adjusted_index
            )
            POGGER.debug("new_index=:$:", new_index)
            POGGER.debug("end_string=:$:", end_string)
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
            parser_state, original_line, text_to_parse, extracted_whitespace
        )
        POGGER.debug("corrected_tab_text=:$:", corrected_tab_text)
        POGGER.debug(
            "corrected_extracted_whitespace=:$:", corrected_extracted_whitespace
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
        parser_state: ParserState,
        original_line: str,
        text_to_parse: str,
        extracted_whitespace: str,
    ) -> Tuple[str, str]:
        corrected_tab_text = ""
        if "\t" in original_line:

            (
                corrected_extracted_whitespace,
                original_line,
            ) = LeafBlockProcessorParagraph.__calculate_corrected_tab_text_prefix(
                parser_state, extracted_whitespace, text_to_parse, original_line
            )

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
        else:
            corrected_extracted_whitespace = extracted_whitespace
        return corrected_tab_text, corrected_extracted_whitespace

    @staticmethod
    def __calculate_corrected_tab_text_prefix(
        parser_state: ParserState,
        extracted_whitespace: str,
        text_to_parse: str,
        original_line: str,
    ) -> Tuple[str, str]:
        POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
        if extracted_whitespace:
            first_non_whitespace_character = text_to_parse[0]
            first_non_whitespace_character_index = original_line.find(
                first_non_whitespace_character
            )
            corrected_extracted_whitespace = original_line[
                :first_non_whitespace_character_index
            ]
            POGGER.debug(
                "corrected_extracted_whitespace=:$:", corrected_extracted_whitespace
            )
            if len(corrected_extracted_whitespace) > 0:
                (
                    detabified_prefix,
                    detabified_suffix,
                    corrected_prefix,
                    corrected_suffix,
                    split_tab,
                ) = LeafBlockProcessorParagraph.match_tabbed_whitespace(
                    extracted_whitespace, corrected_extracted_whitespace
                )
                _ = (detabified_prefix, detabified_suffix, corrected_prefix)
                POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
                if split_tab:
                    LeafBlockProcessorParagraph.adjust_block_quote_indent_for_tab(
                        parser_state
                    )

                corrected_extracted_whitespace = corrected_suffix
            original_line = original_line[first_non_whitespace_character_index:]
        else:
            corrected_extracted_whitespace = extracted_whitespace
        return corrected_extracted_whitespace, original_line

    @staticmethod
    def adjust_block_quote_indent_for_tab(parser_state: ParserState) -> None:
        """
        Adjust the last block quote for a tab.
        """

        POGGER.debug("parser_state=:$:", parser_state.token_stack)
        stack_token_index = len(parser_state.token_stack) - 1
        while (
            stack_token_index > 0
            and not parser_state.token_stack[stack_token_index].is_block_quote
            and not parser_state.token_stack[stack_token_index].is_list
        ):
            stack_token_index -= 1
        POGGER.debug("parser_state=:$:", parser_state.token_stack[stack_token_index])
        assert parser_state.token_stack[stack_token_index].is_block_quote

        block_quote_token = cast(
            BlockQuoteMarkdownToken,
            parser_state.token_stack[stack_token_index].matching_markdown_token,
        )
        POGGER.debug(
            "parser_state=:$:",
            block_quote_token,
        )
        block_quote_leading_spaces = block_quote_token.leading_spaces
        assert block_quote_leading_spaces is not None
        POGGER.debug("block_quote_leading_spaces=:$:", block_quote_leading_spaces)
        block_quote_leading_spaces_index = block_quote_leading_spaces.rfind("\n")
        last_block_quote_leading_space = block_quote_leading_spaces[
            block_quote_leading_spaces_index + 1 :
        ]
        POGGER.debug(
            "last_block_quote_leading_space=:$:", last_block_quote_leading_space
        )
        assert last_block_quote_leading_space.endswith(" ")
        last_block_quote_leading_space = last_block_quote_leading_space[:-1]
        POGGER.debug(
            "last_block_quote_leading_space=:$:", last_block_quote_leading_space
        )
        POGGER.debug(
            "parser_state=:$:",
            block_quote_token,
        )
        block_quote_token.remove_last_leading_space()
        POGGER.debug(
            "parser_state=:$:",
            block_quote_token,
        )
        block_quote_token.add_leading_spaces(last_block_quote_leading_space)
        POGGER.debug(
            "parser_state=:$:",
            block_quote_token,
        )

    @staticmethod
    def match_tabbed_whitespace(
        extracted_whitespace: str, corrected_extracted_whitespace: str
    ) -> Tuple[str, str, str, str, bool]:
        """
        Match any tabbed whitespace with its non-tabbed counterpart.
        """
        assert corrected_extracted_whitespace != ""
        detabified_suffix = ""
        detabified_prefix = ""
        corrected_prefix = ""
        corrected_suffix = corrected_extracted_whitespace
        index_from_end = len(corrected_extracted_whitespace) - 1
        while index_from_end >= 0 and len(detabified_suffix) < len(
            extracted_whitespace
        ):
            corrected_suffix = corrected_extracted_whitespace[index_from_end:]
            corrected_prefix = corrected_extracted_whitespace[:index_from_end]
            POGGER.debug(
                "index_from_end=:$: of :$:",
                index_from_end,
                len(corrected_extracted_whitespace),
            )
            POGGER.debug("corrected_suffix=:$:", corrected_suffix)
            POGGER.debug("corrected_prefix=:$:", corrected_prefix)
            detabified_prefix = ParserHelper.detabify_string(corrected_prefix)
            POGGER.debug("detabified_prefix=:$:", detabified_prefix)
            detabified_suffix = ParserHelper.detabify_string(
                corrected_suffix, additional_start_delta=len(detabified_prefix)
            )
            POGGER.debug("detabified_suffix=:$:", detabified_suffix)
            if len(detabified_suffix) < len(extracted_whitespace):
                index_from_end -= 1
        assert index_from_end >= 0

        split_tab = detabified_suffix != extracted_whitespace
        if split_tab:
            assert detabified_prefix.endswith(">")
            assert detabified_suffix[1:] == extracted_whitespace

        return (
            detabified_prefix,
            detabified_suffix,
            corrected_prefix,
            corrected_suffix,
            split_tab,
        )

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

    # pylint: disable=too-many-locals
    @staticmethod
    def __handle_paragraph_prep(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        original_line: str,
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
            if "\t" in original_line:
                POGGER.debug(">>text_to_parse>>$>>", position_marker.text_to_parse)
                POGGER.debug(">>index_number>>$>>", position_marker.index_number)

                (
                    rest_of_string,
                    rest_of_string_index,
                ) = ParserHelper.find_detabify_string(
                    original_line,
                    position_marker.text_to_parse[position_marker.index_number :],
                )
                POGGER.debug(">>rest_of_string>>$>>", rest_of_string)
                POGGER.debug(">>rest_of_string_index>>$>>", rest_of_string_index)
                assert rest_of_string is not None
                prefix = original_line[:rest_of_string_index]
                if prefix and "\t" in prefix:
                    (
                        detabified_prefix,
                        detabified_suffix,
                        corrected_prefix,
                        corrected_suffix,
                        split_tab,
                    ) = LeafBlockProcessorParagraph.match_tabbed_whitespace(
                        extracted_whitespace, prefix
                    )
                    _ = (detabified_prefix, detabified_suffix, corrected_prefix)
                    POGGER.debug(">>detabified_prefix>>$>>", detabified_prefix)
                    POGGER.debug(">>detabified_suffix>>$>>", detabified_suffix)
                    POGGER.debug(">>corrected_prefix>>$>>", corrected_prefix)
                    POGGER.debug(">>corrected_suffix>>$>>", corrected_suffix)
                    POGGER.debug(">>split_tab>>$>>", split_tab)
                    extracted_whitespace = corrected_suffix
                    if split_tab:
                        LeafBlockProcessorParagraph.adjust_block_quote_indent_for_tab(
                            parser_state
                        )

            new_paragraph_token = ParagraphMarkdownToken(
                extracted_whitespace, position_marker
            )
            parser_state.token_stack.append(ParagraphStackToken(new_paragraph_token))
            new_tokens.append(new_paragraph_token)
            extracted_whitespace = ""
            did_add_paragraph_token = True
        return new_tokens, extracted_whitespace, did_add_paragraph_token

    # pylint: enable=too-many-locals

    @staticmethod
    def check_for_list_in_process(parser_state: ParserState) -> Tuple[bool, int]:
        """
        From the end of the stack, check to see if there is already a list in progress.
        """

        stack_index = len(parser_state.token_stack) - 1

        while stack_index >= 0 and not parser_state.token_stack[stack_index].is_list:
            stack_index -= 1

        return stack_index >= 0, stack_index
