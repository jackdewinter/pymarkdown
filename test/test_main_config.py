"""
Module to provide tests related to the basic parts of the scanner.
"""

import os
import tempfile
from test.markdown_scanner import MarkdownScanner
from typing import Any, Dict

from .utils import (
    create_temporary_configuration_file,
    temporary_change_to_directory,
    write_temporary_configuration,
)

# pylint: disable=too-many-lines


def test_markdown_with_dash_e_single_by_id_and_good_config() -> None:
    """
    Test to make sure we get enable a rule if '-e' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": 2}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>2
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
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_dash_e_single_by_id_and_good_config_with_comment() -> None:
    """
    Test that is a variation of `test_markdown_with_dash_e_single_by_id_and_good_config`
    that supplies the configuration as a JSON5 file with comments.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = """
{
    "plugins": {
        // This is a comment.
        "md999": {
            "test_value": 2
        }
    }
}
"""

    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>2
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
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_dash_e_single_by_id_and_good_config_with_comment_no_json5() -> (
    None
):
    """
    Test that is a variation of `test_markdown_with_dash_e_single_by_id_and_good_config`
    that supplies the configuration as a JSON5 file with comments, but with JSON5 support
    for configuration files disabled.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = """
{
    "plugins": {
        // This is a comment.
        "md999": {
            "test_value": 2
        }
    }
}
"""

    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "--no-json5",
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = f"Specified configuration file '{configuration_file}' was not parseable as a JSON, YAML, or TOML file."

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_dash_e_single_by_id_and_bad_config() -> None:
    """
    Test to make sure we get enable a rule if '-e' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": "fred"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
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
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_dash_e_single_by_id_and_bad_config_file() -> None:
    """
    Test to make sure we get an error if we provide a configuration file that is
    in a json format, but not valid.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"myrule md999": {"test_value": "fred"}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = (
            "Specified configuration file '"
            + configuration_file
            + "' is not valid: Key string `myrule md999` cannot contain a whitespace character, a '=' character, or a '.' character.\n"
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_dash_e_single_by_id_and_non_json_config_file() -> None:
    """
    Test to make sure we get an error if we provide a configuration file that is
    not in a json format.  Note that simple content such as "not a json file"
    may be interpretted as YAML.

    This function shadows
    test_api_config_with_bad_contents
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = """hallo: 1
bye
"""
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = f"Specified configuration file '{configuration_file}' was not parseable as a JSON, YAML, or TOML file."

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_dash_e_single_by_id_and_non_present_config_file() -> None:
    """
    Test to make sure we get an error if we provide a configuration file that is
    not in a json format.

    This function shadows
    test_api_config_with_bad_path
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    configuration_file = "not-exists"
    assert not os.path.exists(configuration_file)
    supplied_arguments = [
        "-e",
        "MD999",
        "-c",
        configuration_file,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """

Specified configuration file `not-exists` does not exist."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_e_single_by_id_and_good_select_config() -> None:
    """
    Test to make sure we get enable a rule if '-e' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.

    This function shadows
    test_api_config_with_config_file_with_good_value
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"other_test_value": 2}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
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
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_dash_e_single_by_id_and_bad_select_config() -> None:
    """
    Test to make sure we get enable a rule if '-e' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.

    This function is shadowed by
    test_api_config_with_config_file_with_bad_value
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"MD999": {"other_test_value": 9}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
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
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_dash_e_single_by_id_and_config_causing_config_exception() -> (
    None
):
    """
    Test to make sure if we tell the test plugin to throw an exception during the
    call to `initialize_from_config`, that it is handled properly.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": 10}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = """MD999>>init_from_config
MD999>>test_value>>10
MD999>>other_test_value>>1
"""
        expected_error = """BadPluginError encountered while configuring plugins:
Plugin id 'MD999' had a critical failure during the '__apply_configuration' action.
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_dash_e_single_by_id_and_config_causing_next_token_exception() -> (
    None
):
    """
    Test to make sure if we tell the test plugin to throw an exception during the
    call to `next_token`, that it is handled properly.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": 20}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = """MD999>>init_from_config
MD999>>test_value>>20
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
"""
        expected_error = """BadPluginError encountered while scanning '{source_path}':
(1,1): Plugin id 'MD999' had a critical failure during the 'next_token' action.
""".replace(
            "{source_path}", os.path.abspath(source_path)
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_bad_strict_config_type() -> None:
    """
    Test to make sure that we can set the strict configuration mode from
    the configuration file, capturing any bad errors.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"mode": {"strict-config": 2}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = "Configuration Error: The value for property 'mode.strict-config' must be of type 'bool'."

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_good_strict_config_type() -> None:
    """
    Test to make sure that we can set the strict configuration mode from
    the configuration file, capturing any bad errors.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration: Dict[str, Any] = {
        "mode": {"strict-config": True},
        "log": {"file": 0},
    }
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = "Configuration Error: The value for property 'log.file' must be of type 'str'.\n"

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_default_configuration_file_with_error() -> None:
    """
    Test to make sure that a default configuration will be read and have the
    same errors as if it was specified on the command line.

    This function shadows
    test_api_config_with_bad_contents_for_default_config
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    default_configuration: Dict[str, Any] = {
        "mode": {"strict-config": True},
        "log": {"file": 0},
    }

    # Note that the default configuration file is determined by the current working
    # directory, so this test creates a new directory and executes the parser from
    # within that directory.
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            default_configuration, file_name=".pymarkdown", directory=tmp_dir_path
        ):
            supplied_arguments = [
                "scan",
                source_path,
            ]

            expected_return_code = 1
            expected_output = ""
            expected_error = "Configuration Error: The value for property 'log.file' must be of type 'str'.\n"

            # Act
            with temporary_change_to_directory(tmp_dir_path):
                execute_results = scanner.invoke_main(arguments=supplied_arguments)

            # Assert
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )


def test_markdown_with_overlapping_configuration_files() -> None:
    """
    Test to make sure that information from a default configuration file and
    a specified configuration file give each other the right layering.
    i.e. specific config file should override default config file
    """

    # Arrange
    scanner = MarkdownScanner()
    xxx = """# This is a document

* a list
  - a sublist
  - a very long sublist item

this is a very long line
"""

    # The `ul-style` item is set by the default configuration and overridden as "asterisk" by the supplied configuration.
    # The `line-length` item is set by the default configuration as `10` and is not overridden.
    # This results in a `ul-style` of `asterisk` and a `line-length` of `10`.
    default_configuration: Dict[str, Any] = {
        "mode": {"strict-config": True},
        "plugins": {"ul-style": {"style": "dash"}, "line-length": {"line_length": 10}},
    }
    supplied_configuration: Dict[str, Any] = {
        "mode": {"strict-config": True},
        "plugins": {"ul-style": {"style": "asterisk"}},
    }

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            supplied_configuration, directory=tmp_dir_path
        ) as configuration_file:
            with create_temporary_configuration_file(
                default_configuration, file_name=".pymarkdown", directory=tmp_dir_path
            ):
                supplied_arguments = ["-c", configuration_file, "scan-stdin"]

                expected_return_code = 1
                expected_output = (
                    "stdin:4:3: MD004: Inconsistent Unordered List Start style "
                    + "[Expected: asterisk; Actual: dash] (ul-style)\n"
                    + "stdin:5:1: MD013: Line length [Expected: 10, Actual: 28] (line-length)\n"
                    + "stdin:7:1: MD013: Line length [Expected: 10, Actual: 24] (line-length)"
                )
                expected_error = ""

                # Act
                with temporary_change_to_directory(tmp_dir_path):
                    execute_results = scanner.invoke_main(
                        arguments=supplied_arguments, standard_input_to_use=xxx
                    )

                # Assert
                execute_results.assert_results(
                    expected_output, expected_error, expected_return_code
                )


def test_markdown_with_pyproject_configuration_file_with_error() -> None:
    """
    Test to make sure that a pyproject configuration will be read and have the
    same errors as if it was specified on the command line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    default_configuration = """
[tool.pymarkdown]
log.file = 2
a.c = "3"
"""

    # Note that the default configuration file is determined by the current working
    # directory, so this test creates a new directory and executes the parser from
    # within that directory.
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            default_configuration, file_name="pyproject.toml", directory=tmp_dir_path
        ):
            supplied_arguments = [
                "--strict-config",
                "scan",
                source_path,
            ]

            expected_return_code = 1
            expected_output = ""
            expected_error = "Configuration Error: The value for property 'log.file' must be of type 'str'.\n"

            # Act
            with temporary_change_to_directory(tmp_dir_path):
                execute_results = scanner.invoke_main(arguments=supplied_arguments)

            # Assert
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )


def test_markdown_with_pyproject_direct_configuration_file_with_error() -> None:
    """
    Test to make sure that a pyproject configuration will be read and have the
    same errors as if it was specified on the command line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    default_configuration = """
[tool.pymarkdown]
plugins.MD013.enabled = false
plugins.MD003.style = "atx"
plugins.MD004.style = "asterisk"
plugins.MD007.indent = 4
plugins.MD033.enabled = false
plugins.MD041.enabled = false
plugins.MD022.enabled = false
log.file = 2
"""

    # Note that the default configuration file is determined by the current working
    # directory, so this test creates a new directory and executes the parser from
    # within that directory.
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            default_configuration,
            file_name="pyproject.toml",
            directory=tmp_dir_path,
            file_name_suffix=".toml",
        ) as config_path:
            supplied_arguments = [
                "--strict-config",
                "--config",
                config_path,
                "scan",
                source_path,
            ]

            expected_return_code = 1
            expected_output = ""
            expected_error = "Configuration Error: The value for property 'log.file' must be of type 'str'.\n"

            # Act
            with temporary_change_to_directory(tmp_dir_path):
                execute_results = scanner.invoke_main(arguments=supplied_arguments)

            # Assert
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )


def test_markdown_with_pyproject_issue_1484_implicitly_load_toml() -> None:
    """
    Test to make sure that we can implicitly load a pyproject configuration file
    and have it apply properly.

    Note: To not conflict with an existing pyproject.toml file in the repository,
          this test creates a temporary directory and places the pyproject.toml
          file there and executes the scanner from within that directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_atx_heading.md"
    )
    assert os.path.exists(source_path)
    source_path = os.path.abspath(source_path)

    default_configuration = """
[tool.pymarkdown]
plugins.MD013.heading_line_length = 79
"""

    # Note that the default configuration file is determined by the current working
    # directory, so this test creates a new directory and executes the parser from
    # within that directory.
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            default_configuration,
            file_name="pyproject.toml",
            directory=tmp_dir_path,
            file_name_suffix=".toml",
        ):
            supplied_arguments = [
                "--strict-config",
                "scan",
                source_path,
            ]

            expected_return_code = 1
            expected_output = f"{source_path}:1:1: MD013: Line length [Expected: 79, Actual: 88] (line-length)"
            expected_error = ""

            # Act
            with temporary_change_to_directory(tmp_dir_path):
                execute_results = scanner.invoke_main(arguments=supplied_arguments)

            # Assert
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )


def test_markdown_with_pyproject_issue_1484_explicitly_load_toml() -> None:
    """
    Test to make sure that we can explicitly load a pyproject configuration file
    and have it apply properly.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md013", "bad_atx_heading.md"
    )
    assert os.path.exists(source_path)
    source_path = os.path.abspath(source_path)

    default_configuration = """
[tool.pymarkdown]
plugins.MD013.heading_line_length = 81
"""

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            default_configuration,
            file_name="my_config.toml",
            directory=tmp_dir_path,
            file_name_suffix=".toml",
        ) as config_path:
            supplied_arguments = [
                "--strict-config",
                "--config",
                config_path,
                "scan",
                source_path,
            ]

            expected_return_code = 1
            expected_output = f"{source_path}:1:1: MD013: Line length [Expected: 81, Actual: 88] (line-length)"
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

            # Assert
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )


CONFIGURATION_JSON_CONTENT = """
{
    "system" : {
        "exclude_path" : "temp/"
    },
    "extensions": {
        "markdown-tables": {
            "enabled" : true
        }
    },
    "plugins": {
        "md013": {
            "enabled": true,
            "line_length": 100
        }
    }
}
"""
CONFIGURATION_YAML_CONTENT = """
system:
  exclude_path: temp/
extensions:
  markdown-tables:
    enabled: true
plugins:
  md013:
    enabled: true
    line_length: 100
"""
CONFIGURATION_TOML_CONTENT = """
[tool.pymarkdown]

system.exclude_path = "temp/"

extensions.markdown-tables.enabled = true

plugins.md013.enabled = true
plugins.md013.line_length = 100
"""
DOCUMENT_CONTENT = """# This is my title

It may look silly, but this is a long, long, long, long, long, long line that is over 80 characters in length.
"""


def test_markdown_documentation_advanced_configuration_no_configuration() -> None:
    """
    Test to make sure that we have a baseline for the tests that follow.
    """

    # Arrange
    scanner = MarkdownScanner()

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        other_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"""{other_document_path}:3:1: MD013: Line length [Expected: 80, Actual: 110] (line-length)
{main_document_path}:3:1: MD013: Line length [Expected: 80, Actual: 110] (line-length)"""
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension() -> (
    None
):
    """
    Test to make sure that the JSON configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    The configuration specifically is set to:
    - apply an exclude path via configuration file
    - enable markdown tables (TBD)
    - change the line length of the MD013 (`line-length`) rule to 100

    The document itself has a line that is 110 characters long, which will trigger
    the Md013 rule.

    The document is written to the temporary directory and to the `temp/` subdirectory
    within that temporary directory.  Because of the `exclude_path` configuration,
    only one eligible document will be found and only one rule violation will be
    triggered.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = "my_config.json"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        config_path = write_temporary_configuration(
            CONFIGURATION_JSON_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "--config",
            config_path,
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"{main_document_path}:3:1: MD013: Line length [Expected: 100, Actual: 110] (line-length)"
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_explicit_json_with_no_extension() -> (
    None
):
    """
    Test to make sure that the JSON configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    See test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension
    for more details.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = "my_config"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        config_path = write_temporary_configuration(
            CONFIGURATION_JSON_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "--config",
            config_path,
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"{main_document_path}:3:1: MD013: Line length [Expected: 100, Actual: 110] (line-length)"
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_implicit_json_with_json_extension() -> (
    None
):
    """
    Test to make sure that the JSON configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    NOTE: The `.json` extension is implied for `.pymarkdown`, so the implicit
          configuration file will not be loaded and will not affect the
          configuration values.

    See test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension
    for more details.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = ".pymarkdown.json"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        write_temporary_configuration(
            CONFIGURATION_JSON_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        other_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"""{other_document_path}:3:1: MD013: Line length [Expected: 80, Actual: 110] (line-length)
{main_document_path}:3:1: MD013: Line length [Expected: 80, Actual: 110] (line-length)
"""
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_implicit_json_with_no_extension() -> (
    None
):
    """
    Test to make sure that the JSON configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    See test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension
    for more details.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = ".pymarkdown"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        write_temporary_configuration(
            CONFIGURATION_JSON_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"{main_document_path}:3:1: MD013: Line length [Expected: 100, Actual: 110] (line-length)"
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_explicit_yaml_with_yml_extension() -> (
    None
):
    """
    Test to make sure that the YAML configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    See test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension
    for more details.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = "my_config.yml"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        config_path = write_temporary_configuration(
            CONFIGURATION_YAML_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "--config",
            config_path,
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"{main_document_path}:3:1: MD013: Line length [Expected: 100, Actual: 110] (line-length)"
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_explicit_yaml_with_yaml_extension() -> (
    None
):
    """
    Test to make sure that the YAML configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    See test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension
    for more details.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = "my_config.yaml"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        config_path = write_temporary_configuration(
            CONFIGURATION_YAML_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "--config",
            config_path,
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"{main_document_path}:3:1: MD013: Line length [Expected: 100, Actual: 110] (line-length)"
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_explicit_yaml_with_no_extension() -> (
    None
):
    """
    Test to make sure that the YAML configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    See test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension
    for more details.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = "my_config"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        config_path = write_temporary_configuration(
            CONFIGURATION_YAML_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "--config",
            config_path,
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"{main_document_path}:3:1: MD013: Line length [Expected: 100, Actual: 110] (line-length)"
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_implicit_yaml_with_yml_extension() -> (
    None
):
    """
    Test to make sure that the YAML configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    See test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension
    for more details.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = ".pymarkdown.yml"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        write_temporary_configuration(
            CONFIGURATION_YAML_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"{main_document_path}:3:1: MD013: Line length [Expected: 100, Actual: 110] (line-length)"
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_implicit_yaml_with_yaml_extension() -> (
    None
):
    """
    Test to make sure that the YAML configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    See test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension
    for more details.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = ".pymarkdown.yaml"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        write_temporary_configuration(
            CONFIGURATION_YAML_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"{main_document_path}:3:1: MD013: Line length [Expected: 100, Actual: 110] (line-length)"
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_implicit_yaml_with_no_extension() -> (
    None
):
    """
    Test to make sure that the YAML configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    NOTE: The `.yml` or `.yaml` extension is required to distinguish an implicit JSON
          file (`.pymarkdown`) from a implicit YAML file (`.pymarkdown.yml` or `.pymarkdown.yaml`).
          As the extension is not present, the implicit configuration file will
          not be loaded and will not affect the configuration values.

    See test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension
    for more details.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = ".pymarkdown"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        configuration_file_path = write_temporary_configuration(
            CONFIGURATION_YAML_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = f"""Specified configuration file '{configuration_file_path}' is not a valid JSON file: ("Expected b'JSON5Value' near 2, found U+0073", None, 's')."""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_explicit_toml_with_toml_extension() -> (
    None
):
    """
    Test to make sure that the TOML configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    See test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension
    for more details.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = "my_config.toml"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        config_path = write_temporary_configuration(
            CONFIGURATION_TOML_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "--config",
            config_path,
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"{main_document_path}:3:1: MD013: Line length [Expected: 100, Actual: 110] (line-length)"
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_explicit_toml_with_no_extension() -> (
    None
):
    """
    Test to make sure that the TOML configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    See test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension
    for more details.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = "my_config"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        config_path = write_temporary_configuration(
            CONFIGURATION_TOML_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "--config",
            config_path,
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"{main_document_path}:3:1: MD013: Line length [Expected: 100, Actual: 110] (line-length)"
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_implicit_toml_with_toml_extension() -> (
    None
):
    """
    Test to make sure that the TOML configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    See test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension
    for more details.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = "pyproject.toml"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        write_temporary_configuration(
            CONFIGURATION_TOML_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"{main_document_path}:3:1: MD013: Line length [Expected: 100, Actual: 110] (line-length)"
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_documentation_advanced_configuration_implicit_toml_with_no_extension() -> (
    None
):
    """
    Test to make sure that the TOML configuration file specified in the
    advanced_configuration.md documentation file works as advertisted.

    See test_markdown_documentation_advanced_configuration_explicit_json_with_json_extension
    for more details.
    """

    # Arrange
    scanner = MarkdownScanner()
    partial_configuration_file_name = "pyproject.toml"

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        child_directory_path = os.path.join(tmp_dir_path, "temp")

        write_temporary_configuration(
            CONFIGURATION_TOML_CONTENT,
            directory=tmp_dir_path,
            file_name=partial_configuration_file_name,
        )
        main_document_path = write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )
        os.makedirs(child_directory_path)
        write_temporary_configuration(
            DOCUMENT_CONTENT,
            directory=child_directory_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "--strict-config",
            "scan",
            "**/*.md",
        ]

        expected_return_code = 1
        expected_output = f"{main_document_path}:3:1: MD013: Line length [Expected: 100, Actual: 110] (line-length)"
        expected_error = ""

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
