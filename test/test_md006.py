"""
Module to provide tests related to the MD006 rule.
"""
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
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/good_indentation.md",
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
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/good_indentation_in_block_quote.md",
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
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "--disable-rules",
        "MD007",
        "scan",
        "test/resources/rules/md006/bad_indentation.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md006/bad_indentation.md:1:2: MD006: "
        + "Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
        + "test/resources/rules/md006/bad_indentation.md:2:2: MD006: "
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
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/bad_indentation_unordered.md",
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
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "--disable-rules",
        "MD007",
        "scan",
        "test/resources/rules/md006/bad_indentation_in_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md006/bad_indentation_in_block_quote.md:1:4: MD006: "
        + "Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
        + "test/resources/rules/md006/bad_indentation_in_block_quote.md:2:4: MD006: "
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
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "--disable-rules",
        "MD005,Md007",
        "scan",
        "test/resources/rules/md006/good_ignore_bad_second_level.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md006/good_ignore_bad_second_level.md:3:4: "
        + "MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
        + "test/resources/rules/md006/good_ignore_bad_second_level.md:4:5: "
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
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/good_not_ordered.md",
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
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/good_items_with_multiple_lines.md",
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
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/good_items_with_multiple_lines_in_block_quote.md",
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
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/good_indentation_ordered_in_unordered.md",
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
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/good_indentation_unordered_in_ordered.md",
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
    supplied_arguments = [
        "--disable-rules",
        "MD007",
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/bad_indentation_ordered_in_unordered.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md006/bad_indentation_ordered_in_unordered.md:1:2: "
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
def test_md006_bad_indentation_unordered_in_ordered():
    """
    TBD
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "MD007",
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/bad_indentation_unordered_in_ordered.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md006/bad_indentation_unordered_in_ordered.md:2:6: "
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
def test_md006_good_indentation_nested():
    """
    TBD
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD006",
        "--stack-trace",
        "scan",
        "test/resources/rules/md006/good_indentation_nested.md",
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
    supplied_arguments = [
        "--disable-rules",
        "MD007",
        "--enable-rules",
        "MD006",
        "scan",
        "test/resources/rules/md006/bad_indentation_nested.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md006/bad_indentation_nested.md:2:4: "
        + "MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
        + "test/resources/rules/md006/bad_indentation_nested.md:3:4: "
        + "MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
        + "test/resources/rules/md006/bad_indentation_nested.md:5:4: "
        + "MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
        + "test/resources/rules/md006/bad_indentation_nested.md:6:4: "
        + "MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
