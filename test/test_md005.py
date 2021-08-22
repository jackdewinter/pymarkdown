"""
Module to provide tests related to the MD005 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md005_good_unordered_list_single_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/good_unordered_list_single_level.md",
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
def test_md005_bad_unordered_list_single_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md007",
        "scan",
        "test/resources/rules/md005/bad_unordered_list_single_level.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_unordered_list_single_level.md:2:2: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 0; Actual: 1] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_good_unordered_list_double_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md032",
        "scan",
        "test/resources/rules/md005/good_unordered_list_double_level.md",
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
def test_md005_bad_unordered_list_double_level_bad_first():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md032,md007",
        "scan",
        "test/resources/rules/md005/bad_unordered_list_double_level_bad_first.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_unordered_list_double_level_bad_first.md:4:2: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 0; Actual: 1] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_bad_unordered_list_double_level_bad_second():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md032,md007",
        "scan",
        "test/resources/rules/md005/bad_unordered_list_double_level_bad_second.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_unordered_list_double_level_bad_second.md:6:4: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 2; Actual: 3] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_good_unordered_list_separate_lists():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md007",
        "scan",
        "test/resources/rules/md005/good_unordered_list_separate_lists.md",
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
def test_md005_good_ordered_list_single_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/good_ordered_list_single_level.md",
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
def test_md005_bad_ordered_list_single_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/bad_ordered_list_single_level.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_single_level.md:2:2: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 0; Actual: 1] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_good_ordered_list_single_level_widths():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/good_ordered_list_single_level_widths.md",
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
def test_md005_bad_ordered_list_single_level_widths():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/bad_ordered_list_single_level_widths.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_single_level_widths.md:2:2: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 0; Actual: 1] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_good_ordered_list_single_level_widths_right():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/good_ordered_list_single_level_widths_right.md",
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
def test_md005_bad_ordered_list_single_level_widths_right():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/bad_ordered_list_single_level_widths_right.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_single_level_widths_right.md:2:1: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 3; Actual: 0] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_good_ordered_list_single_level_short_widths_right():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/good_ordered_list_single_level_short_widths_right.md",
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
def test_md005_good_ordered_list_seperate_single_level_short_widths_right():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/good_ordered_list_seperate_single_level_short_widths_right.md",
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
def test_md005_good_ordered_list_seperate_single_level_short_widths():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/good_ordered_list_seperate_single_level_short_widths.md",
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
def test_md005_good_ordered_list_double_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md032",
        "scan",
        "test/resources/rules/md005/good_ordered_list_double_level.md",
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
@pytest.mark.skip
def test_md005_good_ordered_list_double_level_right():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/good_ordered_list_double_level_right.md",
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
@pytest.mark.skip
def test_md005_bad_ordered_list_double_level_weirdx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/bad_ordered_list_double_level_weird.md",
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


@pytest.mark.skip
@pytest.mark.rules
def test_md005_bad_ordered_list_double_level_weirder():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md005 directory that has...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/bad_ordered_list_double_level_weirder.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_double_level_weirder.md:3:3: "
        + "MD005: Inconsistent indentation for list items at the same level [Expected: 3; Actual: 7] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
