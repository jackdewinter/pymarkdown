"""
Tests for the collect_while_character function.
"""

from pymarkdown.general.parser_helper import ParserHelper


def test_empty_string_with_good_index():
    """
    Make sure that an empty string is handled properly with a good index
    """

    # Arrange
    input_string = ""
    start_index = 0
    character_to_match = " "
    expected_output = (0, 0)

    # Act
    actual_output = ParserHelper.collect_while_character(
        input_string, start_index, character_to_match
    )

    # Assert
    assert expected_output == actual_output


def test_empty_string_with_bad_right_index():
    """
    Make sure that an empty string is handled properly with an index that is too far to the right.
    """

    # Arrange
    input_string = ""
    start_index = 2
    character_to_match = " "
    expected_output = (None, None)

    # Act
    actual_output = ParserHelper.collect_while_character(
        input_string, start_index, character_to_match
    )

    # Assert
    assert expected_output == actual_output


def test_empty_string_with_bad_left_index():
    """
    Make sure that an empty string is handled properly with an index that is too far to the left.
    """

    # Arrange
    input_string = ""
    start_index = -1
    character_to_match = " "
    expected_output = (None, None)

    # Act
    actual_output = ParserHelper.collect_while_character(
        input_string, start_index, character_to_match
    )

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_start_with_whitespace():
    """
    Make sure that we test a simple extraction from the start of the string with whitespace.
    """

    # Arrange
    input_string = "  this is a test"
    start_index = 0
    character_to_match = " "
    expected_output = (2, 2)

    # Act
    actual_output = ParserHelper.collect_while_character(
        input_string, start_index, character_to_match
    )

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_start_without_whitespace():
    """
    Make sure that we test a simple extraction from the start of the string without whitespace.
    """

    # Arrange
    input_string = "  this is a test"
    start_index = 2
    character_to_match = " "
    expected_output = (0, 2)

    # Act
    actual_output = ParserHelper.collect_while_character(
        input_string, start_index, character_to_match
    )

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_middle_with_whitespace():
    """
    Make sure that we test a simple extraction from the middle of the string with whitespace
    """

    # Arrange
    input_string = "this is a test"
    start_index = 4
    character_to_match = " "
    expected_output = (1, 5)

    # Act
    actual_output = ParserHelper.collect_while_character(
        input_string, start_index, character_to_match
    )

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_middle_without_whitespace():
    """
    Make sure that we test a simple extraction from the middle of the string without whitespace
    """

    # Arrange
    input_string = "this is a test"
    start_index = 5
    character_to_match = " "
    expected_output = (0, start_index)

    # Act
    actual_output = ParserHelper.collect_while_character(
        input_string, start_index, character_to_match
    )

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_end_with_whitespace():
    """
    Make sure that we test a simple extraction from the end of the string with whitespace
    """

    # Arrange
    input_string = "this is a test  "
    start_index = 14
    character_to_match = " "
    expected_output = (2, len(input_string))

    # Act
    actual_output = ParserHelper.collect_while_character(
        input_string, start_index, character_to_match
    )

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_end_without_whitespace():
    """
    Make sure that we test a simple extraction from the end of the string without whitespace
    """

    # Arrange
    input_string = "this is a test"
    start_index = 14
    character_to_match = " "
    expected_output = (0, len(input_string))

    # Act
    actual_output = ParserHelper.collect_while_character(
        input_string, start_index, character_to_match
    )

    # Assert
    assert expected_output == actual_output
