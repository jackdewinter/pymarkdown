"""
Module to provide tests related to the MD027 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md027_good_block_quote_empty():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with nothing after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_block_quote_empty.md",
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
def test_md027_good_block_quote_empty_just_blank():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with only a single space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md009",
        "scan",
        "test/resources/rules/md027/good_block_quote_empty_just_blank.md",
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
def test_md027_bad_block_quote_empty_too_many_spaces():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_empty_too_many_spaces.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_empty_too_many_spaces.md:1:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_simple_text():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with simple text
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_block_quote_simple_text.md",
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
def test_md027_good_block_quote_followed_by_heading():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with simple text, an Atx Heading, and more text
    within it.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md022",
        "scan",
        "test/resources/rules/md027/good_block_quote_followed_by_heading.md",
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
def test_md027_good_block_quote_indent():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with simple text.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_block_quote_indent.md",
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
def test_md027_bad_block_quote_indent():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with simple text, indented an extra space.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_indent.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_indent.md:1:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + "test/resources/rules/md027/bad_block_quote_indent.md:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_indent_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with simple text indented by 2 spaces, with
    the entire block being indented by 1 space.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_indent_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_indent_plus_one.md:1:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + "test/resources/rules/md027/bad_block_quote_indent_plus_one.md:2:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_only_one_properly_indented():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text, where only one line is properly
    indented.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_only_one_properly_indented.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_only_one_properly_indented.md:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_only_one_properly_indented_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text, where only one line is properly
    indented, with the entire block being indented by 1.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_only_one_properly_indented_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_only_one_properly_indented_plus_one.md:2:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_indent_with_blank():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with text and a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_block_quote_indent_with_blank.md",
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
def test_md027_good_block_quote_indent_with_blank_space():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with text and a blank line that has a single space.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md009",
        "scan",
        "test/resources/rules/md027/good_block_quote_indent_with_blank_space.md",
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
def test_md027_bad_block_quote_indent_with_blank_two_spaces():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and a blank line that has two spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_indent_with_blank_two_spaces.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_indent_with_blank_two_spaces.md:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_indent_with_blank_two_spaces_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and a blank line that has two spaces,
    the entire block being indented by 1.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_indent_with_blank_two_spaces_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_indent_with_blank_two_spaces_plus_one.md:2:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_indent_with_blank_two_spaces_misaligned():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and a blank line that has two spaces,
    even though the line has extra indent before the block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_indent_with_blank_two_spaces_misaligned.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_indent_with_blank_two_spaces_misaligned.md:2:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_indent_with_blank_space_no_start():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with text and a blank line that has no bq start.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md009,md028",
        "scan",
        "test/resources/rules/md027/good_block_quote_indent_with_blank_space_no_start.md",
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
def test_md027_bad_two_block_quotes_space_top():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text, where the top has extra space.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md028",
        "scan",
        "test/resources/rules/md027/bad_two_block_quotes_space_top.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_two_block_quotes_space_top.md:1:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_two_block_quotes_space_bottom():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text, where the bottom has extra space.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md028",
        "scan",
        "test/resources/rules/md027/bad_two_block_quotes_space_bottom.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_two_block_quotes_space_bottom.md:3:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_misalligned_double_quote():
    """
    Test to make sure this rule does trigger with a document that
    contains a double block quote with text, where the text is aligned
    even though the block quotes are not.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_misalligned_double_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_misalligned_double_quote.md:2:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_aligned_double_quote():
    """
    Test to make sure this rule does not trigger with a document that
    contains a double block quote with text that is aligned to the block
    quote, not the text.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_alligned_double_quote.md",
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
def test_md027_bad_misalligned_quote_within_list():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a list and text, with a misaligned block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md032",
        "scan",
        "test/resources/rules/md027/bad_misalligned_quote_within_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_misalligned_quote_within_list.md:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_aligned_quote_within_list():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a list and text, all properly aligned.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_alligned_quote_within_list.md",
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
def test_md027_good_fenced_block_in_list_in_block_quote():
    """
    A fenced block Within a block quote, surrounded on both sides by lists.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md031,md032",
        "scan",
        "test/resources/rules/md027/good_fenced_block_in_list_in_block_quote.md",
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
def test_md027_good_list_within_block_quote_surrounded():
    """
    Block quote containing a paragraph and a single item list, with paragraphs
    and newlines around the block quote
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md032",
        "scan",
        "test/resources/rules/md027/good_list_within_block_quote_surrounded.md",
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
def test_md027_good_block_quote_list_block_quote():
    """
    Single line blocks quotes on either side of a list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md032",
        "scan",
        "test/resources/rules/md027/good_block_quote_list_block_quote.md",
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
def test_md027_bad_multiple_blanks_in_block_quote():
    """
    Block quote with two paragraphs and multiple blanks between them.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md012",
        "scan",
        "test/resources/rules/md027/bad_multiple_blanks_in_block_quote.md",
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
def test_md027_good_indentation_in_block_quote():
    """
    List with 2 items inside of a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_indentation_in_block_quote.md",
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
def test_md027_good_items_with_multiple_lines_in_block_quote():
    """
    List with 2 items inside of a block quote.  First item has multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_items_with_multiple_lines_in_block_quote.md",
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
def test_md027_good_thematic_break_in_block_quote():
    """
    Block quote with two single line paragraphs and a thematic break between them.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md022",
        "scan",
        "test/resources/rules/md027/good_thematic_break_in_block_quote.md",
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
def test_md027_good_indented_code_block_in_block_quote():
    """
    Block quote with two single line paragraphs and an indented code block
    break between them.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_indented_code_block_in_block_quote.md",
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
