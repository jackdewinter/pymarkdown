"""
Module for directly using PyMarkdown's API with logging enabled.

Most of these functions use the test_api_list_single_file function
and the test_api_list_for_non_existant_file function test data to test logging.
"""

import io
import logging
import os
import tempfile
from test.utils import assert_if_lists_different

from pymarkdown.api import (
    PyMarkdownApi,
    PyMarkdownApiArgumentException,
    PyMarkdownApiException,
    PyMarkdownApiNoFilesFoundException,
    PyMarkdownApiNotSupportedException,
)
from pymarkdown.application_logging import ApplicationLogging


def test_api_logging_bad_value():
    """
    Test to make sure that we report a bad value being specified as a log level.
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    test_value = "Critical"

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().log(test_value).list_path(source_path)
    except PyMarkdownApiArgumentException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.argument_name == "log_level"
    assert (
        caught_exception.reason
        == "Parameter 'log_level' must be one of CRITICAL,ERROR,WARNING,INFO,DEBUG"
    )


def test_api_logging_single_file(caplog):
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


def test_api_logging_debug(caplog):
    """
    Test to make sure that we can invoke a list of a file with debug logging
    or higher specified.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = ["DEBUG", "INFO", "WARNING"]

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().log_debug_and_above().list_path(source_path)
    except PyMarkdownApiNoFilesFoundException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.reason == f"Provided path '{source_path}' does not exist."

    __ensure_log_levels_in_caplog_text(caplog.text, expected_log_levels)


def test_api_logging_debug_to_file():
    """
    Test to make sure that we can invoke a list of a file with debug logging
    or higher specified, and have it sent to a file.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = ["DEBUG", "INFO", "WARNING"]
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            log_path = temp_file.name

        # Act
        caught_exception = None
        try:
            _ = (
                PyMarkdownApi()
                .log_debug_and_above()
                .log_to_file(log_path)
                .list_path(source_path)
            )
        except PyMarkdownApiNoFilesFoundException as this_exception:
            caught_exception = this_exception

        # Assert
        assert caught_exception, "Should have thrown an exception."
        assert (
            caught_exception.reason == f"Provided path '{source_path}' does not exist."
        )

        __ensure_log_levels_in_log_file(log_path, expected_log_levels)
    finally:
        if os.path.exists(log_path):
            os.remove(log_path)


def test_api_logging_debug_to_file_as_directory():
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

        # Act
        caught_exception = None
        try:
            _ = (
                PyMarkdownApi()
                .log_debug_and_above()
                .log_to_file(log_path)
                .list_path(source_path)
            )
        except PyMarkdownApiException as this_exception:
            caught_exception = this_exception

        # Assert
        assert caught_exception, "Should have thrown an exception."
        assert (
            caught_exception.reason
            == "Unexpected Error(ApplicationLoggingException): Failure initializing logging subsystem."
        )


def test_api_logging_debug_to_file_as_directory_and_stack_trace():
    """
    Test to make sure that we can invoke the logging subsystem with
    the log file being a directory, and having it fail properly.
    """

    # Arrange
    source_path = "my-bad-path"
    with tempfile.TemporaryDirectory() as temp_directory:
        log_path = temp_directory

        # Act
        caught_exception = None
        try:
            _ = (
                PyMarkdownApi()
                .log_debug_and_above()
                .enable_stack_trace()
                .log_to_file(log_path)
                .list_path(source_path)
            )
        except PyMarkdownApiException as this_exception:
            caught_exception = this_exception

        # Assert
        assert caught_exception, "Should have thrown an exception."
        assert caught_exception.reason.startswith(
            "Unexpected Error(ApplicationLoggingException): Failure initializing logging subsystem.\nTraceback (most recent call last):"
        )


def test_api_logging_info(caplog):
    """
    Test to make sure that we can invoke a list of a file with info logging
    or higher specified.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = ["INFO", "WARNING"]

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().log_info_and_above().list_path(source_path)
    except PyMarkdownApiNoFilesFoundException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.reason == f"Provided path '{source_path}' does not exist."

    __ensure_log_levels_in_caplog_text(caplog.text, expected_log_levels)


def test_api_logging_warning(caplog):
    """
    Test to make sure that we can invoke a list of a file with warning logging
    or higher specified.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = ["WARNING"]

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().log_warning_and_above().list_path(source_path)
    except PyMarkdownApiNoFilesFoundException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.reason == f"Provided path '{source_path}' does not exist."

    __ensure_log_levels_in_caplog_text(caplog.text, expected_log_levels)


def test_api_logging_error(caplog):
    """
    Test to make sure that we can invoke a list of a file with error logging
    or higher specified.

    TODO Note that there is nothing currently that logs at error.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = []

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().log_error_and_above().list_path(source_path)
    except PyMarkdownApiNoFilesFoundException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.reason == f"Provided path '{source_path}' does not exist."

    __ensure_log_levels_in_caplog_text(caplog.text, expected_log_levels)


def test_api_logging_critical(caplog):
    """
    Test to make sure that we can invoke a list of a file with critical logging
    or higher specified.

    TODO Note that there is nothing currently that logs at critical.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = []

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().log_critical_and_above().list_path(source_path)
    except PyMarkdownApiNoFilesFoundException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.reason == f"Provided path '{source_path}' does not exist."

    __ensure_log_levels_in_caplog_text(caplog.text, expected_log_levels)


def test_api_logging_stack_trace_with_no_exception(caplog):
    """
    Test to make sure that turning on stack trace has an effect, even
    if no exception is registered.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = ["DEBUG", "INFO"]

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


def test_api_logging_inheriting_logging(caplog):
    """
    Test to make sure any logging set up external to the API is respected
    if the inherit_logging flag is passed.
    """

    # Arrange
    source_path = "my-bad-path"
    expected_log_levels = ["DEBUG", "INFO", "WARNING"]

    # Act
    old_log_level = logging.getLogger().level
    log_output = io.StringIO()
    new_handler = logging.StreamHandler(log_output)
    try:
        formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")
        new_handler.setFormatter(formatter)
        logging.getLogger().addHandler(new_handler)
        logging.getLogger().setLevel(
            ApplicationLogging.translate_log_level(ApplicationLogging.log_level_debug)
        )

        caught_exception = None
        try:
            _ = PyMarkdownApi(inherit_logging=True).list_path(source_path)
        except PyMarkdownApiNoFilesFoundException as this_exception:
            caught_exception = this_exception
    finally:
        logging.getLogger().setLevel(old_log_level)
        new_handler.close()

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.reason == f"Provided path '{source_path}' does not exist."

    __ensure_log_levels_in_caplog_text(log_output.getvalue(), expected_log_levels)
    __ensure_log_levels_in_caplog_text(caplog.text, expected_log_levels)


def test_api_logging_inheriting_logging_and_set_log_level():
    """
    Test to make sure that we get a proper exception if we ask for log
    inheritance and then try and set the log level.
    """

    # Arrange
    source_path = "my-bad-path"

    # Act
    caught_exception = None
    try:
        _ = (
            PyMarkdownApi(inherit_logging=True)
            .log_debug_and_above()
            .list_path(source_path)
        )
    except PyMarkdownApiNotSupportedException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == "Set log level functions are not supported in log-inheritance mode."
    )


def test_api_logging_inheriting_logging_and_set_log_file():
    """
    Test to make sure that we get a proper exception if we ask for log
    inheritance and then try and set the log file.
    """

    # Arrange
    source_path = "my-bad-path"

    # Act
    caught_exception = None
    try:
        _ = (
            PyMarkdownApi(inherit_logging=True)
            .log_to_file("bob")
            .list_path(source_path)
        )
    except PyMarkdownApiNotSupportedException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == "Set log file function is not supported in log-inheritance mode."
    )


def __ensure_log_levels_in_log_file(log_file_path, expected_log_levels):
    with open(log_file_path, "r", encoding="utf-8") as readme_file:
        log_file_text = readme_file.read()
        __ensure_log_levels_in_caplog_text(log_file_text, expected_log_levels)


def __ensure_log_levels_in_caplog_text(caplog_text, expected_log_levels):
    """
    For any emitted log information, the log level will always be the first
    piece of information on each line.  This simply ensures that all log level
    values that are expected are present at least once in the output.
    """

    found_levels = set()
    for next_line in caplog_text.split("\n"):
        split_next_line = next_line.split(" ")
        if split_next_line and split_next_line[0]:
            found_levels.add(split_next_line[0])

    for next_log_level in expected_log_levels:
        assert next_log_level in found_levels
        found_levels.remove(next_log_level)
    assert not found_levels
