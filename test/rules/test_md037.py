"""
Module to provide tests related to the MD037 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import (
    assert_file_is_as_expected,
    copy_to_temp_file,
    create_temporary_configuration_file,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md037") + os.sep


@pytest.mark.rules
def test_md037_good_valid_emphasis():
    """
    Test to make sure this rule does not trigger with a document that
    contains one or more valid emphasis sequences.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "good_valid_emphasis.md"
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
def test_md037_bad_surrounding_emphasis():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters surrounded by spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_surrounding_emphasis.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:3:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:5:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_bad_surrounding_emphasis_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_surrounding_emphasis.md"
    ) as temp_source_path:
        original_file_contents = """this text * is * in italics

this text _ is _ in italics

this text ** is ** in bold

this text __ is __ in bold
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

        expected_file_contents = """this text *is* in italics

this text _is_ in italics

this text **is** in bold

this text __is__ in bold
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md037_bad_leading_emphasis():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters with leading spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_leading_emphasis.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:3:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:5:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_bad_leading_emphasis_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(source_path + "bad_leading_emphasis.md") as temp_source_path:
        original_file_contents = """this text * is* in italics

this text _ is_ in italics

this text ** is** in bold

this text __ is__ in bold
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

        expected_file_contents = """this text *is* in italics

this text _is_ in italics

this text **is** in bold

this text __is__ in bold
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md037_bad_trailing_emphasis():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters followed by spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_trailing_emphasis.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:3:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:5:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_bad_trailing_emphasis_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_trailing_emphasis.md"
    ) as temp_source_path:
        original_file_contents = """this text *is * in italics

this text _is _ in italics

this text **is ** in bold

this text __is __ in bold
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

        expected_file_contents = """this text *is* in italics

this text _is_ in italics

this text **is** in bold

this text __is__ in bold
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md037_bad_surrounding_emphasis_multiline():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters surrounded by spaces,
    and the emphasis spans lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_surrounding_emphasis_multiline.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:4:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:10:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_bad_surrounding_emphasis_multiline_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_surrounding_emphasis_multiline.md"
    ) as temp_source_path:
        original_file_contents = """this text * is
not * in italics

this text _ is
not _ in italics

this text ** is
not ** in bold

this text __ is
not __ in bold
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

        expected_file_contents = """this text *is
not* in italics

this text _is
not_ in italics

this text **is
not** in bold

this text __is
not__ in bold
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md037_bad_surrounding_empahsis_setext():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters surrounded by spaces,
    within an SetExt heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_surrounding_empahsis_setext.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:4:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:10:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_bad_surrounding_empahsis_setext_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_surrounding_empahsis_setext.md"
    ) as temp_source_path:
        original_file_contents = """this text * is * in italics
===

this text _ is _ in italics
---

this text ** is ** in bold
---

this text __ is __ in bold
---
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

        expected_file_contents = """this text *is* in italics
===

this text _is_ in italics
---

this text **is** in bold
---

this text __is__ in bold
---
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md037_bad_surrounding_empahsis_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters surrounded by spaces,
    within an Atx Heading element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_surrounding_empahsis_atx.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:3:14: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:5:14: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:7:14: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_bad_surrounding_empahsis_atx_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_surrounding_empahsis_atx.md"
    ) as temp_source_path:
        original_file_contents = """# this text * is * in italics

## this text _ is _ in italics

## this text ** is ** in bold

## this text __ is __ in bold
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

        expected_file_contents = """# this text *is* in italics

## this text _is_ in italics

## this text **is** in bold

## this text __is__ in bold
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md037_bad_surrounding_emphasis_containers():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters surrounded by spaces,
    within a single line within a container element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "bad_surrounding_emphasis_containers.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:3:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)\n"
        + f"{source_path}:5:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md037_bad_surrounding_emphasis_containers_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_surrounding_emphasis_containers.md"
    ) as temp_source_path:
        original_file_contents = """1. this is * not in * italics

+ this is * not in * italics

> this is * not in * italics
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

        expected_file_contents = """1. this is *not in* italics

+ this is *not in* italics

> this is *not in* italics
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md037_good_emphasis_with_code_span():
    """
    Test to make sure this rule does not trigger with a document that
    contains one or two valid emphasis characters surrounded by spaces,
    within a code span.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "good_emphasis_with_code_span.md"
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
def test_md037_good_no_emphasis_but_stars():
    """
    Test to make sure this rule does not trigger with a document that
    contains one or two valid emphasis characters as part of other parts
    of a paragraph.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md037", "good_no_emphasis_but_stars.md"
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
def test_md037_bad_surrounding_emphasis_link_surround():
    """
    Test to make sure this rule does trigger with a document that
    contains one or two valid emphasis characters surrounded by spaces,
    within a single line within a container element.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """abc * [link](/url) * ghi
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = f"{temp_source_path}:1:5: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md037_bad_surrounding_emphasis_link_surround_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """abc * [link](/url) * ghi"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """abc *[link](/url)* ghi
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md037_bad_surrounding_emphasis_link_before_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """abc * [link](/url)* ghi
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--stack-trace",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """abc *[link](/url)* ghi
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md037_bad_surrounding_emphasis_link_after_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an inline link with space on the right side of the link label.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """abc *[link](/url) * ghi
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """abc *[link](/url)* ghi
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)
