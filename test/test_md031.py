"""
Module to provide tests related to the MD031 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md031_bad_configuration_list_items():
    """
    Test to verify that a configuration error is thrown when supplying the
    list_items value with a string that is not a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md031.list_items=bad",
        "--strict-config",
        "scan",
        "test/resources/rules/md031/good_fenced_block_surrounded.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md031.list_items' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md031_good_fenced_block_surrounded():
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced code block surrounded by blank lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/good_fenced_block_surrounded.md",
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
def test_md031_bad_fenced_block_only_after():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block only followed by blank lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/bad_fenced_block_only_after.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md031/bad_fenced_block_only_after.md:2:1: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md031_bad_fenced_block_only_before():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block only prefaced by blank lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/bad_fenced_block_only_before.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md031/bad_fenced_block_only_before.md:5:1: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md031_good_fenced_block_at_start():
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced code block at the start of the document.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/good_fenced_block_at_start.md",
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
def test_md031_good_fenced_block_at_end():
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced code block at the end of the document.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md047",
        "scan",
        "test/resources/rules/md031/good_fenced_block_at_end.md",
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
def test_md031_bad_fenced_block_only_after_start_indent():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block right after a text line, with the
    fenced code block indented by 1.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/bad_fenced_block_only_after_start_indent.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md031/bad_fenced_block_only_after_start_indent.md:2:2: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md031_bad_fenced_block_only_before_start_indent():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block right before a text line, with the
    fenced code block indented by 1.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/bad_fenced_block_only_before_start_indent.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md031/bad_fenced_block_only_before_start_indent.md:5:1: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md031_bad_fenced_block_only_before_end_indent():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block right before a text line, with the
    end fenced code block indented by 1.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/bad_fenced_block_only_before_end_indent.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md031/bad_fenced_block_only_before_end_indent.md:5:2: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md031_good_fenced_block_surrounded_in_block_quote():
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced code block within a block quote surrounded by
    blank lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/good_fenced_block_surrounded_in_block_quote.md",
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
def test_md031_good_fenced_block_surrounded_in_ordered_list():
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced code block within an ordered list surrounded by
    blank lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/good_fenced_block_surrounded_in_ordered_list.md",
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
def test_md031_good_fenced_block_surrounded_in_unordered_list():
    """
    Test to make sure this rule does not trigger with a document that
    contains a fenced code block within an unordered list surrounded by
    blank lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/good_fenced_block_surrounded_in_unordered_list.md",
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
def test_md031_bad_fenced_block_only_after_in_block_quote():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block within a block quote the is immediately
    after a text line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/bad_fenced_block_only_after_in_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md031/bad_fenced_block_only_after_in_block_quote.md:2:3: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md031_bad_fenced_block_only_after_in_unordered_list():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block within an unordered list the is immediately
    after a text line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/bad_fenced_block_only_after_in_unordered_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md031/bad_fenced_block_only_after_in_unordered_list.md:2:3: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md031_bad_fenced_block_only_before_in_unordered_list():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block within an unordered list tha is immediately
    before a text line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/bad_fenced_block_only_before_in_unordered_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md031/bad_fenced_block_only_before_in_unordered_list.md:5:3: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md031_good_fenced_block_only_after_in_unordered_list_with_config():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block within an unordered list tha is immediately
    after a text line, but configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md031.list_items=$!False",
        "--strict-config",
        "scan",
        "test/resources/rules/md031/bad_fenced_block_only_after_in_unordered_list.md",
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
def test_md031_good_fenced_block_only_before_in_unordered_list_with_config():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block within an unordered list tha is immediately
    before a text line, but configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md031.list_items=$!False",
        "scan",
        "test/resources/rules/md031/bad_fenced_block_only_before_in_unordered_list.md",
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
def test_md031_good_fenced_block_empty():
    """
    Test to make sure this rule does not trigger with a document that
    contains an empty fenced code block surrounded by blank lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/good_fenced_block_empty.md",
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
def test_md031_bad_fenced_block_in_block_quote():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block surrounded by block quotes.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md031/bad_fenced_block_in_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md031/bad_fenced_block_in_block_quote.md:2:1: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)\n"
        + "test/resources/rules/md031/bad_fenced_block_in_block_quote.md:4:1: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md031_bad_fenced_block_in_list():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block surrounded by lists.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md032",
        "scan",
        "test/resources/rules/md031/bad_fenced_block_in_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md031/bad_fenced_block_in_list.md:2:1: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)\n"
        + "test/resources/rules/md031/bad_fenced_block_in_list.md:4:1: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md031_bad_fenced_block_in_block_quote_in_list():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block surrounded by block quotes within a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md032",
        "scan",
        "test/resources/rules/md031/bad_fenced_block_in_block_quote_in_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md031/bad_fenced_block_in_block_quote_in_list.md:2:4: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)\n"
        + "test/resources/rules/md031/bad_fenced_block_in_block_quote_in_list.md:4:4: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md031_bad_fenced_block_in_list_in_block_quote():
    """
    Test to make sure this rule does trigger with a document that
    contains a fenced code block surrounded by  list item within a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md032",
        "scan",
        "test/resources/rules/md031/bad_fenced_block_in_list_in_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md031/bad_fenced_block_in_list_in_block_quote.md:2:3: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)\n"
        + "test/resources/rules/md031/bad_fenced_block_in_list_in_block_quote.md:4:3: "
        + "MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
