"""
Module to provide tests related to logging.
"""

import logging
import os
import tempfile
from test.markdown_scanner import MarkdownScanner

from pytest import LogCaptureFixture

from pymarkdown.application_logging import ApplicationLogging
from pymarkdown.container_blocks.container_indices import ContainerIndices
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.tokens.stack_token import StackToken

from .utils import (
    assert_file_is_as_expected,
    create_temporary_configuration_file,
    create_temporary_file_for_reuse,
    read_contents_of_text_file,
)

POGGER = ParserLogger(logging.getLogger(__name__))


def test_markdown_with_dash_dash_log_level_debug(caplog: LogCaptureFixture) -> None:
    """
    Test to make sure we get the right effect if the `--log-level` flag
    is set for debug.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "--log-level",
        "DEBUG",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = """"""

    # Act
    ParserLogger.sync_on_next_call()
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

    # Info messages
    assert "Number of files found: " in caplog.text
    assert f"Determining files to scan for path '{source_path}'." in caplog.text

    # Debug messages
    assert f"Provided path '{source_path}' is a valid file. Adding." in caplog.text


def test_markdown_with_dash_dash_log_level_info(caplog: LogCaptureFixture) -> None:
    """
    Test to make sure we get the right effect if the `--log-level` flag
    is set for info.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "--log-level",
        "INFO",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    ParserLogger.sync_on_next_call()
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

    # Info messages
    assert "Number of files found: " in caplog.text
    assert f"Determining files to scan for path '{source_path}'." in caplog.text

    # Debug messages
    assert f"Provided path '{source_path}' is a valid file. Adding." not in caplog.text


def test_markdown_with_dash_dash_log_level_invalid(caplog: LogCaptureFixture) -> None:
    """
    Test to make sure we get the right effect if the `--log-level` flag
    is set for an invalid log level.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "--log-level",
        "invalid",
        "scan",
        source_path,
    ]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py [-h] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--set SET_CONFIGURATION] [--strict-config] [--stack-trace]
               [--continue-on-error]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE] [--return-code-scheme {default,minimal}]
               {extensions,fix,plugins,scan,scan-stdin,version} ...
main.py: error: argument --log-level: invalid validate_log_level_type value: 'invalid'
"""

    # Act
    ParserLogger.sync_on_next_call()
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

    # Info messages
    assert "Number of scanned files found: " not in caplog.text
    assert (
        "Determining files to scan for path "
        + "'test/resources/rules/md047/end_with_blank_line.md'."
        not in caplog.text
    )

    # Debug messages
    assert (
        "Provided path 'test/resources/rules/md047/end_with_blank_line.md' "
        + "is a valid Markdown file. Adding."
        not in caplog.text
    )


def test_markdown_with_dash_dash_log_level_info_with_file() -> None:
    # sourcery skip: extract-method
    """
    Test to make sure we get the right effect if the `--log-level` flag
    is set for info with the results going to a file.

    This function is shadowed in test_api_simple_clean_scan.
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    with create_temporary_file_for_reuse() as log_file_name:
        scanner = MarkdownScanner()
        supplied_arguments = [
            "--log-level",
            "INFO",
            "--log-file",
            log_file_name,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        ParserLogger.sync_on_next_call()
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )

        file_data = read_contents_of_text_file(log_file_name).replace("\n", "")

        # Info messages
        assert "Number of files found: " in file_data, f">{file_data}<"
        assert f"Determining files to scan for path '{source_path}'." in file_data

        # Debug messages
        assert (
            f"Provided path '{source_path}' is a valid file. Adding." not in file_data
        )


def test_markdown_with_dash_dash_log_level_info_with_file_as_directory() -> None:
    """
    Test to make sure we get the right effect if a directory is specified
    as the file to log to.

    This is shadowed by
    test_api_logging_debug_to_file_as_directory
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    with tempfile.TemporaryDirectory() as temp_directory:
        log_file_name = temp_directory

        scanner = MarkdownScanner()
        supplied_arguments = [
            "--log-file",
            log_file_name,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = "Unexpected Error(ApplicationLoggingException): Failure initializing logging subsystem."

        # Act
        ParserLogger.sync_on_next_call()
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_logger_stack_token_normal_output() -> None:
    """
    Test for normal output of the stack token for debug output.
    """

    # Arrange
    stack_token = StackToken("type", extra_data=None)

    # Act
    stack_token_string = str(stack_token)

    # Assert
    assert stack_token_string == "StackToken(type)"


def test_markdown_logger_stack_token_extra_output() -> None:
    """
    Test for extra output of the stack token for debug output.
    """

    # Arrange
    stack_token = StackToken("type", extra_data="abc")

    # Act
    stack_token_string = str(stack_token)

    # Assert
    assert stack_token_string == "StackToken(type:abc)"


def test_markdown_logger_container_indices() -> None:
    """
    Test for ContainerIndices class for output
    """

    # Arrange
    container_indices = ContainerIndices(1, 2, 3)

    # Act
    container_indices_string = str(container_indices)

    # Assert
    assert (
        container_indices_string
        == "{ContainerIndices:ulist_index:1;olist_index:2;block_index:3}"
    )


def test_markdown_logger_active() -> None:
    """
    Since calls to it are commented out most of the time,
    test the debug_with_visible_whitespace function manually.
    """
    configuration_file_name = None
    new_handler = None
    root_logger = None
    file_as_lines = None
    with create_temporary_configuration_file("") as configuration_file_name:
        try:
            new_handler = logging.FileHandler(configuration_file_name)

            root_logger = logging.getLogger()
            root_logger.setLevel(logging.DEBUG)
            root_logger.addHandler(new_handler)

            assert POGGER.is_enabled_for(logging.DEBUG)
            new_logger = ParserLogger(logging.getLogger(__name__))
            new_logger.debug("simple logging")
        finally:
            if root_logger and new_handler:
                root_logger.removeHandler(new_handler)
                new_handler.close()

            file_as_lines = read_contents_of_text_file(configuration_file_name).split(
                "\n"
            )

    assert len(file_as_lines) == 2
    assert file_as_lines[0] == "simple logging"
    assert file_as_lines[1] == ""


def test_markdown_logger_inactive() -> None:
    """
    Since calls to it are commented out most of the time,
    test the debug_with_visible_whitespace function manually.
    """
    configuration_file_name = None
    new_handler = None
    root_logger = None
    with create_temporary_configuration_file("") as configuration_file_name:
        try:
            new_handler = logging.FileHandler(configuration_file_name)

            root_logger = logging.getLogger()
            root_logger.setLevel(logging.WARNING)
            root_logger.addHandler(new_handler)

            assert POGGER.is_enabled_for(logging.WARNING)
            new_logger = ParserLogger(logging.getLogger(__name__))
            new_logger.debug("simple logging")
        finally:
            if root_logger and new_handler:
                root_logger.removeHandler(new_handler)
                new_handler.close()
            file_contents = read_contents_of_text_file(configuration_file_name)

    assert not file_contents


def test_markdown_logger_arg_list_not_out_of_sync() -> None:
    """
    Since calls to it are commented out most of the time,
    test the debug_with_visible_whitespace function manually.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    assert POGGER.is_enabled_for(logging.WARNING)
    new_logger = ParserLogger(logging.getLogger(__name__))
    new_logger.debug_with_visible_whitespace("one sub $ and one in list", " 1 ")


def test_markdown_logger_arg_list_not_out_of_sync_with_debug() -> None:
    """
    Since calls to it are commented out most of the time,
    test the debug_with_visible_whitespace function manually.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    assert POGGER.is_enabled_for(logging.DEBUG)
    new_logger = ParserLogger(logging.getLogger(__name__))
    new_logger.debug_with_visible_whitespace("one sub $ and one in list", " 1 ")


# pylint: disable=broad-exception-caught
def test_markdown_logger_arg_list_out_of_sync() -> None:
    """
    Test to verify that if we don't have the same number of
    $ characters in the string as arguments in the list, an
    exception with be thrown.
    """

    # Arrange
    try:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        assert POGGER.is_enabled_for(logging.DEBUG)
        new_logger = ParserLogger(logging.getLogger(__name__))
        new_logger.debug("one sub $ but two in list", 1, 2)
        raise AssertionError("An exception should have been thrown by now.")
    except Exception as this_exception:
        assert (
            str(this_exception)
            == "The number of $ substitution characters does not equal the number of arguments in the list."
        )


# pylint: enable=broad-exception-caught


def test_markdown_logger_translate_log_level_valid() -> None:
    """
    Test to make sure that we can translate a valid logging level to its numeric counterpart.
    """

    # Arrange
    log_level_as_string = "DEBUG"

    # Act
    log_level = ApplicationLogging.translate_log_level(log_level_as_string)

    # Assert
    assert log_level == logging.DEBUG


def test_markdown_logger_translate_log_level_invalid() -> None:
    """
    Test to make sure that we can translate an invalid logging level to NOTSET
    to indicate it was bad.
    """

    # Arrange
    log_level_as_string = "other"

    # Act
    log_level = ApplicationLogging.translate_log_level(log_level_as_string)

    # Assert
    assert log_level == logging.NOTSET


def test_markdown_fix_with_no_rescan_log_debug(caplog: LogCaptureFixture) -> None:
    """
    Test that is a mirror of test_md005_bad_unordered_list_single_level_fix with
    slight changes to test logging.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """* Item 1
 * Item 2
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "--log-level",
            "DEBUG",
            "-x-fix-no-rescan-log",
            "fix",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """* Item 1
* Item 2
"""

        # Act
        ParserLogger.sync_on_next_call()
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)

        # Info messages
        assert "Number of files found: " in caplog.text
        assert (
            f"Determining files to scan for path '{temp_source_path}'." in caplog.text
        )

        # Debug messages
        assert (
            f"Provided path '{temp_source_path}' is a valid file. Adding."
            in caplog.text
        )

        # Warning messages
        assert (
            "Setting logging level to WARN during rescan upon request." in caplog.text
        )
        assert "Restoring log level to DEBUG." in caplog.text


def test_markdown_fix_with_no_rescan_log_info(caplog: LogCaptureFixture) -> None:
    """
    Test that is a mirror of test_md005_bad_unordered_list_single_level_fix with
    slight changes to test logging.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """* Item 1
 * Item 2
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "--log-level",
            "INFO",
            "-x-fix-no-rescan-log",
            "fix",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """* Item 1
* Item 2
"""

        # Act
        ParserLogger.sync_on_next_call()
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)

        # Info messages
        assert "Number of files found: " in caplog.text
        assert (
            f"Determining files to scan for path '{temp_source_path}'." in caplog.text
        )

        # Debug messages
        # assert f"Provided path '{temp_source_path}' is a valid file. Adding." in caplog.text

        # Warning messages
        assert (
            "Setting logging level to WARN during rescan upon request." in caplog.text
        )
        assert "Restoring log level to INFO." in caplog.text


def test_markdown_fix_with_no_rescan_log_warn(caplog: LogCaptureFixture) -> None:
    """
    Test that is a mirror of test_md005_bad_unordered_list_single_level_fix with
    slight changes to test logging.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """* Item 1
 * Item 2
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md007,md029",
            "--log-level",
            "WARNING",
            "-x-fix-no-rescan-log",
            "fix",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """* Item 1
* Item 2
"""

        # Act
        ParserLogger.sync_on_next_call()
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)

        # Info messages
        # assert "Number of files found: " in caplog.text
        # assert f"Determining files to scan for path '{temp_source_path}'." in caplog.text

        # Debug messages
        # assert f"Provided path '{temp_source_path}' is a valid file. Adding." in caplog.text

        # Warning messages
        assert (
            "Setting logging level to WARN during rescan upon request." in caplog.text
        )
        assert "Restoring log level to WARNING." in caplog.text
