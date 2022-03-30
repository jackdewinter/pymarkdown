"""
Module to provide tests related to the MD002 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import write_temporary_configuration

import pytest


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
    Test to verify that a configuration error is thrown when supplying the
    level value with a string of "1".
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
def test_md002_bad_configuration_level_value():
    """
    Test to verify that a configuration error is thrown when supplying the
    level value with an integer outside of the range.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--strict-config",
        "--set",
        "plugins.md002.level=$#10",
        "--enable-rules",
        "MD002",
        "scan",
        "test/resources/rules/md002/proper_atx_heading_start.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md002.level' is not valid: Allowable values are between 1 and 6 (inclusive)."
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
    Test to make sure the rule does not trigger with a level 1
    Atx Heading at the start of the document.
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
    Test to make sure the rule does trigger with a level 1 Atx Heading at the
    start of the document with configuration to change the level to 2.
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
    Test to make sure the rule does not trigger with a level 1 SetExt Heading at the
    start of the document.
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
    Test to make sure the rule does trigger with a level 1 SetExt Heading at the
    start of the document and configuration to change level to `2`.
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
    Test to make sure the rule does trigger with a non-level 1 Atx Heading at the
    start of the document.
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
    Test to make sure the rule does not trigger with a level 2 Atx Heading at the
    start of the document and configuration to match.
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
    Test to make sure the rule does trigger with a non-level 1 SetExt Heading at the
    start of the document.
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
    Test to make sure the rule does not trigger with a level 2 SetExt Heading at the
    start of the document and configuration to match.
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
