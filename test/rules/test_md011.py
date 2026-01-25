"""
Module to provide tests related to the MD011 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest

import pytest


@pytest.mark.rules
def test_md011_good_no_reversed() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains no reversed links.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md011", "good_no_reversed.md"
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
def test_md011_bad_with_reversed() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains at least one reversed link.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md011", "bad_with_reversed.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:2:8: "
        + "MD011: Reversed link syntax "
        + "[(reversed)[link]] (no-reversed-links)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md011_good_markdown_footnote() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains what looks like a reversed link, but also looks like a footnote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md011", "good_markdown_extra.md"
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
def test_md011_good_with_reversed_in_code_block() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a "reversed link" in a code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md011", "good_with_reversed_in_code_block.md"
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
def test_md011_good_with_reversed_in_html_block() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a "reversed link" in a HTML block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md011", "good_with_reversed_in_html_block.md"
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
