"""
Module to provide tests related to the MD021 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md021_good_single_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has single spacing inside the hashes of
    a closed atx header.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md021/single_spacing.md",
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
def test_md021_bad_multiple_spacing_both():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has multiple spacing inside the hashes of
    a closed atx header on both sides.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md021/multiple_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md021/multiple_spacing.md:0:0: "
        + "MD021: Multiple spaces inside hashes on closed atx style heading (no-multiple-space-closed-atx)\n"
        + "test/resources/rules/md021/multiple_spacing.md:0:0: "
        + "MD021: Multiple spaces inside hashes on closed atx style heading (no-multiple-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md021_bad_multiple_spacing_left():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has multiple spacing inside the hashes of
    a closed atx header on the left.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md021/multiple_spacing_left.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md021/multiple_spacing_left.md:0:0: "
        + "MD021: Multiple spaces inside hashes on closed atx style heading (no-multiple-space-closed-atx)\n"
        + "test/resources/rules/md021/multiple_spacing_left.md:0:0: "
        + "MD021: Multiple spaces inside hashes on closed atx style heading (no-multiple-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md021_bad_multiple_spacing_right():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has multiple spacing inside the hashes of
    a closed atx header on the right.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md021/multiple_spacing_right.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md021/multiple_spacing_right.md:0:0: "
        + "MD021: Multiple spaces inside hashes on closed atx style heading (no-multiple-space-closed-atx)\n"
        + "test/resources/rules/md021/multiple_spacing_right.md:0:0: "
        + "MD021: Multiple spaces inside hashes on closed atx style heading (no-multiple-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md021_good_multiple_spacing_with_inline():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has single spacing inside the hashes of
    a closed atx header, with inline.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md021/multiple_spacing_with_inline.md",
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
