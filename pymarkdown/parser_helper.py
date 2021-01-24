"""
Module to provide helper functions for parsing.
"""
import logging

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-many-public-methods
class ParserHelper:
    """
    Class to provide helper functions for parsing.
    """

    __backspace_character = "\b"
    __alert_character = "\a"
    whitespace_split_character = "\x02"
    replace_noop_character = "\x03"
    blech_character = "\x04"
    escape_character = "\x05"

    backslash_character = "\\"
    newline_character = "\n"
    tab_character = "\t"
    space_character = " "

    backslash_escape_sequence = backslash_character + __backspace_character

    @staticmethod
    def is_character_at_index(source_string, index_in_string, valid_character):
        """
        Determine if the specified character is at a valid location and is the
        specified valid character.
        """

        return (
            0 <= index_in_string < len(source_string)
            and source_string[index_in_string] == valid_character
        )

    @staticmethod
    def are_characters_at_index(source_string, index_in_string, string_to_match):
        """
        Determine if the specified character is at a valid location and is the
        specified valid character.
        """

        return (
            index_in_string >= 0
            and index_in_string + len(string_to_match) <= len(source_string)
            and source_string[index_in_string : index_in_string + len(string_to_match)]
            == string_to_match
        )

    @staticmethod
    def is_character_at_index_not(source_string, index_in_string, valid_character):
        """
        Determine if the specified character is at a valid location and is
        not the specified valid character.
        """

        return (
            0 <= index_in_string < len(source_string)
            and source_string[index_in_string] != valid_character
        )

    @staticmethod
    def is_character_at_index_whitespace(source_string, index_in_string):
        """
        Determine if the specified character is valid and a whitespace character.
        """

        return 0 <= index_in_string < len(source_string) and (
            source_string[index_in_string] == " "
            or source_string[index_in_string] == ParserHelper.tab_character
        )

    @staticmethod
    def is_character_at_index_one_of(source_string, index_in_string, valid_characters):
        """
        Determine if the specified character is at a valid location and is one
        of the specified valid characters.
        """

        return (
            0 <= index_in_string < len(source_string)
            and source_string[index_in_string] in valid_characters
        )

    @staticmethod
    def is_character_at_index_not_one_of(
        source_string, index_in_string, valid_characters
    ):
        """
        Determine if the specified character is at a valid location and is not one
        of the specified valid characters.
        """

        return (
            0 <= index_in_string < len(source_string)
            and source_string[index_in_string] not in valid_characters
        )

    @staticmethod
    def is_character_at_index_not_whitespace(source_string, index_in_string):
        """
        Determine if the specified character is valid and not a whitespace character.
        """

        return (
            0 <= index_in_string < len(source_string)
            and source_string[index_in_string] != " "
        )

    @staticmethod
    def extract_whitespace(source_string, start_index):
        """
        From the start_index, continue extracting whitespace while we have it.

        Returns the index of the first non-whitespace character and any extracted
        whitespace in a tuple.
        """

        if not 0 <= start_index <= len(source_string):
            return None, None

        index = start_index
        while ParserHelper.is_character_at_index_whitespace(source_string, index):
            index += 1

        return index, source_string[start_index:index]

    @staticmethod
    def extract_any_whitespace(source_string, start_index):
        """
        From the start_index, continue extracting whitespace while we have it.

        Returns the index of the first non-whitespace character and any extracted
        whitespace in a tuple.
        """

        if not 0 <= start_index <= len(source_string):
            return None, None

        index = start_index
        while ParserHelper.is_character_at_index_one_of(
            source_string, index, " \x09\x0a\x0b\x0c\x0d"
        ):
            index += 1

        return index, source_string[start_index:index]

    @staticmethod
    def extract_whitespace_from_end(source_string, start_index=None):
        """
        From the end of the string, continue extracting whitespace while we have it.

        Returns the index of the last non-whitespace character and any extracted whitespace
        in a tuple.
        """
        if not source_string:
            return 0, ""

        if start_index is not None:
            index = start_index - 1
        else:
            index = len(source_string) - 1
        while ParserHelper.is_character_at_index_whitespace(source_string, index):
            index -= 1

        if start_index is not None:
            return index + 1, source_string[index + 1 : start_index]
        return index + 1, source_string[index + 1 :]

    @staticmethod
    def extract_until_whitespace(source_string, start_index):
        """
        From the start_index, continue extracting until we hit whitespace.

        Returns the index of the first whitespace character and any extracted text
        in a tuple.
        """

        if not 0 <= start_index <= len(source_string):
            return None, None

        index = start_index
        while ParserHelper.is_character_at_index_not_whitespace(source_string, index):
            index += 1

        return index, source_string[start_index:index]

    @staticmethod
    def collect_while_character(source_string, start_index, match_character):
        """
        Collect a sequence of the same character from a given starting point in a string.

        Returns the number of characters collected and the index of the first non-matching
        character and any extracted text in a tuple.
        """

        if not 0 <= start_index <= len(source_string):
            return None, None

        index = start_index
        while index < len(source_string) and source_string[index] == match_character:
            index += 1
        return index - start_index, index

    @staticmethod
    def collect_backwards_while_character(source_string, end_index, match_character):
        """
        Collect a sequence of the same character from a given starting point in a string going backwards towards the start of the string.

        Returns the number of characters collected and the index of the first non-matching
        character and any extracted text in a tuple.
        """

        if not -1 <= end_index <= len(source_string):
            return None, None
        if end_index == -1:
            end_index = len(source_string)

        index = end_index
        while index >= 1 and source_string[index - 1] == match_character:
            index -= 1
        return end_index - index, index

    @staticmethod
    def collect_backwards_while_one_of_characters(
        source_string, end_index, match_characters
    ):
        """
        Collect a sequence of the same character from a given starting point in a string going backwards towards the start of the string.

        Returns the number of characters collected and the index of the first non-matching
        character and any extracted text in a tuple.
        """

        if not -1 <= end_index <= len(source_string):
            return None, None
        if end_index == -1:
            end_index = len(source_string)

        index = end_index
        while index >= 1 and source_string[index - 1] in match_characters:
            index -= 1
        return end_index - index, index

    @staticmethod
    def collect_until_character(source_string, start_index, match_character):
        """
        Collect a sequence of characters from a given starting point in a string until we hit a given character.

        Returns the index of the first non-matching character and any extracted text
        in a tuple.
        """

        if not 0 <= start_index <= len(source_string):
            return None, None

        index = start_index
        while index < len(source_string) and source_string[index] != match_character:
            index += 1

        return index, source_string[start_index:index]

    @staticmethod
    def collect_while_one_of_characters(source_string, start_index, match_characters):
        """
        Collect a sequence of characters from a given starting point in a string as long as the character is one of the match characters.

        Returns the index of the first non-matching character and any extracted text
        in a tuple.
        """

        if not 0 <= start_index <= len(source_string):
            return None, None

        index = start_index
        while index < len(source_string) and source_string[index] in match_characters:
            index += 1

        return index, source_string[start_index:index]

    @staticmethod
    def collect_until_one_of_characters(source_string, start_index, match_characters):
        """
        Collect a sequence of characters from a given starting point in a string until we hit one of a given set of characters.

        Returns the index of the first non-matching character and any extracted text
        in a tuple.
        """

        if not 0 <= start_index <= len(source_string):
            return None, None

        index = start_index
        while (
            index < len(source_string) and source_string[index] not in match_characters
        ):
            index += 1

        return index, source_string[start_index:index]

    @staticmethod
    def calculate_length(source_string, start_index=0):
        """
        Calculate an adjusted length for the string.
        """

        string_length = start_index
        for source_character in source_string:
            if source_character == ParserHelper.tab_character:
                string_length = int((string_length + 4) / 4) * 4
            else:
                string_length += 1
        return string_length - start_index

    @staticmethod
    def is_length_less_than_or_equal_to(source_string, length_limit):
        """
        Determine if the adjusted length of the string is less than or equal to the
        specified limit.
        """
        return ParserHelper.calculate_length(source_string) <= length_limit

    @staticmethod
    def is_length_greater_than_or_equal_to(source_string, length_limit, start_index=0):
        """
        Determine if the adjusted length of the string is greater than or equal to the
        specified limit.
        """
        return (
            ParserHelper.calculate_length(source_string, start_index=start_index)
            >= length_limit
        )

    @staticmethod
    def index_any_of(source_text, find_any, start_index=0):
        """
        Determine if any of the specified characters are in the source string.
        """

        while start_index < len(source_text):
            if source_text[start_index] in find_any:
                return start_index
            start_index += 1
        return -1

    @staticmethod
    def replace_any_of(string_to_search_in, characters_to_search_for, replace_with):
        """
        Replace any of a given set of characters with a given sequence.
        """

        rebuilt_string = ""
        start_index = 0
        index, ex_str = ParserHelper.collect_until_one_of_characters(
            string_to_search_in, start_index, characters_to_search_for
        )
        while index < len(string_to_search_in):
            rebuilt_string = rebuilt_string + ex_str + replace_with
            start_index = index + 1
            index, ex_str = ParserHelper.collect_until_one_of_characters(
                string_to_search_in, start_index, characters_to_search_for
            )
        rebuilt_string = rebuilt_string + ex_str
        return rebuilt_string

    @staticmethod
    def count_characters_in_text(text_to_examine, text_to_look_for):
        """
        Count the number of a given character in a given string.
        """
        original_length = len(text_to_examine)
        removed_length = len(text_to_examine.replace(text_to_look_for, ""))
        return original_length - removed_length

    @staticmethod
    def count_newlines_in_text(text_to_examine):
        """
        Count the number of new line characters in a given string.
        """
        return ParserHelper.count_characters_in_text(
            text_to_examine, ParserHelper.newline_character
        )

    @staticmethod
    def make_value_visible(value_to_modify):
        """
        For the given value, turn it into a string if necessary, and then replace
        any known "invisible" characters with more visible strings.
        """
        return (
            str(value_to_modify)
            .replace(ParserHelper.__backspace_character, "\\b")
            .replace(ParserHelper.__alert_character, "\\a")
            .replace(ParserHelper.tab_character, "\\t")
            .replace(ParserHelper.newline_character, "\\n")
            .replace(ParserHelper.whitespace_split_character, "\\x02")
            .replace(ParserHelper.replace_noop_character, "\\x03")
            .replace(ParserHelper.blech_character, "\\x04")
            .replace(ParserHelper.escape_character, "\\x05")
            .replace("\\x07", "\\a")
            .replace("\\x08", "\\b")
        )

    @staticmethod
    def make_whitespace_visible(value_to_modify):
        """
        For the given value, turn it into a string if necessary, and then replace
        any known whitespace characters with more visible strings.
        """
        return (
            str(value_to_modify)
            .replace(ParserHelper.tab_character, "\\t")
            .replace(ParserHelper.newline_character, "\\n")
            .replace(" ", "\\s")
        )

    @staticmethod
    def valid_characters_to_escape():
        """
        List of valid characters that can be escaped.
        """
        return (
            ParserHelper.__backspace_character
            + ParserHelper.__alert_character
            + ParserHelper.whitespace_split_character
            + ParserHelper.replace_noop_character
            + ParserHelper.blech_character
            + ParserHelper.escape_character
        )

    @staticmethod
    def escape_special_characters(string_to_escape):
        """
        Build another string that has any special characters in the argument escaped.
        """
        escaped_string = ""
        characters_to_escape = ParserHelper.valid_characters_to_escape()
        for next_char_index, next_character in enumerate(string_to_escape):
            if ParserHelper.is_character_at_index_one_of(
                string_to_escape, next_char_index, characters_to_escape
            ):
                escaped_string += ParserHelper.escape_character
            escaped_string += next_character
        return escaped_string

    @staticmethod
    def remove_backspaces_from_text(token_text):
        """
        Remove any backspaces from the text.
        """
        start_index = 0
        adjusted_text_token = token_text[0:]
        next_backspace_index = ParserHelper.__find_with_escape(
            adjusted_text_token, ParserHelper.__backspace_character, start_index
        )
        while next_backspace_index != -1:
            adjusted_text_token = (
                adjusted_text_token[0:next_backspace_index]
                + adjusted_text_token[next_backspace_index + 1 :]
            )
            start_index = next_backspace_index
            next_backspace_index = ParserHelper.__find_with_escape(
                adjusted_text_token, ParserHelper.__backspace_character, start_index
            )
        return adjusted_text_token

    @staticmethod
    def resolve_backspaces_from_text(token_text):
        """
        Deal with any backslash encoding in text with backspaces.
        """
        start_index = 0
        adjusted_text_token = token_text[0:]
        next_backspace_index = ParserHelper.__find_with_escape(
            adjusted_text_token, ParserHelper.__backspace_character, start_index
        )
        while next_backspace_index != -1:
            adjusted_text_token = (
                adjusted_text_token[0 : next_backspace_index - 1]
                + adjusted_text_token[next_backspace_index + 1 :]
            )
            start_index = next_backspace_index
            next_backspace_index = ParserHelper.__find_with_escape(
                adjusted_text_token, ParserHelper.__backspace_character, start_index
            )
        return adjusted_text_token

    @staticmethod
    def create_replacement_markers(replace_this_string, with_this_string):
        """
        Create a replacement marker indicating that the first string is being replaced
        by the second string.
        """
        return (
            ParserHelper.__alert_character
            + replace_this_string
            + ParserHelper.__alert_character
            + with_this_string
            + ParserHelper.__alert_character
        )

    @staticmethod
    def create_replace_with_nothing_marker(replace_this_string):
        """
        Create a replacement marker of the given string with the noop character.
        """
        return ParserHelper.create_replacement_markers(
            replace_this_string, ParserHelper.replace_noop_character
        )

    @staticmethod
    def __remove_sequence_from_text(token_text, sequence_to_remove):
        """
        Resolve the specific character out of the text string.
        """
        start_index = 0
        adjusted_text_token = token_text[0:]
        next_backspace_index = ParserHelper.__find_with_escape(
            adjusted_text_token, sequence_to_remove, start_index
        )
        while next_backspace_index != -1:
            adjusted_text_token = (
                adjusted_text_token[0:next_backspace_index]
                + adjusted_text_token[next_backspace_index + 1 :]
            )
            start_index = next_backspace_index
            next_backspace_index = ParserHelper.__find_with_escape(
                adjusted_text_token, sequence_to_remove, start_index
            )
        return adjusted_text_token

    @staticmethod
    def resolve_noops_from_text(token_text):
        """
        Resolve the replacement noop character out of the text string.
        """
        return ParserHelper.__remove_sequence_from_text(
            token_text, ParserHelper.replace_noop_character
        )

    @staticmethod
    def resolve_blechs_from_text(token_text):
        """
        Resolve the blech character out of the text string.
        """
        return ParserHelper.__remove_sequence_from_text(
            token_text, ParserHelper.blech_character
        )

    @staticmethod
    def resolve_escapes_from_text(token_text):
        """
        Resolve any escapes from the text, leaving only what they escaped.
        """
        start_index = 0
        adjusted_text_token = token_text[0:]
        next_backspace_index = ParserHelper.__find_with_escape(
            adjusted_text_token, ParserHelper.escape_character, start_index
        )
        while next_backspace_index != -1:
            # LOGGER.debug(
            #    "before>%s>%s>",
            #    str(len(adjusted_text_token)),
            #    ParserHelper.make_value_visible(adjusted_text_token),
            # )
            adjusted_text_token = (
                adjusted_text_token[0:next_backspace_index]
                + adjusted_text_token[next_backspace_index + 1 :]
            )
            # LOGGER.debug(
            #    "after>%s>%s",
            #    str(len(adjusted_text_token)),
            #    ParserHelper.make_value_visible(adjusted_text_token),
            # )
            start_index = next_backspace_index + 1
            next_backspace_index = ParserHelper.__find_with_escape(
                adjusted_text_token, ParserHelper.escape_character, start_index
            )
        return adjusted_text_token

    @staticmethod
    def remove_escapes_from_text(token_text):
        """
        Remove any escape characters from the text.
        """
        return ParserHelper.resolve_escapes_from_text(token_text)

    @staticmethod
    def resolve_replacement_markers_from_text(main_text):
        """
        Resolve the alert characters (i.e. replacement markers) out of the text string.
        """
        start_index = 0
        start_replacement_index = ParserHelper.__find_with_escape(
            main_text, ParserHelper.__alert_character, start_index
        )
        while start_replacement_index != -1:
            middle_replacement_index = main_text.index(
                ParserHelper.__alert_character, start_replacement_index + 1
            )
            end_replacement_index = main_text.index(
                ParserHelper.__alert_character, middle_replacement_index + 1
            )

            replace_text = main_text[
                start_replacement_index + 1 : middle_replacement_index
            ]

            # It is possible to have one level of nesting, so deal with it.
            if middle_replacement_index + 1 == end_replacement_index:
                inner_start_replacement_index = main_text.index(
                    ParserHelper.__alert_character, end_replacement_index + 1
                )
                inner_middle_replacement_index = main_text.index(
                    ParserHelper.__alert_character, inner_start_replacement_index + 1
                )
                inner_end_replacement_index = main_text.index(
                    ParserHelper.__alert_character, inner_middle_replacement_index + 1
                )
                assert inner_middle_replacement_index + 1 == inner_end_replacement_index
                end_replacement_index = inner_end_replacement_index

            length_before_mod = len(main_text)
            if start_replacement_index:
                main_text = (
                    main_text[0:start_replacement_index]
                    + replace_text
                    + main_text[end_replacement_index + 1 :]
                )
            else:
                main_text = replace_text + main_text[end_replacement_index + 1 :]
            length_after_mod = len(main_text)
            start_index = (
                end_replacement_index + 1 + (length_after_mod - length_before_mod)
            )
            start_replacement_index = ParserHelper.__find_with_escape(
                main_text, ParserHelper.__alert_character, start_index
            )
        return main_text

    @staticmethod
    def __find_with_escape(adjusted_text_token, find_char, start_index):
        repeat_me = True
        found_index = -1
        # LOGGER.debug(
        #    "token>%s>%s",
        #    str(len(adjusted_text_token)),
        #    ParserHelper.make_value_visible(adjusted_text_token),
        # )
        # LOGGER.debug("find_char>%s", ParserHelper.make_value_visible(find_char))
        # LOGGER.debug("start_index>%s", str(start_index))
        while repeat_me and start_index < len(adjusted_text_token):
            repeat_me = False
            # LOGGER.debug("start>%s", str(start_index))
            start_replacement_index = adjusted_text_token.find(find_char, start_index)
            # LOGGER.debug("start_replacement_index>%s", str(start_replacement_index))
            if (
                start_replacement_index != -1
                and start_replacement_index > 0
                and adjusted_text_token[start_replacement_index - 1]
                == ParserHelper.escape_character
            ):
                repeat_me = True
                start_index = start_replacement_index + 1
                # LOGGER.debug("look>%s", str(start_index))
            else:
                found_index = start_replacement_index
                # LOGGER.debug("found>%s", str(found_index))
        return found_index

    @staticmethod
    def resolve_references_from_text(adjusted_text_token):
        """
        The alert characters signal that a replacement has occurred, so make sure
        we take the right text from the replacement.
        """
        start_index = 0
        # LOGGER.debug(
        #    "adjusted_text_token>%s",
        #    ParserHelper.make_value_visible(adjusted_text_token),
        # )
        start_replacement_index = ParserHelper.__find_with_escape(
            adjusted_text_token, ParserHelper.__alert_character, start_index
        )
        # LOGGER.debug("start_replacement_index>%s", str(start_replacement_index))
        while start_replacement_index != -1:
            middle_replacement_index = adjusted_text_token.index(
                ParserHelper.__alert_character, start_replacement_index + 1
            )
            end_replacement_index = adjusted_text_token.index(
                ParserHelper.__alert_character, middle_replacement_index + 1
            )

            if middle_replacement_index + 1 == end_replacement_index:
                inner_start_replacement_index = adjusted_text_token.index(
                    ParserHelper.__alert_character, end_replacement_index + 1
                )
                inner_middle_replacement_index = adjusted_text_token.index(
                    ParserHelper.__alert_character, inner_start_replacement_index + 1
                )
                inner_end_replacement_index = adjusted_text_token.index(
                    ParserHelper.__alert_character, inner_middle_replacement_index + 1
                )
                replace_text = adjusted_text_token[
                    inner_start_replacement_index + 1 : inner_middle_replacement_index
                ]
                assert inner_middle_replacement_index + 1 == inner_end_replacement_index
                end_replacement_index = inner_end_replacement_index
            else:
                replace_text = adjusted_text_token[
                    middle_replacement_index + 1 : end_replacement_index
                ]

            length_before_mod = len(adjusted_text_token)
            if start_replacement_index:
                adjusted_text_token = (
                    adjusted_text_token[0:start_replacement_index]
                    + replace_text
                    + adjusted_text_token[end_replacement_index + 1 :]
                )
            else:
                adjusted_text_token = (
                    replace_text + adjusted_text_token[end_replacement_index + 1 :]
                )
            length_after_mod = len(adjusted_text_token)
            start_index = (
                end_replacement_index + 1 + (length_after_mod - length_before_mod)
            )
            # LOGGER.debug("start_index>%s", str(start_index))
            start_replacement_index = ParserHelper.__find_with_escape(
                adjusted_text_token, ParserHelper.__alert_character, start_index
            )
            # LOGGER.debug("start_replacement_index>%s", str(start_replacement_index))
        return adjusted_text_token

    @staticmethod
    def repeat_string(string_to_repeat, repeat_count):
        """
        Repeat the given character the specified number of times.
        """
        return "".rjust(repeat_count, string_to_repeat)


# pylint: enable=too-many-public-methods


# pylint: disable=too-few-public-methods, too-many-instance-attributes
class ParserState:
    """
    Class to provide for an encapsulation of the high level state of the parser.
    """

    def __init__(
        self, token_stack, token_document, close_open_blocks_fn, handle_blank_line_fn
    ):
        self.token_stack = token_stack
        self.token_document = token_document
        self.close_open_blocks_fn = close_open_blocks_fn
        self.handle_blank_line_fn = handle_blank_line_fn

        self.same_line_container_tokens = None
        self.last_block_quote_stack_token = None
        self.last_block_quote_markdown_token_index = None
        self.copy_of_last_block_quote_markdown_token = None
        self.original_line_to_parse = None


# pylint: enable=too-few-public-methods, too-many-instance-attributes


# pylint: disable=too-few-public-methods
class PositionMarker:
    """
    Class to provide an encapsulation of the location within the Markdown document.
    """

    def __init__(self, line_number, index_number, text_to_parse, index_indent=0):
        self.__line_number = line_number
        self.__index_number = index_number
        self.__text_to_parse = text_to_parse
        self.__index_indent = index_indent

    @property
    def line_number(self):
        """
        Gets the line number.
        """
        return self.__line_number

    @property
    def index_number(self):
        """
        Gets the index number.
        """
        return self.__index_number

    @property
    def text_to_parse(self):
        """
        Gets the text being parsed.
        """
        return self.__text_to_parse

    @property
    def index_indent(self):
        """
        Gets the amount that the index is considered indented by.
        """
        return self.__index_indent


# pylint: enable=too-few-public-methods
