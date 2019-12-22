"""
Tests for the various is_character* functions.
"""
from pymarkdown.parser_helper import ParserHelper


def test_is_character_at_index_whitespace_with_empty_string():
    """
    Make sure that an empty string is handled properly.
    """

    # Arrange
    input_string = ""
    start_index = 0
    expected_output = False

    # Act
    actual_output = ParserHelper.is_character_at_index_whitespace(
        input_string, start_index
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_whitespace_with_low_index():
    """
    Make sure that a string with a low index is handled properly.
    """

    # Arrange
    input_string = "this is a test"
    start_index = -1
    expected_output = False

    # Act
    actual_output = ParserHelper.is_character_at_index_whitespace(
        input_string, start_index
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_whitespace_with_high_index():
    """
    Make sure that a string with a high index is handled properly.
    """

    # Arrange
    input_string = "this is a test"
    start_index = len(input_string)
    expected_output = False

    # Act
    actual_output = ParserHelper.is_character_at_index_whitespace(
        input_string, start_index
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_whitespace_with_whitespace():
    """
    Make sure that a string with whitespace at the index is handled properly.
    """

    # Arrange
    input_string = " "
    start_index = 0
    expected_output = True

    # Act
    actual_output = ParserHelper.is_character_at_index_whitespace(
        input_string, start_index
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_whitespace_with_whitespace_at_end():
    """
    Make sure that a string with whitespace at the index is handled properly.
    """

    # Arrange
    input_string = "this is a test "
    start_index = len(input_string) - 1
    expected_output = True

    # Act
    actual_output = ParserHelper.is_character_at_index_whitespace(
        input_string, start_index
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_whitespace_without_whitespace():
    """
    Make sure that a string with whitespace at the index is handled properly.
    """

    # Arrange
    input_string = "a"
    start_index = 0
    expected_output = False

    # Act
    actual_output = ParserHelper.is_character_at_index_whitespace(
        input_string, start_index
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_not_whitespace_with_empty_string():
    """
    Make sure that an empty string is handled properly.
    """

    # Arrange
    input_string = ""
    start_index = 0
    expected_output = False

    # Act
    actual_output = ParserHelper.is_character_at_index_not_whitespace(
        input_string, start_index
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_not_whitespace_with_low_index():
    """
    Make sure that a string with a low index is handled properly.
    """

    # Arrange
    input_string = "this is a test"
    start_index = -1
    expected_output = False

    # Act
    actual_output = ParserHelper.is_character_at_index_not_whitespace(
        input_string, start_index
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_not_whitespace_with_high_index():
    """
    Make sure that a string with a high index is handled properly.
    """

    # Arrange
    input_string = "this is a test"
    start_index = len(input_string)
    expected_output = False

    # Act
    actual_output = ParserHelper.is_character_at_index_not_whitespace(
        input_string, start_index
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_not_whitespace_with_whitespace():
    """
    Make sure that a string with whitespace at the index is handled properly.
    """

    # Arrange
    input_string = " "
    start_index = 0
    expected_output = False

    # Act
    actual_output = ParserHelper.is_character_at_index_not_whitespace(
        input_string, start_index
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_not_whitespace_with_whitespace_at_end():
    """
    Make sure that a string with whitespace at the index is handled properly.
    """

    # Arrange
    input_string = "this is a test "
    start_index = len(input_string) - 1
    expected_output = False

    # Act
    actual_output = ParserHelper.is_character_at_index_not_whitespace(
        input_string, start_index
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_not_whitespace_without_whitespace():
    """
    Make sure that a string with whitespace at the index is handled properly.
    """

    # Arrange
    input_string = "a"
    start_index = 0
    expected_output = True

    # Act
    actual_output = ParserHelper.is_character_at_index_not_whitespace(
        input_string, start_index
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_one_of_with_empty_string():
    """
    Make sure that an empty string is handled properly.
    """

    # Arrange
    input_string = ""
    start_index = 0
    valid_characters = "abc"
    expected_output = False

    # Act
    actual_output = ParserHelper.is_character_at_index_one_of(
        input_string, start_index, valid_characters
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_one_of_with_low_index():
    """
    Make sure that a string with a low index is handled properly.
    """

    # Arrange
    input_string = "this is a test"
    start_index = -1
    valid_characters = "abc"
    expected_output = False

    # Act
    actual_output = ParserHelper.is_character_at_index_one_of(
        input_string, start_index, valid_characters
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_one_of_with_high_index():
    """
    Make sure that a string with a high index is handled properly.
    """

    # Arrange
    input_string = "this is a test"
    start_index = len(input_string)
    valid_characters = "abc"
    expected_output = False

    # Act
    actual_output = ParserHelper.is_character_at_index_one_of(
        input_string, start_index, valid_characters
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_one_of_with_whitespace():
    """
    Make sure that a string with one of the characters present at the index is handled properly.
    """

    # Arrange
    input_string = "a"
    start_index = 0
    valid_characters = "abc"
    expected_output = True

    # Act
    actual_output = ParserHelper.is_character_at_index_one_of(
        input_string, start_index, valid_characters
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_one_of_with_whitespace2():
    """
    Make sure that a string with another one of the characters present at the index is handled properly.
    """

    # Arrange
    input_string = "c"
    start_index = 0
    valid_characters = "abc"
    expected_output = True

    # Act
    actual_output = ParserHelper.is_character_at_index_one_of(
        input_string, start_index, valid_characters
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_one_of_with_character_at_end():
    """
    Make sure that a string with one of the characters at the index is handled properly.
    """

    # Arrange
    input_string = "this is a test!"
    start_index = len(input_string) - 1
    valid_characters = "abc!"
    expected_output = True

    # Act
    actual_output = ParserHelper.is_character_at_index_one_of(
        input_string, start_index, valid_characters
    )

    # Assert
    assert expected_output == actual_output


def test_is_character_at_index_one_of_without_whitespace():
    """
    Make sure that a string without any characters at the index is handled properly.
    """

    # Arrange
    input_string = "this is a test"
    start_index = 0
    valid_characters = "abc"
    expected_output = False

    # Act
    actual_output = ParserHelper.is_character_at_index_one_of(
        input_string, start_index, valid_characters
    )

    # Assert
    assert expected_output == actual_output
