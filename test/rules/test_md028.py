"""
Module to provide tests related to the MD026 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from typing import Tuple

import pytest


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", "rules", "md028", source_file_name)
    return source_path, os.path.abspath(source_path)


@pytest.mark.rules
def test_md028_good_split_block_quote(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a single block quote containing a blank line with no missing bq character.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_split_block_quote.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md028_bad_split_block_quote(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes separated by a blank line with no bq character.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_split_block_quote.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:2:1: MD028: Blank line inside blockquote (no-blanks-blockquote)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md028_bad_split_block_quote_multiple_blanks(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes containing two blank lines with no bq character.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_split_block_quote_multiple_blanks.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md012",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:2:1: MD028: Blank line inside blockquote (no-blanks-blockquote)
{abs_source_path}:3:1: MD028: Blank line inside blockquote (no-blanks-blockquote)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md028_good_split_atx(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains two block quotes separated by an Atx Heading.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_split_atx.md")
    supplied_arguments = [
        "--disable-rules",
        "md022",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md028_good_split_blank_atx(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains two block quotes separated by a blank Atx Heading.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_split_blank_atx.md")
    supplied_arguments = [
        "--disable-rules",
        "md022",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md028_good_blank_paragraph_blank(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains two block quotes separated by a blank line, a paragraph,
    and another blank line.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_blank_paragraph_blank.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md028_bad_blank_paragraph(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes separated by a paragraph and a blank line.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_blank_paragraph.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:1: MD028: Blank line inside blockquote (no-blanks-blockquote)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md028_good_blank_paragraph(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains two block quotes separated by a blank line and a paragraph.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_blank_paragraph.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md028_bad_split_block_quote_in_list(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes separated by a blank line, all within
    a list item.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_split_block_quote_in_list.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:2:1: MD028: Blank line inside blockquote (no-blanks-blockquote)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md028_bad_para_and_split_block_quote_in_list(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two block quotes separated by a blank within a list item.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_para_and_split_block_quote_in_list.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:1: MD028: Blank line inside blockquote (no-blanks-blockquote)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md028_bad_split_blank_with_nested_bq(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains two double block quotes separated by a blank line with a bq start character.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_split_blank_with_nested_bq.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:2:1: MD028: Blank line inside blockquote (no-blanks-blockquote)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
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
