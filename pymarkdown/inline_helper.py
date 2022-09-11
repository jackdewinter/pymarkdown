"""
Module to help with the parsing of inline elements.
"""
import json
import logging
import os
import re
import string
from typing import Dict, List, Optional, Tuple, cast

from pymarkdown.bad_tokenization_error import BadTokenizationError
from pymarkdown.container_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.html_helper import HtmlHelper
from pymarkdown.inline_markdown_token import (
    EmailAutolinkMarkdownToken,
    HardBreakMarkdownToken,
    InlineCodeSpanMarkdownToken,
    RawHtmlMarkdownToken,
    UriAutolinkMarkdownToken,
)
from pymarkdown.inline_request import InlineRequest
from pymarkdown.inline_response import InlineResponse
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


class InlineHelper:
    """
    Class to help with the parsing of inline elements.
    """

    __valid_email_regex = (
        "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}"
        + "[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    )

    __scheme_end_character = ":"
    __valid_scheme_characters = f"{string.ascii_letters}{string.digits}.-+"

    __backslash_punctuation = "!\"#$%&'()*+,-./:;<=>?@[]^_`{|}~\\"
    __html_character_escape_map = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
        '"': "&quot;",
    }

    angle_bracket_start = "<"
    __angle_bracket_end = ">"
    code_span_bounds = "`"
    backslash_character = "\\"
    __entity_map: Dict[str, str] = {}
    character_reference_start_character = "&"
    __numeric_character_reference_start_character = "#"
    __hex_character_reference_start_character = "xX"
    __character_reference_end_character = ";"
    __invalid_reference_character_substitute = "\ufffd"
    __line_end_whitespace = ParserHelper.space_character
    __valid_backslash_sequence_starts = (
        f"{backslash_character}{character_reference_start_character}"
    )

    __ascii_letters_and_digits = f"{string.ascii_letters}{string.digits}"

    __skip_html5_entities_ending_with = ";"

    __entities_file_name = "entities.json"

    @staticmethod
    def initialize(resource_path: str) -> None:
        """
        Initialize the inline subsystem.
        """
        InlineHelper.__entity_map = InlineHelper.__load_entity_map(resource_path)

    @staticmethod
    def handle_inline_backslash(
        inline_request: InlineRequest, add_text_signature: bool = True
    ) -> InlineResponse:
        """
        Handle the inline case of having a backslash.
        """

        inline_response = InlineResponse()
        (
            inline_response.new_index,
            inline_response.new_string,
            inline_response.new_string_unresolved,
        ) = (inline_request.next_index + 1, "", "")
        if (
            inline_response.new_index >= len(inline_request.source_text)
            or inline_request.source_text[inline_response.new_index]
            == ParserHelper.newline_character
        ):
            inline_response.new_string, inline_response.new_string_unresolved = (
                InlineHelper.backslash_character,
                inline_response.new_string,
            )
        else:
            if (
                inline_request.source_text[inline_response.new_index]
                in InlineHelper.__backslash_punctuation
            ):
                inline_response.new_string = (
                    ParserHelper.backslash_escape_sequence if add_text_signature else ""
                ) + inline_request.source_text[inline_response.new_index]
                inline_response.new_string_unresolved = (
                    InlineHelper.backslash_character + inline_response.new_string
                )
            else:
                inline_response.new_string = (
                    InlineHelper.backslash_character
                    + inline_request.source_text[inline_response.new_index]
                )
                inline_response.new_string_unresolved = inline_response.new_string
            inline_response.new_index += 1

        inline_response.delta_line_number, inline_response.delta_column_number = (
            0,
            inline_response.new_index - inline_request.next_index,
        )
        return inline_response

    @staticmethod
    def handle_character_reference(inline_request: InlineRequest) -> InlineResponse:
        """
        Handle a generic character reference.
        """
        inline_response = InlineResponse()
        inline_response.new_index, inline_response.new_string, source_text_size = (
            inline_request.next_index + 1,
            "",
            len(inline_request.source_text),
        )
        assert inline_response.new_index is not None
        if (
            inline_response.new_index < source_text_size
            and inline_request.source_text[inline_response.new_index]
            == InlineHelper.__numeric_character_reference_start_character
        ):
            InlineHelper.__handle_numeric_character_reference(
                inline_request, inline_response
            )
        else:
            InlineHelper.__handle_non_numeric_character_reference(
                inline_request, inline_response, source_text_size
            )
        inline_response.delta_line_number, inline_response.delta_column_number = (
            0,
            inline_response.new_index - inline_request.next_index,
        )
        return inline_response

    @staticmethod
    def __handle_numeric_character_reference(
        inline_request: InlineRequest, inline_response: InlineResponse
    ) -> None:
        original_new_index = inline_response.new_index
        POGGER.debug("here")
        assert inline_response.new_index is not None
        (
            inline_response.new_string,
            inline_response.new_index,
            inline_response.original_string,
        ) = InlineHelper.__handle_numeric_character_reference_inner(
            inline_request.source_text, inline_response.new_index
        )
        inline_response.new_string_unresolved = (
            InlineHelper.character_reference_start_character
            + inline_request.source_text[original_new_index : inline_response.new_index]
        )
        POGGER.debug("here-->$<--", inline_response.new_string)
        POGGER.debug("here-->$<--", inline_response.new_string_unresolved)

    @staticmethod
    def __handle_non_numeric_character_reference(
        inline_request: InlineRequest,
        inline_response: InlineResponse,
        source_text_size: int,
    ) -> None:
        POGGER.debug("there")
        assert inline_response.new_index is not None
        end_index, collected_string = ParserHelper.collect_while_one_of_characters(
            inline_request.source_text,
            inline_response.new_index,
            InlineHelper.__ascii_letters_and_digits,
        )
        if collected_string:
            assert end_index is not None
            collected_string = (
                f"{InlineHelper.character_reference_start_character}{collected_string}"
            )
            if (
                end_index < source_text_size
                and inline_request.source_text[end_index]
                == InlineHelper.__character_reference_end_character
            ):
                end_index += 1
                collected_string += InlineHelper.__character_reference_end_character
                if collected_string in InlineHelper.__entity_map:
                    inline_response.new_string_unresolved = collected_string
                    inline_response.original_string = collected_string
                    collected_string = InlineHelper.__entity_map[collected_string]
            inline_response.new_string, inline_response.new_index = (
                collected_string,
                end_index,
            )
            POGGER.debug("there-->$<--", inline_response.new_string)
            POGGER.debug("there-->$<--", inline_response.new_string_unresolved)
        else:
            inline_response.new_string = (
                InlineHelper.character_reference_start_character
            )

    @staticmethod
    def handle_backslashes(source_text: str) -> str:
        """
        Handle the processing of backslashes for anything other than the text
        blocks, which have additional needs for parsing.
        """

        start_index, string_parts = 0, []
        next_index = ParserHelper.index_any_of(
            source_text, InlineHelper.__valid_backslash_sequence_starts, start_index
        )
        while next_index != -1:
            string_parts.append(source_text[start_index:next_index])
            current_char = source_text[next_index]

            inline_request = InlineRequest(source_text, next_index)
            POGGER.debug("handle_backslashes>>$>>", current_char)
            if current_char == InlineHelper.backslash_character:
                inline_response = InlineHelper.handle_inline_backslash(
                    inline_request, add_text_signature=False
                )
            else:
                assert (
                    source_text[next_index]
                    == InlineHelper.character_reference_start_character
                )
                inline_response = InlineHelper.handle_character_reference(
                    inline_request
                )
            new_string, new_index = (
                inline_response.new_string,
                inline_response.new_index,
            )
            assert new_string is not None
            assert new_index is not None
            POGGER.debug("handle_backslashes<<$<<$", new_string, new_index)
            string_parts.append(new_string)
            start_index = new_index
            next_index = ParserHelper.index_any_of(
                source_text, InlineHelper.__valid_backslash_sequence_starts, start_index
            )

        if start_index < len(source_text):
            string_parts.append(source_text[start_index:])
        return "".join(string_parts)

    @staticmethod
    def append_text(
        string_to_append_to: str,
        text_to_append: str,
        alternate_escape_map: Optional[Dict[str, str]] = None,
        add_text_signature: bool = True,
    ) -> str:
        """
        Append the text to the given string, doing any needed encoding as we go.
        """

        if not alternate_escape_map:
            alternate_escape_map = InlineHelper.__html_character_escape_map
        key_map = "".join(alternate_escape_map.keys())
        start_index, text_parts = 0, [string_to_append_to]
        next_index = ParserHelper.index_any_of(text_to_append, key_map, start_index)
        while next_index != -1:
            escaped_part = alternate_escape_map[text_to_append[next_index]]
            text_parts.extend(
                [
                    text_to_append[start_index:next_index],
                    ParserHelper.create_replacement_markers(
                        text_to_append[next_index], escaped_part
                    )
                    if add_text_signature
                    else escaped_part,
                ]
            )

            start_index = next_index + 1
            next_index = ParserHelper.index_any_of(text_to_append, key_map, start_index)

        if start_index < len(text_to_append):
            text_parts.append(text_to_append[start_index:])

        return "".join(text_parts)

    @staticmethod
    def handle_inline_backtick(inline_request: InlineRequest) -> InlineResponse:
        """
        Handle the inline case of backticks for code spans.
        """
        POGGER.debug("before_collect>$", inline_request.next_index)
        (
            new_index,
            extracted_start_backticks,
        ) = ParserHelper.collect_while_one_of_characters(
            inline_request.source_text,
            inline_request.next_index,
            InlineHelper.code_span_bounds,
        )
        POGGER.debug("after_collect>$>$", new_index, extracted_start_backticks)

        assert new_index is not None
        assert extracted_start_backticks is not None
        extracted_start_backticks_size, end_backtick_start_index = (
            len(extracted_start_backticks),
            inline_request.source_text.find(extracted_start_backticks, new_index),
        )
        while end_backtick_start_index != -1:
            (
                end_backticks_index,
                end_backticks_attempt,
            ) = ParserHelper.collect_while_one_of_characters(
                inline_request.source_text,
                end_backtick_start_index,
                InlineHelper.code_span_bounds,
            )
            assert end_backticks_attempt is not None
            if len(end_backticks_attempt) == extracted_start_backticks_size:
                break
            end_backtick_start_index = inline_request.source_text.find(
                extracted_start_backticks, end_backticks_index
            )

        inline_response = InlineHelper.__build_backtick_response(
            inline_request,
            end_backtick_start_index,
            extracted_start_backticks,
            new_index,
            extracted_start_backticks_size,
        )

        assert inline_response.new_index is not None
        POGGER.debug(
            ">>delta_line_number>>$<<",
            inline_response.delta_line_number,
        )
        POGGER.debug(
            ">>delta_column_number>>$<<",
            inline_response.delta_column_number,
        )
        if inline_response.delta_line_number == -1:
            inline_response.delta_line_number, inline_response.delta_column_number = (
                0,
                inline_response.new_index - inline_request.next_index,
            )
        return inline_response

    @staticmethod
    def __build_backtick_response(
        inline_request: InlineRequest,
        end_backtick_start_index: int,
        extracted_start_backticks: str,
        new_index: int,
        extracted_start_backticks_size: int,
    ) -> InlineResponse:
        inline_response = InlineResponse()
        inline_response.delta_line_number = -1

        if end_backtick_start_index == -1:
            inline_response.new_string, inline_response.new_index = (
                extracted_start_backticks,
                new_index,
            )
        else:
            (
                between_text,
                original_between_text,
                leading_whitespace,
                trailing_whitespace,
            ) = InlineHelper.__calculate_backtick_between_text(
                inline_request, new_index, end_backtick_start_index
            )

            POGGER.debug("between_text>>$<<", between_text)
            between_text = InlineHelper.append_text("", between_text)
            POGGER.debug("between_text>>$<<", between_text)
            POGGER.debug(
                "leading_whitespace>>$<<",
                leading_whitespace,
            )
            POGGER.debug(
                "trailing_whitespace>>$<<",
                trailing_whitespace,
            )
            end_backtick_start_index += extracted_start_backticks_size
            inline_response.new_string, inline_response.new_index = (
                "",
                end_backtick_start_index,
            )
            assert inline_request.line_number is not None
            assert inline_request.column_number is not None
            assert inline_request.remaining_line is not None
            new_column_number = inline_request.column_number + len(
                inline_request.remaining_line
            )
            POGGER.debug(">>new_column_number>>$", new_column_number)

            inline_response.new_tokens = [
                InlineCodeSpanMarkdownToken(
                    between_text,
                    extracted_start_backticks,
                    leading_whitespace,
                    trailing_whitespace,
                    inline_request.line_number,
                    new_column_number,
                )
            ]

            if ParserHelper.newline_character in original_between_text:
                (
                    inline_response.delta_line_number,
                    inline_response.delta_column_number,
                ) = ParserHelper.calculate_deltas(
                    f"{original_between_text}{extracted_start_backticks}"
                )
        return inline_response

    @staticmethod
    def modify_end_string(
        end_string: Optional[str], removed_end_whitespace: str
    ) -> str:
        """
        Modify the string at the end of the paragraph.
        """
        return (
            f"{removed_end_whitespace}{ParserHelper.newline_character}"
            if end_string is None
            else f"{end_string}{removed_end_whitespace}{ParserHelper.newline_character}"
        )

    @staticmethod
    def __calculate_backtick_between_text(
        inline_request: InlineRequest, new_index: int, end_backtick_start_index: int
    ) -> Tuple[str, str, str, str]:
        POGGER.debug("inline_request.source_text>>$<<", inline_request.source_text)
        POGGER.debug("new_index>>$<<", new_index)
        POGGER.debug("end_backtick_start_index>>$<<", end_backtick_start_index)
        between_text = inline_request.source_text[new_index:end_backtick_start_index]
        original_between_text, leading_whitespace, trailing_whitespace = (
            between_text,
            "",
            "",
        )
        POGGER.debug(
            "after_collect>$>>$>>$<<",
            between_text,
            end_backtick_start_index,
            inline_request.source_text[end_backtick_start_index:],
        )
        POGGER.debug("between_text>>$<<", between_text)
        if (
            len(between_text) > 2
            and between_text[0]
            in [
                ParserHelper.space_character,
                ParserHelper.newline_character,
            ]
            and between_text[-1]
            in [
                ParserHelper.space_character,
                ParserHelper.newline_character,
            ]
        ):
            stripped_between_attempt = between_text[1:-1]
            if len(stripped_between_attempt.strip()) != 0:
                leading_whitespace, trailing_whitespace = (
                    between_text[0],
                    between_text[-1],
                )
                between_text = stripped_between_attempt

        replaced_newline = ParserHelper.create_replacement_markers(
            ParserHelper.newline_character, ParserHelper.space_character
        )
        POGGER.debug("between_text>>$<<", between_text)
        between_text = ParserHelper.escape_special_characters(between_text)
        POGGER.debug("between_text>>$<<", between_text)
        POGGER.debug(
            "leading_whitespace>>$<<",
            leading_whitespace,
        )
        POGGER.debug(
            "trailing_whitespace>>$<<",
            trailing_whitespace,
        )
        between_text, leading_whitespace, trailing_whitespace = (
            between_text.replace(ParserHelper.newline_character, replaced_newline),
            leading_whitespace.replace(
                ParserHelper.newline_character, replaced_newline
            ),
            trailing_whitespace.replace(
                ParserHelper.newline_character, replaced_newline
            ),
        )
        return (
            between_text,
            original_between_text,
            leading_whitespace,
            trailing_whitespace,
        )

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def handle_line_end(
        remaining_line: str,
        end_string: Optional[str],
        current_string: str,
        inline_blocks: List[MarkdownToken],
        is_setext: bool,
        line_number: int,
        column_number: int,
        coalesced_stack: List[MarkdownToken],
        tabified_text: Optional[str],
    ) -> Tuple[str, Optional[str], List[MarkdownToken], str, Optional[str], str]:
        """
        Handle the inline case of having the end of line character encountered.
        """
        new_tokens: List[MarkdownToken] = []

        POGGER.debug(">>current_string>>$>>", current_string)
        POGGER.debug(">>end_string>>$>>", end_string)
        POGGER.debug(">>remaining_line>>$>>", remaining_line)
        _, last_non_whitespace_index = ParserHelper.collect_backwards_while_spaces(
            remaining_line, -1
        )
        POGGER.debug(">>last_non_whitespace_index>>$", last_non_whitespace_index)
        removed_end_whitespace = remaining_line[last_non_whitespace_index:]
        remaining_line = remaining_line[:last_non_whitespace_index]
        POGGER.debug(">>removed_end_whitespace>>$>>", removed_end_whitespace)
        POGGER.debug(">>remaining_line>>$>>", remaining_line)

        POGGER.debug(">>current_string>>$>>", current_string)
        (append_to_current_string, removed_end_whitespace_size, adj_hard_column,) = (
            ParserHelper.newline_character,
            len(removed_end_whitespace),
            column_number + len(remaining_line),
        )
        whitespace_to_add: Optional[str] = None
        POGGER.debug(
            ">>len(r_e_w)>>$>>rem>>$>>",
            removed_end_whitespace_size,
            remaining_line,
        )

        is_proper_hard_break = InlineHelper.__is_proper_hard_break(
            current_string, removed_end_whitespace_size
        )

        (
            current_string,
            whitespace_to_add,
            append_to_current_string,
            end_string,
            remaining_line,
        ) = InlineHelper.__select_line_ending(
            new_tokens,
            is_proper_hard_break,
            line_number,
            adj_hard_column,
            current_string,
            removed_end_whitespace,
            removed_end_whitespace_size,
            whitespace_to_add,
            append_to_current_string,
            end_string,
            remaining_line,
            inline_blocks,
            is_setext,
            tabified_text,
        )

        if coalesced_stack and coalesced_stack[-1].is_block_quote_start:
            block_quote_token = cast(BlockQuoteMarkdownToken, coalesced_stack[-1])
            block_quote_token.leading_text_index += 1

        return (
            append_to_current_string,
            whitespace_to_add,
            new_tokens,
            remaining_line,
            end_string,
            current_string,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __is_proper_hard_break(
        current_string: str, removed_end_whitespace_size: int
    ) -> bool:
        POGGER.debug("__is_proper_hard_break>>current_string>>$>>", current_string)
        POGGER.debug("removed_end_whitespace_size>>$>>", removed_end_whitespace_size)

        current_string_size = len(current_string)
        if (
            removed_end_whitespace_size == 0
            and current_string_size
            and current_string[current_string_size - 1]
            == InlineHelper.backslash_character
        ):
            POGGER.debug(">>$<<", current_string)
            modified_current_string = current_string[:-1]
            is_proper_hard_break = modified_current_string[-2:] != "\\\b"
            POGGER.debug(">>$<<", is_proper_hard_break)
        else:
            is_proper_hard_break = False

        POGGER.debug("__is_proper_hard_break>>$>>", is_proper_hard_break)
        return is_proper_hard_break

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __select_line_ending(
        new_tokens: List[MarkdownToken],
        is_proper_hard_break: bool,
        line_number: int,
        adj_hard_column: int,
        current_string: str,
        removed_end_whitespace: str,
        removed_end_whitespace_size: int,
        whitespace_to_add: Optional[str],
        append_to_current_string: str,
        end_string: Optional[str],
        remaining_line: str,
        inline_blocks: List[MarkdownToken],
        is_setext: bool,
        tabified_text: Optional[str],
    ) -> Tuple[str, Optional[str], str, Optional[str], str]:
        POGGER.debug(">>removed_end_whitespace>:$:<", removed_end_whitespace)
        POGGER.debug(">>tabified_text>:$:<", tabified_text)
        is_proper_end = not tabified_text or tabified_text.endswith("  ")
        if is_proper_hard_break:
            POGGER.debug(">>proper hard break")
            new_tokens.append(
                HardBreakMarkdownToken(
                    InlineHelper.backslash_character, line_number, adj_hard_column - 1
                )
            )
            current_string, whitespace_to_add = current_string[:-1], None
            append_to_current_string = ""
        elif removed_end_whitespace_size >= 2 and is_proper_end:
            POGGER.debug(">>whitespace hard break")
            new_tokens.append(
                HardBreakMarkdownToken(
                    removed_end_whitespace, line_number, adj_hard_column
                )
            )
            whitespace_to_add = None
            append_to_current_string = ""
        else:
            POGGER.debug(">>normal end")
            end_string, remaining_line = \
                InlineHelper.__select_line_ending_normal(is_setext, inline_blocks, current_string, removed_end_whitespace, end_string, remaining_line)

        POGGER.debug(
            "<<append_to_current_string<<$<<",
            append_to_current_string,
        )
        POGGER.debug(
            "<<whitespace_to_add<<$<<",
            whitespace_to_add,
        )
        POGGER.debug("<<remaining_line<<$<<", remaining_line)
        POGGER.debug("<<end_string<<$<<", end_string)
        POGGER.debug("<<current_string<<$<<", current_string)
        return (
            current_string,
            whitespace_to_add,
            append_to_current_string,
            end_string,
            remaining_line,
        )

    # pylint: enable=too-many-arguments, too-many-locals
    @staticmethod
    def __select_line_ending_normal(is_setext, inline_blocks, current_string, removed_end_whitespace, end_string, remaining_line):
        # POGGER.debug("<<is_setext<<$<<", is_setext)
        # POGGER.debug("<<inline_blocks<<$<<", inline_blocks)
        # POGGER.debug("<<current_string<<$<<", current_string)
        # POGGER.debug("<<remaining_line<<$<<", remaining_line)
        # POGGER.debug("<<end_string<<$<<", end_string)
        # POGGER.debug("<<removed_end_whitespace<<$<<", removed_end_whitespace)
        if (
            is_setext
            and inline_blocks
            and inline_blocks[-1].is_inline_hard_break
            and not current_string
        ):
            new_index, ex_ws = ParserHelper.extract_spaces(remaining_line, 0)
            # POGGER.debug("<<new_index<<$<<", new_index)
            # POGGER.debug("<<ex_ws<<$<<", ex_ws)
            assert new_index
            end_string = f"{ex_ws}{ParserHelper.whitespace_split_character}"
            remaining_line = remaining_line[new_index:]

        end_string = InlineHelper.modify_end_string(
            end_string, removed_end_whitespace
        )
        # POGGER.debug("<<end_string<<$<<", end_string)
        return end_string, remaining_line

    @staticmethod
    def extract_bounded_string(
        source_text: str,
        new_index: int,
        close_character: str,
        start_character: Optional[str],
    ) -> Tuple[Optional[int], Optional[str]]:
        """
        Extract a string that is bounded by some manner of characters.
        """
        break_characters = (
            f"{InlineHelper.backslash_character}{close_character}{start_character}"
            if start_character
            else f"{InlineHelper.backslash_character}{close_character}"
        )
        nesting_level: int = 0
        POGGER.debug(
            "extract_bounded_string>>new_index>>$>>data>>$>>",
            new_index,
            source_text[new_index:],
        )
        next_index, data = ParserHelper.collect_until_one_of_characters(
            source_text, new_index, break_characters
        )
        assert data is not None
        extracted_parts: List[str] = [data]
        POGGER.debug(
            ">>next_index1>>$>>data>>$>>",
            next_index,
            data,
        )
        assert next_index is not None
        while next_index < len(source_text) and not (
            source_text[next_index] == close_character and nesting_level == 0
        ):
            (
                next_index,
                nesting_level,
            ) = InlineHelper.__handle_next_extract_bounded_string_item(
                source_text,
                next_index,
                extracted_parts,
                start_character,
                nesting_level,
                close_character,
                break_characters,
            )
            assert next_index is not None
            POGGER.debug(
                "back>>next_index>>$>>data>>$>>",
                next_index,
                data,
            )
        POGGER.debug(
            ">>next_index2>>$>>data>>$>>",
            next_index,
            data,
        )
        assert next_index is not None
        if (
            ParserHelper.is_character_at_index(source_text, next_index, close_character)
            and nesting_level == 0
        ):
            POGGER.debug("extract_bounded_string>>found-close")
            return next_index + 1, "".join(extracted_parts)
        POGGER.debug(
            "extract_bounded_string>>ran out of string>>next_index>>$", next_index
        )
        return next_index, None

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_next_extract_bounded_string_item(
        source_text: str,
        next_index: int,
        extracted_parts: List[str],
        start_character: Optional[str],
        nesting_level: int,
        close_character: str,
        break_characters: str,
    ) -> Tuple[int, int]:

        if ParserHelper.is_character_at_index(
            source_text, next_index, InlineHelper.backslash_character
        ):
            POGGER.debug("pre-back>>next_index>>$>>", next_index)
            old_index = next_index

            inline_request = InlineRequest(source_text, next_index)
            inline_response = InlineHelper.handle_inline_backslash(inline_request)
            assert inline_response.new_index is not None
            next_index = inline_response.new_index
            extracted_parts.append(source_text[old_index:next_index])
        elif start_character is not None and ParserHelper.is_character_at_index(
            source_text, next_index, start_character
        ):
            POGGER.debug("pre-start>>next_index>>$>>", next_index)
            extracted_parts.append(start_character)
            next_index += 1
            nesting_level += 1
        else:
            assert ParserHelper.is_character_at_index(
                source_text, next_index, close_character
            )
            POGGER.debug("pre-close>>next_index>>$>>", next_index)
            extracted_parts.append(close_character)
            next_index += 1
            nesting_level -= 1
        nexter_index, new_data = ParserHelper.collect_until_one_of_characters(
            source_text, next_index, break_characters
        )
        assert new_data is not None
        assert nexter_index is not None
        extracted_parts.append(new_data)
        return nexter_index, nesting_level

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_numeric_character_reference_hex(
        new_index: int, source_text: str, source_text_size: int
    ) -> Tuple[str, int, int]:
        hex_char = source_text[new_index]
        new_index += 1
        end_index, collected_string = ParserHelper.collect_while_one_of_characters(
            source_text, new_index, string.hexdigits
        )

        assert end_index is not None
        assert collected_string is not None
        POGGER.debug(
            "&#x>>a>>$>>b>>$>>$", end_index, collected_string, source_text_size
        )

        delta = end_index - new_index
        POGGER.debug("delta>>$>>", delta)
        translated_reference = int(collected_string, 16) if 1 <= delta <= 6 else -1
        new_string, new_index = (
            f"{InlineHelper.character_reference_start_character}"
            + f"{InlineHelper.__numeric_character_reference_start_character}{hex_char}{collected_string}"
        ), end_index

        return new_string, new_index, translated_reference

    @staticmethod
    def __handle_numeric_character_reference_decimal(
        new_index: int, source_text: str, source_text_size: int
    ) -> Tuple[str, int, int]:
        end_index, collected_string = ParserHelper.collect_while_one_of_characters(
            source_text, new_index, string.digits
        )

        assert end_index is not None
        assert collected_string is not None
        POGGER.debug("&#>>a>>$>>b>>$>>$", end_index, collected_string, source_text_size)

        delta = end_index - new_index
        POGGER.debug("delta>>$>>", delta)
        translated_reference = int(collected_string) if 1 <= delta <= 7 else -1
        new_string, new_index = (
            f"{InlineHelper.character_reference_start_character}"
            + f"{InlineHelper.__numeric_character_reference_start_character}{collected_string}"
        ), end_index

        return new_string, new_index, translated_reference

    @staticmethod
    def __handle_numeric_character_reference_inner(
        source_text: str, new_index: int
    ) -> Tuple[str, int, Optional[str]]:
        """
        Handle a character reference that is numeric in nature.
        """

        original_reference, new_index, source_text_size = (
            None,
            new_index + 1,
            len(source_text),
        )
        if new_index < source_text_size and (
            source_text[new_index]
            in InlineHelper.__hex_character_reference_start_character
        ):
            (
                new_string,
                new_index,
                translated_reference,
            ) = InlineHelper.__handle_numeric_character_reference_hex(
                new_index, source_text, source_text_size
            )
        else:
            (
                new_string,
                new_index,
                translated_reference,
            ) = InlineHelper.__handle_numeric_character_reference_decimal(
                new_index, source_text, source_text_size
            )

        if (
            translated_reference >= 0
            and new_index < source_text_size
            and source_text[new_index]
            == InlineHelper.__character_reference_end_character
        ):
            new_index += 1
            original_reference, new_string = f"{new_string};", (
                InlineHelper.__invalid_reference_character_substitute
                if translated_reference == 0
                else chr(translated_reference)
            )
        return new_string, new_index, original_reference

    @staticmethod
    def __load_entity_map(resource_path: str) -> Dict[str, str]:
        """
        Load the entity map, refreshed from https://html.spec.whatwg.org/entities.json
        into a dict that was can use.
        """

        master_entities_file = os.path.join(
            resource_path, InlineHelper.__entities_file_name
        )
        try:
            with open(
                os.path.abspath(master_entities_file), encoding="utf-8"
            ) as infile:
                results_dictionary = json.load(infile)
        except json.decoder.JSONDecodeError as this_exception:
            error_message = (
                f"Named character entity map file '{master_entities_file}' "
                + f"is not a valid JSON file ({this_exception})."
            )
            raise BadTokenizationError(error_message) from this_exception
        except IOError as this_exception:
            error_message = (
                f"Named character entity map file '{master_entities_file}' "
                + f"was not loaded ({this_exception})."
            )
            raise BadTokenizationError(error_message) from this_exception

        approved_entity_map = {}
        for next_name, char_entity in results_dictionary.items():

            # Downloaded file is for HTML5, which includes some names that do
            # not end with ";".  These are excluded.
            if next_name[-1] != InlineHelper.__skip_html5_entities_ending_with:
                continue

            entity_characters = char_entity["characters"]
            entity_codepoints = char_entity["codepoints"]

            # The only entities we should encounter either have a length of 1 or 2
            if len(entity_characters) == 1:
                assert len(entity_codepoints) == 1
            else:
                assert len(entity_codepoints) == 2
                assert ord(entity_characters[1]) == entity_codepoints[1]
            assert ord(entity_characters[0]) == entity_codepoints[0]
            approved_entity_map[next_name] = entity_characters
        return approved_entity_map

    @staticmethod
    def __parse_valid_email_autolink(
        text_to_parse: str, line_number: int, column_number: int
    ) -> Optional[EmailAutolinkMarkdownToken]:
        """
        Parse a possible email autolink and determine if it is valid.
        """
        return (
            EmailAutolinkMarkdownToken(text_to_parse, line_number, column_number)
            if re.match(InlineHelper.__valid_email_regex, text_to_parse)
            else None
        )

    @staticmethod
    def __parse_valid_uri_autolink(
        text_to_parse: str, line_number: int, column_number: int
    ) -> Optional[UriAutolinkMarkdownToken]:
        """
        Parse a possible uri autolink and determine if it is valid.
        """

        if (
            InlineHelper.angle_bracket_start not in text_to_parse
            and text_to_parse[0] in string.ascii_letters
        ):
            path_index, uri_scheme = ParserHelper.collect_while_one_of_characters(
                text_to_parse, 1, InlineHelper.__valid_scheme_characters
            )
            assert path_index is not None
            uri_scheme, text_to_parse_size = f"{text_to_parse[0]}{uri_scheme}", len(
                text_to_parse
            )
            if (
                2 <= len(uri_scheme) <= 32
                and path_index < text_to_parse_size
                and text_to_parse[path_index] == InlineHelper.__scheme_end_character
            ):
                path_index += 1
                while (
                    path_index < text_to_parse_size
                    and ord(text_to_parse[path_index]) > 32
                ):
                    path_index += 1
                if path_index == text_to_parse_size:
                    return UriAutolinkMarkdownToken(
                        text_to_parse, line_number, column_number
                    )
        else:
            uri_scheme, path_index = "", -1
        return None

    @staticmethod
    def handle_angle_brackets(inline_request: InlineRequest) -> InlineResponse:
        """
        Given an open angle bracket, determine which of the three possibilities it is.
        """
        closing_angle_index = inline_request.source_text.find(
            InlineHelper.__angle_bracket_end, inline_request.next_index
        )
        if closing_angle_index not in (-1, inline_request.next_index + 1):

            between_brackets, remaining_line = (
                inline_request.source_text[
                    inline_request.next_index + 1 : closing_angle_index
                ],
                inline_request.source_text[inline_request.next_index + 1 :],
            )
            closing_angle_index += 1

            assert inline_request.line_number is not None
            assert inline_request.column_number is not None
            assert inline_request.remaining_line is not None
            new_column_number = inline_request.column_number + len(
                inline_request.remaining_line
            )

            new_token: Optional[
                MarkdownToken
            ] = InlineHelper.__parse_valid_uri_autolink(
                between_brackets, inline_request.line_number, new_column_number
            )
            if not new_token:
                new_token = InlineHelper.__parse_valid_email_autolink(
                    between_brackets, inline_request.line_number, new_column_number
                )
            if not new_token:
                new_token, after_index = HtmlHelper.parse_raw_html(
                    between_brackets,
                    remaining_line,
                    inline_request.line_number,
                    new_column_number,
                    inline_request,
                )
                if after_index != -1:
                    closing_angle_index = after_index + inline_request.next_index + 1
                    html_token = cast(RawHtmlMarkdownToken, new_token)
                    between_brackets = html_token.raw_tag
        else:
            new_token, between_brackets = None, None

        inline_response = InlineResponse()
        if new_token:
            (
                inline_response.new_string,
                inline_response.new_index,
                inline_response.new_tokens,
                between_brackets,
            ) = (
                "",
                closing_angle_index,
                [new_token],
                f"{InlineHelper.angle_bracket_start}{between_brackets}{InlineHelper.__angle_bracket_end}",
            )
        else:
            inline_response.new_string, inline_response.new_index, between_brackets = (
                InlineHelper.angle_bracket_start,
                inline_request.next_index + 1,
                InlineHelper.angle_bracket_start,
            )

        (
            inline_response.delta_line_number,
            inline_response.delta_column_number,
        ) = ParserHelper.calculate_deltas(between_brackets)
        return inline_response
