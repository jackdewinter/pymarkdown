"""
Module to provide helper methods for tests.
"""
import difflib
import json
import logging
import tempfile
from test.transform_to_markdown import TransformToMarkdown
from test.verify_line_and_column_numbers import verify_line_and_column_numbers

from pymarkdown.application_properties import ApplicationProperties
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm


def act_and_assert(
    source_markdown, expected_gfm, expected_tokens, show_debug=False, config_map=None
):
    """
    Act and assert on the expected behavior of parsing the source_markdown.
    """

    # Arrange
    logging.getLogger().setLevel(logging.DEBUG if show_debug else logging.WARNING)
    ParserLogger.sync_on_next_call()

    tokenizer = TokenizedMarkdown()
    if config_map:
        test_properties = ApplicationProperties()
        test_properties.load_from_dict(config_map)
        tokenizer.apply_configuration(test_properties)
    transformer = TransformToGfm()

    # Act
    actual_tokens = tokenizer.transform(source_markdown, show_debug=show_debug)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


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
    Compare two lists and make sure they are equal, asserting if not.
    """

    print("\n---")
    print("expected_tokens: " + ParserHelper.make_value_visible(expected_tokens))
    print("parsed_tokens  : " + ParserHelper.make_value_visible(actual_tokens))
    assert len(expected_tokens) == len(actual_tokens), (
        "List lengths are not the same: ("
        + str(len(expected_tokens))
        + ") vs "
        + "("
        + str(len(actual_tokens))
        + ")"
    )
    print("---")

    for element_index, next_expected_token in enumerate(expected_tokens):

        expected_str = str(next_expected_token)
        actual_str = str(actual_tokens[element_index])

        print(
            "expected_tokens("
            + str(len(expected_str))
            + ")>>"
            + ParserHelper.make_value_visible(expected_str)
            + "<<"
        )
        print(
            "actual_tokens  ("
            + str(len(actual_str))
            + ")>>"
            + ParserHelper.make_value_visible(actual_str)
            + "<<"
        )

        diff = difflib.ndiff(expected_str, actual_str)

        diff_values = ParserHelper.newline_character.join(list(diff)) + "\n---\n"

        assert expected_str == str(actual_tokens[element_index]), (
            "List items " + str(element_index) + " are not equal." + diff_values
        )
    print("---\nToken lists are equal.\n---")


def assert_if_strings_different(expected_string, actual_string):
    """
    Compare two strings and make sure they are equal, asserting if not.
    """

    print(
        "expected_string(" + str(len(expected_string)) + ")>>" + expected_string + "<<"
    )
    print("expected_string>>" + ParserHelper.make_value_visible(expected_string) + "<<")

    print("actual_string  (" + str(len(actual_string)) + ")>>" + actual_string + "<<")
    print("actual_string  >>" + ParserHelper.make_value_visible(actual_string) + "<<")

    diff = difflib.ndiff(expected_string, actual_string)

    diff_values = ParserHelper.newline_character.join(list(diff)) + "\n---\n"

    assert expected_string == actual_string, "Strings are not equal." + diff_values


def assert_token_consistency(source_markdown, actual_tokens):
    """
    Compare the markdown document against the tokens that are expected.
    """

    verify_markdown_roundtrip(source_markdown, actual_tokens)
    verify_line_and_column_numbers(source_markdown, actual_tokens)


def verify_markdown_roundtrip(source_markdown, actual_tokens):
    """
    Verify that we can use the information in the tokens to do a round trip back
    to the original Markdown that created the token.
    """

    if ParserHelper.tab_character in source_markdown:
        return

    transformer = TransformToMarkdown()
    original_markdown, avoid_processing = transformer.transform(actual_tokens)

    if avoid_processing:
        print("Comparison of generated Markdown against original Markdown shipped.")
    else:
        print(
            "\n-=-=-\nExpected\n-=-=-\n-->"
            + ParserHelper.make_value_visible(source_markdown)
            + "<--\n-=-=-\nActual\n-=-=-\n-->"
            + ParserHelper.make_value_visible(original_markdown)
            + "<--\n-=-=-\n"
        )
        diff = difflib.ndiff(source_markdown, original_markdown)
        diff_values = (
            "\n-=-=-n"
            + ParserHelper.newline_character.join(list(diff))
            + "\n-=-=-expected\n-->"
            + ParserHelper.make_value_visible(source_markdown)
            + "<--\n-=-=-actual\n-->"
            + ParserHelper.make_value_visible(original_markdown)
            + "<--\n-=-=-\n"
        )

        assert source_markdown == original_markdown, (
            "Strings are not equal." + diff_values
        )
