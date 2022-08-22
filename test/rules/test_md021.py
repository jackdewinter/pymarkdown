"""
Module to provide tests related to the MD021 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md021_good_single_spacing():
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx Closed Heading with single spaces at both ends.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md021", "single_spacing.md"
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
def test_md021_bad_multiple_spacing_both():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx Closed Heading with multiple spaces at both ends.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md021", "multiple_spacing.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        + "(no-multiple-space-closed-atx)\n"
        + f"{source_path}:3:1: "
        + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        + "(no-multiple-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md021_bad_multiple_spacing_left():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx Closed Heading with multiples spaces at the start.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md021", "multiple_spacing_left.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        + "(no-multiple-space-closed-atx)\n"
        + f"{source_path}:3:1: "
        + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        + "(no-multiple-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md021_bad_multiple_spacing_right():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx Closed Heading with multiple spaces at the end.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md021", "multiple_spacing_right.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        + "(no-multiple-space-closed-atx)\n"
        + f"{source_path}:3:1: "
        + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        + "(no-multiple-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md021_good_multiple_spacing_with_inline():
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx Closed Heading with inline emphasis.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md021", "multiple_spacing_with_inline.md"
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
def test_md021_good_multiple_spacing_with_indent():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx Closed Heading with multiple spaces at both ends and indents.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md021", "multiple_spacing_with_indent.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:2: "
        + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        + "(no-multiple-space-closed-atx)\n"
        + f"{source_path}:3:3: "
        + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        + "(no-multiple-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md021_good_single_space_single_tab_before():
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx Closed Heading with tabs at the left end.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md021", "single_space_single_tab_before.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md010",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        + "(no-multiple-space-closed-atx)\n"
        + f"{source_path}:3:1: "
        + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        + "(no-multiple-space-closed-atx)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md021_good_single_space_single_tab_after():
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx Closed Heading with tabs at the end.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md021", "single_space_single_tab_after.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md010",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        + "(no-multiple-space-closed-atx)\n"
        + f"{source_path}:3:1: "
        + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        + "(no-multiple-space-closed-atx)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
