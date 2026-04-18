"""
Module to provide tests related to the MD025 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from typing import Tuple

import pytest


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", "rules", "md025", source_file_name)
    return source_path, os.path.abspath(source_path)


@pytest.mark.rules
def test_md025_bad_configuration_level(scanner_default: MarkdownScanner) -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    level value with a string that is not an integer.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_single_top_level.md")
    supplied_arguments = [
        "--set",
        "plugins.md025.level=1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md025.level' must be of type 'int'.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_good_configuration_level(scanner_default: MarkdownScanner) -> None:
    """
    Test to verify that a configuration error is not thrown when supplying the
    level value with an integer.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_single_top_level_atx.md")
    supplied_arguments = [
        "--set",
        "plugins.md025.level=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_bad_configuration_level_bad(scanner_default: MarkdownScanner) -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    level value an integer that is out of range.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_single_top_level.md")
    supplied_arguments = [
        "--set",
        "plugins.md025.level=$#0",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md025.level' is not valid: Allowable values are between 1 and 6.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_bad_configuration_front_matter_title(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    front_matter_title value with an integer that is not a string.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_single_top_level.md")
    supplied_arguments = [
        "--set",
        "plugins.md025.front_matter_title=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md025.front_matter_title' must be of type 'str'.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_good_configuration_front_matter_title(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to verify that a configuration error is not thrown when supplying the
    front_matter_title value with a valid string.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_single_top_level_atx.md")
    supplied_arguments = [
        "--set",
        "plugins.md025.front_matter_title=subject",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_bad_configuration_front_matter_title_bad(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    front_matter_title value with an invalid string.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_single_top_level.md")
    supplied_arguments = [
        "--set",
        "plugins.md025.front_matter_title=",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md025.front_matter_title' is not valid: Empty strings are not allowable values.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_bad_configuration_front_matter_title_invalid(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    front_matter_title value with an invalid string.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_single_top_level.md")
    supplied_arguments = [
        "--set",
        "plugins.md025.front_matter_title=a:b",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md025.front_matter_title' is not valid: Colons (:) are not allowed in the value.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_good_single_top_level_atx(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a single top level Atx Heading.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_single_top_level_atx.md")
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
def test_md025_good_single_top_level_setext(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a single top level SetExt Heading.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_single_top_level_setext.md")
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
def test_md025_bad_top_level_atx_top_level_atx(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two top level Atx Headings.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_top_level_atx_top_level_atx.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:5:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_bad_top_level_atx_top_level_setext(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a top level Atx Heading and a top level SetExt Heading.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_top_level_atx_top_level_setext.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md003,md024",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:5:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_bad_top_level_setext_top_level_setext(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two top level SetExt Headings.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_top_level_setext_top_level_setext.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:6:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_bad_top_level_setext_top_level_atx(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a top level SetExt Heading and an top level Atx heading.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_top_level_setext_top_level_atx.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md003,md024",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:6:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_good_front_matter_title(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains only a front-matter title.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_front_matter_title.md")
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_bad_front_matter_title_top_level_atx(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a front-matter title and a top level Atx Heading.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_front_matter_title_top_level_atx.md"
    )
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:7:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_bad_front_matter_title_top_level_setext(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a front-matter title and a top level SetExt Heading.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_front_matter_title_top_level_setext.md",
    )
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:7:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md025_query_config() -> None:
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
