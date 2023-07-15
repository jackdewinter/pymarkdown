"""
Module for specifying a configuration file through the API.
"""

import io
import os
import sys
import tempfile
from test.utils import write_temporary_configuration

from pymarkdown.api import (
    PyMarkdownApi,
    PyMarkdownApiArgumentException,
    PyMarkdownApiException,
)


def test_api_config_with_empty_path():
    """
    Test to make sure that an empty path to add is reported as an error.
    """

    # Arrange
    source_path = ""
    configuration_path = ""

    # Act
    caught_exception = None
    try:
        _ = (
            PyMarkdownApi()
            .configuration_file_path(configuration_path)
            .scan_path(source_path)
        )
    except PyMarkdownApiArgumentException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.argument_name == "path_to_config_file"
    assert (
        caught_exception.reason
        == "Parameter named 'path_to_config_file' cannot be empty."
    )


def test_api_config_with_bad_path():
    """
    Test to make sure that a bad configuration path to add is reported as an error.

    This function shadows
    test_markdown_with_dash_e_single_by_id_and_non_present_config_file
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    configuration_file = "not-exists"

    # Act
    caught_exception = None
    try:
        _ = (
            PyMarkdownApi()
            .configuration_file_path(configuration_file)
            .scan_path(source_path)
        )
    except PyMarkdownApiException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert caught_exception.reason.startswith(
        "Specified configuration file 'not-exists' was not loaded:"
    )


def test_api_config_with_bad_contents():
    """
    Test to make sure that a configuration file with bad contents is reported as an error.

    This function shadows
    test_markdown_with_dash_e_single_by_id_and_non_json_config_file
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = "not a json file"
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)

        # Act
        caught_exception = None
        try:
            _ = (
                PyMarkdownApi()
                .configuration_file_path(configuration_file)
                .scan_path(source_path)
            )
        except PyMarkdownApiException as this_exception:
            caught_exception = this_exception
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == f"Specified configuration file '{configuration_file}' is not a valid JSON file: Expecting value: line 1 column 1 (char 0)."
    )


def test_api_config_with_config_file_with_good_value():
    """
    Test to make sure that a configuration file with a good value is interpretted
    as such.

    This function shadows
    test_markdown_with_dash_e_single_by_id_and_good_select_config
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"other_test_value": 2}}}
    configuration_file = None
    std_output = io.StringIO()
    old_output = sys.stdout
    try:
        sys.stdout = std_output
        configuration_file = write_temporary_configuration(supplied_configuration)

        # Act
        scan_result = (
            PyMarkdownApi()
            .enable_rule_by_identifier("MD999")
            .configuration_file_path(configuration_file)
            .scan_path(source_path)
        )
    finally:
        sys.stdout = old_output
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)

    # Assert
    assert scan_result
    assert not scan_result.scan_failures
    assert not scan_result.pragma_errors
    assert (
        std_output.getvalue()
        == """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>2
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>completed_file
"""
    )


def test_api_config_with_config_file_with_bad_value():
    """
    Test to make sure that a configuration file with a bad value is interpretted
    as such.

    This function shadows
    test_markdown_with_dash_e_single_by_id_and_bad_select_config
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"other_test_value": 9}}}
    configuration_file = None
    std_output = io.StringIO()
    old_output = sys.stdout
    try:
        sys.stdout = std_output
        configuration_file = write_temporary_configuration(supplied_configuration)

        # Act
        scan_result = (
            PyMarkdownApi()
            .enable_rule_by_identifier("MD999")
            .configuration_file_path(configuration_file)
            .scan_path(source_path)
        )
    finally:
        sys.stdout = old_output
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)

    # Assert
    assert scan_result
    assert not scan_result.scan_failures
    assert not scan_result.pragma_errors
    assert (
        std_output.getvalue()
        == """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>completed_file
"""
    )


def test_api_config_with_good_strict_and_bad_config():
    """
    Test to make sure that a configuration file with bad contents is reported as an error.

    This function shadows
    test_markdown_with_good_strict_config_type
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"mode": {"strict-config": True}, "log": {"file": 0}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)

        # Act
        caught_exception = None
        try:
            _ = (
                PyMarkdownApi()
                .configuration_file_path(configuration_file)
                .scan_path(source_path)
            )
        except PyMarkdownApiException as this_exception:
            caught_exception = this_exception
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == "Configuration Error: The value for property 'log.file' must be of type 'str'."
    )


def test_api_config_with_bad_strict_and_bad_config():
    """
    Test to make sure that a configuration file with bad contents is reported as an error.

    This function shadows
    test_markdown_with_bad_strict_config_type
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"mode": {"strict-config": 2}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)

        # Act
        caught_exception = None
        try:
            _ = (
                PyMarkdownApi()
                .configuration_file_path(configuration_file)
                .scan_path(source_path)
            )
        except PyMarkdownApiException as this_exception:
            caught_exception = this_exception
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == "Configuration Error: The value for property 'mode.strict-config' must be of type 'bool'."
    )


def test_api_config_with_exception_during_confiuguration():
    """
    Test to make sure that a configuration file...

    This function shadows
    test_markdown_with_dash_e_single_by_id_and_config_causing_config_exception
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": 10}}}
    configuration_file = None
    std_output = io.StringIO()
    old_output = sys.stdout
    try:
        sys.stdout = std_output
        configuration_file = write_temporary_configuration(supplied_configuration)

        # Act
        caught_exception = None
        try:
            _ = (
                PyMarkdownApi()
                .enable_rule_by_identifier("MD999")
                .configuration_file_path(configuration_file)
                .scan_path(source_path)
            )
        except PyMarkdownApiException as this_exception:
            caught_exception = this_exception
    finally:
        sys.stdout = old_output
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == """BadPluginError encountered while configuring plugins:
Plugin id 'MD999' had a critical failure during the 'apply_configuration' action."""
    )
    assert (
        std_output.getvalue()
        == """MD999>>init_from_config
MD999>>test_value>>10
MD999>>other_test_value>>1
"""
    )


def test_api_config_with_exception_during_scanning():
    """
    Test to make sure that a configuration file...

    This function shadows
    test_markdown_with_dash_e_single_by_id_and_config_causing_next_token_exception
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": 20}}}
    configuration_file = None
    std_output = io.StringIO()
    old_output = sys.stdout
    try:
        sys.stdout = std_output
        configuration_file = write_temporary_configuration(supplied_configuration)

        # Act
        caught_exception = None
        try:
            _ = (
                PyMarkdownApi()
                .enable_rule_by_identifier("MD999")
                .configuration_file_path(configuration_file)
                .scan_path(source_path)
            )
        except PyMarkdownApiException as this_exception:
            caught_exception = this_exception
    finally:
        sys.stdout = old_output
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == """BadPluginError encountered while scanning '{path}':
(1,1): Plugin id 'MD999' had a critical failure during the 'next_token' action.""".replace(
            "{path}", source_path
        )
    )
    assert (
        std_output.getvalue()
        == """MD999>>init_from_config
MD999>>test_value>>20
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
""".replace(
            "{path}", source_path.replace("\\", "\\\\")
        )
    )


def test_api_config_with_bad_contents_for_default_config():
    """
    Test to make sure that a default configuration file with bad contents is reported as an error.
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = "this is not json"

    # Note that the default configuration file is determined by the current working
    # directory, so this test creates a new directory and executes the parser from
    # within that directory.
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        configuration_file = write_temporary_configuration(
            supplied_configuration, file_name=".pymarkdown", directory=tmp_dir_path
        )

        # Act
        caught_exception = None
        try:
            old_current_working_directory = os.getcwd()
            try:
                os.chdir(tmp_dir_path)
                _ = PyMarkdownApi().scan_path(source_path)
            finally:
                os.chdir(old_current_working_directory)
        except PyMarkdownApiException as this_exception:
            caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == f"Specified configuration file '{os.path.abspath(configuration_file)}' is not a valid JSON file: Expecting value: line 1 column 1 (char 0)."
    )


def test_api_config_with_bad_settings_for_default_config():
    """
    Test to make sure that a default configuration file with bad contents is reported as an error.

    This function shadows
    test_markdown_with_default_configuration_file_with_error
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"mode": {"strict-config": True}, "log": {"file": 0}}

    # Note that the default configuration file is determined by the current working
    # directory, so this test creates a new directory and executes the parser from
    # within that directory.
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        write_temporary_configuration(
            supplied_configuration, file_name=".pymarkdown", directory=tmp_dir_path
        )

        # Act
        caught_exception = None
        try:
            old_current_working_directory = os.getcwd()
            try:
                os.chdir(tmp_dir_path)
                _ = PyMarkdownApi().scan_path(source_path)
            finally:
                os.chdir(old_current_working_directory)
        except PyMarkdownApiException as this_exception:
            caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    assert (
        caught_exception.reason
        == "Configuration Error: The value for property 'log.file' must be of type 'str'."
    )


def test_api_config_with_bad_contents_for_pyproject_toml():
    """
    Test to make sure that a pyproject.toml file with bad contents is reported as an error.
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"mode": {"strict-config": True}, "log": {"file": 0}}

    # Note that the default configuration file is determined by the current working
    # directory, so this test creates a new directory and executes the parser from
    # within that directory.
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        configuration_file = write_temporary_configuration(
            supplied_configuration, file_name="pyproject.toml", directory=tmp_dir_path
        )

        # Act
        caught_exception = None
        try:
            old_current_working_directory = os.getcwd()
            try:
                os.chdir(tmp_dir_path)
                _ = PyMarkdownApi().scan_path(source_path)
            finally:
                os.chdir(old_current_working_directory)
        except PyMarkdownApiException as this_exception:
            caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    print(sys.platform)
    assert (
        caught_exception.reason
        == f"Specified configuration file '{os.path.abspath(configuration_file)}' is not a valid TOML file: Invalid statement (at line 1, column 1)."
    )
