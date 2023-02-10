"""
Module to provide tests related to the MD006 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md006_good_indentation():
    """
    Test to make sure this rule does not trigger with a document that
    is only level 1 lists with no indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md006", "good_indentation.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD006",
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
def test_md006_good_indentation_in_block_quote():
    """
    Test to make sure this rule does not trigger with a document that
    is only level 1 lists with no indentation, in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md006", "good_indentation_in_block_quote.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD006",
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
def test_md006_bad_indentation_x():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 lists with a single space of indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md006", "bad_indentation.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "--disable-rules",
        "MD007",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:2: MD006: "
        + "Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
        + f"{source_path}:2:2: MD006: "
        + "Consider starting bulleted lists at the beginning of the line (ul-start-left)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md006_bad_indentation_unordered():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 lists with a single space of indentation.

    Note that this rule only applied to unordered lists, so this
    should not generated any errors.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md006", "bad_indentation_unordered.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD006",
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
def test_md006_bad_indentation_in_block_quote():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 lists with a single space of indentation, all
    in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md006", "bad_indentation_in_block_quote.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "--disable-rules",
        "MD007,md027",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:4: MD006: "
        + "Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
        + f"{source_path}:2:4: MD006: "
        + "Consider starting bulleted lists at the beginning of the line (ul-start-left)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md006_good_ignore_bad_second_level():
    """
    Test to make sure this rule does not trigger with a document that
    is nested lists with level 1 lists properly indented.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md006", "good_ignore_bad_second_level.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "--disable-rules",
        "MD005,Md007",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:4: "
        + "MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
        + f"{source_path}:4:5: "
        + "MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md006_good_not_ordered():
    """
    Test to make sure this rule does not trigger with a document that
    is ordered lists.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md006", "good_not_ordered.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD006",
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
def test_md006_good_items_with_multiple_lines():
    """
    Test to make sure this rule does not trigger with a document that
    is contains list items with multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md006", "good_items_with_multiple_lines.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD006",
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
def test_md006_good_items_with_multiple_lines_in_block_quote():
    """
    Test to make sure this rule does not trigger with a document that
    is contains list items with multiple lines, in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md006",
        "good_items_with_multiple_lines_in_block_quote.md",
    )
    supplied_arguments = [
        "--enable-rules",
        "MD006",
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
def test_md006_good_indentation_ordered_in_unordered():
    """
    TBD
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md006",
        "good_indentation_ordered_in_unordered.md",
    )
    supplied_arguments = [
        "--enable-rules",
        "MD006",
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
def test_md006_good_indentation_unordered_in_ordered():
    """
    TBD
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md006",
        "good_indentation_unordered_in_ordered.md",
    )
    supplied_arguments = [
        "--enable-rules",
        "MD006",
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
def test_md006_bad_indentation_ordered_in_unordered():
    """
    TBD
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md006", "bad_indentation_ordered_in_unordered.md"
    )
    expected_return_code = 1
    supplied_arguments = [
        "--disable-rules",
        "MD007",
        "--enable-rules",
        "MD006",
        "scan",
        source_path,
    ]
    expected_output = f"{source_path}:1:2: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md006_bad_indentation_unordered_in_ordered():
    """
    TBD
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md006", "bad_indentation_unordered_in_ordered.md"
    )
    expected_return_code = 1
    supplied_arguments = [
        "--disable-rules",
        "MD007",
        "--enable-rules",
        "MD006",
        "scan",
        source_path,
    ]
    expected_output = f"{source_path}:2:6: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md006_good_indentation_nested():
    """
    TBD
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md006", "good_indentation_nested.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "--stack-trace",
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
def test_md006_bad_indentation_nested():
    """
    TBD
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md006", "bad_indentation_nested.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "MD007",
        "--enable-rules",
        "MD006",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:4: "
        + "MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
        + f"{source_path}:3:4: "
        + "MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
        + f"{source_path}:5:4: "
        + "MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
        + f"{source_path}:6:4: "
        + "MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md006_issue_478():
    """
    TBD
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join("test", "resources", "rules", "md006", "issue_478.md")
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "--disable-rules",
        "md004,MD007",
        "--stack-trace",
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
