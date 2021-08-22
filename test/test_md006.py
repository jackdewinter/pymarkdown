"""
Module to provide tests related to the MD006 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md006_good_indentation():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md006 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/good_indentation.md",
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
def test_md006_bad_indentation():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md006 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/bad_indentation.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md006/bad_indentation.md:1:2: MD006: "
        + "Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
        + "test/resources/rules/md006/bad_indentation.md:2:2: MD006: "
        + "Consider starting bulleted lists at the beginning of the line (ul-start-left)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md006_good_ignore_bad_second_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md006 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "--disable-rules",
        "MD005,md032",
        "scan",
        "test/resources/rules/md006/good_ignore_bad_second_level.md",
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
def test_md006_good_not_ordered():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md006 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/good_not_ordered.md",
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
def test_md006_good_items_with_multiple_lines():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md006 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/good_items_with_multiple_lines.md",
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
