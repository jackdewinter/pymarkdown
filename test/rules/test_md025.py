"""
Module to provide tests related to the MD025 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest

import pytest


@pytest.mark.rules
def test_md025_bad_configuration_level():
    """
    Test to verify that a configuration error is thrown when supplying the
    level value with a string that is not an integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "good_single_top_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md025.level=1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md025.level' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_good_configuration_level():
    """
    Test to verify that a configuration error is not thrown when supplying the
    level value with an integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "good_single_top_level_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md025.level=$#1",
        "--strict-config",
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
def test_md025_bad_configuration_level_bad():
    """
    Test to verify that a configuration error is thrown when supplying the
    level value an integer that is out of range.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "good_single_top_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md025.level=$#0",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md025.level' is not valid: Allowable values are between 1 and 6."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_bad_configuration_front_matter_title():
    """
    Test to verify that a configuration error is thrown when supplying the
    front_matter_title value with an integer that is not a string.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "good_single_top_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md025.front_matter_title=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md025.front_matter_title' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_good_configuration_front_matter_title():
    """
    Test to verify that a configuration error is not thrown when supplying the
    front_matter_title value with a valid string.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "good_single_top_level_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md025.front_matter_title=subject",
        "--strict-config",
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
def test_md025_bad_configuration_front_matter_title_bad():
    """
    Test to verify that a configuration error is thrown when supplying the
    front_matter_title value with an invalid string.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "good_single_top_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md025.front_matter_title=",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md025.front_matter_title' is not valid: Empty strings are not allowable values."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_bad_configuration_front_matter_title_invalid():
    """
    Test to verify that a configuration error is thrown when supplying the
    front_matter_title value with an invalid string.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "good_single_top_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md025.front_matter_title=a:b",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md025.front_matter_title' is not valid: Colons (:) are not allowed in the value."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_good_single_top_level_atx():
    """
    Test to make sure this rule does not trigger with a document that
    contains a single top level Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "good_single_top_level_atx.md"
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
def test_md025_good_single_top_level_setext():
    """
    Test to make sure this rule does not trigger with a document that
    contains a single top level SetExt Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "good_single_top_level_setext.md"
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
def test_md025_bad_top_level_atx_top_level_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains two top level Atx Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "bad_top_level_atx_top_level_atx.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:1: "
        + "MD025: Multiple top-level headings in the same document (single-title,single-h1)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_bad_top_level_atx_top_level_setext():
    """
    Test to make sure this rule does trigger with a document that
    contains a top level Atx Heading and a top level SetExt Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "bad_top_level_atx_top_level_setext.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md003",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:6:1: "
        + "MD025: Multiple top-level headings in the same document (single-title,single-h1)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_bad_top_level_setext_top_level_setext():
    """
    Test to make sure this rule does trigger with a document that
    contains two top level SetExt Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md025",
        "bad_top_level_setext_top_level_setext.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:7:1: "
        + "MD025: Multiple top-level headings in the same document (single-title,single-h1)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_bad_top_level_setext_top_level_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains a top level SetExt Heading and an top level Atx heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "bad_top_level_setext_top_level_atx.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md003",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:6:1: "
        + "MD025: Multiple top-level headings in the same document (single-title,single-h1)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_good_front_matter_title():
    """
    Test to make sure this rule does not trigger with a document that
    contains only a front-matter title.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "good_front_matter_title.md"
    )
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
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
def test_md025_bad_front_matter_title_top_level_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains a front-matter title and a top level Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md025", "bad_front_matter_title_top_level_atx.md"
    )
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:7:1: "
        + "MD025: Multiple top-level headings in the same document (single-title,single-h1)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_bad_front_matter_title_top_level_setext():
    """
    Test to make sure this rule does trigger with a document that
    contains a front-matter title and a top level SetExt Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md025",
        "bad_front_matter_title_top_level_setext.md",
    )
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:8:1: "
        + "MD025: Multiple top-level headings in the same document (single-title,single-h1)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_md025_query_config():
    config_test = pluginQueryConfigTest(
        "md025",
        """
  ITEM               DESCRIPTION

  Id                 md025
  Name(s)            single-title,single-h1
  Short Description  Multiple top-level headings in the same document
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md025.md


  CONFIGURATION ITEM  TYPE     VALUE

  level               integer  1
  front_matter_title  string   "title"

""",
    )
    execute_query_configuration_test(config_test)
