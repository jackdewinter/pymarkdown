"""
Module to provide helper functions for parsing.
"""
import copy


# pylint: disable=too-many-lines
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

        string_to_match_size = len(string_to_match)
        return (
            index_in_string >= 0
            and index_in_string + string_to_match_size <= len(source_string)
            and source_string[index_in_string : index_in_string + string_to_match_size]
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

        index = (
            (start_index - 1) if start_index is not None else (len(source_string) - 1)
        )
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

        source_string_size = len(source_string)

        if not 0 <= start_index <= source_string_size:
            return None, None

        index = start_index
        while index < source_string_size and source_string[index] == match_character:
            index += 1
        return index - start_index, index

    @staticmethod
    def collect_backwards_while_character(source_string, end_index, match_character):
        """
        Collect a sequence of the same character from a given starting point in a string going backwards towards the start of the string.

        Returns the number of characters collected and the index of the first non-matching
        character and any extracted text in a tuple.
        """

        source_string_size = len(source_string)
        if not -1 <= end_index <= source_string_size:
            return None, None
        if end_index == -1:
            end_index = source_string_size

        index = end_index
        while index and source_string[index - 1] == match_character:
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

        source_string_size = len(source_string)
        if not -1 <= end_index <= source_string_size:
            return None, None
        if end_index == -1:
            end_index = source_string_size

        index = end_index
        while index and source_string[index - 1] in match_characters:
            index -= 1
        return end_index - index, index

    @staticmethod
    def collect_until_character(source_string, start_index, match_character):
        """
        Collect a sequence of characters from a given starting point in a string until we hit a given character.

        Returns the index of the first non-matching character and any extracted text
        in a tuple.
        """

        source_string_size = len(source_string)
        if not 0 <= start_index <= source_string_size:
            return None, None

        index = start_index
        while index < source_string_size and source_string[index] != match_character:
            index += 1

        return index, source_string[start_index:index]

    @staticmethod
    def collect_while_one_of_characters(source_string, start_index, match_characters):
        """
        Collect a sequence of characters from a given starting point in a string as long as the character is one of the match characters.

        Returns the index of the first non-matching character and any extracted text
        in a tuple.
        """

        source_string_size = len(source_string)
        if not 0 <= start_index <= source_string_size:
            return None, None

        index = start_index
        while index < source_string_size and source_string[index] in match_characters:
            index += 1

        return index, source_string[start_index:index]

    @staticmethod
    def collect_until_one_of_characters(source_string, start_index, match_characters):
        """
        Collect a sequence of characters from a given starting point in a string until we hit one of a given set of characters.

        Returns the index of the first non-matching character and any extracted text
        in a tuple.
        """

        source_string_size = len(source_string)
        if not 0 <= start_index <= source_string_size:
            return None, None

        index = start_index
        while (
            index < source_string_size and source_string[index] not in match_characters
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
            string_length = (
                (int((string_length + 4) / 4) * 4)
                if source_character == ParserHelper.tab_character
                else (string_length + 1)
            )
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

        first_index = -1
        for next_character in find_any:
            found_index = source_text.find(next_character, start_index)
            if found_index != -1:
                first_index = (
                    found_index if first_index == -1 else min(first_index, found_index)
                )
                if first_index == 0:
                    break
        return first_index

    @staticmethod
    def replace_any_of(string_to_search_in, characters_to_search_for, replace_with):
        """
        Replace any of a given set of characters with a given sequence.
        """

        rebuilt_string, start_index = "", 0
        index, ex_str = ParserHelper.collect_until_one_of_characters(
            string_to_search_in, start_index, characters_to_search_for
        )
        string_to_search_in_size = len(string_to_search_in)
        while index < string_to_search_in_size:
            rebuilt_string = rebuilt_string + ex_str + replace_with
            start_index = index + 1
            index, ex_str = ParserHelper.collect_until_one_of_characters(
                string_to_search_in, start_index, characters_to_search_for
            )
        return rebuilt_string + ex_str

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
    def count_newlines_in_texts(*args):
        """
        Count the number of new line characters in a given string.
        """
        total_newlines = 0
        for next_argument in args:
            total_newlines += ParserHelper.count_characters_in_text(
                next_argument, ParserHelper.newline_character
            )
        return total_newlines

    @staticmethod
    def calculate_deltas(text_to_analyze):
        """
        Calculate the deltas associated with a given string.
        """

        delta_line_number = 0
        if ParserHelper.newline_character in text_to_analyze:
            split_raw_tag = text_to_analyze.split(ParserHelper.newline_character)
            delta_line_number += len(split_raw_tag) - 1

            last_element = ParserHelper.__resolve_replacement_markers_from_text(
                split_raw_tag[-1]
            )
            last_element = ParserHelper.__remove_escapes_from_text(last_element)
            length_of_last_elements = len(last_element)

            delta_column_number = -(length_of_last_elements + 1)
        else:
            delta_column_number = len(text_to_analyze)
        return delta_line_number, delta_column_number

    # pylint: disable=too-many-arguments
    @staticmethod
    def recombine_string_with_whitespace(
        text_string,
        whitespace_string,
        start_index=0,
        add_replace_marker_if_empty=False,
        post_increment_index=False,
        start_text_index=1,
        add_whitespace_after=False,
    ):
        """
        Properly recombine a text-string with a matching whitespace-string.
        """
        split_text_string, split_whitespace_string = (
            text_string.split(ParserHelper.newline_character),
            whitespace_string.split(ParserHelper.newline_character),
        )
        for i in range(start_text_index, len(split_text_string)):
            if not post_increment_index:
                start_index += 1
            ew_part = split_whitespace_string[start_index]
            if ew_part and add_replace_marker_if_empty:
                ew_part = ParserHelper.create_replace_with_nothing_marker(ew_part)
            split_text_string[i] = (
                (split_text_string[i] + ew_part)
                if add_whitespace_after
                else (ew_part + split_text_string[i])
            )
            if post_increment_index:
                start_index += 1
        return ParserHelper.newline_character.join(split_text_string), start_index

    # pylint: enable=too-many-arguments

    @staticmethod
    def calculate_last_line(text_string):
        """
        Determine the last line of a multi-line string.
        """
        split_label = text_string.split(ParserHelper.newline_character)
        return split_label[-1]

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
        escaped_string, characters_to_escape = (
            "",
            ParserHelper.valid_characters_to_escape(),
        )
        for next_char_index, next_character in enumerate(string_to_escape):
            if ParserHelper.is_character_at_index_one_of(
                string_to_escape, next_char_index, characters_to_escape
            ):
                escaped_string += ParserHelper.escape_character
            escaped_string += next_character
        return escaped_string

    @staticmethod
    def __remove_backspaces_from_text(token_text):
        """
        Remove any backspaces from the text.
        """
        start_index, adjusted_text_token = 0, token_text[0:]
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
        start_index, adjusted_text_token = 0, token_text[0:]
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
    def __resolve_blechs_from_text(token_text):
        """
        Resolve the blech character out of the text string.
        """
        return ParserHelper.__remove_sequence_from_text(
            token_text, ParserHelper.blech_character
        )

    @staticmethod
    def __resolve_escapes_from_text(token_text):
        """
        Resolve any escapes from the text, leaving only what they escaped.
        """
        start_index, adjusted_text_token = 0, token_text[0:]
        next_backspace_index = ParserHelper.__find_with_escape(
            adjusted_text_token, ParserHelper.escape_character, start_index
        )
        while next_backspace_index != -1:
            adjusted_text_token = (
                adjusted_text_token[0:next_backspace_index]
                + adjusted_text_token[next_backspace_index + 1 :]
            )
            start_index = next_backspace_index + 1
            next_backspace_index = ParserHelper.__find_with_escape(
                adjusted_text_token, ParserHelper.escape_character, start_index
            )
        return adjusted_text_token

    @staticmethod
    def __remove_escapes_from_text(token_text):
        """
        Remove any escape characters from the text.
        """
        return ParserHelper.__resolve_escapes_from_text(token_text)

    @staticmethod
    def __resolve_replacement_markers_from_text(main_text):
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
            main_text = (
                (
                    main_text[0:start_replacement_index]
                    + replace_text
                    + main_text[end_replacement_index + 1 :]
                )
                if start_replacement_index
                else (replace_text + main_text[end_replacement_index + 1 :])
            )
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
        repeat_me, found_index = True, -1
        while repeat_me and start_index < len(adjusted_text_token):
            repeat_me, start_replacement_index = False, adjusted_text_token.find(
                find_char, start_index
            )
            if (
                start_replacement_index != -1
                and start_replacement_index > 0
                and adjusted_text_token[start_replacement_index - 1]
                == ParserHelper.escape_character
            ):
                repeat_me, start_index = True, start_replacement_index + 1
            else:
                found_index = start_replacement_index
        return found_index

    @staticmethod
    def __resolve_references_from_text(adjusted_text_token):
        """
        The alert characters signal that a replacement has occurred, so make sure
        we take the right text from the replacement.
        """
        start_index = 0
        start_replacement_index = ParserHelper.__find_with_escape(
            adjusted_text_token, ParserHelper.__alert_character, start_index
        )
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
            adjusted_text_token = (
                (
                    adjusted_text_token[0:start_replacement_index]
                    + replace_text
                    + adjusted_text_token[end_replacement_index + 1 :]
                )
                if start_replacement_index
                else (replace_text + adjusted_text_token[end_replacement_index + 1 :])
            )
            length_after_mod = len(adjusted_text_token)
            start_index = (
                end_replacement_index + 1 + (length_after_mod - length_before_mod)
            )
            start_replacement_index = ParserHelper.__find_with_escape(
                adjusted_text_token, ParserHelper.__alert_character, start_index
            )
        return adjusted_text_token

    @staticmethod
    def resolve_all_from_text(text_to_resolve):
        """
        Combination to resolve all of these special characters from the text.
        """
        resolved_text = ParserHelper.resolve_backspaces_from_text(text_to_resolve)
        resolved_text = ParserHelper.__resolve_references_from_text(resolved_text)
        resolved_text = ParserHelper.resolve_noops_from_text(resolved_text)
        resolved_text = ParserHelper.__resolve_blechs_from_text(resolved_text)
        return ParserHelper.__resolve_escapes_from_text(resolved_text)

    @staticmethod
    def remove_all_from_text(text_to_remove):
        """
        Combination to remove all of these special characters from the text.
        """
        removed_text = ParserHelper.__remove_backspaces_from_text(text_to_remove)
        removed_text = ParserHelper.__resolve_replacement_markers_from_text(
            removed_text
        )
        return ParserHelper.__remove_escapes_from_text(removed_text)

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
        (
            self.__token_stack,
            self.__token_document,
            self.__close_open_blocks_fn,
            self.__handle_blank_line_fn,
        ) = (token_stack, token_document, close_open_blocks_fn, handle_blank_line_fn)

        (
            self.__same_line_container_tokens,
            self.__last_block_quote_stack_token,
            self.__last_block_quote_markdown_token_index,
            self.__copy_of_last_block_quote_markdown_token,
            self.__original_line_to_parse,
            self.__original_stack_depth,
            self.__original_document_depth,
            self.__no_para_start_if_empty,
        ) = (None, None, None, None, None, None, None, False)

    @property
    def token_stack(self):
        """
        Stack array containing the currently active stack tokens.
        """
        return self.__token_stack

    @property
    def token_document(self):
        """
        Document array containing any Markdown tokens.
        """
        return self.__token_document

    @property
    def close_open_blocks_fn(self):
        """
        Function to handle the closing of blocks.
        """
        return self.__close_open_blocks_fn

    @property
    def handle_blank_line_fn(self):
        """
        Function to handle blank lines.
        """
        return self.__handle_blank_line_fn

    @property
    def same_line_container_tokens(self):
        """
        State of the container tokens at the start of the leaf processing.
        """
        return self.__same_line_container_tokens

    @property
    def last_block_quote_stack_token(self):
        """
        Last block quote token.
        """
        return self.__last_block_quote_stack_token

    @property
    def last_block_quote_markdown_token_index(self):
        """
        Index of the last block quote token.
        """
        return self.__last_block_quote_markdown_token_index

    @property
    def copy_of_last_block_quote_markdown_token(self):
        """
        Copy of the last block quote markdown token, before any changes.
        """
        return self.__copy_of_last_block_quote_markdown_token

    @property
    def original_line_to_parse(self):
        """
        Line to parse, before any processing occurs.
        """
        return self.__original_line_to_parse

    @property
    def original_stack_depth(self):
        """
        Length of the token_stack array at the start of the line.
        """
        return self.__original_stack_depth

    @property
    def original_document_depth(self):
        """
        Length of the token_document array at the start of the line.
        """
        return self.__original_document_depth

    @property
    def no_para_start_if_empty(self):
        """
        Whether to start a paragraph if the owning list item was empty.
        """
        return self.__no_para_start_if_empty

    def find_last_block_quote_on_stack(self):
        """
        Finds the index of the last block quote on the stack (from the end).
        If no block quotes are found, 0 is returned.
        """
        last_stack_index = len(self.token_stack) - 1
        while not self.token_stack[last_stack_index].is_document:
            if self.token_stack[last_stack_index].is_block_quote:
                break
            last_stack_index -= 1
        return last_stack_index

    def find_last_list_block_on_stack(self):
        """
        Finds the index of the last list block on the stack (from the end).
        If no block quotes are found, 0 is returned.
        """
        last_stack_index = len(self.token_stack) - 1
        while not self.token_stack[last_stack_index].is_document:
            if self.token_stack[last_stack_index].is_list:
                break
            last_stack_index -= 1
        return last_stack_index

    def find_last_container_on_stack(self):
        """
        Finds the index of the last container on the stack (from the end).
        If no container tokens are found, 0 is returned.
        """
        last_stack_index = len(self.token_stack) - 1
        while not self.token_stack[last_stack_index].is_document:
            if (
                self.token_stack[last_stack_index].is_block_quote
                or self.token_stack[last_stack_index].is_list
            ):
                break
            last_stack_index -= 1
        return last_stack_index

    def count_of_block_quotes_on_stack(self):
        """
        Helper method to count the number of block quotes currently on the stack.
        """

        stack_bq_count = 0
        for next_item_on_stack in self.token_stack:
            if next_item_on_stack.is_block_quote:
                stack_bq_count += 1

        return stack_bq_count

    def mark_start_information(self, position_marker):
        """
        Mark the start of processing this line of information.  A lot of
        this information is to allow a requeue to occur, if needed.
        """
        (
            self.__original_line_to_parse,
            self.__original_stack_depth,
            self.__original_document_depth,
            self.__no_para_start_if_empty,
        ) = (
            position_marker.text_to_parse[:],
            len(self.token_stack),
            len(self.token_document),
            False,
        )

        last_stack_index = self.find_last_block_quote_on_stack()

        (
            self.__last_block_quote_stack_token,
            self.__last_block_quote_markdown_token_index,
            self.__copy_of_last_block_quote_markdown_token,
        ) = (None, None, None)
        if not self.token_stack[last_stack_index].is_document:
            self.__last_block_quote_stack_token = self.token_stack[last_stack_index]
            self.__last_block_quote_markdown_token_index = self.token_document.index(
                self.token_stack[last_stack_index].matching_markdown_token
            )
            self.__copy_of_last_block_quote_markdown_token = copy.deepcopy(
                self.token_document[self.__last_block_quote_markdown_token_index]
            )

    def mark_for_leaf_processing(self, container_level_tokens):
        """
        Set things up for leaf processing.
        """
        self.__same_line_container_tokens = container_level_tokens

    def clear_after_leaf_processing(self):
        """
        Reset things after leaf processing.
        """
        self.__same_line_container_tokens = None

    def set_no_para_start_if_empty(self):
        """
        Set the member variable to true.
        """
        self.__no_para_start_if_empty = True


# pylint: enable=too-few-public-methods, too-many-instance-attributes


# pylint: disable=too-few-public-methods
class PositionMarker:
    """
    Class to provide an encapsulation of the location within the Markdown document.
    """

    def __init__(self, line_number, index_number, text_to_parse, index_indent=0):
        (
            self.__line_number,
            self.__index_number,
            self.__text_to_parse,
            self.__index_indent,
        ) = (line_number, index_number, text_to_parse, index_indent)

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
