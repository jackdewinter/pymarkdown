"""
Inline helper
"""
import json
import os
import re
import string
import sys

from pymarkdown.html_helper import HtmlHelper
from pymarkdown.markdown_token import (
    EmailAutolinkMarkdownToken,
    HardBreakMarkdownToken,
    InlineCodeSpanMarkdownToken,
    UriAutolinkMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper


class InlineHelper:
    """
    Class to helper with the parsing of inline elements.
    """

    __valid_email_regex = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    __valid_scheme_characters = string.ascii_letters + string.digits + ".-+"
    __backslash_punctuation = "!\"#$%&'()*+,-./:;<=>?@[]^_`{|}~\\"
    __html_character_escape_map = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
        '"': "&quot;",
    }

    __entity_map = {}

    @staticmethod
    def initialize(resource_path):
        """
        Initialize the inline subsystem.
        """
        InlineHelper.__entity_map = InlineHelper.__load_entity_map(resource_path)

    @staticmethod
    def handle_inline_backslash(source_text, next_index):
        """
        Handle the inline case of having a backslash.
        """

        new_index = next_index + 1
        new_string = ""
        new_string_unresolved = ""
        if new_index >= len(source_text) or (
            new_index < len(source_text) and source_text[new_index] == "\n"
        ):
            new_string = "\\"
            new_string_unresolved = new_string
        else:
            if source_text[new_index] in InlineHelper.__backslash_punctuation:
                new_string = source_text[new_index]
                new_string_unresolved = "\\" + new_string
            else:
                new_string = "\\" + source_text[new_index]
                new_string_unresolved = new_string
            new_index = new_index + 1
        return new_string, new_index, new_string_unresolved

    @staticmethod
    def __handle_numeric_character_reference(source_text, new_index):
        """
        Handle a character reference that is numeric in nature.
        """

        new_index = new_index + 1
        translated_reference = -1
        if new_index < len(source_text) and (
            source_text[new_index] == "x" or source_text[new_index] == "X"
        ):
            hex_char = source_text[new_index]
            new_index = new_index + 1
            end_index, collected_string = ParserHelper.collect_while_one_of_characters(
                source_text, new_index, string.hexdigits
            )
            print(
                "&#x>>a>>"
                + str(end_index)
                + ">>b>>"
                + str(collected_string)
                + ">>"
                + str(len(source_text))
            )
            delta = end_index - new_index
            print("delta>>" + str(delta) + ">>")
            if 1 <= delta <= 6:
                translated_reference = int(collected_string, 16)
            new_string = "&#" + hex_char + collected_string
            new_index = end_index
        else:
            end_index, collected_string = ParserHelper.collect_while_one_of_characters(
                source_text, new_index, string.digits
            )
            print(
                "&#>>a>>"
                + str(end_index)
                + ">>b>>"
                + str(collected_string)
                + ">>"
                + str(len(source_text))
            )
            delta = end_index - new_index
            print("delta>>" + str(delta) + ">>")
            if 1 <= delta <= 7:
                translated_reference = int(collected_string)
            new_string = "&#" + collected_string
            new_index = end_index

        if (
            translated_reference >= 0
            and new_index < len(source_text)
            and source_text[new_index] == ";"
        ):
            new_index = new_index + 1
            if translated_reference == 0:
                new_string = "\ufffd"
            else:
                new_string = chr(translated_reference)
        return new_string, new_index

    @staticmethod
    def handle_character_reference(source_text, next_index):
        """
        Handle a generic character reference.
        """

        new_index = next_index + 1
        new_string = ""
        if new_index < len(source_text) and source_text[new_index] == "#":
            new_string, new_index = InlineHelper.__handle_numeric_character_reference(
                source_text, new_index
            )
        else:
            end_index, collected_string = ParserHelper.collect_while_one_of_characters(
                source_text, new_index, string.ascii_letters + string.digits
            )
            if collected_string:
                collected_string = "&" + collected_string
                if end_index < len(source_text) and source_text[end_index] == ";":
                    end_index = end_index + 1
                    collected_string = collected_string + ";"
                    if collected_string in InlineHelper.__entity_map:
                        collected_string = InlineHelper.__entity_map[collected_string]
                new_string = collected_string
                new_index = end_index
            else:
                new_string = "&"
        return new_string, new_index

    @staticmethod
    def __load_entity_map(resource_path):
        """
        Load the entity map, refreshed from https://html.spec.whatwg.org/entities.json
        into a dict that was can use.
        """

        master_entities_file = os.path.join(resource_path, "entities.json")
        try:
            with open(os.path.abspath(master_entities_file), "r") as infile:
                results_dictionary = json.load(infile)
        except json.decoder.JSONDecodeError as ex:
            print(
                "Named character entity map file '"
                + master_entities_file
                + "' is not a valid JSON file ("
                + str(ex)
                + ")."
            )
            sys.exit(1)
        except IOError as ex:
            print(
                "Named character entity map file '"
                + master_entities_file
                + "' was not loaded ("
                + str(ex)
                + ")."
            )
            sys.exit(1)

        approved_entity_map = {}
        for next_name in results_dictionary:

            # Downloaded file is for HTML5, which includes some names that do
            # not end with ";".  These are excluded.
            if not next_name.endswith(";"):
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
    def extract_bounded_string(
        source_text, new_index, close_character, start_character
    ):
        """
        Extract a string that is bounded by some manner of characters.
        """

        break_characters = "\\" + close_character
        if start_character:
            break_characters = break_characters + start_character
        nesting_level = 0
        print(
            "extract_bounded_string>>new_index>>"
            + str(new_index)
            + ">>data>>"
            + source_text[new_index:]
            + ">>"
        )
        next_index, data = ParserHelper.collect_until_one_of_characters(
            source_text, new_index, break_characters
        )
        print(">>next_index1>>" + str(next_index) + ">>data>>" + data + ">>")
        while next_index < len(source_text) and not (
            source_text[next_index] == close_character and nesting_level == 0
        ):
            if ParserHelper.is_character_at_index(source_text, next_index, "\\"):
                print("pre-back>>next_index>>" + str(next_index) + ">>")
                old_index = next_index
                _, next_index, _ = InlineHelper.handle_inline_backslash(
                    source_text, next_index
                )
                data = data + source_text[old_index:next_index]
            elif start_character is not None and ParserHelper.is_character_at_index(
                source_text, next_index, start_character
            ):
                print("pre-start>>next_index>>" + str(next_index) + ">>")
                data = data + start_character
                next_index = next_index + 1
                nesting_level = nesting_level + 1
            else:  # elif ParserHelper.is_character_at_index(
                # source_text, next_index, close_character
                # ):
                print("pre-close>>next_index>>" + str(next_index) + ">>")
                data = data + close_character
                next_index = next_index + 1
                nesting_level = nesting_level - 1
            next_index, new_data = ParserHelper.collect_until_one_of_characters(
                source_text, next_index, break_characters
            )
            print("back>>next_index>>" + str(next_index) + ">>data>>" + data + ">>")
            data = data + new_data
        print(">>next_index2>>" + str(next_index) + ">>data>>" + data + ">>")
        if (
            ParserHelper.is_character_at_index(source_text, next_index, close_character)
            and nesting_level == 0
        ):
            print("extract_bounded_string>>found-close")
            return next_index + 1, data
        # if next_index == len(source_text):
        print(
            "extract_bounded_string>>ran out of string>>next_index>>" + str(next_index)
        )
        return next_index, None

    @staticmethod
    def handle_backslashes(source_text):
        """
        Handle the processing of backslashes for anything other than the text
        blocks, which have additional needs for parsing.
        """

        valid_sequence_starts = "\\&"
        start_index = 0
        current_string = ""
        next_index = ParserHelper.index_any_of(
            source_text, valid_sequence_starts, start_index
        )
        while next_index != -1:
            current_string = current_string + source_text[start_index:next_index]
            current_char = source_text[next_index]
            if current_char == "\\":
                new_string, new_index, _ = InlineHelper.handle_inline_backslash(
                    source_text, next_index
                )
            else:  # if source_text[next_index] == "&":
                new_string, new_index = InlineHelper.handle_character_reference(
                    source_text, next_index
                )
            current_string = current_string + new_string
            start_index = new_index
            next_index = ParserHelper.index_any_of(
                source_text, valid_sequence_starts, start_index
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
    def handle_inline_backtick(source_text, next_index):
        """
        Handle the inline case of backticks for code spans.
        """

        print("before_collect>" + str(next_index))
        (
            new_index,
            extracted_start_backticks,
        ) = ParserHelper.collect_while_one_of_characters(source_text, next_index, "`")
        print("after_collect>" + str(new_index) + ">" + extracted_start_backticks)

        end_backtick_start_index = source_text.find(
            extracted_start_backticks, new_index
        )
        while end_backtick_start_index != -1:
            (
                end_backticks_index,
                end_backticks_attempt,
            ) = ParserHelper.collect_while_one_of_characters(
                source_text, end_backtick_start_index, "`"
            )
            if len(end_backticks_attempt) == len(extracted_start_backticks):
                break
            end_backtick_start_index = source_text.find(
                extracted_start_backticks, end_backticks_index
            )
        if end_backtick_start_index == -1:
            return extracted_start_backticks, new_index, None

        between_text = source_text[new_index:end_backtick_start_index]
        between_text = (
            between_text.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
        )

        print(
            "after_collect>"
            + between_text
            + ">>"
            + str(end_backtick_start_index)
            + ">>"
            + source_text[end_backtick_start_index:]
            + "<<"
        )
        if len(between_text) > 2 and between_text[0] == " " and between_text[-1] == " ":
            stripped_between_attempt = between_text[1:-1]
            if len(stripped_between_attempt.strip()) != 0:
                between_text = stripped_between_attempt

        between_text = InlineHelper.append_text("", between_text)
        print("between_text>>" + between_text + "<<")
        end_backtick_start_index = end_backtick_start_index + len(
            extracted_start_backticks
        )
        return "", end_backtick_start_index, [InlineCodeSpanMarkdownToken(between_text)]

    @staticmethod
    def modify_end_string(end_string, removed_end_whitespace):
        """
        Modify the string at the end of the paragraph.
        """
        print(
            ">>removed_end_whitespace>>"
            + str(type(removed_end_whitespace))
            + ">>"
            + removed_end_whitespace
            + ">>"
        )
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>NewLine")
        if end_string:
            print(">>end_string>>" + end_string.replace("\n", "\\n") + ">>")
        print(
            ">>removed_end_whitespace>>"
            + removed_end_whitespace.replace("\n", "\\n")
            + ">>"
        )
        if end_string is None:
            end_string = removed_end_whitespace + "\n"
        else:
            end_string = end_string + removed_end_whitespace + "\n"
        print(">>end_string>>" + end_string.replace("\n", "\\n") + ">>")
        return end_string

    @staticmethod
    def handle_line_end(next_index, remaining_line, end_string, current_string):
        """
        Handle the inline case of having the end of line character encountered.
        """

        new_tokens = []

        _, last_non_whitespace_index = ParserHelper.collect_backwards_while_character(
            remaining_line, -1, " "
        )
        print(">>last_non_whitespace_index>>" + str(last_non_whitespace_index))
        print(">>current_string>>" + current_string + ">>")
        removed_end_whitespace = remaining_line[last_non_whitespace_index:]
        remaining_line = remaining_line[0:last_non_whitespace_index]

        append_to_current_string = "\n"
        whitespace_to_add = None
        print(
            ">>len(r_e_w)>>"
            + str(len(removed_end_whitespace))
            + ">>rem>>"
            + remaining_line
            + ">>"
        )
        if (
            len(removed_end_whitespace) == 0
            and len(current_string) >= 1
            and current_string[len(current_string) - 1] == "\\"
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
        if "<" not in text_to_parse and text_to_parse[0] in string.ascii_letters:
            path_index, uri_scheme = ParserHelper.collect_while_one_of_characters(
                text_to_parse, 1, InlineHelper.__valid_scheme_characters
            )
            uri_scheme = text_to_parse[0] + uri_scheme
        if (
            len(uri_scheme) >= 2
            and len(uri_scheme) <= 32
            and path_index < len(text_to_parse)
            and text_to_parse[path_index] == ":"
        ):
            path_index = path_index + 1
            while path_index < len(text_to_parse):
                if ord(text_to_parse[path_index]) <= 32:
                    break
                path_index = path_index + 1
            if path_index == len(text_to_parse):
                return UriAutolinkMarkdownToken(text_to_parse)
        return None

    @staticmethod
    def handle_angle_brackets(source_text, next_index):
        """
        Given an open angle bracket, determine which of the three possibilities it is.
        """
        closing_angle_index = source_text.find(">", next_index)
        new_token = None
        if closing_angle_index not in (-1, next_index + 1):

            between_brackets = source_text[next_index + 1 : closing_angle_index]
            remaining_line = source_text[next_index + 1 :]
            closing_angle_index = closing_angle_index + 1
            new_token = InlineHelper.__parse_valid_uri_autolink(between_brackets)
            if not new_token:
                new_token = InlineHelper.__parse_valid_email_autolink(between_brackets)
            if not new_token:
                new_token, after_index = HtmlHelper.parse_raw_html(
                    between_brackets, remaining_line
                )
                if after_index != -1:
                    closing_angle_index = after_index + next_index + 1

        if new_token:
            return "", closing_angle_index, [new_token]
        return "<", next_index + 1, None
