"""
Module to provide tests related to the MD038 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import assert_file_is_as_expected, copy_to_temp_file

import pytest


@pytest.mark.rules
def test_md038_good_code_span():
    """
    Test to make sure this rule does not trigger with a document that
    contains a code span element that does not start or end with spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md038", "good_code_span.md"
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
def test_md038_bad_code_span_trailing():
    """
    Test to make sure this rule does trigger with a document that
    contains a code span element that end with spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md038", "bad_code_span_trailing.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:9: "
        + "MD038: Spaces inside code span elements (no-space-in-code)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


source_path = os.path.join("test", "resources", "rules", "md038") + os.sep


@pytest.mark.rules
def test_md038_bad_code_span_trailing_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_code_span_trailing.md"
    ) as temp_source_path:
        original_file_contents = """this is `bad code span ` text
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

        expected_file_contents = """this is `bad code span` text
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md038_bad_code_span_leading():
    """
    Test to make sure this rule does trigger with a document that
    contains a code span element that starts with spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md038", "bad_code_span_leading.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:9: "
        + "MD038: Spaces inside code span elements (no-space-in-code)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md038_bad_code_span_leading_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_code_span_leading.md"
    ) as temp_source_path:
        original_file_contents = """this is ` bad code span` text
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

        expected_file_contents = """this is `bad code span` text
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md038_good_code_span_both():
    """
    Test to make sure this rule does not trigger with a document that
    contains a code span element that starts and ends with a single space.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md038", "good_code_span_both.md"
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
def test_md038_bad_code_span_both_extra():
    """
    Test to make sure this rule does trigger with a document that
    contains a code span element that starts and ends with multiple spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md038", "bad_code_span_both_extra.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:9: "
        + "MD038: Spaces inside code span elements (no-space-in-code)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md038_bad_code_span_both_extra_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_code_span_both_extra.md"
    ) as temp_source_path:
        original_file_contents = """this is `  bad code span  ` text
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

        expected_file_contents = """this is ` bad code span ` text
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md038_good_code_span_embedded_leading_backtick():
    """
    Test to make sure this rule does not trigger with a document that
    contains a code span element that starts with a single space
    followed by a backtick.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md038",
        "good_code_span_embedded_leading_backtick.md",
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
def test_md038_good_code_span_embedded_trailing_backtick():
    """
    Test to make sure this rule does not trigger with a document that
    contains a code span element that ends with a single backtick
    followed by a space.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md038",
        "good_code_span_embedded_trailing_backtick.md",
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
def test_md038_bad_code_span_empty():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md004 directory that has consistent asterisk usage on a single
    level list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md038", "bad_code_span_empty.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:25: "
        + "MD038: Spaces inside code span elements (no-space-in-code)\n"
        + f"{source_path}:3:24: "
        + "MD038: Spaces inside code span elements (no-space-in-code)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md038_bad_code_span_empty_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(source_path + "bad_code_span_empty.md") as temp_source_path:
        original_file_contents = """this is an almost empty ` ` codepsan

this is an only spaces `  ` codepsan
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        expected_file_contents = """this is an almost empty ` ` codepsan

this is an only spaces `  ` codepsan
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)
