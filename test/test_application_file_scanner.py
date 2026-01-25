"""
Module to provide tests for the application file scanner module.
"""

import argparse
import sys
from test.utils import assert_that_exception_is_raised, compare_expected_to_actual

from application_file_scanner import ApplicationFileScanner

if sys.version_info < (3, 10):
    ARGPARSE_X = "optional arguments:"
else:
    ARGPARSE_X = "options:"
if sys.version_info < (3, 13):
    ALT_EXTENSIONS_X = (
        "-ae ALTERNATE_EXTENSIONS, --alternate-extensions ALTERNATE_EXTENSIONS"
    )
    EXCLUSIONS_X = "-e PATH_EXCLUSIONS, --exclude PATH_EXCLUSIONS"
else:
    ALT_EXTENSIONS_X = "-ae, --alternate-extensions ALTERNATE_EXTENSIONS"
    EXCLUSIONS_X = "-e, --exclude PATH_EXCLUSIONS"


def test_application_file_scanner_args_no_changes() -> None:
    """
    Test to make sure we get all scanner args without any flags changed.
    """

    # Arrange
    expected_output = f"""usage: pytest [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] [-e PATH_EXCLUSIONS]
              path [path ...]

Lint any found files.

positional arguments:
  path                  one or more paths to examine for eligible files

{ARGPARSE_X}
  -h, --help            show this help message and exit
  -l, --list-files      list any eligible files found on the specified paths
                        and exit
  -r, --recurse         recursively traverse any found directories for
                        matching files
  {ALT_EXTENSIONS_X}
                        provide an alternate set of file extensions to match
                        against
  {EXCLUSIONS_X}
                        one or more paths to exclude from the search. Can be a
                        glob pattern."""
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    ApplicationFileScanner.add_default_command_line_arguments(parser, ".md")
    args = parser.format_help()

    # Assert
    compare_expected_to_actual(expected_output, args)


def test_application_file_scanner_args_bad_extension() -> None:
    """
    Test to make sure we get all scanner args with a bad default extension.
    """

    # Arrange
    expected_output = "Extension '*.md' must start with a period."
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act & Assert
    assert_that_exception_is_raised(
        argparse.ArgumentTypeError,
        expected_output,
        ApplicationFileScanner.add_default_command_line_arguments,
        parser,
        "*.md",
    )


def test_application_file_scanner_args_with_file_type_name() -> None:
    """
    Test to make sure we get all scanner args with a file type name specified.
    """

    # Arrange
    expected_output = f"""usage: pytest [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] [-e PATH_EXCLUSIONS]
              path [path ...]

Lint any found files.

positional arguments:
  path                  one or more paths to examine for eligible MINE files

{ARGPARSE_X}
  -h, --help            show this help message and exit
  -l, --list-files      list any eligible MINE files found on the specified
                        paths and exit
  -r, --recurse         recursively traverse any found directories for
                        matching files
  {ALT_EXTENSIONS_X}
                        provide an alternate set of file extensions to match
                        against
  {EXCLUSIONS_X}
                        one or more paths to exclude from the search. Can be a
                        glob pattern."""
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    ApplicationFileScanner.add_default_command_line_arguments(
        parser, ".md", file_type_name="MINE"
    )
    args = parser.format_help()

    # Assert
    compare_expected_to_actual(expected_output, args)


def test_application_file_scanner_args_with_empty_file_type_name() -> None:
    """
    Test to make sure we get all scanner args with an empty file type name specified.
    """

    # Arrange
    expected_output = f"""usage: pytest [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] [-e PATH_EXCLUSIONS]
              path [path ...]

Lint any found files.

positional arguments:
  path                  one or more paths to examine for eligible files

{ARGPARSE_X}
  -h, --help            show this help message and exit
  -l, --list-files      list any eligible files found on the specified paths
                        and exit
  -r, --recurse         recursively traverse any found directories for
                        matching files
  {ALT_EXTENSIONS_X}
                        provide an alternate set of file extensions to match
                        against
  {EXCLUSIONS_X}
                        one or more paths to exclude from the search. Can be a
                        glob pattern."""
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    ApplicationFileScanner.add_default_command_line_arguments(
        parser, ".md", file_type_name=""
    )
    args = parser.format_help()

    # Assert
    compare_expected_to_actual(expected_output, args)


def test_application_file_scanner_args_without_list_files() -> None:
    """
    Test to make sure we get all scanner args with list files disabled
    """

    # Arrange
    expected_output = f"""usage: pytest [-h] [-r] [-ae ALTERNATE_EXTENSIONS] [-e PATH_EXCLUSIONS]
              path [path ...]

Lint any found files.

positional arguments:
  path                  one or more paths to examine for eligible files

{ARGPARSE_X}
  -h, --help            show this help message and exit
  -r, --recurse         recursively traverse any found directories for
                        matching files
  {ALT_EXTENSIONS_X}
                        provide an alternate set of file extensions to match
                        against
  {EXCLUSIONS_X}
                        one or more paths to exclude from the search. Can be a
                        glob pattern."""
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    ApplicationFileScanner.add_default_command_line_arguments(
        parser, ".md", show_list_files=False
    )
    args = parser.format_help()

    # Assert
    compare_expected_to_actual(expected_output, args)


def test_application_file_scanner_args_without_recurse_directories() -> None:
    """
    Test to make sure we get all scanner args with recurse directories disabled
    """

    # Arrange
    expected_output = f"""usage: pytest [-h] [-l] [-ae ALTERNATE_EXTENSIONS] [-e PATH_EXCLUSIONS]
              path [path ...]

Lint any found files.

positional arguments:
  path                  one or more paths to examine for eligible files

{ARGPARSE_X}
  -h, --help            show this help message and exit
  -l, --list-files      list any eligible files found on the specified paths
                        and exit
  {ALT_EXTENSIONS_X}
                        provide an alternate set of file extensions to match
                        against
  {EXCLUSIONS_X}
                        one or more paths to exclude from the search. Can be a
                        glob pattern."""
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    ApplicationFileScanner.add_default_command_line_arguments(
        parser, ".md", show_recurse_directories=False
    )
    args = parser.format_help()

    # Assert
    compare_expected_to_actual(expected_output, args)


def test_application_file_scanner_args_without_alternate_extensions() -> None:
    """
    Test to make sure we get all scanner args with alternate extensions disabled
    """

    # Arrange
    expected_output = f"""usage: pytest [-h] [-l] [-r] [-e PATH_EXCLUSIONS] path [path ...]

Lint any found files.

positional arguments:
  path                  one or more paths to examine for eligible files

{ARGPARSE_X}
  -h, --help            show this help message and exit
  -l, --list-files      list any eligible files found on the specified paths
                        and exit
  -r, --recurse         recursively traverse any found directories for
                        matching files
  {EXCLUSIONS_X}
                        one or more paths to exclude from the search. Can be a
                        glob pattern."""
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    ApplicationFileScanner.add_default_command_line_arguments(
        parser, ".md", show_alternate_extensions=False
    )
    args = parser.format_help()

    # Assert
    compare_expected_to_actual(expected_output, args)


def test_application_file_scanner_args_without_exclusions() -> None:
    """
    Test to make sure we get all scanner args with alternate extensions disabled
    """

    # Arrange
    expected_output = f"""usage: pytest [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]

Lint any found files.

positional arguments:
  path                  one or more paths to examine for eligible files

{ARGPARSE_X}
  -h, --help            show this help message and exit
  -l, --list-files      list any eligible files found on the specified paths
                        and exit
  -r, --recurse         recursively traverse any found directories for
                        matching files
  {ALT_EXTENSIONS_X}
                        provide an alternate set of file extensions to match
                        against"""
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    ApplicationFileScanner.add_default_command_line_arguments(
        parser, ".md", show_exclusions=False
    )
    args = parser.format_help()

    # Assert
    compare_expected_to_actual(expected_output, args)
