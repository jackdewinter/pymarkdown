"""
Module to provide tests related to the MD018 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md018_good_good_start_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has good atx heading start spacing after
    the first hash.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md018/good_start_spacing.md",
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
def test_md018_bad_ignore_bad_atx_closed_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has an atx heading with no spaces after
    initial hash, but ends with a close hash, making it a closed atx.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md018/ignore_bad_atx_closed_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/ignore_bad_atx_closed_spacing.md:0:0: "
        + "MD020: No space inside hashes on closed atx style heading (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md018/ignore_bad_atx_closed_spacing.md:0:0: "
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
def test_md018_bad_missing_atx_start_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has an atx heading with no spaces after
    initial hash.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md018/missing_start_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/missing_start_spacing.md:0:0: MD018: No space after hash on atx style heading (no-missing-space-atx)\n"
        + "test/resources/rules/md018/missing_start_spacing.md:0:0: MD018: No space after hash on atx style heading (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_good_with_setext_headings():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has a possible atx heading except that
    it is followed by setext headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md018/with_setext_headings.md",
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
def test_md018_good_with_code_blocks():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has a possible atx heading except that
    it is followed by code blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md018/with_code_blocks.md",
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
def test_md018_good_with_html_blocks():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has a possible atx heading except that
    it is followed by html blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md018/with_html_blocks.md",
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
def test_md018_bad_multiple_within_paragraph():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md018/multiple_within_paragraph.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph.md:0:0: "
        + "MD018: No space after hash on atx style heading (no-missing-space-atx)\n"
        + "test/resources/rules/md018/multiple_within_paragraph.md:0:0: "
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
def test_md018_bad_paragraphs_with_starting_whitespace():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings each
    one with starting whitespace that would normally be permitted.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md018/paragraphs_with_starting_whitespace.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/paragraphs_with_starting_whitespace.md:0:0: "
        + "MD018: No space after hash on atx style heading (no-missing-space-atx)\n"
        + "test/resources/rules/md018/paragraphs_with_starting_whitespace.md:0:0: "
        + "MD018: No space after hash on atx style heading (no-missing-space-atx)\n"
        + "test/resources/rules/md018/paragraphs_with_starting_whitespace.md:0:0: "
        + "MD018: No space after hash on atx style heading (no-missing-space-atx)\n"
        + "test/resources/rules/md018/paragraphs_with_starting_whitespace.md:0:0: "
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
def test_md018_bad_single_paragraph_with_starting_whitespace():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph each one with starting whitespace that would normally be
    permitted.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md018/single_paragraph_with_starting_whitespace.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/single_paragraph_with_starting_whitespace.md:0:0: "
        + "MD018: No space after hash on atx style heading (no-missing-space-atx)\n"
        + "test/resources/rules/md018/single_paragraph_with_starting_whitespace.md:0:0: "
        + "MD018: No space after hash on atx style heading (no-missing-space-atx)\n"
        + "test/resources/rules/md018/single_paragraph_with_starting_whitespace.md:0:0: "
        + "MD018: No space after hash on atx style heading (no-missing-space-atx)\n"
        + "test/resources/rules/md018/single_paragraph_with_starting_whitespace.md:0:0: "
        + "MD018: No space after hash on atx style heading (no-missing-space-atx)\n"
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
