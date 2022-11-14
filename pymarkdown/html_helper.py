"""
Module to provide helper functions for parsing html.
"""
import logging
import string
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quote_data import BlockQuoteData
from pymarkdown.constants import Constants
from pymarkdown.container_helper import ContainerHelper
from pymarkdown.inline_markdown_token import RawHtmlMarkdownToken, TextMarkdownToken
from pymarkdown.inline_request import InlineRequest
from pymarkdown.leaf_markdown_token import HtmlBlockMarkdownToken
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.stack_token import HtmlBlockStackToken, ParagraphStackToken, StackToken
from pymarkdown.tab_helper import TabHelper

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


class HtmlHelper:
    """
    Class to provide helper functions for parsing html.
    """

    html_block_1 = "1"
    html_block_2 = "2"
    html_block_3 = "3"
    html_block_4 = "4"
    html_block_5 = "5"
    html_block_6 = "6"
    html_block_7 = "7"

    __html_block_start_character = "<"
    __html_tag_start = "/"
    __html_tag_name_end = " >"
    __html_tag_end = ">"
    __html_attribute_value_single = "'"
    __html_attribute_value_double = '"'
    __html_attribute_name_value_separator = "="
    __html_attribute_separator = ParserHelper.space_character
    __valid_tag_name_start = string.ascii_letters
    __valid_tag_name_characters = f"{string.ascii_letters}{string.digits}-"
    __tag_attribute_name_characters = f"{string.ascii_letters}{string.digits}_.:-"
    __unquoted_attribute_value_stop = f"\"'=<>`{Constants.ascii_whitespace}"
    __tag_attribute_name_start = f"{string.ascii_letters}_:"
    __html_block_1_start_tag_prefix = ["script", "pre", "style"]
    __html_tag_attribute_value_terminators = " \"'=<>`"
    __html_block_2_to_5_start = "!"
    __html_block_2_continued_start = "--"
    __html_block_2_xx = f"{__html_block_2_to_5_start}{__html_block_2_continued_start}"
    __html_block_3_continued_start = "?"
    __html_block_4_continued_start = string.ascii_uppercase
    __html_block_5_continued_start = "[CDATA["
    __html_block_5_xx = f"{__html_block_2_to_5_start}{__html_block_5_continued_start}"
    __html_block_1_end_tags = ["</script>", "</pre>", "</style>"]
    __html_block_2_end = "-->"
    __html_block_3_end = "?>"
    __html_block_4_end = __html_tag_end
    __html_block_5_end = "]]>"

    __attribute_start_characters = "abcdefghijklmnopqrstuvwxyz1234567890:_"
    __attribute_other_characters = f"{__attribute_start_characters}.-"

    __raw_declaration_start_character = "!"
    __raw_declaration_whitespace = ParserHelper.space_character
    __raw_html_exclusion_1 = ">"
    __raw_html_exclusion_2 = "->"
    __raw_html_exclusion_3 = "-"
    __raw_html_exclusion_4 = "--"

    __html_block_6_start = [
        "address",
        "article",
        "aside",
        "base",
        "basefont",
        "blockquote",
        "body",
        "caption",
        "center",
        "col",
        "colgroup",
        "dd",
        "details",
        "dialog",
        "dir",
        "div",
        "dl",
        "dt",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "frame",
        "frameset",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "head",
        "header",
        "hr",
        "html",
        "iframe",
        "legend",
        "li",
        "link",
        "main",
        "menu",
        "menuitem",
        "nav",
        "noframes",
        "ol",
        "optgroup",
        "option",
        "p",
        "param",
        "section",
        "source",
        "summary",
        "table",
        "tbody",
        "td",
        "tfoot",
        "th",
        "thead",
        "title",
        "tr",
        "track",
        "ul",
    ]

    @staticmethod
    def is_valid_tag_name(tag_name: str) -> bool:
        """
        Determine if the html tag name is valid according to the html rules.
        """

        return (
            all(
                next_character in HtmlHelper.__valid_tag_name_characters
                for next_character in tag_name.lower()
            )
            if tag_name
            else False
        )

    @staticmethod
    def extract_html_attribute_name(string_to_parse: str, string_index: int) -> int:
        """
        Attempt to extract the attribute name from the provided string.
        """

        string_to_parse_length = len(string_to_parse)
        if not (
            string_index < string_to_parse_length
            and (
                string_to_parse[string_index] in HtmlHelper.__attribute_start_characters
            )
        ):
            return -1

        new_string_index, __ = ParserHelper.collect_while_one_of_characters(
            string_to_parse, string_index + 1, HtmlHelper.__attribute_other_characters
        )
        assert new_string_index is not None

        if new_string_index < string_to_parse_length and string_to_parse[
            new_string_index
        ] in [
            HtmlHelper.__html_attribute_name_value_separator,
            HtmlHelper.__html_attribute_separator,
            HtmlHelper.__html_tag_start,
            HtmlHelper.__html_tag_end,
        ]:
            return new_string_index
        return -1

    @staticmethod
    def extract_optional_attribute_value(line_to_parse: str, value_index: int) -> int:
        """
        Determine and extract an optional attribute value.
        """

        non_whitespace_index, _ = ParserHelper.extract_spaces(
            line_to_parse, value_index
        )
        assert non_whitespace_index is not None
        line_to_parse_size = len(line_to_parse)
        if (
            non_whitespace_index < line_to_parse_size
            and line_to_parse[non_whitespace_index]
            != HtmlHelper.__html_attribute_name_value_separator
        ) or non_whitespace_index >= line_to_parse_size:
            return non_whitespace_index

        non_whitespace_index, _ = ParserHelper.extract_spaces(
            line_to_parse, non_whitespace_index + 1
        )
        assert non_whitespace_index is not None
        if non_whitespace_index < line_to_parse_size:
            first_character_of_value = line_to_parse[non_whitespace_index]
            extracted_text: Optional[str] = None
            if first_character_of_value == HtmlHelper.__html_attribute_value_double:
                (
                    non_whitespace_index,
                    extracted_text,
                ) = ParserHelper.collect_until_character(
                    line_to_parse,
                    non_whitespace_index + 1,
                    HtmlHelper.__html_attribute_value_double,
                )
                assert non_whitespace_index is not None
                if non_whitespace_index == line_to_parse_size:
                    return -1
                non_whitespace_index += 1
            elif first_character_of_value == HtmlHelper.__html_attribute_value_single:
                (
                    non_whitespace_index,
                    extracted_text,
                ) = ParserHelper.collect_until_character(
                    line_to_parse,
                    non_whitespace_index + 1,
                    HtmlHelper.__html_attribute_value_single,
                )
                assert non_whitespace_index is not None
                if non_whitespace_index == line_to_parse_size:
                    return -1
                non_whitespace_index += 1
            else:
                (
                    non_whitespace_index,
                    extracted_text,
                ) = ParserHelper.collect_until_one_of_characters(
                    line_to_parse,
                    non_whitespace_index,
                    HtmlHelper.__html_tag_attribute_value_terminators,
                )
                assert non_whitespace_index is not None

                if not extracted_text:
                    non_whitespace_index = -1
        else:
            non_whitespace_index = -1
        return non_whitespace_index

    @staticmethod
    def is_complete_html_end_tag(
        tag_name: str, line_to_parse: str, next_char_index: int
    ) -> Tuple[bool, int]:
        """
        Determine if the supplied information is a completed end of tag specification.
        """

        is_valid = HtmlHelper.is_valid_tag_name(tag_name)
        non_whitespace_index, _ = ParserHelper.extract_spaces(
            line_to_parse, next_char_index
        )
        assert non_whitespace_index is not None
        is_valid = is_valid and (
            non_whitespace_index < len(line_to_parse)
            and line_to_parse[non_whitespace_index] == HtmlHelper.__html_tag_end
        )
        return is_valid, non_whitespace_index + 1

    @staticmethod
    def __is_valid_block_1_tag_name(tag_name: str) -> bool:
        """
        Determine if the tag name is a valid block-1 html tag name.
        """

        return tag_name in HtmlHelper.__html_block_1_start_tag_prefix

    @staticmethod
    def is_complete_html_start_tag(
        tag_name: str, line_to_parse: str, next_char_index: int
    ) -> Tuple[bool, Optional[int]]:
        """
        Determine if the supplied information is a completed start of tag specification.
        """

        is_tag_valid = HtmlHelper.is_valid_tag_name(
            tag_name
        ) and not HtmlHelper.__is_valid_block_1_tag_name(tag_name)

        non_whitespace_index, extracted_whitespace = ParserHelper.extract_spaces(
            line_to_parse, next_char_index
        )
        assert non_whitespace_index is not None
        are_attributes_valid: bool = True
        line_to_parse_size: int = len(line_to_parse)
        while (
            is_tag_valid
            and extracted_whitespace
            and are_attributes_valid
            and 0 <= non_whitespace_index < line_to_parse_size
            and line_to_parse[non_whitespace_index]
            not in [HtmlHelper.__html_tag_end, HtmlHelper.__html_tag_start]
        ):

            non_whitespace_index = HtmlHelper.extract_html_attribute_name(
                line_to_parse, non_whitespace_index
            )
            assert non_whitespace_index is not None
            are_attributes_valid = non_whitespace_index != -1
            if not are_attributes_valid:
                break
            non_whitespace_index = HtmlHelper.extract_optional_attribute_value(
                line_to_parse, non_whitespace_index
            )
            assert non_whitespace_index is not None
            are_attributes_valid = non_whitespace_index != -1
            if not are_attributes_valid:
                break
            (
                non_whitespace_index,
                extracted_whitespace,
            ) = ParserHelper.extract_spaces(line_to_parse, non_whitespace_index)
            assert non_whitespace_index is not None

        if non_whitespace_index < line_to_parse_size:
            if line_to_parse[non_whitespace_index] == HtmlHelper.__html_tag_start:
                non_whitespace_index += 1
            is_end_of_tag_present = (
                line_to_parse[non_whitespace_index] == HtmlHelper.__html_tag_end
            )
            if is_end_of_tag_present:
                non_whitespace_index += 1
        else:
            is_end_of_tag_present = False

        non_whitespace_index, _ = ParserHelper.extract_spaces(
            line_to_parse, non_whitespace_index
        )
        return (
            (
                is_tag_valid
                and is_end_of_tag_present
                and non_whitespace_index == line_to_parse_size
                and are_attributes_valid
            ),
            non_whitespace_index,
        )

    @staticmethod
    def __parse_raw_tag_name(text_to_parse: str, start_index: int) -> str:
        """
        Parse a HTML tag name from the string.
        """
        if ParserHelper.is_character_at_index_one_of(
            text_to_parse, start_index, HtmlHelper.__valid_tag_name_start
        ):
            index, __ = ParserHelper.collect_while_one_of_characters(
                text_to_parse, start_index + 1, HtmlHelper.__valid_tag_name_characters
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
            text_to_parse, start_index, HtmlHelper.__tag_attribute_name_characters
        )
        assert parse_index is not None
        end_name_index, extracted_whitespace = ParserHelper.extract_ascii_whitespace(
            text_to_parse, parse_index
        )
        assert end_name_index is not None
        if ParserHelper.is_character_at_index(
            text_to_parse,
            end_name_index,
            HtmlHelper.__html_attribute_name_value_separator,
        ):
            (
                value_start_index,
                extracted_whitespace,
            ) = ParserHelper.extract_ascii_whitespace(text_to_parse, end_name_index + 1)
            assert value_start_index is not None
            value_end_index: Optional[int] = None
            if ParserHelper.is_character_at_index_one_of(
                text_to_parse,
                value_start_index,
                HtmlHelper.__html_attribute_value_single,
            ):
                value_end_index, _ = ParserHelper.collect_until_character(
                    text_to_parse,
                    value_start_index + 1,
                    HtmlHelper.__html_attribute_value_single,
                )
                assert value_end_index is not None
                if not ParserHelper.is_character_at_index(
                    text_to_parse,
                    value_end_index,
                    HtmlHelper.__html_attribute_value_single,
                ):
                    return None, None
                value_end_index += 1
            elif ParserHelper.is_character_at_index_one_of(
                text_to_parse,
                value_start_index,
                HtmlHelper.__html_attribute_value_double,
            ):
                value_end_index, _ = ParserHelper.collect_until_character(
                    text_to_parse,
                    value_start_index + 1,
                    HtmlHelper.__html_attribute_value_double,
                )
                assert value_end_index is not None
                if not ParserHelper.is_character_at_index(
                    text_to_parse,
                    value_end_index,
                    HtmlHelper.__html_attribute_value_double,
                ):
                    return None, None
                value_end_index += 1
            else:
                value_end_index, _ = ParserHelper.collect_until_one_of_characters(
                    text_to_parse,
                    value_start_index,
                    HtmlHelper.__unquoted_attribute_value_stop,
                )
            assert value_end_index is not None
            (
                end_name_index,
                extracted_whitespace,
            ) = ParserHelper.extract_ascii_whitespace(text_to_parse, value_end_index)

        return end_name_index, extracted_whitespace

    @staticmethod
    def __parse_raw_open_tag(text_to_parse: str) -> Tuple[Optional[str], int]:
        """
        Parse the current line as if it is an open tag, and determine if it is valid.
        """

        end_parse_index, valid_raw_html, tag_name = (
            -1,
            None,
            HtmlHelper.__parse_raw_tag_name(text_to_parse, 0),
        )
        if tag_name:
            parse_index, extracted_whitespace = ParserHelper.extract_ascii_whitespace(
                text_to_parse, len(tag_name)
            )
            assert parse_index is not None
            while extracted_whitespace and ParserHelper.is_character_at_index_one_of(
                text_to_parse,
                parse_index,
                HtmlHelper.__tag_attribute_name_start,
            ):
                (
                    parse_index,
                    extracted_whitespace,
                ) = HtmlHelper.__parse_tag_attributes(text_to_parse, parse_index)
                if parse_index is None:
                    return None, -1

            if ParserHelper.is_character_at_index(
                text_to_parse, parse_index, HtmlHelper.__html_tag_start
            ):
                parse_index += 1

            if ParserHelper.is_character_at_index(
                text_to_parse, parse_index, HtmlHelper.__html_tag_end
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
            text_to_parse, 0, HtmlHelper.__html_tag_start
        ):
            if tag_name := HtmlHelper.__parse_raw_tag_name(text_to_parse, 1):
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
    def __parse_raw_declaration(text_to_parse: str) -> Optional[str]:
        """
        Parse a possible raw html declaration sequence, and return if it is valid.
        """

        valid_raw_html = None
        if ParserHelper.is_character_at_index_one_of(
            text_to_parse, 0, HtmlHelper.__raw_declaration_start_character
        ):
            (
                parse_index,
                declaration_name,
            ) = ParserHelper.collect_while_one_of_characters(
                text_to_parse, 1, HtmlHelper.__html_block_4_continued_start
            )
            assert parse_index is not None
            if declaration_name:
                whitespace_count, _ = ParserHelper.collect_while_character(
                    text_to_parse, parse_index, HtmlHelper.__raw_declaration_whitespace
                )
                if whitespace_count:
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
                        remaining_line[0] == HtmlHelper.__raw_html_exclusion_1
                        or remaining_line.startswith(HtmlHelper.__raw_html_exclusion_2)
                        or remaining_line[-1] == HtmlHelper.__raw_html_exclusion_3
                        or HtmlHelper.__raw_html_exclusion_4 in remaining_line
                    )
                ):
                    valid_raw_html = (
                        f"{special_start}{remaining_line}{special_end[:-1]}"
                    )
        return valid_raw_html, parse_index

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

        valid_raw_html, remaining_line_parse_index = HtmlHelper.__parse_raw_open_tag(
            remaining_line
        )
        if not valid_raw_html:
            valid_raw_html = HtmlHelper.__parse_raw_close_tag(only_between_angles)
        if not valid_raw_html:
            (
                valid_raw_html,
                remaining_line_parse_index,
            ) = HtmlHelper.__process_raw_special(
                remaining_line,
                HtmlHelper.__html_block_2_xx,
                HtmlHelper.__html_block_2_end,
                True,
            )
        if not valid_raw_html:
            (
                valid_raw_html,
                remaining_line_parse_index,
            ) = HtmlHelper.__process_raw_special(
                remaining_line,
                HtmlHelper.__html_block_3_continued_start,
                HtmlHelper.__html_block_3_end,
            )
        if not valid_raw_html:
            (
                valid_raw_html,
                remaining_line_parse_index,
            ) = HtmlHelper.__process_raw_special(
                remaining_line,
                HtmlHelper.__html_block_5_xx,
                HtmlHelper.__html_block_5_end,
            )
        if not valid_raw_html:
            valid_raw_html = HtmlHelper.__parse_raw_declaration(only_between_angles)

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
    def __check_for_special_html_blocks(
        line_to_parse: str, character_index: int
    ) -> Optional[str]:
        """
        Check for the easy to spot special blocks: 2-5.
        """

        if character_index >= len(line_to_parse):
            return None
        html_block_type = None
        if ParserHelper.is_character_at_index(
            line_to_parse, character_index, HtmlHelper.__html_block_2_to_5_start
        ):
            if ParserHelper.are_characters_at_index(
                line_to_parse,
                character_index + 1,
                HtmlHelper.__html_block_2_continued_start,
            ):
                html_block_type = HtmlHelper.html_block_2
            elif ParserHelper.is_character_at_index_one_of(
                line_to_parse,
                character_index + 1,
                HtmlHelper.__html_block_4_continued_start,
            ):
                html_block_type = HtmlHelper.html_block_4
            elif ParserHelper.are_characters_at_index(
                line_to_parse,
                character_index + 1,
                HtmlHelper.__html_block_5_continued_start,
            ):
                html_block_type = HtmlHelper.html_block_5
        elif ParserHelper.is_character_at_index(
            line_to_parse,
            character_index,
            HtmlHelper.__html_block_3_continued_start,
        ):
            html_block_type = HtmlHelper.html_block_3

        return html_block_type

    @staticmethod
    def __check_for_normal_html_blocks_adjust_tag(
        remaining_html_tag: str, line_to_parse: str, character_index: int
    ) -> Tuple[str, int, bool]:

        adjusted_remaining_html_tag, line_to_parse_size = remaining_html_tag, len(
            line_to_parse
        )
        is_end_tag = (
            bool(adjusted_remaining_html_tag)
            and adjusted_remaining_html_tag[0] == HtmlHelper.__html_tag_start
        )
        if is_end_tag:
            adjusted_remaining_html_tag = adjusted_remaining_html_tag[1:]

        if (
            character_index < line_to_parse_size
            and line_to_parse[character_index] == HtmlHelper.__html_tag_end
            and adjusted_remaining_html_tag
            and adjusted_remaining_html_tag[-1] == HtmlHelper.__html_tag_start
        ):
            adjusted_remaining_html_tag = adjusted_remaining_html_tag[:-1]

        return adjusted_remaining_html_tag, line_to_parse_size, is_end_tag

    @staticmethod
    def __check_for_normal_html_blocks(
        remaining_html_tag: str, line_to_parse: str, character_index: int
    ) -> Optional[str]:
        """
        Check for the the html blocks that are harder to identify: 1, 6-7.
        """

        html_block_type = None

        if HtmlHelper.__is_valid_block_1_tag_name(remaining_html_tag):
            html_block_type = HtmlHelper.html_block_1
        else:
            (
                adjusted_remaining_html_tag,
                line_to_parse_size,
                is_end_tag,
            ) = HtmlHelper.__check_for_normal_html_blocks_adjust_tag(
                remaining_html_tag, line_to_parse, character_index
            )

            complete_parse_index: Optional[int] = 0
            if adjusted_remaining_html_tag in HtmlHelper.__html_block_6_start:
                html_block_type = HtmlHelper.html_block_6
            elif is_end_tag:
                is_complete, complete_parse_index = HtmlHelper.is_complete_html_end_tag(
                    adjusted_remaining_html_tag, line_to_parse, character_index
                )
                if is_complete:
                    html_block_type, character_index = (
                        HtmlHelper.html_block_7,
                        complete_parse_index,
                    )
            else:
                (
                    is_complete,
                    complete_parse_index,
                ) = HtmlHelper.is_complete_html_start_tag(
                    adjusted_remaining_html_tag, line_to_parse, character_index
                )
                if is_complete:
                    assert complete_parse_index is not None
                    html_block_type, character_index = (
                        HtmlHelper.html_block_7,
                        complete_parse_index,
                    )
            if html_block_type == HtmlHelper.html_block_7:
                new_index, _ = ParserHelper.extract_ascii_whitespace(
                    line_to_parse, character_index
                )
                if new_index != line_to_parse_size:
                    html_block_type = None
        return html_block_type

    @staticmethod
    def __determine_html_block_type(
        token_stack: List[StackToken], line_to_parse: str, start_index: int
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Determine the type of the html block that we are starting.
        """

        character_index = start_index + 1
        html_block_type = HtmlHelper.__check_for_special_html_blocks(
            line_to_parse, character_index
        )
        if html_block_type:
            remaining_html_tag = ""
        else:
            (
                new_character_index,
                new_remaining_html_tag,
            ) = ParserHelper.collect_until_one_of_characters(
                line_to_parse, character_index, HtmlHelper.__html_tag_name_end
            )
            assert new_character_index is not None
            assert new_remaining_html_tag is not None
            remaining_html_tag = new_remaining_html_tag
            character_index = new_character_index
            remaining_html_tag = remaining_html_tag.lower()

            html_block_type = HtmlHelper.__check_for_normal_html_blocks(
                remaining_html_tag, line_to_parse, character_index
            )

        POGGER.debug("html_block_type=$", html_block_type)
        if not html_block_type:
            return None, None
        if html_block_type == HtmlHelper.html_block_7 and token_stack[-1].is_paragraph:
            POGGER.debug("html_block_type 7 cannot interrupt a paragraph")
            return None, None
        return html_block_type, remaining_html_tag

    @staticmethod
    def is_html_block(
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        token_stack: List[StackToken],
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Determine if the current sequence of characters would start a html block element.
        """

        assert extracted_whitespace is not None
        if (
            TabHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index(
            line_to_parse,
            start_index,
            HtmlHelper.__html_block_start_character,
        ):
            (
                html_block_type,
                remaining_html_tag,
            ) = HtmlHelper.__determine_html_block_type(
                token_stack,
                line_to_parse,
                start_index,
            )
        else:
            html_block_type, remaining_html_tag = None, None
        return html_block_type, remaining_html_tag

    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_html_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        block_quote_data: BlockQuoteData,
        original_line: str,
    ) -> Tuple[List[MarkdownToken], bool]:
        """
        Determine if we have the criteria that we need to start an HTML block.
        """

        html_block_type, _ = HtmlHelper.is_html_block(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
            parser_state.token_stack,
        )
        did_adjust_block_quote = False
        POGGER.debug("did_adjust_block_quote=$", did_adjust_block_quote)
        if html_block_type:
            new_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[ParagraphStackToken],
            )
            POGGER.debug("new_tokens=$", new_tokens)

            split_tab = False
            if ParserHelper.tab_character in original_line:
                token_text = position_marker.text_to_parse[
                    position_marker.index_number :
                ]
                POGGER.debug("original_line=:$:", original_line)
                POGGER.debug("token_text=:$:", token_text)
                POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
                _, split_tab, _ = TabHelper.parse_thematic_break_with_tab(
                    original_line, token_text, extracted_whitespace
                )
                POGGER.debug("split_tab=:$:", split_tab)

            POGGER.debug("did_adjust_block_quote=$", did_adjust_block_quote)
            POGGER.debug("split_tab=$", split_tab)
            old_split_tab = split_tab
            did_adjust_block_quote = False
            if split_tab := ContainerHelper.reduce_containers_if_required(
                parser_state, block_quote_data, new_tokens, split_tab
            ):
                TabHelper.adjust_block_quote_indent_for_tab(parser_state)
                did_adjust_block_quote = True
                POGGER.debug("did_adjust_block_quote=$", did_adjust_block_quote)
            POGGER.debug("split_tab=$", split_tab)
            did_adjust_block_quote = (
                split_tab != old_split_tab or did_adjust_block_quote
            )

            assert extracted_whitespace is not None
            new_token = HtmlBlockMarkdownToken(position_marker, extracted_whitespace)
            new_tokens.append(new_token)
            parser_state.token_stack.append(
                HtmlBlockStackToken(html_block_type, new_token)
            )
        else:
            new_tokens = []
        POGGER.debug("did_adjust_block_quote=$", did_adjust_block_quote)
        return new_tokens, did_adjust_block_quote

    # pylint: enable=too-many-arguments

    @staticmethod
    def check_blank_html_block_end(parser_state: ParserState) -> List[MarkdownToken]:
        """
        Check to see if we have encountered the end of the current HTML block
        via an empty line or BLANK.
        """

        assert parser_state.token_stack[-1].is_html_block
        html_token = cast(HtmlBlockStackToken, parser_state.token_stack[-1])
        if html_token.html_block_type in [
            HtmlHelper.html_block_6,
            HtmlHelper.html_block_7,
        ]:
            new_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[HtmlBlockStackToken],
            )
            POGGER.debug("new_tokens=$", new_tokens)
        else:
            new_tokens = []

        return new_tokens

    # pylint: disable=too-many-arguments
    @staticmethod
    def __check_normal_html_block_end_with_tab(
        parser_state: ParserState,
        original_line: str,
        extracted_whitespace: str,
        token_text: str,
        did_adjust_block_quote: bool,
    ) -> Tuple[str, str]:

        POGGER.debug("did_adjust_block_quote>:$:<", did_adjust_block_quote)
        (
            tabified_text,
            split_tab,
            tabified_whitespace,
        ) = TabHelper.parse_thematic_break_with_tab(
            original_line, token_text, extracted_whitespace
        )

        POGGER.debug("tabified_text>:$:<", tabified_text)
        POGGER.debug("tabified_whitespace>:$:<", tabified_whitespace)
        POGGER.debug("split_tab>:$:<", split_tab)

        if split_tab:
            POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
            assert tabified_whitespace is not None
            tabified_whitespace = ParserHelper.create_replacement_markers(
                tabified_whitespace, extracted_whitespace
            )
            POGGER.debug("tabified_whitespace>:$:<", tabified_whitespace)
            if not did_adjust_block_quote:
                TabHelper.adjust_block_quote_indent_for_tab(parser_state)
        assert tabified_whitespace is not None
        return tabified_whitespace, tabified_text

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def check_normal_html_block_end(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: str,
        position_marker: PositionMarker,
        original_line: str,
        did_adjust_block_quote: bool,
    ) -> List[MarkdownToken]:
        """
        Check to see if we have encountered the end of the current HTML block
        via text on a normal line.
        """

        token_text = line_to_parse[start_index:]
        POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
        POGGER.debug("token_text=:$:", token_text)
        POGGER.debug("original_line=:$:", original_line)
        if ParserHelper.tab_character in original_line:
            (
                extracted_whitespace,
                token_text,
            ) = HtmlHelper.__check_normal_html_block_end_with_tab(
                parser_state,
                original_line,
                extracted_whitespace,
                token_text,
                did_adjust_block_quote,
            )

        new_tokens: List[MarkdownToken] = [
            TextMarkdownToken(
                token_text,
                extracted_whitespace,
                position_marker=position_marker,
            )
        ]

        is_block_terminated, adj_line = False, line_to_parse[start_index:]
        assert parser_state.token_stack[-1].is_html_block
        html_token = cast(HtmlBlockStackToken, parser_state.token_stack[-1])
        if html_token.html_block_type == HtmlHelper.html_block_1:
            for next_end_tag in HtmlHelper.__html_block_1_end_tags:
                if next_end_tag in adj_line:
                    is_block_terminated = True
        elif html_token.html_block_type == HtmlHelper.html_block_2:
            is_block_terminated = HtmlHelper.__html_block_2_end in adj_line
        elif html_token.html_block_type == HtmlHelper.html_block_3:
            is_block_terminated = HtmlHelper.__html_block_3_end in adj_line
        elif html_token.html_block_type == HtmlHelper.html_block_4:
            is_block_terminated = HtmlHelper.__html_block_4_end in adj_line
        elif html_token.html_block_type == HtmlHelper.html_block_5:
            is_block_terminated = HtmlHelper.__html_block_5_end in adj_line

        if is_block_terminated:
            terminated_block_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[HtmlBlockStackToken],
            )
            POGGER.debug("terminated_block_tokens=$", terminated_block_tokens)
            assert terminated_block_tokens
            new_tokens.extend(terminated_block_tokens)
        return new_tokens

    # pylint: enable=too-many-arguments
