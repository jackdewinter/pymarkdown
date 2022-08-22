"""
Module to provide tests related to the MD029 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md029_bad_configuration_style():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with an integer that is not a string.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_one_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md029.style' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_bad_configuration_style_invalid():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with a string that is not valid.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_one_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=not-matching",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md029.style' is not valid: Allowable values: ['one', 'ordered', 'zero', 'one_or_ordered']"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_one_list():
    """
    Test to make sure this rule does not trigger with a document that
    contains ordered lists that only have number 1.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_one_list.md"
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
def test_md029_bad_one_one_three_list():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have numbers 1 and 3.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "bad_one_one_three_list.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 1; Actual: 3; Style: 1/1/1] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_bad_one_two_one_list():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have numbers 1 and 2.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "bad_one_two_one_list.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 3; Actual: 1; Style: 1/2/3] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_one_two_three_list():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have numbers 1, 2, and 3.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_one_two_three_list.md"
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
def test_md029_bad_two_three_four_list():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have numbers 2 to 4.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "bad_two_three_four_list.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 1; Actual: 2; Style: 1/2/3] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_zero_one_two_three_list():
    """
    Test to make sure this rule does not trigger with a document that
    contains ordered lists that have numbers 0 to 3.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_zero_one_two_three_list.md"
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
def test_md029_good_zero_list():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that only have number 0.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_zero_list.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 1; Actual: 0; Style: 1/2/3] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_one_list_with_config_one():
    """
    Test to make sure this rule does not trigger with a document that
    contains ordered lists that only have number 1 and matching configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_one_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=one",
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
def test_md029_bad_one_one_three_list_with_config_one():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 3 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "bad_one_one_three_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=one",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 1; Actual: 3; Style: 1/1/1] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_bad_one_two_one_list_with_config_one():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 2 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "bad_one_two_one_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=one",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 1; Actual: 2; Style: 1/1/1] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_one_two_three_list_with_config_one():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1, 2, 3 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_one_two_three_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=one",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 1; Actual: 2; Style: 1/1/1] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_bad_two_three_four_list_with_config_one():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 2 to 4 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "bad_two_three_four_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=one",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 1; Actual: 2; Style: 1/1/1] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_zero_one_two_list_with_config_one():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 0 to 2 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_zero_one_two_three_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=one",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 1; Actual: 0; Style: 1/1/1] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_zero_list_with_config_one():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have only number 0 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_zero_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=one",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 1; Actual: 0; Style: 1/1/1] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_one_list_with_config_ordered():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and `ordered` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_one_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=ordered",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 2; Actual: 1; Style: 1/2/3] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_bad_one_one_three_list_with_config_ordered():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 3 and `ordered` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "bad_one_one_three_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=ordered",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 2; Actual: 1; Style: 1/2/3] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_bad_one_two_one_list_with_config_ordered():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 2 and `ordered` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "bad_one_two_one_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=ordered",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 3; Actual: 1; Style: 1/2/3] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_one_two_three_list_with_config_ordered():
    """
    Test to make sure this rule does not trigger with a document that
    contains ordered lists that have number 1 to 3 and `ordered` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_one_two_three_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=ordered",
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
def test_md029_bad_two_three_four_list_with_config_ordered():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 2 to 4 and `ordered` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "bad_two_three_four_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=ordered",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 1; Actual: 2; Style: 1/2/3] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_zero_one_two_list_with_config_ordered():
    """
    Test to make sure this rule does not trigger with a document that
    contains ordered lists that have number 0 to 3 and `ordered` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_zero_one_two_three_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=ordered",
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
def test_md029_good_zero_list_with_config_ordered():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 0 and `ordered` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_zero_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=ordered",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 1; Actual: 0; Style: 1/2/3] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_one_list_with_config_zero():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and `zero` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_one_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=zero",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_bad_one_one_three_list_with_config_zero():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 3 and `zero` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "bad_one_one_three_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=zero",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_bad_one_two_one_list_with_config_zero():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 2 and `zero` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "bad_one_two_one_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=zero",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_one_two_three_list_with_config_zero():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 to 3 and `zero` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_one_two_three_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=zero",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_bad_two_three_four_list_with_config_zero():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 2 to 4 and `zero` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "bad_two_three_four_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=zero",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 0; Actual: 2; Style: 0/0/0] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_zero_one_two_list_with_config_zero():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 0 to 2 and `zero` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_zero_one_two_three_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=zero",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD029: Ordered list item prefix "
        + "[Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md029_good_zero_list_with_config_zero():
    """
    Test to make sure this rule does not trigger with a document that
    contains ordered lists that have number 0 and `zero` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md029", "good_zero_list.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md029.style=zero",
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
