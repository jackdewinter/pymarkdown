"""
Module for specifying a configuration file through the API.
"""

import os
import sys
import tempfile
from test.utils import (
    assert_that_exception_is_raised,
    capture_stdout,
    create_temporary_configuration_file,
    temporary_change_to_directory,
)

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
    configuration_path = ""
    expected_output = "Parameter named 'path_to_config_file' cannot be empty."

    # Act & Assert
    caught_exception = assert_that_exception_is_raised(
        PyMarkdownApiArgumentException,
        expected_output,
        PyMarkdownApi().configuration_file_path,
        configuration_path,
    )

    assert caught_exception.argument_name == "path_to_config_file"


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

    expected_output = "Specified configuration file `not-exists` does not exist."

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiException,
        expected_output,
        PyMarkdownApi().configuration_file_path(configuration_file).scan_path,
        source_path,
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
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        expected_output = f"Specified configuration file '{configuration_file}' was not parseable as a JSON file or a YAML file."

        # Act & Assert
        assert_that_exception_is_raised(
            PyMarkdownApiException,
            expected_output,
            PyMarkdownApi().configuration_file_path(configuration_file).scan_path,
            source_path,
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
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        with capture_stdout() as std_output:
            # Act
            scan_result = (
                PyMarkdownApi()
                .enable_rule_by_identifier("MD999")
                .configuration_file_path(configuration_file)
                .scan_path(source_path)
            )

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
MD999>>token:[end-of-stream(5,0)]
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
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        with capture_stdout() as std_output:
            # Act
            scan_result = (
                PyMarkdownApi()
                .enable_rule_by_identifier("MD999")
                .configuration_file_path(configuration_file)
                .scan_path(source_path)
            )

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
MD999>>token:[end-of-stream(5,0)]
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
    expected_output = (
        "Configuration Error: The value for property 'log.file' must be of type 'str'."
    )

    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        # Act & Assert
        assert_that_exception_is_raised(
            PyMarkdownApiException,
            expected_output,
            PyMarkdownApi().configuration_file_path(configuration_file).scan_path,
            source_path,
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
    expected_output = "Configuration Error: The value for property 'mode.strict-config' must be of type 'bool'."

    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        # Act & Assert
        assert_that_exception_is_raised(
            PyMarkdownApiException,
            expected_output,
            PyMarkdownApi().configuration_file_path(configuration_file).scan_path,
            source_path,
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

    expected_output = """BadPluginError encountered while configuring plugins:
Plugin id 'MD999' had a critical failure during the 'apply_configuration' action."""

    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        with capture_stdout() as std_output:
            # Act
            caught_exception = assert_that_exception_is_raised(
                PyMarkdownApiException,
                expected_output,
                PyMarkdownApi()
                .enable_rule_by_identifier("MD999")
                .configuration_file_path(configuration_file)
                .scan_path,
                source_path,
            )

    # Assert
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
    expected_output = """BadPluginError encountered while scanning '{path}':
(1,1): Plugin id 'MD999' had a critical failure during the 'next_token' action.""".replace(
        "{path}", source_path
    )

    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        with capture_stdout() as std_output:
            # Act
            assert_that_exception_is_raised(
                PyMarkdownApiException,
                expected_output,
                PyMarkdownApi()
                .enable_rule_by_identifier("MD999")
                .configuration_file_path(configuration_file)
                .scan_path,
                source_path,
            )

    # Assert
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
        with create_temporary_configuration_file(
            supplied_configuration, file_name=".pymarkdown", directory=tmp_dir_path
        ) as configuration_file:
            # Act
            caught_exception = None
            try:
                with temporary_change_to_directory(tmp_dir_path):
                    _ = PyMarkdownApi().scan_path(source_path)
            except PyMarkdownApiException as this_exception:
                caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    if sys.platform == "darwin":
        assert caught_exception.reason.startswith("Specified configuration file '")
        assert caught_exception.reason.endswith(
            "' is not a valid JSON file: Expecting value: line 1 column 1 (char 0)."
        )
    else:
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

    expected_output = (
        "Configuration Error: The value for property 'log.file' must be of type 'str'."
    )

    # Note that the default configuration file is determined by the current working
    # directory, so this test creates a new directory and executes the parser from
    # within that directory.
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            supplied_configuration, file_name=".pymarkdown", directory=tmp_dir_path
        ):
            # Act & Assert
            with temporary_change_to_directory(tmp_dir_path):
                assert_that_exception_is_raised(
                    PyMarkdownApiException,
                    expected_output,
                    PyMarkdownApi().scan_path,
                    source_path,
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
        with create_temporary_configuration_file(
            supplied_configuration, file_name="pyproject.toml", directory=tmp_dir_path
        ) as configuration_file:
            # Act
            caught_exception = None
            try:
                with temporary_change_to_directory(tmp_dir_path):
                    _ = PyMarkdownApi().scan_path(source_path)
            except PyMarkdownApiException as this_exception:
                caught_exception = this_exception

    # Assert
    assert caught_exception, "Should have thrown an exception."
    if sys.platform == "darwin":
        assert caught_exception.reason.startswith("Specified configuration file '")
        assert caught_exception.reason.endswith(
            "' is not a valid TOML file: Invalid statement (at line 1, column 1)."
        )
    else:
        assert (
            caught_exception.reason
            == f"Specified configuration file '{os.path.abspath(configuration_file)}' is not a valid TOML file: Invalid statement (at line 1, column 1)."
        )
