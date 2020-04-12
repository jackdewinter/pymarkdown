"""
Module to provide tests for source providers.
"""
from pymarkdown.source_providers import InMemorySourceProvider


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
