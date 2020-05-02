"""
Module to provide tests related to the MD002 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

from .utils import write_temporary_configuration


@pytest.mark.rules
def test_md002_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md002 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "--disable-rules",
        "MD003",
        "-e",
        "MD002",
        "test/resources/rules/md002",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md002/improper_atx_header_start.md:0:0: "
        + "MD002: First heading should be a top level heading "
        + "[Expected: h1; Actual: h2] (first-heading-h1,first-header-h1)\n"
        + "test/resources/rules/md002/improper_setext_header_start.md:0:0: "
        + "MD002: First heading should be a top level heading "
        + "[Expected: h1; Actual: h2] (first-heading-h1,first-header-h1)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md002_good_proper_atx_header_start():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md002 directory that starts with a h1 atx header.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "-e",
        "MD002",
        "test/resources/rules/md002/proper_atx_header_start.md",
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
def test_md002_bad_proper_atx_header_start_with_alternate_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md002 directory that starts with a h1 atx header.  The modified
    configuration will cause the file to be parsed with reported issues.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD002": {"level": 2}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-e",
            "MD002",
            "-c",
            configuration_file,
            "test/resources/rules/md002/proper_atx_header_start.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md002/proper_atx_header_start.md:0:0: "
            + "MD002: First heading should be a top level heading "
            + "[Expected: h2; Actual: h1] (first-heading-h1,first-header-h1)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md002_good_proper_setext_header_start():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md002 directory starting with a setext header of ====== to
    create a h1 header.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "-e",
        "MD002",
        "test/resources/rules/md002/proper_setext_header_start.md",
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
def test_md002_bad_proper_setext_header_start_with_alternate_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md002 directory starting with a setext header of ====== to
    create a h1 header.  The modified  configuration will cause the file to be parsed
    with reported issues.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD002": {"level": 2}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-e",
            "MD002",
            "-c",
            configuration_file,
            "test/resources/rules/md002/proper_setext_header_start.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md002/proper_setext_header_start.md:0:0: "
            + "MD002: First heading should be a top level heading "
            + "[Expected: h2; Actual: h1] (first-heading-h1,first-header-h1)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md002_bad_improper_atx_header_start():
    """
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md002 directory that starts with a non-h1 header.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "-e",
        "MD002",
        "test/resources/rules/md002/improper_atx_header_start.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md002/improper_atx_header_start.md:0:0: "
        + "MD002: First heading should be a top level heading "
        + "[Expected: h1; Actual: h2] (first-heading-h1,first-header-h1)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md002_good_improper_atx_header_start_with_alternate_configuration():
    """
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md002 directory that starts with a non-h1 header.  The modified
    configuration will allow the file to be parsed properly.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD002": {"level": 2}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-e",
            "MD002",
            "-c",
            configuration_file,
            "test/resources/rules/md002/improper_atx_header_start.md",
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
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md002_bad_improper_setext_header_start():
    """
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md002 directory starting with a setext header of ----- to
    create a h2 header.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "--disable-rules",
        "MD003",
        "-e",
        "MD002",
        "test/resources/rules/md002/improper_setext_header_start.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md002/improper_setext_header_start.md:0:0: "
        + "MD002: First heading should be a top level heading "
        + "[Expected: h1; Actual: h2] (first-heading-h1,first-header-h1)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md002_good_improper_setext_header_start_with_alternate_configuration():
    """
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md002 directory starting with a setext header of ----- to
    create a h2 header.   The modified configuration will allow the file to be parsed
    properly.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD002": {"level": 2}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "--disable-rules",
            "MD003",
            "-e",
            "MD002",
            "-c",
            configuration_file,
            "test/resources/rules/md002/improper_setext_header_start.md",
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
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)
