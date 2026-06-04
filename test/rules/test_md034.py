"""
Module to provide tests related to the MD034 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from typing import Tuple

import pytest


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", "rules", "md034", source_file_name)
    return source_path, os.path.abspath(source_path)


@pytest.mark.rules
def test_md034_good_no_base_url(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains `http`, but no full urls.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_no_base_url.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_good_no_url_marker(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains `www.google.com`, but no full urls.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_no_url_marker.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_bad_with_http_url(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains http and https full urls.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_with_http_url.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:6: MD034: Bare URL used (no-bare-urls)
{abs_source_path}:5:1: MD034: Bare URL used (no-bare-urls)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_bad_with_ftp_url(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains ftp and ftps full urls.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_with_ftp_url.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:6: MD034: Bare URL used (no-bare-urls)
{abs_source_path}:5:1: MD034: Bare URL used (no-bare-urls)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_bad_with_http_url_in_atx(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains http urls in Atx Headings.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_with_http_url_in_atx.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"{abs_source_path}:1:9: MD034: Bare URL used (no-bare-urls)",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_bad_with_http_url_in_setext(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains http urls in SetExt Headings.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "bad_with_http_url_in_setext.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"{abs_source_path}:1:7: MD034: Bare URL used (no-bare-urls)",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_good_http_url_in_indented(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains http urls in indented code blocks.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_http_url_in_indented.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_good_http_url_in_fenced(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains http urls in Fenced code blocks.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_http_url_in_fenced.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_good_http_url_in_html(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains http urls in HTML blocks.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_http_url_in_html.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_good_http_url_in_inline_link(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains http urls in inline links.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_http_url_in_inline_link.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_good_http_url_in_full_link(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains http urls in full links.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_http_url_in_full_link.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_bad_with_local_url(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains http urls with a localhost.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("bad_with_local_url.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"{abs_source_path}:1:11: MD034: Bare URL used (no-bare-urls)",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_good_with_leading_character(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains http urls with non-whitespace directly before it.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_with_leading_character.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_good_only_url_marker(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains http with nothing after it.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_only_url_marker.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_good_only_url_marker_and_leading(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains http:// with nothing after it.
    """

    # Arrange
    source_path, _ = __generate_source_path("good_only_url_marker_and_leading.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md034_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md034",
        """
  ITEM               DESCRIPTION

  Id                 md034
  Name(s)            no-bare-urls
  Short Description  Bare URL used
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md034.md

""",
    )
    execute_query_configuration_test(config_test)
