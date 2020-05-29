"""
Module to provide helper functions for parsing html.
"""
import logging
import string

from pymarkdown.constants import Constants
from pymarkdown.markdown_token import (
    HtmlBlockMarkdownToken,
    RawHtmlMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.stack_token import HtmlBlockStackToken, ParagraphStackToken

LOGGER = logging.getLogger(__name__)


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
    __html_attribute_separator = " "
    __valid_tag_name_start = string.ascii_letters
    __valid_tag_name_characters = string.ascii_letters + string.digits + "-"
    __tag_attribute_name_characters = string.ascii_letters + string.digits + "_.:-"
    __unquoted_attribute_value_stop = "\"'=<>`" + Constants.whitespace
    __tag_attribute_name_start = string.ascii_letters + "_:"
    __html_block_1_start_tag_prefix = ["script", "pre", "style"]
    __html_tag_attribute_value_terminators = " \"'=<>`"
    __html_block_2_to_5_start = "!"
    __html_block_2_continued_start = "--"
    __html_block_3_continued_start = "?"
    __html_block_4_continued_start = string.ascii_uppercase
    __html_block_5_continued_start = "[CDATA["
    __html_block_1_end_tags = ["</script>", "</pre>", "</style>"]
    __html_block_2_end = "-->"
    __html_block_3_end = "?>"
    __html_block_4_end = __html_tag_end
    __html_block_5_end = "]]>"

    __raw_declaration_start_character = "!"
    __raw_declaration_whitespace = " "
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
    def is_valid_tag_name(tag_name):
        """
        Determine if the html tag name is valid according to the html rules.
        """

        is_valid = bool(tag_name)
        for next_character in tag_name.lower():
            if not (
                ("a" <= next_character <= "z")
                or ("0" <= next_character <= "9")
                or next_character == "-"
            ):
                is_valid = False
        return is_valid

    @staticmethod
    def extract_html_attribute_name(string_to_parse, string_index):
        """
        Attempt to extract the attribute name from the provided string.
        """

        if not (
            string_index < len(string_to_parse)
            and (
                (
                    # TODO https://stackoverflow.com/questions/16060899/alphabet-range-in-python
                    "a"
                    <= string_to_parse[string_index]
                    <= "z"
                )
                or ("A" <= string_to_parse[string_index] <= "Z")
                or ("0" <= string_to_parse[string_index] <= "9")
                or string_to_parse[string_index] == ":"
                or string_to_parse[string_index] == "_"
            )
        ):
            return -1
        string_index += 1
        while string_index < len(string_to_parse):
            if not (
                ("a" <= string_to_parse[string_index] <= "z")
                or ("A" <= string_to_parse[string_index] <= "Z")
                or ("0" <= string_to_parse[string_index] <= "9")
                or string_to_parse[string_index] == ":"
                or string_to_parse[string_index] == "."
                or string_to_parse[string_index] == "-"
                or string_to_parse[string_index] == "_"
            ):
                break
            string_index += 1

        if string_index < len(string_to_parse) and (
            string_to_parse[string_index]
            == HtmlHelper.__html_attribute_name_value_separator
            or string_to_parse[string_index] == HtmlHelper.__html_attribute_separator
            or string_to_parse[string_index] == HtmlHelper.__html_tag_start
            or string_to_parse[string_index] == HtmlHelper.__html_tag_end
        ):
            return string_index
        return -1

    @staticmethod
    def extract_optional_attribute_value(line_to_parse, value_index):
        """
        Determine and extract an optional attribute value.
        """

        non_whitespace_index, _ = ParserHelper.extract_whitespace(
            line_to_parse, value_index
        )
        if (
            non_whitespace_index < len(line_to_parse)
            and line_to_parse[non_whitespace_index]
            != HtmlHelper.__html_attribute_name_value_separator
        ) or non_whitespace_index >= len(line_to_parse):
            return non_whitespace_index

        non_whitespace_index += 1
        non_whitespace_index, _ = ParserHelper.extract_whitespace(
            line_to_parse, non_whitespace_index
        )
        if non_whitespace_index < len(line_to_parse):
            first_character_of_value = line_to_parse[non_whitespace_index]
            if first_character_of_value == HtmlHelper.__html_attribute_value_double:
                (
                    non_whitespace_index,
                    extracted_text,
                ) = ParserHelper.collect_until_character(
                    line_to_parse,
                    non_whitespace_index + 1,
                    HtmlHelper.__html_attribute_value_double,
                )
                if non_whitespace_index == len(line_to_parse):
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
                if non_whitespace_index == len(line_to_parse):
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

                if not extracted_text:
                    non_whitespace_index = -1
        else:
            non_whitespace_index = -1
        return non_whitespace_index

    @staticmethod
    def is_complete_html_end_tag(tag_name, line_to_parse, next_char_index):
        """
        Determine if the supplied information is a completed end of tag specification.
        """

        is_valid = HtmlHelper.is_valid_tag_name(tag_name)
        non_whitespace_index, _ = ParserHelper.extract_whitespace(
            line_to_parse, next_char_index
        )
        have_end_of_tag = (
            non_whitespace_index < len(line_to_parse)
            and line_to_parse[non_whitespace_index] == HtmlHelper.__html_tag_end
        )
        return have_end_of_tag and is_valid, non_whitespace_index + 1

    @staticmethod
    def __is_valid_block_1_tag_name(tag_name):
        """
        Determine if the tag name is a valid block-1 html tag name.
        """

        is_tag_valid = tag_name in HtmlHelper.__html_block_1_start_tag_prefix
        return is_tag_valid

    @staticmethod
    def is_complete_html_start_tag(tag_name, line_to_parse, next_char_index):
        """
        Determine if the supplied information is a completed start of tag specification.
        """

        is_tag_valid = HtmlHelper.is_valid_tag_name(
            tag_name
        ) and not HtmlHelper.__is_valid_block_1_tag_name(tag_name)

        non_whitespace_index, extracted_whitespace = ParserHelper.extract_whitespace(
            line_to_parse, next_char_index
        )

        are_attributes_valid = True
        while (
            is_tag_valid
            and extracted_whitespace
            and are_attributes_valid
            and (0 <= non_whitespace_index < len(line_to_parse))
            and not (
                line_to_parse[non_whitespace_index] == HtmlHelper.__html_tag_end
                or line_to_parse[non_whitespace_index] == HtmlHelper.__html_tag_start
            )
        ):

            non_whitespace_index = HtmlHelper.extract_html_attribute_name(
                line_to_parse, non_whitespace_index
            )
            if non_whitespace_index == -1:
                are_attributes_valid = False
                break
            non_whitespace_index = HtmlHelper.extract_optional_attribute_value(
                line_to_parse, non_whitespace_index
            )
            if non_whitespace_index == -1:
                are_attributes_valid = False
                break
            (
                non_whitespace_index,
                extracted_whitespace,
            ) = ParserHelper.extract_whitespace(line_to_parse, non_whitespace_index)

        is_end_of_tag_present = False
        if (
            non_whitespace_index < len(line_to_parse)
            and line_to_parse[non_whitespace_index] == HtmlHelper.__html_tag_start
        ):
            non_whitespace_index += 1
        if (
            non_whitespace_index < len(line_to_parse)
            and line_to_parse[non_whitespace_index] == HtmlHelper.__html_tag_end
        ):
            non_whitespace_index += 1
            is_end_of_tag_present = True

        non_whitespace_index, _ = ParserHelper.extract_whitespace(
            line_to_parse, non_whitespace_index
        )
        at_eol = non_whitespace_index == len(line_to_parse)
        return (
            (
                is_tag_valid
                and is_end_of_tag_present
                and at_eol
                and are_attributes_valid
            ),
            non_whitespace_index,
        )

    @staticmethod
    def __parse_raw_tag_name(text_to_parse, start_index):
        """
        Parse a HTML tag name from the string.
        """
        tag_name = ""
        if ParserHelper.is_character_at_index_one_of(
            text_to_parse, start_index, HtmlHelper.__valid_tag_name_start
        ):
            index = start_index + 1
            while ParserHelper.is_character_at_index_one_of(
                text_to_parse, index, HtmlHelper.__valid_tag_name_characters
            ):
                index += 1
            tag_name = text_to_parse[0:index]
        return tag_name

    @staticmethod
    def __parse_tag_attributes(text_to_parse, start_index):
        """
        Handle the parsing of the attributes for an open tag.
        """
        parse_index, _ = ParserHelper.collect_while_one_of_characters(
            text_to_parse, start_index, HtmlHelper.__tag_attribute_name_characters
        )
        end_name_index, extracted_whitespace = ParserHelper.extract_any_whitespace(
            text_to_parse, parse_index
        )
        if ParserHelper.is_character_at_index(
            text_to_parse,
            end_name_index,
            HtmlHelper.__html_attribute_name_value_separator,
        ):
            (
                value_start_index,
                extracted_whitespace,
            ) = ParserHelper.extract_any_whitespace(text_to_parse, end_name_index + 1)
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
                if not ParserHelper.is_character_at_index(
                    text_to_parse,
                    value_end_index,
                    HtmlHelper.__html_attribute_value_single,
                ):
                    return None, -1
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
                if not ParserHelper.is_character_at_index(
                    text_to_parse,
                    value_end_index,
                    HtmlHelper.__html_attribute_value_double,
                ):
                    return None, -1
                value_end_index += 1
            else:
                value_end_index, _ = ParserHelper.collect_until_one_of_characters(
                    text_to_parse,
                    value_start_index,
                    HtmlHelper.__unquoted_attribute_value_stop,
                )
            end_name_index, extracted_whitespace = ParserHelper.extract_any_whitespace(
                text_to_parse, value_end_index
            )

        return end_name_index, extracted_whitespace

    @staticmethod
    def __parse_raw_open_tag(text_to_parse):
        """
        Parse the current line as if it is an open tag, and determine if it is valid.
        """

        end_parse_index = -1
        valid_raw_html = None
        tag_name = HtmlHelper.__parse_raw_tag_name(text_to_parse, 0)
        if tag_name:
            parse_index, extracted_whitespace = ParserHelper.extract_any_whitespace(
                text_to_parse, len(tag_name)
            )
            if extracted_whitespace:
                while (
                    extracted_whitespace
                    and ParserHelper.is_character_at_index_one_of(
                        text_to_parse,
                        parse_index,
                        HtmlHelper.__tag_attribute_name_start,
                    )
                ):
                    (
                        parse_index,
                        extracted_whitespace,
                    ) = HtmlHelper.__parse_tag_attributes(text_to_parse, parse_index)
                    if parse_index is None:
                        return parse_index, extracted_whitespace

            if ParserHelper.is_character_at_index(
                text_to_parse, parse_index, HtmlHelper.__html_tag_start
            ):
                parse_index += 1

            if ParserHelper.is_character_at_index(
                text_to_parse, parse_index, HtmlHelper.__html_tag_end
            ):
                valid_raw_html = text_to_parse[0:parse_index]
                end_parse_index = parse_index + 1

        return valid_raw_html, end_parse_index

    @staticmethod
    def __parse_raw_close_tag(text_to_parse):
        """
        Parse the current line as if it is a close tag, and determine if it is valid.
        """
        valid_raw_html = None
        if ParserHelper.is_character_at_index(
            text_to_parse, 0, HtmlHelper.__html_tag_start
        ):
            tag_name = HtmlHelper.__parse_raw_tag_name(text_to_parse, 1)
            if tag_name:
                parse_index = len(tag_name)
                if parse_index != len(text_to_parse):
                    parse_index, _ = ParserHelper.extract_whitespace(
                        text_to_parse, parse_index
                    )
                if parse_index == len(text_to_parse):
                    valid_raw_html = text_to_parse
        return valid_raw_html

    @staticmethod
    def __parse_raw_declaration(text_to_parse):
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
            if declaration_name:
                whitespace_count, _ = ParserHelper.collect_while_character(
                    text_to_parse, parse_index, HtmlHelper.__raw_declaration_whitespace
                )
                if whitespace_count:
                    valid_raw_html = text_to_parse
        return valid_raw_html

    @staticmethod
    def __process_raw_special(
        remaining_line, special_start, special_end, do_extra_check=False,
    ):
        """
        Parse a possible raw html special sequence, and return if it is valid.
        """
        valid_raw_html = None
        parse_index = -1

        if remaining_line.startswith(special_start):
            remaining_line = remaining_line[len(special_start) :]
            parse_index = remaining_line.find(special_end)
        if parse_index != -1:
            remaining_line = remaining_line[0:parse_index]
            parse_index = parse_index + len(special_start) + len(special_end)
            if (not do_extra_check) or (
                not (
                    remaining_line.startswith(HtmlHelper.__raw_html_exclusion_1)
                    or remaining_line.startswith(HtmlHelper.__raw_html_exclusion_2)
                    or remaining_line.endswith(HtmlHelper.__raw_html_exclusion_3)
                    or HtmlHelper.__raw_html_exclusion_4 in remaining_line
                )
            ):
                valid_raw_html = special_start + remaining_line + special_end[0:-1]
        return valid_raw_html, parse_index

    @staticmethod
    def parse_raw_html(only_between_angles, remaining_line):
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
                HtmlHelper.__html_block_2_to_5_start
                + HtmlHelper.__html_block_2_continued_start,
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
                HtmlHelper.__html_block_2_to_5_start
                + HtmlHelper.__html_block_5_continued_start,
                HtmlHelper.__html_block_5_end,
            )
        if not valid_raw_html:
            valid_raw_html = HtmlHelper.__parse_raw_declaration(only_between_angles)

        if valid_raw_html:
            return RawHtmlMarkdownToken(valid_raw_html), remaining_line_parse_index
        return None, -1

    @staticmethod
    def __check_for_special_html_blocks(line_to_parse, character_index):
        """
        Check for the easy to spot special blocks: 2-5.
        """

        html_block_type = None
        if character_index < len(line_to_parse):
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
    def __check_for_normal_html_blocks(
        remaining_html_tag, line_to_parse, character_index
    ):
        """
        Check for the the html blocks that are harder to identify: 1, 6-7.
        """

        html_block_type = None

        if HtmlHelper.__is_valid_block_1_tag_name(remaining_html_tag):
            html_block_type = HtmlHelper.html_block_1
        else:
            adjusted_remaining_html_tag = remaining_html_tag
            is_end_tag = False
            if adjusted_remaining_html_tag.startswith(HtmlHelper.__html_tag_start):
                adjusted_remaining_html_tag = adjusted_remaining_html_tag[1:]
                is_end_tag = True
            if (
                character_index < len(line_to_parse)
                and line_to_parse[character_index] == HtmlHelper.__html_tag_end
                and adjusted_remaining_html_tag.endswith(HtmlHelper.__html_tag_start)
            ):
                adjusted_remaining_html_tag = adjusted_remaining_html_tag[0:-1]
            if adjusted_remaining_html_tag in HtmlHelper.__html_block_6_start:
                html_block_type = HtmlHelper.html_block_6
            elif is_end_tag:
                is_complete, complete_parse_index = HtmlHelper.is_complete_html_end_tag(
                    adjusted_remaining_html_tag, line_to_parse, character_index
                )
                if is_complete:
                    html_block_type = HtmlHelper.html_block_7
                    character_index = complete_parse_index
            else:
                (
                    is_complete,
                    complete_parse_index,
                ) = HtmlHelper.is_complete_html_start_tag(
                    adjusted_remaining_html_tag, line_to_parse, character_index
                )
                if is_complete:
                    html_block_type = HtmlHelper.html_block_7
                    character_index = complete_parse_index
            if html_block_type == HtmlHelper.html_block_7:
                new_index, _ = ParserHelper.extract_whitespace(
                    line_to_parse, character_index
                )
                if new_index != len(line_to_parse):
                    html_block_type = None
        return html_block_type

    @staticmethod
    def __determine_html_block_type(parser_state, line_to_parse, start_index):
        """
        Determine the type of the html block that we are starting.
        """

        character_index = start_index + 1
        remaining_html_tag = ""

        html_block_type = HtmlHelper.__check_for_special_html_blocks(
            line_to_parse, character_index
        )
        if not html_block_type:
            (
                character_index,
                remaining_html_tag,
            ) = ParserHelper.collect_until_one_of_characters(
                line_to_parse, character_index, HtmlHelper.__html_tag_name_end
            )
            remaining_html_tag = remaining_html_tag.lower()

            html_block_type = HtmlHelper.__check_for_normal_html_blocks(
                remaining_html_tag, line_to_parse, character_index
            )
        if not html_block_type:
            return None, None
        if html_block_type == HtmlHelper.html_block_7:
            if parser_state.token_stack[-1].is_paragraph:
                return None, None
        return html_block_type, remaining_html_tag

    @staticmethod
    def parse_html_block(parser_state, position_marker, extracted_whitespace):
        """
        Determine if we have the criteria that we need to start an HTML block.
        """

        new_tokens = []
        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index(
            position_marker.text_to_parse,
            position_marker.index_number,
            HtmlHelper.__html_block_start_character,
        ):
            (
                html_block_type,
                remaining_html_tag,
            ) = HtmlHelper.__determine_html_block_type(
                parser_state,
                position_marker.text_to_parse,
                position_marker.index_number,
            )
            if html_block_type:
                new_tokens, _, _ = parser_state.close_open_blocks_fn(
                    parser_state, only_these_blocks=[ParagraphStackToken],
                )
                parser_state.token_stack.append(
                    HtmlBlockStackToken(html_block_type, remaining_html_tag)
                )
                new_tokens.append(HtmlBlockMarkdownToken(position_marker))
        return new_tokens

    @staticmethod
    def check_blank_html_block_end(parser_state):
        """
        Check to see if we have encountered the end of the current HTML block
        via an empty line or BLANK.
        """

        new_tokens = []
        if (
            parser_state.token_stack[-1].html_block_type == HtmlHelper.html_block_6
            or parser_state.token_stack[-1].html_block_type == HtmlHelper.html_block_7
        ):
            new_tokens, _, _ = parser_state.close_open_blocks_fn(
                parser_state, only_these_blocks=[type(parser_state.token_stack[-1])],
            )

        return new_tokens

    @staticmethod
    def check_normal_html_block_end(
        parser_state, line_to_parse, start_index, extracted_whitespace,
    ):
        """
        Check to see if we have encountered the end of the current HTML block
        via text on a normal line.
        """

        new_tokens = [
            TextMarkdownToken(line_to_parse[start_index:], extracted_whitespace)
        ]

        is_block_terminated = False
        adj_line = line_to_parse[start_index:]
        if parser_state.token_stack[-1].html_block_type == HtmlHelper.html_block_1:
            for next_end_tag in HtmlHelper.__html_block_1_end_tags:
                if next_end_tag in adj_line:
                    is_block_terminated = True
        elif parser_state.token_stack[-1].html_block_type == HtmlHelper.html_block_2:
            is_block_terminated = HtmlHelper.__html_block_2_end in adj_line
        elif parser_state.token_stack[-1].html_block_type == HtmlHelper.html_block_3:
            is_block_terminated = HtmlHelper.__html_block_3_end in adj_line
        elif parser_state.token_stack[-1].html_block_type == HtmlHelper.html_block_4:
            is_block_terminated = HtmlHelper.__html_block_4_end in adj_line
        elif parser_state.token_stack[-1].html_block_type == HtmlHelper.html_block_5:
            is_block_terminated = HtmlHelper.__html_block_5_end in adj_line

        if is_block_terminated:
            terminated_block_tokens, _, _ = parser_state.close_open_blocks_fn(
                parser_state, only_these_blocks=[type(parser_state.token_stack[-1])],
            )
            assert terminated_block_tokens
            new_tokens.extend(terminated_block_tokens)
        return new_tokens
