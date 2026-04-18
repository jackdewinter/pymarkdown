"""
Module to test that the return code schemes are set up properly.
"""

import os
import runpy
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.utils import (
    assert_file_is_as_expected,
    copy_to_temp_file,
    create_temporary_markdown_file,
)
from typing import Tuple

from pytest import LogCaptureFixture


def __generate_source_path(
    source_file_name: str, alternate_rule: str = "md009"
) -> Tuple[str, str]:
    source_path = os.path.join(
        "test", "resources", "rules", alternate_rule, source_file_name
    )
    return source_path, os.path.abspath(source_path)


def test_markdown_return_code_command_line_bad(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to...
    """

    # Arrange
    supplied_arguments = ["--return-code-scheme", "invalid", "scan"]

    expected_results = ExpectedResults(
        return_code=2,
        expected_error="""usage: main.py [-h] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--enable-extensions ENABLE_EXTENSIONS]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--set SET_CONFIGURATION] [--strict-config] [--no-json5]
               [--stack-trace] [--continue-on-error]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE]
               [--return-code-scheme {default,minimal,explicit}]
               {extensions,fix,plugins,scan,scan-stdin,version} ...
main.py: error: argument --return-code-scheme: invalid __validate_return_code_scheme value: 'invalid'""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_return_code_default_success(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure a return code of 0 for SUCCESS is a default.

    This function shadows
    test_markdown_with_version
    and is shadowed by
    test_markdown_return_code_minimal_success
    """

    # Arrange
    supplied_arguments = ["version"]

    version_path = os.path.join(".", "pymarkdown", "version.py")
    version_meta = runpy.run_path(version_path)
    semantic_version = version_meta["__version__"]

    expected_results = ExpectedResults(expected_output=f"""{semantic_version}""")

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_return_code_default_no_files_to_scan(
    caplog: LogCaptureFixture, scanner_default: MarkdownScanner
) -> None:
    """
    Test to make sure a return code of 1 for NO_FILES_TO_SCAN is a default.

    This function shadows
    test_markdown_with_direct_args
    and is shadowed by
    test_markdown_return_code_minimal_no_files_to_scan
    """

    # Arrange
    supplied_arguments = ["--log-level", "DEBUG", "scan", "does-not-exist.md"]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""Provided path 'does-not-exist.md' does not exist.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(
        arguments=supplied_arguments, use_direct_arguments=True
    )

    # Assert
    execute_results.assert_results(expected_results=expected_results)

    assert "Using direct arguments: [" in caplog.text


def test_markdown_return_code_default_command_line_error(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a return code of 2 for COMMAND_LINE_ERROR is a default.

    This function shadows
    test_markdown_with_dash_l_only
    and is shadowed by
    test_markdown_return_code_minimal_command_line_error
    """

    # Arrange
    supplied_arguments = ["scan", "-l"]

    expected_results = ExpectedResults(
        return_code=2,
        expected_error="""usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS]
                    [-e PATH_EXCLUSIONS] [--respect-gitignore]
                    path [path ...]
main.py scan: error: the following arguments are required: path
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_return_code_default_fixed_at_least_one_file(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a return code of 3 for FIXED_AT_LEAST_ONE_FILE is a default.

    This function shadows
    test_md009 fix good_unordered_list_item_empty_lines_with_config_strict without the list_item_empty_lines config
    and is shadowed by
    test_markdown_return_code_minimal_fixed_at_least_one_file
    """

    # Arrange
    source_file_contents = """- list item text
\a\a
  list item text
""".replace("\a", " ")
    with create_temporary_markdown_file(source_file_contents) as temp_source_path:
        supplied_arguments = [
            "--set",
            "plugins.md009.strict=$!True",
            "--strict-config",
            "fix",
            temp_source_path,
        ]

        expected_results = ExpectedResults(
            return_code=3, expected_output=f"Fixed: {temp_source_path}"
        )
        expected_file_contents = """- list item text

  list item text
"""

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


def test_markdown_return_code_default_scan_triggered_at_least_once(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a return code of 1 for SCAN_TRIGGERED_AT_LEAST_ONCE is a default.

    This function shadows
    test_md009_good_unordered_list_item_empty_lines_with_config_strict
    and is shadowed by
    test_markdown_return_code_minimal_scan_triggered_at_least_once
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "good_unordered_list_item_empty_lines.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.strict=$!True",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:2:1: MD009: Trailing spaces [Expected: 0; Actual: 2] (no-trailing-spaces)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_return_code_default_system_error(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a return code of 1 for SYSTEM_ERROR is a default.

    This function shadows
    test_markdown_with_dash_dash_add_plugin_and_bad_path
    and is shadowed by
    test_markdown_return_code_minimal_system_error
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md", "md047")
    supplied_arguments = [
        "--add-plugin",
        "MD047",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="BadPluginError encountered while loading plugins:\nPlugin path 'MD047' does not exist.\n",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_return_code_minimal_success(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure a return code of 0 for SUCCESS is applied with the minimal scheme.

    This function shadows
    test_markdown_return_code_default_success
    """

    # Arrange
    supplied_arguments = ["--return-code-scheme", "minimal", "version"]

    version_path = os.path.join(".", "pymarkdown", "version.py")
    version_meta = runpy.run_path(version_path)
    semantic_version = version_meta["__version__"]

    expected_results = ExpectedResults(expected_output=f"""{semantic_version}""")

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_return_code_minimal_no_files_to_scan(
    caplog: LogCaptureFixture, scanner_default: MarkdownScanner
) -> None:
    """
    Test to make sure a return code of 0 for NO_FILES_TO_SCAN is applied with the minimal scheme.

    This function shadows
    test_markdown_return_code_default_no_files_to_scan
    """

    # Arrange
    supplied_arguments = [
        "--log-level",
        "DEBUG",
        "--return-code-scheme",
        "minimal",
        "scan",
        "does-not-exist.md",
    ]

    expected_results = ExpectedResults(
        expected_error="""Provided path 'does-not-exist.md' does not exist."""
    )

    # Act
    execute_results = scanner_default.invoke_main(
        arguments=supplied_arguments, use_direct_arguments=True
    )

    # Assert
    execute_results.assert_results(expected_results=expected_results)

    assert "Using direct arguments: [" in caplog.text


def test_markdown_return_code_minimal_command_line_error(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a return code of 2 for COMMAND_LINE_ERROR is applied with the minimal scheme.

    This function shadows
    test_markdown_return_code_default_command_line_error
    """

    # Arrange
    supplied_arguments = ["--return-code-scheme", "minimal", "scan", "-l"]

    expected_results = ExpectedResults(
        return_code=2,
        expected_error="""usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS]
                    [-e PATH_EXCLUSIONS] [--respect-gitignore]
                    path [path ...]
main.py scan: error: the following arguments are required: path
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_return_code_minimal_fixed_at_least_one_file(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a return code of 0 for FIXED_AT_LEAST_ONE_FILE is applied with the minimal scheme.

    This function shadows
    test_markdown_return_code_default_fixed_at_least_one_file
    """

    # Arrange
    source_path, _ = __generate_source_path("good_unordered_list_item_empty_lines.md")
    with copy_to_temp_file(source_path) as temp_source_path:
        supplied_arguments = [
            "--set",
            "plugins.md009.strict=$!True",
            "--set",
            "plugins.md009.list_item_empty_lines=$!True",
            "--strict-config",
            "--return-code-scheme",
            "minimal",
            "fix",
            temp_source_path,
        ]

        expected_results = ExpectedResults(expected_output=f"Fixed: {temp_source_path}")
        # expected_file_contents = generate_md009_expected_contents(temp_source_path, 2)

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)
        # assert_file_is_as_expected(temp_source_path, expected_file_contents)


def test_markdown_return_code_minimal_scan_triggered_at_least_once(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a return code of 0 for SCAN_TRIGGERED_AT_LEAST_ONCE is applied with the minimal scheme.

    This function shadows
    test_markdown_return_code_default_scan_triggered_at_least_once
    """

    # Arrange
    source_path, absolute_source_path = __generate_source_path(
        "good_unordered_list_item_empty_lines.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.strict=$!True",
        "--strict-config",
        "--return-code-scheme",
        "minimal",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        expected_output=f"""{absolute_source_path}:2:1: MD009: Trailing spaces [Expected: 0; Actual: 2] (no-trailing-spaces)"""
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_return_code_minimal_system_error(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a return code of 1 for SYSTEM_ERROR is applied with the minimal scheme.

    This function shadows
    test_markdown_return_code_default_system_error
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md", "md047")
    supplied_arguments = [
        "--add-plugin",
        "MD047",
        "--return-code-scheme",
        "minimal",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while loading plugins:
Plugin path 'MD047' does not exist.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)
