"""
Tests for the optional front-matter processing
"""
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.gfm
def test_pragmas_01():
    """
    Test the case where we specify a pragma, but do not specify a command.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/pragmas/atx_heading_with_multiple_spaces_no_command.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/pragmas/atx_heading_with_multiple_spaces_no_command.md:1:1: "
        + "INLINE: Inline configuration specified without command.\n"
        + "test/resources/pragmas/atx_heading_with_multiple_spaces_no_command.md:2:1: "
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
def test_pragmas_02():
    """
    Test the case where we specify a pragma, but specify a command that is not recognized.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/pragmas/atx_heading_with_multiple_spaces_bad_command.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/pragmas/atx_heading_with_multiple_spaces_bad_command.md:1:1: "
        + "INLINE: Inline configuration command 'bad' not understood.\n"
        + "test/resources/pragmas/atx_heading_with_multiple_spaces_bad_command.md:2:1: "
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
def test_pragmas_03():
    """
    Test the case where we specify a 'disable-next-line' pragma, but specify no id to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/pragmas/atx_heading_with_multiple_spaces_disable_with_no_id.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/pragmas/atx_heading_with_multiple_spaces_disable_with_no_id.md:1:1: "
        + "INLINE: Inline configuration command 'disable-next-line' specified a plugin with a blank id.\n"
        + "test/resources/pragmas/atx_heading_with_multiple_spaces_disable_with_no_id.md:2:1: "
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
def test_pragmas_04():
    """
    Test the case where we specify a 'disable-next-line' pragma, but specify a bad id to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/pragmas/atx_heading_with_multiple_spaces_disable_with_bad_id.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/pragmas/atx_heading_with_multiple_spaces_disable_with_bad_id.md:1:1: "
        + "INLINE: Inline configuration command 'disable-next-line' unable to find a plugin with the id 'bad-plugin-id'.\n"
        + "test/resources/pragmas/atx_heading_with_multiple_spaces_disable_with_bad_id.md:2:1: "
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
def test_pragmas_05():
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/pragmas/atx_heading_with_multiple_spaces_disable_line_by_id.md",
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
def test_pragmas_06():
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid name to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/pragmas/atx_heading_with_multiple_spaces_disable_line_by_name.md",
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
def test_pragmas_07():
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id and name to disable.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/pragmas/atx_heading_with_multiple_spaces_disable_line_by_id_and_name.md",
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
def test_pragmas_08():
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable
    and the alternate start sequence.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/pragmas/atx_heading_with_multiple_spaces_disable_line_by_id_and_alternate_start.md",
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
def test_pragmas_09():
    """
    Test the case where we specify a 'disable-next-line' pragma with a valid id to disable
    but no firing of that rule.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/pragmas/atx_heading_with_multiple_spaces_disable_line_by_id_with_non_firing.md",
    ]

    expected_return_code = 1
    expected_output = (
        ""
        + "test/resources/pragmas/atx_heading_with_multiple_spaces_disable_line_by_id_with_non_firing.md:2:1: "
        + "MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
