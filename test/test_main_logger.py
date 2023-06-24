"""
Module to provide tests related to logging.
"""
import logging
import os
import tempfile
from test.markdown_scanner import MarkdownScanner

from pymarkdown.container_blocks.container_indices import ContainerIndices
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.stack_token import StackToken

from .utils import write_temporary_configuration

POGGER = ParserLogger(logging.getLogger(__name__))


def test_markdown_with_dash_dash_log_level_debug(caplog):
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


def test_markdown_with_dash_dash_log_level_info(caplog):
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


def test_markdown_with_dash_dash_log_level_invalid(caplog):
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
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE]
               {plugins,extensions,scan,scan-stdin,version} ...
main.py: error: argument --log-level: invalid __log_level_type value: 'invalid'
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


def test_markdown_with_dash_dash_log_level_info_with_file():
    # sourcery skip: extract-method
    """
    Test to make sure we get the right effect if the `--log-level` flag
    is set for info with the results going to a file.
    """

    # Arrange
    temp_file = None
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        log_file_name = temp_file.name

    try:
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

        with open(log_file_name, encoding="utf-8") as file:
            file_data = file.read().replace("\n", "")

        # Info messages
        assert "Number of files found: " in file_data, f">{file_data}<"
        assert f"Determining files to scan for path '{source_path}'." in file_data

        # Debug messages
        assert (
            f"Provided path '{source_path}' is a valid file. Adding." not in file_data
        )

    finally:
        if os.path.exists(log_file_name):
            os.remove(log_file_name)


def test_markdown_logger_stack_token_normal_output():
    """
    Test for normal output of the stack token for debug output.
    """

    # Arrange
    stack_token = StackToken("type", extra_data=None)

    # Act
    stack_token_string = str(stack_token)

    # Assert
    assert stack_token_string == "StackToken(type)"


def test_markdown_logger_stack_token_extra_output():
    """
    Test for extra output of the stack token for debug output.
    """

    # Arrange
    stack_token = StackToken("type", extra_data="abc")

    # Act
    stack_token_string = str(stack_token)

    # Assert
    assert stack_token_string == "StackToken(type:abc)"


def test_markdown_logger_container_indices():
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


def test_markdown_logger_active():
    """
    Since calls to it are commented out most of the time,
    test the debug_with_visible_whitespace function manually.
    """
    configuration_file_name = None
    new_handler = None
    root_logger = None
    file_as_lines = None
    try:
        configuration_file_name = write_temporary_configuration("")
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
        with open(configuration_file_name, encoding="utf-8") as file_to_parse:
            file_as_lines = file_to_parse.readlines()
        if configuration_file_name and os.path.exists(configuration_file_name):
            os.remove(configuration_file_name)

    assert len(file_as_lines) == 1
    assert file_as_lines[0] == "simple logging\n"


def test_markdown_logger_inactive():
    """
    Since calls to it are commented out most of the time,
    test the debug_with_visible_whitespace function manually.
    """
    configuration_file_name = None
    new_handler = None
    root_logger = None
    file_as_lines = None
    try:
        configuration_file_name = write_temporary_configuration("")
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
        with open(configuration_file_name, encoding="utf-8") as file_to_parse:
            file_as_lines = file_to_parse.readlines()
        if configuration_file_name and os.path.exists(configuration_file_name):
            os.remove(configuration_file_name)

    assert not file_as_lines


def test_markdown_logger_arg_list_not_out_of_sync():
    """
    Since calls to it are commented out most of the time,
    test the debug_with_visible_whitespace function manually.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    assert POGGER.is_enabled_for(logging.WARNING)
    new_logger = ParserLogger(logging.getLogger(__name__))
    new_logger.debug_with_visible_whitespace("one sub $ and one in list", " 1 ")


def test_markdown_logger_arg_list_not_out_of_sync_with_debug():
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
def test_markdown_logger_arg_list_out_of_sync():
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
