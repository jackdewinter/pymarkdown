"""
Module to provide tests related to the MD003 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

from .utils import write_temporary_configuration

# pylint: disable=too-many-lines


@pytest.mark.rules
def test_md022_proper_line_spacing_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/proper_line_spacing_atx.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_proper_line_spacing_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/proper_line_spacing_setext.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_no_line_spacing_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/no_line_spacing_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_atx.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_atx.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_no_line_spacing_before_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/no_line_spacing_before_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_before_atx.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_no_line_spacing_after_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/no_line_spacing_after_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_after_atx.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_after_atx.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_atx_with_html_and_good_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/atx_with_html_and_good_line_spacing.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_atx_with_html_and_bad_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/atx_with_html_and_bad_line_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/atx_with_html_and_bad_line_spacing.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/atx_with_html_and_bad_line_spacing.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_atx_with_code_block_and_good_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/atx_with_code_block_and_good_line_spacing.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_atx_with_code_block_and_bad_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/atx_with_code_block_and_bad_line_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/atx_with_code_block_and_bad_line_spacing.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/atx_with_code_block_and_bad_line_spacing.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_atx_with_thematic_break_and_good_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/atx_with_thematic_break_and_good_line_spacing.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_atx_with_thematic_break_and_bad_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/atx_with_thematic_break_and_bad_line_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/atx_with_thematic_break_and_bad_line_spacing.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/atx_with_thematic_break_and_bad_line_spacing.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_no_line_spacing_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing

    Note that setext grabs the last paragraph before the marker and puts it as the
    header.  As such, testing this for one line space before is implied as one line
    space is required to break up the paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/no_line_spacing_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_setext.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_setext.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_no_line_spacing_after_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/no_line_spacing_after_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/no_line_spacing_after_setext.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/no_line_spacing_after_setext.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_setext_with_code_block_and_good_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/setext_with_code_block_and_good_line_spacing.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_setext_with_code_block_and_bad_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/setext_with_code_block_and_bad_line_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/setext_with_code_block_and_bad_line_spacing.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/setext_with_code_block_and_bad_line_spacing.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_setext_with_html_and_good_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/setext_with_html_and_good_line_spacing.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_setext_with_html_and_bad_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/setext_with_html_and_bad_line_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/setext_with_html_and_bad_line_spacing.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/setext_with_html_and_bad_line_spacing.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_setext_with_thematic_break_and_good_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/setext_with_thematic_break_and_good_line_spacing.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_setext_with_thematic_break_and_bad_line_spacing():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md022/setext_with_thematic_break_and_bad_line_spacing.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md022/setext_with_thematic_break_and_bad_line_spacing.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
        + "test/resources/rules/md022/setext_with_thematic_break_and_bad_line_spacing.md:0:0: "
        + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md022_proper_line_spacing_atx_with_alternate_lines_above():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD022": {"lines_above": 2}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md022/proper_line_spacing_atx.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md022/proper_line_spacing_atx.md:0:0: "
            + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md022_double_line_spacing_above_atx_with_alternate_lines_above():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD022": {"lines_above": 2}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md022/double_line_spacing_above_atx.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md022_proper_line_spacing_atx_with_alternate_lines_below():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD022": {"lines_below": 2}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md022/proper_line_spacing_atx.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md022/proper_line_spacing_atx.md:0:0: "
            + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
            + "test/resources/rules/md022/proper_line_spacing_atx.md:0:0: "
            + "MD022: Headings should be surrounded by blank lines (blanks-around-headings,blanks-around-headers)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md022_double_line_spacing_above_atx_with_alternate_lines_below():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD022": {"lines_below": 2}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md022/double_line_spacing_below_atx.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md022_double_line_spacing_above_and_below_atx_with_alternate_lines_both():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx header start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD022": {"lines_below": 2, "lines_above": 2}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md022/double_line_spacing_above_and_below_atx.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


# TODO LRDs
# TODO Lists
# TODO Block Quotes
