"""
Module to provide tests related to the MD040 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from typing import Tuple

import pytest


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", "rules", "md040", source_file_name)
    return source_path, os.path.abspath(source_path)


@pytest.mark.rules
def test_md040_good_fenced_block_with_language(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced code block with language specified.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_fenced_block_with_language.md")
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
def test_md040_good_fenced_block_with_space_before_language(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced code block with language specified after a space.
    """

    # Arrange
    source_path, _ = __generate_source_path(
        "good_fenced_block_with_space_before_language.md",
    )
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
def test_md040_bad_fenced_block_with_no_language(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block with no language specified.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_fenced_block_with_no_language.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:1: MD040: Fenced code blocks should have a language specified (fenced-code-language)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md040_bad_fenced_block_with_whitespace(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block with only whitespace specified.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_fenced_block_with_whitespace.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:4:1: MD040: Fenced code blocks should have a language specified (fenced-code-language)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md040_query_config() -> None:
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
