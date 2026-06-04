"""
Module to provide tests related to the MD045 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from test.utils import create_temporary_markdown_file
from typing import Tuple

import pytest


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", "rules", "md045", source_file_name)
    return source_path, os.path.abspath(source_path)


@pytest.mark.rules
def test_md045_good_inline_image(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains inline images with alt text.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_inline_image.md")
    supplied_arguments = [
        "--set",
        "plugins.md044.names=paragraph",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md045_bad_inline_image(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains inline images with no alt text.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_inline_image.md")
    supplied_arguments = [
        "--set",
        "plugins.md044.names=paragraph",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD045: Images should have alternate text (alt text) (no-alt-text)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md045_bad_inline_image_whitespace_only(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains inline images with alt text that is whitespace only.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_inline_image_whitespace_only.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md039",
        "--set",
        "plugins.md044.names=paragraph",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD045: Images should have alternate text (alt text) (no-alt-text)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md045_bad_inline_image_whitespace_only_2(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains inline images with alt text that is whitespace only.
    """

    # Arrange
    source_contents = """![\u00a0](image.png])
"""

    with create_temporary_markdown_file(source_contents) as source_path:
        supplied_arguments = [
            "--disable-rules",
            "md039",
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:1:1: MD045: Images should have alternate text (alt text) (no-alt-text)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md045_good_full_image(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains full images with alt text.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_full_image.md")
    supplied_arguments = [
        "--set",
        "plugins.md044.names=paragraph",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md045_bad_full_image(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains full images with not alt text.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_full_image.md")
    supplied_arguments = [
        "--set",
        "plugins.md044.names=paragraph",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD045: Images should have alternate text (alt text) (no-alt-text)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md045_good_shortcut_image(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains shortcut images with alt text.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_shortcut_image.md")
    supplied_arguments = [
        "--set",
        "plugins.md044.names=paragraph",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md045_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md045",
        """
  ITEM               DESCRIPTION

  Id                 md045
  Name(s)            no-alt-text
  Short Description  Images should have alternate text (alt text)
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md045.md

""",
    )
    execute_query_configuration_test(config_test)
