"""
Module to provide tests related to the MD001 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md001_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md001 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = ["test/resources/rules/md001"]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md001/improper_atx_header_incrementing.md:0:0: "
        + "MD001: Heading levels should only increment by one level at a time "
        + "[Expected: h2; Actual: h3] (heading-increment,header-increment)\n"
        + "test/resources/rules/md001/improper_setext_header_incrementing.md:0:0: "
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
def test_md001_good_atx_sample():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md001 directory using atx headers.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md001/proper_atx_header_incrementing.md"
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
def test_md001_good_setext_sample():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md001 directory starting with a pair of setext headers and finishing
    with a pair of atx headers.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md001/proper_setext_header_incrementing.md"
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
def test_md001_bad_atx_sample():
    """
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md001 directory that...
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md001/improper_atx_header_incrementing.md"
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md001/improper_atx_header_incrementing.md:0:0: "
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
def test_md001_bad_setext_sample():
    """
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md001 directory that...
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md001/improper_setext_header_incrementing.md"
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md001/improper_setext_header_incrementing.md:0:0: "
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
