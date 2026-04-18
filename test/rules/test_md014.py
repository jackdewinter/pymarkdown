"""
Module to provide tests related to the MD014 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from typing import Tuple

import pytest


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", "rules", "md014", source_file_name)
    return source_path, os.path.abspath(source_path)


@pytest.mark.rules
def test_md014_good_shell_example(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced block with a `shell` tag and no leading $.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_shell_example.md")
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
def test_md014_good_shell_example_some_output(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced block with a `shell` tag and mixed lines with leading $
    and no leading $.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_shell_example_some_output.md")
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
def test_md014_bad_shell_example(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced block with a `shell` tag and only leading $.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_shell_example.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:2:1: MD014: Dollar signs used before commands without showing output (commands-show-output)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md014_bad_shell_example_with_leading_space(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule not trigger with a document that
    contains a fenced block with a `shell` tag and only leading $
    with leading space before that.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_shell_example_with_leading_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:2:2: MD014: Dollar signs used before commands without showing output (commands-show-output)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md014_bad_shell_example_indented(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule not trigger with a document that
    contains an indented block with leading $ that looks like shell output.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_shell_example_indented.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"{abs_source_path}:3:5: MD014: Dollar signs used before commands without showing output (commands-show-output)"
        "",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


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
