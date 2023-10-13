"""
Module to provide tests related to the MD003 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import create_temporary_configuration_file

import pytest

# pylint: disable=too-many-lines

source_path = os.path.join("test", "resources", "rules", "md003") + os.sep


@pytest.mark.rules
def test_md003_bad_configuration_style():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with a string that is not in the list of acceptable values.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--strict-config",
        "--set",
        "plugins.md003.style=fred",
        "scan",
        f"{source_path}headings_atx.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md003.style' is not valid: Allowable values: "
        + "['consistent', 'atx', 'atx_closed', 'setext', 'setext_with_atx', 'setext_with_atx_closed']"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


CONSISTENT_ATX_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_consistent_headings_atx():
    """
    Test to make sure this rule does not trigger with a document that
    only contains Atx Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        f"{source_path}headings_atx.md",
    ]

    expected_return_code = 0
    expected_output = CONSISTENT_ATX_HEADINGS_SAMPLE_OUTPUT
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


CONSISTENT_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_consistent_headings_atx_closed():
    """
    Test to make sure this rule does not trigger with a document that
    only contains Atx Closed Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        f"{source_path}headings_atx_closed.md",
    ]

    expected_return_code = 0
    expected_output = CONSISTENT_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


CONSISTENT_SETEXT_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_consistent_headings_setext():
    """
    Test to make sure this rule does not trigger with a document that
    only contains SetExt Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        f"{source_path}headings_setext.md",
    ]

    expected_return_code = 0
    expected_output = CONSISTENT_SETEXT_HEADINGS_SAMPLE_OUTPUT
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


CONSISTENT_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_setext_with_atx.md:7:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_consistent_headings_setext_with_atx():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for the first two levels and
    Atx Headings after that.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        f"{source_path}headings_setext_with_atx.md",
    ]

    expected_return_code = 1
    expected_output = CONSISTENT_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md003_bad_consistent_headings_setext_with_atx_and_allow_config():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for the first two levels and
    Atx Headings after that.  Also, turn on the `allow-setext-update`
    configuration to allow the discovered `setext` to be upgraded to
    `atx` if possible.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"allow-setext-update": True}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "--strict-config",
            "scan",
            f"{source_path}headings_setext_with_atx.md",
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
def test_md003_bad_consistent_headings_setext_with_level_2_atx_and_allow_config():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for the first two levels and
    Atx Headings after that.  Also, turn on the `allow-setext-update`
    configuration to allow the discovered `setext` to be upgraded to
    `atx` if possible.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"allow-setext-update": True}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "--strict-config",
            "scan",
            f"{source_path}headings_setext_with_level_2_atx.md",
        ]

        expected_return_code = 1
        expected_output = (
            f"{source_path}headings_setext_with_level_2_atx.md:7:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext; Actual: atx] (heading-style,header-style)"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md003_bad_consistent_headings_setext_with_level_3_then_level_2_atx_and_allow_config():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for the first two levels and
    Atx Headings after that.  Also, turn on the `allow-setext-update`
    configuration to allow the discovered `setext` to be upgraded to
    `atx` if possible.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"allow-setext-update": True}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "--strict-config",
            "scan",
            f"{source_path}headings_setext_with_level_3_then_level_2_atx.md",
        ]

        expected_return_code = 1
        expected_output = (
            f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:9:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext_with_atx; Actual: atx] (heading-style,header-style)"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


CONSISTENT_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_setext_with_atx_closed.md:7:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_consistent_headings_setext_with_atx_closed():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for the first two levels and Atx Closed Headings
    for the other levels.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        f"{source_path}headings_setext_with_atx_closed.md",
    ]

    expected_return_code = 1
    expected_output = CONSISTENT_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md003_consistent_all_samples():
    """
    Test to make sure we get the expected behavior after scanning all files in the
    test/resources/rules/md003 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["scan", source_path]

    expected_return_code = 1
    expected_output = (
        CONSISTENT_ATX_HEADINGS_SAMPLE_OUTPUT
        + CONSISTENT_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
        + CONSISTENT_SETEXT_HEADINGS_SAMPLE_OUTPUT
        + CONSISTENT_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
        + CONSISTENT_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
        + f"{source_path}headings_setext_with_level_2_atx.md:7:1: "
        + "MD003: Heading style should be consistent throughout the document. "
        + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
        + f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:7:1: "
        + "MD003: Heading style should be consistent throughout the document. "
        + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
        + f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:9:1: "
        + "MD003: Heading style should be consistent throughout the document. "
        + "[Expected: setext; Actual: atx] (heading-style,header-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


ATX_ATX_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_atx_headings_atx():
    """
    Test to make sure this rule does not trigger with a document that
    only contains Atx Headings for configuration set to "atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_atx.md",
        ]

        expected_return_code = 0
        expected_output = ATX_ATX_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md003_good_atx_headings_atxx():
    """
    Variation of previous test to test default.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "not-valid"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_atx.md",
        ]

        expected_return_code = 0
        expected_output = ATX_ATX_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


ATX_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_atx_closed.md:1:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
    + f"{source_path}headings_atx_closed.md:3:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atx_headings_atx_closed():
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Closed Headings for configuration set to "atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = ATX_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


ATX_SETEXT_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_setext.md:2:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
    + f"{source_path}headings_setext.md:5:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atx_headings_setext():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for configuration set to "atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext.md",
        ]

        expected_return_code = 1
        expected_output = ATX_SETEXT_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


ATX_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_setext_with_atx.md:2:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
    + f"{source_path}headings_setext_with_atx.md:5:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atx_headings_setext_with_atx():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt_Atx Headings for configuration set to "atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext_with_atx.md",
        ]

        expected_return_code = 1
        expected_output = ATX_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


ATX_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_setext_with_atx_closed.md:2:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
    + f"{source_path}headings_setext_with_atx_closed.md:5:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
    + f"{source_path}headings_setext_with_atx_closed.md:7:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atx_headings_setext_with_atx_closed():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt+Atx Closed Headings for configuration set to "atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext_with_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = ATX_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md003_atx_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md003 directory for configuration "atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = (
            ATX_ATX_HEADINGS_SAMPLE_OUTPUT
            + ATX_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
            + ATX_SETEXT_HEADINGS_SAMPLE_OUTPUT
            + ATX_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
            + ATX_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
            + f"{source_path}headings_setext_with_level_2_atx.md:2:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_2_atx.md:5:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:2:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:5:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx; Actual: setext] (heading-style,header-style)"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


ATXCLOSED_ATX_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_atx.md:1:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
    + f"{source_path}headings_atx.md:3:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atxclosed_headings_atx():
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Headings for configuration set to "atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_atx.md",
        ]

        expected_return_code = 1
        expected_output = ATXCLOSED_ATX_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


ATXCLOSED_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_atxclosed_headings_atx_closed():
    """
    Test to make sure this rule does not trigger with a document that
    only contains Atx Closed Headings for configuration set to "atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_atx_closed.md",
        ]

        expected_return_code = 0
        expected_output = ATXCLOSED_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


ATXCLOSED_SETEXT_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_setext.md:2:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
    + f"{source_path}headings_setext.md:5:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atxclosed_headings_setext():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for configuration set to "atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext.md",
        ]

        expected_return_code = 1
        expected_output = ATXCLOSED_SETEXT_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


ATXCLOSED_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_setext_with_atx.md:2:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
    + f"{source_path}headings_setext_with_atx.md:5:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
    + f"{source_path}headings_setext_with_atx.md:7:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atxclosed_headings_setext_with_atx():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt+Atx Headings for configuration set to "atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext_with_atx.md",
        ]

        expected_return_code = 1
        expected_output = ATXCLOSED_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


ATXCLOSED_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_setext_with_atx_closed.md:2:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
    + f"{source_path}headings_setext_with_atx_closed.md:5:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atxclosed_headings_setext_with_atx_closed():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt+Atx Closed Headings for configuration set to "atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext_with_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = ATXCLOSED_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md003_atxclosed_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md003 directory with an "atx closed" configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = (
            ATXCLOSED_ATX_HEADINGS_SAMPLE_OUTPUT
            + ATXCLOSED_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
            + ATXCLOSED_SETEXT_HEADINGS_SAMPLE_OUTPUT
            + ATXCLOSED_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
            + ATXCLOSED_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
            + f"{source_path}headings_setext_with_level_2_atx.md:2:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_2_atx.md:5:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_2_atx.md:7:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:2:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:5:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:7:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:9:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx_closed; Actual: atx] (heading-style,header-style)"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_ATX_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_atx.md:1:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
    + f"{source_path}headings_atx.md:3:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_headings_atx():
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Headings for configuration set to "setext".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_atx.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_ATX_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_atx_closed.md:1:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
    + f"{source_path}headings_atx_closed.md:3:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_headings_atx_closed():
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Closed Headings for configuration set to "setext".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_SETEXT_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_setext_headings_setext():
    """
    Test to make sure this rule does not trigger with a document that
    only contains SetExt Headings for configuration set to "setext".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext.md",
        ]

        expected_return_code = 0
        expected_output = SETEXT_SETEXT_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_setext_with_atx.md:7:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_headings_setext_with_atx():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt+Atx Headings for configuration set to "setext".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext_with_atx.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_setext_with_atx_closed.md:7:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_headings_setext_with_atx_closed():
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Closed Headings for configuration set to "setext".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext_with_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md003_setext_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md003 directory with configuration "setext".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = (
            SETEXT_ATX_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_SETEXT_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
            + f"{source_path}headings_setext_with_level_2_atx.md:7:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:7:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:9:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext; Actual: atx] (heading-style,header-style)"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_WITH_ATX_ATX_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_atx.md:1:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_atx.md:3:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_with_atx_headings_atx():
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Headings for configuration set to "setext_with_atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_atx.md",
        ]

        expected_return_code = 1
        expected_output = (
            f"{source_path}headings_atx.md:1:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext_with_atx; Actual: atx] (heading-style,header-style)\n"
            + f"{source_path}headings_atx.md:3:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext_with_atx; Actual: atx] (heading-style,header-style)"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_WITH_ATX_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_atx_closed.md:1:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_atx_closed.md:3:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_with_atx_headings_atx_closed():
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Closed Headings for configuration set to "setext_with_atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = (
            f"{source_path}headings_atx_closed.md:1:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext_with_atx; Actual: atx_closed] (heading-style,header-style)\n"
            + f"{source_path}headings_atx_closed.md:3:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext_with_atx; Actual: atx_closed] (heading-style,header-style)"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_WITH_ATX_SETEXT_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_setext_with_atx_headings_setext():
    """
    Test to make sure this rule does not trigger with a document that
    only contains SetExt Headings for configuration set to "setext_with_atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext.md",
        ]

        expected_return_code = 0
        expected_output = SETEXT_WITH_ATX_SETEXT_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_WITH_ATX_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_setext_with_atx_headings_setext_with_atx():
    """
    Test to make sure this rule does not trigger with a document that
    only contains SetExt+Atx Headings for configuration set to "setext_with_atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext_with_atx.md",
        ]

        expected_return_code = 0
        expected_output = SETEXT_WITH_ATX_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_WITH_ATX_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_setext_with_atx_closed.md:7:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_with_atx_headings_setext_with_atx_closed():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt+Atx Closed Headings for configuration set to "setext_with_atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext_with_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_WITH_ATX_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md003_setext_with_atx_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md003 directory with configuration "setext_with_atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"{source_path}headings_atx.md:1:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext_with_atx; Actual: atx] (heading-style,header-style)\n"
            + f"{source_path}headings_atx.md:3:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext_with_atx; Actual: atx] (heading-style,header-style)\n"
            + f"{source_path}headings_atx_closed.md:1:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext_with_atx; Actual: atx_closed] (heading-style,header-style)\n"
            + f"{source_path}headings_atx_closed.md:3:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext_with_atx; Actual: atx_closed] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_atx_closed.md:7:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_2_atx.md:7:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext_with_atx; Actual: atx] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:9:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext_with_atx; Actual: atx] (heading-style,header-style)"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_WITH_ATX_CLOSED_ATX_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_atx.md:1:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
    + f"{source_path}headings_atx.md:3:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_with_atx_closed_headings_atx():
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Headings for configuration set to "setext_with_atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_atx.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_WITH_ATX_CLOSED_ATX_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_WITH_ATX_CLOSED_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_atx_closed.md:1:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
    + f"{source_path}headings_atx_closed.md:3:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_with_atx_closed_headings_atx_closed():
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Closed Headings for configuration set to "setext_with_atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_WITH_ATX_CLOSED_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_WITH_ATX_CLOSED_SETEXT_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_setext_with_atx_closed_headings_setext():
    """
    Test to make sure this rule does not trigger with a document that
    only contains SetExt Headings for configuration set to "setext_with_atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext.md",
        ]

        expected_return_code = 0
        expected_output = SETEXT_WITH_ATX_CLOSED_SETEXT_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_WITH_ATX_CLOSED_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT = (
    f"{source_path}headings_setext_with_atx.md:7:1: "
    + "MD003: Heading style should be consistent throughout the document. "
    + "[Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_with_atx_closed_headings_setext_with_atx():
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt+Atx Headings for configuration set to "setext_with_atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext_with_atx.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_WITH_ATX_CLOSED_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


SETEXT_WITH_ATX_CLOSED_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_setext_with_atx_closed_headings_setext_with_atx_closed():
    """
    Test to make sure this rule does not trigger with a document that
    only contains SetExt+Atx Closed Headings for configuration set to "setext_with_atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            f"{source_path}headings_setext_with_atx_closed.md",
        ]

        expected_return_code = 0
        expected_output = (
            SETEXT_WITH_ATX_CLOSED_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md003_setext_with_atx_closed_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md003 directory with configuration setext+atx closed
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = (
            SETEXT_WITH_ATX_CLOSED_ATX_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_WITH_ATX_CLOSED_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_WITH_ATX_CLOSED_SETEXT_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_WITH_ATX_CLOSED_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_WITH_ATX_CLOSED_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
            + f"{source_path}headings_setext_with_level_2_atx.md:7:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:7:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
            + f"{source_path}headings_setext_with_level_3_then_level_2_atx.md:9:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext; Actual: atx] (heading-style,header-style)"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
