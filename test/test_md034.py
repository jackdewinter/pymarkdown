"""
Module to provide tests related to the MD034 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md034_good_no_base_url():
    """
    Test to make sure this rule does not trigger with a document that
    contains `http`, but no full urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/good_no_base_url.md",
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
def test_md034_good_no_url_marker():
    """
    Test to make sure this rule does not trigger with a document that
    contains `www.google.com`, but no full urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/good_no_url_marker.md",
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
def test_md034_bad_with_http_url():
    """
    Test to make sure this rule does trigger with a document that
    contains http and https full urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/bad_with_http_url.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md034/bad_with_http_url.md:3:6: MD034: Bare URL used (no-bare-urls)\n"
        + "test/resources/rules/md034/bad_with_http_url.md:5:1: MD034: Bare URL used (no-bare-urls)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md034_bad_with_ftp_url():
    """
    Test to make sure this rule does trigger with a document that
    contains ftp and ftps full urls.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/bad_with_ftp_url.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md034/bad_with_ftp_url.md:3:6: MD034: Bare URL used (no-bare-urls)\n"
        + "test/resources/rules/md034/bad_with_ftp_url.md:5:1: MD034: Bare URL used (no-bare-urls)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md034_bad_with_http_url_in_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains http urls in Atx Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/bad_with_http_url_in_atx.md",
    ]

    expected_return_code = 1
    expected_output = "test/resources/rules/md034/bad_with_http_url_in_atx.md:1:9: MD034: Bare URL used (no-bare-urls)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md034_bad_with_http_url_in_setext():
    """
    Test to make sure this rule does trigger with a document that
    contains http urls in SetExt Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/bad_with_http_url_in_setext.md",
    ]

    expected_return_code = 1
    expected_output = "test/resources/rules/md034/bad_with_http_url_in_setext.md:1:7: MD034: Bare URL used (no-bare-urls)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md034_good_http_url_in_indented():
    """
    Test to make sure this rule does not trigger with a document that
    contains http urls in indented code blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/good_http_url_in_indented.md",
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
def test_md034_good_http_url_in_fenced():
    """
    Test to make sure this rule does not trigger with a document that
    contains http urls in Fenced code blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/good_http_url_in_fenced.md",
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
def test_md034_good_http_url_in_html():
    """
    Test to make sure this rule does not trigger with a document that
    contains http urls in HTML blocks.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/good_http_url_in_html.md",
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
def test_md034_good_http_url_in_inline_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains http urls in inline links.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/good_http_url_in_inline_link.md",
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
def test_md034_good_http_url_in_full_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains http urls in full links.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/good_http_url_in_full_link.md",
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
def test_md034_bad_with_local_url():
    """
    Test to make sure this rule does trigger with a document that
    contains http urls with a localhost.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/bad_with_local_url.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md034/bad_with_local_url.md:1:11: "
        + "MD034: Bare URL used (no-bare-urls)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md034_good_with_leading_character():
    """
    Test to make sure this rule does not trigger with a document that
    contains http urls with non-whitespace directly before it.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/good_with_leading_character.md",
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
def test_md034_good_only_url_marker():
    """
    Test to make sure this rule does not trigger with a document that
    contains http with nothing after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/good_only_url_marker.md",
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
def test_md034_good_only_url_marker_and_leading():
    """
    Test to make sure this rule does not trigger with a document that
    contains http:// with nothing after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md034/good_only_url_marker_and_leading.md",
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
