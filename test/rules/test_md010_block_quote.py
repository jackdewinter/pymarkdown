"""
Module to provide tests related to the MD010 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.test_md010 import generate_expected_contents
from test.utils import assert_file_is_as_expected, copy_to_temp_file

import pytest


@pytest.mark.rules
def test_md010_in_block_quotes_fall_off_after_fenced_open():
    """
    Test to make sure this rule fires for a fenced code block start in a block quote
    that ends right away.  Because it ends before the "text" of the code block, the
    text is normal text, and subject to normal rules for tabs.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md010",
        "bad_block_quote_fall_off_after_fenced_open.md",
    )
    supplied_arguments = [
        "-d",
        "md031,md041,md040",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)\n"
        + f"{source_path}:4:30: MD010: Hard tabs [Column: 30] (no-hard-tabs)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md010_in_bad_block_quote_fall_off_after_fenced_open_and_text():
    """
    Test to make sure this rule fires for the open fenced block line which
    does contain a tab, but not the code block content, which also contains a tab.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md010",
        "bad_block_quote_fall_off_after_fenced_open_and_text.md",
    )
    supplied_arguments = [
        "-d",
        "md031,md041,md040",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)\n"
        + f"{source_path}:4:26: MD010: Hard tabs [Column: 26] (no-hard-tabs)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md010_in_bad_block_quote_fall_off_after_fenced_open_and_text_and_close():
    """
    Test to make sure this rule fires for the start of the fenced code block, which
    contains a tab, but not for the content.  This is different than the
    test_md010_in_bad_block_quote_fall_off_after_fenced_open_and_text function in
    that the fenced code block is closed "nicely", not by the closing of the block
    quote it is contained in.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md010",
        "bad_block_quote_fall_off_after_fenced_open_and_text_and_close.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)\n"
        + f"{source_path}:4:26: MD010: Hard tabs [Column: 26] (no-hard-tabs)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md010_in_bad_block_quote_fall_off_after_fenced_open_and_text_and_close_and_fix():
    """
    Test to make sure this rule fires for the start of the fenced code block, which
    contains a tab, but not for the content.  This is different than the
    test_md010_in_bad_block_quote_fall_off_after_fenced_open_and_text function in
    that the fenced code block is closed "nicely", not by the closing of the block
    quote it is contained in.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md010",
            "bad_block_quote_fall_off_after_fenced_open_and_text_and_close.md",
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
        # allowed_after_indent_map[4] = 0
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
