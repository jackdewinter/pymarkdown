"""
Module for directly using PyMarkdown's scan api.
"""

import os
from test.utils import assert_if_lists_different

import pytest

from pymarkdown.api import (
    PragmaError,
    PyMarkdownApi,
    PyMarkdownApiArgumentException,
    PyMarkdownApiNoFilesFoundException,
)
from pymarkdown.plugin_manager.plugin_scan_failure import PluginScanFailure


def test_api_scan_bad_path_to_scan():
    """
    Test to make sure that an empty path to scan is reported as an error.
    """

    # Arrange
    source_path = ""

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().scan_path(source_path)
    except PyMarkdownApiArgumentException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.argument_name == "path_to_scan"
    assert caught_exception.reason == "Parameter named 'path_to_scan' cannot be empty."


def test_api_scan_bad_alternate_extensions():
    """
    Test to make sure that a bad list of alternate extensions is reported as an error.
    """

    # Arrange
    source_path = "something"
    alternate_extensions = "not-a-valid-extension"

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().scan_path(
            source_path, alternate_extensions=alternate_extensions
        )
    except PyMarkdownApiArgumentException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.argument_name == "alternate_extensions"
    assert (
        caught_exception.reason
        == "Parameter named 'alternate_extensions' is not a valid comma-separated list of extensions."
    )


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

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().scan_path(source_path)
    except PyMarkdownApiNoFilesFoundException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.reason == f"Provided path '{source_path}' does not exist."


def test_api_scan_for_non_matching_glob():
    """
    Test to make sure that scanning for a glob that does not match
    anything produces a predictable result.

    This function is an API version of the function
    test_markdown_with_dash_l_on_non_matching_globbed_files.
    """

    # Arrange
    source_path = os.path.join("test", "resources", "rules", "md001", "z*.md")

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().scan_path(source_path)
    except PyMarkdownApiNoFilesFoundException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == f"Provided glob path '{source_path}' did not match any files."
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

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().scan_path(source_path)
    except PyMarkdownApiNoFilesFoundException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == f"Provided glob path '{source_path}' did not match any files."
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
    rules_prefix = docs_prefix + "rules" + os.sep
    expected_failure_paths = [
        f"{docs_prefix}advanced_configuration.md",
        f"{docs_prefix}advanced_scanning.md",
        f"{docs_prefix}extensions\\pragmas.md",
        f"{docs_prefix}pre-commit.md",
        f"{rules_prefix}rule_md001.md",
        f"{rules_prefix}rule_md002.md",
        f"{rules_prefix}rule_md003.md",
        f"{rules_prefix}rule_md004.md",
        f"{rules_prefix}rule_md007.md",
        f"{rules_prefix}rule_md009.md",
        f"{rules_prefix}rule_md010.md",
        f"{rules_prefix}rule_md012.md",
        f"{rules_prefix}rule_md013.md",
        f"{rules_prefix}rule_md022.md",
        f"{rules_prefix}rule_md024.md",
        f"{rules_prefix}rule_md025.md",
        f"{rules_prefix}rule_md026.md",
        f"{rules_prefix}rule_md029.md",
        f"{rules_prefix}rule_md030.md",
        f"{rules_prefix}rule_md031.md",
        f"{rules_prefix}rule_md033.md",
        f"{rules_prefix}rule_md034.md",
        f"{rules_prefix}rule_md035.md",
        f"{rules_prefix}rule_md036.md",
        f"{rules_prefix}rule_md041.md",
        f"{rules_prefix}rule_md043.md",
        f"{rules_prefix}rule_md044.md",
        f"{rules_prefix}rule_md046.md",
        f"{rules_prefix}rule_md048.md",
    ]

    # Act
    scan_result = PyMarkdownApi().scan_path(base_path, recurse_if_directory=True)

    # Assert
    assert scan_result
    assert len(scan_result.scan_failures) == 116
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
    assert len(scan_result.scan_failures) == 5
    assert scan_result.scan_failures[0].partial_equals(
        PluginScanFailure(source_path, 1, 1, "MD022", "", "", None)
    )
    assert scan_result.scan_failures[1].partial_equals(
        PluginScanFailure(source_path, 1, 12, "MD010", "", "", None)
    )
    assert scan_result.scan_failures[2].partial_equals(
        PluginScanFailure(source_path, 2, 2, "MD022", "", "", None)
    )
    assert scan_result.scan_failures[3].partial_equals(
        PluginScanFailure(source_path, 2, 2, "MD023", "", "", None)
    )
    assert scan_result.scan_failures[4].partial_equals(
        PluginScanFailure(source_path, 2, 14, "MD010", "", "", None)
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
        PluginScanFailure(source_path, 2, 1, "MD019", "", "", None)
    )
    assert len(scan_result.pragma_errors) == 1
    assert scan_result.pragma_errors[0] == PragmaError(
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


## Test: test_md003_bad_configuration_style
##       supplied_arguments = ["--strict-config","--set","plugins.md003.style=fred","scan",
##       source_path = os.path.join("test", "resources", "rules", "md003") + os.sep
##       "BadPluginError encountered while configuring plugins:\n"

## Test: test_markdown_with_dash_x_init
##       source_path = os.path.join("test", "resources", "rules", "md047", "end_with_blank_line.md")
##       supplied_arguments = ["-x-init","scan",source_path,]
##       "...encountered while initializing tokenizer"

## Test: test_markdown_with_dash_dash_add_plugin_and_bad_path
##       source_path = os.path.join("test", "resources", "rules", "md047", "end_with_blank_line.md")
##       supplied_arguments = ["--add-plugin","MD047","scan",source_path,]
##       "BadPluginError encountered while loading plugins"

## Test: test_markdown_with_repeated_identifier
##      source_path = os.path.join(        "test", "resources", "rules", "md047", "end_with_blank_line.md"    )
##      plugin_path = os.path.join(        "test", "resources", "plugins", "bad", "duplicate_id_debug.py"    )
##      supplied_arguments = [        "--add-plugin",        plugin_path,        "scan",        source_path,    ]
##       "...encountered while initializing plugins"

## Test: test_front_matter_21b
##      source_path = os.path.join(        "test", "resources", "pragmas", "extensions_issue_637.md"    )
##      supplied_arguments = [        "--strict-config",        "-s",        "extensions.front-matter.enabled=true",        "scan",        source_path,    ]
##       "...encountered while initializing extensions"

## Test: test_markdown_with_bad_strict_config_type
##      source_path = os.path.join(        "test", "resources", "rules", "md047", "end_with_blank_line.md"    )
##      supplied_configuration = {"mode": {"strict-config": 2}}
##      supplied_arguments = [            "-c",            configuration_file,            "scan",            source_path,        ]
##       "Configuration Error:..."

## Test: test_markdown_with_dash_e_single_by_id_and_config_causing_next_token_exception
##      source_path = os.path.join(        "test", "resources", "rules", "md047", "end_with_blank_line.md"    )
##      supplied_configuration = {"plugins": {"md999": {"test_value": 20}}}
##      supplied_arguments = [            "-e",            "MD999",            "-c",            configuration_file,            "scan",            source_path,        ]
##       __handle_scan_error


# __handle_error with
# __apply_configuration_layers -> MyApplicationProperties.process_standard_python_configuration_files
# __apply_configuration_layers -> MyApplicationProperties.process_project_specific_json_configuration

# change print_system_error to also accept optional exception?
# OR
# move format_error into presentation?

# stdin?
# direct passing of text?
# config file
# enable, disable
# alt ext: test_markdown_with_dash_ae_with_valid_file_extension_multiple
# list, rec: test_markdown_with_dash_l_and_dash_r_on_directory
# list: test_markdown_with_dash_l_on_mixed_files

# print_system_error(
# plugin_manager, __handle_argparse_subparser_info, __handle_argparse_subparser_list
# extension_manager, __handle_argparse_subparser_info, __handle_argparse_subparser_list
# main, __handle_error(
#  - [x] __apply_configuration_to_plugins
#  - [x] __initialize_parser
#  - [x] __initialize_plugin_manager
#  - [x] __handle_file_scanner_error
#  - [ ] __handle_scan_error
#     - [x] __scan_specific_file
#     - [ ] __process_files_to_scan with stdin
#  - [x] __initialize_plugins
#  - [x] __initialize_extensions
#  - [x] __apply_configuration_layers
#  - [x] main (no files found)
#  - [x] main/ValueError

# print_system_out(
# - [ ] extension_manager, plugin_manager
# - [x] normally Rule failures, but those are handled by ApiPresentation
