"""
Inline helper
"""
import json
import logging
import os
import re
import string

from pymarkdown.bad_tokenization_error import BadTokenizationError
from pymarkdown.html_helper import HtmlHelper
from pymarkdown.inline_markdown_token import (
    EmailAutolinkMarkdownToken,
    HardBreakMarkdownToken,
    InlineCodeSpanMarkdownToken,
    UriAutolinkMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods, too-many-instance-attributes
class InlineRequest:
    """
    Class to hold the request information to pass on to the handle_* functions.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        source_text,
        next_index,
        inline_blocks=None,
        remaining_line=None,
        current_string_unresolved=None,
        line_number=None,
        column_number=None,
        para_owner=None,
    ):
        self.source_text = source_text
        self.next_index = next_index
        self.inline_blocks = inline_blocks
        self.remaining_line = remaining_line
        self.current_string_unresolved = current_string_unresolved
        self.line_number = line_number
        self.column_number = column_number
        self.para_owner = para_owner

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods, too-many-instance-attributes


# pylint: disable=too-few-public-methods,too-many-arguments,too-many-instance-attributes
class InlineResponse:
    """
    Class to hold the response from the inline handle_* functions.
    """

    def __init__(self):
        self.new_string = None
        self.new_index = None
        self.new_tokens = None
        self.new_string_unresolved = None
        self.consume_rest_of_line = False
        self.original_string = None
        self.delta_line_number = 0
        self.delta_column_number = 0
        self.clear_fields()

    def clear_fields(self):
        """
        Clear any of the fields that start with new_*.
        """
        self.new_string = None
        self.new_index = None
        self.new_tokens = None
        self.new_string_unresolved = None
        self.consume_rest_of_line = False
        self.original_string = None
        self.delta_line_number = 0
        self.delta_column_number = 0


# pylint: enable=too-few-public-methods,too-many-arguments,too-many-instance-attributes


class InlineHelper:
    """
    Class to helper with the parsing of inline elements.
    """

    __valid_email_regex = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

    __scheme_end_character = ":"
    __valid_scheme_characters = string.ascii_letters + string.digits + ".-+"

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
    __entity_map = {}
    character_reference_start_character = "&"
    __numeric_character_reference_start_character = "#"
    __hex_character_reference_start_character = "xX"
    __character_reference_end_character = ";"
    __invalid_reference_character_substitute = "\ufffd"
    __line_end_whitespace = ParserHelper.space_character
    __valid_backslash_sequence_starts = (
        backslash_character + character_reference_start_character
    )

    __skip_html5_entities_ending_with = ";"

    __entities_file_name = "entities.json"

    @staticmethod
    def initialize(resource_path):
        """
        Initialize the inline subsystem.
        """
        InlineHelper.__entity_map = InlineHelper.__load_entity_map(resource_path)

    @staticmethod
    def handle_inline_backslash(inline_request, add_text_signature=True):
        """
        Handle the inline case of having a backslash.
        """

        inline_response = InlineResponse()
        inline_response.new_index = inline_request.next_index + 1
        inline_response.new_string = ""
        inline_response.new_string_unresolved = ""
        if inline_response.new_index >= len(inline_request.source_text) or (
            inline_response.new_index < len(inline_request.source_text)
            and inline_request.source_text[inline_response.new_index]
            == ParserHelper.newline_character
        ):
            inline_response.new_string = InlineHelper.backslash_character
            inline_response.new_string_unresolved = inline_response.new_string
        else:
            if (
                inline_request.source_text[inline_response.new_index]
                in InlineHelper.__backslash_punctuation
            ):
                inline_response.new_string = ""
                if add_text_signature:
                    inline_response.new_string += ParserHelper.backslash_escape_sequence
                inline_response.new_string += inline_request.source_text[
                    inline_response.new_index
                ]
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

        inline_response.delta_line_number = 0
        inline_response.delta_column_number = (
            inline_response.new_index - inline_request.next_index
        )
        return inline_response

    @staticmethod
    def handle_character_reference(inline_request):
        """
        Handle a generic character reference.
        """
        inline_response = InlineResponse()
        inline_response.new_index = inline_request.next_index + 1
        inline_response.new_string = ""
        if (
            inline_response.new_index < len(inline_request.source_text)
            and inline_request.source_text[inline_response.new_index]
            == InlineHelper.__numeric_character_reference_start_character
        ):
            original_new_index = inline_response.new_index
            LOGGER.debug("here")
            (
                inline_response.new_string,
                inline_response.new_index,
                inline_response.original_string,
            ) = InlineHelper.__handle_numeric_character_reference(
                inline_request.source_text, inline_response.new_index
            )
            inline_response.new_string_unresolved = (
                InlineHelper.character_reference_start_character
                + inline_request.source_text[
                    original_new_index : inline_response.new_index
                ]
            )
            LOGGER.debug("here-->%s<--", inline_response.new_string)
            LOGGER.debug("here-->%s<--", inline_response.new_string_unresolved)
        else:
            LOGGER.debug("there")
            end_index, collected_string = ParserHelper.collect_while_one_of_characters(
                inline_request.source_text,
                inline_response.new_index,
                string.ascii_letters + string.digits,
            )
            if collected_string:
                collected_string = (
                    InlineHelper.character_reference_start_character + collected_string
                )
                if (
                    end_index < len(inline_request.source_text)
                    and inline_request.source_text[end_index]
                    == InlineHelper.__character_reference_end_character
                ):
                    end_index += 1
                    collected_string += InlineHelper.__character_reference_end_character
                    original_collected_string = collected_string
                    if collected_string in InlineHelper.__entity_map:
                        inline_response.original_string = collected_string
                        collected_string = InlineHelper.__entity_map[collected_string]
                        inline_response.new_string_unresolved = (
                            original_collected_string
                        )
                inline_response.new_string = collected_string
                inline_response.new_index = end_index
                LOGGER.debug("there-->%s<--", inline_response.new_string)
                LOGGER.debug("there-->%s<--", inline_response.new_string_unresolved)
            else:
                inline_response.new_string = (
                    InlineHelper.character_reference_start_character
                )
        inline_response.delta_line_number = 0
        inline_response.delta_column_number = (
            inline_response.new_index - inline_request.next_index
        )
        return inline_response

    @staticmethod
    def handle_backslashes(source_text, add_text_signature=True):
        """
        Handle the processing of backslashes for anything other than the text
        blocks, which have additional needs for parsing.
        """

        start_index = 0
        current_string = ""
        next_index = ParserHelper.index_any_of(
            source_text, InlineHelper.__valid_backslash_sequence_starts, start_index
        )
        while next_index != -1:
            current_string = current_string + source_text[start_index:next_index]
            current_char = source_text[next_index]

            inline_request = InlineRequest(source_text, next_index)
            LOGGER.debug("handle_backslashes>>%s>>", current_char)
            if current_char == InlineHelper.backslash_character:
                inline_response = InlineHelper.handle_inline_backslash(
                    inline_request, add_text_signature=add_text_signature
                )
                new_string = inline_response.new_string
                new_index = inline_response.new_index
            else:
                assert (
                    source_text[next_index]
                    == InlineHelper.character_reference_start_character
                )
                inline_response = InlineHelper.handle_character_reference(
                    inline_request
                )
                new_string = inline_response.new_string
                new_index = inline_response.new_index

            LOGGER.debug("handle_backslashes<<%s<<%s", new_string, str(new_index))
            current_string = current_string + new_string
            start_index = new_index
            next_index = ParserHelper.index_any_of(
                source_text, InlineHelper.__valid_backslash_sequence_starts, start_index
            )

        if start_index < len(source_text):
            current_string = current_string + source_text[start_index:]
        return current_string

    @staticmethod
    def append_text(
        string_to_append_to,
        text_to_append,
        alternate_escape_map=None,
        add_text_signature=True,
    ):
        """
        Append the text to the given string, doing any needed encoding as we go.
        """

        if not alternate_escape_map:
            alternate_escape_map = InlineHelper.__html_character_escape_map

        start_index = 0
        next_index = ParserHelper.index_any_of(
            text_to_append, alternate_escape_map.keys(), start_index
        )
        while next_index != -1:

            string_part = text_to_append[start_index:next_index]
            escaped_part = alternate_escape_map[text_to_append[next_index]]
            if add_text_signature:
                string_part += ParserHelper.create_replacement_markers(
                    text_to_append[next_index], escaped_part
                )
            else:
                string_part += escaped_part

            string_to_append_to += string_part

            start_index = next_index + 1
            next_index = ParserHelper.index_any_of(
                text_to_append, alternate_escape_map.keys(), start_index
            )

        if start_index < len(text_to_append):
            string_to_append_to = string_to_append_to + text_to_append[start_index:]

        return string_to_append_to

    # pylint: disable=too-many-statements, too-many-locals
    @staticmethod
    def handle_inline_backtick(inline_request):
        """
        Handle the inline case of backticks for code spans.
        """
        LOGGER.debug("before_collect>%s", str(inline_request.next_index))
        (
            new_index,
            extracted_start_backticks,
        ) = ParserHelper.collect_while_one_of_characters(
            inline_request.source_text,
            inline_request.next_index,
            InlineHelper.code_span_bounds,
        )
        LOGGER.debug("after_collect>%s>%s", str(new_index), extracted_start_backticks)

        end_backtick_start_index = inline_request.source_text.find(
            extracted_start_backticks, new_index
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
            if len(end_backticks_attempt) == len(extracted_start_backticks):
                break
            end_backtick_start_index = inline_request.source_text.find(
                extracted_start_backticks, end_backticks_index
            )

        inline_response = InlineResponse()
        inline_response.delta_line_number = -1

        if end_backtick_start_index == -1:
            inline_response.new_string = extracted_start_backticks
            inline_response.new_index = new_index
        else:
            between_text = inline_request.source_text[
                new_index:end_backtick_start_index
            ]
            original_between_text = between_text
            LOGGER.debug(
                "after_collect>%s>>%s>>%s<<",
                ParserHelper.make_value_visible(between_text),
                str(end_backtick_start_index),
                inline_request.source_text[end_backtick_start_index:],
            )
            leading_whitespace = ""
            trailing_whitespace = ""
            if (
                len(between_text) > 2
                and (
                    between_text[0] == ParserHelper.space_character
                    or between_text[0] == ParserHelper.newline_character
                )
                and (
                    between_text[-1] == ParserHelper.space_character
                    or between_text[-1] == ParserHelper.newline_character
                )
            ):
                stripped_between_attempt = between_text[1:-1]
                if len(stripped_between_attempt.strip()) != 0:
                    leading_whitespace = between_text[0]
                    trailing_whitespace = between_text[-1]
                    between_text = stripped_between_attempt

            replaced_newline = ParserHelper.create_replacement_markers(
                ParserHelper.newline_character, ParserHelper.space_character
            )
            LOGGER.debug(
                "between_text>>%s<<", ParserHelper.make_value_visible(between_text)
            )
            between_text = ParserHelper.escape_special_characters(between_text)
            LOGGER.debug(
                "between_text>>%s<<", ParserHelper.make_value_visible(between_text)
            )
            LOGGER.debug(
                "leading_whitespace>>%s<<",
                ParserHelper.make_value_visible(leading_whitespace),
            )
            LOGGER.debug(
                "trailing_whitespace>>%s<<",
                ParserHelper.make_value_visible(trailing_whitespace),
            )
            between_text = between_text.replace(
                ParserHelper.newline_character, replaced_newline
            )
            leading_whitespace = leading_whitespace.replace(
                ParserHelper.newline_character, replaced_newline
            )
            trailing_whitespace = trailing_whitespace.replace(
                ParserHelper.newline_character, replaced_newline
            )

            LOGGER.debug(
                "between_text>>%s<<", ParserHelper.make_value_visible(between_text)
            )
            between_text = InlineHelper.append_text("", between_text)
            LOGGER.debug(
                "between_text>>%s<<", ParserHelper.make_value_visible(between_text)
            )
            LOGGER.debug(
                "leading_whitespace>>%s<<",
                ParserHelper.make_value_visible(leading_whitespace),
            )
            LOGGER.debug(
                "trailing_whitespace>>%s<<",
                ParserHelper.make_value_visible(trailing_whitespace),
            )
            end_backtick_start_index += len(extracted_start_backticks)
            inline_response.new_string = ""
            inline_response.new_index = end_backtick_start_index

            new_column_number = inline_request.column_number
            LOGGER.debug(">>new_column_number>>%s", str(new_column_number))
            new_column_number += len(inline_request.remaining_line)
            LOGGER.debug(">>new_column_number>>%s", str(new_column_number))

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
                    original_between_text + extracted_start_backticks
                )

        LOGGER.debug(
            ">>delta_line_number>>%s<<",
            str(inline_response.delta_line_number),
        )
        LOGGER.debug(
            ">>delta_column_number>>%s<<",
            str(inline_response.delta_column_number),
        )
        if inline_response.delta_line_number == -1:
            inline_response.delta_line_number = 0
            inline_response.delta_column_number = (
                inline_response.new_index - inline_request.next_index
            )
        return inline_response

    # pylint: enable=too-many-statements, too-many-locals

    @staticmethod
    def modify_end_string(end_string, removed_end_whitespace):
        """
        Modify the string at the end of the paragraph.
        """
        LOGGER.debug(
            ">>removed_end_whitespace>>%s>>%s>>",
            str(type(removed_end_whitespace)),
            removed_end_whitespace,
        )
        LOGGER.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>NewLine")
        if end_string:
            LOGGER.debug(
                ">>end_string>>%s>>", ParserHelper.make_value_visible(end_string)
            )
        LOGGER.debug(
            ">>removed_end_whitespace>>%s>>",
            ParserHelper.make_value_visible(removed_end_whitespace),
        )
        if end_string is None:
            end_string = removed_end_whitespace + ParserHelper.newline_character
        else:
            end_string = (
                end_string + removed_end_whitespace + ParserHelper.newline_character
            )
        LOGGER.debug(">>end_string>>%s>>", ParserHelper.make_value_visible(end_string))
        return end_string

    # pylint: disable=too-many-arguments
    @staticmethod
    def handle_line_end(
        next_index,
        remaining_line,
        end_string,
        current_string,
        line_number,
        column_number,
    ):
        """
        Handle the inline case of having the end of line character encountered.
        """
        new_tokens = []

        LOGGER.debug(
            ">>current_string>>%s>>", ParserHelper.make_value_visible(current_string)
        )
        LOGGER.debug(">>end_string>>%s>>", ParserHelper.make_value_visible(end_string))
        LOGGER.debug(
            ">>remaining_line>>%s>>", ParserHelper.make_value_visible(remaining_line)
        )
        _, last_non_whitespace_index = ParserHelper.collect_backwards_while_character(
            remaining_line, -1, InlineHelper.__line_end_whitespace
        )
        LOGGER.debug(">>last_non_whitespace_index>>%s", str(last_non_whitespace_index))
        removed_end_whitespace = remaining_line[last_non_whitespace_index:]
        remaining_line = remaining_line[0:last_non_whitespace_index]
        LOGGER.debug(
            ">>removed_end_whitespace>>%s>>",
            ParserHelper.make_value_visible(removed_end_whitespace),
        )
        LOGGER.debug(
            ">>remaining_line>>%s>>", ParserHelper.make_value_visible(remaining_line)
        )

        LOGGER.debug(
            ">>current_string>>%s>>", ParserHelper.make_value_visible(current_string)
        )
        append_to_current_string = ParserHelper.newline_character
        whitespace_to_add = None
        LOGGER.debug(
            ">>len(r_e_w)>>%s>>rem>>%s>>",
            str(len(removed_end_whitespace)),
            remaining_line,
        )

        adj_hard_column = column_number + len(remaining_line)

        LOGGER.debug(
            ">>current_string>>%s>>", ParserHelper.make_value_visible(current_string)
        )

        is_proper_hard_break = False
        if (
            len(removed_end_whitespace) == 0
            and len(current_string) >= 1
            and current_string[len(current_string) - 1]
            == InlineHelper.backslash_character
        ):
            LOGGER.debug(">>%s<<", ParserHelper.make_value_visible(current_string))
            modified_current_string = current_string[0:-1]
            is_proper_hard_break = modified_current_string[-2:] != "\\\b"
            LOGGER.debug(
                ">>%s<<", ParserHelper.make_value_visible(is_proper_hard_break)
            )

        if is_proper_hard_break:
            new_tokens.append(
                HardBreakMarkdownToken(
                    InlineHelper.backslash_character, line_number, adj_hard_column - 1
                )
            )
            current_string = current_string[0:-1]
            whitespace_to_add = ""
        elif len(removed_end_whitespace) >= 2:
            new_tokens.append(
                HardBreakMarkdownToken(
                    removed_end_whitespace, line_number, adj_hard_column
                )
            )
            whitespace_to_add = ""
        else:
            end_string = InlineHelper.modify_end_string(
                end_string, removed_end_whitespace
            )

        LOGGER.debug(
            "<<append_to_current_string<<%s<<",
            ParserHelper.make_value_visible(append_to_current_string),
        )
        LOGGER.debug(
            "<<whitespace_to_add<<%s<<",
            ParserHelper.make_value_visible(whitespace_to_add),
        )
        LOGGER.debug(
            "<<remaining_line<<%s<<", ParserHelper.make_value_visible(remaining_line)
        )
        LOGGER.debug("<<end_string<<%s<<", ParserHelper.make_value_visible(end_string))
        LOGGER.debug(
            "<<current_string<<%s<<", ParserHelper.make_value_visible(current_string)
        )
        return (
            append_to_current_string,
            whitespace_to_add,
            next_index + 1,
            new_tokens,
            remaining_line,
            end_string,
            current_string,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def extract_bounded_string(
        source_text, new_index, close_character, start_character
    ):
        """
        Extract a string that is bounded by some manner of characters.
        """
        break_characters = InlineHelper.backslash_character + close_character
        if start_character:
            break_characters = break_characters + start_character
        nesting_level = 0
        LOGGER.debug(
            "extract_bounded_string>>new_index>>%s>>data>>%s>>",
            str(new_index),
            ParserHelper.make_value_visible(source_text[new_index:]),
        )
        next_index, data = ParserHelper.collect_until_one_of_characters(
            source_text, new_index, break_characters
        )
        LOGGER.debug(
            ">>next_index1>>%s>>data>>%s>>",
            str(next_index),
            ParserHelper.make_value_visible(data),
        )
        while next_index < len(source_text) and not (
            source_text[next_index] == close_character and nesting_level == 0
        ):
            if ParserHelper.is_character_at_index(
                source_text, next_index, InlineHelper.backslash_character
            ):
                LOGGER.debug("pre-back>>next_index>>%s>>", str(next_index))
                old_index = next_index

                inline_request = InlineRequest(source_text, next_index)
                inline_response = InlineHelper.handle_inline_backslash(inline_request)
                next_index = inline_response.new_index
                data = data + source_text[old_index:next_index]
            elif start_character is not None and ParserHelper.is_character_at_index(
                source_text, next_index, start_character
            ):
                LOGGER.debug("pre-start>>next_index>>%s>>", str(next_index))
                data = data + start_character
                next_index += 1
                nesting_level += 1
            else:
                assert ParserHelper.is_character_at_index(
                    source_text, next_index, close_character
                )
                LOGGER.debug("pre-close>>next_index>>%s>>", str(next_index))
                data = data + close_character
                next_index += 1
                nesting_level -= 1
            next_index, new_data = ParserHelper.collect_until_one_of_characters(
                source_text, next_index, break_characters
            )
            LOGGER.debug(
                "back>>next_index>>%s>>data>>%s>>",
                str(next_index),
                ParserHelper.make_value_visible(data),
            )
            data = data + new_data
        LOGGER.debug(
            ">>next_index2>>%s>>data>>%s>>",
            str(next_index),
            ParserHelper.make_value_visible(data),
        )
        if (
            ParserHelper.is_character_at_index(source_text, next_index, close_character)
            and nesting_level == 0
        ):
            LOGGER.debug("extract_bounded_string>>found-close")
            return next_index + 1, data
        LOGGER.debug(
            "extract_bounded_string>>ran out of string>>next_index>>%s", str(next_index)
        )
        return next_index, None

    @staticmethod
    def __handle_numeric_character_reference(source_text, new_index):
        """
        Handle a character reference that is numeric in nature.
        """

        original_reference = None
        new_index += 1
        translated_reference = -1
        if new_index < len(source_text) and (
            source_text[new_index]
            in InlineHelper.__hex_character_reference_start_character
        ):
            hex_char = source_text[new_index]
            new_index += 1
            end_index, collected_string = ParserHelper.collect_while_one_of_characters(
                source_text, new_index, string.hexdigits
            )
            LOGGER.debug(
                "&#x>>a>>%s>>b>>%s>>%s",
                str(end_index),
                str(collected_string),
                str(len(source_text)),
            )
            delta = end_index - new_index
            LOGGER.debug("delta>>%s>>", str(delta))
            if 1 <= delta <= 6:
                translated_reference = int(collected_string, 16)
            new_string = (
                InlineHelper.character_reference_start_character
                + InlineHelper.__numeric_character_reference_start_character
                + hex_char
                + collected_string
            )
            new_index = end_index
        else:
            end_index, collected_string = ParserHelper.collect_while_one_of_characters(
                source_text, new_index, string.digits
            )
            LOGGER.debug(
                "&#>>a>>%s>>b>>%s>>%s",
                str(end_index),
                str(collected_string),
                str(len(source_text)),
            )
            delta = end_index - new_index
            LOGGER.debug("delta>>%s>>", str(delta))
            if 1 <= delta <= 7:
                translated_reference = int(collected_string)
            new_string = (
                InlineHelper.character_reference_start_character
                + InlineHelper.__numeric_character_reference_start_character
                + collected_string
            )
            new_index = end_index

        if (
            translated_reference >= 0
            and new_index < len(source_text)
            and source_text[new_index]
            == InlineHelper.__character_reference_end_character
        ):
            new_index += 1
            original_reference = new_string + ";"
            if translated_reference == 0:
                new_string = InlineHelper.__invalid_reference_character_substitute
            else:
                new_string = chr(translated_reference)
        return new_string, new_index, original_reference

    @staticmethod
    def __load_entity_map(resource_path):
        """
        Load the entity map, refreshed from https://html.spec.whatwg.org/entities.json
        into a dict that was can use.
        """

        master_entities_file = os.path.join(
            resource_path, InlineHelper.__entities_file_name
        )
        try:
            with open(os.path.abspath(master_entities_file)) as infile:
                results_dictionary = json.load(infile)
        except json.decoder.JSONDecodeError as this_exception:
            error_message = (
                "Named character entity map file '"
                + master_entities_file
                + "' is not a valid JSON file ("
                + str(this_exception)
                + ")."
            )
            raise BadTokenizationError(error_message) from this_exception
        except IOError as this_exception:
            error_message = (
                "Named character entity map file '"
                + master_entities_file
                + "' was not loaded ("
                + str(this_exception)
                + ")."
            )
            raise BadTokenizationError(error_message) from this_exception

        approved_entity_map = {}
        for next_name in results_dictionary:

            # Downloaded file is for HTML5, which includes some names that do
            # not end with ";".  These are excluded.
            if not next_name.endswith(InlineHelper.__skip_html5_entities_ending_with):
                continue

            char_entity = results_dictionary[next_name]
            entity_characters = char_entity["characters"]
            entity_codepoints = char_entity["codepoints"]

            # The only entities we should encounter either have a length of 1 or 2
            if len(entity_characters) == 1:
                assert len(entity_codepoints) == 1
                assert ord(entity_characters[0]) == entity_codepoints[0]
            else:
                assert len(entity_codepoints) == 2
                assert ord(entity_characters[0]) == entity_codepoints[0]
                assert ord(entity_characters[1]) == entity_codepoints[1]
            approved_entity_map[next_name] = entity_characters
        return approved_entity_map

    @staticmethod
    def __parse_valid_email_autolink(text_to_parse, line_number, column_number):
        """
        Parse a possible email autolink and determine if it is valid.
        """
        if re.match(InlineHelper.__valid_email_regex, text_to_parse):
            return EmailAutolinkMarkdownToken(text_to_parse, line_number, column_number)
        return None

    @staticmethod
    def __parse_valid_uri_autolink(text_to_parse, line_number, column_number):
        """
        Parse a possible uri autolink and determine if it is valid.
        """

        uri_scheme = ""
        path_index = -1
        if (
            InlineHelper.angle_bracket_start not in text_to_parse
            and text_to_parse[0] in string.ascii_letters
        ):
            path_index, uri_scheme = ParserHelper.collect_while_one_of_characters(
                text_to_parse, 1, InlineHelper.__valid_scheme_characters
            )
            uri_scheme = text_to_parse[0] + uri_scheme

        if (
            2 <= len(uri_scheme) <= 32
            and path_index < len(text_to_parse)
            and text_to_parse[path_index] == InlineHelper.__scheme_end_character
        ):
            path_index += 1
            while path_index < len(text_to_parse):
                if ord(text_to_parse[path_index]) <= 32:
                    break
                path_index += 1
            if path_index == len(text_to_parse):
                return UriAutolinkMarkdownToken(
                    text_to_parse, line_number, column_number
                )
        return None

    @staticmethod
    def handle_angle_brackets(inline_request):
        """
        Given an open angle bracket, determine which of the three possibilities it is.
        """
        closing_angle_index = inline_request.source_text.find(
            InlineHelper.__angle_bracket_end, inline_request.next_index
        )
        new_token = None
        between_brackets = None
        if closing_angle_index not in (-1, inline_request.next_index + 1):

            between_brackets = inline_request.source_text[
                inline_request.next_index + 1 : closing_angle_index
            ]
            remaining_line = inline_request.source_text[inline_request.next_index + 1 :]
            closing_angle_index += 1

            new_column_number = inline_request.column_number
            new_column_number += len(inline_request.remaining_line)

            new_token = InlineHelper.__parse_valid_uri_autolink(
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
                    between_brackets = new_token.raw_tag

        inline_response = InlineResponse()
        if new_token:
            inline_response.new_string = ""
            inline_response.new_index = closing_angle_index
            inline_response.new_tokens = [new_token]
            between_brackets = (
                InlineHelper.angle_bracket_start
                + between_brackets
                + InlineHelper.__angle_bracket_end
            )
        else:
            inline_response.new_string = InlineHelper.angle_bracket_start
            inline_response.new_index = inline_request.next_index + 1
            between_brackets = InlineHelper.angle_bracket_start

        (
            inline_response.delta_line_number,
            inline_response.delta_column_number,
        ) = ParserHelper.calculate_deltas(between_brackets)
        return inline_response
