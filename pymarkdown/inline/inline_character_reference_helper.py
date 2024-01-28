"""
Module to help with the parsing of character reference inline elements.
"""

import json
import logging
import os
import string
from typing import Dict, Optional, Tuple

from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.general.bad_tokenization_error import BadTokenizationError
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.inline.inline_request import InlineRequest
from pymarkdown.inline.inline_response import InlineResponse

POGGER = ParserLogger(logging.getLogger(__name__))


class InlineCharacterReferenceHelper:
    """
    Class to help with the parsing of character reference inline elements.
    """

    __invalid_reference_character_substitute = "\ufffd"

    __hex_character_reference_start_character = "xX"
    __numeric_character_reference_start_character = "#"

    character_reference_start_character = "&"
    __character_reference_end_character = ";"

    __skip_html5_entities_ending_with = ";"

    __ascii_letters_and_digits = f"{string.ascii_letters}{string.digits}"

    __entity_map: Dict[str, str] = {}
    __entities_file_name = "entities.json"

    @staticmethod
    def initialize(resource_path: str) -> None:
        """
        Initialize the inline subsystem.
        """
        InlineCharacterReferenceHelper.__entity_map = (
            InlineCharacterReferenceHelper.__load_entity_map(resource_path)
        )

    @staticmethod
    def handle_character_reference(
        parser_properties: ParseBlockPassProperties, inline_request: InlineRequest
    ) -> InlineResponse:
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
            == InlineCharacterReferenceHelper.__numeric_character_reference_start_character
        ):
            InlineCharacterReferenceHelper.__handle_numeric_character_reference(
                inline_request, inline_response
            )
        else:
            InlineCharacterReferenceHelper.__handle_non_numeric_character_reference(
                inline_request, inline_response, source_text_size
            )
        inline_response.delta_line_number, inline_response.delta_column_number = (
            0,
            inline_response.new_index - inline_request.next_index,
        )
        return inline_response

    @staticmethod
    def __load_entity_map(resource_path: str) -> Dict[str, str]:
        """
        Load the entity map, refreshed from https://html.spec.whatwg.org/entities.json
        into a dict that was can use.
        """

        master_entities_file = os.path.join(
            resource_path, InlineCharacterReferenceHelper.__entities_file_name
        )
        try:
            with open(
                os.path.abspath(master_entities_file), "rt", encoding="utf-8"
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
            if (
                next_name[-1]
                != InlineCharacterReferenceHelper.__skip_html5_entities_ending_with
            ):
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
            f"{InlineCharacterReferenceHelper.character_reference_start_character}"
            + f"{InlineCharacterReferenceHelper.__numeric_character_reference_start_character}{hex_char}{collected_string}"
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
            f"{InlineCharacterReferenceHelper.character_reference_start_character}"
            + f"{InlineCharacterReferenceHelper.__numeric_character_reference_start_character}{collected_string}"
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
            in InlineCharacterReferenceHelper.__hex_character_reference_start_character
        ):
            (
                new_string,
                new_index,
                translated_reference,
            ) = InlineCharacterReferenceHelper.__handle_numeric_character_reference_hex(
                new_index, source_text, source_text_size
            )
        else:
            (
                new_string,
                new_index,
                translated_reference,
            ) = InlineCharacterReferenceHelper.__handle_numeric_character_reference_decimal(
                new_index, source_text, source_text_size
            )

        if (
            translated_reference >= 0
            and new_index < source_text_size
            and source_text[new_index]
            == InlineCharacterReferenceHelper.__character_reference_end_character
        ):
            new_index += 1
            original_reference, new_string = f"{new_string};", (
                InlineCharacterReferenceHelper.__invalid_reference_character_substitute
                if translated_reference == 0
                else chr(translated_reference)
            )
        return new_string, new_index, original_reference

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
        ) = InlineCharacterReferenceHelper.__handle_numeric_character_reference_inner(
            inline_request.source_text, inline_response.new_index
        )
        inline_response.new_string_unresolved = (
            InlineCharacterReferenceHelper.character_reference_start_character
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
            InlineCharacterReferenceHelper.__ascii_letters_and_digits,
        )
        if collected_string:
            assert end_index is not None
            collected_string = f"{InlineCharacterReferenceHelper.character_reference_start_character}{collected_string}"
            if (
                end_index < source_text_size
                and inline_request.source_text[end_index]
                == InlineCharacterReferenceHelper.__character_reference_end_character
            ):
                end_index += 1
                collected_string += (
                    InlineCharacterReferenceHelper.__character_reference_end_character
                )
                if collected_string in InlineCharacterReferenceHelper.__entity_map:
                    inline_response.new_string_unresolved = collected_string
                    inline_response.original_string = collected_string
                    collected_string = InlineCharacterReferenceHelper.__entity_map[
                        collected_string
                    ]
            inline_response.new_string, inline_response.new_index = (
                collected_string,
                end_index,
            )
            POGGER.debug("there-->$<--", inline_response.new_string)
            POGGER.debug("there-->$<--", inline_response.new_string_unresolved)
        else:
            inline_response.new_string = (
                InlineCharacterReferenceHelper.character_reference_start_character
            )
