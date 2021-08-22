"""
Module to provide tests related to the MD007 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md007_bad_configuration_indent():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md007.indent=bad",
        "--strict-config",
        "scan",
        "test/resources/rules/md007/good_list_indentation.md",
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
def test_md007_bad_configuration_indent_bad():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md007.indent=$#5",
        "--strict-config",
        "scan",
        "test/resources/rules/md007/good_list_indentation.md",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/good_list_indentation.md",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_list_indentation_level_0.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_list_indentation_level_0.md:3:2: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_list_indentation_level_1.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_list_indentation_level_1.md:4:4: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_list_indentation_level_2.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_list_indentation_level_2.md:5:6: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "test/resources/rules/md007/good_list_indentation_in_block_quote.md",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/good_list_indentation_in_double_block_quote.md",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/good_unordered_list_in_ordered_list.md",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_unordered_list_in_ordered_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_unordered_list_in_ordered_list.md:2:6: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_level_1_unordered_list_in_ordered_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_level_1_unordered_list_in_ordered_list.md:3:8: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/good_unordered_list_in_double_ordered_list.md",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_unordered_list_in_double_ordered_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_unordered_list_in_double_ordered_list.md:3:8: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/good_unordered_ordered_unordere_ordered_unordered.md",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_unordered_bad_ordered_unordered_ordered_unordered.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_unordered_bad_ordered_unordered_ordered_unordered.md:1:2: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_unordered_ordered_unordered_bad_ordered_unordered.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_unordered_ordered_unordered_bad_ordered_unordered.md:3:7: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_unordered_ordered_unordered_ordered_unordered_bad.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_unordered_ordered_unordered_ordered_unordered_bad.md:5:12: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_list_indentation_in_block_quote_level_0.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_list_indentation_in_block_quote_level_0.md:3:4: "
        + "MD007: Unordered list indentation "
        + "[Expected: 0, Actual=1] (ul-indent)\n"
        + "test/resources/rules/md007/bad_list_indentation_in_block_quote_level_0.md:4:6: "
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
def test_md007_bad_list_in_block_quote_after_text():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_list_in_block_quote_after_text.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_list_in_block_quote_after_text.md:4:6: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_list_in_block_quote_after_atx_heading.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_list_in_block_quote_after_atx_heading.md:4:6: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_list_in_block_quote_after_thematic_break.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_list_in_block_quote_after_thematic_break.md:6:6: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_list_in_block_quote_after_setext_heading.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_list_in_block_quote_after_setext_heading.md:5:6: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_list_in_block_quote_after_html_block.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_list_in_block_quote_after_html_block.md:6:6: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_list_in_block_quote_after_fenced_block.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_list_in_block_quote_after_fenced_block.md:6:6: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_list_in_block_quote_after_indented_block.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_list_in_block_quote_after_indented_block.md:4:6: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_list_in_block_quote_after_link_reference_definition.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_list_in_block_quote_after_link_reference_definition.md:4:6: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/bad_list_in_block_quote_after_other_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md007/bad_list_in_block_quote_after_other_list.md:4:6: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md007/good_unordered_list_elements.md",
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
def test_md007_good_list_indentation_by_four():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md007.indent=$#4",
        "scan",
        "test/resources/rules/md007/good_list_indentation_by_four.md",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md007.start_indented=$!True",
        "scan",
        "test/resources/rules/md007/good_list_indentation_with_start.md",
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
