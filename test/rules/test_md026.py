"""
Module to provide tests related to the MD026 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from test.utils import create_temporary_configuration_file
from typing import Tuple

import pytest


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", "rules", "md026", source_file_name)
    return source_path, os.path.abspath(source_path)


@pytest.mark.rules
def test_md026_good_ends_without_punctuation_atx(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a Atx heading that does not end in punctuation.
    """

    # Arrange
    source_path, _ = __generate_source_path("ends_without_punctuation_atx.md")
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
def test_md026_good_ends_with_entity_atx(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a Atx heading that does end in punctuation, but in entity form.
    """

    # Arrange
    source_path, _ = __generate_source_path("ends_with_entity_atx.md")
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
def test_md026_bad_ends_with_punctuation_atx(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a Atx heading that does end in punctuation.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "ends_with_punctuation_atx.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:18: MD026: Trailing punctuation present in heading text. (no-trailing-punctuation)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md026_good_ends_with_punctuation_then_inline_atx(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a Atx heading that ends in punctuation followed by emphasis.
    """

    # Arrange
    source_path, _ = __generate_source_path(
        "ends_with_punctuation_then_inline_atx.md",
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
def test_md026_good_ends_with_punctuation_atx_with_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a Atx heading that does end in punctuation, but with configuration
    to compensate.
    """

    # Arrange
    source_path, _ = __generate_source_path("ends_with_punctuation_atx.md")
    supplied_configuration = {"plugins": {"md026": {"punctuation": "?!"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults()

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md026_good_ends_without_punctuation_setext(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that does not end in punctuation.
    """

    # Arrange
    source_path, _ = __generate_source_path("ends_without_punctuation_setext.md")
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
def test_md026_good_ends_with_entity_setext(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that does end in punctuation, but as an entity.
    """

    # Arrange
    source_path, _ = __generate_source_path("ends_with_entity_setext.md")
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
def test_md026_bad_ends_with_punctuation_setext(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a SetExt heading that does end in punctuation.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "ends_with_punctuation_setext.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:18: MD026: Trailing punctuation present in heading text. (no-trailing-punctuation)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md026_bad_ends_with_punctuation_setext_multiline(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a SetExt heading that is multiline and does end in punctuation.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "ends_with_punctuation_setext_multiline.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:2:18: MD026: Trailing punctuation present in heading text. (no-trailing-punctuation)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md026_good_ends_with_punctuation_then_inline_setext(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that does end in punctuation and then emphasis.
    """

    # Arrange
    source_path, _ = __generate_source_path(
        "ends_with_punctuation_then_inline_setext.md",
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
def test_md026_good_ends_with_punctuation_setext_with_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that does end in punctuation, but configuration to compensate for it.
    """

    # Arrange
    source_path, _ = __generate_source_path("ends_with_punctuation_setext.md")
    supplied_configuration = {"plugins": {"md026": {"punctuation": "?!"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults()

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_md026_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md026",
        """
  ITEM               DESCRIPTION

  Id                 md026
  Name(s)            no-trailing-punctuation
  Short Description  Trailing punctuation present in heading text.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md026.md


  CONFIGURATION ITEM  TYPE    VALUE

  punctuation         string  ".,;:!。，；
                              ：！"

""",
    )
    execute_query_configuration_test(config_test)
