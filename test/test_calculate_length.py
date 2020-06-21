"""
Tests for the calculate_length function
"""
from pymarkdown.parser_helper import ParserHelper


def test_calculate_length_empty_string():
    """
    Make sure that an empty string is handled properly.
    """

    # Arrange
    input_string = ""
    expected_output = 0

    # Act
    actual_output = ParserHelper.calculate_length(input_string)

    # Assert
    assert expected_output == actual_output


def test_calculate_length_single_space():
    """
    Make sure that a string with a single space is handled properly.
    """

    # Arrange
    input_string = " "
    expected_output = 1

    # Act
    actual_output = ParserHelper.calculate_length(input_string)

    # Assert
    assert expected_output == actual_output


def test_calculate_length_multiple_spaces():
    """
    Make sure that a string with multiple spaces is handled properly.
    """

    # Arrange
    for i in range(1, 10):
        input_string = "".rjust(i, " ")
        expected_output = i

        # Act
        actual_output = ParserHelper.calculate_length(input_string)

        # Assert
        assert expected_output == actual_output


def test_calculate_length_single_tab():
    """
    Make sure that a string with a single tab is handled properly.
    """

    # Arrange
    input_string = "\t"
    expected_output = 4

    # Act
    actual_output = ParserHelper.calculate_length(input_string)

    # Assert
    assert expected_output == actual_output


def test_calculate_length_multiple_tabs():
    """
    Make sure that a string with multiple tabs is handled properly.
    """

    # Arrange
    for i in range(1, 10):
        input_string = "".rjust(i, "\t")
        expected_output = i * 4

        # Act
        actual_output = ParserHelper.calculate_length(input_string)

        # Assert
        assert expected_output == actual_output


def test_calculate_length_space_then_tab():
    """
    Make sure that a string with a single space then a tab is handled properly.
    """

    # Arrange
    input_string = " \t"
    expected_output = 4

    # Act
    actual_output = ParserHelper.calculate_length(input_string)

    # Assert
    assert expected_output == actual_output


def test_calculate_length_space_then_tab_twice():
    """
    Make sure that a string with a single space then a tab (twice) is handled properly.
    """

    # Arrange
    input_string = " \t"
    input_string += input_string
    expected_output = 8

    # Act
    actual_output = ParserHelper.calculate_length(input_string)

    # Assert
    assert expected_output == actual_output


def test_calculate_length_double_space_then_tab():
    """
    Make sure that a string with two spaces then a tab is handled properly.
    """

    # Arrange
    input_string = "  \t"
    expected_output = 4

    # Act
    actual_output = ParserHelper.calculate_length(input_string)

    # Assert
    assert expected_output == actual_output


def test_calculate_length_triple_space_then_tab():
    """
    Make sure that a string with three spaces then a tab is handled properly.
    """

    # Arrange
    input_string = "   \t"
    expected_output = 4

    # Act
    actual_output = ParserHelper.calculate_length(input_string)

    # Assert
    assert expected_output == actual_output


def test_calculate_length_tab_after_0_index_start():
    """
    Make sure that a string with a tab is handled properly after a start of 0.
    """

    # Arrange
    input_string = "\t"
    start_index = 0
    expected_output = 4

    # Act
    actual_output = ParserHelper.calculate_length(input_string, start_index)

    # Assert
    assert expected_output == actual_output


def test_calculate_length_tab_after_1_index_start():
    """
    Make sure that a string with a tab is handled properly after a start of 1.
    Note that with a start of 1, a tab moves it to the next tab stop at 4, specifying
    that 3 space characters should be added.
    """

    # Arrange
    input_string = "\t"
    start_index = 1
    expected_output = 3

    # Act
    actual_output = ParserHelper.calculate_length(input_string, start_index)

    # Assert
    assert expected_output == actual_output


def test_calculate_length_tab_after_2_index_start():
    """
    Make sure that a string with a tab is handled properly after a start of 2.
    Note that with a start of 2, a tab moves it to the next tab stop at 4, specifying
    that 2 space characters should be added.
    """

    # Arrange
    input_string = "\t"
    start_index = 2
    expected_output = 2

    # Act
    actual_output = ParserHelper.calculate_length(input_string, start_index)

    # Assert
    assert expected_output == actual_output


def test_calculate_length_tab_after_3_index_start():
    """
    Make sure that a string with a tab is handled properly after a start of 3.
    Note that with a start of 3, a tab moves it to the next tab stop at 4, specifying
    that 1 space characters should be added.
    """

    # Arrange
    input_string = "\t"
    start_index = 3
    expected_output = 1

    # Act
    actual_output = ParserHelper.calculate_length(input_string, start_index)

    # Assert
    assert expected_output == actual_output


def test_calculate_length_tab_after_4_index_start():
    """
    Make sure that a string with a tab is handled properly after a start of 4.
    Note that with a start of 4, a tab moves it to the next tab stop at 8, specifying
    that 4 space characters should be added.
    """

    # Arrange
    input_string = "\t"
    start_index = 4
    expected_output = 4

    # Act
    actual_output = ParserHelper.calculate_length(input_string, start_index)

    # Assert
    assert expected_output == actual_output
