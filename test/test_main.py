"""
Module to provide tests related to the basic parts of the scanner.
"""

import logging
import os
import runpy
import sys
from test.markdown_scanner import MarkdownScanner
from test.patches.patch_builtin_open import path_builtin_open_with_exception

from pymarkdown.general.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))

if sys.version_info < (3, 11):
    ARGPARSE_X = "optional arguments:"
    ENABLE_RULES_X = "-e ENABLE_RULES, --enable-rules ENABLE_RULES"
    DISABLE_RULES_X = "-d DISABLE_RULES, --disable-rules DISABLE_RULES"
    CONFIG_FILE_X = "--config CONFIGURATION_FILE, -c CONFIGURATION_FILE"
    SET_CONFIG_X = "--set SET_CONFIGURATION, -s SET_CONFIGURATION"
else:
    ARGPARSE_X = "options:"
    ENABLE_RULES_X = "-e, --enable-rules ENABLE_RULES"
    DISABLE_RULES_X = "-d, --disable-rules DISABLE_RULES"
    CONFIG_FILE_X = "--config, -c CONFIGURATION_FILE"
    SET_CONFIG_X = "--set, -s SET_CONFIGURATION"


def test_markdown_with_no_parameters():
    """
    Test to make sure we get the simple information if no parameters are supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = []

    expected_return_code = 2
    expected_output = (
        """usage: main.py [-h] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--set SET_CONFIGURATION] [--strict-config] [--stack-trace]
               [--continue-on-error]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE] [--return-code-scheme {default,minimal}]
               {extensions,fix,plugins,scan,scan-stdin,version} ...

Lint any found Markdown files.

positional arguments:
  {extensions,fix,plugins,scan,scan-stdin,version}
    extensions          extension commands
    fix                 fix the Markdown files in any specified paths
    plugins             plugin commands
    scan                scan the Markdown files in any specified paths
    scan-stdin          scan the standard input as a Markdown file
    version             version of the application

{ARGPARSE_X}
  -h, --help            show this help message and exit
  {ENABLE_RULES_X}
                        comma separated list of rules to enable
  {DISABLE_RULES_X}
                        comma separated list of rules to disable
  --add-plugin ADD_PLUGIN
                        path to a plugin containing a new rule to apply
  {CONFIG_FILE_X}
                        path to the configuration file to use
  {SET_CONFIG_X}
                        manually set an individual configuration property
  --strict-config       throw an error if configuration is bad, instead of
                        assuming default
  --stack-trace         if an error occurs, print out the stack trace for
                        debug purposes
  --continue-on-error   if a tokenization or plugin error occurs, allow
                        processing to continue
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        minimum level required to log messages
  --log-file LOG_FILE   destination file for log messages
  --return-code-scheme {default,minimal}
                        scheme to choose for selecting the application return
                        code""".replace(
            "{ARGPARSE_X}", ARGPARSE_X
        )
        .replace("{ENABLE_RULES_X}", ENABLE_RULES_X)
        .replace("{DISABLE_RULES_X}", DISABLE_RULES_X)
        .replace("{CONFIG_FILE_X}", CONFIG_FILE_X)
        .replace("{SET_CONFIG_X}", SET_CONFIG_X)
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_no_parameters_through_module():
    """
    Test to make sure we get the simple information if no parameters are supplied,
    but through the module interface.
    """

    # Arrange
    scanner = MarkdownScanner(use_module=True)
    supplied_arguments = []

    expected_return_code = 2
    expected_output = (
        """usage: __main.py__ [-h] [-e ENABLE_RULES] [-d DISABLE_RULES]
                   [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
                   [--set SET_CONFIGURATION] [--strict-config] [--stack-trace]
                   [--continue-on-error]
                   [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
                   [--log-file LOG_FILE]
                   [--return-code-scheme {default,minimal}]
                   {extensions,fix,plugins,scan,scan-stdin,version} ...

Lint any found Markdown files.

positional arguments:
  {extensions,fix,plugins,scan,scan-stdin,version}
    extensions          extension commands
    fix                 fix the Markdown files in any specified paths
    plugins             plugin commands
    scan                scan the Markdown files in any specified paths
    scan-stdin          scan the standard input as a Markdown file
    version             version of the application

{ARGPARSE_X}
  -h, --help            show this help message and exit
  {ENABLE_RULES_X}
                        comma separated list of rules to enable
  {DISABLE_RULES_X}
                        comma separated list of rules to disable
  --add-plugin ADD_PLUGIN
                        path to a plugin containing a new rule to apply
  {CONFIG_FILE_X}
                        path to the configuration file to use
  {SET_CONFIG_X}
                        manually set an individual configuration property
  --strict-config       throw an error if configuration is bad, instead of
                        assuming default
  --stack-trace         if an error occurs, print out the stack trace for
                        debug purposes
  --continue-on-error   if a tokenization or plugin error occurs, allow
                        processing to continue
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        minimum level required to log messages
  --log-file LOG_FILE   destination file for log messages
  --return-code-scheme {default,minimal}
                        scheme to choose for selecting the application return
                        code""".replace(
            "{ARGPARSE_X}", ARGPARSE_X
        )
        .replace("{ENABLE_RULES_X}", ENABLE_RULES_X)
        .replace("{DISABLE_RULES_X}", DISABLE_RULES_X)
        .replace("{CONFIG_FILE_X}", CONFIG_FILE_X)
        .replace("{SET_CONFIG_X}", SET_CONFIG_X)
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_no_parameters_through_main():
    """
    Test to make sure we get the simple information if no parameters are supplied,
    but through the main interface.
    """

    # Arrange
    scanner = MarkdownScanner(use_main=True)
    supplied_arguments = []

    expected_return_code = 2
    expected_output = (
        """usage: main.py [-h] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--set SET_CONFIGURATION] [--strict-config] [--stack-trace]
               [--continue-on-error]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE] [--return-code-scheme {default,minimal}]
               {extensions,fix,plugins,scan,scan-stdin,version} ...

Lint any found Markdown files.

positional arguments:
  {extensions,fix,plugins,scan,scan-stdin,version}
    extensions          extension commands
    fix                 fix the Markdown files in any specified paths
    plugins             plugin commands
    scan                scan the Markdown files in any specified paths
    scan-stdin          scan the standard input as a Markdown file
    version             version of the application

{ARGPARSE_X}
  -h, --help            show this help message and exit
  {ENABLE_RULES_X}
                        comma separated list of rules to enable
  {DISABLE_RULES_X}
                        comma separated list of rules to disable
  --add-plugin ADD_PLUGIN
                        path to a plugin containing a new rule to apply
  {CONFIG_FILE_X}
                        path to the configuration file to use
  {SET_CONFIG_X}
                        manually set an individual configuration property
  --strict-config       throw an error if configuration is bad, instead of
                        assuming default
  --stack-trace         if an error occurs, print out the stack trace for
                        debug purposes
  --continue-on-error   if a tokenization or plugin error occurs, allow
                        processing to continue
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        minimum level required to log messages
  --log-file LOG_FILE   destination file for log messages
  --return-code-scheme {default,minimal}
                        scheme to choose for selecting the application return
                        code""".replace(
            "{ARGPARSE_X}", ARGPARSE_X
        )
        .replace("{ENABLE_RULES_X}", ENABLE_RULES_X)
        .replace("{DISABLE_RULES_X}", DISABLE_RULES_X)
        .replace("{CONFIG_FILE_X}", CONFIG_FILE_X)
        .replace("{SET_CONFIG_X}", SET_CONFIG_X)
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_h():
    """
    Test to make sure we get help if '-h' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["-h"]

    expected_return_code = 0
    expected_output = (
        """usage: main.py [-h] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--set SET_CONFIGURATION] [--strict-config] [--stack-trace]
               [--continue-on-error]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE] [--return-code-scheme {default,minimal}]
               {extensions,fix,plugins,scan,scan-stdin,version} ...

Lint any found Markdown files.

positional arguments:
  {extensions,fix,plugins,scan,scan-stdin,version}
    extensions          extension commands
    fix                 fix the Markdown files in any specified paths
    plugins             plugin commands
    scan                scan the Markdown files in any specified paths
    scan-stdin          scan the standard input as a Markdown file
    version             version of the application

{ARGPARSE_X}
  -h, --help            show this help message and exit
  {ENABLE_RULES_X}
                        comma separated list of rules to enable
  {DISABLE_RULES_X}
                        comma separated list of rules to disable
  --add-plugin ADD_PLUGIN
                        path to a plugin containing a new rule to apply
  {CONFIG_FILE_X}
                        path to the configuration file to use
  {SET_CONFIG_X}
                        manually set an individual configuration property
  --strict-config       throw an error if configuration is bad, instead of
                        assuming default
  --stack-trace         if an error occurs, print out the stack trace for
                        debug purposes
  --continue-on-error   if a tokenization or plugin error occurs, allow
                        processing to continue
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        minimum level required to log messages
  --log-file LOG_FILE   destination file for log messages
  --return-code-scheme {default,minimal}
                        scheme to choose for selecting the application return
                        code""".replace(
            "{ARGPARSE_X}", ARGPARSE_X
        )
        .replace("{ENABLE_RULES_X}", ENABLE_RULES_X)
        .replace("{DISABLE_RULES_X}", DISABLE_RULES_X)
        .replace("{CONFIG_FILE_X}", CONFIG_FILE_X)
        .replace("{SET_CONFIG_X}", SET_CONFIG_X)
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_version():
    """
    Test to make sure we get help if 'version' is supplied.

    This function is shadowed by
    test_markdown_return_code_default_success.
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


def test_markdown_with_direct_args(caplog):
    """
    Test to make sure we can specify the arguments directly.

    This function is shadowed by
    test_markdown_return_code_default_no_files_to_scan.
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


def test_markdown_without_direct_args(caplog):
    """
    Test to make sure we can specify the arguments normally.

    This function is shadowed by test_api_scan_for_non_existant_file.
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
        arguments=supplied_arguments, use_direct_arguments=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

    assert "Using supplied command line arguments." in caplog.text


def test_markdown_with_failure_during_file_scan():
    """
    Test to make sure we get simulate a test scan exception.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]
    exception_path = os.path.abspath(
        os.path.join("pymarkdown", "resources", "entities.json")
    )

    expected_return_code = 1
    expected_output = ""
    expected_error = """
    
BadTokenizationError encountered while initializing tokenizer:
Named character entity map file '{source_path}' was not loaded (bob).
""".replace(
        "{source_path}", exception_path
    )

    # Act
    with path_builtin_open_with_exception(exception_path, "rt", IOError("bob"), True):
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_x_init():
    """
    Test to make sure we get simulate a test initialization exception if the
    `-x-init` flag is set.

    This function shadows
    test_api_tokenizer_init_exception
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    exception_path = os.path.join("pymarkdown", "resources", "entities.json")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadTokenizationError encountered while initializing tokenizer:\n"
        + f"Named character entity map file '{os.path.abspath(exception_path)}' was not loaded (blah)."
    )

    # Act
    with path_builtin_open_with_exception(
        os.path.abspath(exception_path), "rt", OSError("blah")
    ):
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


# TODO add Markdown parsing of some binary file to cause the tokenizer to throw an exception?


def test_markdown_with_multiple_errors_reported():
    """
    Test to make sure we properly sort errors from files.

    Variation on test_md020_bad_single_paragraph_with_whitespace_at_end
    with no rules disabled.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md020",
        "single_paragraph_with_whitespace_at_end.md",
    )
    expected_return_code = 1
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_output = (
        f"{source_path}:1:1: MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{source_path}:1:12: "
        + "MD010: Hard tabs "
        + "[Column: 12] (no-hard-tabs)\n"
        + f"{source_path}:2:2: "
        + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        + "(no-multiple-space-closed-atx)\n"
        + f"{source_path}:2:2: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{source_path}:2:2: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + f"{source_path}:2:14: "
        + "MD010: Hard tabs "
        + "[Column: 14] (no-hard-tabs)"
    )

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
