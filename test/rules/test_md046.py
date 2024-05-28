"""
Module to provide tests related to the MD046 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest

import pytest


@pytest.mark.rules
def test_md046_bad_configuration_style():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with an integer that is not a string.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md046", "good_both_fenced.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md046.style=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md046.style' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md046_bad_configuration_style_bad():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with a string that is not valid.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md046", "good_both_fenced.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md046.style=not-matching",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md046.style' is not valid: Allowable values: ['consistent', 'fenced', 'indented']"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md046_good_both_fenced_with_consistent():
    """
    Test to make sure this rule does not trigger with a document that
    contains code blocks that are fenced and consistent configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md046", "good_both_fenced.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md046.style=consistent",
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
def test_md046_good_both_indented_with_consistent():
    """
    Test to make sure this rule does not trigger with a document that
    contains code blocks that are indented and consistent configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md046", "good_both_indented.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md046.style=consistent",
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
def test_md046_bad_fenced_and_indented_with_consistent():
    """
    Test to make sure this rule does trigger with a document that
    contains code blocks that are fenced and indented and consistent configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md046", "bad_fenced_and_indented.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md046.style=consistent",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:5: "
        + "MD046: Code block style "
        + "[Expected: fenced; Actual: indented] (code-block-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md046_good_both_fenced_with_fenced():
    """
    Test to make sure this rule does not trigger with a document that
    contains code blocks that are fenced and fenced configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md046", "good_both_fenced.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md046.style=fenced",
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
def test_md046_good_both_indented_with_fenced():
    """
    Test to make sure this rule does trigger with a document that
    contains code blocks that are indented and fenced configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md046", "good_both_indented.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md046.style=fenced",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:5: "
        + "MD046: Code block style "
        + "[Expected: fenced; Actual: indented] (code-block-style)\n"
        + f"{source_path}:5:5: "
        + "MD046: Code block style "
        + "[Expected: fenced; Actual: indented] (code-block-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md046_bad_fenced_and_indented_with_fenced():
    """
    Test to make sure this rule does trigger with a document that
    contains code blocks that are fenced and indented and fenced configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md046", "bad_fenced_and_indented.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md046.style=fenced",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:5: "
        + "MD046: Code block style "
        + "[Expected: fenced; Actual: indented] (code-block-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md046_good_both_fenced_with_indented():
    """
    Test to make sure this rule does trigger with a document that
    contains code blocks that are fenced and indented configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md046", "good_both_fenced.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md046.style=indented",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD046: Code block style "
        + "[Expected: indented; Actual: fenced] (code-block-style)\n"
        + f"{source_path}:5:1: "
        + "MD046: Code block style "
        + "[Expected: indented; Actual: fenced] (code-block-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md046_good_both_indented_with_indented():
    """
    Test to make sure this rule does not trigger with a document that
    contains code blocks that are indented and indented configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md046", "good_both_indented.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md046.style=indented",
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
def test_md046_bad_fenced_and_indented_with_indented():
    """
    Test to make sure this rule does trigger with a document that
    contains code blocks that are fenced and indented and indented configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md046", "bad_fenced_and_indented.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md046.style=indented",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD046: Code block style "
        + "[Expected: indented; Actual: fenced] (code-block-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_md046_query_config():
    config_test = pluginQueryConfigTest(
        "md046",
        """
  ITEM               DESCRIPTION

  Id                 md046
  Name(s)            code-block-style
  Short Description  Code block style
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md046.md


  CONFIGURATION ITEM  TYPE    VALUE

  style               string  "consistent"

""",
    )
    execute_query_configuration_test(config_test)
