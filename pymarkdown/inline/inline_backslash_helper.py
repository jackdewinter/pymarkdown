"""
Module to help with the parsing of backslash inline elements.
"""
import logging

from pymarkdown.inline.inline_character_reference_helper import (
    InlineCharacterReferenceHelper,
)
from pymarkdown.inline.inline_request import InlineRequest
from pymarkdown.inline.inline_response import InlineResponse
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


class InlineBackslashHelper:
    """
    Class to help with the parsing of backslash inline elements.
    """

    backslash_character = "\\"
    __backslash_punctuation = "!\"#$%&'()*+,-./:;<=>?@[]^_`{|}~\\"

    __valid_backslash_sequence_starts = f"{backslash_character}{InlineCharacterReferenceHelper.character_reference_start_character}"

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
                InlineBackslashHelper.backslash_character,
                inline_response.new_string,
            )
        else:
            if (
                inline_request.source_text[inline_response.new_index]
                in InlineBackslashHelper.__backslash_punctuation
            ):
                inline_response.new_string = (
                    ParserHelper.backslash_escape_sequence if add_text_signature else ""
                ) + inline_request.source_text[inline_response.new_index]
                inline_response.new_string_unresolved = (
                    InlineBackslashHelper.backslash_character
                    + inline_response.new_string
                )
            else:
                inline_response.new_string = (
                    InlineBackslashHelper.backslash_character
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
    def handle_backslashes(source_text: str) -> str:
        """
        Handle the processing of backslashes for anything other than the text
        blocks, which have additional needs for parsing.
        """

        start_index, string_parts = 0, []
        next_index = ParserHelper.index_any_of(
            source_text,
            InlineBackslashHelper.__valid_backslash_sequence_starts,
            start_index,
        )
        while next_index != -1:
            string_parts.append(source_text[start_index:next_index])
            current_char = source_text[next_index]

            inline_request = InlineRequest(source_text, next_index)
            POGGER.debug("handle_backslashes>>$>>", current_char)
            if current_char == InlineBackslashHelper.backslash_character:
                inline_response = InlineBackslashHelper.handle_inline_backslash(
                    inline_request, add_text_signature=False
                )
            else:
                assert (
                    source_text[next_index]
                    == InlineCharacterReferenceHelper.character_reference_start_character
                )
                inline_response = (
                    InlineCharacterReferenceHelper.handle_character_reference(
                        inline_request
                    )
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
                source_text,
                InlineBackslashHelper.__valid_backslash_sequence_starts,
                start_index,
            )

        if start_index < len(source_text):
            string_parts.append(source_text[start_index:])
        return "".join(string_parts)
