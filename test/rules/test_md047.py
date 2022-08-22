"""
Module to provide tests related to the MD047 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md047_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md047 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join("test", "resources", "rules", "md047") + os.sep
    supplied_arguments = ["scan", source_path]

    expected_return_code = 1
    expected_output = (
        f"{source_path}end_with_no_blank_line.md:3:41: "
        + "MD047: Each file should end with a single newline character. "
        + "(single-trailing-newline)\n"
        + f"{source_path}end_with_no_blank_line_and_spaces.md:4:2: "
        + "MD047: Each file should end with a single newline character. "
        + "(single-trailing-newline)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md047_good_end_with_blank_line():
    """
    Test to make sure this rule does not trigger with a document that
    properly ends with a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = ["scan", source_path]

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
def test_md047_bad_end_with_no_blank_line():
    """
    Test to make sure this rule does trigger with a document that
    does not end with a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_no_blank_line.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:41: "
        + "MD047: Each file should end with a single newline character. (single-trailing-newline)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md047_bad_end_with_blank_line_containing_spaces():
    """
    Test to make sure this rule does trigger with a document that
    ends with a line that is only whitespace.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_no_blank_line_and_spaces.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:2: "
        + "MD047: Each file should end with a single newline character. (single-trailing-newline)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
