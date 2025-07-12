"""
Module to provide tests related to the MD033 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest

import pytest


@pytest.mark.rules
def test_md033_bad_configuration_allowed_elements() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    allowed_elements value with an integer that is not a string.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_asterisk_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md033.allowed_elements=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md033.allowed_elements' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_configuration_allowed_elements_with_empty() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    allowed_elements value with an integer that is not a string.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_asterisk_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md033.allowed_elements=html,,a",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "Elements in the comma-separated list cannot be empty."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_configuration_allow_first_image_element() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    allow_first_image_element value with an integer that is not a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_asterisk_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md033.allow_first_image_element=1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md033.allow_first_image_element' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_html_block_present() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains html blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "bad_html_block_present.md"
    )
    supplied_arguments = [
        "-d",
        "PML100,MD041",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD033: Inline HTML [Element: script] (no-inline-html)\n"
        + f"{source_path}:12:1: MD033: Inline HTML [Element: ?] (no-inline-html)\n"
        + f"{source_path}:16:1: "
        + "MD033: Inline HTML "
        + "[Element: !A] (no-inline-html)\n"
        + f"{source_path}:24:1: "
        + "MD033: Inline HTML [Element: p] (no-inline-html)\n"
        + f"{source_path}:28:1: "
        + "MD033: Inline HTML [Element: robert] (no-inline-html)\n"
        + f"{source_path}:34:1: "
        + "MD033: Inline HTML [Element: robert] (no-inline-html)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_html_block_present_with_configuration() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains html blocks with emptied out allowed_elements.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "bad_html_block_present.md"
    )
    supplied_arguments = [
        "-d",
        "PML100,MD041",
        "--set",
        "plugins.md033.allowed_elements=",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD033: Inline HTML [Element: script] (no-inline-html)\n"
        + f"{source_path}:7:1: "
        + "MD033: Inline HTML "
        + "[Element: !--] (no-inline-html)\n"
        + f"{source_path}:12:1: "
        + "MD033: Inline HTML "
        + "[Element: ?] (no-inline-html)\n"
        + f"{source_path}:16:1: "
        + "MD033: Inline HTML "
        + "[Element: !A] (no-inline-html)\n"
        + f"{source_path}:20:1: "
        + "MD033: Inline HTML "
        + "[Element: ![CDATA[] (no-inline-html)\n"
        + f"{source_path}:24:1: "
        + "MD033: Inline HTML [Element: p] (no-inline-html)\n"
        + f"{source_path}:28:1: "
        + "MD033: Inline HTML [Element: robert] (no-inline-html)\n"
        + f"{source_path}:34:1: "
        + "MD033: Inline HTML [Element: robert] (no-inline-html)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_html_block_present_with_other_configuration() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains html blocks with alternate allowed_elements.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "bad_html_block_present.md"
    )
    supplied_arguments = [
        "-d",
        "PML100,MD041",
        "--set",
        "plugins.md033.allowed_elements=robert,p,!A",
        "scan",
        "test/resources/rules/md033/bad_html_block_present.md",
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD033: Inline HTML [Element: script] (no-inline-html)\n"
        + f"{source_path}:7:1: "
        + "MD033: Inline HTML "
        + "[Element: !--] (no-inline-html)\n"
        + f"{source_path}:12:1: "
        + "MD033: Inline HTML "
        + "[Element: ?] (no-inline-html)\n"
        + f"{source_path}:20:1: "
        + "MD033: Inline HTML "
        + "[Element: ![CDATA[] (no-inline-html)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_inline_html_present() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains raw html.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "bad_inline_html_present.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:9: MD033: Inline HTML [Element: a] (no-inline-html)"
    )

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_html_in_atx_heading() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains raw html in an atx heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "bad_html_in_atx_heading.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:3: "
        + "MD033: Inline HTML "
        + "[Element: foo] (no-inline-html)\n"
        + f"{source_path}:1:14: "
        + "MD033: Inline HTML "
        + "[Element: foo] (no-inline-html) "
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_good_html_comment() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains an hTML comment block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "good_html_comment.md"
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
def test_md033_good_html_image_heading() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a html block image heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "good_html_image_heading.md"
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
def test_md033_good_html_image_heading_with_config() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a html block image heading and configuration to turn
    that support off.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "good_html_image_heading.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md033.allow_first_image_element=$!false",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD033: Inline HTML "
        + "[Element: h1] (no-inline-html)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_html_heading() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a bad html block image heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "bad_html_heading.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD033: Inline HTML "
        + "[Element: h1] (no-inline-html)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_html_image_heading_blank() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a bad html block image heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "bad_html_image_heading_blank.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD033: Inline HTML "
        + "[Element: h1] (no-inline-html)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_html_image_with_other() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a bad html block image heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "bad_html_image_with_other.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD033: Inline HTML "
        + "[Element: h1] (no-inline-html)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_good_convoluted() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a weird html block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "good_convoluted.md"
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
def test_md033_bad_html_dangling() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a html block that is opened but not closed.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "bad_html_dangling.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD033: Inline HTML "
        + "[Element: h1] (no-inline-html)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_good_by_default() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains some of the weirder HTML elements, but still valid
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "good_by_default.md"
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
def test_md033_bad_html_declaration() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a HTML declaration that is not the DOCTYPE declaration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md033", "bad_html_declaration.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: MD033: Inline HTML [Element: !OTHER] (no-inline-html)"
    )

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


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
