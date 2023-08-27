"""
Module to provide tests related to the MD030 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md030_bad_configuration_ul_single():
    """
    Test to verify that a configuration error is thrown when supplying the
    ul_single value with a string that is not an integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "good_one_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=not-integer",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md030.ul_single' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_configuration_ul_single_zero():
    """
    Test to verify that a configuration error is thrown when supplying the
    ul_single value with an integer not greater than 0.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "good_one_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#0",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md030.ul_single' is not valid: Allowable values are any integer greater than 0."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_configuration_ul_multi():
    """
    Test to verify that a configuration error is thrown when supplying the
    ul_multi value with a string that is not an integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "good_one_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_multi=not-integer",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md030.ul_multi' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_configuration_ul_multi_zero():
    """
    Test to verify that a configuration error is thrown when supplying the
    ul_multi value with an integer not greater than 0.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "good_one_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_multi=$#0",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md030.ul_multi' is not valid: Allowable values are any integer greater than 0."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_good_spacing_ul_single():
    """
    Test to make sure this rule does not trigger with a document that
    contains unordered lists with a single space after the marker.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "good_spacing_ul_single.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
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
def test_md030_good_spacing_ul_single_with_config_1_2():
    """
    Test to make sure this rule does not trigger with a document that
    contains unordered lists with a single space after the marker,
    with configuration.  ul_multi does not come into effect as all
    list items have a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "good_spacing_ul_single.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#1",
        "--set",
        "plugins.md030.ul_multi=$#2",
        "--strict-config",
        "scan",
        source_path,
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
def test_md030_good_spacing_ul_single_with_config_2_1():
    """
    Test to make sure this rule does trigger with a document that
    contains unordered lists with a single space after the marker,
    and configuration that applies. ul_multi does not come into effect
    as all list items have a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "good_spacing_ul_single.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#2",
        "--set",
        "plugins.md030.ul_multi=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)\n"
        + f"{source_path}:2:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)\n"
        + f"{source_path}:3:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_single():
    """
    Test to make sure this rule does trigger with a document that
    contains unordered lists with two spaces after the marker.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "bad_spacing_ul_single.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + f"{source_path}:2:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + f"{source_path}:3:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_single_config_1_2():
    """
    Test to make sure this rule does trigger with a document that
    contains unordered lists with two spaces after the marker and
    configuration for multi line lists.  ul_multi does not come into
    effect as all list items have a single paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "bad_spacing_ul_single.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#1",
        "--set",
        "plugins.md030.ul_multi=$#2",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + f"{source_path}:2:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + f"{source_path}:3:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_single_config_2_1():
    """
    Test to make sure this rule does not trigger with a document that contains
    unordered lists with two spaces after the marker, and configuration to make
    it okay. ul_multi does not come into effect as all list items have a single
    paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "bad_spacing_ul_single.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#2",
        "--set",
        "plugins.md030.ul_multi=$#1",
        "--strict-config",
        "scan",
        source_path,
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
def test_md030_good_spacing_ul_double():
    """
    Test to make sure this rule does not trigger with a document that
    contains single-paragraph unordered lists with one space after the marker.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "good_spacing_ul_double.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
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
def test_md030_good_spacing_ul_double_config_1_2():
    """
    Test to make sure this rule does trigger with a document that
    contains single-paragraph unordered lists with one space after the marker,
    and configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "good_spacing_ul_double.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#1",
        "--set",
        "plugins.md030.ul_multi=$#2",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_good_spacing_ul_double_config_2_1():
    """
    Test to make sure this rule does trigger with a document that
    contains single-paragraph unordered lists with one space after the marker,
    and configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "good_spacing_ul_double.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#2",
        "--set",
        "plugins.md030.ul_multi=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)\n"
        + f"{source_path}:5:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_double():
    """
    Test to make sure this rule does trigger with a document that
    contains single-paragraph unordered lists with two space after the marker.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "bad_spacing_ul_double.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md007",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + f"{source_path}:2:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + f"{source_path}:5:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_double_config_1_2():
    """
    Test to make sure this rule does trigger with a document that
    contains single-paragraph unordered lists with two space after the marker,
    and configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "bad_spacing_ul_double.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md007",
        "--set",
        "plugins.md030.ul_single=$#1",
        "--set",
        "plugins.md030.ul_multi=$#2",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + f"{source_path}:5:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_double_config_2_1():
    """
    Test to make sure this rule does trigger with a document that
    contains single-paragraph unordered lists with two space after the marker,
    and configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "bad_spacing_ul_double.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md007",
        "--set",
        "plugins.md030.ul_single=$#2",
        "--set",
        "plugins.md030.ul_multi=$#1",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_good_spacing_ul_single_nested():
    """
    Test to make sure this rule does not trigger with a document that
    contains nested unordered lists with one space after the marker,
    single-paragraph and double-paragraph lists.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "good_spacing_ul_single_nested.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
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
def test_md030_bad_spacing_ul_single_nested():
    """
    Test to make sure this rule does trigger with a document that
    contains nested unordered lists with two space after the marker,
    single-paragraph and double-paragraph lists.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "bad_spacing_ul_single_nested.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md007",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + f"{source_path}:2:4: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + f"{source_path}:3:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_good_spacing_ul_single_nested_double():
    """
    Test to make sure this rule does not trigger with a document that
    contains nested unordered lists with one space after the marker,
    single-paragraph and nested double-paragraph lists.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "good_spacing_ul_single_nested_double.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
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
def test_md030_good_spacing_ul_single_nested_double_2_1():
    """
    Test to make sure this rule does not trigger with a document that
    contains nested unordered lists with one space after the marker,
    single-paragraph and nested double-paragraph lists.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "good_spacing_ul_single_nested_double.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#2",
        "--set",
        "plugins.md030.ul_multi=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)\n"
        + f"{source_path}:7:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 2; Actual: 1] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_single_nested_double():
    """
    Test to make sure this rule does trigger with a document that
    contains nested unordered lists with two space after the marker,
    single-paragraph and nested double-paragraph lists.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "bad_spacing_ul_single_nested_double.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md007",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + f"{source_path}:2:4: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)\n"
        + f"{source_path}:5:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md030_bad_spacing_ul_single_nested_double_2_1():
    """
    Test to make sure this rule does trigger with a document that
    contains nested unordered lists with two space after the marker,
    single-paragraph and nested double-paragraph lists.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md030", "bad_spacing_ul_single_nested_double.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md030.ul_single=$#2",
        "--set",
        "plugins.md030.ul_multi=$#1",
        "--strict-config",
        "--disable-rules",
        "md007",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD030: Spaces after list markers "
        + "[Expected: 1; Actual: 2] (list-marker-space)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
