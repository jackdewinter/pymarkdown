"""
Tests for the detabisty_string functions.
"""

from pymarkdown.tab_helper import TabHelper


def test_detabify_string_simple_case():
    """
    xxx
    """

    # Arrange
    line_with_tabs = "\torig"
    additional_start_delta = 0
    detabified_line_to_match = "    orig"

    # Act
    adjusted_line = TabHelper.detabify_string(line_with_tabs, additional_start_delta)

    # Assert
    assert detabified_line_to_match == adjusted_line


def test_detabify_string_simple_case_with_offset():
    """
    xxx
    """

    # Arrange
    line_with_tabs = "\torig"
    additional_start_delta = 2
    detabified_line_to_match = "  orig"

    # Act
    adjusted_line = TabHelper.detabify_string(line_with_tabs, additional_start_delta)

    # Assert
    assert detabified_line_to_match == adjusted_line


def test_detabify_string_simple_case_with_spaces():
    """
    xxx
    """

    # Arrange
    line_with_tabs = "\t    "
    additional_start_delta = 0
    detabified_line_to_match = "        "

    # Act
    adjusted_line = TabHelper.detabify_string(line_with_tabs, additional_start_delta)

    # Assert
    assert detabified_line_to_match == adjusted_line


def test_detabify_string_simple_case_with_spaces_and_offset():
    """
    xxx
    """

    # Arrange
    line_with_tabs = "\t    "
    additional_start_delta = 2
    detabified_line_to_match = "      "

    # Act
    adjusted_line = TabHelper.detabify_string(line_with_tabs, additional_start_delta)

    # Assert
    assert detabified_line_to_match == adjusted_line


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
    adjusted_original_line, actual_index, _ = TabHelper.find_detabify_string(
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
    # Act
    adjusted_original_line, actual_index, _ = TabHelper.find_detabify_string(
        line_with_tabs, detabified_line_to_match
    )

    # Assert
    assert actual_index == expected_index
    assert adjusted_original_line is None
