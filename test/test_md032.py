"""
Module to provide tests related to the MD032 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md032_good_list_surrounded():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md032/good_list_surrounded.md",
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
def test_md032_good_list_at_start():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md032/good_list_at_start.md",
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
def test_md032_good_list_at_end():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md047",
        "scan",
        "test/resources/rules/md032/good_list_at_end.md",
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
def test_md032_bad_list_before():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md032/bad_list_before.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md032/bad_list_before.md:2:1: "
        + "MD032: Lists should be surrounded by blank lines (blanks-around-lists)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md032_bad_list_after():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md022",
        "scan",
        "test/resources/rules/md032/bad_list_after.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md032/bad_list_after.md:3:1: "
        + "MD032: Lists should be surrounded by blank lines (blanks-around-lists)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md032_bad_block_quote_list_block_quote():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md032/bad_block_quote_list_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md032/bad_block_quote_list_block_quote.md:2:1: "
        + "MD032: Lists should be surrounded by blank lines (blanks-around-lists)\n"
        + "test/resources/rules/md032/bad_block_quote_list_block_quote.md:3:1: "
        + "MD032: Lists should be surrounded by blank lines (blanks-around-lists)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md032_bad_other_list_list_other_list():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md032/bad_other_list_list_other_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md032/bad_other_list_list_other_list.md:1:1: "
        + "MD032: Lists should be surrounded by blank lines (blanks-around-lists)\n"
        + "test/resources/rules/md032/bad_other_list_list_other_list.md:2:1: "
        + "MD032: Lists should be surrounded by blank lines (blanks-around-lists)\n"
        + "test/resources/rules/md032/bad_other_list_list_other_list.md:3:1: "
        + "MD032: Lists should be surrounded by blank lines (blanks-around-lists)\n"
        + "test/resources/rules/md032/bad_other_list_list_other_list.md:4:1: "
        + "MD032: Lists should be surrounded by blank lines (blanks-around-lists)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md032_good_list_within_list_surrounded():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md032/good_list_within_list_surrounded.md",
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
def test_md032_bad_list_within_block_quote_surrounded():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md032/bad_list_within_block_quote_surrounded.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md032/bad_list_within_block_quote_surrounded.md:4:3: "
        + "MD032: Lists should be surrounded by blank lines (blanks-around-lists)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md032_good_nested_lists():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md032/good_nested_lists.md",
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
def test_md032_good_list_levels_1_2_3_2_1():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024,md025",
        "scan",
        "test/resources/rules/md032/good_list_levels_1_2_3_2_1.md",
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
def test_md032_good_list_levels_1_2_3_space_1():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024,md025",
        "scan",
        "test/resources/rules/md032/good_list_levels_1_2_3_space_1.md",
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
def test_md032_good_list_levels_1_2_3_1():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024,md025",
        "scan",
        "test/resources/rules/md032/good_list_levels_1_2_3_1.md",
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
def test_md032_bad_fenced_block_in_list_in_block_quote():
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
        "test/resources/rules/md031/bad_fenced_block_in_list_in_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md031/bad_fenced_block_in_list_in_block_quote.md:1:3: "
        + "MD032: Lists should be surrounded by blank lines (blanks-around-lists)\n"
        + "test/resources/rules/md031/bad_fenced_block_in_list_in_block_quote.md:5:3: "
        + "MD032: Lists should be surrounded by blank lines (blanks-around-lists)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
