"""
Module to provide tests related to parsing from stdin.
"""

import os
from test.markdown_scanner import MarkdownScanner


def test_markdown_with_scan_stdin_without_triggers() -> None:
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan-stdin",
    ]

    supplied_standard_input = "test\nme\n"
    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=supplied_standard_input
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_scan_stdin_with_triggers() -> None:
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan-stdin",
    ]

    supplied_standard_input = "# test"
    expected_return_code = 1
    expected_output = """stdin:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
stdin:1:6: MD047: Each file should end with a single newline character. (single-trailing-newline)"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=supplied_standard_input
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_scan_stdin_with_triggers_and_disabled_rules() -> None:
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "-d",
        "MD022, MD047",
        "scan-stdin",
    ]

    supplied_standard_input = "# test"
    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=supplied_standard_input
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_scan_stdin_with_bad_write() -> None:
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "-x-stdin",
        "scan-stdin",
    ]

    supplied_standard_input = f"# test{os.linesep}"
    expected_return_code = 1
    expected_output = ""
    expected_error = """OSError encountered while scanning 'stdin':
Temporary file to capture stdin was not written (made up)."""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=supplied_standard_input
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
