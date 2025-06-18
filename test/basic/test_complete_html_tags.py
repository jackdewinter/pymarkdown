"""
Tests for the functions that deal with parsing of complete html tags.
"""

from typing import Optional

from pymarkdown.html.html_helper import HtmlHelper


def test_simple_complete_html_end_tag() -> None:
    """
    Make sure to test a simple complete html tag.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = ">"
    parse_index = 0
    expected_is_valid = True

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_end_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 1


def test_simple_complete_html_end_tag_with_invalid_tag_name() -> None:
    """
    Make sure to test a simple complete html tag with an invalid tag name.
    """

    # Arrange
    input_tag_name = "a*b"
    string_to_parse = ">"
    parse_index = 0
    expected_is_valid = False

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_end_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 1


def test_simple_complete_html_end_tag_with_whitespace() -> None:
    """
    Make sure to test a simple complete html tag with extra whitespace.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " >"
    parse_index = 0
    expected_is_valid = True

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_end_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 2


def test_complete_html_end_tag_with_bad_attribute() -> None:
    """
    Make sure to test a complete html tag with an attribute specified (bad).
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " foo>"
    parse_index = 0
    expected_is_valid = False

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_end_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 2


def test_complete_html_end_tag_with_no_more_string() -> None:
    """
    Make sure to test a complete html tag that isn't terminated.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = ""
    parse_index = 0
    expected_is_valid = False

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_end_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 1


def test_simple_complete_html_start_tag_with_no_attributes() -> None:
    """
    Make sure to test a simple complete html start tag with no attributes.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = ">"
    parse_index: Optional[int] = 0
    expected_is_valid = True

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 1


def test_simple_complete_html_start_tag_with_bad_tag_name() -> None:
    """
    Make sure to test a simple complete html start tag with a bad tag name.
    """

    # Arrange
    input_tag_name = "a*b"
    string_to_parse = ">"
    parse_index: Optional[int] = 0
    expected_is_valid = False

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 1


def test_simple_complete_html_start_tag_with_no_attributes_and_whitespace() -> None:
    """
    Make sure to test a simple complete html start tag with no attributes and whitespace.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " >"
    parse_index: Optional[int] = 0
    expected_is_valid = True

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 2


def test_complete_html_start_tag_with_single_no_value_attributes() -> None:
    """
    Make sure to test a simple complete html start tag with a single attribute with no value.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show>"
    parse_index: Optional[int] = 0
    expected_is_valid = True

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 6


def test_complete_html_start_tag_with_invalidly_named_no_value_attributes() -> None:
    """
    Make sure to test a simple complete html start tag with a single attribute that has an invalid name.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " sh*ow>"
    parse_index: Optional[int] = 0
    expected_is_valid = False

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 1


def test_complete_html_start_tag_with_single_no_value_attributes_and_whitespace() -> (
    None
):
    """
    Make sure to test a simple complete html start tag with a single attribute with no value and whitespace.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show >"
    parse_index: Optional[int] = 0
    expected_is_valid = True

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 7


def test_complete_html_start_tag_with_single_attribute() -> None:
    """
    Make sure to test a simple complete html start tag with a single attribute.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show=1>"
    parse_index: Optional[int] = 0
    expected_is_valid = True

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 8


def test_complete_html_start_tag_with_single_attribute_with_bad_value() -> None:
    """
    Make sure to test a simple complete html start tag with a single attribute with bad value.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show=>"
    parse_index: Optional[int] = 0
    expected_is_valid = False

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 1


def test_complete_html_start_tag_with_single_attribute_with_whitespace() -> None:
    """
    Make sure to test a simple complete html start tag with a single attribute with whitespace.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show = '1' >"
    parse_index: Optional[int] = 0
    expected_is_valid = True

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 13


def test_complete_html_start_tag_with_multiple_attributes() -> None:
    """
    Make sure to test a simple complete html start tag with multiple attributes.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show=1 maximize=1 opacity='70'>"
    parse_index: Optional[int] = 0
    expected_is_valid = True

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 32


def test_complete_html_start_tag_with_self_closing_tag() -> None:
    """
    Make sure to test a simple complete html start tag with multiple attributes.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show/>"
    parse_index: Optional[int] = 0
    expected_is_valid = True

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 7


def test_complete_html_start_tag_with_normal_opening_tag() -> None:
    """
    Make sure to test a simple complete html start tag with multiple attributes.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show>"
    parse_index: Optional[int] = 0
    expected_is_valid = True

    # Act
    assert parse_index is not None
    actual_is_valid, parse_index = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
    assert parse_index == 6
