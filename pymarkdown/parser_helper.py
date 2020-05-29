"""
Module to provide helper functions for parsing.
"""


# pylint: disable=too-many-public-methods
class ParserHelper:
    """
    Class to provide helper functions for parsing.
    """

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
            or source_string[index_in_string] == "\t"
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
    def extract_whitespace_from_end(source_string):
        """
        From the end of the string, continue extracting whitespace while we have it.

        Returns the index of the last non-whitespace character and any extracted whitespace
        in a tuple.
        """
        if not source_string:
            return 0, ""

        index = len(source_string) - 1
        while ParserHelper.is_character_at_index_whitespace(source_string, index):
            index -= 1

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
            if source_character == "\t":
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


# pylint: enable=too-many-public-methods


# pylint: disable=too-few-public-methods
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


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class PositionMarker:
    """
    Class to provide an encapsulation of the location within the Markdown document.
    """

    def __init__(self, line_number, index_number, text_to_parse):
        self.line_number = line_number
        self.index_number = index_number
        self.text_to_parse = text_to_parse
        self.index_indent = 0


# pylint: enable=too-few-public-methods
