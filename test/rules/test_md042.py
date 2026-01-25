"""
Module to provide tests related to the MD042 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest

import pytest


@pytest.mark.rules
def test_md042_good_non_empty_link() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains links that have non-empty urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md042", "good_non_empty_link.md"
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
def test_md042_bad_empty_link() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains links that have empty urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md042", "bad_empty_link.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:2:1: MD042: No empty links (no-empty-links)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md042_bad_whitespace_link() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains links that have whitespace only urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md042", "bad_whitespace_link.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:2:1: MD042: No empty links (no-empty-links)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md042_good_non_empty_fragment() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains links that has a non-empty url fragment.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md042", "good_non_empty_fragment.md"
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
def test_md042_bad_link_empty_fragment() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains links that have empty url fragments.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md042", "bad_link_empty_fragment.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:2:1: MD042: No empty links (no-empty-links)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md042_bad_link_whitespace_fragment() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains links that have whitespace only url fragments.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md042", "bad_link_whitespace_fragment.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:2:1: MD042: No empty links (no-empty-links)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md042_good_non_empty_image() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains images that have non-empty urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md042", "good_non_empty_image.md"
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
def test_md042_bad_empty_image() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains links that have empty urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md042", "bad_empty_image.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:2:1: MD042: No empty links (no-empty-links)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


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
