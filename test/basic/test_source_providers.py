"""
Module to provide tests for source providers.
"""

import os

from pymarkdown.general.source_providers import (
    FileSourceProvider,
    InMemorySourceProvider,
)


def __verify_line(expected_line, actual_line):
    if expected_line is None:
        assert actual_line is None, (
            "Actual line should be None, not: '" + actual_line + "'"
        )
    else:
        assert actual_line == expected_line, (
            "Actual line:   '"
            + actual_line
            + "'\n"
            + "Expected line: '"
            + expected_line
            + "'\n"
        )


def test_source_provider_in_memory_empty_string():
    """
    Test the in memory source provider with an empty string.
    """

    # Arrange
    source_provider = InMemorySourceProvider("")
    expected_first_line = ""
    expected_second_line = None

    # Act
    actual_first_line = source_provider.get_next_line()
    actual_second_line = source_provider.get_next_line()

    # Assert
    __verify_line(expected_first_line, actual_first_line)
    __verify_line(expected_second_line, actual_second_line)


def test_source_provider_in_memory_one_line():
    """
    Test the in memory source provider with one line of input.
    """

    # Arrange
    expected_first_line = "this is the first line"
    expected_second_line = None
    source_provider = InMemorySourceProvider(expected_first_line)

    # Act
    actual_first_line = source_provider.get_next_line()
    actual_second_line = source_provider.get_next_line()

    # Assert
    __verify_line(expected_first_line, actual_first_line)
    __verify_line(expected_second_line, actual_second_line)


def test_source_provider_in_memory_two_lines():
    """
    Test the in memory source provider with two lines of input.
    """

    # Arrange
    expected_first_line = "this is the first line"
    expected_second_line = "this is the second line"
    expected_third_line = None
    source_provider = InMemorySourceProvider(
        expected_first_line + "\n" + expected_second_line
    )

    # Act
    actual_first_line = source_provider.get_next_line()
    actual_second_line = source_provider.get_next_line()
    actual_third_line = source_provider.get_next_line()

    # Assert
    __verify_line(expected_first_line, actual_first_line)
    __verify_line(expected_second_line, actual_second_line)
    __verify_line(expected_third_line, actual_third_line)


def test_source_provider_file_empty():
    """
    Test the file source provider with an empty file.
    """

    # Arrange
    resource_directory = os.path.join(os.getcwd(), "test", "resources")
    input_file = os.path.join(resource_directory, "empty-file.txt")
    source_provider = FileSourceProvider(input_file)
    expected_first_line = ""
    expected_second_line = None

    # Act
    actual_first_line = source_provider.get_next_line()
    actual_second_line = source_provider.get_next_line()

    # Assert
    __verify_line(expected_first_line, actual_first_line)
    __verify_line(expected_second_line, actual_second_line)


def test_source_provider_file_single_line():
    """
    Test the file source provider with a single line
    """

    # Arrange
    resource_directory = os.path.join(os.getcwd(), "test", "resources")
    input_file = os.path.join(resource_directory, "single-line.txt")
    source_provider = FileSourceProvider(input_file)
    expected_first_line = "this is the first line"
    expected_second_line = None

    # Act
    actual_first_line = source_provider.get_next_line()
    actual_second_line = source_provider.get_next_line()

    # Assert
    __verify_line(expected_first_line, actual_first_line)
    __verify_line(expected_second_line, actual_second_line)


def test_source_provider_file_two_lines():
    """
    Test the file source provider with two lines of input.
    """

    # Arrange
    resource_directory = os.path.join(os.getcwd(), "test", "resources")
    input_file = os.path.join(resource_directory, "double-line.txt")
    source_provider = FileSourceProvider(input_file)
    expected_first_line = "this is the first line"
    expected_second_line = "this is the second line"
    expected_third_line = None

    # Act
    actual_first_line = source_provider.get_next_line()
    actual_second_line = source_provider.get_next_line()
    actual_third_line = source_provider.get_next_line()

    # Assert
    __verify_line(expected_first_line, actual_first_line)
    __verify_line(expected_second_line, actual_second_line)
    __verify_line(expected_third_line, actual_third_line)


def test_source_provider_file_two_lines_with_blank_between():
    """
    Test the file source provider with two lines of input with a blank between them.
    """

    # Arrange
    resource_directory = os.path.join(os.getcwd(), "test", "resources")
    input_file = os.path.join(resource_directory, "double-line-with-blank.txt")
    source_provider = FileSourceProvider(input_file)
    expected_first_line = "this is the first line"
    expected_second_line = ""
    expected_third_line = "this is the second line"
    expected_fourth_line = None

    # Act
    actual_first_line = source_provider.get_next_line()
    actual_second_line = source_provider.get_next_line()
    actual_third_line = source_provider.get_next_line()
    actual_fourth_line = source_provider.get_next_line()

    # Assert
    __verify_line(expected_first_line, actual_first_line)
    __verify_line(expected_second_line, actual_second_line)
    __verify_line(expected_third_line, actual_third_line)
    __verify_line(expected_fourth_line, actual_fourth_line)


def test_source_provider_file_two_lines_with_blank_between_and_trailing():
    """
    Test the file source provider with two lines of input with a blank between them and a trailing line.
    """

    # Arrange
    resource_directory = os.path.join(os.getcwd(), "test", "resources")
    input_file = os.path.join(
        resource_directory, "double-line-with-blank-and-trailing.txt"
    )
    source_provider = FileSourceProvider(input_file)
    expected_first_line = "this is the first line"
    expected_second_line = ""
    expected_third_line = "this is the second line"
    expected_fourth_line = ""
    expected_fifth_line = None

    # Act
    actual_first_line = source_provider.get_next_line()
    actual_second_line = source_provider.get_next_line()
    actual_third_line = source_provider.get_next_line()
    actual_fourth_line = source_provider.get_next_line()
    actual_fifth_line = source_provider.get_next_line()

    # Assert
    __verify_line(expected_first_line, actual_first_line)
    __verify_line(expected_second_line, actual_second_line)
    __verify_line(expected_third_line, actual_third_line)
    __verify_line(expected_fourth_line, actual_fourth_line)
    __verify_line(expected_fifth_line, actual_fifth_line)
