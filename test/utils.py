"""
Module to provide helper methods for tests.
"""
import difflib
import json
import tempfile

from pymarkdown.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.parser_helper import PositionMarker


def write_temporary_configuration(supplied_configuration):
    """
    Write the configuration as a temporary file that is kept around.
    """
    try:
        with tempfile.TemporaryFile("wt", delete=False) as outfile:
            if isinstance(supplied_configuration, str):
                outfile.write(supplied_configuration)
            else:
                json.dump(supplied_configuration, outfile)
            return outfile.name
    except IOError as ex:
        assert False, "Test configuration file was not written (" + str(ex) + ")."


def assert_if_lists_different(expected_tokens, actual_tokens):
    """
    Compart two lists and make sure they are equal, asserting if not.
    """

    print("\n---")
    print("expected_tokens: " + str(expected_tokens))
    print(
        "parsed_tokens  : "
        + str(actual_tokens).replace("\n", "\\n").replace("\t", "\\t")
    )
    assert len(expected_tokens) == len(actual_tokens), (
        "List lengths are not the same: ("
        + str(len(expected_tokens))
        + ") vs "
        + "("
        + str(len(actual_tokens))
        + ")"
    )
    print("---")

    # pylint: disable=consider-using-enumerate
    for element_index in range(0, len(expected_tokens)):

        expected_str = str(expected_tokens[element_index])
        actual_str = str(actual_tokens[element_index])

        print(
            "expected_tokens("
            + str(len(expected_str))
            + ")>>"
            + expected_str.replace("\t", "\\t")
            + "<<"
        )
        print(
            "actual_tokens  ("
            + str(len(actual_str))
            + ")>>"
            + actual_str.replace("\t", "\\t")
            + "<<"
        )

        diff = difflib.ndiff(expected_str, actual_str)

        diff_values = "\n".join(list(diff)) + "\n---\n"

        assert expected_str == str(actual_tokens[element_index]), (
            "List items " + str(element_index) + " are not equal." + diff_values
        )
    print("---\nToken lists are equal.\n---")
    # pylint: enable=consider-using-enumerate


def assert_if_strings_different(expected_string, actual_string):
    """
    Compart two strings and make sure they are equal, asserting if not.
    """

    print(
        "expected_string(" + str(len(expected_string)) + ")>>" + expected_string + "<<"
    )
    print("actual_string  (" + str(len(actual_string)) + ")>>" + actual_string + "<<")

    diff = difflib.ndiff(expected_string, actual_string)

    diff_values = "\n".join(list(diff)) + "\n---\n"

    assert expected_string == actual_string, "Strings are not equal." + diff_values


def __calc_me(calc_token):
    if calc_token.token_name == MarkdownToken.token_thematic_break:
        depth = 1
    else:
        depth = -1
        # assert False
    return depth


def __calc_adjusted_position(markdown_token):
    if markdown_token.token_name == MarkdownToken.token_setext_heading:
        line_number = markdown_token.original_line_number
        index_number = markdown_token.original_column_number
    else:
        line_number = markdown_token.line_number
        index_number = markdown_token.column_number
    return PositionMarker(line_number, index_number, "")


def assert_token_consistency(source_markdown, expected_tokens):
    """
    Compare the markdown document against the tokens that are expected.
    """

    assert source_markdown
    # split_lines = source_markdown.split("\n")
    # number_of_lines = len(split_lines)
    # print(">>" + str(number_of_lines))
    last_token = None
    for current_token in expected_tokens:
        if current_token.token_class == MarkdownTokenClass.INLINE_BLOCK:
            continue

        current_position = __calc_adjusted_position(current_token)

        # fg = __calc_me(i)
        print(
            "this>>"
            + str(current_token.token_name)
            + ">>"
            + str(current_token.token_class)
            + ">>("
            + str(current_position.line_number)
            + ","
            + str(current_position.index_number)
            + ")"
        )
        if last_token:
            last_position = __calc_adjusted_position(last_token)
            print(
                "last>>"
                + str(last_token.token_name)
                + ">>"
                + str(last_token.token_class)
                + ">>("
                + str(last_position.line_number)
                + ","
                + str(last_position.index_number)
                + ")"
            )
            if last_position.line_number == current_position.line_number:
                assert last_token.token_class == MarkdownTokenClass.CONTAINER_BLOCK
                assert current_position.index_number > last_position.index_number
        else:
            assert current_position.line_number == 1

        last_token = current_token
