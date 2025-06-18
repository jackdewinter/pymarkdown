"""
Module to provide tests related to the MD043 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md043_bad_configuration_headings() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    headings value with an integer that is not a string.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_simple_headings.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md043.headings' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_configuration_headings_dupicate_stars() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    headings value with duplicate wildcards.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_simple_headings.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# 1,*,*,# 2",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md043.headings' is not valid: Heading format not valid: Two wildcard elements cannot be next to each other."
    )

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_good_configuration_headings_empty() -> None:
    """
    Test to verify that a configuration error is thrown when supplying the
    headings value that is an empty string.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_simple_headings.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_configuration_headings_no_atx_start() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple headings and a pattern of one constant heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_simple_headings.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=a heading",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md043.headings' is not valid: "
        + "Heading format not valid: Element must start with hash characters (#)."
    )

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_configuration_headings_too_many_hashes() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple headings and a pattern of one bad level constant heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_simple_headings.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=####### a heading",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md043.headings' is not valid: "
        + "Heading format not valid: Element must start with between 1 and 6 hash characters (#)."
    )

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_configuration_headings_bad_whitespace() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple headings and a pattern of one badly specified heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_simple_headings.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=######a heading",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md043.headings' is not valid: Heading format not valid: "
        + "Element must have exactly one space character and one non-space character after any hash characters (#)."
    )

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_configuration_headings_bad_text() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple headings and a pattern with no text.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_simple_headings.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=###### ",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "\n\nBadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md043.headings' is not valid: "
        + "Heading format not valid: Element must have exactly one space character and one non-space character after any hash characters (#)."
    )

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_configuration_headings_bad_text_2() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains multiple headings and a pattern with no text.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_simple_headings.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=######  a",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "\n\nBadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md043.headings' is not valid: "
        + "Heading format not valid: Element must have exactly one space character and one non-space character after any hash characters (#)."
    )

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_good_simple_headings_no_format() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains multiple headings and a default pattern.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_simple_headings.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_good_single_heading_atx_with_single_rule() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains a single heading and a pattern of that one heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_single_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_single_heading_atx_with_double_rule() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains a single heading and a pattern of two headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_single_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,## Another heading",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD043: Required heading structure "
        + "[Missing heading: ## Another heading] (required-headings,required-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_double_heading_atx_with_single_rule() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two headings and a pattern of one heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_double_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD043: Required heading structure "
        + "[Extra heading] (required-headings,required-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_good_double_heading_atx_with_double_rule() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two headings and a pattern of those two headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_double_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,## Another heading",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_good_double_heading_atx_with_double_rule_with_spaces_in_config() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two headings and a pattern of those two headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_double_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings= # This is a single heading , ## Another heading ",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_double_heading_atx_with_double_rule_bad_level() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two headings and a pattern with a bad level matching second heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_double_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,### A bad level",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD043: Required heading structure "
        + "[Bad heading level: Expected: 3, Actual: 2] (required-headings,required-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_double_heading_atx_with_double_rule_bad_text() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two headings and a pattern with a bad text matching second heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_double_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,## A bad level",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD043: Required heading structure "
        + "[Bad heading text: Expected: A bad level, Actual: Another heading] (required-headings,required-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_good_double_heading_atx_second_has_emphasis() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two headings and a pattern with a bad text (emphasis) matching second heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md043",
        "good_double_heading_atx_second_has_emphasis.md",
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,## Another heading",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD043: Required heading structure "
        + "[Bad heading: Required headings must only be normal text.] (required-headings,required-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_good_simple_headings_simple_format() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains mixed headings and a pattern with those headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_simple_headings.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,## Heading 2,### Heading 3,## Heading 2,### Heading 3",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_good_double_heading_atx_with_double_rule_matching_1_star() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains two headings and a pattern with the first heading and a wildcard.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_double_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,*",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_double_heading_atx_with_double_rule_unmatching_1_star() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two headings and a pattern that does not match the first, followed by wildcard.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_double_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# A single heading,*",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD043: Required heading structure "
        + "[Wildcard heading match failed.] (required-headings,required-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_good_double_heading_atx_with_double_rule_matching_star_2() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains two headings and a pattern with a wildcard and the second heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_double_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=*,## Another heading",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_double_heading_atx_with_double_rule_unmatching_star_2() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two headings and a pattern with a wildcard and a bad matching second.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_double_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=*,## Second heading",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD043: Required heading structure "
        + "[Wildcard heading match failed.] (required-headings,required-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_double_heading_atx_unmatching_1_2_3_star() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two headings and a pattern with three constant headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_double_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,## Another heading,## Another heading,*",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD043: Required heading structure "
        + "[Wildcard heading match failed.] (required-headings,required-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_double_heading_atx_unmatching_star_1_2_3() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two headings and a pattern with a wildcard and three headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_double_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=*,# This is a single heading,## Another heading,## Another heading",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD043: Required heading structure "
        + "[Wildcard heading match failed.] (required-headings,required-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_double_heading_atx_matching_1_2_start_2_over() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains two headings and a pattern with two headings, a wildcard, and a matching heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_double_heading_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,## Another heading,*,## Another heading",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD043: Required heading structure "
        + "[Wildcard heading match failed.] (required-headings,required-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_good_simple_headings_rule_matching_1_star_2_3() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains headings and a pattern with a pattern of wildcards and matching headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_simple_headings.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,## Heading 2,### Heading 3",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_good_good_simple_headings_1_star_3_star_3() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains headings and a pattern with a pattern of wildcards and matching headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_simple_headings.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,### Heading 3,*,### Heading 3",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_good_many_level_two_1_star_3_star_3() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains headings and a pattern with a pattern of wildcards and matching headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_many_level_two.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,### Heading 3,*,### Heading 3",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD043: Required heading structure "
        + "[Multiple wildcard matching failed.] (required-headings,required-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_good_good_many_level_two_1_star_2_star_2_star_3() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains headings and a pattern with a pattern of wildcards and matching headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_many_level_two.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,## Heading 2,*,## Heading 2,*,### Heading 3",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_good_many_level_two_1_star_2_star_2_star_3() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains headings and a pattern with a pattern of wildcards and matching headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_many_level_two.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,### Heading 3,*,### Heading 3,*,### Heading 3",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD043: Required heading structure "
        + "[Multiple wildcard matching failed.] (required-headings,required-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_good_good_simple_headings_two_1_star_3_2_star_3() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains headings and a pattern with a pattern of wildcards and matching headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_simple_headings.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,### Heading 3,## Heading 2,*,### Heading 3",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md043_bad_good_many_level_two_1_star_3_2_star_3() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains headings and a pattern with a pattern of wildcards and matching headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md043", "good_many_level_two.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,### Heading 3,## Heading 2,*,### Heading 3",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD043: Required heading structure "
        + "[Multiple wildcard matching failed.] (required-headings,required-headers)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_md043_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md043",
        """
  ITEM               DESCRIPTION

  Id                 md043
  Name(s)            required-headings,required-headers
  Short Description  Required heading structure
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md043.md


  CONFIGURATION ITEM  TYPE    VALUE

  headings            string  ""

""",
    )
    execute_query_configuration_test(config_test)
