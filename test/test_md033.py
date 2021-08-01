"""
Module to provide tests related to the MD026 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md033_bad_configuration_style():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md033.allowed_elements=$#1",
        "--strict-config",
        "scan",
        "test/resources/rules/md004/good_list_asterisk_single_level.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md033.allowed_elements' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_html_block_present():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md033/bad_html_block_present.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md033/bad_html_block_present.md:3:1: "
        + "MD033: Inline HTML [Element: script] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:12:1: "
        + "MD033: Inline HTML [Element: ?] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:16:1: "
        + "MD033: Inline HTML [Element: !A] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:20:1: "
        + "MD033: Inline HTML [Element: ![CDATA[] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:24:1: "
        + "MD033: Inline HTML [Element: p] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:28:1: "
        + "MD033: Inline HTML [Element: robert] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:31:1: "
        + "MD033: Inline HTML [Element: robert] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:34:1: "
        + "MD033: Inline HTML [Element: robert] (no-inline-html)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_html_block_present_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md033.allowed_elements=",
        "scan",
        "test/resources/rules/md033/bad_html_block_present.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md033/bad_html_block_present.md:3:1: "
        + "MD033: Inline HTML [Element: script] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:7:1: "
        + "MD033: Inline HTML [Element: !--] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:12:1: "
        + "MD033: Inline HTML [Element: ?] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:16:1: "
        + "MD033: Inline HTML [Element: !A] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:20:1: "
        + "MD033: Inline HTML [Element: ![CDATA[] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:24:1: "
        + "MD033: Inline HTML [Element: p] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:28:1: "
        + "MD033: Inline HTML [Element: robert] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:31:1: "
        + "MD033: Inline HTML [Element: robert] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:34:1: "
        + "MD033: Inline HTML [Element: robert] (no-inline-html)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_html_block_present_with_other_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md033.allowed_elements=robert,p,!A",
        "scan",
        "test/resources/rules/md033/bad_html_block_present.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md033/bad_html_block_present.md:3:1: "
        + "MD033: Inline HTML [Element: script] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:7:1: "
        + "MD033: Inline HTML [Element: !--] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:12:1: "
        + "MD033: Inline HTML [Element: ?] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_html_block_present.md:20:1: "
        + "MD033: Inline HTML [Element: ![CDATA[] (no-inline-html)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md033_bad_inline_html_present():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "test/resources/rules/md033/bad_inline_html_present.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md033/bad_inline_html_present.md:3:9: "
        + "MD033: Inline HTML [Element: a] (no-inline-html)\n"
        + "test/resources/rules/md033/bad_inline_html_present.md:5:17: "
        + "MD033: Inline HTML [Element: ![CDATA[] (no-inline-html)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
