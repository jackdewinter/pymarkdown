"""
Module to provide tests related to the "-l" option.
"""

import os
import sys
from test.markdown_scanner import MarkdownScanner

if sys.version_info < (3, 10):
    ARGPARSE_X = "optional arguments:"
else:
    ARGPARSE_X = "options:"
if sys.version_info < (3, 13):
    ALT_EXTENSIONS_X = (
        "-ae ALTERNATE_EXTENSIONS, --alternate-extensions ALTERNATE_EXTENSIONS"
    )
else:
    ALT_EXTENSIONS_X = "-ae, --alternate-extensions ALTERNATE_EXTENSIONS"


def test_markdown_with_dash_h():
    """
    Test to make sure we get help if '-h' is supplied
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["scan", "-h"]

    expected_return_code = 0
    expected_output = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]

positional arguments:
  path                  one or more paths to examine for eligible Markdown
                        files

{ARGPARSE_X}
  -h, --help            show this help message and exit
  -l, --list-files      list any eligible Markdown files found on the
                        specified paths and exit
  -r, --recurse         recursively traverse any found directories for
                        matching files
  {ALT_EXTENSIONS_X}
                        provide an alternate set of file extensions to match
                        against
""".replace(
        "{ARGPARSE_X}", ARGPARSE_X
    ).replace(
        "{ALT_EXTENSIONS_X}", ALT_EXTENSIONS_X
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_only():
    """
    Test to make sure we get simple help if '-l' is supplied without any paths

    This function is shadowed by
    test_markdown_return_code_default_command_line_error.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["scan", "-l"]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]
main.py scan: error: the following arguments are required: path
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_bad_path():
    """
    Test to make sure we get failure text if '-l' is supplied with a bad path.

    This function is shadowed by test_api_list_for_non_existant_file
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["scan", "-l", "my-bad-path"]

    expected_return_code = 1
    expected_output = ""
    expected_error = """Provided path 'my-bad-path' does not exist.


No matching files found."""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_non_md_directory():
    """
    Test to make sure we get failure text if '-l' is supplied with a path containing no md files.

    This function is shadowed by test_api_list_for_directory_without_markdown_files.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["scan", "-l", "only-text"]

    expected_return_code = 1
    expected_output = ""
    expected_error = """No matching files found.
"""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_md_directory():
    """
    Test to make sure we get the path to a single file if '-l' is supplied
    with a path containing a simple md file.

    This function is shadowed by test_api_list_for_directory_with_markdown_files.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = f"simple{os.sep}"
    supplied_arguments = ["scan", "-l", source_path]

    expected_return_code = 0
    expected_output = """{source_path}simple.md
""".replace(
        "{source_path}", source_path
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_mixed_directories():
    """
    Test to make sure we get the path to a single file if '-l' is supplied
    with multiple paths containing a simple md file.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = f"simple{os.sep}"
    supplied_arguments = ["scan", "-l", "only-text", source_path]

    expected_return_code = 0
    expected_output = """{source_path}simple.md
""".replace(
        "{source_path}", source_path
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_non_md_file():
    """
    Test to make sure we get a failure if '-l' is supplied with a file path that isn't a md file.

    This function is shadowed by test_api_scan_for_non_markdown_file.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join("only-text", "simple_text_file.txt")
    supplied_arguments = ["scan", "-l", source_path]

    expected_return_code = 1
    expected_output = ""
    expected_error = """Provided file path '{source_path}' is not a valid file. Skipping.


No matching files found.""".replace(
        "{source_path}", source_path
    )

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_md_file():
    """
    Test to make sure we a single path to a file if '-l' is supplied with
    a file path that is a simple md file.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join("simple", "simple.md")
    supplied_arguments = ["scan", "-l", source_path]

    expected_return_code = 0
    expected_output = """{source_path}
""".replace(
        "{source_path}", source_path
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_mixed_files():
    """
    Test to make sure we get a failure '-l' is supplied with a file path
    that is a simple md file and one that isn't.
    """

    # Arrange
    scanner = MarkdownScanner()
    existing_source_path = os.path.join("simple", "simple.md")
    nonexisting_source_path = os.path.join("only-text", "simple_text_file.txt")
    supplied_arguments = [
        "scan",
        "-l",
        nonexisting_source_path,
        existing_source_path,
    ]

    expected_return_code = 1
    expected_output = """"""
    expected_error = """Provided file path '{nonexisting_source_path}' is not a valid file. Skipping.


No matching files found.""".replace(
        "{nonexisting_source_path}", nonexisting_source_path
    )

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_globbed_files():
    """
    Test to make sure we get a list of valid paths if '-l' is supplied
    with a globbed file path that works.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join("rules", "md001") + os.sep
    supplied_arguments = ["scan", "-l", f"{source_path}*.md"]

    expected_return_code = 0
    expected_output = """{source_path}empty.md
{source_path}front_matter_with_alternate_title.md
{source_path}front_matter_with_no_title.md
{source_path}front_matter_with_title.md
{source_path}improper_atx_heading_incrementing.md
{source_path}improper_setext_heading_incrementing.md
{source_path}proper_atx_heading_incrementing.md
{source_path}proper_setext_heading_incrementing.md""".replace(
        "{source_path}", source_path
    )
    expected_error = """"""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_non_matching_globbed_files():
    """
    Test to make sure we get a failure if '-l' is supplied with a
    globbed file path that works but does not find any matching files.

    This function is shadowed by test_api_scan_for_non_matching_glob.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join("rules", "md001", "z*.md")
    supplied_arguments = ["scan", "-l", source_path]

    expected_return_code = 1
    expected_output = """"""
    expected_error = f"Provided glob path '{source_path}' did not match any files.\n\n\nNo matching files found."

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_directory():
    """
    Test to make sure we get a list of paths if '-l' is supplied with a directory
    containing valid Markdown files.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join("..", "..", "docs") + os.sep
    supplied_arguments = ["scan", "-l", source_path]

    expected_return_code = 0
    expected_output = """{source_path}advanced_configuration.md
{source_path}advanced_plugins.md
{source_path}advanced_scanning.md
{source_path}api-usage.md
{source_path}api.md
{source_path}developer.md
{source_path}extensions.md
{source_path}faq.md
{source_path}old_README.md
{source_path}pre-commit.md
{source_path}rules.md
{source_path}writing_rule_plugins.md""".replace(
        "{source_path}", source_path
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_and_dash_r_on_directory():
    """
    Test to make sure we get a large list of files if '-l' and '-r' is
    supplied with a directory that, recursively, contains lots of valid
    files.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join("..", "..", "docs") + os.sep
    extensions_source_path = os.path.join("..", "..", "docs", "extensions") + os.sep
    rules_source_path = os.path.join("..", "..", "docs", "rules") + os.sep
    supplied_arguments = ["scan", "-l", "-r", source_path]

    expected_return_code = 0
    expected_output = (
        """{source_path}advanced_configuration.md
{source_path}advanced_plugins.md
{source_path}advanced_scanning.md
{source_path}api-usage.md
{source_path}api.md
{source_path}developer.md
{source_path}extensions.md
{extensions_source_path}disallowed-raw_html.md
{extensions_source_path}extended_autolinks.md
{extensions_source_path}front-matter.md
{extensions_source_path}pragmas.md
{extensions_source_path}strikethrough.md
{extensions_source_path}task-list-items.md
{source_path}faq.md
{source_path}old_README.md
{source_path}pre-commit.md
{source_path}rules.md
{rules_source_path}rule_md001.md
{rules_source_path}rule_md002.md
{rules_source_path}rule_md003.md
{rules_source_path}rule_md004.md
{rules_source_path}rule_md005.md
{rules_source_path}rule_md006.md
{rules_source_path}rule_md007.md
{rules_source_path}rule_md009.md
{rules_source_path}rule_md010.md
{rules_source_path}rule_md011.md
{rules_source_path}rule_md012.md
{rules_source_path}rule_md013.md
{rules_source_path}rule_md014.md
{rules_source_path}rule_md018.md
{rules_source_path}rule_md019.md
{rules_source_path}rule_md020.md
{rules_source_path}rule_md021.md
{rules_source_path}rule_md022.md
{rules_source_path}rule_md023.md
{rules_source_path}rule_md024.md
{rules_source_path}rule_md025.md
{rules_source_path}rule_md026.md
{rules_source_path}rule_md027.md
{rules_source_path}rule_md028.md
{rules_source_path}rule_md029.md
{rules_source_path}rule_md030.md
{rules_source_path}rule_md031.md
{rules_source_path}rule_md032.md
{rules_source_path}rule_md033.md
{rules_source_path}rule_md034.md
{rules_source_path}rule_md035.md
{rules_source_path}rule_md036.md
{rules_source_path}rule_md037.md
{rules_source_path}rule_md038.md
{rules_source_path}rule_md039.md
{rules_source_path}rule_md040.md
{rules_source_path}rule_md041.md
{rules_source_path}rule_md042.md
{rules_source_path}rule_md043.md
{rules_source_path}rule_md044.md
{rules_source_path}rule_md045.md
{rules_source_path}rule_md046.md
{rules_source_path}rule_md047.md
{rules_source_path}rule_md048.md
{rules_source_path}rule_pml100.md
{rules_source_path}rule_pml101.md
{source_path}writing_rule_plugins.md""".replace(
            "{source_path}", source_path
        )
        .replace("{extensions_source_path}", extensions_source_path)
        .replace("{rules_source_path}", rules_source_path)
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
