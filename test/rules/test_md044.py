"""
Module to provide tests related to the MD044 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md044_bad_configuration_names():
    """
    Test to verify that a configuration error is thrown when supplying the
    names value with an integer that is not a string.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_paragraph_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md044.names' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_bad_configuration_names_empty_elements():
    """
    Test to verify that a configuration error is thrown when supplying the
    names value with a string with empty elements.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_paragraph_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=,,",
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
def test_md044_bad_configuration_names_repeated_elements():
    """
    Test to verify that a configuration error is thrown when supplying the
    names value with a string with repeated elements.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_paragraph_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=one,two,One",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "Element `One` is already present in the list as `one`."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_bad_configuration_code_blocks():
    """
    Test to verify that a configuration error is thrown when supplying the
    code_blocks value with a string instead of a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_paragraph_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.code_blocks=one",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md044.code_blocks' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_paragraph_text():
    """
    Test to make sure this rule does not trigger with a document that
    contains normal paragraphs containing the word with proper capitalization.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_paragraph_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=paragraph",
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
def test_md044_bad_paragraph_text():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing the word with configuration
    to specify proper capitalization.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_paragraph_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_paragraph_text_prefix():
    """
    Test to make sure this rule does not trigger with a document that
    contains normal paragraphs containing the word with improper capitalization
    and a prefix, and configuration to match the main word.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_paragraph_text_prefix.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
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
def test_md044_good_paragraph_text_suffix():
    """
    Test to make sure this rule does not trigger with a document that
    contains normal paragraphs containing the word with improper capitalization
    and a suffix, and configuration to match the main word.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_paragraph_text_suffix.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
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
def test_md044_bad_paragraph_text_start():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing the word with improper capitalization
    and configuration to match the main word, where it occurs at the very
    start of the line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_paragraph_text_start.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_bad_paragraph_text_end():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing the word with improper capitalization
    and configuration to match the main word, where it occurs at the very
    end of the paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_paragraph_text_end.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:20: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_bad_paragraph_text_followed_non_alpha():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing the word with improper capitalization
    and configuration to match the main word, where it is followed by non-alpha
    characters.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md044",
        "good_paragraph_text_followed_non_alpha.md",
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_bar_paragraph_text_multiples():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_paragraph_text_multiples.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:1:26: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_bar_paragraph_text_multiples_on_multiple_lines():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md044",
        "good_paragraph_text_multiples_on_multiple_lines.md",
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:33: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:3:39: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_bar_atx_heading_text():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    an Atx Heading element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_atx_heading_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:27: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:3:8: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_bad_setext_heading_text():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a SetExt Heading element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_setext_heading_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:25: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:4:8: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_bad_indented_code_block_text():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    an Indented Code Block element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_indented_code_block_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:27: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:3:12: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_bad_fenced_code_block_text():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a Fenced Code Block element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_fenced_code_block_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:27: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:4:8: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_indented_code_block_text():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    an Indented Code Block element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_indented_code_block_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "--set",
        "plugins.md044.code_blocks=$!False",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:27: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_fenced_code_block_text():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a Fenced Code Block element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_fenced_code_block_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "--set",
        "plugins.md044.code_blocks=$!False",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:27: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_html_block_text():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a HTML Block element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_html_block_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:27: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:4:8: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_block_quote_text():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a Block Quote element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_block_quote_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:27: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:3:10: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_code_span_text():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a Code Span element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_code_span_text.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:27: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:3:7: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_code_span_text_multiple_lines():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a Code span element that is over multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_code_span_text_multiple_lines.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:27: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:3:7: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:4:6: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_inline_link():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    an Inline Link element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_inline_link.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:4: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:1:41: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_inline_link_multiple_lines_x():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    an Inline Link element over multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_inline_link_multiple_lines.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:4: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:3:2: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_inline_link_multiple_lines_two():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    an Inline Link element over multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_inline_link_multiple_lines_two.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:4: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:4:13: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_inline_link_multiple_lines_three():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    an Inline Line element over multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md044",
        "good_inline_link_multiple_lines_three.md",
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:4:2: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_inline_image():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    an Inline Image element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_inline_image.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:5: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:1:42: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_inline_image_multiple_lines():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    an Inline Image element over multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_inline_image_multiple_lines.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:5: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:3:2: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_inline_image_multiple_lines_two():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    an Inline Image element over multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_inline_image_multiple_lines_two.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:5: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:4:13: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_full_link():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a Full Link element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_full_link.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:4: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:5:16: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_full_link_multiple():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a Full Link element over multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_full_link_multiple.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:9:1: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_full_image():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a Full Image element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_full_image.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:5: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:5:16: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_full_image_multiple():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a Full Image element over multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_full_image_multiple.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:9:1: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_collapsed_link():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a Collapsed Link element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_collapsed_link.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:7:1: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:7:21: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_collapsed_link_multiple():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a Collapsed Link element over multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_collapsed_link_multiple.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:6: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:7:6: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:8:5: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_collapsed_image():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a Collapsed Image element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_collapsed_image.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:7:1: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:7:21: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md044_good_collapsed_image_multiple():
    """
    Test to make sure this rule does trigger with a document that
    contains normal paragraphs containing multiples of the word with
    improper capitalization and configuration to match, some within
    a Collapsed Image element over multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md044", "good_collapsed_image_multiple.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=ParaGraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:7:1: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)\n"
        + f"{source_path}:8:5: "
        + "MD044: Proper names should have the correct capitalization "
        + "[Expected: ParaGraph; Actual: paragraph] (proper-names)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_md044_query_config():
    config_test = pluginQueryConfigTest(
        "md044",
        """
  ITEM               DESCRIPTION

  Id                 md044
  Name(s)            proper-names
  Short Description  Proper names should have the correct capitalization
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md044.md


  CONFIGURATION ITEM  TYPE     VALUE

  code_blocks         boolean  True
  names               string   ""

""",
    )
    execute_query_configuration_test(config_test)
