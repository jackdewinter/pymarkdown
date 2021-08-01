"""
Module to provide tests related to the MD012 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md014_good_shell_example():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md014/good_shell_example.md",
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
def test_md014_good_shell_example_some_output():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md014/good_shell_example_some_output.md",
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
def test_md014_bad_shell_example():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "test/resources/rules/md014/bad_shell_example.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md014/bad_shell_example.md:2:1: "
        + "MD014: Dollar signs used before commands without showing output (commands-show-output)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md014_bad_shell_example_with_leading_space():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "test/resources/rules/md014/bad_shell_example_with_leading_space.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md014/bad_shell_example_with_leading_space.md:2:2: "
        + "MD014: Dollar signs used before commands without showing output (commands-show-output)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md014_bad_shell_example_indented():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md033",
        "scan",
        "test/resources/rules/md014/bad_shell_example_indented.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md014/bad_shell_example_indented.md:3:5: "
        + "MD014: Dollar signs used before commands without showing output (commands-show-output)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
