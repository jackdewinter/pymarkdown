"""
Module to provide tests related to the MD023 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md023_good_proper_indent_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD023 directory that has an atx heading that is not indented
    from the start of the line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md023/proper_indent_atx.md",
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
def test_md023_good_proper_indent_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD023 directory that has an setext heading that is not indented
    from the start of the line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md023/proper_indent_setext.md",
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
def test_md023_bad_improper_indent_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md023 directory that has an atx heading that is indented from
    the start of the line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md023/improper_indent_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md023/improper_indent_atx.md:3:3: "
        + "MD023: Headings must start at the beginning of the line (heading-start-left, header-start-left)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indent_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md023 directory that has a setext heading that is indented from
    the start of the line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md023/improper_indent_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md023/improper_indent_setext.md:4:3: "
        + "MD023: Headings must start at the beginning of the line (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext.md:9:3: "
        + "MD023: Headings must start at the beginning of the line (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext.md:14:1: "
        + "MD023: Headings must start at the beginning of the line (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext.md:22:1: "
        + "MD023: Headings must start at the beginning of the line (heading-start-left, header-start-left)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
