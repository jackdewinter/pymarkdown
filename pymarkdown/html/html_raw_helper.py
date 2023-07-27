"""
Module to provide helper functions for parsing the raw html inline blocks.
"""
import logging
import string
from typing import Optional, Tuple

from pymarkdown.constants import Constants
from pymarkdown.inline.inline_request import InlineRequest
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.tokens.inline_markdown_token import RawHtmlMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class HtmlRawHelper:
    """
    Class to provide helper functions for parsing the raw html inline blocks.
    """

    __raw_declaration_start_character = "!"
    __raw_declaration_whitespace = ParserHelper.space_character

    __raw_html_exclusion_1 = ">"
    __raw_html_exclusion_2 = "->"
    __raw_html_exclusion_3 = "-"
    __raw_html_exclusion_4 = "--"

    __html_block_2_to_5_start = "!"

    __html_block_2_continued_start = "--"
    __html_block_2_xx = f"{__html_block_2_to_5_start}{__html_block_2_continued_start}"
    __html_block_2_end = "-->"

    __html_block_3_continued_start = "?"
    __html_block_3_end = "?>"

    __html_block_4_continued_start = string.ascii_uppercase

    __html_block_5_continued_start = "[CDATA["
    __html_block_5_xx = f"{__html_block_2_to_5_start}{__html_block_5_continued_start}"
    __html_block_5_end = "]]>"

    __html_tag_start = "/"
    __html_tag_end = ">"

    __tag_attribute_name_start = f"{string.ascii_letters}_:"
    __tag_attribute_name_characters = f"{string.ascii_letters}{string.digits}_.:-"

    __valid_tag_name_start = string.ascii_letters
    __valid_tag_name_characters = f"{string.ascii_letters}{string.digits}-"

    __html_attribute_value_single = "'"
    __html_attribute_value_double = '"'
    __html_attribute_name_value_separator = "="

    __unquoted_attribute_value_stop = f"\"'=<>`{Constants.ascii_whitespace}"

    @staticmethod
    def parse_raw_html(
        only_between_angles: str,
        remaining_line: str,
        line_number: int,
        column_number: int,
        inline_request: InlineRequest,
    ) -> Tuple[Optional[RawHtmlMarkdownToken], int]:
        """
        Given an open HTML tag character (<), try the various possibilities for
        types of tag, and determine if any of them parse validly.
        """

        valid_raw_html, remaining_line_parse_index = HtmlRawHelper.__parse_raw_open_tag(
            remaining_line
        )
        if not valid_raw_html:
            valid_raw_html = HtmlRawHelper.__parse_raw_close_tag(only_between_angles)
        if not valid_raw_html:
            (
                valid_raw_html,
                remaining_line_parse_index,
            ) = HtmlRawHelper.__process_raw_special(
                remaining_line,
                HtmlRawHelper.__html_block_2_xx,
                HtmlRawHelper.__html_block_2_end,
                True,
            )
        if not valid_raw_html:
            (
                valid_raw_html,
                remaining_line_parse_index,
            ) = HtmlRawHelper.__process_raw_special(
                remaining_line,
                HtmlRawHelper.__html_block_3_continued_start,
                HtmlRawHelper.__html_block_3_end,
            )
        if not valid_raw_html:
            (
                valid_raw_html,
                remaining_line_parse_index,
            ) = HtmlRawHelper.__process_raw_special(
                remaining_line,
                HtmlRawHelper.__html_block_5_xx,
                HtmlRawHelper.__html_block_5_end,
            )
        if not valid_raw_html:
            valid_raw_html = HtmlRawHelper.__parse_raw_declaration(only_between_angles)

        if not valid_raw_html:
            return None, -1
        if inline_request.para_owner:
            (
                valid_raw_html,
                inline_request.para_owner.rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                valid_raw_html,
                inline_request.para_owner.extracted_whitespace,
                inline_request.para_owner.rehydrate_index,
                add_replace_marker_if_empty=True,
            )
        return (
            RawHtmlMarkdownToken(valid_raw_html, line_number, column_number),
            remaining_line_parse_index,
        )

    @staticmethod
    def __parse_raw_open_tag(text_to_parse: str) -> Tuple[Optional[str], int]:
        """
        Parse the current line as if it is an open tag, and determine if it is valid.
        """

        end_parse_index, valid_raw_html, tag_name = (
            -1,
            None,
            HtmlRawHelper.__parse_raw_tag_name(text_to_parse, 0),
        )
        if tag_name:
            parse_index, extracted_whitespace = ParserHelper.extract_ascii_whitespace(
                text_to_parse, len(tag_name)
            )
            assert parse_index is not None
            while extracted_whitespace and ParserHelper.is_character_at_index_one_of(
                text_to_parse,
                parse_index,
                HtmlRawHelper.__tag_attribute_name_start,
            ):
                (
                    parse_index,
                    extracted_whitespace,
                ) = HtmlRawHelper.__parse_tag_attributes(text_to_parse, parse_index)
                if parse_index is None:
                    return None, -1

            if ParserHelper.is_character_at_index(
                text_to_parse, parse_index, HtmlRawHelper.__html_tag_start
            ):
                parse_index += 1

            if ParserHelper.is_character_at_index(
                text_to_parse, parse_index, HtmlRawHelper.__html_tag_end
            ):
                valid_raw_html = text_to_parse[:parse_index]
                end_parse_index = parse_index + 1

        return valid_raw_html, end_parse_index

    @staticmethod
    def __parse_raw_close_tag(text_to_parse: str) -> Optional[str]:
        """
        Parse the current line as if it is a close tag, and determine if it is valid.
        """
        valid_raw_html = None
        if ParserHelper.is_character_at_index(
            text_to_parse, 0, HtmlRawHelper.__html_tag_start
        ):
            if tag_name := HtmlRawHelper.__parse_raw_tag_name(text_to_parse, 1):
                parse_index: Optional[int] = len(tag_name)
                assert parse_index is not None
                text_to_parse_size = len(text_to_parse)
                if parse_index != text_to_parse_size:
                    parse_index, _ = ParserHelper.extract_spaces(
                        text_to_parse, parse_index
                    )
                if parse_index == text_to_parse_size:
                    valid_raw_html = text_to_parse
        return valid_raw_html

    @staticmethod
    def __process_raw_special(
        remaining_line: str,
        special_start: str,
        special_end: str,
        do_extra_check: bool = False,
    ) -> Tuple[Optional[str], int]:
        """
        Parse a possible raw html special sequence, and return if it is valid.
        """
        valid_raw_html: Optional[str] = None
        parse_index = -1
        if remaining_line.startswith(special_start):
            special_start_size = len(special_start)
            remaining_line = remaining_line[special_start_size:]
            parse_index = remaining_line.find(special_end)
            if parse_index != -1:
                remaining_line = remaining_line[:parse_index]
                parse_index = parse_index + special_start_size + len(special_end)
                if (not do_extra_check) or (
                    not (
                        remaining_line[0] == HtmlRawHelper.__raw_html_exclusion_1
                        or remaining_line.startswith(
                            HtmlRawHelper.__raw_html_exclusion_2
                        )
                        or remaining_line[-1] == HtmlRawHelper.__raw_html_exclusion_3
                        or HtmlRawHelper.__raw_html_exclusion_4 in remaining_line
                    )
                ):
                    valid_raw_html = (
                        f"{special_start}{remaining_line}{special_end[:-1]}"
                    )
        return valid_raw_html, parse_index

    @staticmethod
    def __parse_raw_declaration(text_to_parse: str) -> Optional[str]:
        """
        Parse a possible raw html declaration sequence, and return if it is valid.
        """

        valid_raw_html = None
        if ParserHelper.is_character_at_index_one_of(
            text_to_parse, 0, HtmlRawHelper.__raw_declaration_start_character
        ):
            (
                parse_index,
                declaration_name,
            ) = ParserHelper.collect_while_one_of_characters(
                text_to_parse, 1, HtmlRawHelper.__html_block_4_continued_start
            )
            assert parse_index is not None
            if declaration_name:
                whitespace_count, _ = ParserHelper.collect_while_character(
                    text_to_parse,
                    parse_index,
                    HtmlRawHelper.__raw_declaration_whitespace,
                )
                if whitespace_count:
                    valid_raw_html = text_to_parse
        return valid_raw_html

    @staticmethod
    def __parse_raw_tag_name(text_to_parse: str, start_index: int) -> str:
        """
        Parse a HTML tag name from the string.
        """
        if ParserHelper.is_character_at_index_one_of(
            text_to_parse, start_index, HtmlRawHelper.__valid_tag_name_start
        ):
            index, __ = ParserHelper.collect_while_one_of_characters(
                text_to_parse,
                start_index + 1,
                HtmlRawHelper.__valid_tag_name_characters,
            )
            return text_to_parse[:index]
        return ""

    @staticmethod
    def __parse_tag_attributes(
        text_to_parse: str, start_index: int
    ) -> Tuple[Optional[int], Optional[str]]:
        """
        Handle the parsing of the attributes for an open tag.
        """
        parse_index, _ = ParserHelper.collect_while_one_of_characters(
            text_to_parse, start_index, HtmlRawHelper.__tag_attribute_name_characters
        )
        assert parse_index is not None
        end_name_index, extracted_whitespace = ParserHelper.extract_ascii_whitespace(
            text_to_parse, parse_index
        )
        assert end_name_index is not None
        if ParserHelper.is_character_at_index(
            text_to_parse,
            end_name_index,
            HtmlRawHelper.__html_attribute_name_value_separator,
        ):
            (
                value_start_index,
                _,
            ) = ParserHelper.extract_ascii_whitespace(text_to_parse, end_name_index + 1)
            assert value_start_index is not None
            value_end_index: Optional[int] = None
            if ParserHelper.is_character_at_index_one_of(
                text_to_parse,
                value_start_index,
                HtmlRawHelper.__html_attribute_value_single,
            ):
                value_end_index, _ = ParserHelper.collect_until_character(
                    text_to_parse,
                    value_start_index + 1,
                    HtmlRawHelper.__html_attribute_value_single,
                )
                assert value_end_index is not None
                if not ParserHelper.is_character_at_index(
                    text_to_parse,
                    value_end_index,
                    HtmlRawHelper.__html_attribute_value_single,
                ):
                    return None, None
                value_end_index += 1
            elif ParserHelper.is_character_at_index_one_of(
                text_to_parse,
                value_start_index,
                HtmlRawHelper.__html_attribute_value_double,
            ):
                value_end_index, _ = ParserHelper.collect_until_character(
                    text_to_parse,
                    value_start_index + 1,
                    HtmlRawHelper.__html_attribute_value_double,
                )
                assert value_end_index is not None
                if not ParserHelper.is_character_at_index(
                    text_to_parse,
                    value_end_index,
                    HtmlRawHelper.__html_attribute_value_double,
                ):
                    return None, None
                value_end_index += 1
            else:
                value_end_index, _ = ParserHelper.collect_until_one_of_characters(
                    text_to_parse,
                    value_start_index,
                    HtmlRawHelper.__unquoted_attribute_value_stop,
                )
            assert value_end_index is not None
            (
                end_name_index,
                extracted_whitespace,
            ) = ParserHelper.extract_ascii_whitespace(text_to_parse, value_end_index)

        return end_name_index, extracted_whitespace
