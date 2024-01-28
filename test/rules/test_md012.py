"""
Module to provide tests related to the MD012 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md012_bad_configuration_maximum():
    """
    Test to verify that a configuration error is thrown when supplying the
    maximum value with an integer that is negative.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md012", "good_simple_paragraphs_single_blanks.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md012.maximum=$#-2",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md012.maximum' is not valid: Allowable values are any non-negative integers."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md012_good_simple_paragraphs_single_blanks():
    """
    Test to make sure this rule does not trigger with a document that
    contains only paragraphs with a single blank line between them.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md012", "good_simple_paragraphs_single_blanks.md"
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
def test_md012_bad_simple_paragraphs_double_blanks():
    """
    Test to make sure this rule does trigger with a document that
    contains only paragraphs with two blank lines between them.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md012", "good_simple_paragraphs_double_blanks.md"
    )
    supplied_arguments = [
        # "--log-level", "DEBUG",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md012_good_simple_paragraphs_double_blanks():
    """
    Test to make sure this rule does not trigger with a document that
    contains only paragraphs with two blank lines between them and
    the configuration to make that correct.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md012", "good_simple_paragraphs_double_blanks.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md012.maximum=$#2",
        "--strict-config",
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
def test_md012_good_simple_paragraphs_triple_blanks():
    """
    Test to make sure this rule does trigger with a document that
    contains only paragraphs with three blank lines between them.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md012", "good_simple_paragraphs_triple_blanks.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:1: "
        + "MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md012_bad_double_blanks_at_end():
    """
    Test to make sure this rule does trigger with a document that
    contains a paragraph followed by two blank lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md012", "bad_double_blanks_at_end.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md012_bad_multiple_blanks_in_block_quote():
    """
    Test to make sure this rule does not trigger with a document that
    contains two paragraphs separated by two blank lines, all within a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md012", "bad_multiple_blanks_in_block_quote.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:2: "
        + "MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md012_bad_multiple_blanks_in_list():
    """
    Test to make sure this rule does trigger with a document that
    contains a paragraph followed by two blank lines, in a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md012", "bad_multiple_blanks_in_list.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md009",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md012_good_multiple_blanks_in_fenced():
    """
    Test to make sure this rule does not trigger with a document that
    contains a two blank lines within a fenced code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md012", "good_multiple_blanks_in_fenced.md"
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
def test_md012_good_multiple_blanks_in_indented():
    """
    Test to make sure this rule does not trigger with a document that
    contains a two blank lines within a indented code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md012", "good_multiple_blanks_in_indented.md"
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
def test_md012_bad_multiple_blanks_in_html():
    """
    Test to make sure this rule does not trigger with a document that
    contains a two blank lines within a HTML block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md012", "bad_multiple_blanks_in_html.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
