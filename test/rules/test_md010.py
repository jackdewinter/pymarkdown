"""
Module to provide tests related to the MD010 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import (
    assert_file_is_as_expected,
    copy_to_temp_file,
    read_contents_of_text_file,
)
from typing import Dict

import pytest

from pymarkdown.general.tab_helper import TabHelper


def generate_expected_contents(
    temp_source_path: str, allowed_after_indent_map: Dict[int, int] = None
) -> str:
    """
    Given the source file, make any required changes to the file outside of the
    plugin.
    """
    existing_file_contents = read_contents_of_text_file(temp_source_path)
    # print("---\n" + existing_file_contents.replace("\n", "\\n").replace("\t", "\\t") + "\n---")
    new_lines = []
    split_lines = existing_file_contents.splitlines(keepends=True)
    for next_line_index, next_line in enumerate(split_lines):
        if allowed_after_indent_map and next_line_index + 1 in allowed_after_indent_map:
            modify_after_index = allowed_after_indent_map[next_line_index + 1]
            altered_line = (
                TabHelper.detabify_string(next_line[:modify_after_index])
                + next_line[modify_after_index:]
            )
        else:
            altered_line = TabHelper.detabify_string(next_line)
        new_lines.append(altered_line)
    expected_file_contents = "".join(new_lines)
    # print("---\n" + expected_file_contents.replace("\n", "\\n").replace("\t", "\\t") + "\n---")
    return expected_file_contents


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
        + f"{source_path}:3:22: MD010: "
        + "Hard tabs [Column: 22] (no-hard-tabs)\n"
        + f"{source_path}:4:2: MD010: "
        + "Hard tabs [Column: 2] (no-hard-tabs)\n"
        + f"{source_path}:4:7: MD010: "
        + "Hard tabs [Column: 7] (no-hard-tabs)\n"
        + f"{source_path}:4:12: MD010: "
        + "Hard tabs [Column: 12] (no-hard-tabs)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md010_bad_simple_text_with_tab_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains tab characters.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test", "resources", "rules", "md010", "bad_simple_text_with_tab.md"
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
        expected_file_contents = generate_expected_contents(temp_source_path)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md010_bad_simple_text_with_tab_fix_and_debug():
    """
    Test to make sure this rule does trigger with a document that
    contains tab characters.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test", "resources", "rules", "md010", "bad_simple_text_with_tab.md"
        )
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md009",
            "-x-fix-debug",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = """md010-before:before-tab\\tafter-tab:
md010-after :before-tab  after-tab:
md047-before:before-tab  after-tab:
nl-ltw:before-tab  after-tab\\n:
md010-before:before-tab\\tafter-tab:
md010-after :before-tab  after-tab:
md047-before:before-tab  after-tab:
nl-ltw:before-tab  after-tab\\n:
md010-before:before-tab\\tafter-tab\\tafter-another:
md010-after :before-tab  after-tab   after-another:
md047-before:before-tab  after-tab   after-another:
nl-ltw:before-tab  after-tab   after-another\\n:
md010-before:a\\tbb\\tccc\\tddd:
md010-after :a   bb  ccc ddd:
md047-before:a   bb  ccc ddd:
nl-ltw:a   bb  ccc ddd\\n:
md010-before::
md047-before::
was_newline_added_at_end_of_file=True
fixed:a   bb  ccc ddd\\n:
is_line_empty=True
was_modified=True
nl-ltw::
FixLineRecord(source='next_line', line_number=1, plugin_id='md010')
FixLineRecord(source='next_line', line_number=2, plugin_id='md010')
FixLineRecord(source='next_line', line_number=3, plugin_id='md010')
FixLineRecord(source='next_line', line_number=4, plugin_id='md010')
Fixed: {path}""".replace(
            "{path}", temp_source_path
        )
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
def test_md010_bad_simple_text_with_tabs_in_code_block_with_end_line():
    """
    Test to make sure this rule fires when the code block end is followed
    by a blank line, or any other token.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md010",
        "bad_simple_text_with_tabs_in_code_block.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:4:5: MD010: Hard tabs [Column: 5] (no-hard-tabs)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md010_bad_simple_text_with_tabs_in_code_block_no_end_line():
    """
    Test to make sure this rule fires when the code block end token is
    the "last" token (except for the end of stream token).
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md010",
        "bad_simple_text_with_tabs_in_code_block_no_end_line.md",
    )
    supplied_arguments = [
        "-d",
        "MD041,MD047",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:4:5: MD010: Hard tabs [Column: 5] (no-hard-tabs)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md010_bad_simple_text_with_tabs_in_code_block_turned_off():
    """
    Test to make sure this rule fires for a tab within a code block,
    when the code blocks setting is turned off.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md010",
        "bad_simple_text_with_tabs_in_code_block.md",
    )
    supplied_arguments = [
        "--set",
        "plugins.md010.code_blocks=$!false",
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
def test_md010_bad_simple_text_with_tabs_in_code_block_turned_off_and_fix():
    """
    Test to make sure this rule fires for a tab within a code block,
    when the code blocks setting is turned off.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md010",
            "bad_simple_text_with_tabs_in_code_block.md",
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

        expected_return_code = 0
        expected_output = ""
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
