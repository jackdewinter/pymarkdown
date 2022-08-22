"""
Module to provide tests related to the MD027 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md027_good_block_quote_empty():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with nothing after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_empty.md"
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
def test_md027_good_block_quote_empty_just_blank():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with only a single space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_empty_just_blank.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md009",
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
def test_md027_bad_block_quote_empty_too_many_spaces():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_empty_too_many_spaces.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:3: "
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
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_simple_text.md"
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
def test_md027_good_block_quote_followed_by_heading():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with simple text, an Atx Heading, and more text
    within it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_followed_by_heading.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md022",
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
def test_md027_good_block_quote_indent():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with simple text.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_indent.md"
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
def test_md027_bad_block_quote_indent():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with simple text, indented an extra space.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_indent.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:2:3: "
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
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_indent_plus_one.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:2:4: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_only_one_properly_indented.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_only_one_properly_indented_plus_one.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:4: "
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
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_indent_with_blank.md"
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
def test_md027_good_block_quote_indent_with_blank_space():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with text and a blank line that has a single space.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_indent_with_blank_space.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md009",
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
def test_md027_bad_block_quote_indent_with_blank_two_spaces():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and a blank line that has two spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_indent_with_blank_two_spaces.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_indent_with_blank_two_spaces_plus_one.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:4: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_indent_with_blank_two_spaces_misaligned.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:4: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_indent_with_blank_space_no_start.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md009,md028",
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
def test_md027_bad_two_block_quotes_space_top():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text, where the top has extra space.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_two_block_quotes_space_top.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md028",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:3: "
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
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_two_block_quotes_space_bottom.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md028",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
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
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_misalligned_double_quote.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:4: "
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
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_alligned_double_quote.md"
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
def test_md027_bad_misindented_quote_within_list():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a list and text, with a misindented block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_misindented_quote_within_list.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md032",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
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
def test_md027_bad_misalligned_quote_within_list():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a list and text, with a misaligned block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_misalligned_quote_within_list.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md032",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:5: "
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
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_alligned_quote_within_list.md"
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
def test_md027_good_fenced_block_in_list_in_block_quote():
    """
    A fenced block Within a block quote, surrounded on both sides by lists.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_fenced_block_in_list_in_block_quote.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md031,md032",
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
def test_md027_good_list_within_block_quote_surrounded():
    """
    Block quote containing a paragraph and a single item list, with paragraphs
    and newlines around the block quote
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_list_within_block_quote_surrounded.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md032",
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
def test_md027_good_block_quote_list_block_quote():
    """
    Single line blocks quotes on either side of a list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_list_block_quote.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md032",
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
def test_md027_bad_multiple_blanks_in_block_quote():
    """
    Block quote with two paragraphs and multiple blanks between them.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_multiple_blanks_in_block_quote.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md012",
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
def test_md027_good_indentation_in_block_quote():
    """
    List with 2 items inside of a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_indentation_in_block_quote.md"
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
def test_md027_good_items_with_multiple_lines_in_block_quote():
    """
    List with 2 items inside of a block quote.  First item has multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_items_with_multiple_lines_in_block_quote.md",
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
def test_md027_good_thematic_break_in_block_quote():
    """
    Block quote with two single line paragraphs and a thematic break between them.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_thematic_break_in_block_quote.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md022",
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
def test_md027_good_indented_code_block_in_block_quote():
    """
    Block quote with two single line paragraphs and an indented code block
    break between them.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_indented_code_block_in_block_quote.md",
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
def test_md027_bad_block_quote_misindented_unordered_list_first():
    """
    Block quote with a misaligned multiline unordered list and a properly
    aligned unordered list to follow.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_misindented_unordered_list_first.md",
    )
    supplied_arguments = [
        "--stack-trace",
        "--disable-rules",
        "md005,md007",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:3: "
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
def test_md027_bad_block_quote_misindented_ordered_list_first():
    """
    Block quote with a misaligned multiline ordered list and a properly
    aligned ordered list to follow.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_misindented_ordered_list_first.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md005,md007",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:3: "
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
def test_md027_bad_block_quote_misindented_unordered_list_last():
    """
    Block quote with an aligned multiline unordered list and a misaligned
    unordered list to follow.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_misindented_unordered_list_last.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md005,md007",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
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
def test_md027_bad_block_quote_misindented_ordered_list_last():
    """
    Block quote with an aligned multiline ordered list and a misaligned
    ordered list to follow.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_misindented_ordered_list_last.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md005,md007",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
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
def test_md027_good_block_quote_unordered_list():
    """
    Block quote with an aligned multiline unordered list and an aligned
    unordered list to follow.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_unordered_list.md"
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
def test_md027_good_block_quote_ordered_list():
    """
    Block quote with an aligned multiline ordered list and an aligned
    ordered list to follow.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_ordered_list.md"
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
def test_md027_good_block_quote_unordered_list_unordered_list():
    """
    Block quote with an aligned multiline ordered list and an aligned
    ordered list to follow, with another level of an unordered list in
    the middle.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_unordered_list_unordered_list.md",
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
def test_md027_good_block_quote_unordered_list_ordered_list():
    """
    Block quote with an aligned multiline ordered list and an aligned
    ordered list to follow, with another level of an ordered list in
    the middle.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_unordered_list_ordered_list.md",
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
def test_md027_good_block_quote_ordered_list_ordered_list():
    """
    Block quote with an aligned multiline ordered list and an aligned
    ordered list to follow, with another level of an ordered list in
    the middle.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_ordered_list.md",
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
def test_md027_good_block_quote_ordered_list_unordered_list():
    """
    Block quote with an aligned multiline ordered list and an aligned
    ordered list to follow, with another level of an unordered list in
    the middle.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_unordered_list.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md007",
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
def test_md027_good_block_quote_unordered_list_block_quote_text():
    """
    Block quote with an aligned multiline list and an aligned block
    quote within it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_unordered_list.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md007",
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
def test_md027_bad_block_quote_unordered_list_block_quote_text_first():
    """
    Block quote with an aligned multiline list and an aligned block
    quote within it, but text with an extra space on the first line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_unordered_list_block_quote_text_first.md",
    )
    supplied_arguments = [
        "--stack-trace",
        "--disable-rules",
        "md007",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
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
def test_md027_bad_block_quote_unordered_list_block_quote_text_last():
    """
    Block quote with an aligned multiline list and an aligned block
    quote within it, but text with an extra space on the last line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_unordered_list_block_quote_text_last.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md007",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:7: "
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
def test_md027_good_block_quote_ordered_list_thematic_break():
    """
    Block quote with an aligned multiline list followed by a thematic break.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_thematic_break.md",
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
def test_md027_good_block_quote_ordered_list_thematic_break_misaligned():
    """
    Block quote with an aligned multiline list followed by a thematic break
    which is misaligned.  The misalignment should not matter as it occurs
    within the list's scope, and not the block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_thematic_break_misaligned.md",
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
def test_md027_good_block_quote_ordered_list_atx_heading():
    """
    Block quote with an aligned multiline list followed by an Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_atx_heading.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md022,md023,md032",
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
def test_md027_good_block_quote_ordered_list_setext_heading():
    """
    Block quote with an aligned multiline list followed by an Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_setext_heading.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md022,md023",
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
def test_md027_bad_block_quote_ordered_list_setext_heading_first():
    """
    Block quote with an aligned multiline list followed by a SetExt Heading
    with a misaligned first line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_ordered_list_setext_heading_first.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md022,md023",
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
def test_md027_bad_block_quote_ordered_list_setext_heading_last():
    """
    Block quote with an aligned multiline list followed by a SetExt Heading
    with a misaligned last line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_ordered_list_setext_heading_last.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md022,md023",
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
def test_md027_good_block_quote_ordered_list_indented_code_block():
    """
    Block quote with an aligned multiline list followed by an indented code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_indented_code_block.md",
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
def test_md027_bad_block_quote_ordered_list_indented_code_block_first():
    """
    Block quote with an aligned multiline list followed by an indented code block
    with the first line added an extra space.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_ordered_list_indented_code_block_first.md",
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
def test_md027_bad_block_quote_ordered_list_indented_code_block_last():
    """
    Block quote with an aligned multiline list followed by an indented code block
    with the last line added an extra space.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_ordered_list_indented_code_block_last.md",
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
def test_md027_good_block_quote_ordered_list_fenced_code_block():
    """
    Block quote with an aligned multiline list followed by a fecned code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_fenced_code_block.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md031,md032",
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
def test_md027_good_block_quote_ordered_list_fenced_code_block_indent_first():
    """
    Block quote with an aligned multiline list followed by a fecned code block
    and an indent on the first line of the block.

    Note that the indent is closest to the list, so this rule will not fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_fenced_code_block_indent_first.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md031,md032",
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
def test_md027_good_block_quote_ordered_list_fenced_code_block_indent_second():
    """
    Block quote with an aligned multiline list followed by a fecned code block
    and an indent on the second line of the block.

    Note that the indent is closest to the list, so this rule will not fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_fenced_code_block_indent_second.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md031,md032",
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
def test_md027_good_block_quote_ordered_list_fenced_code_block_indent_third():
    """
    Block quote with an aligned multiline list followed by a fecned code block
    and an indent on the third line of the block.

    Note that the indent is closest to the list, so this rule will not fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_fenced_code_block_indent_third.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md031,md032",
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
def test_md027_good_block_quote_ordered_list_html_block():
    """
    Block quote with an aligned multiline list followed by a HTML block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_html_block.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md032",
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
def test_md027_good_block_quote_ordered_list_html_block_with_indent():
    """
    Block quote with an aligned multiline list followed by a HTML block that is
    indented past the list.

    Note that because HTML blocks are blocks, any indent belongs to the HTML Block
    itself, and is not considered to be extra.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_html_block_with_indent.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md032",
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
def test_md027_good_block_quote_ordered_list_html_block_with_multiline():
    """
    Block quote with an aligned multiline list followed by a HTML block that has
    multiple lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_ordered_list_html_block_with_multiline.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md032",
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
def test_md027_good_block_quote_ordered_list_lrd():
    """
    Block quote with an aligned multiline list followed by an LRD.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_ordered_list_lrd.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md032",
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
def test_md027_bad_list_in_block_quote_after_other_list():
    """
    TBD
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_list_in_block_quote_after_other_list.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md007",
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
def test_md027_bad_list_indentation_in_block_quote_level_0():
    """
    Three levels of nested unordered list items within a block quote, each item
    with simple text.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "test_md007_bad_list_indentation_in_block_quote_level_0.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md007",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
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
def test_md027_bad_block_quote_unordered_list_text_first():
    """
    Block quote with an aligned multiline list including multiline text with
    a misaligned first line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_unordered_list_text_first.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md005,md030",
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
def test_md027_bad_block_quote_unordered_list_text_last():
    """
    Block quote with an aligned multiline list including multiline text with
    a misaligned second line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_unordered_list_text_last.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md005,md030",
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
def test_md027_good_block_quote_with_trailing_empty_line():
    """
    TBD
    reported as https://github.com/jackdewinter/pymarkdown/issues/189
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_with_trailing_empty_line.md",
    )
    supplied_arguments = [
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
def test_md027_issue_189():
    """
    TBD
    reported as https://github.com/jackdewinter/pymarkdown/issues/189
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join("test", "resources", "rules", "md027", "issue-189.md")
    supplied_arguments = [
        "--stack-trace",
        "--disable-rules",
        "md003,md013,md022",
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
def test_md027_issue_189_mini():
    """
    TBD
    reported as https://github.com/jackdewinter/pymarkdown/issues/189
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "issue-189-mini.md"
    )
    supplied_arguments = [
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
