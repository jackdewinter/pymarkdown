"""
Module to provide tests related to the MD009 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md009_bad_configuration_br_spaces():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md009.br_spaces=not-integer",
        "--strict-config",
        "scan",
        "test/resources/rules/md009/good_paragraph_no_extra.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md009.br_spaces' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_configuration_br_spaces_invalid():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md009.br_spaces=$#-1",
        "--strict-config",
        "scan",
        "test/resources/rules/md009/good_paragraph_no_extra.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md009.br_spaces' is not valid: Allowable values are greater than or equal to 0."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_configuration_strict():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md009.strict=not-boolean",
        "--strict-config",
        "scan",
        "test/resources/rules/md009/good_paragraph_no_extra.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md009.strict' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_configuration_list_item_empty_lines():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md009.list_item_empty_lines=not-boolean",
        "--strict-config",
        "scan",
        "test/resources/rules/md009/good_paragraph_no_extra.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md009.list_item_empty_lines' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_good_paragraph_no_extra():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md009/good_paragraph_no_extra.md",
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
def test_md009_bad_paragraph_increasing_extra():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md009/bad_paragraph_increasing_extra.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md009/bad_paragraph_increasing_extra.md:1:18: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_paragraph_increasing_extra.md:3:20: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 3] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_paragraph_increasing_extra_with_config_br_spaces_3():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md009.br_spaces=$#3",
        "--strict-config",
        "scan",
        "test/resources/rules/md009/bad_paragraph_increasing_extra.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md009/bad_paragraph_increasing_extra.md:1:18: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 3; Actual: 1] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_paragraph_increasing_extra.md:2:19: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 3; Actual: 2] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_paragraph_increasing_extra.md:4:17: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 3; Actual: 2] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_paragraph_increasing_extra_with_config_br_spaces_0():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md009.br_spaces=$#0",
        "--strict-config",
        "scan",
        "test/resources/rules/md009/bad_paragraph_increasing_extra.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md009/bad_paragraph_increasing_extra.md:1:18: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 1] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_paragraph_increasing_extra.md:2:19: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 2] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_paragraph_increasing_extra.md:3:20: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 3] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_paragraph_increasing_extra.md:4:17: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 2] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_paragraph_increasing_extra_with_config_strict():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md009.strict=$!True",
        "--strict-config",
        "scan",
        "test/resources/rules/md009/bad_paragraph_increasing_extra.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md009/bad_paragraph_increasing_extra.md:1:18: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 1] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_paragraph_increasing_extra.md:2:19: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 2] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_paragraph_increasing_extra.md:3:20: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 3] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_paragraph_increasing_extra.md:4:17: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 2] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_atx_heading_with_extra():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md009/bad_atx_heading_with_extra.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md009/bad_atx_heading_with_extra.md:1:32: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_setext_heading_with_extra():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md009/bad_setext_heading_with_extra.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md009/bad_setext_heading_with_extra.md:1:30: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_setext_heading_with_extra.md:2:22: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_setext_heading_with_extra.md:3:22: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_theamtic_break_with_extra():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md009/bad_theamtic_break_with_extra.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md009/bad_theamtic_break_with_extra.md:1:11: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_good_indented_code_block_with_extra():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md009/good_indented_code_block_with_extra.md",
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
def test_md009_good_fenced_code_block_with_extra():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md009/good_fenced_code_block_with_extra.md",
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
def test_md009_bad_html_block_with_extra():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md009/bad_html_block_with_extra.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md009/bad_html_block_with_extra.md:2:5: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_html_block_with_extra.md:3:3: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_html_block_with_extra.md:4:2: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_html_block_with_extra.md:5:5: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_html_block_with_extra.md:6:6: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_link_reference_definition_with_extra():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md009/bad_link_reference_definition_with_extra.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md009/bad_link_reference_definition_with_extra.md:1:7: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_link_reference_definition_with_extra.md:2:9: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_link_reference_definition_with_extra.md:3:12: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_blank_lines_with_extra():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md012",
        "scan",
        "test/resources/rules/md009/bad_blank_lines_with_extra.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md009/bad_blank_lines_with_extra.md:1:1: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + "test/resources/rules/md009/bad_blank_lines_with_extra.md:3:1: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 3] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_good_unordered_list_item_empty_lines():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md009/good_unordered_list_item_empty_lines.md",
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
def test_md009_good_unordered_list_item_empty_lines_with_config_strict():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md009.strict=$!True",
        "--strict-config",
        "scan",
        "test/resources/rules/md009/good_unordered_list_item_empty_lines.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md009/good_unordered_list_item_empty_lines.md:2:1: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 2] (no-trailing-spaces)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_good_unordered_list_item_empty_lines_with_config_strict_and_list_empty():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md009.strict=$!True",
        "--set",
        "plugins.md009.list_item_empty_lines=$!True",
        "--strict-config",
        "scan",
        "test/resources/rules/md009/good_unordered_list_item_empty_lines.md",
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
def test_md009_good_ordered_list_item_empty_lines_with_list_empty():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md020 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md009.list_item_empty_lines=$!True",
        "--strict-config",
        "scan",
        "test/resources/rules/md009/good_unordered_list_item_empty_lines.md",
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
