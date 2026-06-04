"""
Module to provide tests related to the MD036 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from test.utils import create_temporary_configuration_file
from typing import List, Tuple

import pytest


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", "rules", "md036", source_file_name)
    return source_path, os.path.abspath(source_path)


@pytest.mark.rules
def test_md036_bad_configuration_punctuation(scanner_default: MarkdownScanner) -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    punctuation value with an integer that is not a string.
    """

    # Arrange
    source_path, _ = __generate_source_path("proper_headings_atx.md")
    supplied_arguments = [
        "--set",
        "plugins.md036.punctuation=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md036.punctuation' must be of type 'str'.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md036_good_proper_headings_atx(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains valid Atx Headings and not emphasis.
    """

    # Arrange
    source_path, _ = __generate_source_path("proper_headings_atx.md")
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
def test_md036_good_proper_headings_setext(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains valid SetExt Headings and not emphasis.
    """

    # Arrange
    source_path, _ = __generate_source_path("proper_headings_setext.md")
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
def test_md036_good_proper_emphasis_with_link(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains an emphasis "heading" containing a link.
    """

    # Arrange
    source_path, _ = __generate_source_path("proper_emphasis_with_link.md")
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
def test_md036_good_proper_emphasis_with_text_then_link(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains an emphasis "heading" containing text and then a link.
    """

    # Arrange
    source_path, _ = __generate_source_path("proper_emphasis_with_text_then_link.md")
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
def test_md036_good_proper_emphasis_with_text_then_link_then_text(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains an emphasis "heading" containing text and then a link and then text.
    """

    # Arrange
    source_path, _ = __generate_source_path(
        "proper_emphasis_with_text_then_link_then_text.md",
    )
    supplied_arguments: List[str] = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md036_good_proper_emphasis_with_text_end_emphasis_more_text(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains an emphasis "heading" containing text in the emphasis and
    more text after.
    """

    # Arrange
    source_path, _ = __generate_source_path(
        "proper_emphasis_with_text_end_emphasis_more_text.md",
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
def test_md036_good_proper_emphasis_within_text(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a line containing text and emphasis within the line.
    """

    # Arrange
    source_path, _ = __generate_source_path("proper_emphasis_within_text.md")
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
def test_md036_good_proper_emphasis_within_multiline_text(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains an emphasis "heading", with the emphasis going over 2 lines.
    """

    # Arrange
    source_path, _ = __generate_source_path(
        "proper_emphasis_within_multiline_text.md",
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
def test_md036_good_proper_emphasis_ending_with_punctuation(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains an emphasis "heading" where the text ends with punctuation.
    """

    # Arrange
    source_path, x = __generate_source_path(
        "proper_emphasis_ending_with_punctuation.md",
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
def test_md036_bad_proper_emphasis_ending_with_punctuation_with_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains an emphasis "heading" ending with punctuation, but not punctuation
    according to configuration.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "proper_emphasis_ending_with_punctuation.md",
    )
    supplied_configuration = {"plugins": {"md036": {"punctuation": ".!"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{abs_source_path}:1:1: MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)
{abs_source_path}:5:1: MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md036_bad_valid_emphasis_headings(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a valid emphasis "heading".
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("valid_emphasis_headings.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)
{abs_source_path}:5:1: MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md036_bad_valid_emphasis_headings_in_list(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a valid emphasis "heading" in a list.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "valid_emphasis_headings_in_list.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:3: MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)
{abs_source_path}:5:3: MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md036_bad_valid_emphasis_headings_in_block_quote(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a valid emphasis "heading" in a block quote.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "valid_emphasis_headings_in_block_quote.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:3: MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)
{abs_source_path}:5:3: MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md036_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md036",
        """
  ITEM               DESCRIPTION

  Id                 md036
  Name(s)            no-emphasis-as-heading,no-emphasis-as-header
  Short Description  Emphasis possibly used instead of a heading element.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md036.md


  CONFIGURATION ITEM  TYPE    VALUE

  punctuation         string  ".,;:!?。，；
                              ：？"

""",
    )
    execute_query_configuration_test(config_test)
