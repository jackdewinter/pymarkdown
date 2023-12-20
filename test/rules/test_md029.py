"""
Module to provide tests related to the MD029 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import (
    assert_file_is_as_expected,
    copy_to_temp_file,
    create_temporary_configuration_file,
)

import pytest

# pylint: disable=too-many-lines

source_path = os.path.join("test", "resources", "rules", "md029") + os.sep


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
def test_md029_bad_one_one_three_list_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have numbers 1 and 3.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_one_one_three_list.md"
    ) as temp_source_path:
        original_file_contents = """1. Simple
1. One
3. List
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Simple
1. One
1. List
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


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
def test_md029_bad_one_two_one_list_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have numbers 1 and 2.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(source_path + "bad_one_two_one_list.md") as temp_source_path:
        original_file_contents = """1. Simple
2. One
1. List
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Simple
2. One
3. List
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


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
def test_md029_bad_two_three_four_list_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have numbers 1 and 2.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_two_three_four_list.md"
    ) as temp_source_path:
        original_file_contents = """2. Simple
3. One
4. List
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Simple
2. One
3. List
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md029_bad_nested_lists_1_with_no_config():
    """
    Test to make sure this rule does trigger...
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """2. first
   1. first-first
   1. first-second
   2. first-third
3. second
   1. second-first
   2. second-second
   2. second-third
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--strict-config",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = """{path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/2/3] (ol-prefix)
{path}:4:4: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/1/1] (ol-prefix)
{path}:8:4: MD029: Ordered list item prefix [Expected: 3; Actual: 2; Style: 1/2/3] (ol-prefix)""".replace(
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
def test_md029_bad_nested_lists_1_with_no_config_fix():
    """
    Test to make sure this rule does trigger
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """2. first
   1. first-first
   1. first-second
3. second
   1. second-first
   2. second-second
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. first
   1. first-first
   1. first-second
2. second
   1. second-first
   2. second-second
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md029_bad_nested_lists_2_with_no_config():
    """
    Test to make sure this rule does trigger...
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """0. first
   1. first-first
   31. first-second
3. second
   1. second-first
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--strict-config",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = """{path}:3:4: MD029: Ordered list item prefix [Expected: 2; Actual: 31; Style: 1/2/3] (ol-prefix)
{path}:4:1: MD029: Ordered list item prefix [Expected: 1; Actual: 3; Style: 1/2/3] (ol-prefix)""".replace(
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
def test_md029_bad_nested_lists_2_with_no_config_fix():
    """
    Test to make sure this rule does trigger
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """0. first
   1. first-first
   31. first-second
3. second
   1. second-first
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """0. first
   1. first-first
   2.  first-second
1. second
   1. second-first
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md029_good_nested_lists_3_with_no_config():
    """
    Test to make sure this rule does trigger...
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """1. First Line
1. Second Line

text to break up lists

1. First Item
2. Second Item
3. Third Item
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--strict-config",
            "scan",
            temp_source_path,
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
def test_md029_bad__lists_1_with_no_config():
    """
    Test to make sure this rule does trigger...
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """3. first
3. second
3. third
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--strict-config",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = """{path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 3; Style: 1/2/3] (ol-prefix)""".replace(
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
def test_md029_bad__lists_1_with_no_config_fix():
    """
    Test to make sure this rule does trigger
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """3. first
3. second
3. third
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. first
2. second
3. third
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


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
def test_md029_bad_one_one_three_list_with_config_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 3 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_one_one_three_list.md"
    ) as temp_source_path:
        original_file_contents = """1. Simple
1. One
3. List
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md029.style=one",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Simple
1. One
1. List
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


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
def test_md029_bad_one_two_one_list_with_config_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 3 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(source_path + "bad_one_two_one_list.md") as temp_source_path:
        original_file_contents = """1. Simple
2. One
1. List
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md029.style=one",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Simple
1. One
1. List
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


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
def test_md029_bad_two_three_four_list_with_config_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 3 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_two_three_four_list.md"
    ) as temp_source_path:
        original_file_contents = """2. Simple
3. One
4. List
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md029.style=one",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Simple
1. One
1. List
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md029_bad_nested_lists_with_config_one():
    """
    Test to make sure this rule does trigger...
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """2. first
   1. first-first
   2. first-second
3. second
   1. second-first
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--set",
            "plugins.md029.style=one",
            "--strict-config",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = """{path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/1/1] (ol-prefix)
{path}:3:4: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/1/1] (ol-prefix)""".replace(
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
def test_md029_bad_nested_lists_with_config_one_fix():
    """
    Test to make sure this rule does trigger
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """2. first
   1. first-first
   2. first-second
3. second
   1. second-first
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md029.style=one",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. first
   1. first-first
   1. first-second
1. second
   1. second-first
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


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
def test_md029_bad_one_one_three_list_with_config_ordered_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 3 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_one_one_three_list.md"
    ) as temp_source_path:
        original_file_contents = """1. Simple
1. One
3. List
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md029.style=ordered",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Simple
2. One
3. List
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


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
def test_md029_bad_one_two_one_list_with_config_ordered_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 3 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(source_path + "bad_one_two_one_list.md") as temp_source_path:
        original_file_contents = """1. Simple
2. One
1. List
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md029.style=ordered",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Simple
2. One
3. List
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


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
def test_md029_bad_two_three_four_list_with_config_ordered_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 3 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_two_three_four_list.md"
    ) as temp_source_path:
        original_file_contents = """2. Simple
3. One
4. List
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md029.style=ordered",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Simple
2. One
3. List
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md029_bad_nested_lists_with_config_ordered():
    """
    Test to make sure this rule does trigger...
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """2. first
   1. first-first
   1. first-second
3. second
   1. second-first
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--set",
            "plugins.md029.style=ordered",
            "--strict-config",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = """{path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/2/3] (ol-prefix)
{path}:3:4: MD029: Ordered list item prefix [Expected: 2; Actual: 1; Style: 1/2/3] (ol-prefix)""".replace(
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
def test_md029_bad_nested_lists_with_config_ordered_fix():
    """
    Test to make sure this rule does trigger
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """2. first
   1. first-first
   1. first-second
3. second
   1. second-first
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md029.style=ordered",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. first
   1. first-first
   2. first-second
2. second
   1. second-first
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


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
def test_md029_bad_one_one_three_list_with_config_zero_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 3 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_one_one_three_list.md"
    ) as temp_source_path:
        original_file_contents = """1. Simple
1. One
3. List
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md029.style=zero",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """0. Simple
0. One
0. List
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


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
def test_md029_bad_one_two_one_list_with_config_zero_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 3 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(source_path + "bad_one_two_one_list.md") as temp_source_path:
        original_file_contents = """1. Simple
2. One
1. List
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md029.style=zero",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """0. Simple
0. One
0. List
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


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
def test_md029_bad_two_three_four_list_with_config_zero_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains ordered lists that have number 1 and 3 and `one` configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_two_three_four_list.md"
    ) as temp_source_path:
        original_file_contents = """2. Simple
3. One
4. List
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md029.style=zero",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """0. Simple
0. One
0. List
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md029_bad_nested_lists_with_config_zero():
    """
    Test to make sure this rule does trigger...
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """2. first
   1. first-first
   2. first-second
3. second
   1. second-first
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--set",
            "plugins.md029.style=zero",
            "--strict-config",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = """{path}:1:1: MD029: Ordered list item prefix [Expected: 0; Actual: 2; Style: 0/0/0] (ol-prefix)
{path}:2:4: MD029: Ordered list item prefix [Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)
{path}:5:4: MD029: Ordered list item prefix [Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)""".replace(
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
def test_md029_bad_nested_lists_with_config_zero_fix():
    """
    Test to make sure this rule does trigger
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """2. first
   1. first-first
   2. first-second
3. second
   1. second-first
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md029.style=zero",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """0. first
   0. first-first
   0. first-second
0. second
   0. second-first
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


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
