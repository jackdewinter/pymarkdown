"""
Module to provide tests related to the MD022 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from test.utils import create_temporary_configuration_file

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md022_bad_proper_line_spacing_atx() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains atx headings with proper spacing around them.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "proper_line_spacing_atx.md"
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
def test_md022_good_proper_line_spacing_setext() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains setext headings with proper spacing around them.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "proper_line_spacing_setext.md"
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
def test_md022_bad_no_line_spacing_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with no proper spacing around them.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "no_line_spacing_atx.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:1:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:4:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:4:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_atx_in_same_block_quote() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with no proper spacing around them in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "no_line_spacing_atx_in_same_block_quote.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:4:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:4:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_atx_in_same_list_item() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with no proper spacing around them in a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "no_line_spacing_atx_in_same_list_item.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:4:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:4:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_atx_in_different_list_items() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with no proper spacing around them in different list items.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "no_line_spacing_atx_in_different_list_items.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:4:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:4:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_before_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with no proper spacing before them.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "no_line_spacing_before_atx.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:5:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_before_atx_in_same_list_item() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with no proper spacing before them in a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "no_line_spacing_before_atx_in_same_list_item.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_before_atx_in_different_list_items() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with no proper spacing before them in different list items.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "no_line_spacing_before_atx_in_different_list_items.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_before_atx_in_same_block_quote() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with no proper spacing before them in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "no_line_spacing_before_atx_in_same_block_quote.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_before_setext() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains setext headings with no proper spacing before them.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "no_line_spacing_before_setext.md"
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
def test_md022_bad_no_line_spacing_after_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with no proper spacing after them.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "no_line_spacing_after_atx.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:1:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:5:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_after_atx_in_same_list_item() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with no proper spacing after them in the same list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "no_line_spacing_after_atx_in_same_list_item.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_after_atx_in_same_block_quote() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with no proper spacing after them in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "no_line_spacing_after_atx_in_same_block_quote.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_after_atx_in_different_list_items() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with no proper spacing after them in different list items.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "no_line_spacing_after_atx_in_different_list_items.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_after_atx_in_different_block_quotes() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with no proper spacing after them in different block quotes.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "no_line_spacing_after_atx_in_different_block_quotes.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md028",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:1:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:5:3: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_atx_with_html_and_good_line_spacing() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains atx headings with good spacing between them and the HTML
    blocks on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "atx_with_html_and_good_line_spacing.md"
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
def test_md022_bad_atx_with_html_and_bad_line_spacing() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings without good spacing between them and the HTML
    blocks on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "atx_with_html_and_bad_line_spacing.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:3:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:8:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_atx_with_paragraph_and_good_line_spacing() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains atx headings with good spacing between them and the paragraphs
    on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "atx_with_paragraph_and_good_line_spacing.md",
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
def test_md022_bad_atx_with_paragraph_and_bad_line_spacing() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with good spacing between them and the paragraphs
    on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "atx_with_paragraph_and_bad_line_spacing.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:7:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_atx_with_code_block_and_good_line_spacing() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains atx headings with good spacing between them and the code
    blocks on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "atx_with_code_block_and_good_line_spacing.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md040",
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
def test_md022_bad_atx_with_code_block_and_bad_line_spacing() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with bad spacing between them and the code
    blocks on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "atx_with_code_block_and_bad_line_spacing.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md040,md031",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:4:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:9:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_atx_with_thematic_break_and_good_line_spacing() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains atx headings with good spacing between them and the thematic
    breaks on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "atx_with_thematic_break_and_good_line_spacing.md",
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
def test_md022_bad_atx_with_thematic_break_and_bad_line_spacing() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with bad spacing between them and the thematic
    breaks on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "atx_with_thematic_break_and_bad_line_spacing.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:7:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_setext() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with bad spacing after them and the
    paragraphs on either side.

    Note that setext grabs the last paragraph before the marker and puts it as the
    heading.  As such, testing this for one line space before is implied as one line
    space is required to break up the paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "no_line_spacing_setext.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:1:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:6:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_no_line_spacing_after_setext() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains setext headings with bad spacing after them and the
    paragraphs on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "no_line_spacing_after_setext.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:1:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:6:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_setext_with_code_block_and_good_line_spacing() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains setext headings with good spacing between them and the
    code blocks on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "setext_with_code_block_and_good_line_spacing.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md040",
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
def test_md022_bad_setext_with_code_block_and_bad_line_spacing() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains setext headings with bad spacing between them and the
    code blocks on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "setext_with_code_block_and_bad_line_spacing.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md040,md031",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:4:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:10:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_setext_with_html_and_good_line_spacing() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains setext headings with good spacing between them and the
    HTML blocks on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "setext_with_html_and_good_line_spacing.md",
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
def test_md022_bad_setext_with_html_and_bad_line_spacing() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains setext headings with bad spacing between them and the
    HTML blocks on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "setext_with_html_and_bad_line_spacing.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:3:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:9:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_setext_with_thematic_break_and_good_line_spacing() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains setext headings with good spacing between them and the
    thematic breaks on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "setext_with_thematic_break_and_good_line_spacing.md",
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
def test_md022_bad_setext_with_thematic_break_and_bad_line_spacing() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains setext headings with bad spacing between them and the
    thematic breaks on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "setext_with_thematic_break_and_bad_line_spacing.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:8:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_proper_line_spacing_atx_with_alternate_lines_above() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with good spacing between them and the
    lines on either side, but configuration the requests more space.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "proper_line_spacing_atx.md"
    )
    supplied_configuration = {"plugins": {"md022": {"lines_above": 2}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"{os.path.abspath(source_path)}:7:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md022_good_double_line_spacing_above_atx_with_alternate_lines_above() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains atx headings with extra spacing between them and the
    lines on either side, but configuration that requests more space.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "double_line_spacing_above_atx.md"
    )
    supplied_configuration = {"plugins": {"md022": {"lines_above": 2}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "--disable-rules",
            "md012",
            "-c",
            configuration_file,
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
def test_md022_bad_proper_line_spacing_atx_with_alternate_lines_below() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains atx headings with good spacing between them and the
    lines on either side, but configuration the requests more space below.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "proper_line_spacing_atx.md"
    )
    supplied_configuration = {"plugins": {"md022": {"lines_below": 2}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"{os.path.abspath(source_path)}:1:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)\n"
            + f"{os.path.abspath(source_path)}:7:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md022_good_double_line_spacing_above_atx_with_alternate_lines_below() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains atx headings with extra spacing between them and the
    lines below, but configuration the requests more space below.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "double_line_spacing_below_atx.md"
    )
    supplied_configuration = {"plugins": {"md022": {"lines_below": 2}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "--disable-rules",
            "md012",
            "-c",
            configuration_file,
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
def test_md022_good_double_line_spacing_above_and_below_atx_with_alternate_lines_both() -> (
    None
):
    """
    Test to make sure this rule does not trigger with a document that
    contains atx headings with extra spacing above them and the
    lines on either side, but configuration the requests more space above.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "double_line_spacing_above_and_below_atx.md",
    )
    supplied_configuration = {
        "plugins": {"md022": {"lines_below": 2, "lines_above": 2}}
    }
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "--disable-rules",
            "md012",
            "-c",
            configuration_file,
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
def test_md022_good_alternating_heading_types() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains alternating heading types with good spacing between them and the
    lines on either side.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "alternating_heading_types.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "MD003,md025",
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
def test_md022_bad_alternating_heading_types_with_alternate_spacing() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains alternating heading types with good spacing between them and the
    lines on either side, but alternative configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "alternating_heading_types.md"
    )
    supplied_configuration = {
        "plugins": {"md022": {"lines_below": 2, "lines_above": 2}}
    }
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "--disable-rules",
            "MD003,md025",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"{os.path.abspath(source_path)}:1:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)\n"
            + f"{os.path.abspath(source_path)}:3:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
            + f"{os.path.abspath(source_path)}:3:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)\n"
            + f"{os.path.abspath(source_path)}:6:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
            + f"{os.path.abspath(source_path)}:6:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)\n"
            + f"{os.path.abspath(source_path)}:8:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
            + f"{os.path.abspath(source_path)}:8:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md022_bad_alternating_heading_types_with_alternate_spacing_and_bad_config() -> (
    None
):
    """
    Test to make sure this rule does trigger with a document that
    contains alternating heading types with good spacing between them and the
    lines on either side, but alternative configuration.  Note that due to
    bad configuration on the `below` setting, it will be ignored.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "alternating_heading_types.md"
    )
    supplied_configuration = {
        "plugins": {"md022": {"lines_below": -2, "lines_above": 2}}
    }
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "--disable-rules",
            "MD003,md025",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"{os.path.abspath(source_path)}:3:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
            + f"{os.path.abspath(source_path)}:6:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
            + f"{os.path.abspath(source_path)}:8:1: "
            + "MD022: Headings should be surrounded by blank lines. "
            + "[Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md022_bad_alternating_heading_types_with_alternate_spacing_and_bad_config_strict_mode() -> (
    None
):
    """
    Test to make sure this rule fails with alternative configuration that is invalid.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "alternating_heading_types.md"
    )
    supplied_configuration = {
        "plugins": {"md022": {"lines_below": -2, "lines_above": 2}}
    }
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "--strict-config",
            "--disable-rules",
            "MD003",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = (
            "BadPluginError encountered while configuring plugins:\n"
            + "The value for property 'plugins.md022.lines_below' is not valid: Value must not be zero or a positive integer.\n"
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md022_good_unordered_list_into_atx_into_paragraph() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx heading types with good spacing between them and
    the list item above and the paragraph below.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "unordered_list_into_atx_into_paragraph.md",
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
def test_md022_bad_heading_surrounded_by_block_quote() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading types with block quotes directly before
    and after the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "bad_heading_surrounded_by_block_quote.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_bad_heading_surrounded_by_list() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading types with list items directly before
    and after the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "bad_heading_surrounded_by_list.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md032",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_good_heading_in_block_quote() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx heading in a block quote, with nicely spaced
    elements before and after the block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "good_heading_in_block_quote.md"
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
def test_md022_good_heading_in_list() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx heading in a list item, with nicely spaced
    elements before and after the list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "good_heading_in_list.md"
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
def test_md022_link_reference_definition_before_header() -> None:
    """
    Test to make sure this rule
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "link_reference_definition_before_header.md",
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
def test_md022_link_reference_definition_around_header() -> None:
    """
    Test to make sure this rule
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md022",
        "bad_link_reference_definition_around_header.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md012",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:1:1: MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 2; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{os.path.abspath(source_path)}:7:1: MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 2; Above] (blanks-around-headings,blanks-around-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_fenced_block_before_header() -> None:
    """
    Test to make sure this rule
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md022", "fenced_block_before_header.md"
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
def test_md022_issue_1268() -> None:
    """
    Test to make sure this rule
    """

    # Arrange
    scanner = MarkdownScanner()
    source_file_contents = """# My header

<!-- pyml disable-num-lines 3 md011,md013-->

Some long lines
"""
    with create_temporary_configuration_file(
        source_file_contents, file_name_suffix=".md"
    ) as source_path:
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
def test_md022_good_with_pragmas_blanks_after_around_and_before() -> None:
    """
    Test to make sure this rule works properly with pragmas.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_file_contents = """# Heading 1

<!--pyml disable-num-lines 1 md012-->

Some text

Some more text

<!--pyml disable-num-lines 1 md012-->

## Heading 2

<!--pyml disable-num-lines 5 md012-->

## Heading 3
"""
    with create_temporary_configuration_file(
        source_file_contents, file_name_suffix=".md"
    ) as source_path:
        supplied_configuration = {
            "plugins": {"md022": {"lines_below": 1, "lines_above": 1}}
        }
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                "-c",
                configuration_file,
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
def test_md022_bad_with_pragmas_blanks_after_around_and_before() -> None:
    """
    Test to make sure this rule works properly with pragmas.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_file_contents = """# Heading 1

<!--pyml disable-num-lines 1 md012-->

Some text

Some more text

<!--pyml disable-num-lines 1 md012-->

## Heading 2

<!--pyml disable-num-lines 5 md012-->

## Heading 3
"""
    with create_temporary_configuration_file(
        source_file_contents, file_name_suffix=".md"
    ) as source_path:
        supplied_configuration = {
            "plugins": {"md022": {"lines_below": 2, "lines_above": 2}}
        }
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                "-c",
                configuration_file,
                "scan",
                source_path,
            ]

            expected_return_code = 1
            expected_output = f"""{source_path}:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)
{source_path}:11:1: MD022: Headings should be surrounded by blank lines. [Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)
{source_path}:11:1: MD022: Headings should be surrounded by blank lines. [Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)
{source_path}:15:1: MD022: Headings should be surrounded by blank lines. [Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)
{source_path}:15:1: MD022: Headings should be surrounded by blank lines. [Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)"""
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

            # Assert
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )


@pytest.mark.rules
def test_md022_good_with_pragmas_blanks_before() -> None:
    """
    Test to make sure this rule works properly with pragmas.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_file_contents = """# Heading 1

<!--pyml disable-num-lines 1 md012-->

Some text
"""
    with create_temporary_configuration_file(
        source_file_contents, file_name_suffix=".md"
    ) as source_path:
        supplied_configuration = {
            "plugins": {"md022": {"lines_below": 1, "lines_above": 1}}
        }
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                "-c",
                configuration_file,
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
def test_md022_bad_with_pragmas_blanks_before() -> None:
    """
    Test to make sure this rule works properly with pragmas.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_file_contents = """# Heading 1

<!--pyml disable-num-lines 1 md012-->

Some text
"""
    with create_temporary_configuration_file(
        source_file_contents, file_name_suffix=".md"
    ) as source_path:
        supplied_configuration = {
            "plugins": {"md022": {"lines_below": 2, "lines_above": 2}}
        }
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                "-c",
                configuration_file,
                "scan",
                source_path,
            ]

            expected_return_code = 1
            expected_output = f"""{source_path}:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)"""
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

            # Assert
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )


@pytest.mark.rules
def test_md022_good_with_pragmas_blanks_around() -> None:
    """
    Test to make sure this rule works properly with pragmas.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_file_contents = """Some text

<!--pyml disable-num-lines 1 md012-->

## Heading 2

<!--pyml disable-num-lines 5 md012-->

Some more text
"""
    with create_temporary_configuration_file(
        source_file_contents, file_name_suffix=".md"
    ) as source_path:
        supplied_configuration = {
            "plugins": {"md022": {"lines_below": 1, "lines_above": 1}}
        }
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                "-c",
                configuration_file,
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
def test_md022_bad_with_pragmas_blanks_around() -> None:
    """
    Test to make sure this rule works properly with pragmas.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_file_contents = """Some text

<!--pyml disable-num-lines 1 md012-->

## Heading 2

<!--pyml disable-num-lines 5 md012-->

Some more text
"""
    with create_temporary_configuration_file(
        source_file_contents, file_name_suffix=".md"
    ) as source_path:
        supplied_configuration = {
            "plugins": {"md022": {"lines_below": 2, "lines_above": 2}}
        }
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                "-c",
                configuration_file,
                "scan",
                source_path,
            ]

            expected_return_code = 1
            expected_output = f"""{source_path}:5:1: MD022: Headings should be surrounded by blank lines. [Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)
{source_path}:5:1: MD022: Headings should be surrounded by blank lines. [Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)"""
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

            # Assert
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )


@pytest.mark.rules
def test_md022_good_with_pragmas_blanks_after() -> None:
    """
    Test to make sure this rule works properly with pragmas.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_file_contents = """<!--pyml disable-num-lines 5 md012-->

## Heading 3
"""
    with create_temporary_configuration_file(
        source_file_contents, file_name_suffix=".md"
    ) as source_path:
        supplied_configuration = {
            "plugins": {"md022": {"lines_below": 1, "lines_above": 1}}
        }
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                "-c",
                configuration_file,
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
def test_md022_bad_with_pragmas_blanks_after() -> None:
    """
    Test to make sure this rule works properly with pragmas.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_file_contents = """
<!--pyml disable-num-lines 5 md012-->

## Heading 3
"""
    with create_temporary_configuration_file(
        source_file_contents, file_name_suffix=".md"
    ) as source_path:
        supplied_configuration = {
            "plugins": {"md022": {"lines_below": 2, "lines_above": 2}}
        }
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                "-c",
                configuration_file,
                "scan",
                source_path,
            ]

            expected_return_code = 1
            expected_output = f"""{source_path}:4:1: MD022: Headings should be surrounded by blank lines. [Expected: 2; Actual: 1; Above] (blanks-around-headings,blanks-around-headers)
{source_path}:4:1: MD022: Headings should be surrounded by blank lines. [Expected: 2; Actual: 1; Below] (blanks-around-headings,blanks-around-headers)"""
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

            # Assert
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )


def test_md022_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md022",
        """
  ITEM               DESCRIPTION

  Id                 md022
  Name(s)            blanks-around-headings,blanks-around-headers
  Short Description  Headings should be surrounded by blank lines.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md022.md


  CONFIGURATION ITEM  TYPE     VALUE

  lines_above         integer  1
  lines_below         integer  1

""",
    )
    execute_query_configuration_test(config_test)
