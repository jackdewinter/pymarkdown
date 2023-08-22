"""
Module to provide tests related to the MD009 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest


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
