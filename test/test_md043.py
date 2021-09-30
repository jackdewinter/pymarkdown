"""
Module to provide tests related to the MD026 rule.
"""
from test.markdown_scanner import MarkdownScanner

import pytest

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md043_bad_configuration_headings():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=$#1",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_simple_headings.md",
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
def test_md043_bad_configuration_headings_dupicate_stars():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# 1,*,*,# 2",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_simple_headings.md",
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
def test_md043_good_configuration_headings_empty():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_simple_headings.md",
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
def test_md043_bad_configuration_headings_no_atx_start():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=a heading",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_simple_headings.md",
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
def test_md043_bad_configuration_headings_too_many_hashes():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=####### a heading",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_simple_headings.md",
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
def test_md043_bad_configuration_headings_bad_whitespace():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=######a heading",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_simple_headings.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md043.headings' is not valid: Heading format not valid: "
        + "Element must have at least one space character after any hash characters (#)."
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
def test_md043_bad_configuration_headings_bad_text():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=###### ",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_simple_headings.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md043.headings' is not valid: "
        + "Heading format not valid: Element must have at least one non-space character after any space characters."
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
def test_md043_good_simple_headings_no_format():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "scan",
        "test/resources/rules/md043/good_simple_headings.md",
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
def test_md043_good_single_heading_atx_with_single_rule():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_single_heading_atx.md",
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
def test_md043_bad_single_heading_atx_with_double_rule():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,## Another heading",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_single_heading_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md043/good_single_heading_atx.md:1:1: "
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
def test_md043_bad_double_heading_atx_with_single_rule():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_double_heading_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md043/good_double_heading_atx.md:3:1: "
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
def test_md043_good_double_heading_atx_with_double_rule():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,## Another heading",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_double_heading_atx.md",
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
def test_md043_bad_double_heading_atx_with_double_rule_bad_level():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,### A bad level",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_double_heading_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md043/good_double_heading_atx.md:3:1: "
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
def test_md043_bad_double_heading_atx_with_double_rule_bad_text():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,## A bad level",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_double_heading_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md043/good_double_heading_atx.md:3:1: "
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
def test_md043_good_double_heading_atx_second_has_emphasis():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,## Another heading",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_double_heading_atx_second_has_emphasis.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md043/good_double_heading_atx_second_has_emphasis.md:3:1: "
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
def test_md043_good_simple_headings_simple_format():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,## Heading 2,### Heading 3,## Heading 2,### Heading 3",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_simple_headings.md",
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
def test_md043_good_double_heading_atx_with_double_rule_matching_1_star():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,*",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_double_heading_atx.md",
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
def test_md043_bad_double_heading_atx_with_double_rule_unmatching_1_star():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# A single heading,*",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_double_heading_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md043/good_double_heading_atx.md:1:1: "
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
def test_md043_good_double_heading_atx_with_double_rule_matching_star_2():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=*,## Another heading",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_double_heading_atx.md",
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
def test_md043_bad_double_heading_atx_with_double_rule_unmatching_star_2():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=*,## Second heading",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_double_heading_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md043/good_double_heading_atx.md:3:1: "
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
def test_md043_bad_double_heading_atx_unmatching_1_2_3_star():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,## Another heading,## Another heading,*",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_double_heading_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md043/good_double_heading_atx.md:3:1: "
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
def test_md043_bad_double_heading_atx_unmatching_star_1_2_3():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=*,# This is a single heading,## Another heading,## Another heading",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_double_heading_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md043/good_double_heading_atx.md:3:1: "
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
def test_md043_bad_double_heading_atx_matching_1_2_start_2_over():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--set",
        "plugins.md043.headings=# This is a single heading,## Another heading,*,## Another heading",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_double_heading_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md043/good_double_heading_atx.md:3:1: "
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
def test_md043_good_simple_headings_rule_matching_1_star_2_3():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,## Heading 2,### Heading 3",
        "--strict-config",
        "scan",
        "test/resources/rules/md043/good_simple_headings.md",
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
def test_md043_good_good_simple_headings_1_star_3_star_3():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,### Heading 3,*,### Heading 3",
        "--strict-config",
        "--stack-trace",
        "scan",
        "test/resources/rules/md043/good_simple_headings.md",
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
def test_md043_bad_good_many_level_two_1_star_3_star_3():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,### Heading 3,*,### Heading 3",
        "--strict-config",
        "--stack-trace",
        "scan",
        "test/resources/rules/md043/good_many_level_two.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md043/good_many_level_two.md:3:1: "
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
def test_md043_good_good_many_level_two_1_star_2_star_2_star_3():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,## Heading 2,*,## Heading 2,*,### Heading 3",
        "--strict-config",
        "--stack-trace",
        "scan",
        "test/resources/rules/md043/good_many_level_two.md",
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
def test_md043_bad_good_many_level_two_1_star_2_star_2_star_3():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,### Heading 3,*,### Heading 3,*,### Heading 3",
        "--strict-config",
        "--stack-trace",
        "scan",
        "test/resources/rules/md043/good_many_level_two.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md043/good_many_level_two.md:3:1: "
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
def test_md043_good_good_simple_headings_two_1_star_3_2_star_3():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,### Heading 3,## Heading 2,*,### Heading 3",
        "--strict-config",
        "--stack-trace",
        "scan",
        "test/resources/rules/md043/good_simple_headings.md",
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
def test_md043_bad_good_many_level_two_1_star_3_2_star_3():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md024",
        "--set",
        "plugins.md043.headings=# Heading 1,*,### Heading 3,## Heading 2,*,### Heading 3",
        "--strict-config",
        "--stack-trace",
        "scan",
        "test/resources/rules/md043/good_many_level_two.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md043/good_many_level_two.md:3:1: "
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
