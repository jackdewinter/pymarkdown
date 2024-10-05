"""
Module for directly using PyMarkdown's scan api.
"""

import os
import tempfile
from test.utils import (
    assert_if_lists_different,
    assert_that_exception_is_raised,
    write_temporary_configuration,
)

import pytest

from pymarkdown.api import (
    PyMarkdownApi,
    PyMarkdownApiArgumentException,
    PyMarkdownApiException,
    PyMarkdownApiNoFilesFoundException,
    PyMarkdownPragmaError,
    PyMarkdownScanFailure,
)


def test_api_scan_bad_path_to_scan():
    """
    Test to make sure that an empty path to scan is reported as an error.
    """

    # Arrange
    source_path = ""

    expected_output = "Parameter named 'path_to_scan' cannot be empty."

    # Act & Assert
    caught_exception = assert_that_exception_is_raised(
        PyMarkdownApiArgumentException,
        expected_output,
        PyMarkdownApi().scan_path,
        source_path,
    )

    # Assert
    assert caught_exception.argument_name == "path_to_scan"


def test_api_scan_bad_alternate_extensions():
    """
    Test to make sure that a bad list of alternate extensions is reported as an error.
    """

    # Arrange
    source_path = "something"
    alternate_extensions = "not-a-valid-extension"

    expected_output = "Parameter named 'alternate_extensions' is not a valid comma-separated list of extensions."

    # Act & Assert
    caught_exception = assert_that_exception_is_raised(
        PyMarkdownApiArgumentException,
        expected_output,
        PyMarkdownApi().scan_path,
        source_path,
        alternate_extensions=alternate_extensions,
    )

    # Assert
    assert caught_exception.argument_name == "alternate_extensions"


def test_api_scan_simple_clean():
    """
    Test to make sure that we can invoke a scan of a file that scans cleanly.

    This function is an API version of the function
    test_markdown_with_dash_dash_log_level_info_with_file.
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )

    # Act
    scan_result = PyMarkdownApi().scan_path(source_path)

    # Assert
    assert scan_result
    assert not scan_result.scan_failures
    assert not scan_result.pragma_errors


def test_api_scan_for_non_existant_file():
    """
    Test to make sure that scanning for a non-existant file returns a
    reproducible result.

    This function is an API version of the function
    test_markdown_without_direct_args.
    """

    # Arrange
    source_path = "does-not-exist.md"

    expected_output = f"Provided path '{source_path}' does not exist."

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiNoFilesFoundException,
        expected_output,
        PyMarkdownApi().scan_path,
        source_path,
    )


def test_api_scan_for_non_matching_glob():
    """
    Test to make sure that scanning for a glob that does not match
    anything produces a predictable result.

    This function is an API version of the function
    test_markdown_with_dash_l_on_non_matching_globbed_files.
    """

    # Arrange
    source_path = os.path.join("test", "resources", "rules", "md001", "z*.md")

    expected_output = f"Provided glob path '{source_path}' did not match any files."

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiNoFilesFoundException,
        expected_output,
        PyMarkdownApi().scan_path,
        source_path,
    )


def test_api_scan_for_non_markdown_file():
    """
    Test to make sure that scanning for a file that does not have markdown
    extension produces reliable results.

    This function is an API version of the function
    test_markdown_with_dash_l_on_non_md_file.
    """

    # Arrange
    source_path = os.path.join("test", "resources", "rules", "md001", "z*.md")

    expected_output = f"Provided glob path '{source_path}' did not match any files."

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiNoFilesFoundException,
        expected_output,
        PyMarkdownApi().scan_path,
        source_path,
    )


def test_api_scan_for_non_markdown_file_with_alternate_extensions():
    """
    Test to make sure that scanning for a file that does not have markdown
    extension but with alternate extensions enabled produces reliable results.

    This function is an API version of the function
    test_api_list_for_non_markdown_file_with_alternate_extensions.
    """

    # Arrange
    source_path = os.path.join("test", "resources", "only-text", "simple_text_file.txt")
    alternate_extensions = ".txt,.md"

    # Act
    scan_result = PyMarkdownApi().scan_path(
        source_path, alternate_extensions=alternate_extensions
    )

    # Assert
    assert scan_result
    assert not scan_result.scan_failures
    assert not scan_result.pragma_errors


@pytest.mark.timeout(30)
def test_api_scan_recursive_for_directory():
    """
    Test to make sure that scanning a directory gives predictable results.

    This function is an API version of the function
    test_markdown_with_dash_l_and_dash_r_on_directory.
    """

    # Arrange
    base_path = os.path.join("docs")
    docs_prefix = "docs" + os.sep
    extensions_prefix = docs_prefix + "extensions" + os.sep
    rules_prefix = docs_prefix + "rules" + os.sep
    expected_failure_paths = [
        f"{docs_prefix}advanced_configuration.md",
        f"{docs_prefix}advanced_scanning.md",
        f"{docs_prefix}api-usage.md",
        f"{docs_prefix}api.md",
        f"{docs_prefix}developer.md",
        f"{extensions_prefix}front-matter.md",
        f"{docs_prefix}old_README.md",
        f"{docs_prefix}pre-commit.md",
        f"{rules_prefix}rule_md001.md",
        f"{rules_prefix}rule_md002.md",
        f"{rules_prefix}rule_md003.md",
        f"{rules_prefix}rule_md004.md",
        f"{rules_prefix}rule_md009.md",
        f"{rules_prefix}rule_md013.md",
        f"{rules_prefix}rule_md024.md",
        f"{rules_prefix}rule_md025.md",
        f"{rules_prefix}rule_md026.md",
        f"{rules_prefix}rule_md029.md",
        f"{rules_prefix}rule_md030.md",
        f"{rules_prefix}rule_md031.md",
        f"{rules_prefix}rule_md033.md",
        f"{rules_prefix}rule_md036.md",
        f"{rules_prefix}rule_md038.md",
        f"{rules_prefix}rule_md041.md",
        f"{rules_prefix}rule_md043.md",
        f"{rules_prefix}rule_md044.md",
        f"{rules_prefix}rule_md046.md",
        f"{rules_prefix}rule_md048.md",
        f"{rules_prefix}rule_pml100.md",
    ]

    # Act
    scan_result = (
        PyMarkdownApi()
        .set_integer_property("plugins.md013.line_length", 100)
        .scan_path(base_path, recurse_if_directory=True)
    )

    # Assert
    assert scan_result

    itemized_scan_failures = ""
    for i in scan_result.scan_failures:
        itemized_scan_failures = itemized_scan_failures + "\n" + str(i)
    print(itemized_scan_failures)
    assert len(scan_result.scan_failures) == 99

    scan_failures = []
    for i in scan_result.scan_failures:
        if i.scan_file not in scan_failures:
            scan_failures.append(i.scan_file)
    scan_failures.sort()
    assert_if_lists_different(scan_failures, expected_failure_paths)


def test_api_scan_with_multiple_scan_issues():
    """
    Test to make sure that we can handle multiple scan issues within
    a given file.

    This function is an API version of the function
    test_md020_bad_single_paragraph_with_whitespace_at_end
    """

    # Arrange
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md020",
        "single_paragraph_with_whitespace_at_end.md",
    )

    # Act
    scan_result = PyMarkdownApi().scan_path(source_path)

    # Assert
    assert scan_result
    assert len(scan_result.scan_failures) == 6
    print(scan_result.scan_failures)
    assert scan_result.scan_failures[0].partial_equals(
        PyMarkdownScanFailure(source_path, 1, 1, "MD022", "", "", None)
    )
    assert scan_result.scan_failures[1].partial_equals(
        PyMarkdownScanFailure(source_path, 1, 12, "MD010", "", "", None)
    )
    assert scan_result.scan_failures[2].partial_equals(
        PyMarkdownScanFailure(source_path, 2, 2, "MD021", "", "", None)
    )
    assert scan_result.scan_failures[3].partial_equals(
        PyMarkdownScanFailure(source_path, 2, 2, "MD022", "", "", None)
    )
    assert scan_result.scan_failures[4].partial_equals(
        PyMarkdownScanFailure(source_path, 2, 2, "MD023", "", "", None)
    )
    assert scan_result.scan_failures[5].partial_equals(
        PyMarkdownScanFailure(source_path, 2, 14, "MD010", "", "", None)
    )

    # TODO, same, but disable rules

    # TODO another one, where have to enable rules


def test_api_scan_with_pragma_failure():
    """
    Test to make sure that we can handle a case where we specify a pragma,
    but do not specify a command.  Because the pragma was not successful,
    the MD019 rule is triggered.

    This function is an API version of the function test_pragmas_01.
    """

    # Arrange
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_no_command.md",
    )

    # Act
    scan_result = PyMarkdownApi().scan_path(source_path)

    # Assert
    assert scan_result
    assert len(scan_result.scan_failures) == 1
    assert scan_result.scan_failures[0].partial_equals(
        PyMarkdownScanFailure(source_path, 2, 1, "MD019", "", "", None)
    )
    assert len(scan_result.pragma_errors) == 1
    assert scan_result.pragma_errors[0] == PyMarkdownPragmaError(
        source_path, 1, "Inline configuration specified without command."
    )


def test_api_with_good_pragma():
    """
    Test to make sure that we can handle a case where we specify a valid pragma
    that disabled the Md019 rule on the line following it.  This is a version of
    the test_api_scan_with_pragma_failure function, but where the disabling
    succeeds, so no rule is triggered.

    This function is an API version of the function test_pragmas_05.
    """

    # Arrange
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_id.md",
    )

    # Act
    scan_result = PyMarkdownApi().scan_path(source_path)

    # Assert
    assert scan_result
    assert not scan_result.scan_failures
    assert not scan_result.pragma_errors


def test_api_scan_string_test():
    """
    Test to make sure that an empty path to scan is reported as an error.
    """

    # Arrange
    source_string = "bob"
    source_path = "in-memory"

    # Act
    scan_result = PyMarkdownApi().scan_string(source_string)

    # Assert
    assert scan_result
    assert len(scan_result.scan_failures) == 2
    assert scan_result.scan_failures[0].partial_equals(
        PyMarkdownScanFailure(source_path, 1, 1, "MD041", "", "", None)
    )
    assert scan_result.scan_failures[1].partial_equals(
        PyMarkdownScanFailure(source_path, 1, 3, "MD047", "", "", None)
    )
    assert not scan_result.pragma_errors


def test_api_scan_string_test_good_file_after_disables():
    """
    Test to make sure that an empty path to scan is reported as an error.

    This function shadows
    test_markdown_with_config_general_command_line
    """

    # Arrange
    source_string = """# This is a document

* a list
  - a sublist
  - a very long sublist item

this is a very long line
"""

    # Act
    scan_result = (
        PyMarkdownApi().disable_rule_by_identifier("md004").scan_string(source_string)
    )

    # Assert
    assert scan_result
    assert not scan_result.scan_failures
    assert not scan_result.pragma_errors


def test_api_scan_string_test_bad_file_due_to_no_disables():
    """
    Test to make sure that an empty path to scan is reported as an error.

    This function shadows
    test_markdown_with_config_no_config
    """

    # Arrange
    source_string = """# This is a document

* a list
  - a sublist
  - a very long sublist item

this is a very long line
"""
    source_path = "in-memory"

    # Act
    scan_result = PyMarkdownApi().scan_string(source_string)

    # Assert
    assert scan_result
    assert len(scan_result.scan_failures) == 1
    assert scan_result.scan_failures[0].partial_equals(
        PyMarkdownScanFailure(source_path, 4, 3, "MD004", "", "", None)
    )
    assert not scan_result.pragma_errors


def test_api_fix_string_simple_clean():
    """
    Test to make sure that we can invoke a fix of a file with no issues.
    """

    # Arrange
    string_to_scan = """# This is a test

The line after this line should be blank.
"""

    # Act
    scan_result = PyMarkdownApi().fix_string(string_to_scan)

    # Assert
    assert not scan_result.was_fixed
    assert string_to_scan == scan_result.fixed_file


def test_api_fix_string_simple_small_fix():
    """
    Test to make sure that we can invoke a fix of a file with a simple fix.
    """

    # Arrange
    string_to_scan = """# This is a test

The line after this line should be blank."""
    expected_string = """# This is a test

The line after this line should be blank.
"""

    # Act
    scan_result = PyMarkdownApi().fix_string(string_to_scan)

    # Assert
    assert scan_result.was_fixed
    assert expected_string == scan_result.fixed_file


def test_api_fix_path_no_files():
    """
    Test to make sure that we can invoke a fix of files on a path, where none are found.
    """

    # Arrange
    with tempfile.TemporaryDirectory() as tmp_dir_path:

        # Act
        scan_result = PyMarkdownApi().fix_path(tmp_dir_path)

        # Assert
        assert not scan_result.files_fixed


def test_api_fix_path_single_file_no_fix_required():
    """
    Test to make sure that we can invoke a fix of files on a path, where a single file is found requiring no fixes.
    """

    # Arrange
    string_to_scan = """# This is a test

The line after this line should be blank.
"""

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        write_temporary_configuration(
            string_to_scan, directory=tmp_dir_path, file_name_suffix=".md"
        )

        # Act
        scan_result = PyMarkdownApi().fix_path(tmp_dir_path)

        # Assert
        assert not scan_result.files_fixed


def test_api_fix_path_single_file_fix_required():
    """
    Test to make sure that we can invoke a fix of files on a path, where a single file is found requiring fixes.
    """

    # Arrange
    string_to_scan = """# This is a test

The line after this line should be blank."""

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        file_name = write_temporary_configuration(
            string_to_scan, directory=tmp_dir_path, file_name_suffix=".md"
        )

        # Act
        scan_result = PyMarkdownApi().fix_path(tmp_dir_path)

        # Assert
        assert scan_result.files_fixed
        assert file_name in scan_result.files_fixed


def test_api_fix_path_single_file_fix_required_with_error():
    """
    Test to make sure that we can invoke a fix of files on a path, where a single file is found requiring fixes,
    but an exception is thrown during processing.
    """

    # Arrange
    string_to_scan = """---
test: assert
---
"""
    expected_error_message = "Unexpected Error(BadTokenizationError): An unhandled error occurred processing the document."

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        write_temporary_configuration(
            string_to_scan, directory=tmp_dir_path, file_name_suffix=".md"
        )

        # Act & Assert
        assert_that_exception_is_raised(
            PyMarkdownApiException,
            expected_error_message,
            PyMarkdownApi()
            .set_boolean_property("extensions.front-matter.enabled", True)
            .fix_path,
            tmp_dir_path,
        )


def test_api_fix_path_single_file_fix_required_with_alternate_extension():
    """
    Test to make sure that we can invoke a fix of files on a path, where a single file is found requiring fixes,
    but with a non-standard extension.
    """

    # Arrange
    string_to_scan = """# This is a test

The line after this line should be blank."""

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        file_name = write_temporary_configuration(
            string_to_scan, directory=tmp_dir_path, file_name_suffix=".nse"
        )

        # Act
        scan_result = PyMarkdownApi().fix_path(
            tmp_dir_path, alternate_extensions=".nse"
        )

        # Assert
        assert scan_result.files_fixed
        assert file_name in scan_result.files_fixed


def test_api_fix_path_multiple_files_same_directory_fix_required():
    """
    Test to make sure that we can invoke a fix of files on a path, where multiple files are found requiring fixes.
    """

    # Arrange
    string_to_scan = """# This is a test

The line after this line should be blank."""

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        file_name_one = write_temporary_configuration(
            string_to_scan, directory=tmp_dir_path, file_name_suffix=".md"
        )
        file_name_two = write_temporary_configuration(
            string_to_scan, directory=tmp_dir_path, file_name_suffix=".md"
        )

        # Act
        scan_result = PyMarkdownApi().fix_path(tmp_dir_path)

        # Assert
        assert scan_result.files_fixed
        assert file_name_one in scan_result.files_fixed
        assert file_name_two in scan_result.files_fixed


def test_api_fix_path_multiple_files_nested_directory_fix_required_no_recursion():
    """
    Test to make sure that we can invoke a fix of files on a path, where multiple files in nested
    directories exist requiring fixes, but only the base directory is specified.
    """

    # Arrange
    string_to_scan = """# This is a test

The line after this line should be blank."""

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        file_name_one = write_temporary_configuration(
            string_to_scan, directory=tmp_dir_path, file_name_suffix=".md"
        )
        nested_directory = os.path.join(tmp_dir_path, "inner")
        os.mkdir(nested_directory)
        file_name_two = write_temporary_configuration(
            string_to_scan, directory=nested_directory, file_name_suffix=".md"
        )

        # Act
        scan_result = PyMarkdownApi().fix_path(tmp_dir_path)

        # Assert
        assert scan_result.files_fixed
        assert file_name_one in scan_result.files_fixed
        assert file_name_two not in scan_result.files_fixed


def test_api_fix_path_multiple_files_nested_directory_fix_required_with_recursion():
    """
    Test to make sure that we can invoke a fix of files on a path, where multiple files in nested
    directories exist requiring fixes, and the base directory is specified with recursion enabled.
    """

    # Arrange
    string_to_scan = """# This is a test

The line after this line should be blank."""

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        file_name_one = write_temporary_configuration(
            string_to_scan, directory=tmp_dir_path, file_name_suffix=".md"
        )
        nested_directory = os.path.join(tmp_dir_path, "inner")
        os.mkdir(nested_directory)
        file_name_two = write_temporary_configuration(
            string_to_scan, directory=nested_directory, file_name_suffix=".md"
        )

        # Act
        scan_result = PyMarkdownApi().fix_path(tmp_dir_path, recurse_if_directory=True)

        # Assert
        assert scan_result.files_fixed
        assert file_name_one in scan_result.files_fixed
        assert file_name_two in scan_result.files_fixed


# change print_system_error to also accept optional exception?
# OR
# move format_error into presentation?

# print_system_error(
# plugin_manager, __handle_argparse_subparser_info, __handle_argparse_subparser_list
# extension_manager, __handle_argparse_subparser_info, __handle_argparse_subparser_list

# print_system_out(
# - [ ] extension_manager, plugin_manager
