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
    supplied_arguments = [
        "--disable-rules",
        "MD003",
        "--enable-rules",
        "MD002",
        "scan",
        "test/resources/rules/md002",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md002/improper_atx_heading_start.md:1:1: "
        + "MD002: First heading of the document should be a top level heading. "
        + "[Expected: h1; Actual: h2] (first-heading-h1,first-header-h1)\n"
        + "test/resources/rules/md002/improper_setext_heading_start.md:2:1: "
        + "MD002: First heading of the document should be a top level heading. "
        + "[Expected: h1; Actual: h2] (first-heading-h1,first-header-h1)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md002_bad_configuration_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md002 directory that starts with a h1 atx heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--strict-config",
        "--set",
        "plugins.md002.level=1",
        "--enable-rules",
        "MD002",
        "scan",
        "test/resources/rules/md002/proper_atx_heading_start.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md002.level' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md002_good_proper_atx_heading_start():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md002 directory that starts with a h1 atx heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD002",
        "scan",
        "test/resources/rules/md002/proper_atx_heading_start.md",
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
def test_md002_bad_proper_atx_heading_start_with_alternate_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md002 directory that starts with a h1 atx heading.  The modified
    configuration will cause the file to be parsed with reported issues.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md002": {"level": 2}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "--enable-rules",
            "MD002",
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md002/proper_atx_heading_start.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md002/proper_atx_heading_start.md:1:1: "
            + "MD002: First heading of the document should be a top level heading. "
            + "[Expected: h2; Actual: h1] (first-heading-h1,first-header-h1)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md002_good_proper_setext_heading_start():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md002 directory starting with a setext heading of ====== to
    create a h1 heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD002",
        "scan",
        "test/resources/rules/md002/proper_setext_heading_start.md",
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
def test_md002_bad_proper_setext_heading_start_with_alternate_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md002 directory starting with a setext heading of ====== to
    create a h1 heading.  The modified  configuration will cause the file to be parsed
    with reported issues.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md002": {"level": 2}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "--enable-rules",
            "MD002",
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md002/proper_setext_heading_start.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md002/proper_setext_heading_start.md:2:1: "
            + "MD002: First heading of the document should be a top level heading. "
            + "[Expected: h2; Actual: h1] (first-heading-h1,first-header-h1)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md002_bad_improper_atx_heading_start():
    """
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md002 directory that starts with a non-h1 heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--enable-rules",
        "MD002",
        "scan",
        "test/resources/rules/md002/improper_atx_heading_start.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md002/improper_atx_heading_start.md:1:1: "
        + "MD002: First heading of the document should be a top level heading. "
        + "[Expected: h1; Actual: h2] (first-heading-h1,first-header-h1)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md002_good_improper_atx_heading_start_with_alternate_configuration():
    """
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md002 directory that starts with a non-h1 heading.  The modified
    configuration will allow the file to be parsed properly.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md002": {"level": 2}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "--enable-rules",
            "MD002",
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md002/improper_atx_heading_start.md",
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
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md002_bad_improper_setext_heading_start():
    """
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md002 directory starting with a setext heading of ----- to
    create a h2 heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "MD003",
        "--enable-rules",
        "MD002",
        "scan",
        "test/resources/rules/md002/improper_setext_heading_start.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md002/improper_setext_heading_start.md:2:1: "
        + "MD002: First heading of the document should be a top level heading. "
        + "[Expected: h1; Actual: h2] (first-heading-h1,first-header-h1)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md002_good_improper_setext_heading_start_with_alternate_configuration():
    """
    Test to make sure we get the expected behavior after scanning a bad file from the
    test/resources/rules/md002 directory starting with a setext heading of ----- to
    create a h2 heading.   The modified configuration will allow the file to be parsed
    properly.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md002": {"level": 2}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "--disable-rules",
            "MD003",
            "--enable-rules",
            "MD002",
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md002/improper_setext_heading_start.md",
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
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)
