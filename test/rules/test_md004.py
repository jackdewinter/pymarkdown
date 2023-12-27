"""
Module to provide tests related to the MD004 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import assert_file_is_as_expected, copy_to_temp_file

import pytest

source_path = os.path.join("test", "resources", "rules", "md004") + os.sep


@pytest.mark.rules
def test_md004_bad_configuration_style():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with a string that is not in the list of acceptable values.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_asterisk_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=bad",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md004.style' is not valid: Allowable values: ['consistent', 'asterisk', 'plus', 'dash', 'sublist']"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_good_asterisk_single_level():
    """
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with asterisk and the
    configuration is set to asterisk.

    This function shadows
    test_api_config_with_good_string_property
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_asterisk_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=asterisk",
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
def test_md004_good_asterisk_single_level_consistent():
    """
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with asterisk and the
    configuration is set to consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_asterisk_single_level.md"
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
def test_md004_bad_asterisk_dash_single_level():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_dash_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=asterisk",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: dash] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_asterisk_dash_single_level_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "good_list_dash_single_level.md"
    ) as temp_source_path:
        original_file_contents = """- first
- second
- third
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md004.style=asterisk",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """* first
* second
* third
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md004_bad_asterisk_plus_single_level():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with plus and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_plus_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=asterisk",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: plus] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_asterisk_plus_single_level_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "good_list_plus_single_level.md"
    ) as temp_source_path:
        original_file_contents = """+ first
+ second
+ third
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md004.style=asterisk",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """* first
* second
* third
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md004_good_dash_single_level():
    """
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to dash.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_dash_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=dash",
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
def test_md004_good_dash_single_level_consistent():
    """
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_dash_single_level.md"
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
def test_md004_bad_dash_asterisk_single_level():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with asterisks and the
    configuration is also set to dash.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_asterisk_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=dash",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: dash; Actual: asterisk] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_dash_asterisk_single_level_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "good_list_asterisk_single_level.md"
    ) as temp_source_path:
        original_file_contents = """* first
* second
* third
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md004.style=dash",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """- first
- second
- third
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md004_bad_dash_plus_single_level():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with plus and the
    configuration is also set to dash.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_plus_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=dash",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: dash; Actual: plus] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_dash_plus_single_level_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "good_list_plus_single_level.md"
    ) as temp_source_path:
        original_file_contents = """+ first
+ second
+ third
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md004.style=dash",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """- first
- second
- third
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md004_good_plus_single_level():
    """
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with plus and the
    configuration is also set to plus.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_plus_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=plus",
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
def test_md004_good_plus_single_level_consistent():
    """
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_plus_single_level.md"
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
def test_md004_bad_plus_asterisk_single_level():
    """
    Test to make sure this rule does not trigger with a document that
    is only level 1 unordered lists starting with asterisk and the
    configuration is also set to plus.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_asterisk_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=plus",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: plus; Actual: asterisk] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_good_plus_single_level_consistent_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "good_list_asterisk_single_level.md"
    ) as temp_source_path:
        original_file_contents = """* first
* second
* third
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md004.style=plus",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """+ first
+ second
+ third
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md004_bad_plus_dash_single_level():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to plus.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_dash_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=plus",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: plus; Actual: dash] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_plus_dash_single_level_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "good_list_dash_single_level.md"
    ) as temp_source_path:
        original_file_contents = """- first
- second
- third
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md004.style=plus",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """+ first
+ second
+ third
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md004_bad_single_level_consistent():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with each of the valid starts.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "bad_list_different_single_level.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md032",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: plus] (ul-style)\n"
        + f"{source_path}:3:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: dash] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_single_level_consistent_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_list_different_single_level.md"
    ) as temp_source_path:
        original_file_contents = """* first
+ second
- third
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

        expected_file_contents = """* first
* second
* third
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md004_good_multi_level_sublevel():
    """
    Test to make sure this rule does not trigger with a document that contains
    the three start characters, each on their own sublevel.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_multi_level_sublevel.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=sublist",
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
def test_md004_good_multi_level_sublevel_complex():
    """
    Variation of the previous test with a more complex list structure.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_multi_level_complex.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=sublist",
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
def test_md004_bad_multi_level_sublevel_complex():
    """
    Test to make sure this rule does trigger with a document that contains
    the inconsistent start characters at one specific sublevel.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "bad_multi_level_complex.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=sublist",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:6:6: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: dash; Actual: plus] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_multi_level_sublevel_complex_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_multi_level_complex.md"
    ) as temp_source_path:
        original_file_contents = """+ first
  1. second
     - third
+ first
  1. second
     + third
       1. fourth
          * fifth
     + third
       1. fourth
          * fifth
     + third
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md004.style=sublist",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """+ first
  1. second
     - third
+ first
  1. second
     - third
       1. fourth
          * fifth
     - third
       1. fourth
          * fifth
     - third
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md004_bad_multi_level_sublevel_complex_asterisk():
    """
    Test to make sure this rule does trigger with a document that contains
    the three start characters, each on their own sublevel, and configuration
    specifically set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "bad_multi_level_complex.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=asterisk",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: plus] (ul-style)\n"
        + f"{source_path}:3:6: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: dash] (ul-style)\n"
        + f"{source_path}:6:6: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: asterisk; Actual: plus] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_multi_level_sublevel_complex_asterisk_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_multi_level_complex.md"
    ) as temp_source_path:
        original_file_contents = """+ first
  1. second
     - third
+ first
  1. second
     + third
       1. fourth
          * fifth
     + third
       1. fourth
          * fifth
     + third
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md004.style=asterisk",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """* first
  1. second
     * third
* first
  1. second
     * third
       1. fourth
          * fifth
     * third
       1. fourth
          * fifth
     * third
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md004_bad_dual_lists_with_separator():
    """
    Test to make sure this rule does trigger with a document that contains
    two separate lists with different start characters, and configuration
    specifically set to sublist.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "bad_dual_lists_with_separator.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=sublist",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:6:1: "
        + "MD004: Inconsistent Unordered List Start style "
        + "[Expected: plus; Actual: asterisk] (ul-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md004_bad_dual_lists_with_separator_fix():
    """
    Test to make sure this rule does trigger with a document that
    is only level 1 unordered lists starting with dash and the
    configuration is also set to asterisk.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_dual_lists_with_separator.md"
    ) as temp_source_path:
        original_file_contents = """+ item 1
  - item 1a

this is a separator

* item 2
  - item 2a
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--set",
            "plugins.md004.style=sublist",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """+ item 1
  - item 1a

this is a separator

+ item 2
  - item 2a
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)
