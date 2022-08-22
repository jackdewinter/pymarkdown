"""
Module to provide tests related to the MD010 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md010_bad_configuration_code_blocks():
    """
    Test to verify that a configuration error is thrown when supplying the
    code_blocks value with a string that is not a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_asterisk_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md010.code_blocks=bad",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md010.code_blocks' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md010_good_simple_text_no_tab():
    """
    Test to make sure this rule does not trigger with a document that
    contains no tab characters.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md010", "good_simple_text_no_tab.md"
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
def test_md010_bad_simple_text_with_tab():
    """
    Test to make sure this rule does trigger with a document that
    contains tab characters.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md010", "bad_simple_text_with_tab.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: MD010: "
        + "Hard tabs [Column: 11] (no-hard-tabs)\n"
        + f"{source_path}:2:11: MD010: "
        + "Hard tabs [Column: 11] (no-hard-tabs)\n"
        + f"{source_path}:3:11: MD010: "
        + "Hard tabs [Column: 11] (no-hard-tabs)\n"
        + f"{source_path}:3:21: MD010: "
        + "Hard tabs [Column: 21] (no-hard-tabs)\n"
        + f"{source_path}:4:2: MD010: "
        + "Hard tabs [Column: 2] (no-hard-tabs)\n"
        + f"{source_path}:4:5: MD010: "
        + "Hard tabs [Column: 5] (no-hard-tabs)\n"
        + f"{source_path}:4:9: MD010: "
        + "Hard tabs [Column: 9] (no-hard-tabs)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
