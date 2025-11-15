"""
Module to provide tests related to the MD003 rule.
"""

from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from test.utils import create_temporary_configuration_file

import pytest

# pylint: disable=too-many-lines

only_enable_this_rule_arguments = (
    "-e",
    "md003",
    "-d",
    "*",
)

__headings_atx_both = """# ATX style H1

## ATX style H2
"""

__headings_atx_closed_both = """# ATX style H1 #

## ATX style H2 ##
"""

__headings_atx_with_atx_closed = """# ATX style H1

## ATX style H2 ##
"""

__headings_setext_both = """Heading 1
---------

Heading 2
=========
"""
__headings_setext_with_atx = """Heading 1
=========

Heading 2
---------

### Heading 3
"""
__headings_setext_with_atx_closed = """Heading 1
=========

Heading 2
---------

### Heading 3 ###
"""

__headings_setext_with_level_2_atx = """Heading 1
=========

Heading 2
---------

## Heading 2
"""
__headings_setext_with_level_3_then_level_2_atx = """Heading 1
=========

Heading 2
---------

### Heading 3

## Heading 2 Again
"""


@pytest.mark.plugins
def test_md003_bad_configuration_style() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with a string that is not in the list of acceptable values.
    """

    # Arrange
    scanner = MarkdownScanner()
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_both, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            *only_enable_this_rule_arguments,
            "--strict-config",
            "--set",
            "plugins.md003.style=fred",
            "scan",
            markdown_file_path,
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


## --- Style = consistent (default) ---


@pytest.mark.plugins
def test_md003_good_consistent_headings_atx() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    only contains Atx Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_both, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            *only_enable_this_rule_arguments,
            "scan",
            markdown_file_path,
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


@pytest.mark.plugins
@pytest.mark.user_properties(
    {"DupCov": {"W002": {"Reason": "Part of consistent setting tests."}}}
)
def test_md003_good_consistent_atx_with_invalid_style() -> None:
    """
    Variation of previous test to test default if an invalid style is given.
    Because it is not one of the "known" styles, it should default to "consistent".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "not-valid"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
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


@pytest.mark.plugins
@pytest.mark.user_properties(
    {"DupCov": {"W002": {"Reason": "Part of consistent setting tests."}}}
)
def test_md003_good_consistent_headings_atx_closed() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    only contains Atx Closed Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_closed_both, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            *only_enable_this_rule_arguments,
            "scan",
            markdown_file_path,
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


@pytest.mark.plugins
@pytest.mark.user_properties(
    {"DupCov": {"W002": {"Reason": "Part of consistent setting tests."}}}
)
def test_md003_good_consistent_headings_setext() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    only contains SetExt Headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_both, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            *only_enable_this_rule_arguments,
            "scan",
            markdown_file_path,
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


@pytest.mark.plugins
@pytest.mark.user_properties(
    {"DupCov": {"W002": {"Reason": "Part of consistent setting tests."}}}
)
def test_md003_bad_consistent_headings_setext_with_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for the first two levels and
    Atx Headings after that.
    """

    # Arrange
    scanner = MarkdownScanner()
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_atx, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            *only_enable_this_rule_arguments,
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"{markdown_file_path}:7:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
def test_md003_good_consistent_headings_setext_with_atx_with_allow_config() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for the first two levels and
    Atx Headings after that.  Also, turn on the `allow-setext-update`
    configuration to allow the discovered `setext` to be upgraded to
    `atx` if possible, negating the rule violation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"allow-setext-update": True}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_atx, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "--strict-config",
                "scan",
                markdown_file_path,
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


@pytest.mark.plugins
def test_md003_bad_consistent_headings_setext_with_level_2_atx_and_allow_config() -> (
    None
):
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for the first two levels and
    Atx Headings after that.  Also, turn on the `allow-setext-update`
    configuration to allow the discovered `setext` to be upgraded to
    `atx` if possible.  In this case, the setext cannot be upgraded.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"allow-setext-update": True}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_level_2_atx,
        file_name_suffix=".md",
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "--strict-config",
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:7:1: "
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


@pytest.mark.plugins
@pytest.mark.skip(reason="Duplicate coverage")
@pytest.mark.user_properties({"DupCov": {"W002": {}}})
def test_md003_bad_consistent_headings_setext_with_level_3_then_level_2_atx_and_allow_config() -> (
    None
):
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for the first two levels and
    Atx Headings after that.  Also, turn on the `allow-setext-update`
    configuration to allow the discovered `setext` to be upgraded to
    `atx` if possible.  In this case, the setext cannot be upgraded.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"allow-setext-update": True}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_level_3_then_level_2_atx,
        file_name_suffix=".md",
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "--strict-config",
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:9:1: "
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


@pytest.mark.plugins
@pytest.mark.user_properties(
    {"DupCov": {"W002": {"Reason": "Part of consistent setting tests."}}}
)
def test_md003_bad_consistent_headings_setext_with_atx_closed() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for the first two levels and Atx Closed Headings
    for the other levels. Variation on test_md003_bad_consistent_headings_setext_with_atx
    with atx closed instead of atx.
    """

    # Arrange
    scanner = MarkdownScanner()
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_atx_closed, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            *only_enable_this_rule_arguments,
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"{markdown_file_path}:7:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
@pytest.mark.user_properties(
    {"DupCov": {"W002": {"Reason": "Part of consistent setting tests."}}}
)
def test_md003_bad_consistent_headings_atx_with_atx_closed() -> None:
    """
    Test to make sure this rule does trigger with a document that starts with an atx
    heading and then has an atx closed heading, with configuration set to consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_with_atx_closed, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            *only_enable_this_rule_arguments,
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"{markdown_file_path}:3:1: "
            + "MD003: Heading style should be consistent throughout the document. "
            + "[Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


## --- Style = atx ---


@pytest.mark.plugins
def test_md003_good_atx_headings_atx() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    only contains Atx Headings for configuration set to "atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
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


@pytest.mark.plugins
@pytest.mark.user_properties(
    {
        "DupCov": {
            "W001": {"Reason": "Part of atx setting tests."},
            "W002": {"Reason": "Part of atx setting tests."},
            "W003": {"Reason": "Part of atx setting tests."},
        }
    }
)
def test_md003_bad_atx_headings_atx_closed() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Closed Headings for configuration set to "atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_closed_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:1:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
                + f"{markdown_file_path}:3:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
# TODO
@pytest.mark.user_properties(
    {
        "DupCov": {
            "W001": {"Reason": "Part of atx setting tests."},
            "W002": {"Reason": "Part of atx setting tests."},
            "W003": {"Reason": "Part of atx setting tests."},
        }
    }
)
def test_md003_bad_atx_headings_setext() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for configuration set to "atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:2:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
                + f"{markdown_file_path}:5:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
            )

            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
@pytest.mark.user_properties(
    {"DupCov": {"W002": {"Reason": "Part of atx setting tests."}}}
)
def test_md003_bad_atx_headings_setext_with_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt_Atx Headings for configuration set to "atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_atx, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:2:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
                + f"{markdown_file_path}:5:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
@pytest.mark.user_properties(
    {
        "DupCov": {
            "W002": {"Reason": "Part of atx setting tests."},
            "W003": {"Reason": "Part of atx setting tests."},
        }
    }
)
def test_md003_bad_atx_headings_setext_with_atx_closed() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt+Atx Closed Headings for configuration set to "atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_atx_closed, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:2:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
                + f"{markdown_file_path}:5:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx; Actual: setext] (heading-style,header-style)\n"
                + f"{markdown_file_path}:7:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
            )

            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
@pytest.mark.user_properties(
    {"DupCov": {"W002": {"Reason": "Part of consistent setting tests."}}}
)
def test_md003_bad_atx_headings_atx_with_atx_closed() -> None:
    """
    Test to make sure this rule does trigger with a document that starts with an atx
    heading and then has an atx closed heading, with configuration set to consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_with_atx_closed, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:3:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


## --- Style = atx_closed ---


@pytest.mark.plugins
@pytest.mark.user_properties(
    {
        "DupCov": {
            "W001": {"Reason": "Part of atx setting tests."},
            "W003": {"Reason": "Part of atx_closed setting tests."},
        }
    }
)
def test_md003_bad_atxclosed_headings_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Headings for configuration set to "atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:1:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
                + f"{markdown_file_path}:3:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
def test_md003_good_atxclosed_headings_atx_closed() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    only contains Atx Closed Headings for configuration set to "atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_closed_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
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


@pytest.mark.plugins
@pytest.mark.user_properties(
    {"DupCov": {"W003": {"Reason": "Part of atx_closed setting tests."}}}
)
def test_md003_bad_atxclosed_headings_setext() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt Headings for configuration set to "atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:2:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
                + f"{markdown_file_path}:5:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
@pytest.mark.user_properties(
    {
        "DupCov": {
            "W002": {"Reason": "Part of atx_closed setting tests."},
            "W003": {"Reason": "Part of atx_closed setting tests."},
        }
    }
)
def test_md003_bad_atxclosed_headings_setext_with_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt+Atx Headings for configuration set to "atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_atx, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:2:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
                + f"{markdown_file_path}:5:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
                + f"{markdown_file_path}:7:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
            )

            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
@pytest.mark.user_properties(
    {"DupCov": {"W002": {"Reason": "Part of atx_closed setting tests."}}}
)
def test_md003_bad_atxclosed_headings_setext_with_atx_closed() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt+Atx Closed Headings for configuration set to "atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_atx_closed, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:2:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
                + f"{markdown_file_path}:5:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


## --- Style = setext ---


@pytest.mark.plugins
@pytest.mark.user_properties(
    {"DupCov": {"W003": {"Reason": "Part of setext setting tests."}}}
)
def test_md003_bad_setext_headings_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Headings for configuration set to "setext".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:1:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
                + f"{markdown_file_path}:3:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
@pytest.mark.user_properties(
    {"DupCov": {"W003": {"Reason": "Part of setext setting tests."}}}
)
def test_md003_bad_setext_headings_atx_closed() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Closed Headings for configuration set to "setext".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_closed_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:1:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
                + f"{markdown_file_path}:3:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
def test_md003_good_setext_headings_setext() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    only contains SetExt Headings for configuration set to "setext".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
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


@pytest.mark.plugins
@pytest.mark.user_properties(
    {
        "DupCov": {
            "W002": {"Reason": "Part of setext setting tests."},
            "W003": {"Reason": "Part of setext setting tests."},
        }
    }
)
def test_md003_bad_setext_headings_setext_with_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt+Atx Headings for configuration set to "setext".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_atx, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:7:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
@pytest.mark.user_properties(
    {
        "DupCov": {
            "W002": {"Reason": "Part of setext setting tests."},
            "W003": {"Reason": "Part of setext setting tests."},
        }
    }
)
def test_md003_bad_setext_headings_setext_with_atx_closed() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Closed Headings for configuration set to "setext".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_atx_closed, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:7:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


## --- Style = setext_with_atx ---


@pytest.mark.plugins
def test_md003_bad_setext_with_atx_headings_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Headings for configuration set to "setext_with_atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:1:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: setext_with_atx; Actual: atx] (heading-style,header-style)\n"
                + f"{markdown_file_path}:3:1: "
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


@pytest.mark.plugins
@pytest.mark.user_properties(
    {"DupCov": {"W002": {"Reason": "Part of setext_with_atx setting tests."}}}
)
def test_md003_bad_setext_with_atx_headings_atx_closed() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Closed Headings for configuration set to "setext_with_atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_closed_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:1:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: setext_with_atx; Actual: atx_closed] (heading-style,header-style)\n"
                + f"{markdown_file_path}:3:1: "
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


@pytest.mark.plugins
# TODO
@pytest.mark.user_properties(
    {"DupCov": {"W003": {"Reason": "Part of setext_with_atx setting tests."}}}
)
def test_md003_good_setext_with_atx_headings_setext() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    only contains SetExt Headings for configuration set to "setext_with_atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
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


@pytest.mark.plugins
def test_md003_good_setext_with_atx_headings_setext_with_atx() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    only contains SetExt+Atx Headings for configuration set to "setext_with_atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_atx, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
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


@pytest.mark.plugins
# TODO ?
@pytest.mark.user_properties({"DupCov": {"W002": {}}})
def test_md003_bad_setext_with_atx_headings_setext_with_atx_closed() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt+Atx Closed Headings for configuration set to "setext_with_atx".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_atx_closed, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:7:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


## --- Style = setext_with_atx_closed ---


@pytest.mark.plugins
def test_md003_bad_setext_with_atx_closed_headings_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Headings for configuration set to "setext_with_atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:1:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
                + f"{markdown_file_path}:3:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
@pytest.mark.user_properties({"DupCov": {"W002": {}}})
def test_md003_bad_setext_with_atx_closed_headings_atx_closed() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains Atx Closed Headings for configuration set to "setext_with_atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_atx_closed_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:1:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
                + f"{markdown_file_path}:3:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
@pytest.mark.user_properties({"DupCov": {"W002": {}, "W003": {}}})
def test_md003_good_setext_with_atx_closed_headings_setext() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    only contains SetExt Headings for configuration set to "setext_with_atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_both, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
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


@pytest.mark.plugins
def test_md003_bad_setext_with_atx_closed_headings_setext_with_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    only contains SetExt+Atx Headings for configuration set to "setext_with_atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_atx, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
            ]

            expected_return_code = 1
            expected_output = (
                f"{markdown_file_path}:7:1: "
                + "MD003: Heading style should be consistent throughout the document. "
                + "[Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
            )
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.plugins
@pytest.mark.user_properties({"DupCov": {"W002": {}}})
def test_md003_good_setext_with_atx_closed_headings_setext_with_atx_closed() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    only contains SetExt+Atx Closed Headings for configuration set to "setext_with_atx_closed".
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md003": {"style": "setext_with_atx_closed"}}}
    with create_temporary_configuration_file(
        supplied_configuration=__headings_setext_with_atx_closed, file_name_suffix=".md"
    ) as markdown_file_path:
        with create_temporary_configuration_file(
            supplied_configuration
        ) as configuration_file:
            supplied_arguments = [
                *only_enable_this_rule_arguments,
                "-c",
                configuration_file,
                "scan",
                markdown_file_path,
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


@pytest.mark.plugins
def test_md003_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md003",
        """
  ITEM               DESCRIPTION

  Id                 md003
  Name(s)            heading-style,header-style
  Short Description  Heading style should be consistent throughout the documen
                     t.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md003.md


  CONFIGURATION ITEM   TYPE     VALUE

  style                string   "consistent"
  allow-setext-update  boolean  False

""",
    )
    execute_query_configuration_test(config_test)
