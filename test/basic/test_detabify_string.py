"""
Tests for the detabisty_string functions.
"""

from pymarkdown.parser_helper import ParserHelper


def test_find_detabify_string_simple_case():
    """
    xxx
    """

    # Arrange
    line_with_tabs = "\torig"
    detabified_line_to_match = "    orig"

    expected_index = 0
    expected_adjusted_line = line_with_tabs

    # Act
    adjusted_original_line, actual_index = ParserHelper.find_detabify_string(
        line_with_tabs, detabified_line_to_match
    )

    # Assert
    assert actual_index == expected_index
    assert adjusted_original_line == expected_adjusted_line


def test_find_detabify_string_simple_case_x():
    """
    xxx
    """

    # Arrange
    line_with_tabs = "\torig"
    detabified_line_to_match = "   orig"

    expected_index = -1
    expected_adjusted_line = None

    # Act
    adjusted_original_line, actual_index = ParserHelper.find_detabify_string(
        line_with_tabs, detabified_line_to_match
    )

    # Assert
    assert actual_index == expected_index
    assert adjusted_original_line == expected_adjusted_line
