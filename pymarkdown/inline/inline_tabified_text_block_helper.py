"""
Module to help with the parsing of tabbified text inline elements.
"""

import logging
from typing import Optional

from pymarkdown.inline.inline_helper import InlineHelper
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.tab_helper import TabHelper

POGGER = ParserLogger(logging.getLogger(__name__))


class InlineTabifiedTextBlockHelper:
    """
    Class to help with the parsing of tabbified text inline elements.
    """

    @staticmethod
    def handle_next_inline_character_tabified(
        source_text: str,
        tabified_text: str,
        newlines_encountered: int,
        start_index: int,
        next_index: int,
    ) -> Optional[str]:
        """
        Handle an inline character that is tabified.
        """
        adj_tabified_text, _ = InlineHelper.xdg(tabified_text, newlines_encountered)
        POGGER.debug("adj_tabified_text>:$:<", adj_tabified_text)

        _, line_start_index = InlineHelper.xdg(source_text, newlines_encountered)
        # POGGER.debug("adj_source_text>:$:<", adj_source_text)

        current_line_source_text = source_text[start_index:next_index]
        POGGER.debug("source_text>:$:<", source_text)
        POGGER.debug("current_line_source_text>:$:<", current_line_source_text)

        stop_character = source_text[next_index]
        if stop_character == "\n":
            ex_original_line, _ = TabHelper.find_detabify_string_ex(
                adj_tabified_text, current_line_source_text
            )
            assert ex_original_line is not None
            return ex_original_line

        POGGER.debug("stop_character>:$:<", stop_character)

        stop_character_in_tabified_index = InlineTabifiedTextBlockHelper.__handle_next_inline_character_tabified_find_stop(
            adj_tabified_text,
            stop_character,
            source_text,
            line_start_index,
            next_index,
        )

        (
            current_line_leading_space_index,
            current_line_leading_space,
        ) = ParserHelper.extract_spaces(current_line_source_text, 0)
        POGGER.debug(
            "current_line_leading_space_index>:$:<, current_line_leading_space>:$:<",
            current_line_leading_space_index,
            current_line_leading_space,
        )
        assert current_line_leading_space_index is not None

        return InlineTabifiedTextBlockHelper.__handle_next_inline_character_tabified_cleanup(
            current_line_source_text,
            current_line_leading_space_index,
            stop_character,
            adj_tabified_text,
            stop_character_in_tabified_index,
            current_line_leading_space,
        )

    @staticmethod
    def __handle_next_inline_character_tabified_find_stop(
        adj_tabified_text: str,
        stop_character: str,
        source_text: str,
        line_start_index: int,
        next_index: int,
    ) -> int:
        found_in_source_text_count = 0
        found_in_source_text_index = source_text.find(stop_character, line_start_index)
        POGGER.debug(
            "source_text[$]>:$:<",
            found_in_source_text_index,
            source_text[found_in_source_text_index:],
        )
        while found_in_source_text_index != next_index:
            found_in_source_text_count += 1
            found_in_source_text_index = source_text.find(
                stop_character, found_in_source_text_index + 1
            )
            POGGER.debug(
                "source_text[$]>:$:<",
                found_in_source_text_index,
                source_text[found_in_source_text_index:],
            )
        POGGER.debug("found_in_source_text_count>:$:<", found_in_source_text_count)
        POGGER.debug(
            "source_text[$]>:$:<",
            found_in_source_text_index,
            source_text[found_in_source_text_index:],
        )

        found_in_tabified_text_count = 0
        stop_character_in_tabified_index = adj_tabified_text.find(stop_character)
        POGGER.debug(
            "adj_tabified_text[$]>:$:<",
            stop_character_in_tabified_index,
            adj_tabified_text[stop_character_in_tabified_index:],
        )
        while found_in_tabified_text_count != found_in_source_text_count:
            found_in_tabified_text_count += 1
            stop_character_in_tabified_index = adj_tabified_text.find(
                stop_character, stop_character_in_tabified_index + 1
            )
            POGGER.debug(
                "adj_tabified_text[$]>:$:<",
                stop_character_in_tabified_index,
                adj_tabified_text[stop_character_in_tabified_index:],
            )
            assert stop_character_in_tabified_index != -1
        POGGER.debug("found_in_tabified_text_count>:$:<", found_in_tabified_text_count)
        POGGER.debug(
            "adj_tabified_text[$]>:$:<",
            stop_character_in_tabified_index,
            adj_tabified_text[stop_character_in_tabified_index:],
        )
        assert adj_tabified_text[stop_character_in_tabified_index] == stop_character
        return stop_character_in_tabified_index

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_next_inline_character_tabified_cleanup(
        current_line_source_text: str,
        current_line_leading_space_index: int,
        stop_character: str,
        adj_tabified_text: str,
        stop_character_in_tabified_index: int,
        current_line_leading_space: Optional[str],
    ) -> str:
        (
            current_line_first_word_index,
            current_line_first_word,
        ) = ParserHelper.collect_until_one_of_characters(
            current_line_source_text,
            current_line_leading_space_index,
            " \t" + stop_character,
        )
        POGGER.debug(
            "current_line_first_word_index>:$:<, current_line_first_word>:$:<",
            current_line_first_word_index,
            current_line_first_word,
        )

        if current_line_leading_space_index == current_line_first_word_index:
            tabified_start_index, _ = ParserHelper.extract_spaces_from_end(
                adj_tabified_text, stop_character_in_tabified_index
            )
        else:
            assert current_line_first_word is not None
            tabified_start_index = InlineHelper.pdff(
                current_line_source_text,
                current_line_first_word,
                current_line_leading_space_index,
                adj_tabified_text,
                stop_character_in_tabified_index,
                current_line_leading_space,
            )
        return adj_tabified_text[tabified_start_index:stop_character_in_tabified_index]

    # pylint: enable=too-many-arguments

    @staticmethod
    def complete_inline_block_processing_tabified(
        source_text: str,
        start_index: int,
        tabified_text: str,
        newlines_encountered: int,
    ) -> str:
        """
        Complete the processing on a tabified block
        """

        source_text_spaces_index, source_text_spaces = ParserHelper.extract_spaces(
            source_text, start_index
        )
        POGGER.debug(
            "source_text_spaces_index=>:$:<, source_text_spaces=>:$:<",
            source_text_spaces_index,
            source_text_spaces,
        )
        assert source_text_spaces_index is not None
        (
            source_text_word_index,
            source_text_word,
        ) = ParserHelper.collect_until_one_of_characters(
            source_text, source_text_spaces_index, " \t"
        )
        POGGER.debug(
            "source_text_word_index=>:$:<, source_text_word=>:$:<",
            source_text_word_index,
            source_text_word,
        )
        assert source_text_word is not None

        current_line_source_text, current_line_start_index = InlineHelper.xdf(
            source_text, newlines_encountered
        )
        POGGER.debug("current_line_source_text>:$:<", current_line_source_text)
        POGGER.debug("current_line_start_index>:$:<", current_line_start_index)

        find_word_count = 0
        word_index = current_line_source_text.find(source_text_word, 0)
        adj_word_index = word_index + current_line_start_index
        POGGER.debug(
            "[$]-->current_line_source_text[$:]>:$:<",
            find_word_count,
            word_index,
            current_line_source_text[word_index:],
        )
        POGGER.debug(
            "adj_word_index=$ != source_text_spaces_index=$",
            adj_word_index,
            source_text_spaces_index,
        )
        while adj_word_index != source_text_spaces_index:
            find_word_count += 1
            word_index = current_line_source_text.find(source_text_word, word_index + 1)
            adj_word_index = word_index + current_line_start_index
            POGGER.debug(
                "[$]-->current_line_source_text[$:]>:$:<",
                find_word_count,
                word_index,
                current_line_source_text[word_index:],
            )
            POGGER.debug(
                "adj_word_index=$ != source_text_spaces_index=$",
                adj_word_index,
                source_text_spaces_index,
            )
        POGGER.debug(
            "[$]-->current_line_source_text[$:]>:$:<",
            find_word_count,
            word_index,
            current_line_source_text[word_index:],
        )

        current_line_tabified_text, _ = InlineHelper.xdf(
            tabified_text, newlines_encountered
        )
        POGGER.debug("current_line_tabified_text>:$:<", current_line_tabified_text)

        found_word_index = InlineHelper.calculate_word_index(
            current_line_tabified_text,
            source_text_word,
            find_word_count,
            source_text_spaces,
        )
        return current_line_tabified_text[found_word_index:]
