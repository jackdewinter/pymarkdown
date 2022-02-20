"""
Module to provide tests related to the MD025 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md025_bad_configuration_level():
    """
    Test to verify that a configuration error is thrown when supplying the
    level value with a string that is not an integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md025.level=1",
        "--strict-config",
        "scan",
        "test/resources/rules/md025/good_single_top_level.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md025.level' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_good_configuration_level():
    """
    Test to verify that a configuration error is not thrown when supplying the
    level value with an integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md025.level=$#1",
        "--strict-config",
        "scan",
        "test/resources/rules/md025/good_single_top_level_atx.md",
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
def test_md025_bad_configuration_level_bad():
    """
    Test to verify that a configuration error is thrown when supplying the
    level value an integer that is out of range.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md025.level=$#0",
        "--strict-config",
        "scan",
        "test/resources/rules/md025/good_single_top_level.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md025.level' is not valid: Allowable values are between 1 and 6."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_bad_configuration_front_matter_title():
    """
    Test to verify that a configuration error is thrown when supplying the
    front_matter_title value with an integer that is not a string.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md025.front_matter_title=$#1",
        "--strict-config",
        "scan",
        "test/resources/rules/md025/good_single_top_level.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md025.front_matter_title' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_good_configuration_front_matter_title():
    """
    Test to verify that a configuration error is not thrown when supplying the
    front_matter_title value with a valid string.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md025.front_matter_title=subject",
        "--strict-config",
        "scan",
        "test/resources/rules/md025/good_single_top_level_atx.md",
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
def test_md025_bad_configuration_front_matter_title_bad():
    """
    Test to verify that a configuration error is thrown when supplying the
    front_matter_title value with an invalid string.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md025.front_matter_title=",
        "--strict-config",
        "scan",
        "test/resources/rules/md025/good_single_top_level.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md025.front_matter_title' is not valid: Empty strings are not allowable values."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_bad_configuration_front_matter_title_invalid():
    """
    Test to verify that a configuration error is thrown when supplying the
    front_matter_title value with an invalid string.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md025.front_matter_title=a:b",
        "--strict-config",
        "scan",
        "test/resources/rules/md025/good_single_top_level.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md025.front_matter_title' is not valid: Colons (:) are not allowed in the value."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_good_single_top_level_atx():
    """
    Test to make sure this rule does not trigger with a document that
    contains a single top level Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md025/good_single_top_level_atx.md",
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
def test_md025_good_single_top_level_setext():
    """
    Test to make sure this rule does not trigger with a document that
    contains a single top level SetExt Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md025/good_single_top_level_setext.md",
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
def test_md025_bad_top_level_atx_top_level_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains two top level Atx Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md025/bad_top_level_atx_top_level_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md025/bad_top_level_atx_top_level_atx.md:5:1: "
        + "MD025: Multiple top-level headings in the same document (single-title,single-h1)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_bad_top_level_atx_top_level_setext():
    """
    Test to make sure this rule does trigger with a document that
    contains a top level Atx Heading and a top level SetExt Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md003",
        "scan",
        "test/resources/rules/md025/bad_top_level_atx_top_level_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md025/bad_top_level_atx_top_level_setext.md:6:1: "
        + "MD025: Multiple top-level headings in the same document (single-title,single-h1)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_bad_top_level_setext_top_level_setext():
    """
    Test to make sure this rule does trigger with a document that
    contains two top level SetExt Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md025/bad_top_level_setext_top_level_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md025/bad_top_level_setext_top_level_setext.md:7:1: "
        + "MD025: Multiple top-level headings in the same document (single-title,single-h1)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_bad_top_level_setext_top_level_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains a top level SetExt Heading and an top level Atx heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md003",
        "scan",
        "test/resources/rules/md025/bad_top_level_setext_top_level_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md025/bad_top_level_setext_top_level_atx.md:6:1: "
        + "MD025: Multiple top-level headings in the same document (single-title,single-h1)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_good_front_matter_title():
    """
    Test to make sure this rule does not trigger with a document that
    contains only a front-matter title.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
        "scan",
        "test/resources/rules/md025/good_front_matter_title.md",
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
def test_md025_bad_front_matter_title_top_level_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains a front-matter title and a top level Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
        "scan",
        "test/resources/rules/md025/bad_front_matter_title_top_level_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md025/bad_front_matter_title_top_level_atx.md:7:1: "
        + "MD025: Multiple top-level headings in the same document (single-title,single-h1)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md025_bad_front_matter_title_top_level_setext():
    """
    Test to make sure this rule does trigger with a document that
    contains a front-matter title and a top level SetExt Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
        "scan",
        "test/resources/rules/md025/bad_front_matter_title_top_level_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md025/bad_front_matter_title_top_level_setext.md:8:1: "
        + "MD025: Multiple top-level headings in the same document (single-title,single-h1)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
