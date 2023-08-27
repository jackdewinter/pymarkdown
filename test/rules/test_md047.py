"""
Module to provide tests related to the MD047 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import (
    assert_file_is_as_expected,
    copy_to_temp_file,
    read_contents_of_text_file,
)

import pytest


@pytest.mark.rules
def test_md047_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md047 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join("test", "resources", "rules", "md047") + os.sep
    supplied_arguments = ["scan", source_path]

    expected_return_code = 1
    expected_output = (
        f"{source_path}end_with_no_blank_line.md:3:41: "
        + "MD047: Each file should end with a single newline character. "
        + "(single-trailing-newline)\n"
        + f"{source_path}end_with_no_blank_line_and_spaces.md:4:2: "
        + "MD047: Each file should end with a single newline character. "
        + "(single-trailing-newline)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md047_good_end_with_blank_line():
    """
    Test to make sure this rule does not trigger with a document that
    properly ends with a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = ["scan", source_path]

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
def test_md047_good_end_with_blank_line_fix():
    """
    Test to make sure this rule does not trigger with a document that
    properly ends with a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join("test", "resources", "rules", "md047", "end_with_blank_line.md")
    ) as temp_source_path:
        supplied_arguments = ["-x-fix", "scan", temp_source_path]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""
        expected_file_contents = read_contents_of_text_file(temp_source_path)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md047_bad_end_with_no_blank_line():
    """
    Test to make sure this rule does trigger with a document that
    does not end with a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_no_blank_line.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:41: "
        + "MD047: Each file should end with a single newline character. (single-trailing-newline)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md047_bad_end_with_no_blank_line_fix():
    """
    Test to make sure this rule does trigger with a document that
    does not end with a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join("test", "resources", "rules", "md047", "end_with_no_blank_line.md")
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = read_contents_of_text_file(temp_source_path) + "\n"

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md047_bad_end_with_blank_line_containing_spaces():
    """
    Test to make sure this rule does trigger with a document that
    ends with a line that is only whitespace.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_no_blank_line_and_spaces.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:2: "
        + "MD047: Each file should end with a single newline character. (single-trailing-newline)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md047_bad_end_with_blank_line_containing_spaces_fix():
    """
    Test to make sure this rule does trigger with a document that
    ends with a line that is only whitespace.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md047",
            "end_with_no_blank_line_and_spaces.md",
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
        expected_file_contents = read_contents_of_text_file(temp_source_path) + "\n"

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md047_bad_conflicting_changes_at_end_of_file():
    """
    Test to make sure that only one plugin can make a change to the last line.
    """

    # Arrange
    scanner = MarkdownScanner()
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_update_last_line.py"
    )
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md047",
            "end_with_no_blank_line_and_spaces.md",
        )
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "--add-plugin",
            plugin_path,
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = """BadPluginError encountered while scanning '{path}':
Plugin id 'MDE003' had a critical failure during the 'completed_file' action.""".replace(
            "{path}", temp_source_path
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md047_bad_end_with_no_blank_line_fix_and_debug():
    """
    Test to make sure this rule does trigger with a document that
    does not end with a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join("test", "resources", "rules", "md047", "end_with_no_blank_line.md")
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
        expected_output = """md010-before:# This is a test:
md047-before:# This is a test:
nl-ltw:# This is a test\\n:
md010-before::
md047-before::
nl-ltw:\\n:
md010-before:The line after this line should be blank.:
md047-before:The line after this line should be blank.:
was_newline_added_at_end_of_file=False
fixed:\\n:
is_line_empty=False
was_modified=True
nl-ltw:The line after this line should be blank.:
cf-ltw:\\n:
FixLineRecord(source='completed_file', line_number=4, plugin_id='md047')
Fixed: {path}""".replace(
            "{path}", temp_source_path
        )
        expected_error = ""
        expected_file_contents = read_contents_of_text_file(temp_source_path) + "\n"

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)
