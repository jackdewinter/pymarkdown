"""
Module to provide tests related to the MD045 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import create_temporary_configuration_file

import pytest


@pytest.mark.rules
def test_md045_good_inline_image():
    """
    Test to make sure this rule does not trigger with a document that
    contains inline images with alt text.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md045", "good_inline_image.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=paragraph",
        "scan",
        source_path,
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
def test_md045_bad_inline_image():
    """
    Test to make sure this rule does trigger with a document that
    contains inline images with no alt text.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md045", "bad_inline_image.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=paragraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD045: Images should have alternate text (alt text) (no-alt-text)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md045_bad_inline_image_whitespace_only():
    """
    Test to make sure this rule does trigger with a document that
    contains inline images with alt text that is whitespace only.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md045", "bad_inline_image_whitespace_only.md"
    )
    supplied_arguments = [
        "--stack-trace",
        "--disable-rules",
        "md039",
        "--set",
        "plugins.md044.names=paragraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD045: Images should have alternate text (alt text) (no-alt-text)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md045_bad_inline_image_whitespace_only_2():
    """
    Test to make sure this rule does trigger with a document that
    contains inline images with alt text that is whitespace only.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_contents = """![\u00a0](image.png])
"""

    with create_temporary_configuration_file(
        source_contents, file_name_suffix=".md"
    ) as source_path:
        supplied_arguments = [
            "--disable-rules",
            "md039",
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"{source_path}:1:1: "
            + "MD045: Images should have alternate text (alt text) (no-alt-text)"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md045_good_full_image():
    """
    Test to make sure this rule does not trigger with a document that
    contains full images with alt text.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md045", "good_full_image.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=paragraph",
        "scan",
        source_path,
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
def test_md045_bad_full_image():
    """
    Test to make sure this rule does trigger with a document that
    contains full images with not alt text.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md045", "bad_full_image.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=paragraph",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD045: Images should have alternate text (alt text) (no-alt-text)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md045_good_shortcut_image():
    """
    Test to make sure this rule does not trigger with a document that
    contains shortcut images with alt text.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md045", "good_shortcut_image.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md044.names=paragraph",
        "scan",
        source_path,
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
