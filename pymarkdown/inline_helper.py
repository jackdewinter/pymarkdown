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
from pymarkdown.markdown_token import (
    EmailAutolinkMarkdownToken,
    HardBreakMarkdownToken,
    InlineCodeSpanMarkdownToken,
    UriAutolinkMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper


# pylint: disable=too-few-public-methods
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
    ):
        self.source_text = source_text
        self.next_index = next_index
        self.inline_blocks = inline_blocks
        self.remaining_line = remaining_line
        self.current_string_unresolved = current_string_unresolved

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
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


# pylint: enable=too-few-public-methods


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
    __line_end_whitespace = " "
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
    def handle_inline_backslash(inline_request):
        """
        Handle the inline case of having a backslash.
        """

        inline_response = InlineResponse()
        inline_response.new_index = inline_request.next_index + 1
        inline_response.new_string = ""
        inline_response.new_string_unresolved = ""
        if inline_response.new_index >= len(inline_request.source_text) or (
            inline_response.new_index < len(inline_request.source_text)
            and inline_request.source_text[inline_response.new_index] == "\n"
        ):
            inline_response.new_string = InlineHelper.backslash_character
            inline_response.new_string_unresolved = inline_response.new_string
        else:
            if (
                inline_request.source_text[inline_response.new_index]
                in InlineHelper.__backslash_punctuation
            ):
                inline_response.new_string = inline_request.source_text[
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

        return inline_response

    @staticmethod
    def handle_character_reference(inline_request):
        """
        Handle a generic character reference.
        """
        logger = logging.getLogger(__name__)

        inline_response = InlineResponse()
        inline_response.new_index = inline_request.next_index + 1
        inline_response.new_string = ""
        if (
            inline_response.new_index < len(inline_request.source_text)
            and inline_request.source_text[inline_response.new_index]
            == InlineHelper.__numeric_character_reference_start_character
        ):
            (
                inline_response.new_string,
                inline_response.new_index,
            ) = InlineHelper.__handle_numeric_character_reference(
                logger, inline_request.source_text, inline_response.new_index
            )
        else:
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
                    if collected_string in InlineHelper.__entity_map:
                        collected_string = InlineHelper.__entity_map[collected_string]
                inline_response.new_string = collected_string
                inline_response.new_index = end_index
            else:
                inline_response.new_string = (
                    InlineHelper.character_reference_start_character
                )
        return inline_response

    @staticmethod
    def handle_backslashes(source_text):
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
            if current_char == InlineHelper.backslash_character:
                inline_response = InlineHelper.handle_inline_backslash(inline_request)
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
            current_string = current_string + new_string
            start_index = new_index
            next_index = ParserHelper.index_any_of(
                source_text, InlineHelper.__valid_backslash_sequence_starts, start_index
            )

        if start_index < len(source_text):
            current_string = current_string + source_text[start_index:]
        return current_string

    @staticmethod
    def append_text(string_to_append_to, text_to_append, alternate_escape_map=None):
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
            string_to_append_to = (
                string_to_append_to
                + text_to_append[start_index:next_index]
                + alternate_escape_map[text_to_append[next_index]]
            )

            start_index = next_index + 1
            next_index = ParserHelper.index_any_of(
                text_to_append, alternate_escape_map.keys(), start_index
            )

        if start_index < len(text_to_append):
            string_to_append_to = string_to_append_to + text_to_append[start_index:]

        return string_to_append_to

    @staticmethod
    def handle_inline_backtick(inline_request):
        """
        Handle the inline case of backticks for code spans.
        """
        logger = logging.getLogger(__name__)

        logger.debug("before_collect>%s", str(inline_request.next_index))
        (
            new_index,
            extracted_start_backticks,
        ) = ParserHelper.collect_while_one_of_characters(
            inline_request.source_text,
            inline_request.next_index,
            InlineHelper.code_span_bounds,
        )
        logger.debug("after_collect>%s>%s", str(new_index), extracted_start_backticks)

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
        if end_backtick_start_index == -1:
            inline_response.new_string = extracted_start_backticks
            inline_response.new_index = new_index
        else:
            between_text = inline_request.source_text[
                new_index:end_backtick_start_index
            ]
            between_text = (
                between_text.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
            )

            logger.debug(
                "after_collect>%s>>%s>>%s<<",
                between_text,
                str(end_backtick_start_index),
                inline_request.source_text[end_backtick_start_index:],
            )
            if (
                len(between_text) > 2
                and between_text[0] == " "
                and between_text[-1] == " "
            ):
                stripped_between_attempt = between_text[1:-1]
                if len(stripped_between_attempt.strip()) != 0:
                    between_text = stripped_between_attempt

            between_text = InlineHelper.append_text("", between_text)
            logger.debug("between_text>>%s<<", between_text)
            end_backtick_start_index += len(extracted_start_backticks)
            inline_response.new_string = ""
            inline_response.new_index = end_backtick_start_index
            inline_response.new_tokens = [InlineCodeSpanMarkdownToken(between_text)]
        return inline_response

    @staticmethod
    def modify_end_string(end_string, removed_end_whitespace):
        """
        Modify the string at the end of the paragraph.
        """
        logger = logging.getLogger(__name__)

        logger.debug(
            ">>removed_end_whitespace>>%s>>%s>>",
            str(type(removed_end_whitespace)),
            removed_end_whitespace,
        )
        logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>NewLine")
        if end_string:
            logger.debug(">>end_string>>%s>>", end_string.replace("\n", "\\n"))
        logger.debug(
            ">>removed_end_whitespace>>%s>>",
            removed_end_whitespace.replace("\n", "\\n"),
        )
        if end_string is None:
            end_string = removed_end_whitespace + "\n"
        else:
            end_string = end_string + removed_end_whitespace + "\n"
        logger.debug(">>end_string>>%s>>", end_string.replace("\n", "\\n"))
        return end_string

    @staticmethod
    def handle_line_end(next_index, remaining_line, end_string, current_string):
        """
        Handle the inline case of having the end of line character encountered.
        """
        logger = logging.getLogger(__name__)

        new_tokens = []

        _, last_non_whitespace_index = ParserHelper.collect_backwards_while_character(
            remaining_line, -1, InlineHelper.__line_end_whitespace
        )
        logger.debug(">>last_non_whitespace_index>>%s", str(last_non_whitespace_index))
        logger.debug(">>current_string>>%s>>", current_string)
        removed_end_whitespace = remaining_line[last_non_whitespace_index:]
        remaining_line = remaining_line[0:last_non_whitespace_index]

        append_to_current_string = "\n"
        whitespace_to_add = None
        logger.debug(
            ">>len(r_e_w)>>%s>>rem>>%s>>",
            str(len(removed_end_whitespace)),
            remaining_line,
        )
        if (
            len(removed_end_whitespace) == 0
            and len(current_string) >= 1
            and current_string[len(current_string) - 1]
            == InlineHelper.backslash_character
        ):
            new_tokens.append(HardBreakMarkdownToken())
            current_string = current_string[0:-1]
        elif len(removed_end_whitespace) >= 2:
            new_tokens.append(HardBreakMarkdownToken())
            whitespace_to_add = removed_end_whitespace
        else:
            end_string = InlineHelper.modify_end_string(
                end_string, removed_end_whitespace
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

    @staticmethod
    def extract_bounded_string(
        source_text, new_index, close_character, start_character
    ):
        """
        Extract a string that is bounded by some manner of characters.
        """
        logger = logging.getLogger(__name__)

        break_characters = InlineHelper.backslash_character + close_character
        if start_character:
            break_characters = break_characters + start_character
        nesting_level = 0
        logger.debug(
            "extract_bounded_string>>new_index>>%s>>data>>%s>>",
            str(new_index),
            source_text[new_index:],
        )
        next_index, data = ParserHelper.collect_until_one_of_characters(
            source_text, new_index, break_characters
        )
        logger.debug(">>next_index1>>%s>>data>>%s>>", str(next_index), data)
        while next_index < len(source_text) and not (
            source_text[next_index] == close_character and nesting_level == 0
        ):
            if ParserHelper.is_character_at_index(
                source_text, next_index, InlineHelper.backslash_character
            ):
                logger.debug("pre-back>>next_index>>%s>>", str(next_index))
                old_index = next_index

                inline_request = InlineRequest(source_text, next_index)
                inline_response = InlineHelper.handle_inline_backslash(inline_request)
                next_index = inline_response.new_index
                data = data + source_text[old_index:next_index]
            elif start_character is not None and ParserHelper.is_character_at_index(
                source_text, next_index, start_character
            ):
                logger.debug("pre-start>>next_index>>%s>>", str(next_index))
                data = data + start_character
                next_index += 1
                nesting_level += 1
            else:
                assert ParserHelper.is_character_at_index(
                    source_text, next_index, close_character
                )
                logger.debug("pre-close>>next_index>>%s>>", str(next_index))
                data = data + close_character
                next_index += 1
                nesting_level -= 1
            next_index, new_data = ParserHelper.collect_until_one_of_characters(
                source_text, next_index, break_characters
            )
            logger.debug("back>>next_index>>%s>>data>>%s>>", str(next_index), data)
            data = data + new_data
        logger.debug(">>next_index2>>%s>>data>>%s>>", str(next_index), data)
        if (
            ParserHelper.is_character_at_index(source_text, next_index, close_character)
            and nesting_level == 0
        ):
            logger.debug("extract_bounded_string>>found-close")
            return next_index + 1, data
        logger.debug(
            "extract_bounded_string>>ran out of string>>next_index>>%s", str(next_index)
        )
        return next_index, None

    @staticmethod
    def __handle_numeric_character_reference(logger, source_text, new_index):
        """
        Handle a character reference that is numeric in nature.
        """

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
            logger.debug(
                "&#x>>a>>"
                + str(end_index)
                + ">>b>>"
                + str(collected_string)
                + ">>"
                + str(len(source_text))
            )
            delta = end_index - new_index
            logger.debug("delta>>" + str(delta) + ">>")
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
            logger.debug(
                "&#>>a>>"
                + str(end_index)
                + ">>b>>"
                + str(collected_string)
                + ">>"
                + str(len(source_text))
            )
            delta = end_index - new_index
            logger.debug("delta>>" + str(delta) + ">>")
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
            if translated_reference == 0:
                new_string = InlineHelper.__invalid_reference_character_substitute
            else:
                new_string = chr(translated_reference)
        return new_string, new_index

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
    def __parse_valid_email_autolink(text_to_parse):
        """
        Parse a possible email autolink and determine if it is valid.
        """
        if re.match(InlineHelper.__valid_email_regex, text_to_parse):
            return EmailAutolinkMarkdownToken(text_to_parse)
        return None

    @staticmethod
    def __parse_valid_uri_autolink(text_to_parse):
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
                return UriAutolinkMarkdownToken(text_to_parse)
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
        if closing_angle_index not in (-1, inline_request.next_index + 1):

            between_brackets = inline_request.source_text[
                inline_request.next_index + 1 : closing_angle_index
            ]
            remaining_line = inline_request.source_text[inline_request.next_index + 1 :]
            closing_angle_index += 1
            new_token = InlineHelper.__parse_valid_uri_autolink(between_brackets)
            if not new_token:
                new_token = InlineHelper.__parse_valid_email_autolink(between_brackets)
            if not new_token:
                new_token, after_index = HtmlHelper.parse_raw_html(
                    between_brackets, remaining_line
                )
                if after_index != -1:
                    closing_angle_index = after_index + inline_request.next_index + 1

        inline_response = InlineResponse()
        if new_token:
            inline_response.new_string = ""
            inline_response.new_index = closing_angle_index
            inline_response.new_tokens = [new_token]
        else:
            inline_response.new_string = InlineHelper.angle_bracket_start
            inline_response.new_index = inline_request.next_index + 1
        return inline_response
