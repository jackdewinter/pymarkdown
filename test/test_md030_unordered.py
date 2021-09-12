"""
Module to provide tests related to the MD030 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md030_bad_configuration_ul_single():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=not-integer",
        "--strict-config",
        "scan",
        "test/resources/rules/md030/good_one_list.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md030.ul_single' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_configuration_ul_single_zero():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#0",
        "--strict-config",
        "scan",
        "test/resources/rules/md030/good_one_list.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md030.ul_single' is not valid: Allowable values are any integer greater than 0."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_configuration_ul_multi():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_multi=not-integer",
        "--strict-config",
        "scan",
        "test/resources/rules/md030/good_one_list.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md030.ul_multi' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_configuration_ul_multi_zero():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_multi=$#0",
        "--strict-config",
        "scan",
        "test/resources/rules/md030/good_one_list.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md030.ul_multi' is not valid: Allowable values are any integer greater than 0."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_good_spacing_ul_single():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md030/good_spacing_ul_single.md",
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
def test_md030_good_spacing_ul_single_with_config_1_2():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#1",
        "--set",
        "plugins.md030.ul_multi=$#2",
        "--strict-config",
        "scan",
        "test/resources/rules/md030/good_spacing_ul_single.md",
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
def test_md030_good_spacing_ul_single_with_config_2_1():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#2",
        "--set",
        "plugins.md030.ul_multi=$#1",
        "--strict-config",
        "scan",
        "test/resources/rules/md030/good_spacing_ul_single.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md030/good_spacing_ul_single.md:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)\n"
        + "test/resources/rules/md030/good_spacing_ul_single.md:2:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)\n"
        + "test/resources/rules/md030/good_spacing_ul_single.md:3:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_single():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "test/resources/rules/md030/bad_spacing_ul_single.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md030/bad_spacing_ul_single.md:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + "test/resources/rules/md030/bad_spacing_ul_single.md:2:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + "test/resources/rules/md030/bad_spacing_ul_single.md:3:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_single_config_1_2():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#1",
        "--set",
        "plugins.md030.ul_multi=$#2",
        "--strict-config",
        "--stack-trace",
        "scan",
        "test/resources/rules/md030/bad_spacing_ul_single.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md030/bad_spacing_ul_single.md:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + "test/resources/rules/md030/bad_spacing_ul_single.md:2:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + "test/resources/rules/md030/bad_spacing_ul_single.md:3:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_single_config_2_1():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#2",
        "--set",
        "plugins.md030.ul_multi=$#1",
        "--strict-config",
        "--stack-trace",
        "scan",
        "test/resources/rules/md030/bad_spacing_ul_single.md",
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
def test_md030_good_spacing_ul_double():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md030/good_spacing_ul_double.md",
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
def test_md030_good_spacing_ul_double_config_1_2():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#1",
        "--set",
        "plugins.md030.ul_multi=$#2",
        "--strict-config",
        "scan",
        "test/resources/rules/md030/good_spacing_ul_double.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md030/good_spacing_ul_double.md:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)\n"
        + "test/resources/rules/md030/good_spacing_ul_double.md:2:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)\n"
        + "test/resources/rules/md030/good_spacing_ul_double.md:4:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_good_spacing_ul_double_config_2_1():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#2",
        "--set",
        "plugins.md030.ul_multi=$#1",
        "--strict-config",
        "scan",
        "test/resources/rules/md030/good_spacing_ul_double.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md030/good_spacing_ul_double.md:3:3: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_double():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md005,md007",
        "--stack-trace",
        "scan",
        "test/resources/rules/md030/bad_spacing_ul_double.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md030/bad_spacing_ul_double.md:3:4: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + "test/resources/rules/md030/bad_spacing_ul_double.md:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + "test/resources/rules/md030/bad_spacing_ul_double.md:2:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + "test/resources/rules/md030/bad_spacing_ul_double.md:4:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_double_config_1_2():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md005,md007",
        "--set",
        "plugins.md030.ul_single=$#1",
        "--set",
        "plugins.md030.ul_multi=$#2",
        "--stack-trace",
        "scan",
        "test/resources/rules/md030/bad_spacing_ul_double.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md030/bad_spacing_ul_double.md:3:4: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_double_config_2_1():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md005,md007",
        "--set",
        "plugins.md030.ul_single=$#2",
        "--set",
        "plugins.md030.ul_multi=$#1",
        "--stack-trace",
        "scan",
        "test/resources/rules/md030/bad_spacing_ul_double.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md030/bad_spacing_ul_double.md:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + "test/resources/rules/md030/bad_spacing_ul_double.md:2:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + "test/resources/rules/md030/bad_spacing_ul_double.md:4:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
