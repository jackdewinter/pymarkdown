"""
Module to provide tests related to the MD009 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import (
    assert_file_is_as_expected,
    copy_to_temp_file,
    read_contents_of_text_file,
)

import pytest

from pymarkdown.general.parser_helper import ParserHelper


def __generate_expected_contents(temp_source_path: str, break_point: int) -> str:
    """
    Given the source file, make any required changes to the file outside of the
    plugin.
    """
    existing_file_contents = read_contents_of_text_file(temp_source_path)
    # print("---\n" + existing_file_contents.replace("\n", "\\n").replace("\t", "\\t") + "\n---")
    new_lines = []
    for next_line in existing_file_contents.splitlines(keepends=True):
        removed_end_of_line = ""
        if next_line and next_line[-1] == "\n":
            removed_end_of_line = next_line[-1]
            next_line = next_line[:-1]
        (
            first_non_whitespace_index,
            extracted_whitespace,
        ) = ParserHelper.extract_spaces_from_end(next_line)
        print("before>:" + next_line + ":<")
        if len(extracted_whitespace) < break_point:
            next_line = next_line[:first_non_whitespace_index]
        else:
            next_line = next_line[: first_non_whitespace_index + break_point]
        print(" after>:" + next_line + ":<")
        next_line += removed_end_of_line

        new_lines.append(next_line)
    expected_file_contents = "".join(new_lines)
    # print("---\n" + expected_file_contents.replace("\n", "\\n").replace("\t", "\\t") + "\n---")
    return expected_file_contents


def generate_md009_expected_contents(temp_source_path: str, break_point: int) -> str:
    return __generate_expected_contents(temp_source_path, break_point)


@pytest.mark.rules
def test_md009_bad_paragraph_increasing_extra():
    """
    Test to make sure this rule does trigger with a document that
    has increasing amounts of trailing spaces at the end of lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_paragraph_increasing_extra.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:18: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:3:20: "
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
def test_md009_bad_paragraph_increasing_extra_fix():
    """
    Test to make sure this rule does trigger with a document that
    has increasing amounts of trailing spaces at the end of lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test", "resources", "rules", "md009", "bad_paragraph_increasing_extra.md"
        )
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = __generate_expected_contents(temp_source_path, 2)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md009_bad_paragraph_increasing_extra_with_config_br_spaces_3():
    """
    Test to make sure this rule does trigger with a document that
    has increasing amounts trailing spaces at the end of lines, and
    configuration set to 3.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_paragraph_increasing_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.br_spaces=$#3",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:18: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 3; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:2:19: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 3; Actual: 2] (no-trailing-spaces)\n"
        + f"{source_path}:4:17: "
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
def test_md009_bad_paragraph_increasing_extra_with_config_br_spaces_3_fix():
    """
    Test to make sure this rule does trigger with a document that
    has increasing amounts trailing spaces at the end of lines, and
    configuration set to 3.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test", "resources", "rules", "md009", "bad_paragraph_increasing_extra.md"
        )
    ) as temp_source_path:
        supplied_arguments = [
            "--set",
            "plugins.md009.br_spaces=$#3",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = __generate_expected_contents(temp_source_path, 3)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md009_bad_paragraph_increasing_extra_with_config_br_spaces_0():
    """
    Test to make sure this rule does trigger with a document that
    has increasing amounts trailing spaces at the end of lines, and
    configuration set to 0.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_paragraph_increasing_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.br_spaces=$#0",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:18: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:2:19: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 2] (no-trailing-spaces)\n"
        + f"{source_path}:3:20: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 3] (no-trailing-spaces)\n"
        + f"{source_path}:4:17: "
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
def test_md009_bad_paragraph_increasing_extra_with_config_br_spaces_0_fix():
    """
    Test to make sure this rule does trigger with a document that
    has increasing amounts trailing spaces at the end of lines, and
    configuration set to 0.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test", "resources", "rules", "md009", "bad_paragraph_increasing_extra.md"
        )
    ) as temp_source_path:
        supplied_arguments = [
            "--set",
            "plugins.md009.br_spaces=$#0",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = __generate_expected_contents(temp_source_path, 0)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md009_bad_paragraph_increasing_extra_with_config_strict():
    """
    Test to make sure this rule does trigger with a document that
    has increasing amounts trailing spaces at the end of lines, and
    configuration set to strict.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_paragraph_increasing_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.strict=$!True",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:18: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:2:19: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 2] (no-trailing-spaces)\n"
        + f"{source_path}:3:20: "
        + "MD009: Trailing spaces "
        + "[Expected: 0; Actual: 3] (no-trailing-spaces)\n"
        + f"{source_path}:4:17: "
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
def test_md009_bad_paragraph_increasing_extra_with_config_strict_fix():
    """
    Test to make sure this rule does trigger with a document that
    has increasing amounts trailing spaces at the end of lines, and
    configuration set to strict.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test", "resources", "rules", "md009", "bad_paragraph_increasing_extra.md"
        )
    ) as temp_source_path:
        supplied_arguments = [
            "--set",
            "plugins.md009.strict=$!True",
            "--strict-config",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = __generate_expected_contents(temp_source_path, 2)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md009_bad_atx_heading_with_extra():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end of an Atx Heading element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_atx_heading_with_extra.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:32: "
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
def test_md009_bad_atx_heading_with_extra_fix():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end of an Atx Heading element.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test", "resources", "rules", "md009", "bad_atx_heading_with_extra.md"
        )
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = __generate_expected_contents(temp_source_path, 2)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md009_bad_setext_heading_with_extra():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end of a SetExt Heading element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_setext_heading_with_extra.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:30: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:2:22: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:3:22: "
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
def test_md009_bad_setext_heading_with_extra_fix():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end of a SetExt Heading element.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test", "resources", "rules", "md009", "bad_setext_heading_with_extra.md"
        )
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = __generate_expected_contents(temp_source_path, 2)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md009_bad_theamtic_break_with_extra():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end of a Thematic break element.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_theamtic_break_with_extra.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:11: "
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
def test_md009_bad_theamtic_break_with_extra_fix():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end of a Thematic break element.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test", "resources", "rules", "md009", "bad_theamtic_break_with_extra.md"
        )
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = __generate_expected_contents(temp_source_path, 2)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md009_bad_html_block_with_extra():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces for text within a HTML block.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_html_block_with_extra.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md033",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:5: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:3:3: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:4:2: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:5:5: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:6:6: "
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
def test_md009_bad_html_block_with_extra_fix():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces for text within a HTML block.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test", "resources", "rules", "md009", "bad_html_block_with_extra.md"
        )
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md033",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = __generate_expected_contents(temp_source_path, 2)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md009_bad_link_reference_definition_with_extra():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces within a Link Reference Definition.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md009",
        "bad_link_reference_definition_with_extra.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:7: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:2:9: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:3:12: "
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
def test_md009_bad_link_reference_definition_with_extra_fix():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces within a Link Reference Definition.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md009",
            "bad_link_reference_definition_with_extra.md",
        )
    ) as temp_source_path:
        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = __generate_expected_contents(temp_source_path, 2)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md009_bad_blank_lines_with_extra():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end various blank lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "bad_blank_lines_with_extra.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md012",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD009: Trailing spaces "
        + "[Expected: 0 or 2; Actual: 1] (no-trailing-spaces)\n"
        + f"{source_path}:3:1: "
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
def test_md009_bad_blank_lines_with_extra_fix():
    """
    Test to make sure this rule does trigger with a document that
    has trailing spaces at the end various blank lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test", "resources", "rules", "md009", "bad_blank_lines_with_extra.md"
        )
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md012",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = __generate_expected_contents(temp_source_path, 2)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)
