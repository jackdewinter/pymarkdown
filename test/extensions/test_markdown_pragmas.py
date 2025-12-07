"""
Tests for the optional front-matter processing
"""

import os
from test.markdown_scanner import MarkdownScanner

import pytest

from test.utils import create_temporary_configuration_file


@pytest.mark.gfm
def test_pragmas_no_command() -> None:
    """
    Test the case where we specify a pragma, but do not specify a command.

    This function is shadowed by test_api_scan_with_pragma_failure.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "pragmas", "atx_heading_with_multiple_spaces_no_command.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration specified without command.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_bad_command() -> None:
    """
    Test the case where we specify a pragma, but specify a command that is not recognized.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_bad_command.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration command 'bad' not understood.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_next_line_no_id() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma, but specify no id to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_with_no_id.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration command 'disable-next-line' specified a plugin with a blank id.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_next_line_no_id_more_spaces() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma, but specify no id to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_with_no_id_ms.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration command 'disable-next-line' specified a plugin with a blank id.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_next_line_bad_id() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma, but specify a bad id to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_with_bad_id.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration command 'disable-next-line' unable to find a plugin with the id 'bad-plugin-id'.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_next_line_valid_id() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_id.md",
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


@pytest.mark.gfm
def test_pragmas_disable_next_line_valid_name() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid name to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_name.md",
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


@pytest.mark.gfm
def test_pragmas_disable_next_line_valid_name_and_id() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id and name to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_id_and_name.md",
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


@pytest.mark.gfm
def test_pragmas_disable_next_line_valid_id_and_alternate_start() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable
    and the alternate start sequence.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_id_and_alternate_start.md",
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


@pytest.mark.gfm
def test_pragmas_disable_next_line_valid_id_and_no_fire() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable
    but no firing of that rule.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_id_with_non_firing.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_next_line_no_pragmas() -> None:
    """
    Test the case where we test the file used in test_pragmas_disable_next_line_valid_id, but disable pragmas.

    Note that as the pragma is not being interpreted as a pragma, it causes md022 to
    file because it is on the line right before the Atx Heading.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_id.md",
    )
    supplied_arguments = [
        "--set",
        "extensions.linter-pragmas.enabled=$!False",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
        + f"{source_path}:2:1: "
        + "MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_pragmas_disable_next_line_valid_id_extra_ws_before_pragma() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable and extra whitespace
    before the pyml.
    """
    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_id_with_space_before_pyml.md",
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


def test_pragmas_disable_next_line_valid_id_extra_ws_after_pragma() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable and extra whitespace
    after the pyml.
    """
    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_id_with_space_after_pyml.md",
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


def test_pragmas_disable_next_line_valid_id_extra_ws_after() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable and extra whitespace
    after the pyml.
    """
    # Arrange
    scanner = MarkdownScanner(use_main=False, use_alternate_presentation=True)
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_id_with_space_after_pyml.md",
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


def test_pragmas_disable_next_line_valid_id_extra_ws_after_command() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable and extra whitespace
    after the pyml command.
    """
    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_id_with_space_after_pyml_command.md",
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


@pytest.mark.gfm
def test_pragmas_disable_num_line_no_lines() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma, but specify no lines to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_num_with_no_id.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration command 'disable-num-lines' was not followed by a count and a list of plugin ids to temporarily disable.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_num_line_bad_id() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma, but specify no lines to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_num_with_bad_id.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration command 'disable-num-lines' unable to find a plugin with the id 'bad-plugin-id'.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_num_line_no_whitespace_before_count() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma, but specify no lines to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_num_with_no_whitespace_before_count.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration command 'disable-num-lines' was not followed by a count and a list of plugin ids to temporarily disable.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_num_line_bad_lines() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma, but specify no lines to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_num_with_bad_count.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration command 'disable-num-lines' specified a count 'abc' that is not a valid positive integer.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_num_line_no_whitespace_before_countx() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma, but specify no lines to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_num_with_no_whitespace_before_count.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration command 'disable-num-lines' was not followed by a count and a list of plugin ids to temporarily disable.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_num_line_after_lines() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma, but specify no lines to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_num_with_no_whitespace_after_count.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration command 'disable-num-lines' and its count were not followed by a list of plugin ids to temporarily disable.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_num_line_bad_idx() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma, but specify a bad id to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_with_bad_id.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration command 'disable-next-line' unable to find a plugin with the id 'bad-plugin-id'.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_num_line_valid_id() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_id.md",
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


@pytest.mark.gfm
def test_pragmas_disable_num_line_valid_name() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid name to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_name.md",
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


@pytest.mark.gfm
def test_pragmas_disable_num_line_valid_name_and_id() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id and name to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_line_by_id_and_name.md",
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


@pytest.mark.gfm
def test_pragmas_disable_num_line_valid_id_and_no_fire() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable
    but no firing of that rule.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_num_line_by_id_with_non_firing.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_num_line_valid_id_and_only_comma() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable
    but no firing of that rule.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_num_valid_id_only_comma.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration command 'disable-num-lines' specified a plugin with a blank id.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_num_line_valid_id_and_bad_id() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable
    but no firing of that rule.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_num_valid_id_and_bad_id.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = (
        f"{source_path}:1:1: "
        + "INLINE: Inline configuration command 'disable-num-lines' unable to find a plugin with the id 'bad-id'.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_num_line_multiple_disabled() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable
    but no firing of that rule.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_num_multiple_lines.md",
    )
    supplied_arguments = [
        "--set",
        "extensions.linter-pragmas.enabled=$!False",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = """{source_path}:2:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{source_path}:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
{source_path}:7:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)
{source_path}:8:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)
{source_path}:9:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)""".replace(
        "{source_path}", source_path
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_num_line_multiple_enabled() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable
    but no firing of that rule.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_num_multiple_lines.md",
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


@pytest.mark.gfm
def test_pragmas_disable_num_line_multiple_enabled_by_name() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable
    but no firing of that rule.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_num_multiple_lines.md",
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


@pytest.mark.gfm
def test_pragmas_disable_num_line_multiple_enabled_one_pragmad_one_not() -> None:
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable
    but no firing of that rule.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_num_multiple_lines_multiple.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = """{source_path}:11:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)
{source_path}:12:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)
{source_path}:13:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)""".replace(
        "{source_path}", source_path
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_disable_without_enabled() -> None:
    """
    Test the case where we specify a 'disable' pragma with a valid id to disable but without a balancing enable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_without_enable.md",
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


@pytest.mark.gfm
def test_pragmas_disable_with_enabled() -> None:
    """
    Test the case where we specify a 'disable' pragma with a valid id to disable but without a balancing enable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_disable_with_enable.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"""{source_path}:11:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)
{source_path}:12:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)
{source_path}:13:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_enable_with_no_disable() -> None:
    """
    Test the case where we specify a 'disable' pragma with a valid id to disable but without a balancing enable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_enable_with_no_disable.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"""{source_path}:5:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)
{source_path}:6:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)
{source_path}:7:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)
{source_path}:9:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)
{source_path}:10:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)
{source_path}:11:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_double_disable_with_enable() -> None:
    """
    Test the case where we specify a 'disable' pragma with a valid id to disable but without a balancing enable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_double_disable_with_enable.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"""{source_path}:12:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)
{source_path}:13:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)
{source_path}:14:1: MD013: Line length [Expected: 80, Actual: 85] (line-length)"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_multiple_disable_enable_blocks() -> None:
    """
    Test the case where we specify a 'disable' pragma with a valid id to disable but without a balancing enable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_multiple_disable_enable_blocks.md",
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


@pytest.mark.gfm
def test_pragmas_multiple_disable_with_no_rules() -> None:
    """
    Test the case where we specify a 'disable' pragma with a valid id to disable but without a balancing enable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_multiple_disable_with_no_rules.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"""{source_path}:1:21: MD047: Each file should end with a single newline character. (single-trailing-newline)"""
    expected_error = f"""{source_path}:1:1: INLINE: Inline configuration command 'disable' specified a plugin with a blank id."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_multiple_enable_with_no_rules() -> None:
    """
    Test the case where we specify a 'disable' pragma with a valid id to disable but without a balancing enable.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "pragmas",
        "atx_heading_with_multiple_spaces_multiple_enable_with_no_rules.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = f"""{source_path}:1:20: MD047: Each file should end with a single newline character. (single-trailing-newline)"""
    expected_error = f"""{source_path}:1:1: INLINE: Inline configuration command 'enable' specified a plugin with a blank id."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

