"""
Tests for the collect_while_one_of_characters function.
"""
from pymarkdown.parser_helper import ParserHelper


def test_empty_string_with_good_index():
    """
    Make sure that an empty string is handled properly with a good index
    """

    # Arrange
    input_string = ""
    start_index = 0
    characters_to_match = " !"
    expected_output = (0, "")

    # Act
    actual_output = ParserHelper.collect_while_one_of_characters(
        input_string, start_index, characters_to_match
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
    characters_to_match = " !"
    expected_output = (None, None)

    # Act
    actual_output = ParserHelper.collect_while_one_of_characters(
        input_string, start_index, characters_to_match
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
    characters_to_match = " !"
    expected_output = (None, None)

    # Act
    actual_output = ParserHelper.collect_while_one_of_characters(
        input_string, start_index, characters_to_match
    )

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_start():
    """
    Make sure that we test a simple extraction from the start of the string.
    """

    # Arrange
    input_string = "tata is a test"
    start_index = 0
    characters_to_match = "at"
    expected_output = (4, "tata")

    # Act
    actual_output = ParserHelper.collect_while_one_of_characters(
        input_string, start_index, characters_to_match
    )

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_middle():
    """
    Make sure that we test a simple extraction from the middle of the string.
    """

    # Arrange
    input_string = "this!is!a!test"
    start_index = 5
    characters_to_match = "is"
    expected_output = (7, "is")

    # Act
    actual_output = ParserHelper.collect_while_one_of_characters(
        input_string, start_index, characters_to_match
    )

    # Assert
    assert expected_output == actual_output


def test_simple_case_from_end():
    """
    Make sure that we test a simple extraction from the end of the string.
    """

    # Arrange
    input_string = "this is a test"
    start_index = 10
    characters_to_match = "set"
    expected_output = (len(input_string), "test")

    # Act
    actual_output = ParserHelper.collect_while_one_of_characters(
        input_string, start_index, characters_to_match
    )

    # Assert
    assert expected_output == actual_output


def test_already_on_whitespace():
    """
    Make sure that we test extracting while already on a whitespace character.
    """

    # Arrange
    input_string = "this!is!a!test"
    start_index = 9
    characters_to_match = "xyz"
    expected_output = (9, "")

    # Act
    actual_output = ParserHelper.collect_while_one_of_characters(
        input_string, start_index, characters_to_match
    )

    # Assert
    assert expected_output == actual_output
