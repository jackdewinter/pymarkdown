"""
Module to provide tests related to the MD026 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md041_bad_configuration_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md041.level=1",
        "--strict-config",
        "scan",
        "test/resources/rules/md041/good_single_top_level.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md041.level' must be of type 'int'."
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
def test_md041_good_configuration_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md041.level=$#1",
        "--strict-config",
        "scan",
        "test/resources/rules/md041/good_heading_top_level_atx.md",
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
def test_md041_bad_configuration_level_bad():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md041.level=$#0",
        "--strict-config",
        "scan",
        "test/resources/rules/md041/good_single_top_level.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md041.level' is not valid: Allowable values are between 1 and 6."
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
def test_md041_bad_configuration_front_matter_title():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md041.front_matter_title=$#1",
        "--strict-config",
        "scan",
        "test/resources/rules/md041/good_single_top_level.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md041.front_matter_title' must be of type 'str'."
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
def test_md041_good_configuration_front_matter_title():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md041.front_matter_title=subject",
        "--strict-config",
        "scan",
        "test/resources/rules/md041/good_heading_top_level_atx.md",
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
def test_md041_bad_configuration_front_matter_title_bad():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md041.front_matter_title=",
        "--strict-config",
        "scan",
        "test/resources/rules/md041/good_heading_top_level_atx.md",
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
def test_md041_bad_configuration_front_matter_title_invalid():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md041.front_matter_title=a:b",
        "--strict-config",
        "scan",
        "test/resources/rules/md041/good_single_top_level.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md041.front_matter_title' is not valid: Colons (:) are not allowed in the value."
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
def test_md041_good_single_top_level_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md041/good_heading_top_level_atx.md",
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
def test_md041_good_blank_lines_top_level_atx_heading():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md041/good_blank_lines_top_level_atx_heading.md",
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
def test_md041_bad_single_top_level_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md041/bad_heading_top_level_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md041/bad_heading_top_level_atx.md:1:1: "
        + "MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)"
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
def test_md041_good_heading_top_level_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md041/good_heading_top_level_setext.md",
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
def test_md041_bad_single_top_level_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md041/bad_heading_top_level_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md041/bad_heading_top_level_setext.md:2:1: "
        + "MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)"
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
def test_md041_good_front_matter_top_level():
    """
    Test to verify that a good title is interpreted from the front-matter.
    If the verification goes properly, line 5 should trigger a md025 for
    a multiple top level heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
        "scan",
        "test/resources/rules/md041/good_front_matter_top_level.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md041/good_front_matter_top_level.md:5:1: "
        + "MD025: Multiple top level headings in the same document (single-title,single-h1)"
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
def test_md041_bad_front_matter_top_level():
    """
    Test to verify that a bad title is not interpreted from the front-matter.
    If the verification goes properly, no rules should be triggered as the
    front-matter did not contribute to the top-level.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "extensions.front-matter.enabled=$!True",
        "scan",
        "test/resources/rules/md041/bad_front_matter_top_level.md",
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
def test_md041_bad_fenced_code_block():
    """
    Test to verify that a bad title is not interpreted from the front-matter.
    If the verification goes properly, no rules should be triggered as the
    front-matter did not contribute to the top-level.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md041/bad_fenced_code_block.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md041/bad_fenced_code_block.md:1:1: "
        + "MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)"
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
def test_md041_bad_thematic_break():
    """
    Test to verify that a bad title is not interpreted from the front-matter.
    If the verification goes properly, no rules should be triggered as the
    front-matter did not contribute to the top-level.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md041/bad_thematic_break.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md041/bad_thematic_break.md:1:1: "
        + "MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)"
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
def test_md041_bad_indented_code_block():
    """
    Test to verify that a bad title is not interpreted from the front-matter.
    If the verification goes properly, no rules should be triggered as the
    front-matter did not contribute to the top-level.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md041/bad_indented_code_block.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md041/bad_indented_code_block.md:1:5: "
        + "MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)"
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
def test_md041_bad_html_block():
    """
    Test to verify that a bad title is not interpreted from the front-matter.
    If the verification goes properly, no rules should be triggered as the
    front-matter did not contribute to the top-level.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md041/bad_html_block.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md041/bad_html_block.md:1:1: "
        + "MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)"
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
def test_md041_bad_html_block_heading():
    """
    Test to verify that a bad title is not interpreted from the front-matter.
    If the verification goes properly, no rules should be triggered as the
    front-matter did not contribute to the top-level.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md033",
        "scan",
        "test/resources/rules/md041/bad_html_block_heading.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md041/bad_html_block_heading.md:1:1: "
        + "MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)"
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
def test_md041_good_html_block_heading():
    """
    Test to verify that a bad title is not interpreted from the front-matter.
    If the verification goes properly, no rules should be triggered as the
    front-matter did not contribute to the top-level.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md033",
        "scan",
        "test/resources/rules/md041/good_html_block_heading.md",
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
