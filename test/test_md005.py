"""
Module to provide tests related to the MD005 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md005_good_unordered_list_single_level():
    """
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists with no indentation.
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
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists with 1 indent before the second list.
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
    Test to make sure this rule does not trigger with a document that
    is level 1 and 2 unordered lists, both with consistent left-aligned
    indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
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
    Test to make sure this rule does trigger with a document that
    is has level 1 and 2 unordered lists with inconsistent indentation
    at the first level.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md007",
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
    Test to make sure this rule does trigger with a document that
    is has level 1 and 2 unordered lists with inconsistent indentation
    at the second level.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md007",
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
    Test to make sure this rule does not trigger with a document that
    has level 1 and 2 unordered lists with consistent indentation.
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
def test_md005_bad_unordered_list_single_level_twice():
    """
    Test to make sure this rule does trigger with a document that
    has multiple level 1 unordered lists with inconsistent indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md007",
        "scan",
        "test/resources/rules/md005/bad_unordered_list_single_level_twice.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_unordered_list_single_level_twice.md:2:2: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 0; Actual: 1] (list-indent)\n"
        + "test/resources/rules/md005/bad_unordered_list_single_level_twice.md:3:2: "
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
def test_md005_good_ordered_list_single_level():
    """
    Test to make sure this rule does not trigger with a document that
    has level 1 ordered lists with consistent indentation.
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
    Test to make sure this rule does trigger with a document that
    has level 1 ordered lists with inconsistent indentation.
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
        + "[Expected: 0; Actual: 2] (list-indent)"
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
    Test to make sure this rule does not trigger with a document that
    has level 1 ordered lists with consistent indentation with either
    left or right alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
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
    Test to make sure this rule does trigger with a document that
    has level 1 ordered lists with inconsistent indentation with either
    left alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        "test/resources/rules/md005/bad_ordered_list_single_level_widths.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_single_level_widths.md:2:2: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 0; Actual: 2] (list-indent)"
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
    Test to make sure this rule does not trigger with a document that
    has level 1 ordered lists with consistent indentation and right alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
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
    Test to make sure this rule does trigger with a document that
    has level 1 ordered lists with inconsistent indentation with either
    right alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        "test/resources/rules/md005/bad_ordered_list_single_level_widths_right.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_single_level_widths_right.md:2:1: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 3; Actual: 1] (list-indent)"
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
    Test to make sure this rule does not trigger with a document that
    has level 1 ordered lists with consistent indentation and right alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
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
def test_md005_good_ordered_list_separate_single_level_short_widths_right():
    """
    Test to make sure this rule does not trigger with a document that
    has two level 1 ordered lists with consistent indentation and right alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
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
def test_md005_good_ordered_list_separate_single_level_short_widths():
    """
    Test to make sure this rule does not trigger with a document that
    has two level 1 ordered lists with consistent indentation and left alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029,md030",
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
    Test to make sure this rule does not trigger with a document that
    has two level 1 ordered lists with consistent indentation and left alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
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
def test_md005_good_ordered_list_double_level_right():
    """
    Test to make sure this rule does not trigger with a document that
    has two level 1 ordered lists with consistent indentation and right alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
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
def test_md005_bad_ordered_list_double_level_weirdx():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with consistent indentation and weird alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        "test/resources/rules/md005/bad_ordered_list_double_level_weird.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_double_level_weird.md:3:5: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 3; Actual: 5] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_bad_ordered_list_double_level_weirder():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with consistent indentation and weirder alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--stack-trace",
        "--disable-rules",
        "md029",
        "scan",
        "test/resources/rules/md005/bad_ordered_list_double_level_weirder.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_double_level_weirder.md:3:3: "
        + "MD005: Inconsistent indentation for list items at the same level [Expected: 0; Actual: 3] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_good_unordered_list_double_level_in_block_quote():
    """
    Test to make sure this rule does not trigger with a document that
    has level 1 and 2 unordered lists with consistent indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md005/good_unordered_list_double_level_in_block_quote.md",
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
def test_md005_good_unordered_list_double_level_in_block_quote_first():
    """
    Test to make sure this rule does not trigger with a document that
    has level 1 and 2 unordered lists with consistent indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md007,md027",
        "scan",
        "test/resources/rules/md005/bad_unordered_list_double_level_in_block_quote_first.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_unordered_list_double_level_in_block_quote_first.md:4:4: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 2; Actual: 1] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_good_unordered_list_double_level_in_block_quote_second():
    """
    Test to make sure this rule does not trigger with a document that
    has level 1 and 2 unordered lists with consistent indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md007",
        "scan",
        "test/resources/rules/md005/bad_unordered_list_double_level_in_block_quote_second.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_unordered_list_double_level_in_block_quote_second.md:5:6: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 2; Actual: 3] (list-indent)\n"
        + "test/resources/rules/md005/bad_unordered_list_double_level_in_block_quote_second.md:6:6: "
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
def test_md005_bad_ordered_list_double_level_left():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with left alignment and bad indentation
    on the second list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        "test/resources/rules/md005/bad_ordered_list_double_level_left.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_double_level_left.md:5:5: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 4; Actual: 5] (list-indent)\n"
        + "test/resources/rules/md005/bad_ordered_list_double_level_left.md:6:5: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 4; Actual: 5] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_bad_ordered_list_double_level_right():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with right alignment and bad indentation
    on the second list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        "test/resources/rules/md005/bad_ordered_list_double_level_right.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_double_level_right.md:5:6: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 5; Actual: 6] (list-indent)\n"
        + "test/resources/rules/md005/bad_ordered_list_double_level_right.md:6:5: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 0; Actual: 5] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_bad_ordered_list_double_level_left_then_right():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with left alignment on the first list
    and right alignment on the second list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        "test/resources/rules/md005/bad_ordered_list_double_level_left_then_right.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_double_level_left_then_right.md:5:5: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 4; Actual: 5] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_bad_ordered_list_double_level_right_then_left():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with right alignment on the first list
    and left alignment on the second list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        "test/resources/rules/md005/bad_ordered_list_double_level_right_then_left.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_double_level_right_then_left.md:5:4: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 3; Actual: 4] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_bad_ordered_list_single_level_left_then_right():
    """
    Test to make sure this rule does trigger with a document that
    has a single level 1 ordered list with left alignment on the first
    two list items and right alignment on the third item.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        "test/resources/rules/md005/bad_ordered_list_single_level_left_then_right.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_single_level_left_then_right.md:3:2: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 0; Actual: 2] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_bad_ordered_list_single_level_right_then_left():
    """
    Test to make sure this rule does trigger with a document that
    has a single level 1 ordered list with right alignment on the first
    two list items and left alignment on the third item.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        "test/resources/rules/md005/bad_ordered_list_single_level_right_then_left.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md005/bad_ordered_list_single_level_right_then_left.md:3:1: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 1; Actual: 1] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
