"""
Module to provide tests for the application file scanner module.
"""
import argparse
import difflib

from pymarkdown.application_file_scanner import ApplicationFileScanner


def compare_expected_to_actual(expected_text, actual_text, xx_title="Text"):
    """
    Compare the expected text to the actual text.
    """
    if actual_text.strip() != expected_text.strip():
        diff = difflib.ndiff(expected_text.splitlines(), actual_text.splitlines())
        diff_values = "\n".join(list(diff))
        raise AssertionError(f"{xx_title} not as expected:\n{diff_values}")


def test_application_file_scanner_args_no_changes():
    """
    Test to make sure we get all scanner args without any flags changed.
    """

    # Arrange
    expected_output = """usage: pytest [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]

Lint any found files.

positional arguments:
  path                  one or more paths to scan for eligible files

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-files      list the eligible files and exit
  -r, --recurse         recursively scan directories for files
  -ae ALTERNATE_EXTENSIONS, --alternate-extensions ALTERNATE_EXTENSIONS
                        provide an alternate set of file extensions to scan
                        for"""
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    ApplicationFileScanner.add_default_command_line_arguments(parser, ".md")
    args = parser.format_help()

    # Assert
    compare_expected_to_actual(expected_output, args)


def test_application_file_scanner_args_bad_extension():
    """
    Test to make sure we get all scanner args with a bad default extension.
    """

    # Arrange
    expected_output = "Extension '*.md' is not a valid extension: Extension '*.md' must start with a period."
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    found_exception = None
    try:
        ApplicationFileScanner.add_default_command_line_arguments(parser, "*.md")
        raise AssertionError()
    except argparse.ArgumentTypeError as ex:
        found_exception = ex

    # Assert
    assert found_exception
    compare_expected_to_actual(expected_output, str(found_exception))


def test_application_file_scanner_args_with_file_type_name():
    """
    Test to make sure we get all scanner args with a file type name specified.
    """

    # Arrange
    expected_output = """usage: pytest [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]

Lint any found files.

positional arguments:
  path                  one or more paths to scan for eligible MINE files

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-files      list the eligible MINE files and exit
  -r, --recurse         recursively scan directories for files
  -ae ALTERNATE_EXTENSIONS, --alternate-extensions ALTERNATE_EXTENSIONS
                        provide an alternate set of file extensions to scan
                        for"""
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    ApplicationFileScanner.add_default_command_line_arguments(
        parser, ".md", file_type_name="MINE"
    )
    args = parser.format_help()

    # Assert
    compare_expected_to_actual(expected_output, args)


def test_application_file_scanner_args_with_empty_file_type_name():
    """
    Test to make sure we get all scanner args with an empty file type name specified.
    """

    # Arrange
    expected_output = """usage: pytest [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]

Lint any found files.

positional arguments:
  path                  one or more paths to scan for eligible files

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-files      list the eligible files and exit
  -r, --recurse         recursively scan directories for files
  -ae ALTERNATE_EXTENSIONS, --alternate-extensions ALTERNATE_EXTENSIONS
                        provide an alternate set of file extensions to scan
                        for"""
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    ApplicationFileScanner.add_default_command_line_arguments(
        parser, ".md", file_type_name=""
    )
    args = parser.format_help()

    # Assert
    compare_expected_to_actual(expected_output, args)


def test_application_file_scanner_args_without_list_files():
    """
    Test to make sure we get all scanner args with list files disabled
    """

    # Arrange
    expected_output = """usage: pytest [-h] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]

Lint any found files.

positional arguments:
  path                  one or more paths to scan for eligible files

optional arguments:
  -h, --help            show this help message and exit
  -r, --recurse         recursively scan directories for files
  -ae ALTERNATE_EXTENSIONS, --alternate-extensions ALTERNATE_EXTENSIONS
                        provide an alternate set of file extensions to scan
                        for"""
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    ApplicationFileScanner.add_default_command_line_arguments(
        parser, ".md", show_list_files=False
    )
    args = parser.format_help()

    # Assert
    compare_expected_to_actual(expected_output, args)


def test_application_file_scanner_args_without_recurse_directories():
    """
    Test to make sure we get all scanner args with recurse directories disabled
    """

    # Arrange
    expected_output = """usage: pytest [-h] [-l] [-ae ALTERNATE_EXTENSIONS] path [path ...]

Lint any found files.

positional arguments:
  path                  one or more paths to scan for eligible files

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-files      list the eligible files and exit
  -ae ALTERNATE_EXTENSIONS, --alternate-extensions ALTERNATE_EXTENSIONS
                        provide an alternate set of file extensions to scan
                        for"""
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    ApplicationFileScanner.add_default_command_line_arguments(
        parser, ".md", show_recurse_directories=False
    )
    args = parser.format_help()

    # Assert
    compare_expected_to_actual(expected_output, args)


def test_application_file_scanner_args_without_alternate_extensions():
    """
    Test to make sure we get all scanner args with alternate extensions disabled
    """

    # Arrange
    expected_output = """usage: pytest [-h] [-l] [-r] path [path ...]

Lint any found files.

positional arguments:
  path              one or more paths to scan for eligible files

optional arguments:
  -h, --help        show this help message and exit
  -l, --list-files  list the eligible files and exit
  -r, --recurse     recursively scan directories for files"""
    parser = argparse.ArgumentParser(description="Lint any found files.", prog="pytest")

    # Act
    ApplicationFileScanner.add_default_command_line_arguments(
        parser, ".md", show_alternate_extensions=False
    )
    args = parser.format_help()

    # Assert
    compare_expected_to_actual(expected_output, args)
