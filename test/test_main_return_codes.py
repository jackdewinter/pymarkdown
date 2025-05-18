"""
Module to test that the return code schemes are set up properly.
"""

import os
import runpy
from test.markdown_scanner import MarkdownScanner
from test.utils import (
    assert_file_is_as_expected,
    copy_to_temp_file,
    create_temporary_configuration_file,
)


def test_markdown_return_code_command_line_bad():
    """
    Test to...
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["--return-code-scheme", "invalid", "scan"]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py [-h] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--set SET_CONFIGURATION] [--strict-config] [--stack-trace]
               [--continue-on-error]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE] [--return-code-scheme {default,minimal}]
               {extensions,fix,plugins,scan,scan-stdin,version} ...
main.py: error: argument --return-code-scheme: invalid __validate_return_code_scheme value: 'invalid'"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_return_code_default_success():
    """
    Test to make sure a return code of 0 for SUCCESS is a default.

    This function shadows
    test_markdown_with_version
    and is shadowed by
    test_markdown_return_code_minimal_success
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["version"]

    version_path = os.path.join(".", "pymarkdown", "version.py")
    version_meta = runpy.run_path(version_path)
    semantic_version = version_meta["__version__"]

    expected_return_code = 0
    expected_output = """{version}
""".replace(
        "{version}", semantic_version
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_return_code_default_no_files_to_scan(caplog):
    """
    Test to make sure a return code of 1 for NO_FILES_TO_SCAN is a default.

    This function shadows
    test_markdown_with_direct_args
    and is shadowed by
    test_markdown_return_code_minimal_no_files_to_scan
    """

    # Arrange
    scanner = MarkdownScanner(use_main=False)
    supplied_arguments = ["--log-level", "DEBUG", "scan", "does-not-exist.md"]

    expected_return_code = 1
    expected_output = ""
    expected_error = """Provided path 'does-not-exist.md' does not exist.


No matching files found."""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, use_direct_arguments=True
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

    assert "Using direct arguments: [" in caplog.text


def test_markdown_return_code_default_command_line_error():
    """
    Test to make sure a return code of 2 for COMMAND_LINE_ERROR is a default.

    This function shadows
    test_markdown_with_dash_l_only
    and is shadowed by
    test_markdown_return_code_minimal_command_line_error
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["scan", "-l"]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS]
                    [-e PATH_EXCLUSIONS]
                    path [path ...]
main.py scan: error: the following arguments are required: path
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_return_code_default_fixed_at_least_one_file():
    """
    Test to make sure a return code of 3 for FIXED_AT_LEAST_ONE_FILE is a default.

    This function shadows
    test_md009 fix good_unordered_list_item_empty_lines_with_config_strict without the list_item_empty_lines config
    and is shadowed by
    test_markdown_return_code_minimal_fixed_at_least_one_file
    """

    # Arrange
    scanner = MarkdownScanner()
    source_file_contents = """- list item text
\a\a
  list item text
""".replace(
        "\a", " "
    )
    with create_temporary_configuration_file(
        source_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--set",
            "plugins.md009.strict=$!True",
            "--strict-config",
            "fix",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = """- list item text

  list item text
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


def test_markdown_return_code_default_scan_triggered_at_least_once():
    """
    Test to make sure a return code of 1 for SCAN_TRIGGERED_AT_LEAST_ONCE is a default.

    This function shadows
    test_md009_good_unordered_list_item_empty_lines_with_config_strict
    and is shadowed by
    test_markdown_return_code_minimal_scan_triggered_at_least_once
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_unordered_list_item_empty_lines.md"
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
        f"{source_path}:2:1: "
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


def test_markdown_return_code_default_system_error():
    """
    Test to make sure a return code of 1 for SYSTEM_ERROR is a default.

    This function shadows
    test_markdown_with_dash_dash_add_plugin_and_bad_path
    and is shadowed by
    test_markdown_return_code_minimal_system_error
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "--add-plugin",
        "MD047",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while loading plugins:\n"
        + "Plugin path 'MD047' does not exist.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_return_code_minimal_success():
    """
    Test to make sure a return code of 0 for SUCCESS is applied with the minimal scheme.

    This function shadows
    test_markdown_return_code_default_success
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["--return-code-scheme", "minimal", "version"]

    version_path = os.path.join(".", "pymarkdown", "version.py")
    version_meta = runpy.run_path(version_path)
    semantic_version = version_meta["__version__"]

    expected_return_code = 0
    expected_output = """{version}
""".replace(
        "{version}", semantic_version
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_return_code_minimal_no_files_to_scan(caplog):
    """
    Test to make sure a return code of 0 for NO_FILES_TO_SCAN is applied with the minimal scheme.

    This function shadows
    test_markdown_return_code_default_no_files_to_scan
    """

    # Arrange
    scanner = MarkdownScanner(use_main=False)
    supplied_arguments = [
        "--log-level",
        "DEBUG",
        "--return-code-scheme",
        "minimal",
        "scan",
        "does-not-exist.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = """Provided path 'does-not-exist.md' does not exist.


No matching files found."""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, use_direct_arguments=True
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

    assert "Using direct arguments: [" in caplog.text


def test_markdown_return_code_minimal_command_line_error():
    """
    Test to make sure a return code of 2 for COMMAND_LINE_ERROR is applied with the minimal scheme.

    This function shadows
    test_markdown_return_code_default_command_line_error
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["--return-code-scheme", "minimal", "scan", "-l"]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS]
                    [-e PATH_EXCLUSIONS]
                    path [path ...]
main.py scan: error: the following arguments are required: path
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_return_code_minimal_fixed_at_least_one_file():
    """
    Test to make sure a return code of 0 for FIXED_AT_LEAST_ONE_FILE is applied with the minimal scheme.

    This function shadows
    test_markdown_return_code_default_fixed_at_least_one_file
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md009",
            "good_unordered_list_item_empty_lines.md",
        )
    ) as temp_source_path:
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

        expected_return_code = 0
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        # expected_file_contents = generate_md009_expected_contents(temp_source_path, 2)

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        # assert_file_is_as_expected(temp_source_path, expected_file_contents)


def test_markdown_return_code_minimal_scan_triggered_at_least_once():
    """
    Test to make sure a return code of 0 for SCAN_TRIGGERED_AT_LEAST_ONCE is applied with the minimal scheme.

    This function shadows
    test_markdown_return_code_default_scan_triggered_at_least_once
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_unordered_list_item_empty_lines.md"
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

    expected_return_code = 0
    expected_output = (
        f"{source_path}:2:1: "
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


def test_markdown_return_code_minimal_system_error():
    """
    Test to make sure a return code of 1 for SYSTEM_ERROR is applied with the minimal scheme.

    This function shadows
    test_markdown_return_code_default_system_error
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "--add-plugin",
        "MD047",
        "--return-code-scheme",
        "minimal",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while loading plugins:\n"
        + "Plugin path 'MD047' does not exist.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
