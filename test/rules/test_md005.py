"""
Module to provide tests related to the MD005 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import (
    assert_file_is_as_expected,
    copy_to_temp_file,
    create_temporary_configuration_file,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md005") + os.sep


@pytest.mark.rules
def test_md005_good_unordered_list_single_level():
    """
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists with no indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md005", "good_unordered_list_single_level.md"
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
def test_md005_bad_unordered_list_single_level():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists with 1 indent before the second list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md005", "bad_unordered_list_single_level.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md007,md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:2: "
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
def test_md005_bad_unordered_list_single_level_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_unordered_list_single_level.md"
    ) as temp_source_path:
        original_file_contents = """* Item 1
 * Item 2
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--stack-trace",
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """* Item 1
* Item 2
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_good_unordered_list_double_level():
    """
    Test to make sure this rule does not trigger with a document that
    is level 1 and 2 unordered lists, both with consistent left-aligned
    indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md005", "good_unordered_list_double_level.md"
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
def test_md005_bad_unordered_list_double_level_bad_first():
    """
    Test to make sure this rule does trigger with a document that
    is has level 1 and 2 unordered lists with inconsistent indentation
    at the first level.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "bad_unordered_list_double_level_bad_first.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md007,md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:2: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 0; Actual: 1] (list-indent)\n"
        + f"{source_path}:5:4: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 2; Actual: 3] (list-indent)\n"
        + f"{source_path}:6:4: "
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
def test_md005_bad_unordered_list_double_level_bad_first_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_unordered_list_double_level_bad_first.md"
    ) as temp_source_path:
        original_file_contents = """* Item 1
  * Item 1a
  * Item 1b
 * Item 2
   * Item 2a
   * Item 2b
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """* Item 1
  * Item 1a
  * Item 1b
* Item 2
  * Item 2a
  * Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_unordered_list_double_level_bad_second():
    """
    Test to make sure this rule does trigger with a document that
    is has level 1 and 2 unordered lists with inconsistent indentation
    at the second level.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "bad_unordered_list_double_level_bad_second.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md007,md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:6:4: "
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
def test_md005_bad_unordered_list_double_level_bad_second_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_unordered_list_double_level_bad_second.md"
    ) as temp_source_path:
        original_file_contents = """* Item 1
  * Item 1a
  * Item 1b
* Item 2
  * Item 2a
   * Item 2b
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """* Item 1
  * Item 1a
  * Item 1b
* Item 2
  * Item 2a
  * Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_good_unordered_list_separate_lists():
    """
    Test to make sure this rule does not trigger with a document that
    has level 1 and 2 unordered lists with consistent indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md005", "good_unordered_list_separate_lists.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md007,md029",
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
def test_md005_bad_unordered_list_single_level_twice():
    """
    Test to make sure this rule does trigger with a document that
    has multiple level 1 unordered lists with inconsistent indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "bad_unordered_list_single_level_twice.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md007,md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:2: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 0; Actual: 1] (list-indent)\n"
        + f"{source_path}:3:2: "
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
def test_md005_bad_unordered_list_single_level_twice_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_unordered_list_single_level_twice.md"
    ) as temp_source_path:
        original_file_contents = """* Item 1
 * Item 2
 * Item 2
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """* Item 1
* Item 2
* Item 2
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_good_ordered_list_single_level():
    """
    Test to make sure this rule does not trigger with a document that
    has level 1 ordered lists with consistent indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md005", "good_ordered_list_single_level.md"
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
def test_md005_bad_ordered_list_single_level_x():
    """
    Test to make sure this rule does trigger with a document that
    has level 1 ordered lists with inconsistent indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md005", "bad_ordered_list_single_level.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:2: "
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
def test_md005_bad_ordered_list_single_level_x_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_ordered_list_single_level.md"
    ) as temp_source_path:
        original_file_contents = """1. Item 1
 1. Item 2
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
1. Item 2
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_good_ordered_list_single_level_widths():
    """
    Test to make sure this rule does not trigger with a document that
    has level 1 ordered lists with consistent indentation with either
    left or right alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "good_ordered_list_single_level_widths.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
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
def test_md005_bad_ordered_list_single_level_widths():
    """
    Test to make sure this rule does trigger with a document that
    has level 1 ordered lists with inconsistent indentation with either
    left alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md005", "bad_ordered_list_single_level_widths.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:2: "
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
def test_md005_bad_ordered_list_single_level_widths_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_ordered_list_single_level.md"
    ) as temp_source_path:
        original_file_contents = """1. Item 1
 1. Item 2
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
1. Item 2
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_good_ordered_list_single_level_widths_right():
    """
    Test to make sure this rule does not trigger with a document that
    has level 1 ordered lists with consistent indentation and right alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "good_ordered_list_single_level_widths_right.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
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
def test_md005_bad_ordered_list_single_level_widths_right():
    """
    Test to make sure this rule does trigger with a document that
    has level 1 ordered lists with inconsistent indentation with either
    right alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "bad_ordered_list_single_level_widths_right.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
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
def test_md005_bad_ordered_list_single_level_widths_right_fix():
    """
    Test to make sure this rule does trigger with a document that
    has level 1 ordered lists with inconsistent indentation with either
    right alignment.

    Note that the first line does not start a right aligned list as it is
    way too out of sync with line 2.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_ordered_list_single_level_widths_right.md"
    ) as temp_source_path:
        original_file_contents = """   1. Item 1
10. Item 2
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """   1. Item 1
   10. Item 2
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_good_ordered_list_single_level_short_widths_right():
    """
    Test to make sure this rule does not trigger with a document that
    has level 1 ordered lists with consistent indentation and right alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "good_ordered_list_single_level_short_widths_right.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
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
def test_md005_good_ordered_list_separate_single_level_short_widths_right():
    """
    Test to make sure this rule does not trigger with a document that
    has two level 1 ordered lists with consistent indentation and right alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "good_ordered_list_seperate_single_level_short_widths_right.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
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
def test_md005_good_ordered_list_separate_single_level_short_widths():
    """
    Test to make sure this rule does not trigger with a document that
    has two level 1 ordered lists with consistent indentation and left alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "good_ordered_list_seperate_single_level_short_widths.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md029,md030",
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
def test_md005_good_ordered_list_double_level():
    """
    Test to make sure this rule does not trigger with a document that
    has two level 1 ordered lists with consistent indentation and left alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md005", "good_ordered_list_double_level.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
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
def test_md005_good_ordered_list_double_level_right():
    """
    Test to make sure this rule does not trigger with a document that
    has two level 1 ordered lists with consistent indentation and right alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md005", "good_ordered_list_double_level_right.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
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
def test_md005_bad_ordered_list_double_level_weirdx():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with consistent indentation and weird alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md005", "bad_ordered_list_double_level_weird.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:5: "
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
def test_md005_bad_ordered_list_double_level_weirdx_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_ordered_list_double_level_weird.md"
    ) as temp_source_path:
        original_file_contents = """1. Item 1
   1. Item 1a
    100. Item 1b
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
   1. Item 1a
   100. Item 1b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_list_double_level_weirder():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with consistent indentation and weirder alignment.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "bad_ordered_list_double_level_weirder.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
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
def test_md005_bad_ordered_list_double_level_weirder_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_ordered_list_double_level_weirder.md"
    ) as temp_source_path:
        original_file_contents = """1. Item 1
   1. Item 1a
  100. Item 1b
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
   1. Item 1a
100. Item 1b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_good_unordered_list_double_level_in_block_quote():
    """
    Test to make sure this rule does not trigger with a document that
    has level 1 and 2 unordered lists with consistent indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "good_unordered_list_double_level_in_block_quote.md",
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
def test_md005_good_unordered_list_double_level_in_block_quote_first():
    """
    Test to make sure this rule does not trigger with a document that
    has level 1 and 2 unordered lists with consistent indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "bad_unordered_list_double_level_in_block_quote_first.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md007,md027,md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:4: "
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
def test_md005_good_unordered_list_double_level_in_block_quote_second():
    """
    Test to make sure this rule does not trigger with a document that
    has level 1 and 2 unordered lists with consistent indentation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "bad_unordered_list_double_level_in_block_quote_second.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md007,md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:6: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 4; Actual: 5] (list-indent)\n"
        + f"{source_path}:6:6: "
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
def test_md005_bad_ordered_list_double_level_left():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with left alignment and bad indentation
    on the second list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md005", "bad_ordered_list_double_level_left.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:5: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 3; Actual: 4] (list-indent)\n"
        + f"{source_path}:6:5: "
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
def test_md005_bad_ordered_list_double_level_left_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_ordered_list_double_level_left.md"
    ) as temp_source_path:
        original_file_contents = """1. Item 1
   1. Item 1a
   10. Item 1b
2. Item 2
    1. Item 2a
    10. Item 2b
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            # "--stack-trace",
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
   1. Item 1a
   10. Item 1b
2. Item 2
   1. Item 2a
   10. Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_list_double_level_right_x():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with right alignment and bad indentation
    on the second list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md005", "bad_ordered_list_double_level_right.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:6: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 4; Actual: 5] (list-indent)\n"
        + f"{source_path}:6:5: "
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
def test_md005_bad_ordered_list_double_level_right_x_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_ordered_list_double_level_right.md"
    ) as temp_source_path:
        original_file_contents = """1. Item 1
    1. Item 1a
   10. Item 1b
2. Item 2
     1. Item 2a
    10. Item 2b
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
    1. Item 1a
   10. Item 1b
2. Item 2
    1. Item 2a
   10. Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_list_double_level_left_then_right():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with left alignment on the first list
    and right alignment on the second list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "bad_ordered_list_double_level_left_then_right.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:5: "
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
def test_md005_bad_ordered_list_double_level_left_then_right_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_ordered_list_double_level_left_then_right.md"
    ) as temp_source_path:
        original_file_contents = """1. Item 1
   1. Item 1a
   10. Item 1b
2. Item 2
    1. Item 2a
   10. Item 2b
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
   1. Item 1a
   10. Item 1b
2. Item 2
   1. Item 2a
   10. Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_list_double_level_right_then_left():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with right alignment on the first list
    and left alignment on the second list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "bad_ordered_list_double_level_right_then_left.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:4: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 4; Actual: 3] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_bad_ordered_list_double_level_right_then_left_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_ordered_list_double_level_right_then_left.md"
    ) as temp_source_path:
        original_file_contents = """1. Item 1
    1. Item 1a
   10. Item 1b
2. Item 2
   1. Item 2a
   10. Item 2b
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
    1. Item 1a
   10. Item 1b
2. Item 2
    1. Item 2a
   10. Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_list_single_level_left_then_right():
    """
    Test to make sure this rule does trigger with a document that
    has a single level 1 ordered list with left alignment on the first
    two list items and right alignment on the third item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "bad_ordered_list_single_level_left_then_right.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:2: "
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
def test_md005_bad_ordered_list_single_level_left_then_right_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_ordered_list_single_level_left_then_right.md"
    ) as temp_source_path:
        original_file_contents = """1. Item 1
10. Item 2
 2. Item 3
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
10. Item 2
2. Item 3
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_list_single_level_right_then_left():
    """
    Test to make sure this rule does trigger with a document that
    has a single level 1 ordered list with right alignment on the first
    two list items and left alignment on the third item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md005",
        "bad_ordered_list_single_level_right_then_left.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md029",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:1: "
        + "MD005: Inconsistent indentation for list items at the same level "
        + "[Expected: 1; Actual: 0] (list-indent)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md005_bad_ordered_list_single_level_right_then_left_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_ordered_list_single_level_right_then_left.md"
    ) as temp_source_path:
        original_file_contents = """ 1. Item 1
10. Item 2
2. Item 3
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ 1. Item 1
10. Item 2
 2. Item 3
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_left_unordered_x():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with right alignment and bad indentation
    on the second list.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """1. Item 1
   + Item 1a
   + Item 1b
 10. Item 2
     + Item 2a
     + Item 2b
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md029,md007",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = """{path}:4:2: MD005: Inconsistent indentation for list items at the same level [Expected: 0; Actual: 1] (list-indent)
{path}:5:6: MD005: Inconsistent indentation for list items at the same level [Expected: 3; Actual: 5] (list-indent)
{path}:6:6: MD005: Inconsistent indentation for list items at the same level [Expected: 3; Actual: 5] (list-indent)
""".replace(
            "{path}", temp_source_path
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md005_bad_ordered_left_unordered_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """1. Item 1
   + Item 1a
   + Item 1b
 10. Item 2
     + Item 2a
     + Item 2b
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--stack-trace",
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
   + Item 1a
   + Item 1b
10. Item 2
    + Item 2a
    + Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_right_unordered_x():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with right alignment and bad indentation
    on the second list.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """ 1. Item 1
    + Item 1a
    + Item 1b
 10. Item 2
     + Item 2a
     + Item 2b
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md029,md007",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = """{path}:5:6: MD005: Inconsistent indentation for list items at the same level [Expected: 4; Actual: 5] (list-indent)
{path}:6:6: MD005: Inconsistent indentation for list items at the same level [Expected: 4; Actual: 5] (list-indent)
""".replace(
            "{path}", temp_source_path
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
@pytest.mark.skip
def test_md005_bad_ordered_right_unordered_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """ 1. Item 1
    + Item 1a
    + Item 1b
 10. Item 2
     + Item 2a
     + Item 2b
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ 1. Item 1
    + Item 1a
    + Item 1b
 10. Item 2
     + Item 2a
     + Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_unordered_ordered_left_x():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with right alignment and bad indentation
    on the second list.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """+ Item 1
   1. Item 1a
   10. Item 1b
 + Item 2
    1. Item 2a
    10. Item 2b
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md029,md007",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = """{path}:4:2: MD005: Inconsistent indentation for list items at the same level [Expected: 0; Actual: 1] (list-indent)
{path}:5:5: MD005: Inconsistent indentation for list items at the same level [Expected: 3; Actual: 4] (list-indent)
{path}:6:5: MD005: Inconsistent indentation for list items at the same level [Expected: 3; Actual: 4] (list-indent)
""".replace(
            "{path}", temp_source_path
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md005_bad_unordered_ordered_left_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """+ Item 1
  1. Item 1a
  10. Item 1b
 + Item 2
    1. Item 2a
    10. Item 2b
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """+ Item 1
  1. Item 1a
  10. Item 1b
+ Item 2
  1. Item 2a
  10. Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_unordered_ordered_right_x():
    """
    Test to make sure this rule does trigger with a document that
    has two level 1 ordered lists with right alignment and bad indentation
    on the second list.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """+ Item 1
   1. Item 1a
   10. Item 1b
 + Item 2
     1. Item 2a
    10. Item 2b
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md029,md007",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = """{path}:4:2: MD005: Inconsistent indentation for list items at the same level [Expected: 0; Actual: 1] (list-indent)
{path}:5:6: MD005: Inconsistent indentation for list items at the same level [Expected: 3; Actual: 5] (list-indent)
{path}:6:5: MD005: Inconsistent indentation for list items at the same level [Expected: 3; Actual: 4] (list-indent)
""".replace(
            "{path}", temp_source_path
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
@pytest.mark.skip
def test_md005_bad_unordered_ordered_right_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """+ Item 1
  1. Item 1a
  10. Item 1b
 + Item 2
     1. Item 2a
    10. Item 2b
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """+ Item 1
  1. Item 1a
  10. Item 1b
+ Item 2
   1. Item 2a
  10. Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_unordered_lt_with_text_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """+ Item 1
  more Item 1
 + Item 2
   more Item 2
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--stack-trace",
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """+ Item 1
  more Item 1
+ Item 2
  more Item 2
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_unordered_lt_with_double_text_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """+ Item 1
  more Item 1
 + Item 2
   more Item 2
 + Item 3
   more Item 3
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--stack-trace",
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """+ Item 1
  more Item 1
+ Item 2
  more Item 2
+ Item 3
  more Item 3
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_unordered_lt_with_text_nested_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """+ Item 1
  more Item 1
   + Item 1a
     more Item 1a
   + Item 1b
     more Item 1b
 + Item 2
   more Item 2
    + Item 2a
      more Item 2a
    + Item 2b
      more Item 2b
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """+ Item 1
  more Item 1
   + Item 1a
     more Item 1a
   + Item 1b
     more Item 1b
+ Item 2
  more Item 2
   + Item 2a
     more Item 2a
   + Item 2b
     more Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_unordered_gt_with_text_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """  + Item 1
    more Item 1
 + Item 2
   more Item 2
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """  + Item 1
    more Item 1
  + Item 2
    more Item 2
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_unordered_gt_with_double_text_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """  + Item 1
    more Item 1
 + Item 2
   more Item 2
 + Item 3
   more Item 3
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """  + Item 1
    more Item 1
  + Item 2
    more Item 2
  + Item 3
    more Item 3
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_unordered_gt_with_text_nested_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """+ Item 1
  more Item 1
    + Item 1a
      more Item 1a
    + Item 1b
      more Item 1b
 + Item 2
   more Item 2
   + Item 2a
     more Item 2a
   + Item 2b
     more Item 2b
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """+ Item 1
  more Item 1
    + Item 1a
      more Item 1a
    + Item 1b
      more Item 1b
+ Item 2
  more Item 2
    + Item 2a
      more Item 2a
    + Item 2b
      more Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_lt_with_text_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """1. Item 1
   more Item 1
 1. Item 2
    more Item 2
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--stack-trace",
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
   more Item 1
1. Item 2
   more Item 2
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_lt_with_double_text_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """1. Item 1
   more Item 1
 2. Item 2
    more Item 2
 3. Item 3
    more Item 3
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--stack-trace",
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
   more Item 1
2. Item 2
   more Item 2
3. Item 3
   more Item 3
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_lt_with_double_text_with_raw_html_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """1. Item 1
   more Item 1
 2. Item 2 <b2
    data="foo" > and inline HTML
 3. Item 3
    more Item 3
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--stack-trace",
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
   more Item 1
2. Item 2 <b2
   data="foo" > and inline HTML
3. Item 3
   more Item 3
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_lt_with_text_nested_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """1. Item 1
   more Item 1
    1. Item 1a
       more Item 1a
    2. Item 1b
       more Item 1b
 2. Item 2
    more Item 2
     1. Item 2a
        more Item 2a
     2. Item 2b
        more Item 2b
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--stack-trace",
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
   more Item 1
    1. Item 1a
       more Item 1a
    2. Item 1b
       more Item 1b
2. Item 2
   more Item 2
    1. Item 2a
       more Item 2a
    2. Item 2b
       more Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_gt_with_text_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """  1. Item 1
     more Item 1
 2. Item 2
    more Item 2
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """  1. Item 1
     more Item 1
  2. Item 2
     more Item 2
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_gt_with_double_text_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """  1. Item 1
     more Item 1
 2. Item 2
    more Item 2
 2. Item 3
    more Item 3
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """  1. Item 1
     more Item 1
  2. Item 2
     more Item 2
  2. Item 3
     more Item 3
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md005_bad_ordered_gt_with_text_nested_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """1. Item 1
   more Item 1
     1. Item 1a
        more Item 1a
     2. Item 1b
        more Item 1b
 2. Item 2
    more Item 2
    1. Item 2a
       more Item 2a
    2. Item 2b
       more Item 2b
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Item 1
   more Item 1
     1. Item 1a
        more Item 1a
     2. Item 1b
        more Item 1b
2. Item 2
   more Item 2
     1. Item 2a
        more Item 2a
     2. Item 2b
        more Item 2b
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)
