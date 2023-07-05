"""
Module to provide tests related to the MD026 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import write_temporary_configuration

import pytest


@pytest.mark.rules
def test_md051_all_assets_are_referenced():
    """
    Test to make sure this rule does not trigger with a document that
    contains a Atx heading that does not end in punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(".")
    supplied_arguments = [
        "scan",
        source_path,
    ]
    cwd = os.path.join("test", "resources", "rules", "md051", "good")

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(cwd=cwd, arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md051_all_assets_are_referenced_in_multiple_files():
    """
    Test to make sure this rule does not trigger with a document that
    contains a Atx heading that does not end in punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(".")
    supplied_arguments = [
        "scan",
        source_path,
    ]
    cwd = os.path.join("test", "resources", "rules", "md051", "good2")

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(cwd=cwd, arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md051_all_assets_are_referenced_only_once_in_multiple_files():
    """
    Test to make sure this rule does not trigger with a document that
    contains a Atx heading that does not end in punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(".")
    supplied_arguments = [
        "scan",
        source_path,
    ]
    cwd = os.path.join("test", "resources", "rules", "md051", "good3")

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(cwd=cwd, arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md051_excluded_files():
    """
    Test to make sure this rule does not trigger with a document that
    contains a Atx heading that does not end in punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(".")
    supplied_arguments = [
        "scan",
        source_path,
    ]
    cwd = os.path.join("test", "resources", "rules", "md051", "excluded")

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(cwd=cwd, arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md051_unused_asset():
    """
    Test to make sure this rule does not trigger with a document that
    contains a Atx heading that does not end in punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(".")
    supplied_arguments = [
        "scan",
        source_path,
    ]
    cwd = os.path.join("test", "resources", "rules", "md051", "bad")

    expected_return_code = 1
    asset_path = os.path.join("assets", "1x1.png")
    expected_output = f"{asset_path}:0:0: MD051: Unused assets found. (unused-assets)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(cwd=cwd, arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md051_with_configuration():
    """
    Test to make sure this rule does trigger in the configured asset folder on the configured files
    """

    # Arrange
    scanner = MarkdownScanner()
    cwd = os.path.join("test", "resources", "rules", "md051", "config")
    supplied_configuration = {
        "plugins": {
            "md051": {"assetsglob": "**/assets2use/**/*", "assetsregex": r".*\.(txt)$"}
        }
    }
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            ".",
        ]

        expected_return_code = 1
        asset_path = os.path.join("assets2use", "unused.txt")
        expected_output = (
            f"{asset_path}:0:0: MD051: Unused assets found. (unused-assets)"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(cwd=cwd, arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)
