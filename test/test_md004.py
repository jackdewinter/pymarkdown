"""
Module to provide tests related to the MD004 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md004_bad_configuration_style():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=bad",
        "--strict-config",
        "scan",
        "test/resources/rules/md004/good_list_asterisk_single_level.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md004.style' is not valid: Allowable values: ['consistent', 'asterisk', 'plus', 'dash', 'sublist']"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_good_asterisk_single_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=asterisk",
        "scan",
        "test/resources/rules/md004/good_list_asterisk_single_level.md",
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
def test_md004_good_asterisk_single_level_consistent():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md004/good_list_asterisk_single_level.md",
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
def test_md004_bad_asterisk_dash_single_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=asterisk",
        "scan",
        "test/resources/rules/md004/good_list_dash_single_level.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md004/good_list_dash_single_level.md:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: dash] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_asterisk_plus_single_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=asterisk",
        "scan",
        "test/resources/rules/md004/good_list_plus_single_level.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md004/good_list_plus_single_level.md:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: plus] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_good_dash_single_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=dash",
        "scan",
        "test/resources/rules/md004/good_list_dash_single_level.md",
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
def test_md004_good_dash_single_level_consistent():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md004/good_list_dash_single_level.md",
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
def test_md004_bad_dash_asterisk_single_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=dash",
        "scan",
        "test/resources/rules/md004/good_list_asterisk_single_level.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md004/good_list_asterisk_single_level.md:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: dash; Actual: asterisk] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_dash_plus_single_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=dash",
        "scan",
        "test/resources/rules/md004/good_list_plus_single_level.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md004/good_list_plus_single_level.md:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: dash; Actual: plus] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_good_plus_single_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=plus",
        "scan",
        "test/resources/rules/md004/good_list_plus_single_level.md",
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
def test_md004_good_plus_single_level_consistent():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md004/good_list_plus_single_level.md",
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
def test_md004_bad_plus_asterisk_single_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=plus",
        "scan",
        "test/resources/rules/md004/good_list_asterisk_single_level.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md004/good_list_asterisk_single_level.md:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: plus; Actual: asterisk] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_plus_dash_single_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=plus",
        "scan",
        "test/resources/rules/md004/good_list_dash_single_level.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md004/good_list_dash_single_level.md:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: plus; Actual: dash] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_single_level_consistent():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has inconsistent usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md004/bad_list_different_single_level.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md004/bad_list_different_single_level.md:2:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: plus] (ul-style)\n"
        + "test/resources/rules/md004/bad_list_different_single_level.md:3:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: dash] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_good_multi_level_sublevel():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent usage on multiple levels of list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=sublist",
        "scan",
        "test/resources/rules/md004/good_multi_level_sublevel.md",
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
def test_md004_good_multi_level_sublevel_complex():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent usage on multiple levels of list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=sublist",
        "scan",
        "test/resources/rules/md004/good_multi_level_complex.md",
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
def test_md004_bad_multi_level_sublevel_complex():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent usage on multiple levels of list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=sublist",
        "scan",
        "test/resources/rules/md004/bad_multi_level_complex.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md004/bad_multi_level_complex.md:6:6: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: dash; Actual: plus] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_multi_level_sublevel_complex_asterisk():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent usage on multiple levels of list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=asterisk",
        "scan",
        "test/resources/rules/md004/bad_multi_level_complex.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md004/bad_multi_level_complex.md:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: plus] (ul-style)\n"
        + "test/resources/rules/md004/bad_multi_level_complex.md:3:6: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: dash] (ul-style)\n"
        + "test/resources/rules/md004/bad_multi_level_complex.md:6:6: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: plus] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_dual_lists_with_separator():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent usage on multiple levels of list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md004.style=sublist",
        "scan",
        "test/resources/rules/md004/bad_dual_lists_with_separator.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md004/bad_dual_lists_with_separator.md:6:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: plus; Actual: asterisk] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
