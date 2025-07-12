"""
Module to provide tests related to the MD026 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest

import pytest


@pytest.mark.rules
def test_md028_good_split_block_quote() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a single block quote containing a blank line with no missing bq character.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md028", "good_split_block_quote.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
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
def test_md028_bad_split_block_quote() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes separated by a blank line with no bq character.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md028", "bad_split_block_quote.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
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
def test_md028_bad_split_block_quote_multiple_blanks() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes containing two blank lines with no bq character.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md028",
        "bad_split_block_quote_multiple_blanks.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md012",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD028: Blank line inside blockquote (no-blanks-blockquote)\n"
        + f"{source_path}:3:1: "
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
def test_md028_good_split_atx() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains two block quotes separated by an Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md028", "good_split_atx.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md022",
        "scan",
        source_path,
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
def test_md028_good_split_blank_atx() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains two block quotes separated by a blank Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md028", "good_split_blank_atx.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md022",
        "scan",
        source_path,
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
def test_md028_good_blank_paragraph_blank() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains two block quotes separated by a blank line, a paragraph,
    and another blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md028", "good_blank_paragraph_blank.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
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
def test_md028_bad_blank_paragraph() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes separated by a paragraph and a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md028", "bad_blank_paragraph.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
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
def test_md028_good_blank_paragraph() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains two block quotes separated by a blank line and a paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md028", "good_blank_paragraph.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
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
def test_md028_bad_split_block_quote_in_list() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes separated by a blank line, all within
    a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md028", "bad_split_block_quote_in_list.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
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
def test_md028_bad_para_and_split_block_quote_in_list() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes separated by a blank within a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md028",
        "bad_para_and_split_block_quote_in_list.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
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
def test_md028_bad_split_blank_with_nested_bq() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains two double block quotes separated by a blank line with a bq start character.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md028", "bad_split_blank_with_nested_bq.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD028: Blank line inside blockquote (no-blanks-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_md028_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md028",
        """
  ITEM               DESCRIPTION

  Id                 md028
  Name(s)            no-blanks-blockquote
  Short Description  Blank line inside blockquote
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md028.md


""",
    )
    execute_query_configuration_test(config_test)
