"""
Tests for the functions that deal with parsing of complete html tags.
"""
from pymarkdown.html_helper import HtmlHelper


def test_simple_complete_html_end_tag():
    """
    Make sure to test a simple complete html tag.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = ">"
    parse_index = 0
    expected_is_valid = True

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_end_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_simple_complete_html_end_tag_with_invalid_tag_name():
    """
    Make sure to test a simple complete html tag.
    """

    # Arrange
    input_tag_name = "a*b"
    string_to_parse = ">"
    parse_index = 0
    expected_is_valid = False

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_end_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_simple_complete_html_end_tag_with_whitespace():
    """
    Make sure to test a simple complete html tag with extra whitespace.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " >"
    parse_index = 0
    expected_is_valid = True

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_end_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_complete_html_end_tag_with_bad_attribute():
    """
    Make sure to test a complete html tag with a attribute specified (bad).
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " foo>"
    parse_index = 0
    expected_is_valid = False

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_end_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_complete_html_end_tag_with_no_more_string():
    """
    Make sure to test a complete html tag that isn't terminated.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = ""
    parse_index = 0
    expected_is_valid = False

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_end_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_simple_complete_html_start_tag_with_no_attributes():
    """
    Make sure to test a simple complete html start tag with no attributes.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = ">"
    parse_index = 0
    expected_is_valid = True

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_simple_complete_html_start_tag_with_bad_tag_name():
    """
    Make sure to test a simple complete html start tag with a bad tag name.
    """

    # Arrange
    input_tag_name = "a*b"
    string_to_parse = ">"
    parse_index = 0
    expected_is_valid = False

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_simple_complete_html_start_tag_with_no_attributes_and_whitespace():
    """
    Make sure to test a simple complete html start tag with no attributes and whitespace.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " >"
    parse_index = 0
    expected_is_valid = True

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_complete_html_start_tag_with_single_no_value_attributes():
    """
    Make sure to test a simple complete html start tag with a single attribute with no value.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show>"
    parse_index = 0
    expected_is_valid = True

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_complete_html_start_tag_with_invalidly_named_no_value_attributes():
    """
    Make sure to test a simple complete html start tag with a single attribute that has an invalid name.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " sh*ow>"
    parse_index = 0
    expected_is_valid = False

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_complete_html_start_tag_with_single_no_value_attributes_and_whitespace():
    """
    Make sure to test a simple complete html start tag with a single attribute with no value and whitespace.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show >"
    parse_index = 0
    expected_is_valid = True

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_complete_html_start_tag_with_single_attribute():
    """
    Make sure to test a simple complete html start tag with a single attribute.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show=1>"
    parse_index = 0
    expected_is_valid = True

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_complete_html_start_tag_with_single_attribute_with_bad_value():
    """
    Make sure to test a simple complete html start tag with a single attribute with bad value.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show=>"
    parse_index = 0
    expected_is_valid = False

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_complete_html_start_tag_with_single_attribute_with_whitespace():
    """
    Make sure to test a simple complete html start tag with a single attribute with whitespace.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show = '1' >"
    parse_index = 0
    expected_is_valid = True

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_complete_html_start_tag_with_multiple_attributes():
    """
    Make sure to test a simple complete html start tag with multiple attributes.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show=1 maximize=1 opacity='70'>"
    parse_index = 0
    expected_is_valid = True

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_complete_html_start_tag_with_self_closing_tag():
    """
    Make sure to test a simple complete html start tag with multiple attributes.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show/>"
    parse_index = 0
    expected_is_valid = True

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid


def test_complete_html_start_tag_with_normal_opening_tag():
    """
    Make sure to test a simple complete html start tag with multiple attributes.
    """

    # Arrange
    input_tag_name = "a"
    string_to_parse = " show>"
    parse_index = 0
    expected_is_valid = True

    # Act
    actual_is_valid = HtmlHelper.is_complete_html_start_tag(
        input_tag_name, string_to_parse, parse_index
    )

    # Assert
    assert expected_is_valid == actual_is_valid
