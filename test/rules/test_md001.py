"""
Module to provide tests related to the MD001 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md001_all_samples():
    """
    Test to make sure we get the expected behavior after scanning all the files in the
    test/resources/rules/md001 directory.  Note that with three front-matter files in
    this directory and no config to enable that extension, Md022 will report bad
    heading formats.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "MD003",
        "scan",
        "test/resources/rules/md001",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md001/front_matter_with_alternate_title.md:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md001/front_matter_with_no_title.md:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md001/front_matter_with_title.md:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md001/improper_atx_heading_incrementing.md:3:1: "
        + "MD001: Heading levels should only increment by one level at a time. "
        + "[Expected: h2; Actual: h3] (heading-increment,header-increment)\n"
        + "test/resources/rules/md001/improper_setext_heading_incrementing.md:4:1: "
        + "MD001: Heading levels should only increment by one level at a time. "
        + "[Expected: h3; Actual: h4] (heading-increment,header-increment)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md001_bad_configuration_enabled():
    """
    Test to verify that enabling front matter with text "True" fails.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--strict-config",
        "--set",
        "extensions.front-matter.enabled=True",
        "scan",
        "test/resources/rules/md001/front_matter_with_title.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """Configuration error ValueError encountered while initializing extensions:
The value for property 'extensions.front-matter.enabled' must be of type 'bool'."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md001_bad_configuration_front_matter_title():
    """
    Test to verify that enabling front matter title with number "1" fails.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--strict-config",
        "--set",
        "extensions.front-matter.enabled=$!True",
        "--set",
        "plugins.md001.front_matter_title=$#1",
        "scan",
        "test/resources/rules/md001/proper_atx_heading_incrementing.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md001.front_matter_title' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md001_good_proper_atx_heading_incrementing():
    """
    Test to make sure the rule doesn't trigger with a document with
    only Atx Headings, that when they increase, only increase by 1.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md001/proper_atx_heading_incrementing.md",
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
def test_md001_good_proper_setext_heading_incrementing():
    """
    Test to make sure the rule doesn't trigger with a document with
    only SetExt Headings, that when they increase, only increase by 1.
    Note that after the first 2 headings, it switches over to Atx Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "MD003",
        "scan",
        "test/resources/rules/md001/proper_setext_heading_incrementing.md",
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
def test_md001_bad_improper_atx_heading_incrementing():
    """
    Test to make sure the rule does trigger with a document with
    only Atx Headings, that when they increase, only increase by 2.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md001/improper_atx_heading_incrementing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md001/improper_atx_heading_incrementing.md:3:1: "
        + "MD001: Heading levels should only increment by one level at a time. "
        + "[Expected: h2; Actual: h3] (heading-increment,header-increment)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md001_bad_improper_setext_heading_incrementing():
    """
    Test to make sure the rule does trigger with a document with
    only SetExt Headings (and Atx Headings after level 2), that when they
    increase, only increase by 2.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "MD003",
        "scan",
        "test/resources/rules/md001/improper_setext_heading_incrementing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md001/improper_setext_heading_incrementing.md:4:1: "
        + "MD001: Heading levels should only increment by one level at a time. "
        + "[Expected: h3; Actual: h4] (heading-increment,header-increment)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md001_front_matter_with_no_title():
    """
    Test to make sure the rule does not trigger with a document with
    a front-matter element with no title and the front matter extension
    enabled, and a following Atx Heading of level 3.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
        "scan",
        "test/resources/rules/md001/front_matter_with_no_title.md",
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
def test_md001_front_matter_with_title():
    """
    Test to make sure the rule does trigger with a document with
    a front-matter element with a title and the front matter extension
    enabled, and a following Atx Heading of level 3.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
        "scan",
        "test/resources/rules/md001/front_matter_with_title.md",
    ]

    expected_return_code = 1
    expected_output = "test/resources/rules/md001/front_matter_with_title.md:5:1: MD001: Heading levels should only increment by one level at a time. [Expected: h2; Actual: h3] (heading-increment,header-increment)\n"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md001_front_matter_with_alternate_title():
    """
    Variation of test_md001_front_matter_with_title using configuration
    to specify an alternate title.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
        "--set",
        "plugins.md001.front_matter_title=Subject",
        "scan",
        "test/resources/rules/md001/front_matter_with_alternate_title.md",
    ]

    expected_return_code = 1
    expected_output = "test/resources/rules/md001/front_matter_with_alternate_title.md:5:1: MD001: Heading levels should only increment by one level at a time. [Expected: h2; Actual: h3] (heading-increment,header-increment)\n"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
