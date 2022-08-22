"""
Module to provide tests related to the MD027 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md027_good_block_quote_atx_heading():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with an Atx Heading with the right amount of spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_atx_heading.md"
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
def test_md027_bad_block_quote_atx_heading():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an Atx Heading with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_atx_heading.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md022,md023",
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
def test_md027_good_block_quote_setext_heading():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with an SetExt Heading with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_setext_heading.md"
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
def test_md027_bad_block_quote_setext_heading_first_line():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an SetExt Heading with extra spaces on the
    first line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_setext_heading_first_line.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
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
def test_md027_bad_block_quote_setext_heading_second_line():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an SetExt Heading with extra spaces on the
    second line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_setext_heading_second_line.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
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
def test_md027_good_block_quote_setext_heading_multiples():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with an SetExt Heading with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "good_block_quote_setext_heading_multiples.md",
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
def test_md027_bad_block_quote_setext_heading_multiples_first():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with an SetExt Heading with no spaces with
    extra space on the first line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_setext_heading_multiples_first.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
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
def test_md027_bad_block_quote_setext_heading_multiples_middle():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an SetExt Heading with no spaces with
    extra space on one of the middle lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_setext_heading_multiples_middle.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
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
def test_md027_bad_block_quote_setext_heading_multiples_last():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an SetExt Heading with no spaces with
    extra space on the last line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_setext_heading_multiples_last.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:3: "
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
def test_md027_good_block_quote_thematic():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a Thematic Break with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_thematic.md"
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
def test_md027_bad_block_quote_thematic():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a Thematic Break with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_thematic.md"
    )
    supplied_arguments = [
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
def test_md027_good_block_quote_html():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a HTML block with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_html.md"
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
def test_md027_good_block_quote_html_first():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a HTML block with extra spaces on the first line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_html_first.md"
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
def test_md027_good_block_quote_html_middle():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a HTML block with extra spaces on one
    of the middle lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_html_middle.md"
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
def test_md027_good_block_quote_html_last():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a HTML block with extra spaces on the last line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_html_last.md"
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
def test_md027_good_block_quote_fenced():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a fenced block with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_fenced.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md031",
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
def test_md027_good_block_quote_fenced_middle():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a fenced block with extra spaces in the middle.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_fenced_middle.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md031",
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
def test_md027_bad_block_quote_fenced_first():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a fenced block with extra spaces on the first line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_fenced_first.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md031",
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
def test_md027_bad_block_quote_fenced_last():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a fenced block with extra spaces on the
    last line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_fenced_last.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md031",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
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
def test_md027_good_block_quote_indented():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a indented block with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_indented.md"
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
def test_md027_good_block_quote_indented_first():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a indented block with extra spaces on
    the first line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_indented_first.md"
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
def test_md027_good_block_quote_indented_middle():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a indented block with extra spaces on
    one of the middle lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_indented_middle.md"
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
def test_md027_good_block_quote_indented_last():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a indented block with extra spaces on
    the last line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_indented_last.md"
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
def test_md027_good_block_quote_lrd():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a LRD with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_lrd.md"
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
def test_md027_good_block_quote_lrd_multiple():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a multiple line LRD with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_lrd_multiple.md"
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
def test_md027_bad_block_quote_lrd_multiple_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multiple line LRD with extra space on line 1.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_lrd_multiple_one.md"
    )
    supplied_arguments = [
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
def test_md027_good_block_quote_lrd_multiple_two():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a multiple line LRD with extra space on line 2.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_lrd_multiple_two.md"
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
def test_md027_bad_block_quote_lrd_multiple_three():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multiple line LRD with extra space on line 3.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_lrd_multiple_three.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:3: "
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
def test_md027_bad_block_quote_lrd_multiple_four():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multiple line LRD with extra space on line 4.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_lrd_multiple_four.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:6:3: "
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
def test_md027_good_block_quote_lrd_multiple_five():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a multiple line LRD with extra space on line 5.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_lrd_multiple_five.md"
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
def test_md027_bad_block_quote_link_multiple_extra():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multiple line link with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_link_multiple_extra.md"
    )
    supplied_arguments = [
        "--stack-trace",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:4:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:6:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:7:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
