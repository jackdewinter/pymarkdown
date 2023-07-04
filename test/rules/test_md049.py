"""
Module to provide tests related to the MD049 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md049_relative_file_invalid():
    """
    Test to verify that an error is thrown when a local relative URI doesn't
    resolve to a file.
    """

    # Arrange
    scanner = MarkdownScanner()
    markdown_path = os.path.join(
        "test", "resources", "rules", "md049", "file-relative-invalid.md"
    )
    supplied_arguments = [
        "--strict-config",
        "-e md049",
        "scan",
        markdown_path,
    ]

    expected_return_code = 1
    expected_output = f"{markdown_path}:1:1: MD049: Local URIs should be valid [Dangling reference: file does not exist!] (validate-refs)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md049_relative_file_valid():
    """
    Test to verify that no error is thrown when a local relative URI resolves
    to a file.
    """

    # Arrange
    scanner = MarkdownScanner()
    markdown_path = os.path.join(
        "test", "resources", "rules", "md049", "file-relative-valid.md"
    )
    supplied_arguments = [
        "--strict-config",
        "-e md049",
        "scan",
        markdown_path,
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
def test_md049_absolute_file_invalid():
    """
    Test to verify that an error is thrown when a local absolute URI doesn't
    resolve to a file.
    """
    # Arrange
    scanner = MarkdownScanner()
    markdown_path = os.path.join(
        "test", "resources", "rules", "md049", "file-absolute-invalid.md"
    )
    supplied_arguments = [
        "--strict-config",
        "-e md049",
        "scan",
        markdown_path,
    ]

    expected_return_code = 1
    expected_output = f"{markdown_path}:1:1: MD049: Local URIs should be valid [Dangling reference: file does not exist!] (validate-refs)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md049_absolute_file_valid():
    """
    Test to verify that no error is thrown when a local absolute URI resolves to a file.
    """

    # Arrange
    scanner = MarkdownScanner()
    markdown_path = os.path.join(
        "test", "resources", "rules", "md049", "file-absolute-valid.md"
    )
    supplied_arguments = [
        "--strict-config",
        "-e md049",
        "scan",
        markdown_path,
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
