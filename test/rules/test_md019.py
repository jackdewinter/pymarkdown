"""
Module to provide tests related to the MD019 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import assert_file_is_as_expected, copy_to_temp_file

import pytest

# pylint: disable=too-many-lines

source_path = os.path.join("test", "resources", "rules", "md019") + os.sep


@pytest.mark.rules
def test_md019_good_single_spacing():
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx Heading with a single space before text.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md019", "single_spacing.md"
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
def test_md019_bad_multiple_spacing():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx Headings with multiple spaces before text.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md019", "multiple_spacing.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
        + f"{source_path}:3:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md019_bad_multiple_spacing_fix():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx Headings with multiple spaces before text.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(source_path + "multiple_spacing.md") as temp_source_path:
        original_file_contents = """#  Heading 1

##  Heading 2
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

        expected_file_contents = """# Heading 1

## Heading 2
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


def test_md019_bad_multiple_spacing_with_inline():
    """
    Test to make sure this rule does not trigger with a document that
    contains multiple Atx Headings with multiple spaces before text,
    including an inline element in the heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md019", "multiple_spacing_with_inline.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
        + f"{source_path}:3:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md019_bad_multiple_spacing_with_inline_fix():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx Headings with multiple spaces before text.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "multiple_spacing_with_inline.md"
    ) as temp_source_path:
        original_file_contents = """#  Heading *number* 1

##  Heading *number* 2
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

        expected_file_contents = """# Heading *number* 1

## Heading *number* 2
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


def test_md019_bad_multiple_spacing_with_indent():
    """
    Test to make sure this rule does not trigger with a document that
    contains multiple Atx Headings with multiple spaces before text,
    including indets.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md019", "multiple_spacing_with_indent.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:2: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
        + f"{source_path}:3:3: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md019_bad_multiple_spacing_with_indent_fix():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx Headings with multiple spaces before text.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "multiple_spacing_with_indent.md"
    ) as temp_source_path:
        original_file_contents = """ #  Heading 1

  ##  Heading 2
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md023",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ # Heading 1

  ## Heading 2
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


def test_md019_bad_single_space_single_tab():
    """
    Test to make sure this rule does trigger with a document that
    contains multiple Atx Headings with tabs before text.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md019", "single_space_single_tab.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md010",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
        + f"{source_path}:3:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md019_bad_single_space_single_tab_fix():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx Headings with multiple spaces before text.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "single_space_single_tab.md"
    ) as temp_source_path:
        original_file_contents = """# \tHeading 1

## \tHeading 2
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md010",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """# Heading 1

## Heading 2
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)
