"""
Module to provide tests related to the MD022 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

from .utils import write_temporary_configuration

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md022_bad_proper_line_spacing_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that have proper default
    spacing both before and after the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/proper_line_spacing_atx.md",
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
def test_md022_good_proper_line_spacing_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has setext headings that have proper default
    spacing both before and after the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/proper_line_spacing_setext.md",
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
def test_md022_bad_no_line_spacing_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing both before and after the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_atx.md:1:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_atx.md:4:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_atx.md:4:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_atx_in_same_block_quote():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing both before and after the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_atx_in_same_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_atx_in_same_block_quote.md:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_atx_in_same_block_quote.md:4:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_atx_in_same_block_quote.md:4:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_atx_in_same_list_item():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing both before and after the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_atx_in_same_list_item.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_atx_in_same_list_item.md:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_atx_in_same_list_item.md:4:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_atx_in_same_list_item.md:4:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_atx_in_different_list_items():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing both before and after the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_atx_in_different_list_items.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_atx_in_different_list_items.md:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_atx_in_different_list_items.md:4:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_atx_in_different_list_items.md:4:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_before_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing before the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_before_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_before_atx.md:5:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_before_atx_in_same_list_item():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing before the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_before_atx_in_same_list_item.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_before_atx_in_same_list_item.md:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_before_atx_in_different_list_items():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing before the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_before_atx_in_different_list_items.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_before_atx_in_different_list_items.md:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_before_atx_in_same_block_quote():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing before the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_before_atx_in_same_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_before_atx_in_same_block_quote.md:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_before_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing before the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_before_setext.md",
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
def test_md022_bad_no_line_spacing_after_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing after the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_after_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_after_atx.md:1:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_after_atx.md:5:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_after_atx_in_same_list_item():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing after the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_after_atx_in_same_list_item.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_after_atx_in_same_list_item.md:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_after_atx_in_same_list_item.md:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_after_atx_in_same_block_quote():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing after the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_after_atx_in_same_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_after_atx_in_same_block_quote.md:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_after_atx_in_same_block_quote.md:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_after_atx_in_different_list_items():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing after the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_after_atx_in_different_list_items.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_after_atx_in_different_list_items.md:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_after_atx_in_different_list_items.md:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_after_atx_in_different_block_quotes():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing after the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_after_atx_in_different_block_quotes.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_after_atx_in_different_block_quotes.md:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_after_atx_in_different_block_quotes.md:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_atx_with_html_and_good_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do have proper
    default spacing before and after the heading, surrounded by html blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/atx_with_html_and_good_line_spacing.md",
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
def test_md022_bad_atx_with_html_and_bad_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing before and after the heading, surrounded by html blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/atx_with_html_and_bad_line_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/atx_with_html_and_bad_line_spacing.md:3:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/atx_with_html_and_bad_line_spacing.md:8:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_atx_with_paragraph_and_good_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do have proper
    default spacing before and after the heading, surrounded by html blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/atx_with_paragraph_and_good_line_spacing.md",
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
def test_md022_bad_atx_with_paragraph_and_bad_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing before and after the heading, surrounded by html blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/atx_with_paragraph_and_bad_line_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/atx_with_paragraph_and_bad_line_spacing.md:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/atx_with_paragraph_and_bad_line_spacing.md:7:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_atx_with_code_block_and_good_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do have proper
    default spacing before and after the heading, surrounded by code blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/atx_with_code_block_and_good_line_spacing.md",
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
def test_md022_bad_atx_with_code_block_and_bad_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing before and after the heading, surrounded by code blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/atx_with_code_block_and_bad_line_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/atx_with_code_block_and_bad_line_spacing.md:4:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/atx_with_code_block_and_bad_line_spacing.md:9:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_atx_with_thematic_break_and_good_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do have proper
    default spacing before and after the heading, surrounded by thematic breaks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/atx_with_thematic_break_and_good_line_spacing.md",
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
def test_md022_bad_atx_with_thematic_break_and_bad_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    default spacing before and after the heading, surrounded by thematic breaks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/atx_with_thematic_break_and_bad_line_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/atx_with_thematic_break_and_bad_line_spacing.md:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/atx_with_thematic_break_and_bad_line_spacing.md:7:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has setext headings that do have proper
    default spacing before the heading.

    Note that setext grabs the last paragraph before the marker and puts it as the
    heading.  As such, testing this for one line space before is implied as one line
    space is required to break up the paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_setext.md:1:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_setext.md:6:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_after_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has setext headings that do not have proper
    default spacing before the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/no_line_spacing_after_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_after_setext.md:1:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_after_setext.md:6:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_setext_with_code_block_and_good_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has setext headings that do have proper
    default spacing before and after the heading, surrounded by code blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/setext_with_code_block_and_good_line_spacing.md",
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
def test_md022_bad_setext_with_code_block_and_bad_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has setext headings that do not have proper
    default spacing before and after the heading, surrounded by code blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/setext_with_code_block_and_bad_line_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/setext_with_code_block_and_bad_line_spacing.md:4:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/setext_with_code_block_and_bad_line_spacing.md:10:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_setext_with_html_and_good_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has setext headings that do have proper
    default spacing before and after the heading, surrounded by html blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/setext_with_html_and_good_line_spacing.md",
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
def test_md022_bad_setext_with_html_and_bad_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has setext headings that do not have proper
    default spacing before and after the heading, surrounded by html blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/setext_with_html_and_bad_line_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/setext_with_html_and_bad_line_spacing.md:3:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/setext_with_html_and_bad_line_spacing.md:9:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_setext_with_thematic_break_and_good_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has setext headings that do have proper
    default spacing before and after the heading, surrounded by thematic breaks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/setext_with_thematic_break_and_good_line_spacing.md",
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
def test_md022_bad_setext_with_thematic_break_and_bad_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has setext headings that do not have proper
    default spacing before and after the heading, surrounded by thematic breaks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md022/setext_with_thematic_break_and_bad_line_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/setext_with_thematic_break_and_bad_line_spacing.md:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/setext_with_thematic_break_and_bad_line_spacing.md:8:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_proper_line_spacing_atx_with_alternate_lines_above():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    spacing before the heading with an alternate configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md022": {"lines_above": 2}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md022/proper_line_spacing_atx.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md022/proper_line_spacing_atx.md:7:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md022_good_double_line_spacing_above_atx_with_alternate_lines_above():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do have proper
    spacing before the heading with an alternate configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md022": {"lines_above": 2}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md022/double_line_spacing_above_atx.md",
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
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md022_bad_proper_line_spacing_atx_with_alternate_lines_below():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do not have proper
    spacing below the heading with an alternate configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md022": {"lines_below": 2}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md022/proper_line_spacing_atx.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md022/proper_line_spacing_atx.md:1:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)\n"
            + "test/resources/rules/md022/proper_line_spacing_atx.md:7:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md022_good_double_line_spacing_above_atx_with_alternate_lines_below():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do have proper
    spacing below the heading with an alternate configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md022": {"lines_below": 2}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md022/double_line_spacing_below_atx.md",
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
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md022_good_double_line_spacing_above_and_below_atx_with_alternate_lines_both():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has atx headings that do have proper
    spacing above and below the heading with an alternate configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {
        "plugins": {"md022": {"lines_below": 2, "lines_above": 2}}
    }
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md022/double_line_spacing_above_and_below_atx.md",
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
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md022_good_alternating_heading_types():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has alternating heading types.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable",
        "MD003",
        "scan",
        "test/resources/rules/md022/alternating_heading_types.md",
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
def test_md022_bad_alternating_heading_types_with_alternate_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD022 directory that has alternating heading types with
    an alternate configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {
        "plugins": {"md022": {"lines_below": 2, "lines_above": 2}}
    }
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "--disable",
            "MD003",
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md022/alternating_heading_types.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md022/alternating_heading_types.md:1:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)\n"
            + "test/resources/rules/md022/alternating_heading_types.md:3:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
            + "test/resources/rules/md022/alternating_heading_types.md:3:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)\n"
            + "test/resources/rules/md022/alternating_heading_types.md:6:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
            + "test/resources/rules/md022/alternating_heading_types.md:6:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)\n"
            + "test/resources/rules/md022/alternating_heading_types.md:8:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
            + "test/resources/rules/md022/alternating_heading_types.md:8:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)

@pytest.mark.rules
def test_md022_bad_alternating_heading_types_with_alternate_spacing_and_bad_config():
    """
    Same as above, but with the lines_below being an illegal value.  Without
    strict mode, this means the value will not be used, and the default of 1
    will be used.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {
        "plugins": {"md022": {"lines_below": -2, "lines_above": 2}}
    }
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "--disable",
            "MD003",
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md022/alternating_heading_types.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md022/alternating_heading_types.md:3:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
            + "test/resources/rules/md022/alternating_heading_types.md:6:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
            + "test/resources/rules/md022/alternating_heading_types.md:8:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)

@pytest.mark.rules
def test_md022_bad_alternating_heading_types_with_alternate_spacing_and_bad_config_strict_mode():
    """
    Same as above, but with the lines_below being an illegal value.  With strict mode,
    this means that an error will be displayed.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {
        "plugins": {"md022": {"lines_below": -2, "lines_above": 2}}
    }
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "--strict-config",
            "--disable",
            "MD003",
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md022/alternating_heading_types.md",
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = "BadPluginError encountered while configuring plugins:\n" \
        + "The value for property 'plugins.md022.lines_below' is not valid: Value must not be zero or a positive integer.\n"

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)
