"""
Module to provide tests related to the MD009 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md009_bad_configuration_br_spaces():
    """
    Test to verify that a configuration error is thrown when supplying the
    br_spaces value with a string that is not an integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_paragraph_no_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.br_spaces=not-integer",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md009.br_spaces' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_configuration_br_spaces_invalid():
    """
    Test to verify that a configuration error is thrown when supplying the
    br_spaces value is not an integer in the proper range.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_paragraph_no_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.br_spaces=$#-1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md009.br_spaces' is not valid: Allowable values are greater than or equal to 0."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_configuration_strict():
    """
    Test to verify that a configuration error is thrown when supplying the
    strict value with a string that is not a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_paragraph_no_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.strict=not-boolean",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md009.strict' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_configuration_list_item_empty_lines():
    """
    Test to verify that a configuration error is thrown when supplying the
    list_item_empty_lines value with a string that is not a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_paragraph_no_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.list_item_empty_lines=not-boolean",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md009.list_item_empty_lines' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_good_paragraph_no_extra():
    """
    Test to make sure this rule does not trigger with a document that
    has no trailing spaces at the end of lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_paragraph_no_extra.md"
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
def test_md009_bad_paragraph_increasing_extra():
    """
    Test to make sure this rule does trigger with a document that
    has increasing amounts of trailing spaces at the end of lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_paragraph_increasing_extra.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:18: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:3:20: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 3] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_paragraph_increasing_extra_with_config_br_spaces_3():
    """
    Test to make sure this rule does trigger with a document that
    has increasing amounts trailing spaces at the end of lines, and
    configuration set to 3.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_paragraph_increasing_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.br_spaces=$#3",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:18: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 3; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:2:19: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 3; Actual: 2] (no-trailing-spaces)\n"
        + f"{source_path}:4:17: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 3; Actual: 2] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_paragraph_increasing_extra_with_config_br_spaces_0():
    """
    Test to make sure this rule does trigger with a document that
    has increasing amounts trailing spaces at the end of lines, and
    configuration set to 0.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_paragraph_increasing_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.br_spaces=$#0",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:18: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:2:19: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 2] (no-trailing-spaces)\n"
        + f"{source_path}:3:20: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 3] (no-trailing-spaces)\n"
        + f"{source_path}:4:17: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 2] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_paragraph_increasing_extra_with_config_strict():
    """
    Test to make sure this rule does trigger with a document that
    has increasing amounts trailing spaces at the end of lines, and
    configuration set to strict.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_paragraph_increasing_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.strict=$!True",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:18: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:2:19: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 2] (no-trailing-spaces)\n"
        + f"{source_path}:3:20: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 3] (no-trailing-spaces)\n"
        + f"{source_path}:4:17: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 2] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_atx_heading_with_extra():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end of an Atx Heading element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_atx_heading_with_extra.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:32: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_setext_heading_with_extra():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end of a SetExt Heading element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_setext_heading_with_extra.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:30: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:2:22: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:3:22: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_theamtic_break_with_extra():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end of a Thematic break element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_theamtic_break_with_extra.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_good_indented_code_block_with_extra():
    """
    Test to make sure this rule does not trigger with a document that
    has trailing spaces inside of an indented code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_indented_code_block_with_extra.md"
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
def test_md009_good_fenced_code_block_with_extra():
    """
    Test to make sure this rule does not trigger with a document that
    has trailing spaces inside of a fenced code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_fenced_code_block_with_extra.md"
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
def test_md009_bad_html_block_with_extra():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces for text within a HTML block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_html_block_with_extra.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md033",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:5: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:3:3: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:4:2: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:5:5: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:6:6: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_link_reference_definition_with_extra():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces within a Link Reference Definition.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md009",
        "bad_link_reference_definition_with_extra.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:7: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:2:9: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:3:12: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_blank_lines_with_extra():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end various blank lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_blank_lines_with_extra.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md012",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:3:1: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 3] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_good_unordered_list_item_empty_lines():
    """
    Test to make sure this rule does not trigger with a document that
    has trailing spaces at the end of a blank line within a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_unordered_list_item_empty_lines.md"
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
def test_md009_good_unordered_list_item_empty_lines_with_config_strict():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end of a blank line within a list item,
    but with strict configuration enabled.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_unordered_list_item_empty_lines.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.strict=$!True",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 2] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_good_unordered_list_item_empty_lines_with_config_strict_and_list_empty():
    """
    Test to make sure this rule does not trigger with a document that
    has trailing spaces at the end of a blank line within a list item,
    with strict and list item empty lines configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_unordered_list_item_empty_lines.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.strict=$!True",
        "--set",
        "plugins.md009.list_item_empty_lines=$!True",
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
def test_md009_good_ordered_list_item_empty_lines_with_list_empty():
    """
    Test to make sure this rule does not trigger with a document that
    has trailing spaces at the end of a blank line within a list item,
    with list item empty lines configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_unordered_list_item_empty_lines.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.list_item_empty_lines=$!True",
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
