"""
Module to provide tests related to the MD045 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md048_bad_configuration_style():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md048.style=$#1",
        "--strict-config",
        "scan",
        "test/resources/rules/md048/good_both_tildes.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md048.style' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md048_bad_configuration_style_bad():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md048.style=not-matching",
        "--strict-config",
        "scan",
        "test/resources/rules/md048/good_both_tildes.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md048.style' is not valid: Allowable values: ['consistent', 'tilde', 'backtick']"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md048_good_fenced_tildes_with_consistent():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md048.style=consistent",
        "scan",
        "test/resources/rules/md048/good_fenced_tildes.md",
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
def test_md048_good_fenced_backticks_with_consistent():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md048.style=consistent",
        "scan",
        "test/resources/rules/md048/good_fenced_backticks.md",
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
def test_md048_bad_fenced_backticks_and_tildes_with_consistent():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md048.style=consistent",
        "scan",
        "test/resources/rules/md048/bad_fenced_backticks_and_tildes.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md048/bad_fenced_backticks_and_tildes.md:6:1: "
        + "MD048: Code fence style "
        + "[Expected: backtick; Actual: tilde] (code-fence-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md048_good_fenced_backticks_with_backticks():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md048.style=backtick",
        "scan",
        "test/resources/rules/md048/good_fenced_backticks.md",
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
def test_md048_good_fenced_tildes_with_backticks():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md048.style=backtick",
        "scan",
        "test/resources/rules/md048/good_fenced_tildes.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md048/good_fenced_tildes.md:1:1: "
        + "MD048: Code fence style "
        + "[Expected: backtick; Actual: tilde] (code-fence-style)\n"
        + "test/resources/rules/md048/good_fenced_tildes.md:6:1: "
        + "MD048: Code fence style "
        + "[Expected: backtick; Actual: tilde] (code-fence-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md048_bad_fenced_backticks_and_tildes_with_backticks():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md048.style=backtick",
        "scan",
        "test/resources/rules/md048/bad_fenced_backticks_and_tildes.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md048/bad_fenced_backticks_and_tildes.md:6:1: "
        + "MD048: Code fence style "
        + "[Expected: backtick; Actual: tilde] (code-fence-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md048_good_fenced_tildes_with_tilde():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md048.style=tilde",
        "scan",
        "test/resources/rules/md048/good_fenced_tildes.md",
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
def test_md048_good_fenced_backticks_with_tilde():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md048.style=tilde",
        "scan",
        "test/resources/rules/md048/good_fenced_backticks.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md048/good_fenced_backticks.md:1:1: "
        + "MD048: Code fence style "
        + "[Expected: tilde; Actual: backtick] (code-fence-style)\n"
        + "test/resources/rules/md048/good_fenced_backticks.md:6:1: "
        + "MD048: Code fence style "
        + "[Expected: tilde; Actual: backtick] (code-fence-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md048_bad_fenced_backticks_and_tildes_with_indented():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md048.style=tilde",
        "scan",
        "test/resources/rules/md048/bad_fenced_backticks_and_tildes.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md048/bad_fenced_backticks_and_tildes.md:1:1: "
        + "MD048: Code fence style "
        + "[Expected: tilde; Actual: backtick] (code-fence-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
