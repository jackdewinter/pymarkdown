"""
Module for directly using PyMarkdown's API with logging enabled.

Most of these functions use the test_api_list_single_file function
and the test_api_list_for_non_existant_file function test data to test logging.
"""

import logging
import os
import tempfile
from test.utils import (
    assert_if_lists_different,
    assert_that_exception_is_raised,
    assert_that_exception_is_raised2,
    capture_logging_changes_with_new_handler,
    create_temporary_file_for_reuse,
)
from typing import List, Set, cast

from pytest import LogCaptureFixture

from pymarkdown.api import (
    PyMarkdownApi,
    PyMarkdownApiArgumentException,
    PyMarkdownApiException,
    PyMarkdownApiNoFilesFoundException,
    PyMarkdownApiNotSupportedException,
)
from pymarkdown.application_logging import ApplicationLogging


def test_api_logging_bad_value() -> None:
    """
    Test to make sure that we report a bad value being specified as a log level.
    """

    # Arrange
    test_value = "Critical"
    expected_output = (
        "Parameter 'log_level' must be one of CRITICAL,ERROR,WARNING,INFO,DEBUG"
    )

    # Act & Assert
    caught_exception = assert_that_exception_is_raised(
        PyMarkdownApiArgumentException, expected_output, PyMarkdownApi().log, test_value
    )
    assert (
        cast(PyMarkdownApiArgumentException, caught_exception).argument_name
        == "log_level"
    )


def test_api_logging_single_file(caplog: LogCaptureFixture) -> None:
    """
    Test to make sure that we can invoke a list of a file with no logging
    specified at all.
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )

    # Act
    list_result = PyMarkdownApi().list_path(source_path)

    # Assert
    assert_if_lists_different(list_result.matching_files, [source_path])
    assert caplog.text == ""


def test_api_logging_debug(caplog: LogCaptureFixture) -> None:
    """
    Test to make sure that we can invoke a list of a file with debug logging
    or higher specified.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = ["DEBUG", "INFO", "WARNING"]

    expected_output = f"Provided path '{source_path}' does not exist."

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiNoFilesFoundException,
        expected_output,
        PyMarkdownApi().log_debug_and_above().list_path,
        source_path,
    )
    __ensure_log_levels_in_caplog_text(caplog.text, expected_log_levels)


def test_api_logging_debug_to_file() -> None:
    """
    Test to make sure that we can invoke a list of a file with debug logging
    or higher specified, and have it sent to a file.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = ["DEBUG", "INFO", "WARNING"]

    expected_output = f"Provided path '{source_path}' does not exist."

    with create_temporary_file_for_reuse() as log_path:
        # Act & Assert
        assert_that_exception_is_raised(
            PyMarkdownApiNoFilesFoundException,
            expected_output,
            PyMarkdownApi().log_debug_and_above().log_to_file(log_path).list_path,
            source_path,
        )
        __ensure_log_levels_in_log_file(log_path, expected_log_levels)


def test_api_logging_debug_to_file_as_directory() -> None:
    """
    Test to make sure that we can invoke the logging subsystem with
    the log file being a directory, and having it fail properly.

    This test shadows
    test_markdown_with_dash_dash_log_level_info_with_file_as_directory
    """

    # Arrange
    source_path = "my-bad-path"
    with tempfile.TemporaryDirectory() as temp_directory:
        log_path = temp_directory

        expected_output = "Unexpected Error(ApplicationLoggingException): Failure initializing logging subsystem."

        # Act & Assert
        assert_that_exception_is_raised(
            PyMarkdownApiException,
            expected_output,
            PyMarkdownApi().log_debug_and_above().log_to_file(log_path).list_path,
            source_path,
        )


def test_api_logging_debug_to_file_as_directory_and_stack_trace() -> None:
    """
    Test to make sure that we can invoke the logging subsystem with
    the log file being a directory, and having it fail properly.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_output = "Unexpected Error(ApplicationLoggingException): Failure initializing logging subsystem.\nTraceback (most recent call last):"

    with tempfile.TemporaryDirectory() as temp_directory:
        log_path = temp_directory

        # Act & Assert
        assert_that_exception_is_raised2(
            PyMarkdownApiException,
            expected_output,
            PyMarkdownApi()
            .log_debug_and_above()
            .enable_stack_trace()
            .log_to_file(log_path)
            .list_path,
            source_path,
        )


def test_api_logging_info(caplog: LogCaptureFixture) -> None:
    """
    Test to make sure that we can invoke a list of a file with info logging
    or higher specified.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = ["INFO", "WARNING"]
    expected_output = f"Provided path '{source_path}' does not exist."

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiNoFilesFoundException,
        expected_output,
        PyMarkdownApi().log_info_and_above().list_path,
        source_path,
    )
    __ensure_log_levels_in_caplog_text(caplog.text, expected_log_levels)


def test_api_logging_warning(caplog: LogCaptureFixture) -> None:
    """
    Test to make sure that we can invoke a list of a file with warning logging
    or higher specified.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = ["WARNING"]
    expected_output = f"Provided path '{source_path}' does not exist."

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiNoFilesFoundException,
        expected_output,
        PyMarkdownApi().log_warning_and_above().list_path,
        source_path,
    )
    __ensure_log_levels_in_caplog_text(caplog.text, expected_log_levels)


def test_api_logging_error(caplog: LogCaptureFixture) -> None:
    """
    Test to make sure that we can invoke a list of a file with error logging
    or higher specified.

    TODO Note that there is nothing currently that logs at error.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels: List[str] = []
    expected_output = f"Provided path '{source_path}' does not exist."

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiNoFilesFoundException,
        expected_output,
        PyMarkdownApi().log_error_and_above().list_path,
        source_path,
    )
    __ensure_log_levels_in_caplog_text(caplog.text, expected_log_levels)


def test_api_logging_critical(caplog: LogCaptureFixture) -> None:
    """
    Test to make sure that we can invoke a list of a file with critical logging
    or higher specified.

    TODO Note that there is nothing currently that logs at critical.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels: List[str] = []

    expected_output = f"Provided path '{source_path}' does not exist."

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiNoFilesFoundException,
        expected_output,
        PyMarkdownApi().log_critical_and_above().list_path,
        source_path,
    )
    __ensure_log_levels_in_caplog_text(caplog.text, expected_log_levels)


def test_api_logging_stack_trace_with_no_exception(caplog: LogCaptureFixture) -> None:
    """
    Test to make sure that turning on stack trace has an effect, even
    if no exception is registered.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = ["DEBUG", "INFO", "WARNING"]

    # Act
    try:
        _ = PyMarkdownApi().log_info_and_above().list_path(source_path)
    except PyMarkdownApiNoFilesFoundException:
        pass
    first_capture_text = caplog.text

    try:
        _ = (
            PyMarkdownApi()
            .log_info_and_above()
            .enable_stack_trace()
            .list_path(source_path)
        )
    except PyMarkdownApiNoFilesFoundException:
        pass
    second_capture_text = caplog.text

    # Assert

    # As caplog.text does not get reset, ensure that the second capture starts
    # with the first (asserting our assumption) and adjust the second to its
    # proper value.
    assert second_capture_text.startswith(first_capture_text)
    second_capture_text = second_capture_text[len(first_capture_text) :]

    # Now turn around and make sure that the second capture ends with the same
    # text as the first.  This only works because the logged error is not reporting
    # a raised error.
    assert second_capture_text.endswith(first_capture_text)

    # The difference between the two are any log entries added specifically due
    # to stack trace being enabled.
    diff_text = second_capture_text[: -len(first_capture_text)]
    __ensure_log_levels_in_caplog_text(diff_text, expected_log_levels)


# TODO version with exception


def test_api_logging_inheriting_logging(caplog: LogCaptureFixture) -> None:
    """
    Test to make sure any logging set up external to the API is respected
    if the inherit_logging flag is passed.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = ["DEBUG", "INFO", "WARNING"]

    # Act
    with capture_logging_changes_with_new_handler() as (new_handler, log_output):
        formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")
        new_handler.setFormatter(formatter)
        logging.getLogger().addHandler(new_handler)
        logging.getLogger().setLevel(
            ApplicationLogging.translate_log_level(ApplicationLogging.log_level_debug)
        )

        expected_output = f"Provided path '{source_path}' does not exist."

        assert_that_exception_is_raised(
            PyMarkdownApiNoFilesFoundException,
            expected_output,
            PyMarkdownApi(inherit_logging=True).list_path,
            source_path,
        )

    # Assert
    __ensure_log_levels_in_caplog_text(log_output.getvalue(), expected_log_levels)
    __ensure_log_levels_in_caplog_text(caplog.text, expected_log_levels)


def test_api_logging_inheriting_logging_and_set_log_level() -> None:
    """
    Test to make sure that we get a proper exception if we ask for log
    inheritance and then try and set the log level.
    """

    # Arrange
    expected_output = (
        "Set log level functions are not supported in log-inheritance mode."
    )

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiNotSupportedException,
        expected_output,
        PyMarkdownApi(inherit_logging=True).log_debug_and_above,
    )


def test_api_logging_inheriting_logging_and_set_log_file() -> None:
    """
    Test to make sure that we get a proper exception if we ask for log
    inheritance and then try and set the log file.
    """

    # Arrange
    expected_output = "Set log file function is not supported in log-inheritance mode."

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiNotSupportedException,
        expected_output,
        PyMarkdownApi(inherit_logging=True).log_to_file,
        "bob",
    )


def __ensure_log_levels_in_log_file(
    log_file_path: str, expected_log_levels: List[str]
) -> None:
    with open(log_file_path, "r", encoding="utf-8") as readme_file:
        log_file_text = readme_file.read()
        __ensure_log_levels_in_caplog_text(log_file_text, expected_log_levels)


def __ensure_log_levels_in_caplog_text(
    caplog_text: str, expected_log_levels: List[str]
) -> None:
    """
    For any emitted log information, the log level will always be the first
    piece of information on each line.  This simply ensures that all log level
    values that are expected are present at least once in the output.
    """

    found_levels: Set[str] = set()
    for next_line in caplog_text.split("\n"):
        split_next_line = next_line.split(" ")
        if split_next_line and split_next_line[0]:
            found_levels.add(split_next_line[0])

    for next_log_level in expected_log_levels:
        assert next_log_level in found_levels
        found_levels.remove(next_log_level)
    assert not found_levels
