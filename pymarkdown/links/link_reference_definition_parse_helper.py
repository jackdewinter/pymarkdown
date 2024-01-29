"""
Module to helper with the parsing of link reference definitions.
"""

import logging
from typing import Optional, Tuple

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.inline.inline_backslash_helper import InlineBackslashHelper
from pymarkdown.links.link_parse_helper import LinkParseHelper
from pymarkdown.links.link_reference_info import LinkReferenceInfo
from pymarkdown.links.link_reference_titles import LinkReferenceTitles
from pymarkdown.links.link_reference_tuple import LinkReferenceDefinitionTuple

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods
class LinkReferenceDefinitionParseHelper:
    """
    Class to helper with the parsing of link reference definitions.
    """

    __lrd_start_character = "["

    # pylint: disable=too-many-locals
    @staticmethod
    def parse_link_reference_definition(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        is_blank_line: Optional[bool],
    ) -> Tuple[bool, Optional[int], Optional[LinkReferenceDefinitionTuple]]:
        """
        Handle the parsing of what appears to be a link reference definition.
        """
        did_start = LinkReferenceDefinitionParseHelper.__is_link_reference_definition(
            parser_state, line_to_parse, start_index, extracted_whitespace
        )
        if not did_start:
            POGGER.debug("BAIL")
            return False, -1, None

        new_index: Optional[int] = None
        (
            keep_going,
            new_index,
            collected_destination,
        ) = LinkParseHelper.extract_link_label(
            parser_state.parse_properties, line_to_parse, start_index + 1
        )
        assert is_blank_line is not None
        if keep_going:
            (
                keep_going,
                new_index,
                inline_link,
                _,
                line_destination_whitespace,
                inline_raw_link,
            ) = LinkParseHelper.extract_link_destination(
                parser_state.parse_properties, line_to_parse, new_index, is_blank_line
            )
        else:
            inline_link = None
        if keep_going:
            (
                keep_going,
                new_index,
                inline_title,
                _,
                line_title_whitespace,
                inline_raw_title,
            ) = LinkParseHelper.extract_link_title(
                parser_state.parse_properties, line_to_parse, new_index, is_blank_line
            )
        else:
            inline_title = ""
        if keep_going:
            (
                keep_going,
                new_index,
                end_whitespace,
            ) = LinkReferenceDefinitionParseHelper.__verify_link_definition_end(
                line_to_parse, new_index
            )
        if keep_going:
            assert collected_destination is not None
            normalized_destination = LinkParseHelper.normalize_link_label(
                collected_destination
            )
            if not normalized_destination:
                keep_going, new_index = False, -1
        else:
            normalized_destination = None
        return (
            LinkReferenceDefinitionParseHelper.__create_lrd_token(
                new_index,
                collected_destination,
                normalized_destination,
                line_destination_whitespace,
                inline_link,
                inline_raw_link,
                inline_title,
                inline_raw_title,
                line_title_whitespace,
                end_whitespace,
            )
            if keep_going
            else (keep_going, new_index, None)
        )

    # pylint: enable=too-many-locals

    @staticmethod
    def __is_link_reference_definition(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
    ) -> bool:
        """
        Determine whether or not we have the start of a link reference definition.
        """

        if parser_state.token_stack[-1].is_paragraph:
            return False

        assert extracted_whitespace is not None
        POGGER.debug(
            "__is_link_reference_definition - extracted_whitespace:>:$:<",
            extracted_whitespace,
        )
        POGGER.debug(
            "__is_link_reference_definition - line_to_parse:>:$:<", line_to_parse
        )
        if (
            TabHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse,
            start_index,
            LinkReferenceDefinitionParseHelper.__lrd_start_character,
        ):
            POGGER.debug("__is_link_reference_definition - potential")
            remaining_line, continue_with_lrd = line_to_parse[start_index + 1 :], True
            if (
                remaining_line
                and remaining_line[-1] == InlineBackslashHelper.backslash_character
            ):
                remaining_line_size, start_index, found_index = (
                    len(remaining_line),
                    0,
                    remaining_line.find(
                        InlineBackslashHelper.backslash_character, start_index
                    ),
                )
                POGGER.debug(">>$<<$", remaining_line, remaining_line_size)
                POGGER.debug(">>$<<$", remaining_line, start_index)
                POGGER.debug(">>$<<", found_index)
                while found_index != -1 and found_index < (remaining_line_size - 1):
                    start_index = found_index + 2
                    POGGER.debug(">>$<<$", remaining_line, start_index)
                    found_index = remaining_line.find(
                        InlineBackslashHelper.backslash_character, start_index
                    )
                    POGGER.debug(">>$<<", found_index)
                POGGER.debug(">>>>>>>$<<", found_index)
                continue_with_lrd = found_index != remaining_line_size - 1
            return continue_with_lrd
        return False

    # pylint: disable=too-many-arguments
    @staticmethod
    def __create_lrd_token(
        new_index: Optional[int],
        collected_destination: Optional[str],
        normalized_destination: Optional[str],
        line_destination_whitespace: Optional[str],
        inline_link: Optional[str],
        inline_raw_link: Optional[str],
        inline_title: Optional[str],
        inline_raw_title: Optional[str],
        line_title_whitespace: Optional[str],
        end_whitespace: Optional[str],
    ) -> Tuple[bool, Optional[int], Optional[LinkReferenceDefinitionTuple]]:
        assert new_index != -1

        POGGER.debug(
            ">>collected_destination(normalized)>>$",
            normalized_destination,
        )

        if (
            not inline_title
            and line_title_whitespace
            and line_title_whitespace[-1] == ParserHelper.newline_character
        ):
            line_title_whitespace = line_title_whitespace[:-1]

        POGGER.debug(">>inline_link>>$<<", inline_link)
        POGGER.debug(">>inline_title>>$<<", inline_title)
        parsed_lrd_tuple = LinkReferenceDefinitionTuple(
            normalized_destination,
            LinkReferenceTitles(inline_link, inline_title),
            LinkReferenceInfo(
                collected_destination,
                line_destination_whitespace,
                inline_raw_link,
                line_title_whitespace,
                inline_raw_title,
                end_whitespace,
            ),
        )
        return True, new_index, parsed_lrd_tuple

    # pylint: enable=too-many-arguments

    @staticmethod
    def __verify_link_definition_end(
        line_to_parse: str, new_index: Optional[int]
    ) -> Tuple[bool, Optional[int], Optional[str]]:
        """
        Verify that the link reference definition's ends properly.
        """

        assert new_index is not None
        POGGER.debug("look for EOL-ws>>$<<", line_to_parse[new_index:])
        new_index, ex_ws = ParserHelper.extract_ascii_whitespace(
            line_to_parse, new_index
        )
        assert new_index is not None
        POGGER.debug("look for EOL>>$<<", line_to_parse[new_index:])
        if new_index < len(line_to_parse):
            POGGER.debug(">> characters left at EOL, bailing")
            return False, -1, None
        return True, new_index, ex_ws


# pylint: enable=too-few-public-methods
