"""
Module to provide tests related to the MD018 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from test.utils import create_temporary_markdown_file
from typing import List, Tuple

import pytest

# pylint: disable=too-many-lines


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", "rules", "md018", source_file_name)
    return source_path, os.path.abspath(source_path)


@pytest.mark.rules
def test_md018_good_start_spacing(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains properly spaced Atx Headings that are interpretted as such.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_start_spacing.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_good_start_spacing_in_list(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains properly spaced Atx Headings that are interpretted as such
    with a list.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_start_spacing_in_list.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_good_start_spacing_in_block_quotes(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains properly spaced Atx Headings that are interpretted as such
    within a block quote.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_start_spacing_in_block_quote.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_ignore_bad_atx_closed_spacing(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains improperly spaced Atx Headings that are considered to be
    Atx Closed Headings.
    """

    # Arrange
    source_path, _ = __generate_source_path("ignore_bad_atx_closed_spacing.md")
    supplied_arguments = [
        "--disable-rules",
        "md020",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_missing_atx_start_spacing(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a possible Atx Headings without the proper space at the start.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("missing_start_spacing.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{abs_source_path}:3:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_missing_atx_start_spacing_in_list(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a possible Atx Headings without the proper space at the start
    and in a list.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "missing_start_spacing_in_list.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{abs_source_path}:3:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_missing_atx_start_spacing_in_block_quote(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a possible Atx Headings without the proper space at the start
    in a block quote.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "missing_start_spacing_in_block_quote.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{abs_source_path}:3:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_good_with_setext_headings(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a possible Atx Headings without the proper space at the start
    if contained within a SetExt Heading.
    """

    # Arrange
    source_path, _ = __generate_source_path("with_setext_headings.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_good_with_code_blocks(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a possible Atx Headings without the proper space at the start
    if contained within a code block.
    """

    # Arrange
    source_path, _ = __generate_source_path("with_code_blocks.md")
    supplied_arguments = [
        "--disable-rules",
        "md046",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_good_with_html_blocks(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a possible Atx Headings without the proper space at the start
    if contained within a HTML block.
    """

    # Arrange
    source_path, _ = __generate_source_path("with_html_blocks.md")
    supplied_arguments = [
        "--disable-rules",
        "md033,PML100",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{abs_source_path}:2:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)\n""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_codespan(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a code span on its own line.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph_separated_codespan.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{abs_source_path}:3:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_codespan_multi(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a code span over two lines.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph_separated_codespan_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{abs_source_path}:4:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_inline_codespan_multi(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a code span on its own line and a code
    span interupting two of the lines.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph_separated_inline_codespan_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:4:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_inline_rawhtml_multi(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by an html on its own line and
    between lines.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph_separated_inline_rawhtml_multi.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md033",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:4:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_inline_image_multi(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by an image on its own line as well
    as splitting.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph_separated_inline_image_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:8:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_full_image_multi(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a full image on its own line as well
    as splitting.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph_separated_full_image_multi.md",
    )
    supplied_arguments: List[str] = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:5:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_shortcut_image_multi(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a shortcut image on its own line as well
    as splitting.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph_separated_shortcut_image_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:4:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_collapsed_image_multi(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a collapsed image on its own line as well
    as splitting.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph_separated_collapsed_image_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:4:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_inline_link_multi(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a link on its own line as well
    as splitting.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph_separated_inline_link_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:8:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_full_link_multi(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a full link on its own line as well
    as splitting.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph_separated_full_link_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:5:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_shortcut_link_multi(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a shortcut link on its own line as well
    as splitting.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph_separated_shortcut_link_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:4:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_collapsed_link_multi(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a collapsed link on its own line as well
    as splitting.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph_separated_collapsed_link_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:4:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_multiple_within_paragraph_separated_inline_hardbreak_multi(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but separated by a hardbreak.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "multiple_within_paragraph_separated_inline_hardbreak_multi.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_paragraphs_with_starting_whitespace(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but with increasing whitespace.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "paragraphs_with_starting_whitespace.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{abs_source_path}:3:2: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{abs_source_path}:5:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{abs_source_path}:7:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_single_paragraph_with_starting_space(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph but with increasing indent.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "single_paragraph_with_starting_space.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{abs_source_path}:2:2: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{abs_source_path}:3:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{abs_source_path}:4:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_single_paragraph_with_starting_whitespace(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph with a lot of leading space.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "single_paragraph_with_starting_whitespace.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md010",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_bad_single_paragraph_with_whitespace(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple possible Atx Headings without the proper space at the start
    with a single paragraph with leading space.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "single_paragraph_with_whitespace.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md010,md022,md023",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:1:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{abs_source_path}:2:2: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1267(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule handles having a task list as part of the document.
    Reported as Issue 1267, ran up against guard code.
    """

    # Arrange
    source_file_contents = """---
title: abc
---

- [ ] abc
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "--disable-rules",
            "md022",
            "--set",
            "extensions.markdown-task-list-items.enabled=$!True",
            "--stack-trace",
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults()

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_single_trigger_no_pragma(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single trigger of this rule without any containers
    and without any pragmas.
    """

    # Arrange
    source_file_contents = """#Heading 1
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:1:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_single_trigger_pragma_without_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single trigger of this rule without any containers
    and with a single pragma on the line before.
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->
#Heading 1
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:2:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_single_trigger_pragma_with_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single trigger of this rule without any containers
    and with a single pragma two lines before with a blank line between.
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->

#Heading 1
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:3:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_single_trigger_within_list_no_pragma(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles
    """

    # Arrange
    source_file_contents = """1. #Heading 1
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:1:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_single_trigger_within_list_pragma_without_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single pragma that occurs
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->
1. #Heading 1
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:2:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_single_trigger_within_list_pragma_with_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single pragma that occurs
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->

1. #Heading 1
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:3:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_single_trigger_within_block_quote_no_pragma(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles
    """

    # Arrange
    source_file_contents = """> #Heading 1
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:1:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_single_trigger_within_block_quote_pragma_without_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single pragma that occurs
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->
> #Heading 1
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:2:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_single_trigger_within_block_quote_pragma_with_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single pragma that occurs
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->

> #Heading 1
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:3:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_double_trigger_no_pragma(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a double trigger of this rule without any containers
    and without any pragmas.
    """

    # Arrange
    source_file_contents = """#Heading 1
more text here
##Heading 2
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:1:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:3:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_double_trigger_pragma_without_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a double trigger of this rule without any containers
    and with a single pragma on the line before.
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->
#Heading 1
more text here
<!-- pyml disable-next-line line-length -->
##Heading 2
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:2:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:5:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_double_trigger_pragma_with_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single trigger of this rule without any containers
    and with a single pragma two lines before with a blank line between.
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->

#Heading 1
more text here
<!-- pyml disable-next-line line-length -->

##Heading 2
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:3:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:7:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_double_trigger_within_list_no_pragma(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles
    """

    # Arrange
    source_file_contents = """1. #Heading 1
   more text here
   ##Heading 2
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:1:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:3:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_double_trigger_within_list_pragma_without_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single pragma that occurs
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->
1. #Heading 1
   more text here
<!-- pyml disable-next-line line-length -->
   ##Heading 2
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:2:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:5:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_double_trigger_within_list_pragma_with_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single pragma that occurs
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->

1. #Heading 1
   more text here
<!-- pyml disable-next-line line-length -->

   ##Heading 2
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:3:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:7:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_double_trigger_within_block_quote_no_pragma(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles
    """

    # Arrange
    source_file_contents = """> #Heading 1
> more text here
> ##Heading 2
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:1:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:3:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_double_trigger_within_block_quote_pragma_without_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single pragma that occurs
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->
> #Heading 1
> more text here
<!-- pyml disable-next-line line-length -->
> ##Heading 2
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:2:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:5:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_double_trigger_within_block_quote_pragma_with_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single pragma that occurs
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->

> #Heading 1
> some text
<!-- pyml disable-next-line line-length -->

> ##Heading 2
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:3:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:7:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_triple_trigger_no_pragma(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a triple trigger of this rule without any containers
    and without any pragmas.
    """

    # Arrange
    source_file_contents = """#Heading 1
more text here
##Heading 2
more text here
###Heading 3
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:1:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:3:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:5:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_triple_trigger_pragma_without_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a double trigger of this rule without any containers
    and with a single pragma on the line before.
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->
#Heading 1
more text here
<!-- pyml disable-next-line line-length -->
##Heading 2
more text here
<!-- pyml disable-next-line line-length -->
###Heading 3
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:2:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:5:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:8:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_triple_trigger_pragma_with_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single trigger of this rule without any containers
    and with a single pragma two lines before with a blank line between.
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->

#Heading 1
more text here
<!-- pyml disable-next-line line-length -->

##Heading 2
more text here
<!-- pyml disable-next-line line-length -->

###Heading 3
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:3:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:7:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:11:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_triple_trigger_within_list_no_pragma(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles
    """

    # Arrange
    source_file_contents = """1. #Heading 1
   more text here
   ##Heading 2
   more text here
   ###Heading 3
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:1:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:3:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:5:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_triple_trigger_within_list_pragma_without_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single pragma that occurs
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->
1. #Heading 1
   more text here
<!-- pyml disable-next-line line-length -->
   ##Heading 2
   more text here
<!-- pyml disable-next-line line-length -->
   ###Heading 3
"""

    with create_temporary_markdown_file(
        source_file_contents,
    ) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:2:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:5:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:8:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_triple_trigger_within_list_pragma_with_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single pragma that occurs
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->

1. #Heading 1
   more text here
<!-- pyml disable-next-line line-length -->

   ##Heading 2
   more text here
<!-- pyml disable-next-line line-length -->

   ###Heading 3
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:3:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:7:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:11:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_triple_trigger_within_block_quote_no_pragma(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles
    """

    # Arrange
    source_file_contents = """> #Heading 1
> some text
> ##Heading 2
> some text
> ###Heading 3
"""

    with create_temporary_markdown_file(
        source_file_contents,
    ) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:1:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:3:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:5:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_triple_trigger_within_block_quote_pragma_without_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single pragma that occurs
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->
> #Heading 1
> some text
<!-- pyml disable-next-line line-length -->
> ##Heading 2
> some text
<!-- pyml disable-next-line line-length -->
> ###Heading 3
"""

    with create_temporary_markdown_file(
        source_file_contents,
    ) as source_path:
        supplied_arguments = [
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:2:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:5:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:8:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1479_triple_trigger_within_block_quote_pragma_with_blank(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule handles a single pragma that occurs
    """

    # Arrange
    source_file_contents = """<!-- pyml disable-next-line line-length -->

> #Heading 1
> some text
<!-- pyml disable-next-line line-length -->

> ##Heading 2
> some text
<!-- pyml disable-next-line line-length -->

> ###Heading 3
"""

    with create_temporary_markdown_file(
        source_file_contents,
    ) as source_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_path}:3:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:7:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{source_path}:11:3: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_issue_1566(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule handles a single pragma that occurs
    """

    # Arrange
    source_file_contents = """
> > a block
> >
> > 1. another list
> >    properly indented content
> >  1. another list
> >     properly indented content
"""

    with create_temporary_markdown_file(source_file_contents) as source_path:
        supplied_arguments = [
            "-d",
            "md005,md027,md041",
            "scan",
            source_path,
        ]

        expected_results = ExpectedResults()

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md018_query_config() -> None:
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
