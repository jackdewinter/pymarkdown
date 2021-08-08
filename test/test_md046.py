"""
Module to provide tests related to the MD045 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md046_bad_configuration_style():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md046.style=$#1",
        "--strict-config",
        "scan",
        "test/resources/rules/md046/good_both_fenced.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md046.style' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md046_bad_configuration_style_bad():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md046.style=not-matching",
        "--strict-config",
        "scan",
        "test/resources/rules/md046/good_both_fenced.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md046.style' is not valid: Allowable values: ['consistent', 'fenced', 'indented']"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md046_good_both_fenced_with_consistent():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md046.style=consistent",
        "scan",
        "test/resources/rules/md046/good_both_fenced.md",
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
def test_md046_good_both_indented_with_consistent():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md046.style=consistent",
        "scan",
        "test/resources/rules/md046/good_both_indented.md",
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
def test_md046_bad_fenced_and_indented_with_consistent():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md046.style=consistent",
        "scan",
        "test/resources/rules/md046/bad_fenced_and_indented.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md046/bad_fenced_and_indented.md:5:5: "
        + "MD046: Code block style "
        + "[Expected: fenced; Actual: indented] (code-block-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md046_good_both_fenced_with_fenced():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md046.style=fenced",
        "scan",
        "test/resources/rules/md046/good_both_fenced.md",
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
def test_md046_good_both_indented_with_fenced():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md046.style=fenced",
        "scan",
        "test/resources/rules/md046/good_both_indented.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md046/good_both_indented.md:1:5: "
        + "MD046: Code block style "
        + "[Expected: fenced; Actual: indented] (code-block-style)\n"
        + "test/resources/rules/md046/good_both_indented.md:5:5: "
        + "MD046: Code block style "
        + "[Expected: fenced; Actual: indented] (code-block-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md046_bad_fenced_and_indented_with_fenced():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md046.style=fenced",
        "scan",
        "test/resources/rules/md046/bad_fenced_and_indented.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md046/bad_fenced_and_indented.md:5:5: "
        + "MD046: Code block style "
        + "[Expected: fenced; Actual: indented] (code-block-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md046_good_both_fenced_with_indented():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md046.style=indented",
        "scan",
        "test/resources/rules/md046/good_both_fenced.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md046/good_both_fenced.md:1:1: "
        + "MD046: Code block style "
        + "[Expected: indented; Actual: fenced] (code-block-style)\n"
        + "test/resources/rules/md046/good_both_fenced.md:5:1: "
        + "MD046: Code block style "
        + "[Expected: indented; Actual: fenced] (code-block-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md046_good_both_indented_with_indented():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md046.style=indented",
        "scan",
        "test/resources/rules/md046/good_both_indented.md",
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
def test_md046_bad_fenced_and_indented_with_indented():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md046.style=indented",
        "scan",
        "test/resources/rules/md046/bad_fenced_and_indented.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md046/bad_fenced_and_indented.md:1:1: "
        + "MD046: Code block style "
        + "[Expected: indented; Actual: fenced] (code-block-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
