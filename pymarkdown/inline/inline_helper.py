"""
Module to help with the parsing of inline elements.
"""

import logging
from typing import Dict, List, Optional, Tuple

from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.inline.inline_backslash_helper import InlineBackslashHelper
from pymarkdown.inline.inline_request import InlineRequest

POGGER = ParserLogger(logging.getLogger(__name__))


class InlineHelper:
    """
    Class to help with the parsing of inline elements.
    """

    __html_character_escape_map = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
        '"': "&quot;",
    }

    @staticmethod
    def extract_bounded_string(
        parser_properties: ParseBlockPassProperties,
        source_text: str,
        new_index: int,
        close_character: str,
        start_character: Optional[str],
    ) -> Tuple[Optional[int], Optional[str]]:
        """
        Extract a string that is bounded by some manner of characters.
        """
        nesting_level: int = 0
        break_characters = (
            f"{InlineBackslashHelper.backslash_character}{close_character}{start_character}"
            if start_character
            else f"{InlineBackslashHelper.backslash_character}{close_character}"
        )

        POGGER.debug(
            "extract_bounded_string>>new_index>>$>>data>>$>>",
            new_index,
            source_text[new_index:],
        )
        next_index, data = ParserHelper.collect_until_one_of_characters_verified(
            source_text, new_index, break_characters
        )
        extracted_parts: List[str] = [data]
        POGGER.debug(
            ">>next_index1>>$>>data>>$>>",
            next_index,
            data,
        )
        while next_index < len(source_text) and (
            source_text[next_index] != close_character or nesting_level != 0
        ):
            (
                next_index,
                nesting_level,
            ) = InlineHelper.__handle_next_extract_bounded_string_item(
                parser_properties,
                source_text,
                next_index,
                extracted_parts,
                start_character,
                nesting_level,
                close_character,
                break_characters,
            )
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
        parser_properties: ParseBlockPassProperties,
        source_text: str,
        next_index: int,
        extracted_parts: List[str],
        start_character: Optional[str],
        nesting_level: int,
        close_character: str,
        break_characters: str,
    ) -> Tuple[int, int]:
        if ParserHelper.is_character_at_index(
            source_text, next_index, InlineBackslashHelper.backslash_character
        ):
            POGGER.debug("pre-back>>next_index>>$>>", next_index)
            old_index = next_index

            inline_request = InlineRequest(source_text, next_index)
            inline_response = InlineBackslashHelper.handle_inline_backslash(
                parser_properties, inline_request
            )
            assert inline_response.new_index is not None, "New index must be defined."
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
            ), "Character at index must be the close character."
            POGGER.debug("pre-close>>next_index>>$>>", next_index)
            extracted_parts.append(close_character)
            next_index += 1
            nesting_level -= 1
        nexter_index, new_data = ParserHelper.collect_until_one_of_characters_verified(
            source_text, next_index, break_characters
        )
        extracted_parts.append(new_data)
        return nexter_index, nesting_level

    # pylint: enable=too-many-arguments

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
                    (
                        ParserHelper.create_replacement_markers(
                            text_to_append[next_index], escaped_part
                        )
                        if add_text_signature
                        else escaped_part
                    ),
                ]
            )

            start_index = next_index + 1
            next_index = ParserHelper.index_any_of(text_to_append, key_map, start_index)

        if start_index < len(text_to_append):
            text_parts.append(text_to_append[start_index:])

        return "".join(text_parts)

    # pylint: disable=too-many-arguments
    @staticmethod
    def pdff(
        current_line_source_text: str,
        current_line_first_word: str,
        current_line_leading_space_index: Optional[int],
        adj_tabified_text: str,
        stop_character_in_tabified_index: int,
        current_line_leading_space: Optional[str],
    ) -> int:
        """
        This method needs a better name.
        """
        first_word_index = current_line_source_text.rfind(current_line_first_word)
        POGGER.debug("first_word_index>:$:<", first_word_index)
        first_word_count = 0
        while (
            first_word_index != current_line_leading_space_index
            and first_word_index > 0
        ):
            first_word_index = current_line_source_text.rfind(
                current_line_first_word, 0, first_word_index - 1
            )
            POGGER.debug("first_word_index>:$:<", first_word_index)
            first_word_count += 1
        POGGER.debug("first_word_count>:$:<", first_word_count)
        assert (
            first_word_index == current_line_leading_space_index
        ), "Indices must match up."

        tabified_start_index = adj_tabified_text.rfind(
            current_line_first_word, 0, stop_character_in_tabified_index
        )
        POGGER.debug(
            "tabified_start_index=$,stop=$..>:$:<",
            tabified_start_index,
            stop_character_in_tabified_index,
            adj_tabified_text[tabified_start_index:stop_character_in_tabified_index],
        )
        for _ in range(first_word_count):
            tabified_start_index = adj_tabified_text.rfind(
                current_line_first_word, 0, tabified_start_index - 1
            )
            POGGER.debug(
                "tabified_start_index=$,stop=$..>:$:<",
                tabified_start_index,
                stop_character_in_tabified_index,
                adj_tabified_text[
                    tabified_start_index:stop_character_in_tabified_index
                ],
            )
            assert (
                tabified_start_index <= stop_character_in_tabified_index
            ), "Normal and tabified indices must match up."

        if current_line_leading_space:
            POGGER.debug(
                "adj_tabified_text[$:]>:$:<",
                tabified_start_index,
                adj_tabified_text[tabified_start_index:],
            )
            tabified_start_index, _ = ParserHelper.extract_spaces_from_end(
                adj_tabified_text, tabified_start_index
            )
            POGGER.debug(
                "adj_tabified_text[$:]>:$:<",
                tabified_start_index,
                adj_tabified_text[tabified_start_index:],
            )

        return tabified_start_index

    # pylint: enable=too-many-arguments

    @staticmethod
    def xdf(tabified_text: str, newlines_encountered: int) -> Tuple[str, int]:
        """
        This method needs a better name.
        """
        start_index = 0
        for _ in range(newlines_encountered):
            next_index = tabified_text.find("\n", start_index)
            assert next_index != -1, "Next newline must be found."
            start_index = next_index + 1

        next_index = tabified_text.find("\n", start_index)
        assert next_index == -1, "Next newline must not be found."

        return tabified_text[start_index:], start_index

    @staticmethod
    def xdg(tabified_text: str, newlines_encountered: int) -> Tuple[str, int]:
        """
        This method needs a better name.
        """
        line_start_index = 0
        for _ in range(newlines_encountered):
            line_end_index = tabified_text.find("\n", line_start_index)
            line_start_index = line_end_index + 1
        POGGER.debug("line_start_index>:$:<", line_start_index)
        line_end_index = tabified_text.find("\n", line_start_index)
        return (
            (
                tabified_text[line_start_index:line_end_index]
                if line_end_index != -1
                else tabified_text[line_start_index:]
            ),
            line_start_index,
        )

    @staticmethod
    def calculate_word_index(
        current_line_tabified_text: str,
        source_text_word: str,
        find_word_count: int,
        source_text_spaces: str,
    ) -> int:
        """
        Calculate the location of a given word.
        """
        POGGER.debug("source_text_word>:$:<", source_text_word)
        found_word_index = current_line_tabified_text.find(source_text_word)
        POGGER.debug(
            "[$]-->current_line_source_text[$:]>:$:<",
            0,
            found_word_index,
            current_line_tabified_text[found_word_index:],
        )
        for found_word_count in range(find_word_count):
            found_word_index = current_line_tabified_text.find(
                source_text_word, found_word_index + 1
            )
            POGGER.debug(
                "[$]-->current_line_source_text[$:]>:$:<",
                found_word_count,
                found_word_index,
                current_line_tabified_text[found_word_index:],
            )
            assert found_word_index != -1, "Found index must be set to a valid index."

        if source_text_spaces:
            POGGER.debug(
                "current_line_source_text[$:]>:$:<",
                found_word_index,
                current_line_tabified_text[found_word_index:],
            )
            found_word_index, _ = ParserHelper.extract_spaces_from_end(
                current_line_tabified_text, found_word_index
            )
            POGGER.debug(
                "current_line_source_text[$:]>:$:<",
                found_word_index,
                current_line_tabified_text[found_word_index:],
            )
        return found_word_index
