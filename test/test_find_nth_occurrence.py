"""
Tests for the find_nth_occurrence function.
"""
from pymarkdown.parser_helper import ParserHelper


def test_find_nth_simple_positive():
    """
    Make sure that...
    """

    # Arrange
    search_in = "abc"
    search_for = "abc"
    nth = 1
    expected_output = 0

    # Act
    actual_output = ParserHelper.find_nth_occurrence(search_in, search_for, nth)

    # Assert
    assert expected_output == actual_output


def test_find_nth_simple_negative():
    """
    Make sure that...
    """

    # Arrange
    search_in = "abc"
    search_for = "bcd"
    nth = 1
    expected_output = -1

    # Act
    actual_output = ParserHelper.find_nth_occurrence(search_in, search_for, nth)

    # Assert
    assert expected_output == actual_output


def test_find_nth_double_positive():
    """
    Make sure that...
    """

    # Arrange
    search_in = "abc def abc"
    search_for = "abc"
    nth = 2
    expected_output = 8

    # Act
    actual_output = ParserHelper.find_nth_occurrence(search_in, search_for, nth)

    # Assert
    assert expected_output == actual_output


def test_find_nth_double_negative():
    """
    Make sure that...
    """

    # Arrange
    search_in = "abc"
    search_for = "abc def def"
    nth = 2
    expected_output = -1

    # Act
    actual_output = ParserHelper.find_nth_occurrence(search_in, search_for, nth)

    # Assert
    assert expected_output == actual_output


def test_find_nth_overlap_positive():
    """
    Make sure that...
    """

    # Arrange
    search_in = "abababababababa"
    search_for = "aba"
    nth = 4
    expected_output = 6

    # Act
    actual_output = ParserHelper.find_nth_occurrence(search_in, search_for, nth)

    # Assert
    assert expected_output == actual_output
