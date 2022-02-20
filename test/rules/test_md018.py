"""
Module to provide tests related to the MD018 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md018_good_start_spacing():
    """
    Test to make sure this rule does not trigger with a document that
    contains properly spaced Atx Headings that are interpretted as such.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/good_start_spacing.md",
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
def test_md018_good_start_spacing_in_list():
    """
    Test to make sure this rule does not trigger with a document that
    contains properly spaced Atx Headings that are interpretted as such
    with a list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/good_start_spacing_in_list.md",
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
def test_md018_good_start_spacing_in_block_quotes():
    """
    Test to make sure this rule does not trigger with a document that
    contains properly spaced Atx Headings that are interpretted as such
    within a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/good_start_spacing_in_block_quote.md",
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
def test_md018_bad_ignore_bad_atx_closed_spacing():
    """
    Test to make sure this rule does not trigger with a document that
    contains improperly spaced Atx Headings that are considered to be
    Atx Closed Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
        "scan",
        "test/resources/rules/md018/ignore_bad_atx_closed_spacing.md",
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
def test_md018_bad_missing_atx_start_spacing():
    """
    Test to make sure this rule does trigger with a document that
    contains a possible Atx Headings without the proper space at the start.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/missing_start_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/missing_start_spacing.md:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/missing_start_spacing.md:3:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_missing_atx_start_spacing_in_list():
    """
    Test to make sure this rule does trigger with a document that
    contains a possible Atx Headings without the proper space at the start
    and in a list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/missing_start_spacing_in_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/missing_start_spacing_in_list.md:1:4: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/missing_start_spacing_in_list.md:3:4: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_missing_atx_start_spacing_in_block_quote():
    """
    Test to make sure this rule does trigger with a document that
    contains a possible Atx Headings without the proper space at the start
    in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/missing_start_spacing_in_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/missing_start_spacing_in_block_quote.md:1:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/missing_start_spacing_in_block_quote.md:3:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_good_with_setext_headings():
    """
    Test to make sure this rule does not trigger with a document that
    contains a possible Atx Headings without the proper space at the start
    if contained within a SetExt Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/with_setext_headings.md",
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
def test_md018_good_with_code_blocks():
    """
    Test to make sure this rule does not trigger with a document that
    contains a possible Atx Headings without the proper space at the start
    if contained within a code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md046",
        "scan",
        "test/resources/rules/md018/with_code_blocks.md",
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
def test_md018_good_with_html_blocks():
    """
    Test to make sure this rule does not trigger with a document that
    contains a possible Atx Headings without the proper space at the start
    if contained within a HTML block.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md033",
        "scan",
        "test/resources/rules/md018/with_html_blocks.md",
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
def test_md018_bad_multiple_within_paragraph():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph.md:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/multiple_within_paragraph.md:2:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_codespan():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a code span on its own line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph_separated_codespan.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph_separated_codespan.md:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/multiple_within_paragraph_separated_codespan.md:3:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_codespan_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a code span over two lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph_separated_codespan_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph_separated_codespan_multi.md:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/multiple_within_paragraph_separated_codespan_multi.md:4:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_inline_codespan_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a code span on its own line and a code
    span interupting two of the lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph_separated_inline_codespan_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph_separated_inline_codespan_multi.md:4:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_inline_rawhtml_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by an html on its own line and
    between lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md033",
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph_separated_inline_rawhtml_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph_separated_inline_rawhtml_multi.md:4:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_inline_image_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by an image on its own line as well
    as splitting.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph_separated_inline_image_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph_separated_inline_image_multi.md:8:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_full_image_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a full image on its own line as well
    as splitting.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph_separated_full_image_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph_separated_full_image_multi.md:5:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_shortcut_image_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a shortcut image on its own line as well
    as splitting.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph_separated_shortcut_image_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph_separated_shortcut_image_multi.md:4:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_collapsed_image_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a collapsed image on its own line as well
    as splitting.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph_separated_collapsed_image_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph_separated_collapsed_image_multi.md:4:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_inline_link_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a link on its own line as well
    as splitting.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph_separated_inline_link_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph_separated_inline_link_multi.md:8:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_full_link_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a full link on its own line as well
    as splitting.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph_separated_full_link_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph_separated_full_link_multi.md:5:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_shortcut_link_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a shortcut link on its own line as well
    as splitting.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph_separated_shortcut_link_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph_separated_shortcut_link_multi.md:4:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_collapsed_link_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a collapsed link on its own line as well
    as splitting.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph_separated_collapsed_link_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph_separated_collapsed_link_multi.md:4:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_inline_hardbreak_multi():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a hardbreak.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/multiple_within_paragraph_separated_inline_hardbreak_multi.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/multiple_within_paragraph_separated_inline_hardbreak_multi.md:3:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_paragraphs_with_starting_whitespace():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but with increasing whitespace.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/paragraphs_with_starting_whitespace.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/paragraphs_with_starting_whitespace.md:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/paragraphs_with_starting_whitespace.md:3:2: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/paragraphs_with_starting_whitespace.md:5:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/paragraphs_with_starting_whitespace.md:7:4: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_single_paragraph_with_starting_space():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but with increasing indent.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/single_paragraph_with_starting_space.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/single_paragraph_with_starting_space.md:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/single_paragraph_with_starting_space.md:2:2: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/single_paragraph_with_starting_space.md:3:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/single_paragraph_with_starting_space.md:4:4: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_single_paragraph_with_starting_whitespace():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph with a lot of leading space.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md010",
        "scan",
        "test/resources/rules/md018/single_paragraph_with_starting_whitespace.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/single_paragraph_with_starting_whitespace.md:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md018_bad_single_paragraph_with_whitespace():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph with leading space.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md010,md022,md023",
        "scan",
        "test/resources/rules/md018/single_paragraph_with_whitespace.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/single_paragraph_with_whitespace.md:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/single_paragraph_with_whitespace.md:2:2: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
