"""
Module to provide helper functions for parsing html.
"""
from pymarkdown.parser_helper import ParserHelper


class HtmlHelper:
    """
    Class to provide helper functions for parsing html.
    """

    html_block_1_start_tag_prefix = ["script", "pre", "style"]
    html_tag_attribute_value_terminators = " \"'=<>`"

    @staticmethod
    # pylint: disable=chained-comparison
    def is_valid_tag_name(tag_name):
        """
        Determine if the html tag name is valid according to the html rules.
        """

        is_valid = bool(tag_name)
        for next_character in tag_name.lower():
            if not (
                (next_character >= "a" and next_character <= "z")
                or (next_character >= "0" and next_character <= "9")
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
                    string_to_parse[string_index] >= "a"
                    and string_to_parse[string_index] <= "z"
                )
                or (
                    string_to_parse[string_index] >= "A"
                    and string_to_parse[string_index] <= "Z"
                )
                or (
                    string_to_parse[string_index] >= "0"
                    and string_to_parse[string_index] <= "9"
                )
                or string_to_parse[string_index] == ":"
                or string_to_parse[string_index] == "_"
            )
        ):
            return -1
        string_index = string_index + 1
        while string_index < len(string_to_parse):
            if not (
                (
                    string_to_parse[string_index] >= "a"
                    and string_to_parse[string_index] <= "z"
                )
                or (
                    string_to_parse[string_index] >= "A"
                    and string_to_parse[string_index] <= "Z"
                )
                or (
                    string_to_parse[string_index] >= "0"
                    and string_to_parse[string_index] <= "9"
                )
                or string_to_parse[string_index] == ":"
                or string_to_parse[string_index] == "."
                or string_to_parse[string_index] == "-"
                or string_to_parse[string_index] == "_"
            ):
                break
            string_index = string_index + 1

        if string_index < len(string_to_parse) and (
            string_to_parse[string_index] == "="
            or string_to_parse[string_index] == " "
            or string_to_parse[string_index] == "/"
            or string_to_parse[string_index] == ">"
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
            and line_to_parse[non_whitespace_index] != "="
        ) or non_whitespace_index >= len(line_to_parse):
            return non_whitespace_index

        non_whitespace_index = non_whitespace_index + 1
        non_whitespace_index, _ = ParserHelper.extract_whitespace(
            line_to_parse, non_whitespace_index
        )
        if non_whitespace_index < len(line_to_parse):
            first_character_of_value = line_to_parse[non_whitespace_index]
            if first_character_of_value == '"':
                (
                    non_whitespace_index,
                    extracted_text,
                ) = ParserHelper.collect_until_character(
                    line_to_parse, non_whitespace_index + 1, '"'
                )
                if non_whitespace_index == len(line_to_parse):
                    return -1
                non_whitespace_index = non_whitespace_index + 1
            elif first_character_of_value == "'":
                (
                    non_whitespace_index,
                    extracted_text,
                ) = ParserHelper.collect_until_character(
                    line_to_parse, non_whitespace_index + 1, "'"
                )
                if non_whitespace_index == len(line_to_parse):
                    return -1
                non_whitespace_index = non_whitespace_index + 1
            else:
                (
                    non_whitespace_index,
                    extracted_text,
                ) = ParserHelper.collect_until_one_of_characters(
                    line_to_parse,
                    non_whitespace_index,
                    HtmlHelper.html_tag_attribute_value_terminators,
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
            and line_to_parse[non_whitespace_index] == ">"
        )
        return have_end_of_tag and is_valid, non_whitespace_index + 1

    @staticmethod
    def is_valid_block_1_tag_name(tag_name):
        """
        Determine if the tag name is a valid block-1 html tag name.
        """

        is_tag_valid = tag_name in HtmlHelper.html_block_1_start_tag_prefix
        return is_tag_valid

    @staticmethod
    def is_complete_html_start_tag(tag_name, line_to_parse, next_char_index):
        """
        Determine if the supplied information is a completed start of tag specification.
        """

        is_tag_valid = HtmlHelper.is_valid_tag_name(
            tag_name
        ) and not HtmlHelper.is_valid_block_1_tag_name(tag_name)

        non_whitespace_index, extracted_whitespace = ParserHelper.extract_whitespace(
            line_to_parse, next_char_index
        )

        are_attributes_valid = True
        while (
            is_tag_valid
            and extracted_whitespace
            and are_attributes_valid
            and (
                # pylint: disable=chained-comparison
                non_whitespace_index >= 0
                and non_whitespace_index < len(line_to_parse)
            )
            and not (
                line_to_parse[non_whitespace_index] == ">"
                or line_to_parse[non_whitespace_index] == "/"
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
            and line_to_parse[non_whitespace_index] == "/"
        ):
            non_whitespace_index = non_whitespace_index + 1
        if (
            non_whitespace_index < len(line_to_parse)
            and line_to_parse[non_whitespace_index] == ">"
        ):
            non_whitespace_index = non_whitespace_index + 1
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
