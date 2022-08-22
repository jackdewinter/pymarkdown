"""
Module to provide tests related to the MD037 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md037_good_valid_emphasis():
    """
    Test to make sure this rule does not trigger with a document that
    contains one or more valid emphasis sequences.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "good_valid_emphasis.md"
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
def test_md037_bad_surrounding_emphasis():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters surrounded by spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_surrounding_emphasis.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:3:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:5:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_bad_leading_emphasis():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters with leading spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_leading_emphasis.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:3:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:5:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_bad_trailing_emphasis():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters followed by spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_trailing_emphasis.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:3:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:5:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_bad_surrounding_emphasis_multiline():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters surrounded by spaces,
    and the emphasis spans lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_surrounding_emphasis_multiline.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:4:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:10:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_bad_surrounding_empahsis_setext():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters surrounded by spaces,
    within an SetExt heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_surrounding_empahsis_setext.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:4:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:10:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_bad_surrounding_empahsis_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters surrounded by spaces,
    within an Atx Heading element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_surrounding_empahsis_atx.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:3:14: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:5:14: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:7:14: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_bad_surrounding_emphasis_containers():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters surrounded by spaces,
    within a single line within a container element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_surrounding_emphasis_containers.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:3:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:5:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_good_emphasis_with_code_span():
    """
    Test to make sure this rule does not trigger with a document that
    contains one or two valid emphasis characters surrounded by spaces,
    within a code span.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "good_emphasis_with_code_span.md"
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
def test_md037_good_no_emphasis_but_stars():
    """
    Test to make sure this rule does not trigger with a document that
    contains one or two valid emphasis characters as part of other parts
    of a paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "good_no_emphasis_but_stars.md"
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
