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
    Test to make
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
    expected_error = """ValueError encountered while initializing extensions:
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md001 directory using atx headings.
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md001 directory using atx headings.
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
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md001 directory starting with a pair of setext headings and finishing
    with a pair of atx headings.
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
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md001 directory that has an atx heading that is more than a 1
    step positive jump.
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
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md001 directory that starts with a level 2 setext heading and
    is then followed by a level 4 atx heading (as there is only a level 1 and 2 setext
    heading).
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
    Test to make
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
    Test to make
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
    Test to make
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
