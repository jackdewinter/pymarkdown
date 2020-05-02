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
    test/resources/rules/md019 directory that has atx headers with a single space
    after the initial hash.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md019/single_spacing.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md019_bad_multiple_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md019 directory that has atx headers with multiple spaces
    after the initial hash.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md019/multiple_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md019/multiple_spacing.md:0:0: "
        + "MD019: Multiple spaces after hash on atx style heading (no-multiple-space-atx)\n"
        "test/resources/rules/md019/multiple_spacing.md:0:0: "
        + "MD019: Multiple spaces after hash on atx style heading (no-multiple-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_md019_bad_multiple_spacing_with_inline():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md019 directory that has atx headers with a single space
    after the initial hash, with inline processing in the header for good measure.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md019/multiple_spacing_with_inline.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md019/multiple_spacing_with_inline.md:0:0: "
        + "MD019: Multiple spaces after hash on atx style heading (no-multiple-space-atx)\n"
        "test/resources/rules/md019/multiple_spacing_with_inline.md:0:0: "
        + "MD019: Multiple spaces after hash on atx style heading (no-multiple-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
