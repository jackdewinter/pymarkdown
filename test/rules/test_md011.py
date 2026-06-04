"""
Module to provide tests related to the MD011 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from typing import Tuple

import pytest


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", "rules", "md011", source_file_name)
    return source_path, os.path.abspath(source_path)


@pytest.mark.rules
def test_md011_good_no_reversed(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains no reversed links.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_no_reversed.md")
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
def test_md011_bad_with_reversed(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains at least one reversed link.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_with_reversed.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:2:8: MD011: Reversed link syntax [(reversed)[link]] (no-reversed-links)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md011_good_markdown_footnote(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains what looks like a reversed link, but also looks like a footnote.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_markdown_extra.md")
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
def test_md011_good_with_reversed_in_code_block(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a "reversed link" in a code block.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_with_reversed_in_code_block.md")
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
def test_md011_good_with_reversed_in_html_block(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a "reversed link" in a HTML block.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_with_reversed_in_html_block.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_md011_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md011",
        """
  ITEM               DESCRIPTION

  Id                 md011
  Name(s)            no-reversed-links
  Short Description  Reversed link syntax
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md011.md
""",
    )
    execute_query_configuration_test(config_test)
