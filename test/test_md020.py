"""
Module to provide tests related to the MD003 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md020_good_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md020/good_spacing.md",
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
def test_md020_ignore_bad_atx_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md020/ignore_bad_atx_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/ignore_bad_atx_spacing.md:0:0: "
        + "MD018: No space after hash on atx style heading (no-missing-space-atx)\n"
        + "test/resources/rules/md020/ignore_bad_atx_spacing.md:0:0: "
        + "MD018: No space after hash on atx style heading (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_missing_start_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md020/missing_start_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/missing_start_spacing.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/missing_start_spacing.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_missing_end_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md020/missing_end_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/missing_end_spacing.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/missing_end_spacing.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_almost_missing_end_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md020/almost_missing_end_spacing.md",
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
def test_md020_missing_both_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md020/missing_both_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/missing_both_spacing.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/missing_both_spacing.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_with_setext_headers():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md020/with_setext_headers.md",
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
def test_md020_with_code_blocks():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md020/with_code_blocks.md",
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
def test_md020_with_html_blocks():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md020/with_html_blocks.md",
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
def test_md020_multiple_within_paragraph():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md020/multiple_within_paragraph.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/multiple_within_paragraph.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_paragraphs_with_starting_whitespace():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md020/paragraphs_with_starting_whitespace.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/paragraphs_with_starting_whitespace.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/paragraphs_with_starting_whitespace.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/paragraphs_with_starting_whitespace.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/paragraphs_with_starting_whitespace.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_single_paragraph_with_starting_whitespace():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md020/single_paragraph_with_starting_whitespace.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/single_paragraph_with_starting_whitespace.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/single_paragraph_with_starting_whitespace.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/single_paragraph_with_starting_whitespace.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/single_paragraph_with_starting_whitespace.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


# TODO not in list
# TODO not in block quote
