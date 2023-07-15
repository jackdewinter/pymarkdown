"""
Module for adding and configuring plugins through the API.
"""

import io
import os
import sys
from test.utils import write_temporary_configuration

from pymarkdown.api import (
    PyMarkdownApi,
    PyMarkdownApiArgumentException,
    PyMarkdownApiException,
    PyMarkdownScanFailure,
)


def test_api_plugins_add_with_empty_path():
    """
    Test to make sure that an empty path to add is reported as an error.
    """

    # Arrange
    source_path = ""
    plugin_path = ""

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().add_plugin_path(plugin_path).scan_path(source_path)
    except PyMarkdownApiArgumentException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.argument_name == "path_to_plugin"
    assert (
        caught_exception.reason == "Parameter named 'path_to_plugin' cannot be empty."
    )


def test_api_plugins_enable_with_empty_id():
    """
    Test to make sure that an empty identifier is raises an error.
    """

    # Arrange
    source_path = ""
    enable_identifier = ""

    # Act
    caught_exception = None
    try:
        _ = (
            PyMarkdownApi()
            .enable_rule_by_identifier(enable_identifier)
            .scan_path(source_path)
        )
    except PyMarkdownApiArgumentException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.argument_name == "rule_identifier"
    assert (
        caught_exception.reason == "Parameter named 'rule_identifier' cannot be empty."
    )


def test_api_plugins_disable_with_empty_id():
    """
    Test to make sure that an empty identifier is raises an error.
    """

    # Arrange
    source_path = ""
    enable_identifier = ""

    # Act
    caught_exception = None
    try:
        _ = (
            PyMarkdownApi()
            .disable_rule_by_identifier(enable_identifier)
            .scan_path(source_path)
        )
    except PyMarkdownApiArgumentException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.argument_name == "rule_identifier"
    assert (
        caught_exception.reason == "Parameter named 'rule_identifier' cannot be empty."
    )


def test_api_plugins_add_with_bad_path():
    """
    Test to make sure that an empty path to add is reported as an error.

    This function shadows
    test_markdown_with_dash_dash_add_plugin_and_bad_path
    """

    # Arrange
    source_path = "*.md"
    plugin_path = "MD047"

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().add_plugin_path(plugin_path).scan_path(source_path)
    except PyMarkdownApiException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == "BadPluginError encountered while loading plugins:\nPlugin path 'MD047' does not exist."
    )


def test_api_plugins_add_with_simple_plugin():
    """
    Test to make sure that a valid path causes a plugin to be loaded.
    Note that this plugin is a debug plugin, and outputs directly to stdout,
    which is not normal for plugins.

    This function shadows
    test_markdown_with_dash_dash_add_plugin_and_single_plugin_file
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = "test/resources/plugins/plugin_two.py"

    # Act
    std_output = io.StringIO()
    old_output = sys.stdout
    try:
        sys.stdout = std_output
        scan_result = (
            PyMarkdownApi().add_plugin_path(plugin_path).scan_path(source_path)
        )
    finally:
        sys.stdout = old_output

    # Assert
    assert scan_result
    assert not scan_result.scan_failures
    assert not scan_result.pragma_errors
    assert (
        std_output.getvalue()
        == """MD998>>init_from_config
MD998>>starting_new_file>>
MD998>>next_line:# This is a test
MD998>>next_line:
MD998>>next_line:The line after this line should be blank.
MD998>>next_line:
MD998>>completed_file
"""
    )


def test_api_plugins_add_with_simple_plugins_by_directory():
    """
    Test to make sure that a valid path to a directory causes any
    plugins in that directory to be loaded.
    Note that this plugin is a debug plugin, and outputs directly to stdout,
    which is not normal for plugins.

    This function shadows
    test_markdown_with_dash_dash_add_plugin_and_single_plugin_directory
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = "test/resources/plugins/"

    # Act
    std_output = io.StringIO()
    old_output = sys.stdout
    try:
        sys.stdout = std_output
        scan_result = (
            PyMarkdownApi().add_plugin_path(plugin_path).scan_path(source_path)
        )
    finally:
        sys.stdout = old_output

    # Assert
    assert scan_result
    assert not scan_result.scan_failures
    assert not scan_result.pragma_errors
    assert (
        std_output.getvalue()
        == """MD998>>init_from_config
MD998>>starting_new_file>>
MD998>>next_line:# This is a test
MD998>>next_line:
MD998>>next_line:The line after this line should be blank.
MD998>>next_line:
MD998>>completed_file
"""
    )


def test_api_plugins_add_with_repeated_identifier():
    """
    Test to make sure that a valid plugin with a bad identifier is handled.

    This function shadows
    test_markdown_with_repeated_identifier
    """

    # Arrange
    source_path = "*.md"
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "duplicate_id_debug.py"
    )

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().add_plugin_path(plugin_path).scan_path(source_path)
    except PyMarkdownApiException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == "ValueError encountered while initializing plugins:\nUnable to register plugin 'duplicate_id_debug.py' with id 'md999' as plugin 'plugin_one.py' is already registered with that id."
    )


def test_api_plugins_add_with_bad_starting_new_file():
    """
    Test to make sure that we handle an exception thrown during the starting_new_file function.

    This function shadows
    test_markdown_with_dash_dash_add_plugin_with_bad_starting_new_file
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_starting_new_file.py"
    )

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().add_plugin_path(plugin_path).scan_path(source_path)
    except PyMarkdownApiException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == f"BadPluginError encountered while scanning '{source_path}':\nPlugin id 'MDE001' had a critical failure during the 'starting_new_file' action."
    )


def test_api_plugins_add_with_bad_next_token():
    """
    Test to make sure that we handle an exception thrown during the next_token function.

    This function shadows
    test_markdown_with_dash_dash_add_plugin_with_bad_next_token
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_next_token.py"
    )

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().add_plugin_path(plugin_path).scan_path(source_path)
    except PyMarkdownApiException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == f"BadPluginError encountered while scanning '{source_path}':\n(1,1): Plugin id 'MDE003' had a critical failure during the 'next_token' action."
    )


def test_api_plugins_add_with_bad_next_token_and_stack_trace():
    """
    Test to make sure that we handle an exception thrown during the next_token function,
    along with a stack trace.

    This function shadows
    test_markdown_with_dash_dash_add_plugin_with_bad_next_token_with_stack_trace
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_next_token.py"
    )

    # Act
    caught_exception = None
    try:
        _ = (
            PyMarkdownApi()
            .enable_stack_trace()
            .add_plugin_path(plugin_path)
            .scan_path(source_path)
        )
    except PyMarkdownApiException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.reason.startswith(
        """BadPluginError encountered while scanning '{path}':
(1,1): Plugin id 'MDE003' had a critical failure during the 'next_token' action.""".replace(
            "{path}", source_path
        )
    )


# Actual Token: [atx(1,1):1:0:]
# Traceback (most recent call last):
#  File"""


def test_api_plugins_add_with_bad_load_due_to_configuration():
    """
    Test to make sure that we handle any exceptions raised during the configuration of plugins.

    This function shadows
    test_markdown_with_dash_dash_add_plugin_with_bad_string_detail_from_configuration
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_string_detail_is_int.py"
    )
    supplied_configuration = {"plugins": {"additional_paths": plugin_path}}

    # Act
    caught_exception = None
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        _ = (
            PyMarkdownApi()
            .configuration_file_path(configuration_file)
            .scan_path(source_path)
        )
    except PyMarkdownApiException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.reason == (
        """BadPluginError encountered while loading plugins:
Plugin class 'BadStringDetailIsInt' returned an improperly typed value for field name 'plugin_description'."""
    )


def test_api_plugins_disable_multiple_enable_one():
    """
    Test to make sure that we can disable multiple plugins if needed.

    This function shadows
    test_md002_all_samples
    """

    # Arrange
    source_path = os.path.join("test", "resources", "rules", "md002") + os.sep
    source_path_1 = os.path.join(source_path, "improper_atx_heading_start.md")
    source_path_2 = os.path.join(source_path, "improper_setext_heading_start.md")

    # Act
    scan_result = (
        PyMarkdownApi()
        .disable_rule_by_identifier("MD003")
        .disable_rule_by_identifier("MD041")
        .enable_rule_by_identifier("MD002")
        .scan_path(source_path)
    )

    # Assert
    assert scan_result
    assert len(scan_result.scan_failures) == 2
    assert scan_result.scan_failures[0].partial_equals(
        PyMarkdownScanFailure(source_path_1, 1, 1, "MD002", "", "", None)
    )
    assert scan_result.scan_failures[1].partial_equals(
        PyMarkdownScanFailure(source_path_2, 2, 1, "MD002", "", "", None)
    )
    assert not scan_result.pragma_errors
