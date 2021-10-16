"""
Module to provide tests related to the MD027 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md027_good_block_quote_code_span():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a single line code span with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_block_quote_code_span.md",
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
def test_md027_bad_block_quote_code_span_multiple():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multiple line code span with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_code_span_multiple.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_code_span_multiple.md:3:3: "
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
def test_md027_bad_block_quote_code_span_multiple_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multiple line code span with extra spaces,
    and the block quote indented.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_code_span_multiple_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_code_span_multiple_plus_one.md:3:4: "
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
def test_md027_bad_block_quote_code_span_multiple_misaligned():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multiple line code span with extra spaces,
    where the block quotes are misaligned.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_code_span_multiple_misaligned.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_code_span_multiple_misaligned.md:3:3: "
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
def test_md027_good_block_quote_emphasis():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a emphasis with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_block_quote_emphasis.md",
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
def test_md027_good_block_quote_emphasis_multiple():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multi line emphasis with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_block_quote_emphasis_multiple.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/good_block_quote_emphasis_multiple.md:2:3: "
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
def test_md027_good_block_quote_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with an inline link with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_block_quote_link.md",
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
def test_md027_bad_block_quote_link():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an inline link with extra spaces on each line.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_link.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_link.md:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + "test/resources/rules/md027/bad_block_quote_link.md:3:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + "test/resources/rules/md027/bad_block_quote_link.md:4:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + "test/resources/rules/md027/bad_block_quote_link.md:5:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + "test/resources/rules/md027/bad_block_quote_link.md:6:3: "
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
def test_md027_good_block_quote_link_multiple():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an inline link with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_block_quote_link_multiple.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/good_block_quote_link_multiple.md:3:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + "test/resources/rules/md027/good_block_quote_link_multiple.md:5:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + "test/resources/rules/md027/good_block_quote_link_multiple.md:6:3: "
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
def test_md027_good_block_quote_raw_html():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with an inline rawhtml with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_block_quote_raw_html.md",
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
def test_md027_bad_block_quote_raw_html_multiple():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multiline inline rawhtml with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_raw_html_multiple.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_raw_html_multiple.md:3:3: "
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
def test_md027_good_block_quote_autolink():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with an inline autolink with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/good_block_quote_autolink.md",
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
def test_md027_bad_block_quote_autolink():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an inline autolink with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_autolink.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_autolink.md:2:3: "
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
def test_md027_bad_block_quote_autolink_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an inline autolink with extra spaces,
    with the block quote indented.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_autolink_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_autolink_plus_one.md:2:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
