"""
Tests for the functions that deal with parsing of html tags.
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown


def test_empty_tag_name():
    """
    Make sure to test an empty tag name.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = ""
    expected_is_valid = False

    # Act
    actual_is_valid = tokenizer.is_valid_tag_name(input_tag_name)

    # Assert
    assert expected_is_valid == actual_is_valid


def test_simple_alphabetic_tag_name():
    """
    Make sure to test a simple valid tag name.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "script"
    expected_is_valid = True

    # Act
    actual_is_valid = tokenizer.is_valid_tag_name(input_tag_name)

    # Assert
    assert expected_is_valid == actual_is_valid


def test_simple_alphanumeric_tag_name():
    """
    Make sure to test a simple valid tag name.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "h2"
    expected_is_valid = True

    # Act
    actual_is_valid = tokenizer.is_valid_tag_name(input_tag_name)

    # Assert
    assert expected_is_valid == actual_is_valid


def test_simple_upper_case_alphanumeric_tag_name():
    """
    Make sure to test a simple valid tag name.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "H2"
    expected_is_valid = True

    # Act
    actual_is_valid = tokenizer.is_valid_tag_name(input_tag_name)

    # Assert
    assert expected_is_valid == actual_is_valid


def test_simple_mixed_case_alphanumeric_tag_name():
    """
    Make sure to test a simple valid tag name.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "ScRiPt"
    expected_is_valid = True

    # Act
    actual_is_valid = tokenizer.is_valid_tag_name(input_tag_name)

    # Assert
    assert expected_is_valid == actual_is_valid


def test_simple_dashed_tag_name():
    """
    Make sure to test a simple valid tag name with a dash.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "x-new"
    expected_is_valid = True

    # Act
    actual_is_valid = tokenizer.is_valid_tag_name(input_tag_name)

    # Assert
    assert expected_is_valid == actual_is_valid


def test_simple_dashed_bad_name():
    """
    Make sure to test a simple invalid tag name.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "x_new"
    expected_is_valid = False

    # Act
    actual_is_valid = tokenizer.is_valid_tag_name(input_tag_name)

    # Assert
    assert expected_is_valid == actual_is_valid


def test_simple_attribute_name():
    """
    Make sure to test a simple attribute name.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_text = "<a href='foo'>"
    start_index = 3
    expected_resultant_index = 7

    # Act
    actual_resultant_index = tokenizer.extract_html_attribute_name(
        input_tag_text, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_dashed_attribute_name():
    """
    Make sure to test an attribute name with a dash.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_text = "<form accept-charset='foo'>"
    start_index = 6
    expected_resultant_index = 20

    # Act
    actual_resultant_index = tokenizer.extract_html_attribute_name(
        input_tag_text, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_coloned_attribute_name():
    """
    Make sure to test an attribute name with a colon.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_text = "<meta http:equiv='foo'>"
    start_index = 6
    expected_resultant_index = 16

    # Act
    actual_resultant_index = tokenizer.extract_html_attribute_name(
        input_tag_text, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_invalid_attribute_name_start():
    """
    Make sure to test an attribute name that has an invalid start character
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_text = "<meta -http='foo'>"
    start_index = 6
    expected_resultant_index = -1

    # Act
    actual_resultant_index = tokenizer.extract_html_attribute_name(
        input_tag_text, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_invalid_attribute_name():
    """
    Make sure to test an attribute name that is invalid.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_text = "<meta http*equiv='foo'>"
    start_index = 6
    expected_resultant_index = -1

    # Act
    actual_resultant_index = tokenizer.extract_html_attribute_name(
        input_tag_text, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_attribute_name_runs_out_of_string():
    """
    Make sure to test an attribute name that runs out of space in the string.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_text = "<meta httpequiv"
    start_index = 6
    expected_resultant_index = -1

    # Act
    actual_resultant_index = tokenizer.extract_html_attribute_name(
        input_tag_text, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_no_attribute_name_following_value():
    """
    Make sure to test an attribute name without a following attribute value.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "<meta http:equiv>"
    start_index = 16
    expected_resultant_index = 16

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_no_attribute_name_following_value_and_no_close():
    """
    Make sure to test an attribute name without a following attribute value and no close bracket.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "<meta http:equiv"
    start_index = 16
    expected_resultant_index = len(input_tag_name)

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_attribute_name_equals_sign_only():
    """
    Make sure to test an attribute name with a following equal sign only.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "<meta http:equiv="
    start_index = 16
    expected_resultant_index = -1

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_attribute_name_equals_sign_and_close():
    """
    Make sure to test an attribute name with a following equal sign and a close.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "<meta http:equiv=>"
    start_index = 16
    expected_resultant_index = -1

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_double_quoted_attribute_name_following_value_empty():
    """
    Make sure to test an attribute name with a following double quoted value that is empty.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = '<meta http:equiv="">'
    start_index = 16
    expected_resultant_index = 19

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_double_quoted_attribute_name_following_value_not_empty():
    """
    Make sure to test an attribute name with a following double quoted value that is not empty.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = '<meta http:equiv="foo">'
    start_index = 16
    expected_resultant_index = 22

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_double_quoted_attribute_name_following_value_and_whitespace_around():
    """
    Make sure to test an attribute name with a following double quoted value with whitespace around it.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = '<meta http:equiv = "foo">'
    start_index = 16
    expected_resultant_index = 24

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_double_quoted_attribute_name_following_value_and_no_close_quotes():
    """
    Make sure to test an attribute name with a following double quoted value that has no close quotes.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = '<meta http:equiv="foo'
    start_index = 16
    expected_resultant_index = -1

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_double_quoted_attribute_name_following_value_and_no_close():
    """
    Make sure to test an attribute name with a following double quoted value that has no close tag.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = '<meta http:equiv="foo"'
    start_index = 16
    expected_resultant_index = len(input_tag_name)

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_single_quoted_attribute_name_following_value_empty():
    """
    Make sure to test an attribute name with a following single quoted value that is empty.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "<meta http:equiv=''>"
    start_index = 16
    expected_resultant_index = 19

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_single_quoted_attribute_name_following_value_not_empty():
    """
    Make sure to test an attribute name with a following single quoted value that is not empty.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "<meta http:equiv='foo'>"
    start_index = 16
    expected_resultant_index = 22

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_single_quoted_attribute_name_following_value_and_whitespace_around():
    """
    Make sure to test an attribute name with a following single quoted value with whitespace around it.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "<meta http:equiv = 'foo'>"
    start_index = 16
    expected_resultant_index = 24

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_single_quoted_attribute_name_following_value_and_no_close_quotes():
    """
    Make sure to test an attribute name with a following single quoted value that has no close quotes.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "<meta http:equiv='foo"
    start_index = 16
    expected_resultant_index = -1

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_single_quoted_attribute_name_following_value_and_no_close():
    """
    Make sure to test an attribute name with a following single quoted value that has no close tag.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "<meta http:equiv='foo'"
    start_index = 16
    expected_resultant_index = len(input_tag_name)

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_non_quoted_attribute_name_following_value():
    """
    Make sure to test an attribute name with a following non-quoted value that is not empty.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "<meta http:equiv=abc>"
    start_index = 16
    expected_resultant_index = 20

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index


def test_non_quoted_attribute_name_following_value_empty():
    """
    Make sure to test an attribute name with a following non-quoted value that is empty.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    input_tag_name = "<meta http:equiv=="
    start_index = 16
    expected_resultant_index = -1

    # Act
    actual_resultant_index = tokenizer.extract_optional_attribute_value(
        input_tag_name, start_index
    )

    # Assert
    assert expected_resultant_index == actual_resultant_index
