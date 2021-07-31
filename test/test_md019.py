"""
Module to provide tests related to the MD019 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md019_good_single_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md019 directory that has atx headings with a single space
    after the initial hash.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md019/single_spacing.md",
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
def test_md019_bad_multiple_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md019 directory that has atx headings with multiple spaces
    after the initial hash.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md019/multiple_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md019/multiple_spacing.md:1:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
        "test/resources/rules/md019/multiple_spacing.md:3:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_md019_bad_multiple_spacing_with_inline():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md019 directory that has atx headings with a single space
    after the initial hash, with inline processing in the heading for good measure.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md019/multiple_spacing_with_inline.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md019/multiple_spacing_with_inline.md:1:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
        "test/resources/rules/md019/multiple_spacing_with_inline.md:3:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_md019_bad_multiple_spacing_with_indent():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md019 directory that has atx headings with a single space
    after the initial hash, with inline processing in the heading for good measure.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        "test/resources/rules/md019/multiple_spacing_with_indent.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md019/multiple_spacing_with_indent.md:1:2: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
        "test/resources/rules/md019/multiple_spacing_with_indent.md:3:3: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_md019_bad_single_space_single_tab():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md019 directory that has two headers that start with various
    amounts of leading whitespace, followed by 1-2 hash characters, a single space
    character, and a single tab character.  This rule should not fire as in both cases,
    there is a single space after the hash character.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--stack-trace",
        "--disable-rules",
        "md010,md023",
        "scan",
        "test/resources/rules/md019/single_space_single_tab.md",
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
