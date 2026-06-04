"""
Module to provide tests for source providers.
"""

import os
from typing import Optional

from pymarkdown.general.source_providers import (
    FileSourceProvider,
    InMemorySourceProvider,
)


def __generate_source_path(source_file_name: str) -> str:
    source_path = os.path.join("test", "resources", source_file_name)
    return source_path


def __verify_line(expected_line: Optional[str], actual_line: Optional[str]) -> None:
    if expected_line is None:
        assert actual_line is None, (
            "Actual line should be None, not: '" + actual_line + "'"
        )
    else:
        actual_line_text = actual_line or "<NONE>"
        assert actual_line == expected_line, (
            "Actual line:   '"
            + actual_line_text
            + "'\n"
            + "Expected line: '"
            + expected_line
            + "'\n"
        )


def test_source_provider_in_memory_empty_string() -> None:
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


def test_source_provider_in_memory_one_line() -> None:
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


def test_source_provider_in_memory_two_lines() -> None:
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


def test_source_provider_file_empty() -> None:
    """
    Test the file source provider with an empty file.
    """

    # Arrange
    source_provider = FileSourceProvider(__generate_source_path("empty-file.txt"))
    expected_first_line = ""
    expected_second_line = None

    # Act
    actual_first_line = source_provider.get_next_line()
    actual_second_line = source_provider.get_next_line()

    # Assert
    __verify_line(expected_first_line, actual_first_line)
    __verify_line(expected_second_line, actual_second_line)


def test_source_provider_file_single_line() -> None:
    """
    Test the file source provider with a single line
    """

    # Arrange
    source_provider = FileSourceProvider(__generate_source_path("single-line.txt"))
    expected_first_line = "this is the first line"
    expected_second_line = None

    # Act
    actual_first_line = source_provider.get_next_line()
    actual_second_line = source_provider.get_next_line()

    # Assert
    __verify_line(expected_first_line, actual_first_line)
    __verify_line(expected_second_line, actual_second_line)


def test_source_provider_file_two_lines() -> None:
    """
    Test the file source provider with two lines of input.
    """

    # Arrange
    source_provider = FileSourceProvider(__generate_source_path("double-line.txt"))
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


def test_source_provider_file_two_lines_with_blank_between() -> None:
    """
    Test the file source provider with two lines of input with a blank between them.
    """

    # Arrange
    source_provider = FileSourceProvider(
        __generate_source_path("double-line-with-blank.txt")
    )
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


def test_source_provider_file_two_lines_with_blank_between_and_trailing() -> None:
    """
    Test the file source provider with two lines of input with a blank between them and a trailing line.
    """

    # Arrange
    source_provider = FileSourceProvider(
        __generate_source_path("double-line-with-blank-and-trailing.txt")
    )
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
