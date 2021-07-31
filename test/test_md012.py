"""
Module to provide tests related to the MD012 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md012_bad_configuration_maximum():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md012.maximum=$#-2",
        "--strict-config",
        "scan",
        "test/resources/rules/md012/good_simple_paragraphs_single_blanks.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md012.maximum' is not valid: Allowable values are any non-negative integers."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md012_good_simple_paragraphs_single_blanks():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md010 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md012/good_simple_paragraphs_single_blanks.md",
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
def test_md012_bad_simple_paragraphs_double_blanks():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md010 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md012/good_simple_paragraphs_double_blanks.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md012/good_simple_paragraphs_double_blanks.md:3:1: "
        + "MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md012_good_simple_paragraphs_double_blanks():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md010 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md012.maximum=$#2",
        "--strict-config",
        "scan",
        "test/resources/rules/md012/good_simple_paragraphs_double_blanks.md",
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
def test_md012_good_simple_paragraphs_triple_blanks():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md010 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md012/good_simple_paragraphs_triple_blanks.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md012/good_simple_paragraphs_triple_blanks.md:4:1: "
        + "MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md012_bad_double_blanks_at_end():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md010 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md012/bad_double_blanks_at_end.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md012/bad_double_blanks_at_end.md:3:1: "
        + "MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md012_bad_multiple_blanks_in_block_quote():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md010 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md012/bad_multiple_blanks_in_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md012/bad_multiple_blanks_in_block_quote.md:3:2: "
        + "MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md012_bad_multiple_blanks_in_list():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md010 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md012/bad_multiple_blanks_in_list.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md012/bad_multiple_blanks_in_list.md:3:1: "
        + "MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md012_good_multiple_blanks_in_fenced():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md010 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md012/good_multiple_blanks_in_fenced.md",
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
def test_md012_good_multiple_blanks_in_indented():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md010 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md012/good_multiple_blanks_in_indented.md",
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
def test_md012_bad_multiple_blanks_in_html():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md010 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md012/bad_multiple_blanks_in_html.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md012/bad_multiple_blanks_in_html.md:3:1: "
        + "MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
