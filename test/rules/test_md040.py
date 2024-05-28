"""
Module to provide tests related to the MD040 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest

import pytest


@pytest.mark.rules
def test_md040_good_fenced_block_with_language():
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced code block with language specified.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md040", "good_fenced_block_with_language.md"
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
def test_md040_good_fenced_block_with_space_before_language():
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced code block with language specified after a space.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md040",
        "good_fenced_block_with_space_before_language.md",
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
def test_md040_bad_fenced_block_with_no_language():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block with no language specified.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md040", "bad_fenced_block_with_no_language.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD040: Fenced code blocks should have a language specified (fenced-code-language)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md040_bad_fenced_block_with_whitespace():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block with only whitespace specified.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md040", "bad_fenced_block_with_whitespace.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:1: "
        + "MD040: Fenced code blocks should have a language specified (fenced-code-language)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_md040_query_config():
    config_test = pluginQueryConfigTest(
        "md040",
        """
  ITEM               DESCRIPTION

  Id                 md040
  Name(s)            fenced-code-language
  Short Description  Fenced code blocks should have a language specified
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md040.md

""",
    )
    execute_query_configuration_test(config_test)
