"""
Module to provide tests related to the MD026 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md028_good_split_block_quote():
    """
    Test to make sure this rule does not trigger with a document that
    contains a single block quote containing a blank line with no missing bq character.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md028/good_split_block_quote.md",
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
def test_md028_bad_split_block_quote():
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes separated by a blank line with no bq character.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md028/bad_split_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md028/bad_split_block_quote.md:2:1: "
        + "MD028: Blank line inside blockquote (no-blanks-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md028_bad_split_block_quote_multiple_blanks():
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes containing two blank lines with no bq character.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md012",
        "scan",
        "test/resources/rules/md028/bad_split_block_quote_multiple_blanks.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md028/bad_split_block_quote_multiple_blanks.md:2:1: "
        + "MD028: Blank line inside blockquote (no-blanks-blockquote)\n"
        + "test/resources/rules/md028/bad_split_block_quote_multiple_blanks.md:3:1: "
        + "MD028: Blank line inside blockquote (no-blanks-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md028_good_split_atx():
    """
    Test to make sure this rule does not trigger with a document that
    contains two block quotes separated by an Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md022",
        "scan",
        "test/resources/rules/md028/good_split_atx.md",
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
def test_md028_good_split_blank_atx():
    """
    Test to make sure this rule does not trigger with a document that
    contains two block quotes separated by a blank Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md022",
        "scan",
        "test/resources/rules/md028/good_split_blank_atx.md",
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
def test_md028_good_blank_paragraph_blank():
    """
    Test to make sure this rule does not trigger with a document that
    contains two block quotes separated by a blank line, a paragraph,
    and another blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md028/good_blank_paragraph_blank.md",
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
def test_md028_bad_blank_paragraph():
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes separated by a paragraph and a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md028/bad_blank_paragraph.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md028/bad_blank_paragraph.md:3:1: "
        + "MD028: Blank line inside blockquote (no-blanks-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md028_good_blank_paragraph():
    """
    Test to make sure this rule does not trigger with a document that
    contains two block quotes separated by a blank line and a paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md028/good_blank_paragraph.md",
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
@pytest.mark.skip
def test_md028_bad_split_block_quote_in_list():
    """
    TBD
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md028/bad_split_block_quote_in_list.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md028_bad_para_and_split_block_quote_in_list():
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes separated by a blank within a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md028/bad_para_and_split_block_quote_in_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md028/bad_para_and_split_block_quote_in_list.md:3:1: "
        + "MD028: Blank line inside blockquote (no-blanks-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md028_bad_split_blank_with_nested_bq():
    """
    Test to make sure this rule does not trigger with a document that
    contains two double block quotes separated by a blank line with a bq start character.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md028/bad_split_blank_with_nested_bq.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md028/bad_split_blank_with_nested_bq.md:2:1: "
        + "MD028: Blank line inside blockquote (no-blanks-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
