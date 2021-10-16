"""
Module to provide tests related to the MD020 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md020_good_start_spacing():
    """
    Test to make sure this rule does not trigger with a document that
    contains multiple Atx Closed Headings with proper spacing.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/good_start_spacing.md",
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
def test_md020_good_start_spacing_in_list():
    """
    Test to make sure this rule does not trigger with a document that
    contains multiple Atx Closed Headings with proper spacing in a list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/good_start_spacing_in_list.md",
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
def test_md020_good_start_spacing_in_block_quote():
    """
    Test to make sure this rule does not trigger with a document that
    contains multiple Atx Closed Headings with proper spacing in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/good_start_spacing_in_block_quote.md",
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
def test_md020_bad_ignore_bad_atx_spacing():
    """
    Test to make sure this rule does not trigger with a document that
    contains multiple Atx Headings that are not closed.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md018",
        "scan",
        "test/resources/rules/md020/ignore_bad_atx_spacing.md",
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
def test_md020_bad_missing_start_spacing():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings with missing spacing at the start.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/missing_start_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/missing_start_spacing.md:1:1: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/missing_start_spacing.md:3:1: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_missing_start_spacing_in_list():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings with missing spacing at the start,
    in a list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/missing_start_spacing_in_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/missing_start_spacing_in_list.md:1:4: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/missing_start_spacing_in_list.md:3:4: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_missing_start_spacing_in_block_quotes():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings with missing spacing at the start
    in block quotes.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md009",
        "scan",
        "test/resources/rules/md020/missing_start_spacing_in_block_quotes.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/missing_start_spacing_in_block_quotes.md:1:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/missing_start_spacing_in_block_quotes.md:3:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_missing_end_spacingx():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings with missing spacing at the end.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/missing_end_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/missing_end_spacing.md:1:12: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/missing_end_spacing.md:3:13: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_missing_end_spacing_in_list():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings with missing spacing at the end in a list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/missing_end_spacing_in_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/missing_end_spacing_in_list.md:1:15: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/missing_end_spacing_in_list.md:3:16: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_missing_end_spacing_in_block_quotes():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings with missing spacing at the end in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/missing_end_spacing_in_block_quotes.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/missing_end_spacing_in_block_quotes.md:1:14: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/missing_end_spacing_in_block_quotes.md:3:15: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_good_almost_missing_end_spacing():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Headings that might be Atx Closed, except for
    extra characters after the last #
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/almost_missing_end_spacing.md",
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
def test_md020_bad_missing_both_spacing():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings with missing spacing at the
    start and the end.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/missing_both_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/missing_both_spacing.md:1:1: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/missing_both_spacing.md:3:1: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_missing_both_spacing_in_list():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings with missing spacing at the
    start and the end in a list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/missing_both_spacing_in_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/missing_both_spacing_in_list.md:1:4: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/missing_both_spacing_in_list.md:3:4: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_missing_both_spacing_in_block_quotes():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings with missing spacing at the
    start and the end in block quotes.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md009",
        "scan",
        "test/resources/rules/md020/missing_both_spacing_in_block_quotes.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/missing_both_spacing_in_block_quotes.md:1:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/missing_both_spacing_in_block_quotes.md:3:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_good_with_setext_headings():
    """
    Test to make sure this rule does not trigger with a document that
    contains multiple Atx Closed Headings within a SetExt heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/with_setext_headings.md",
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
def test_md020_good_with_code_blocks():
    """
    Test to make sure this rule does not trigger with a document that
    contains multiple Atx Closed Headings within a code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md046",
        "scan",
        "test/resources/rules/md020/with_code_blocks.md",
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
def test_md020_good_with_html_blocks():
    """
    Test to make sure this rule does not trigger with a document that
    contains multiple Atx Closed Headings within a HTML block.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md033",
        "scan",
        "test/resources/rules/md020/with_html_blocks.md",
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
def test_md020_bad_multiple_within_paragraph():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph.md:1:1: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/multiple_within_paragraph.md:2:1: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_multiple_within_paragraph_separated_codespan():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    separated by the code span.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph_separated_codespan.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph_separated_codespan.md:1:1: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/multiple_within_paragraph_separated_codespan.md:3:1: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_multiple_within_paragraph_separated_codespan_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    separated by the multi line code span.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph_separated_codespan_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph_separated_codespan_multi.md:1:1: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/multiple_within_paragraph_separated_codespan_multi.md:4:1: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_multiple_within_paragraph_separated_inline_codespan_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    separated by the multiple types of code span.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph_separated_inline_codespan_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph_separated_inline_codespan_multi.md:4:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_multiple_within_paragraph_separated_inline_rawhtml_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    separated by the multiple types of raw html.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md033",
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph_separated_inline_rawhtml_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph_separated_inline_rawhtml_multi.md:4:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_multiple_within_paragraph_separated_inline_image_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    separated by the multiple types of inline images.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph_separated_inline_image_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph_separated_inline_image_multi.md:8:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_multiple_within_paragraph_separated_full_image_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    separated by the multiple types of full images.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph_separated_full_image_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph_separated_full_image_multi.md:5:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_multiple_within_paragraph_separated_shortcut_image_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    separated by the multiple types of shortcut images.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph_separated_shortcut_image_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph_separated_shortcut_image_multi.md:4:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_multiple_within_paragraph_separated_collapsed_image_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    separated by the multiple types of collapsed images.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph_separated_collapsed_image_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph_separated_collapsed_image_multi.md:4:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_multiple_within_paragraph_separated_inline_link_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    separated by the multiple types of inline links.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph_separated_inline_link_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph_separated_inline_link_multi.md:8:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_multiple_within_paragraph_separated_full_link_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    separated by the multiple types of full links.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph_separated_full_link_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph_separated_full_link_multi.md:5:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_multiple_within_paragraph_separated_separated_shortcut_link_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    separated by the multiple types of separated links.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph_separated_shortcut_link_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph_separated_shortcut_link_multi.md:4:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_multiple_within_paragraph_separated_collapsed_link_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    separated by the multiple types of collapsed links.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph_separated_collapsed_link_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph_separated_collapsed_link_multi.md:4:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_multiple_within_paragraph_separated_inline_hardbreak_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    separated by at least one hard line break.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/multiple_within_paragraph_separated_inline_hardbreak_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/multiple_within_paragraph_separated_inline_hardbreak_multi.md:3:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_paragraphs_with_starting_whitespace():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    with increasing starting whitespace.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/paragraphs_with_starting_whitespace.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/paragraphs_with_starting_whitespace.md:1:1: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/paragraphs_with_starting_whitespace.md:3:2: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/paragraphs_with_starting_whitespace.md:5:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/paragraphs_with_starting_whitespace.md:7:4: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_single_paragraph_with_starting_whitespace():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    with increasing starting whitespace.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md020/single_paragraph_with_starting_whitespace.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/single_paragraph_with_starting_whitespace.md:1:1: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/single_paragraph_with_starting_whitespace.md:2:2: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/single_paragraph_with_starting_whitespace.md:3:3: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/single_paragraph_with_starting_whitespace.md:4:4: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_single_paragraph_with_whitespace_at_start():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    including extra whitespace at the start of the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md010",
        "scan",
        "test/resources/rules/md020/single_paragraph_with_whitespace_at_start.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/single_paragraph_with_whitespace_at_start.md:1:1: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/single_paragraph_with_whitespace_at_start.md:2:2: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md020_bad_single_paragraph_with_whitespace_at_end():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Closed Headings within a paragraph
    including extra whitespace at the end of the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md010,md022,md023",
        "scan",
        "test/resources/rules/md020/single_paragraph_with_whitespace_at_end.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md020/single_paragraph_with_whitespace_at_end.md:1:13: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
        + "test/resources/rules/md020/single_paragraph_with_whitespace_at_end.md:2:15: "
        + "MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
