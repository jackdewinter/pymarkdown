"""
Module to provide tests related to the MD047 rule.
"""
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
    supplied_arguments = ["scan", "test/resources/rules/md047"]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md047/end_with_no_blank_line.md:3:41: "
        + "MD047: Each file should end with a single newline character. "
        + "(single-trailing-newline)\n"
        + "test/resources/rules/md047/end_with_no_blank_line_and_spaces.md:4:2: "
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md047 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["scan", "test/resources/rules/md047/end_with_blank_line.md"]

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
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md047 directory which does not end with a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md047/end_with_no_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md047/end_with_no_blank_line.md:3:41: "
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
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md047 directory which does not end with a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md047/end_with_no_blank_line_and_spaces.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md047/end_with_no_blank_line_and_spaces.md:4:2: "
        + "MD047: Each file should end with a single newline character. (single-trailing-newline)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
