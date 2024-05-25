"""
Module for directly using PyMarkdown's list api.
"""

import os
from test.utils import assert_if_lists_different, assert_that_exception_is_raised

from pymarkdown.api import (
    PyMarkdownApi,
    PyMarkdownApiArgumentException,
    PyMarkdownApiNoFilesFoundException,
)


def test_api_list_bad_path_to_scan():
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
        PyMarkdownApi().list_path,
        source_path,
    )
    assert caught_exception.argument_name == "path_to_scan"


def test_api_list_bad_alternate_extensions():
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
        PyMarkdownApi().list_path,
        source_path,
        alternate_extensions=alternate_extensions,
    )
    assert caught_exception.argument_name == "alternate_extensions"


def test_api_list_single_file():
    """
    Test to make sure that we can invoke a list of a file.

    This function is an (list) API version of the function
    test_markdown_with_dash_dash_log_level_info_with_file.
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )

    # Act
    list_result = PyMarkdownApi().list_path(source_path)

    # Assert
    assert_if_lists_different(list_result.matching_files, [source_path])


def test_api_list_for_non_existant_file():
    """
    Test to make sure that listing for a non-existant path returns a
    reproducible result.

    This function is an API version of the function
    test_markdown_with_dash_l_on_bad_path.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_output = f"Provided path '{source_path}' does not exist."

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiNoFilesFoundException,
        expected_output,
        PyMarkdownApi().list_path,
        source_path,
    )


def test_api_list_for_directory_without_markdown_files():
    """
    Test to make sure that listing for a path that does not contain
    any markdown files returns a reproducible result.

    This function is an API version of the function
    test_markdown_with_dash_l_on_non_md_directory.
    """

    # Arrange
    source_path = os.path.join("test", "resources", "only-text")
    expected_output = ""

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiNoFilesFoundException,
        expected_output,
        PyMarkdownApi().list_path,
        source_path,
    )


def test_api_list_for_directory_with_markdown_files():
    """
    Test to make sure that listing for a path that does contain
    any markdown files returns a reproducible result.

    This function is an API version of the function
    test_markdown_with_dash_l_on_md_directory.
    """

    # Arrange
    source_path = os.path.join("test", "resources", "simple")
    expected_path = os.path.join(source_path, "simple.md")

    # Act
    list_result = PyMarkdownApi().list_path(source_path)

    # Assert
    assert_if_lists_different(list_result.matching_files, [expected_path])


def test_api_list_for_non_matching_glob():
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
        PyMarkdownApi().list_path,
        source_path,
    )


def test_api_list_for_non_markdown_file():
    """
    Test to make sure that scanning for a file that does not have markdown
    extension produces reliable results.

    This function is an API version of the function
    test_markdown_with_dash_l_on_non_md_file.
    """
    # TODO add version with alternate extensions

    # Arrange
    source_path = os.path.join("test", "resources", "only-text", "simple_text_file.txt")
    expected_output = (
        f"Provided file path '{source_path}' is not a valid file. Skipping."
    )

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiNoFilesFoundException,
        expected_output,
        PyMarkdownApi().list_path,
        source_path,
    )


def test_api_list_for_non_markdown_file_with_alternate_extensions():
    """
    Test to make sure that scanning for a file that does not have markdown
    extension but with alternate extensions enabled produces reliable results.

    This function is an API version of the function
    test_markdown_with_dash_l_on_non_md_file and
    test_markdown_with_dash_ae_with_valid_file_extension_multiple.
    """

    # Arrange
    source_path = os.path.join("test", "resources", "only-text", "simple_text_file.txt")
    alternate_extensions = ".txt,.md"

    # Act
    list_result = PyMarkdownApi().list_path(
        source_path, alternate_extensions=alternate_extensions
    )

    # Assert
    assert_if_lists_different(list_result.matching_files, [source_path])


def test_api_list_for_markdown_file():
    """
    Test to make sure that scanning for a file that does have markdown
    extension produces reliable results.

    This function is an API version of the function
    test_markdown_with_dash_l_on_md_file.
    """

    # Arrange
    source_path = os.path.join("test", "resources", "simple", "simple.md")

    # Act
    list_result = PyMarkdownApi().list_path(source_path)

    # Assert
    assert_if_lists_different(list_result.matching_files, [source_path])


def test_api_list_for_matching_globbed_markdown_file():
    """
    Test to make sure that scanning for files that match a given glob
    produces reliable results.

    This function is an API version of the function
    test_markdown_with_dash_l_on_globbed_files.
    """

    # Arrange
    base_path = os.path.join("test", "resources", "rules", "md001")
    source_path = os.path.join(base_path, "*.md")
    expected_relative_paths = [
        "empty.md",
        "front_matter_with_alternate_title.md",
        "front_matter_with_no_title.md",
        "front_matter_with_title.md",
        "improper_atx_heading_incrementing.md",
        "improper_setext_heading_incrementing.md",
        "proper_atx_heading_incrementing.md",
        "proper_setext_heading_incrementing.md",
    ]
    expected_paths = []
    for i in expected_relative_paths:
        expected_paths.append(os.path.join(base_path, i))

    # Act
    list_result = PyMarkdownApi().list_path(source_path)

    # Assert
    assert_if_lists_different(list_result.matching_files, expected_paths)


def test_api_list_for_directory():
    """
    Test to make sure that scanning a directory gives predictable results.

    This function is an API version of the function
    test_markdown_with_dash_l_on_directory.
    """

    # Arrange
    base_path = os.path.join("docs")
    expected_relative_paths = [
        "advanced_configuration.md",
        "advanced_plugins.md",
        "advanced_scanning.md",
        "api-usage.md",
        "api.md",
        "developer.md",
        "extensions.md",
        "faq.md",
        "old_README.md",
        "pre-commit.md",
        "rules.md",
        "writing_rule_plugins.md",
    ]
    expected_paths = []
    for i in expected_relative_paths:
        expected_paths.append(os.path.join(base_path, i))

    # Act
    list_result = PyMarkdownApi().list_path(base_path)

    # Assert
    assert_if_lists_different(list_result.matching_files, expected_paths)


def test_api_list_recursive_for_directory():
    """
    Test to make sure that scanning a directory gives predictable results.

    This function is an API version of the function
    test_markdown_with_dash_l_and_dash_r_on_directory.
    """

    # Arrange
    base_path = os.path.join("docs")
    expected_relative_paths = [
        "advanced_configuration.md",
        "advanced_plugins.md",
        "advanced_scanning.md",
        "api-usage.md",
        "api.md",
        "developer.md",
        "extensions.md",
        "{extensions}disallowed-raw_html.md",
        "{extensions}extended_autolinks.md",
        "{extensions}front-matter.md",
        "{extensions}pragmas.md",
        "{extensions}strikethrough.md",
        "{extensions}task-list-items.md",
        "faq.md",
        "old_README.md",
        "pre-commit.md",
        "rules.md",
        "{rules}rule_md001.md",
        "{rules}rule_md002.md",
        "{rules}rule_md003.md",
        "{rules}rule_md004.md",
        "{rules}rule_md005.md",
        "{rules}rule_md006.md",
        "{rules}rule_md007.md",
        "{rules}rule_md009.md",
        "{rules}rule_md010.md",
        "{rules}rule_md011.md",
        "{rules}rule_md012.md",
        "{rules}rule_md013.md",
        "{rules}rule_md014.md",
        "{rules}rule_md018.md",
        "{rules}rule_md019.md",
        "{rules}rule_md020.md",
        "{rules}rule_md021.md",
        "{rules}rule_md022.md",
        "{rules}rule_md023.md",
        "{rules}rule_md024.md",
        "{rules}rule_md025.md",
        "{rules}rule_md026.md",
        "{rules}rule_md027.md",
        "{rules}rule_md028.md",
        "{rules}rule_md029.md",
        "{rules}rule_md030.md",
        "{rules}rule_md031.md",
        "{rules}rule_md032.md",
        "{rules}rule_md033.md",
        "{rules}rule_md034.md",
        "{rules}rule_md035.md",
        "{rules}rule_md036.md",
        "{rules}rule_md037.md",
        "{rules}rule_md038.md",
        "{rules}rule_md039.md",
        "{rules}rule_md040.md",
        "{rules}rule_md041.md",
        "{rules}rule_md042.md",
        "{rules}rule_md043.md",
        "{rules}rule_md044.md",
        "{rules}rule_md045.md",
        "{rules}rule_md046.md",
        "{rules}rule_md047.md",
        "{rules}rule_md048.md",
        "{rules}rule_pml100.md",
        "{rules}rule_pml101.md",
        "writing_rule_plugins.md",
    ]
    expected_paths = []
    for i in expected_relative_paths:
        prefix = "{extensions}"
        if i.startswith(prefix):
            i = os.path.join("extensions", i[len(prefix) :])
        prefix = "{rules}"
        if i.startswith(prefix):
            i = os.path.join("rules", i[len(prefix) :])
        expected_paths.append(os.path.join(base_path, i))

    # Act
    list_result = PyMarkdownApi().list_path(base_path, recurse_if_directory=True)

    # Assert
    assert_if_lists_different(list_result.matching_files, expected_paths)
