"""
Module to provide tests related to the MD039 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md039_good_inline_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains an inline link with no space on either side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "good_inline_link.md"
    )
    supplied_arguments = [
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
def test_md039_bad_inline_link_trailing_space():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "bad_inline_link_trailing_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)"

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md039_bad_inline_link_leading_space():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the left side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "bad_inline_link_leading_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)"

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md039_bad_inline_link_both_space():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on both sides of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "bad_inline_link_both_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)"

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md039_good_full_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains a full link with no space on either side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "good_full_link.md"
    )
    supplied_arguments = [
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
def test_md039_bad_full_link_both_space():
    """
    Test to make sure this rule does trigger with a document that
    contains a full link with space on both sides of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "bad_full_link_both_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)"

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md039_good_collapsed_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains a collapsed link with no space on either side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "good_collapsed_link.md"
    )
    supplied_arguments = [
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
def test_md039_bad_collapsed_link_both_space():
    """
    Test to make sure this rule does not trigger with a document that
    contains a collapsed link with space on both sides of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "bad_collapsed_link_both_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)"

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md039_good_shortcut_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains a shortcut link with no space on either side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "good_shortcut_link.md"
    )
    supplied_arguments = [
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
def test_md039_bad_shortcut_link_both_space():
    """
    Test to make sure this rule does not trigger with a document that
    contains a shortcut link with spaces on both sides of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "bad_shortcut_link_both_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)"

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md039_good_inline_image():
    """
    Test to make sure this rule does not trigger with a document that
    contains an inline image with no space on either side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "good_inline_image.md"
    )
    supplied_arguments = [
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
def test_md039_bad_inline_image_trailing_space():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline image with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "bad_inline_image_trailing_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)"

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md039_bad_inline_image_leading_space():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline image with space on the left side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "bad_inline_image_leading_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)"

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md039_bad_inline_image_both_space():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline image with space on both sides of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "bad_inline_image_both_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)"

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md039_good_full_image():
    """
    Test to make sure this rule does not trigger with a document that
    contains a full image with no space on either side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "good_full_image.md"
    )
    supplied_arguments = [
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
def test_md039_bad_full_image_both_space():
    """
    Test to make sure this rule does not trigger with a document that
    contains a full image with spaces on both sides of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "bad_full_image_both_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)"

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md039_good_collapsed_image():
    """
    Test to make sure this rule does not trigger with a document that
    contains a collapsed image with no space on either side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "good_collapsed_image.md"
    )
    supplied_arguments = [
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
def test_md039_bad_collapsed_image_both_space():
    """
    Test to make sure this rule does trigger with a document that
    contains a collapsed image with spaces on both sides of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "bad_collapsed_image_both_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)"

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md039_good_shortcut_image():
    """
    Test to make sure this rule does not trigger with a document that
    contains a shortcut image with no space on either side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "good_shortcut_image.md"
    )
    supplied_arguments = [
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
def test_md039_bad_shortcut_image_both_space():
    """
    Test to make sure this rule does trigger with a document that
    contains a shortcut image with spaces on both sides of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md039", "bad_shortcut_image_both_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"{source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)"

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
