"""
Module to provide tests related to the MD033 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from typing import Tuple

import pytest


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", "rules", "md033", source_file_name)
    return source_path, os.path.abspath(source_path)


@pytest.mark.rules
def test_md033_bad_configuration_allowed_elements(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    allowed_elements value with an integer that is not a string.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_html_image_heading.md")
    supplied_arguments = [
        "--set",
        "plugins.md033.allowed_elements=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md033.allowed_elements' must be of type 'str'.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_bad_configuration_allowed_elements_with_empty(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    allowed_elements value with an integer that is not a string.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_html_image_heading.md")
    supplied_arguments = [
        "--set",
        "plugins.md033.allowed_elements=html,,a",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while configuring plugins:
Elements in the comma-separated list cannot be empty.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_bad_configuration_allow_first_image_element(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    allow_first_image_element value with an integer that is not a boolean.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_list_asterisk_single_level.md")
    supplied_arguments = [
        "--set",
        "plugins.md033.allow_first_image_element=1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md033.allow_first_image_element' must be of type 'bool'.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_bad_html_block_present(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains html blocks.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_html_block_present.md")
    supplied_arguments = [
        "-d",
        "PML100,MD041",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:1: MD033: Inline HTML [Element: script] (no-inline-html)
{abs_source_path}:12:1: MD033: Inline HTML [Element: ?] (no-inline-html)
{abs_source_path}:16:1: MD033: Inline HTML [Element: !A] (no-inline-html)
{abs_source_path}:24:1: MD033: Inline HTML [Element: p] (no-inline-html)
{abs_source_path}:28:1: MD033: Inline HTML [Element: robert] (no-inline-html)
{abs_source_path}:34:1: MD033: Inline HTML [Element: robert] (no-inline-html)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_bad_html_block_present_with_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains html blocks with emptied out allowed_elements.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_html_block_present.md")
    supplied_arguments = [
        "-d",
        "PML100,MD041",
        "--set",
        "plugins.md033.allowed_elements=",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:1: MD033: Inline HTML [Element: script] (no-inline-html)
{abs_source_path}:7:1: MD033: Inline HTML [Element: !--] (no-inline-html)
{abs_source_path}:12:1: MD033: Inline HTML [Element: ?] (no-inline-html)
{abs_source_path}:16:1: MD033: Inline HTML [Element: !A] (no-inline-html)
{abs_source_path}:20:1: MD033: Inline HTML [Element: ![CDATA[] (no-inline-html)
{abs_source_path}:24:1: MD033: Inline HTML [Element: p] (no-inline-html)
{abs_source_path}:28:1: MD033: Inline HTML [Element: robert] (no-inline-html)
{abs_source_path}:34:1: MD033: Inline HTML [Element: robert] (no-inline-html)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_bad_html_block_present_with_other_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains html blocks with alternate allowed_elements.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_html_block_present.md")
    supplied_arguments = [
        "-d",
        "PML100,MD041",
        "--set",
        "plugins.md033.allowed_elements=robert,p,!A",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:1: MD033: Inline HTML [Element: script] (no-inline-html)
{abs_source_path}:7:1: MD033: Inline HTML [Element: !--] (no-inline-html)
{abs_source_path}:12:1: MD033: Inline HTML [Element: ?] (no-inline-html)
{abs_source_path}:20:1: MD033: Inline HTML [Element: ![CDATA[] (no-inline-html)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_bad_inline_html_present(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains raw html.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_inline_html_present.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"{abs_source_path}:3:9: MD033: Inline HTML [Element: a] (no-inline-html)",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_bad_html_in_atx_heading(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains raw html in an atx heading.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_html_in_atx_heading.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:3: MD033: Inline HTML [Element: foo] (no-inline-html)
{abs_source_path}:1:14: MD033: Inline HTML [Element: foo] (no-inline-html) """,
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_good_html_comment(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains an hTML comment block.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_html_comment.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_results=expected_results,
    )


@pytest.mark.rules
def test_md033_good_html_image_heading(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a html block image heading.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_html_image_heading.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_results=expected_results,
    )


@pytest.mark.rules
def test_md033_good_html_image_heading_with_config(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a html block image heading and configuration to turn
    that support off.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("good_html_image_heading.md")
    supplied_arguments = [
        "--set",
        "plugins.md033.allow_first_image_element=$!false",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD033: Inline HTML [Element: h1] (no-inline-html)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_bad_html_heading(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a bad html block image heading.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_html_heading.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD033: Inline HTML [Element: h1] (no-inline-html)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_bad_html_image_heading_blank(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a bad html block image heading.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_html_image_heading_blank.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:2:1: MD033: Inline HTML [Element: h1] (no-inline-html)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_bad_html_image_with_other(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a bad html block image heading.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_html_image_with_other.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD033: Inline HTML [Element: h1] (no-inline-html)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_good_convoluted(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a weird html block.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_convoluted.md")
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
def test_md033_bad_html_dangling(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a html block that is opened but not closed.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_html_dangling.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD033: Inline HTML [Element: h1] (no-inline-html)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_good_by_default(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains some of the weirder HTML elements, but still valid
    """

    # Arrange
    source_path, _ = __generate_source_path("good_by_default.md")
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
def test_md033_bad_html_declaration(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a HTML declaration that is not the DOCTYPE declaration.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_html_declaration.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"{abs_source_path}:1:1: MD033: Inline HTML [Element: !OTHER] (no-inline-html)",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md033_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md033",
        """
  ITEM               DESCRIPTION

  Id                 md033
  Name(s)            no-inline-html
  Short Description  Inline HTML
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md033.md


  CONFIGURATION ITEM         TYPE     VALUE

  allow_first_image_element  boolean  True
  allowed_elements           string   "!--,![CDATA[,!DOCTYPE"

""",
    )
    execute_query_configuration_test(config_test)
