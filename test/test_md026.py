"""
Module to provide tests related to the MD003 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

from .utils import write_temporary_configuration


@pytest.mark.rules
def test_md026_ends_without_punctuation_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md026/ends_without_punctuation_atx.md",
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
def test_md026_ends_with_punctuation_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md026/ends_with_punctuation_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md026/ends_with_punctuation_atx.md:0:0: "
        + "MD026: Trailing punctuation in heading (no-trailing-punctuation)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md026_ends_with_punctuation_then_inline_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md026/ends_with_punctuation_then_inline_atx.md",
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
def test_md026_ends_with_punctuation_atx_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD026": {"punctuation": "?!"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md026/ends_with_punctuation_atx.md",
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
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md026_ends_without_punctuation_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md026/ends_without_punctuation_setext.md",
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
def test_md026_ends_with_punctuation_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md026/ends_with_punctuation_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md026/ends_with_punctuation_setext.md:0:0: "
        + "MD026: Trailing punctuation in heading (no-trailing-punctuation)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md026_ends_with_punctuation_then_inline_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md026/ends_with_punctuation_then_inline_setext.md",
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
def test_md026_ends_with_punctuation_setext_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD026": {"punctuation": "?!"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md026/ends_with_punctuation_setext.md",
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
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)
