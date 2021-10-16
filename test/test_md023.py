"""
Module to provide tests related to the MD023 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md023_good_proper_indent_atx():
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx heading that starts at the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        "test/resources/rules/md023/proper_indent_atx.md",
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
def test_md023_good_proper_indent_setext():
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that starts at the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        "test/resources/rules/md023/proper_indent_setext.md",
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
def test_md023_bad_improper_indent_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading that does not start at the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        "test/resources/rules/md023/improper_indent_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md023/improper_indent_atx.md:3:3: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indent_atx_in_list_item():
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx heading that does not start at the very left in a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        "test/resources/rules/md023/improper_indent_atx_in_list_item.md",
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
def test_md023_bad_improper_indent_atx_in_block_quote():
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx heading that does not start at the very left in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        "test/resources/rules/md023/improper_indent_atx_in_block_quote.md",
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
def test_md023_bad_improper_indent_setext_x():
    """
    Test to make sure this rule does trigger with a document that
    contains a SetExt heading that any part of it does not start at
    the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        "test/resources/rules/md023/improper_indent_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md023/improper_indent_setext.md:4:3: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext.md:9:3: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext.md:14:1: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext.md:22:1: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indent_setext_in_block_quote():
    """
    Test to make sure this rule does trigger with a document that
    contains a SetExt heading that any part of it does not start at
    the very left in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "--disable-rules",
        "MD027,md022",
        "scan",
        "test/resources/rules/md023/improper_indent_setext_in_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md023/improper_indent_setext_in_block_quote.md:4:5: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext_in_block_quote.md:9:5: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext_in_block_quote.md:14:3: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext_in_block_quote.md:22:3: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indent_setext_in_list_item():
    """
    Test to make sure this rule does trigger with a document that
    contains a SetExt heading that any part of it does not start at
    the very left in a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "--disable-rules",
        "MD005,md030",
        "scan",
        "test/resources/rules/md023/improper_indent_setext_in_list_item.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md023/improper_indent_setext_in_list_item.md:4:5: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext_in_list_item.md:9:6: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + "test/resources/rules/md023/improper_indent_setext_in_list_item.md:22:3: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indented_atx_after_emphasis():
    """
    Test to make sure this rule does not trigger with a document that
    contains a "SetExt heading" that is encapsulated in emphasis.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        "test/resources/rules/md023/improper_indented_atx_after_emphasis.md",
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
def test_md023_proper_indent_setext_trailing_x():
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that ends with spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "MD009",
        "--enable-rules",
        "MD023",
        "scan",
        "test/resources/rules/md023/proper_indent_setext_trailing.md",
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
def test_md023_proper_indent_setext_trailing_first():
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that ends with spaces on the first line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "--disable-rules",
        "MD009",
        "scan",
        "test/resources/rules/md023/proper_indent_setext_trailing_first.md",
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
def test_md023_proper_indent_setext_trailing_second():
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that ends with spaces on the second line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "--disable-rules",
        "MD009",
        "scan",
        "test/resources/rules/md023/proper_indent_setext_trailing_second.md",
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
def test_md023_proper_indent_setext_trailing_third():
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that ends with spaces on the third line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "--disable-rules",
        "MD009",
        "scan",
        "test/resources/rules/md023/proper_indent_setext_trailing_third.md",
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
def test_md023_proper_indent_setext_larger_trailing_middle():
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that ends with spaces in the middle.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "--disable-rules",
        "MD009",
        "scan",
        "test/resources/rules/md023/proper_indent_setext_larger_trailing_middle.md",
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
