"""
Module to provide tests related to the MD027 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md027_bad_block_quote_atx_heading_plus_one():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md022,md023",
        "scan",
        "test/resources/rules/md027/bad_block_quote_atx_heading_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_atx_heading_plus_one.md:2:4: "
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
def test_md027_bad_block_quote_atx_heading_misaligned():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md022,md023",
        "scan",
        "test/resources/rules/md027/bad_block_quote_atx_heading_misaligned.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_atx_heading_misaligned.md:2:3: "
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
def test_md027_bad_block_quote_fenced_first_plus_one():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md031",
        "scan",
        "test/resources/rules/md027/bad_block_quote_fenced_first_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_fenced_first_plus_one.md:2:4: "
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
def test_md027_bad_block_quote_fenced_last_plus_one():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md031",
        "scan",
        "test/resources/rules/md027/bad_block_quote_fenced_last_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_fenced_last_plus_one.md:4:4: "
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
def test_md027_bad_block_quote_fenced_last_misaligned():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md031",
        "scan",
        "test/resources/rules/md027/bad_block_quote_fenced_last_misaligned.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_fenced_last_misaligned.md:4:3: "
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
def test_md027_bad_block_quote_lrd_multiple_one_plus_one():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_lrd_multiple_one_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_lrd_multiple_one_plus_one.md:3:4: "
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
def test_md027_bad_block_quote_lrd_multiple_three_plus_one():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_lrd_multiple_three_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_lrd_multiple_three_plus_one.md:5:4: "
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
def test_md027_bad_block_quote_lrd_multiple_three_misaligned():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_lrd_multiple_three_misaligned.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_lrd_multiple_three_misaligned.md:5:3: "
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
def test_md027_bad_block_quote_lrd_multiple_four_plus_one():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_lrd_multiple_four_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_lrd_multiple_four_plus_one.md:6:4: "
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
def test_md027_bad_block_quote_lrd_multiple_four_misaligned():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_lrd_multiple_four_misaligned.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_lrd_multiple_four_misaligned.md:6:3: "
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
def test_md027_bad_block_quote_thematic_plus_one():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md027/bad_block_quote_thematic_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_thematic_plus_one.md:3:4: "
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
def test_md027_bad_block_quote_setext_heading_first_line_plus_one():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        "test/resources/rules/md027/bad_block_quote_setext_heading_first_line_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_setext_heading_first_line_plus_one.md:3:4: "
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
def test_md027_bad_block_quote_setext_heading_multiples_first_plus_one():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        "test/resources/rules/md027/bad_block_quote_setext_heading_multiples_first_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_setext_heading_multiples_first_plus_one.md:3:4: "
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
def test_md027_bad_block_quote_setext_heading_multiples_middle_plus_one():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        "test/resources/rules/md027/bad_block_quote_setext_heading_multiples_middle_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_setext_heading_multiples_middle_plus_one.md:4:4: "
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
def test_md027_bad_block_quote_setext_heading_multiples_middle_misaligned():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        "test/resources/rules/md027/bad_block_quote_setext_heading_multiples_middle_misaligned.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_setext_heading_multiples_middle_misaligned.md:4:3: "
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
def test_md027_bad_block_quote_setext_heading_multiples_last_plus_one():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        "test/resources/rules/md027/bad_block_quote_setext_heading_multiples_last_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_setext_heading_multiples_last_plus_one.md:5:4: "
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
def test_md027_bad_block_quote_setext_heading_multiples_last_misaligned():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        "test/resources/rules/md027/bad_block_quote_setext_heading_multiples_last_misaligned.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_setext_heading_multiples_last_misaligned.md:5:3: "
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
def test_md027_bad_block_quote_setext_heading_second_line_plus_one():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        "test/resources/rules/md027/bad_block_quote_setext_heading_second_line_plus_one.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_setext_heading_second_line_plus_one.md:4:4: "
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
def test_md027_bad_block_quote_setext_heading_second_line_misaligned():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        "test/resources/rules/md027/bad_block_quote_setext_heading_second_line_misaligned.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md027/bad_block_quote_setext_heading_second_line_misaligned.md:4:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
