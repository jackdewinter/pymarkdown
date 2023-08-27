"""
Module to provide tests related to the MD010 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.test_md010 import generate_expected_contents
from test.utils import assert_file_is_as_expected, copy_to_temp_file

import pytest


@pytest.mark.rules
def test_md010_bad_unordered_list_fall_off_after_fenced_open():
    """
    Test to make sure this rule fires properly for a fenced code block
    that is started within an unordered list, but is then closed before
    any text can be placed in the code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md010",
        "bad_unordered_list_fall_off_after_fenced_open.md",
    )
    supplied_arguments = [
        "-d",
        "md031,md040,md041",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)\n"
        + f"{source_path}:4:16: MD010: Hard tabs [Column: 16] (no-hard-tabs)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md010_bad_unordered_list_fall_off_after_fenced_open_and_text():
    """
    Test to make sure this rule fires properly for a fenced code block
    that is started within an unordered list and has text in the code
    block, but is then closed without using an end code block sequence.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md010",
        "bad_unordered_list_fall_off_after_fenced_open_and_text.md",
    )
    supplied_arguments = [
        "-d",
        "md031,md040,md041",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md010_bad_unordered_list_fall_off_after_fenced_open_and_text_and_close():
    """
    Test to make sure this rule fires properly for a fenced code block
    that is started, has text, and is properly closed, all within an
    unordered list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md010",
        "bad_unordered_list_fall_off_after_fenced_open_and_text_and_close.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md010_bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_and_fix():
    """
    Test to make sure this rule fires properly for a fenced code block
    that is started, has text, and is properly closed, all within an
    unordered list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md010",
            "bad_unordered_list_fall_off_after_fenced_open_and_text_and_close.md",
        )
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        allowed_after_indent_map = {}
        allowed_after_indent_map[4] = 2
        expected_file_contents = generate_expected_contents(
            temp_source_path, allowed_after_indent_map
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md010_bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_code_blocks_off():
    """
    Test to make sure this rule fires properly for a fenced code block
    that is started, has text, and is properly closed, all within an
    unordered list item, but with code blocks turned off.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md010",
        "bad_unordered_list_fall_off_after_fenced_open_and_text_and_close.md",
    )
    supplied_arguments = [
        "--set",
        "plugins.md010.code_blocks=$!false",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)\n"
        + f"{source_path}:4:16: MD010: Hard tabs [Column: 16] (no-hard-tabs)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md010_bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_code_blocks_off_and_fix():
    """
    Test to make sure this fires properly for a tab in a code block within an
    unordered list.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md010",
            "bad_unordered_list_fall_off_after_fenced_open_and_text_and_close.md",
        )
    ) as temp_source_path:
        supplied_arguments = [
            "--set",
            "plugins.md010.code_blocks=$!false",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = generate_expected_contents(temp_source_path)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md010_bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_space_indent():
    """
    Test to make sure we handle things properly in an unordered list that
    uses spaces for the ident.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md010",
        "bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_space_indent.md",
    )
    supplied_arguments = [
        "-d",
        "md030,md041",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:12: MD010: Hard tabs [Column: 12] (no-hard-tabs)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md010_bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_space_indent_and_fix():
    """
    Test to make sure we handle things properly in an unordered list that
    uses spaces for the ident.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md010",
            "bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_space_indent.md",
        )
    ) as temp_source_path:
        supplied_arguments = [
            "-d",
            "md030,md041",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        allowed_after_indent_map = {}
        allowed_after_indent_map[4] = 2
        expected_file_contents = generate_expected_contents(
            temp_source_path, allowed_after_indent_map
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md010_bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_tab_indent():
    """
    Test to make sure we handle things properly in an unordered list that
    uses tabs for the ident.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md010",
        "bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_tab_indent.md",
    )
    supplied_arguments = [
        "--stack-trace",
        "-d",
        "md030,md041",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)\n"
        + f"{source_path}:3:1: MD010: Hard tabs [Column: 1] (no-hard-tabs)\n"
        + f"{source_path}:3:12: MD010: Hard tabs [Column: 12] (no-hard-tabs)\n"
        + f"{source_path}:5:1: MD010: Hard tabs [Column: 1] (no-hard-tabs)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md010_bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_tab_indent_and_fix():
    """
    Test to make sure we handle things properly in an unordered list that
    uses tabs for the ident.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md010",
            "bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_tab_indent.md",
        )
    ) as temp_source_path:
        supplied_arguments = [
            "--stack-trace",
            "-d",
            "md030,md041",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        allowed_after_indent_map = {}
        allowed_after_indent_map[4] = 0
        expected_file_contents = generate_expected_contents(
            temp_source_path, allowed_after_indent_map
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)
