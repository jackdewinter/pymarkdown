"""
Module to provide tests related to the MD018 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from test.utils import create_temporary_configuration_file

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
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "good_start_spacing.md"
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
def test_md018_good_start_spacing_in_list():
    """
    Test to make sure this rule does not trigger with a document that
    contains properly spaced Atx Headings that are interpretted as such
    with a list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "good_start_spacing_in_list.md"
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
def test_md018_good_start_spacing_in_block_quotes():
    """
    Test to make sure this rule does not trigger with a document that
    contains properly spaced Atx Headings that are interpretted as such
    within a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "good_start_spacing_in_block_quote.md"
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
def test_md018_bad_ignore_bad_atx_closed_spacing():
    """
    Test to make sure this rule does not trigger with a document that
    contains improperly spaced Atx Headings that are considered to be
    Atx Closed Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "ignore_bad_atx_closed_spacing.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md020",
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
def test_md018_bad_missing_atx_start_spacing():
    """
    Test to make sure this rule does trigger with a document that
    contains a possible Atx Headings without the proper space at the start.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "missing_start_spacing.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + f"{source_path}:3:1: "
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
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "missing_start_spacing_in_list.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:4: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + f"{source_path}:3:4: "
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
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "missing_start_spacing_in_block_quote.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + f"{source_path}:3:3: "
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
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "with_setext_headings.md"
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
def test_md018_good_with_code_blocks():
    """
    Test to make sure this rule does not trigger with a document that
    contains a possible Atx Headings without the proper space at the start
    if contained within a code block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "with_code_blocks.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md046",
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
def test_md018_good_with_html_blocks():
    """
    Test to make sure this rule does not trigger with a document that
    contains a possible Atx Headings without the proper space at the start
    if contained within a HTML block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "with_html_blocks.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md033,PML100",
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
def test_md018_bad_multiple_within_paragraph():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "multiple_within_paragraph.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + f"{source_path}:2:1: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "multiple_within_paragraph_separated_codespan.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + f"{source_path}:3:1: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "multiple_within_paragraph_separated_codespan_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + f"{source_path}:4:1: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "multiple_within_paragraph_separated_inline_codespan_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "multiple_within_paragraph_separated_inline_rawhtml_multi.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md033",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "multiple_within_paragraph_separated_inline_image_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:8:3: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "multiple_within_paragraph_separated_full_image_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:3: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "multiple_within_paragraph_separated_shortcut_image_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "multiple_within_paragraph_separated_collapsed_image_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "multiple_within_paragraph_separated_inline_link_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:8:3: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "multiple_within_paragraph_separated_full_link_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:3: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "multiple_within_paragraph_separated_shortcut_link_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "multiple_within_paragraph_separated_collapsed_link_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "multiple_within_paragraph_separated_inline_hardbreak_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
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
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "paragraphs_with_starting_whitespace.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + f"{source_path}:3:2: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + f"{source_path}:5:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + f"{source_path}:7:4: "
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
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "single_paragraph_with_starting_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + f"{source_path}:2:2: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + f"{source_path}:3:3: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + f"{source_path}:4:4: "
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
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md018",
        "single_paragraph_with_starting_whitespace.md",
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
    source_path = os.path.join(
        "test", "resources", "rules", "md018", "single_paragraph_with_whitespace.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md010,md022,md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n"
        + f"{source_path}:2:2: "
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
def test_md018_issue_1267():
    """
    Test to make sure this rule handles having a task list as part of the document.
    Reported as Issue 1267, ran up against guard code.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_file_contents = """---
title: abc
---

- [ ] abc
"""

    with create_temporary_configuration_file(
        source_file_contents, file_name_suffix=".md"
    ) as source_path:
        supplied_arguments = [
            "--disable-rules",
            "md022",
            "--set",
            "extensions.markdown-task-list-items.enabled=$!True",
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


def test_md018_query_config():
    config_test = pluginQueryConfigTest(
        "md018",
        """
  ITEM               DESCRIPTION

  Id                 md018
  Name(s)            no-missing-space-atx
  Short Description  No space present after the hash character on a possible A
                     tx Heading.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md018.md
  """,
    )
    execute_query_configuration_test(config_test)
