"""
Module to provide tests related to the MD042 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from typing import Tuple

import pytest


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", "rules", "md042", source_file_name)
    return source_path, os.path.abspath(source_path)


@pytest.mark.rules
def test_md042_good_non_empty_link(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains links that have non-empty urls.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_non_empty_link.md")
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
def test_md042_bad_empty_link(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains links that have empty urls.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_empty_link.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"{abs_source_path}:2:1: MD042: No empty links (no-empty-links)",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md042_bad_whitespace_link(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains links that have whitespace only urls.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_whitespace_link.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"{abs_source_path}:2:1: MD042: No empty links (no-empty-links)",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md042_good_non_empty_fragment(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains links that has a non-empty url fragment.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_non_empty_fragment.md")
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
def test_md042_bad_link_empty_fragment(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains links that have empty url fragments.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_link_empty_fragment.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"{abs_source_path}:2:1: MD042: No empty links (no-empty-links)",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md042_bad_link_whitespace_fragment(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains links that have whitespace only url fragments.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_link_whitespace_fragment.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"{abs_source_path}:2:1: MD042: No empty links (no-empty-links)",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md042_good_non_empty_image(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains images that have non-empty urls.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_non_empty_image.md")
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
def test_md042_bad_empty_image(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains links that have empty urls.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_empty_image.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"{abs_source_path}:2:1: MD042: No empty links (no-empty-links)",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_md042_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md042",
        """
  ITEM               DESCRIPTION

  Id                 md042
  Name(s)            no-empty-links
  Short Description  No empty links
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md042.md

""",
    )
    execute_query_configuration_test(config_test)
