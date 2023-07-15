"""
Module to provide tests related to the MD007 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md007_bad_configuration_indent():
    """
    Test to verify that a configuration error is thrown when supplying the
    indent value with a string that is not an integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "good_list_indentation.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md007.indent=bad",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md007.indent' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_configuration_start_indented():
    """
    Test to verify that a configuration error is thrown when supplying the
    start_indented value with a value that is not a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "good_list_indentation.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md007.start_indented=bad",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md007.start_indented' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_configuration_indent_bad():
    """
    Test to verify that a configuration error is thrown when supplying the
    indent value with a string that is not a valid integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "good_list_indentation.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md007.indent=$#5",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md007.indent' is not valid: Allowable values are between 2 and 4."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_good_list_indentation_x():
    """
    Test to make sure this rule does not trigger with a document that
    only has the required spaces after the list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "good_list_indentation.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_list_indentation_level_0():
    """
    Test to make sure this rule does trigger with a document that
    has the extra spaces after the level 1 list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "bad_list_indentation_level_0.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:2: "
        + "MD007: Unordered list indentation "
        + "[Expected: 0, Actual=1] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_list_indentation_level_1():
    """
    Test to make sure this rule does trigger with a document that
    has the extra spaces after the level 2 list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "bad_list_indentation_level_1.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:4: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_list_indentation_level_2():
    """
    Test to make sure this rule does trigger with a document that
    has the extra spaces after the level 3 list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "bad_list_indentation_level_2.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:6: "
        + "MD007: Unordered list indentation "
        + "[Expected: 4, Actual=5] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_good_list_indentation_in_block_quote():
    """
    Test to make sure this rule does not trigger with a document that
    only has the required spaces after the list item, but in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "good_list_indentation_in_block_quote.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_good_list_indentation_in_double_block_quote():
    """
    Test to make sure this rule does not trigger with a document that
    only has the required spaces after the list item, but in a doulbe block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "good_list_indentation_in_double_block_quote.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_good_unordered_list_in_ordered_list():
    """
    Test to make sure this rule does not trigger with a document that
    only has the required spaces after the list item, but in an ordered list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "good_unordered_list_in_ordered_list.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md030",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_unordered_list_in_ordered_list():
    """
    Test to make sure this rule does trigger with a document that has
    an unordered list starting with extra spaces inside of an ordered list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "bad_unordered_list_in_ordered_list.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md030",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:6: "
        + "MD007: Unordered list indentation "
        + "[Expected: 5, Actual=6] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_level_1_unordered_list_in_ordered_list():
    """
    Test to make sure this rule does trigger with a document that has
    two nested unordered lists, the inner one starting with extra spaces,
    inside of an ordered list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_level_1_unordered_list_in_ordered_list.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md030",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:8: "
        + "MD007: Unordered list indentation "
        + "[Expected: 7, Actual=8] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_good_unordered_list_in_double_ordered_list():
    """
    Test to make sure this rule does not trigger with a document that has
    two nested ordered lists with a good unordered list with them that
    does not have extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "good_unordered_list_in_double_ordered_list.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_unordered_list_in_double_ordered_list():
    """
    Test to make sure this rule does trigger with a document that has
    two nested ordered lists with a bad unordered list with them that
    does have extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_unordered_list_in_double_ordered_list.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:8: "
        + "MD007: Unordered list indentation "
        + "[Expected: 7, Actual=8] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_good_unordered_ordered_unordere_ordered_unordered():
    """
    Test to make sure this rule does not trigger with a document that has
    nested ordered lists and unordered lists, with no extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "good_unordered_ordered_unordere_ordered_unordered.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_unordered_bad_ordered_unordered_ordered_unordered():
    """
    Test to make sure this rule does trigger with a document that has
    nested ordered lists and unordered lists, with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_unordered_bad_ordered_unordered_ordered_unordered.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:2: "
        + "MD007: Unordered list indentation "
        + "[Expected: 0, Actual=1] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_unordered_ordered_unordered_bad_ordered_unordered():
    """
    Test to make sure this rule does trigger with a document that has
    nested ordered lists and unordered lists, with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_unordered_ordered_unordered_bad_ordered_unordered.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:7: "
        + "MD007: Unordered list indentation "
        + "[Expected: 6, Actual=7] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_unordered_ordered_unordered_ordered_unordered_bad():
    """
    Test to make sure this rule does trigger with a document that has
    nested ordered lists and unordered lists, with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_unordered_ordered_unordered_ordered_unordered_bad.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:12: "
        + "MD007: Unordered list indentation "
        + "[Expected: 11, Actual=12] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_list_indentation_in_block_quote_level_0():
    """
    Test to make sure this rule does trigger with a document that has
    nested unordered lists within a block quote, with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_list_indentation_in_block_quote_level_0.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md027",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:4: "
        + "MD007: Unordered list indentation "
        + "[Expected: 0, Actual=1] (ul-indent)\n"
        + f"{source_path}:4:6: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)\n"
        + f"{source_path}:5:8: "
        + "MD007: Unordered list indentation "
        + "[Expected: 4, Actual=5] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_list_in_block_quote_after_text():
    """
    Test to make sure this rule does trigger with a document that has
    a bad nested unordered lists after a text block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "bad_list_in_block_quote_after_text.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:6: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_list_in_block_quote_after_atx_heading():
    """
    Test to make sure this rule does trigger with a document that has
    a bad nested unordered lists after an Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_list_in_block_quote_after_atx_heading.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:6: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_list_in_block_quote_after_thematic_break():
    """
    Test to make sure this rule does trigger with a document that has
    a bad nested unordered lists after a thematic break.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_list_in_block_quote_after_thematic_break.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:6:6: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_list_in_block_quote_after_setext_heading():
    """
    Test to make sure this rule does trigger with a document that has
    a bad nested unordered lists after a SetExt Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_list_in_block_quote_after_setext_heading.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:6: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_list_in_block_quote_after_html_block():
    """
    Test to make sure this rule does trigger with a document that has
    a bad nested unordered lists after a HTML block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_list_in_block_quote_after_html_block.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:6:6: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_list_in_block_quote_after_fenced_block():
    """
    Test to make sure this rule does trigger with a document that has
    a bad nested unordered lists after a fenced code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_list_in_block_quote_after_fenced_block.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:6:6: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_list_in_block_quote_after_indented_block():
    """
    Test to make sure this rule does trigger with a document that has
    a bad nested unordered lists after an indented code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_list_in_block_quote_after_indented_block.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:6: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_list_in_block_quote_after_link_reference_definition():
    """
    Test to make sure this rule does trigger with a document that has
    a bad nested unordered lists after a link reference definition.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_list_in_block_quote_after_link_reference_definition.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:6: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_list_in_block_quote_after_other_list():
    """
    Test to make sure this rule does trigger with a document that has
    a bad nested unordered lists after another list
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md007",
        "bad_list_in_block_quote_after_other_list.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:6: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_good_unordered_list_elements():
    """
    Test to make sure this rule does not trigger with a document that has
    many nested unordered lists, each one properly indented.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "good_unordered_list_elements.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_unordered_list_elements():
    """
    Test to make sure this rule does trigger with a document that has
    many nested unordered lists, most of them improperly indented.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "bad_unordered_list_elements.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md005",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:2: "
        + "MD007: Unordered list indentation "
        + "[Expected: 0, Actual=1] (ul-indent)\n"
        + f"{source_path}:4:2: "
        + "MD007: Unordered list indentation "
        + "[Expected: 0, Actual=1] (ul-indent)\n"
        + f"{source_path}:5:4: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)\n"
        + f"{source_path}:6:4: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)\n"
        + f"{source_path}:7:7: "
        + "MD007: Unordered list indentation "
        + "[Expected: 4, Actual=6] (ul-indent)\n"
        + f"{source_path}:8:4: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=3] (ul-indent)\n"
        + f"{source_path}:9:5: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=4] (ul-indent)\n"
        + f"{source_path}:10:5: "
        + "MD007: Unordered list indentation "
        + "[Expected: 2, Actual=4] (ul-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_good_list_indentation_by_four():
    """
    Test to make sure this rule does not trigger with a document that has
    each list indented by 4, but configuration to support it.

    This function shadows
    test_api_config_with_good_integer_property
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "good_list_indentation_by_four.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md007.indent=$#4",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_good_list_indentation_with_start():
    """
    Test to make sure this rule does not trigger with a document that has
    the level 1 list indented, due to configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "good_list_indentation_with_start.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md007.start_indented=$!True",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_issue_301():
    """
    Test to make sure that the reported issue 301 does not happen.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join("test", "resources", "rules", "md007", "issue-301.md")
    supplied_arguments = [
        "--set",
        "plugins.md007.indent=$#4",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:7:5: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
