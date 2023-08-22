"""
Module to provide tests related to the MD009 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.rules.test_md009 import generate_md009_expected_contents
from test.utils import assert_file_is_as_expected, copy_to_temp_file

import pytest


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
def test_md009_good_paragraph_no_extra_fix():
    """
    Test to make sure this rule does not trigger with a document that
    has no trailing spaces at the end of lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test", "resources", "rules", "md009", "good_paragraph_no_extra.md"
        )
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
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
def test_md009_good_indented_code_block_with_extra_fix():
    """
    Test to make sure this rule does not trigger with a document that
    has trailing spaces inside of an indented code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md009",
            "good_indented_code_block_with_extra.md",
        )
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
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
def test_md009_good_fenced_code_block_with_extra_fix():
    """
    Test to make sure this rule does not trigger with a document that
    has trailing spaces inside of a fenced code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md009",
            "good_fenced_code_block_with_extra.md",
        )
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
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
def test_md009_good_unordered_list_item_empty_lines_fix():
    """
    Test to make sure this rule does not trigger with a document that
    has trailing spaces at the end of a blank line within a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md009",
            "good_unordered_list_item_empty_lines.md",
        )
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
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
def test_md009_good_unordered_list_item_empty_lines_with_config_strict_fix():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end of a blank line within a list item,
    but with strict configuration enabled.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md009",
            "good_unordered_list_item_empty_lines.md",
        )
    ) as temp_source_path:
        supplied_arguments = [
            "--set",
            "plugins.md009.strict=$!True",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = generate_md009_expected_contents(temp_source_path, 2)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


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
def test_md009_good_unordered_list_item_empty_lines_with_config_strict_and_list_empty_fix():
    """
    Test to make sure this rule does not trigger with a document that
    has trailing spaces at the end of a blank line within a list item,
    with strict and list item empty lines configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md009",
            "good_unordered_list_item_empty_lines.md",
        )
    ) as temp_source_path:
        supplied_arguments = [
            "--set",
            "plugins.md009.strict=$!True",
            "--set",
            "plugins.md009.list_item_empty_lines=$!True",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
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


@pytest.mark.rules
def test_md009_good_ordered_list_item_empty_lines_with_list_empty_fix():
    """
    Test to make sure this rule does not trigger with a document that
    has trailing spaces at the end of a blank line within a list item,
    with list item empty lines configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md009",
            "good_unordered_list_item_empty_lines.md",
        )
    ) as temp_source_path:
        supplied_arguments = [
            "--set",
            "plugins.md009.list_item_empty_lines=$!True",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
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
