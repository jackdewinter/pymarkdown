"""
Module to provide tests related to the MD049 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md049_valid_anchors():
    """
    Test to verify that no error is thrown.
    """

    # Arrange
    scanner = MarkdownScanner()
    path1 = os.path.join("test", "resources", "rules", "md049", "anchor1_valid.md")
    path2 = os.path.join("test", "resources", "rules", "md049", "anchor2_valid.md")
    supplied_arguments = [
        "--strict-config",
        "-e md049",
        "scan",
        path1,
        path2,
    ]

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md049_valid_anchors_setext():
    """
    Test to verify that no error is thrown with setext headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    path1 = os.path.join(
        "test", "resources", "rules", "md049", "anchor1_valid_setext.md"
    )
    path2 = os.path.join(
        "test", "resources", "rules", "md049", "anchor2_valid_setext.md"
    )
    supplied_arguments = [
        "--strict-config",
        "-e md049",
        "scan",
        path1,
        path2,
    ]

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md049_invalid_anchors():
    """
    Test to verify that an error is thrown.
    """

    # Arrange
    scanner = MarkdownScanner()
    path1 = os.path.join("test", "resources", "rules", "md049", "anchor1_invalid.md")
    path2 = os.path.join("test", "resources", "rules", "md049", "anchor2_invalid.md")
    supplied_arguments = [
        "--strict-config",
        "-e md049",
        "scan",
        path1,
        path2,
    ]

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    expected_return_code = 1
    expected_output = f"""{path1}:5:1: MD049: Local URIs should be valid [Wrong reference: # anchor not a valid heading] (validate-refs)
{path2}:3:1: MD049: Local URIs should be valid [Wrong reference: # anchor not a valid heading] (validate-refs)
{path1}:3:1: MD049: Local URIs should be valid [Wrong reference: # anchor not a valid heading] (validate-refs)
{path2}:5:1: MD049: Local URIs should be valid [Wrong reference: # anchor not a valid heading] (validate-refs)
"""
    expected_error = ""

    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
