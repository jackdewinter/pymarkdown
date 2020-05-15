"""
Module to provide tests related to the MD001 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md001_all_samples():
    """
    Test to make sure we get the expected behavior after scanning all the files in the
    test/resources/rules/md001 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = ["--disable-rules", "MD003", "test/resources/rules/md001"]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md001/improper_atx_heading_incrementing.md:0:0: "
        + "MD001: Heading levels should only increment by one level at a time "
        + "[Expected: h2; Actual: h3] (heading-increment,header-increment)\n"
        + "test/resources/rules/md001/improper_setext_heading_incrementing.md:0:0: "
        + "MD001: Heading levels should only increment by one level at a time "
        + "[Expected: h3; Actual: h4] (heading-increment,header-increment)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "test/resources/rules/md001/proper_atx_heading_incrementing.md"
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "--disable-rules",
        "MD003",
        "test/resources/rules/md001/proper_setext_heading_incrementing.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "test/resources/rules/md001/improper_atx_heading_incrementing.md"
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md001/improper_atx_heading_incrementing.md:0:0: "
        + "MD001: Heading levels should only increment by one level at a time "
        + "[Expected: h2; Actual: h3] (heading-increment,header-increment)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "--disable-rules",
        "MD003",
        "test/resources/rules/md001/improper_setext_heading_incrementing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md001/improper_setext_heading_incrementing.md:0:0: "
        + "MD001: Heading levels should only increment by one level at a time "
        + "[Expected: h3; Actual: h4] (heading-increment,header-increment)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
