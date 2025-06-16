"""
Tests for the extract_whitespace function.
"""

from pymarkdown.general.parser_helper import ParserHelper


def test_empty_string_with_good_index() -> None:
    """
    Make sure that an empty string is handled properly with a good index
    """

    # Arrange
    input_string = ""
    start_index = 0
    expected_output = (0, "")

    # Act
    actual_output = ParserHelper.extract_ascii_whitespace(input_string, start_index)

    # Assert
    assert expected_output == actual_output


def test_empty_string_with_bad_right_index() -> None:
    """
    Make sure that an empty string is handled properly with an index that is too far to the right.
    """

    # Arrange
    input_string = ""
    start_index = 2
    expected_output = (None, None)

    # Act
    actual_output = ParserHelper.extract_ascii_whitespace(input_string, start_index)

    # Assert
    assert expected_output == actual_output


def test_empty_string_with_bad_left_index() -> None:
    """
    Make sure that an empty string is handled properly with an index that is too far to the left.
    """

    # Arrange
    input_string = ""
    start_index = -1
    expected_output = (None, None)

    # Act
    actual_output = ParserHelper.extract_ascii_whitespace(input_string, start_index)

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_start_with_whitespace() -> None:
    """
    Make sure that we test a simple extraction from the start of the string with whitespace.
    """

    # Arrange
    input_string = "  this is a test"
    start_index = 0
    expected_output = (2, "  ")

    # Act
    actual_output = ParserHelper.extract_ascii_whitespace(input_string, start_index)

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_start_without_whitespace() -> None:
    """
    Make sure that we test a simple extraction from the start of the string without whitespace.
    """

    # Arrange
    input_string = "  this is a test"
    start_index = 2
    expected_output = (start_index, "")

    # Act
    actual_output = ParserHelper.extract_ascii_whitespace(input_string, start_index)

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_middle_with_whitespace() -> None:
    """
    Make sure that we test a simple extraction from the middle of the string with whitespace
    """

    # Arrange
    input_string = "this is a test"
    start_index = 4
    expected_output = (5, " ")

    # Act
    actual_output = ParserHelper.extract_ascii_whitespace(input_string, start_index)

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_middle_without_whitespace() -> None:
    """
    Make sure that we test a simple extraction from the middle of the string without whitespace
    """

    # Arrange
    input_string = "this is a test"
    start_index = 5
    expected_output = (start_index, "")

    # Act
    actual_output = ParserHelper.extract_ascii_whitespace(input_string, start_index)

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_end_with_whitespace() -> None:
    """
    Make sure that we test a simple extraction from the end of the string with whitespace
    """

    # Arrange
    input_string = "this is a test  "
    start_index = 14
    expected_output = (len(input_string), "  ")

    # Act
    actual_output = ParserHelper.extract_ascii_whitespace(input_string, start_index)

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_end_without_whitespace() -> None:
    """
    Make sure that we test a simple extraction from the end of the string without whitespace
    """

    # Arrange
    input_string = "this is a test"
    start_index = 14
    expected_output = (len(input_string), "")

    # Act
    actual_output = ParserHelper.extract_ascii_whitespace(input_string, start_index)

    # Assert
    assert expected_output == actual_output
