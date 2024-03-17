"""
Tests for the find_nth_occurrence function.
"""

from pymarkdown.general.parser_helper import ParserHelper


def test_get_replacement_indices_none():
    """
    TBD
    """

    # Arrange
    search_in = "abc"
    start_index = 0

    # Act
    start_index, middle_index, end_index = ParserHelper.get_replacement_indices(
        search_in, start_index
    )

    # Assert
    assert start_index == -1
    assert middle_index == -1
    assert end_index == -1


def test_get_replacement_indices_valid():
    """
    TBD
    """

    # Arrange
    search_in = "abc" + ParserHelper.create_replacement_markers("\t", "tab") + "def"
    start_index = 0

    # Act
    start_index, middle_index, end_index = ParserHelper.get_replacement_indices(
        search_in, start_index
    )

    # Assert
    assert start_index == 3
    assert middle_index == 5
    assert end_index == 9


def test_get_replacement_indices_only_start():
    """
    TBD
    """

    # Arrange
    search_in = "abc\adef"
    start_index = 0

    # Act
    start_index, middle_index, end_index = ParserHelper.get_replacement_indices(
        search_in, start_index
    )

    # Assert
    assert start_index == 3
    assert middle_index == -1
    assert end_index == -1


def test_get_replacement_indices_only_start_and_middle():
    """
    TBD
    """

    # Arrange
    search_in = "abc\a\t\adef"
    start_index = 0

    # Act
    start_index, middle_index, end_index = ParserHelper.get_replacement_indices(
        search_in, start_index
    )

    # Assert
    assert start_index == 3
    assert middle_index == 5
    assert end_index == -1
