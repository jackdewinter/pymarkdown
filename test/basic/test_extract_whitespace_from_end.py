"""
Tests for the extract_whitespace_from_end function.
"""
from pymarkdown.general.parser_helper import ParserHelper


def test_empty_string():
    """
    Make sure that an empty string is handled properly
    """

    # Arrange
    input_string = ""
    expected_output = (0, "")

    # Act
    actual_output = ParserHelper.extract_spaces_from_end(input_string)

    # Assert
    assert expected_output == actual_output


def test_string_with_no_trailing_spaces():
    """
    Make sure that a string with no trailing spaces is handled properly
    """

    # Arrange
    input_string = "no trailing spaces"
    expected_output = (len(input_string), "")

    # Act
    actual_output = ParserHelper.extract_spaces_from_end(input_string)

    # Assert
    assert expected_output == actual_output


def test_string_with_some_trailing_spaces():
    """
    Make sure that a string with some trailing spaces is handled properly
    """

    # Arrange
    input_string = "some trailing spaces  "
    expected_output = (len(input_string) - 2, "  ")

    # Act
    actual_output = ParserHelper.extract_spaces_from_end(input_string)

    # Assert
    assert expected_output == actual_output
