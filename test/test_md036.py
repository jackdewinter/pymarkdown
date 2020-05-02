"""
Module to provide tests related to the MD003 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

from .utils import write_temporary_configuration


@pytest.mark.rules
def test_md036_proper_headings_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md036/proper_headings_atx.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_headings_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md036/proper_headings_setext.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_with_link():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md036/proper_emphasis_with_link.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_with_text_then_link():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md036/proper_emphasis_with_text_then_link.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_with_text_then_link_then_text():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md036/proper_emphasis_with_text_then_link_then_text.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_with_text_end_emphasis_more_text():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md036/proper_emphasis_with_text_end_emphasis_more_text.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_within_text():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md036/proper_emphasis_within_text.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_within_multiline_text():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md036/proper_emphasis_within_multiline_text.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_ending_with_punctuation():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md036/proper_emphasis_ending_with_punctuation.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_ending_with_punctuation_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD036": {"punctuation": ".!"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md036/proper_emphasis_ending_with_punctuation.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md036/proper_emphasis_ending_with_punctuation.md:0:0: "
            + "MD036: Emphasis used instead of a heading (no-emphasis-as-heading,no-emphasis-as-header)\n"
            + "test/resources/rules/md036/proper_emphasis_ending_with_punctuation.md:0:0: "
            + "MD036: Emphasis used instead of a heading (no-emphasis-as-heading,no-emphasis-as-header)\n"
        )

        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md036_valid_emphasis_headings():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md036/valid_emphasis_headings.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md036/valid_emphasis_headings.md:0:0: "
        + "MD036: Emphasis used instead of a heading (no-emphasis-as-heading,no-emphasis-as-header)\n"
        + "test/resources/rules/md036/valid_emphasis_headings.md:0:0: "
        + "MD036: Emphasis used instead of a heading (no-emphasis-as-heading,no-emphasis-as-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
