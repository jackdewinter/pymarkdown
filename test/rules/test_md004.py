"""
Module to provide tests related to the MD004 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md004_bad_configuration_style():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with a string that is not in the list of acceptable values.
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
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with asterisk and the
    configuration is set to asterisk.
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
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with asterisk and the
    configuration is set to consistent.
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
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
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
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with plus and the
    configuration is also set to asterisk.
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
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to dash.
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
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to consistent.
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
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with asterisks and the
    configuration is also set to dash.
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
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with plus and the
    configuration is also set to dash.
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
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with plus and the
    configuration is also set to plus.
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
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to consistent.
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
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with asterisk and the
    configuration is also set to plus.
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
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to plus.
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
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with each of the valid starts.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md032",
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
    Test to make sure this rule does not trigger with a document that contains
    the three start characters, each on their own sublevel.
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
    Variation of the previous test with a more complex list structure.
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
    Test to make sure this rule does trigger with a document that contains
    the inconsistent start characters at one specific sublevel.
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
    Test to make sure this rule does trigger with a document that contains
    the three start characters, each on their own sublevel, and configuration
    specifically set to asterisk.
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
    Test to make sure this rule does trigger with a document that contains
    two separate lists with different start characters, and configuration
    specifically set to sublist.
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
