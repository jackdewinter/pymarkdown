"""
Module to provide tests related to the MD036 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

from .utils import write_temporary_configuration


@pytest.mark.rules
def test_md036_proper_headings_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md036 directory that normal atx headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md036/proper_headings_atx.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_headings_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md036 directory that normal setext headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md036/proper_headings_setext.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_with_link():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md036 directory that has a single line wrapped in emphasis
    that contains an inline link.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md036/proper_emphasis_with_link.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_with_text_then_link():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md036 directory that has a single line wrapped in emphasis
    that contains text and then an inline link.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md036/proper_emphasis_with_text_then_link.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_with_text_then_link_then_text():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md036 directory that has a single line wrapped in emphasis
    that contains text, an inline link, and then text again.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md036/proper_emphasis_with_text_then_link_then_text.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_with_text_end_emphasis_more_text():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md036 directory that has a single line wrapped with emphasis
    that contains text, followed by more text.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md036/proper_emphasis_with_text_end_emphasis_more_text.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_within_text():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md036 directory that has a single line with emphasis within
    the text.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md036/proper_emphasis_within_text.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_within_multiline_text():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md036 directory that has a single line with emphasis wrapped
    around the multiline text.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md036/proper_emphasis_within_multiline_text.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_ending_with_punctuation():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md036 directory that has a single line with emphasis wrapped
    around the text, the text ending with punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md036/proper_emphasis_ending_with_punctuation.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_proper_emphasis_ending_with_punctuation_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md036 directory that has a single line with emphasis wrapped
    around the text, the text ending with punctuation, with configuration that makes
    the punctuation okay.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md036": {"punctuation": ".!"}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md036/proper_emphasis_ending_with_punctuation.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md036/proper_emphasis_ending_with_punctuation.md:1:1: "
            + "MD036: Emphasis used instead of a heading (no-emphasis-as-heading,no-emphasis-as-header)\n"
            + "test/resources/rules/md036/proper_emphasis_ending_with_punctuation.md:5:1: "
            + "MD036: Emphasis used instead of a heading (no-emphasis-as-heading,no-emphasis-as-header)\n"
        )

        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md036_valid_emphasis_headings():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md036 directory that has a single line with emphasis wrapped
    around the text, valid golden case for recommending.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md036/valid_emphasis_headings.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md036/valid_emphasis_headings.md:1:1: "
        + "MD036: Emphasis used instead of a heading (no-emphasis-as-heading,no-emphasis-as-header)\n"
        + "test/resources/rules/md036/valid_emphasis_headings.md:5:1: "
        + "MD036: Emphasis used instead of a heading (no-emphasis-as-heading,no-emphasis-as-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

@pytest.mark.rules
def test_md036_valid_emphasis_headings_in_list():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md036 directory that has a single line with emphasis wrapped
    around the text, valid golden case for recommending.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md036/valid_emphasis_headings_in_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md036/valid_emphasis_headings.md:1:1: "
        + "MD036: Emphasis used instead of a heading (no-emphasis-as-heading,no-emphasis-as-header)\n"
        + "test/resources/rules/md036/valid_emphasis_headings.md:5:1: "
        + "MD036: Emphasis used instead of a heading (no-emphasis-as-heading,no-emphasis-as-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

@pytest.mark.rules
def test_md036_valid_emphasis_headings_in_block_quote():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md036 directory that has a single line with emphasis wrapped
    around the text, valid golden case for recommending.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md036/valid_emphasis_headings_in_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md036/valid_emphasis_headings.md:1:1: "
        + "MD036: Emphasis used instead of a heading (no-emphasis-as-heading,no-emphasis-as-header)\n"
        + "test/resources/rules/md036/valid_emphasis_headings.md:5:1: "
        + "MD036: Emphasis used instead of a heading (no-emphasis-as-heading,no-emphasis-as-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
