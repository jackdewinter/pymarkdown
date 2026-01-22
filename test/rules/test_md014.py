"""
Module to provide tests related to the MD014 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest

import pytest


@pytest.mark.rules
def test_md014_good_shell_example() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced block with a `shell` tag and no leading $.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md014", "good_shell_example.md"
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
def test_md014_good_shell_example_some_output() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced block with a `shell` tag and mixed lines with leading $
    and no leading $.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md014", "good_shell_example_some_output.md"
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
def test_md014_bad_shell_example() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced block with a `shell` tag and only leading $.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md014", "bad_shell_example.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:2:1: "
        + "MD014: Dollar signs used before commands without showing output (commands-show-output)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md014_bad_shell_example_with_leading_space() -> None:
    """
    Test to make sure this rule not trigger with a document that
    contains a fenced block with a `shell` tag and only leading $
    with leading space before that.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md014", "bad_shell_example_with_leading_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:2:2: "
        + "MD014: Dollar signs used before commands without showing output (commands-show-output)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md014_bad_shell_example_indented() -> None:
    """
    Test to make sure this rule not trigger with a document that
    contains an indented block with leading $ that looks like shell output.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md014", "bad_shell_example_indented.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:3:5: "
        + "MD014: Dollar signs used before commands without showing output (commands-show-output)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_md014_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md014",
        """
  ITEM               DESCRIPTION

  Id                 md014
  Name(s)            commands-show-output
  Short Description  Dollar signs used before commands without showing output
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md014.md
  """,
    )
    execute_query_configuration_test(config_test)
