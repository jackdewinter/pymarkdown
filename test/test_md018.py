"""
Module to provide tests related to the MD018 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md018_good_start_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has good atx heading start spacing after
    the first hash.
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has good atx heading start spacing after
    the first hash.
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has good atx heading start spacing after
    the first hash.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md022",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has an atx heading with no spaces after
    initial hash, but ends with a close hash, making it a closed atx.
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has an atx heading with no spaces after
    initial hash.
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has an atx heading with no spaces after
    initial hash.
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has an atx heading with no spaces after
    initial hash.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md018/missing_start_spacing_in_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md018/missing_start_spacing_in_block_quote.md:1:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + "test/resources/rules/md018/missing_start_spacing_in_block_quote.md:3:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has a possible atx heading except that
    it is followed by setext headings.
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has a possible atx heading except that
    it is followed by code blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has a possible atx heading except that
    it is followed by html blocks.
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings each
    one with starting whitespace that would normally be permitted.
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph each one with starting space that would normally be permitted.
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph each one with starting whitespace that would normally be
    permitted.
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md018 directory that has multiple possible atx headings within
    a single paragraph. The first one should be detected as it has a space character
    between the # and the text, but the second one should not as it contains a tab
    character between the # and the text.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md010",
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
