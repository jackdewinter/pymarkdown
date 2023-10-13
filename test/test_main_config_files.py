"""
Module to provide tests related to the basic parts of the scanner.
"""
import os
import tempfile
from test.markdown_scanner import MarkdownScanner

import yaml

from .utils import create_temporary_configuration_file, temporary_change_to_directory

__TEST_DOCUMENT = """# This is a document

* a list
  - a sublist
  - a very long sublist item

this is a very long line
"""


def test_markdown_with_config_no_config():
    """
    Test to make sure that we have a baseline for the other configuration tests.

    This function shadows
    test_api_scan_string_test_bad_file_due_to_no_disables
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = __TEST_DOCUMENT
    supplied_arguments = [
        "--strict-config",
        "scan-stdin",
    ]

    expected_return_code = 1
    expected_output = "stdin:4:3: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: dash] (ul-style)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=stdin_to_use
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_general_command_line():
    """
    Test to make sure that we can disable a rule from the command line without
    any configuration file.

    This test shadows
    test_api_scan_string_test_good_file_after_disables
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = __TEST_DOCUMENT
    supplied_arguments = [
        "--strict-config",
        "-d",
        "Md004",
        "scan-stdin",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=stdin_to_use
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_general_command_line_and_specific_command_line():
    """
    Test to make sure that we can disable a rule specifically and enable a
    rule through a configuration setting, with the disable winning as it is
    the more specific configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = __TEST_DOCUMENT
    supplied_arguments = [
        "--strict-config",
        "-d",
        "Md004",
        "-s",
        "plugins.md004.enabled=$!True",
        "scan-stdin",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=stdin_to_use
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_json_configuration_file():
    """
    Test to make sure that we can supply configuration via a JSON configuration file.
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = __TEST_DOCUMENT
    specified_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": False}},
    }

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            specified_configuration, file_name="myconfig", directory=tmp_dir_path
        ) as configuration_file:
            supplied_arguments = [
                "-c",
                configuration_file,
                "scan-stdin",
            ]

            expected_return_code = 0
            expected_output = ""
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(
                arguments=supplied_arguments, standard_input_to_use=stdin_to_use
            )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_yaml_configuration_file():
    """
    Test to make sure that we can supply configuration via a YAML configuration file.
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = __TEST_DOCUMENT
    specified_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": False}},
    }

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            yaml.dump(specified_configuration),
            file_name="myconfig",
            directory=tmp_dir_path,
        ) as configuration_file:
            supplied_arguments = [
                "--stack-trace",
                "-c",
                configuration_file,
                "scan-stdin",
            ]

            expected_return_code = 0
            expected_output = ""
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(
                arguments=supplied_arguments, standard_input_to_use=stdin_to_use
            )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_default_yaml():
    """
    Test to make sure that we can supply configuration via a YAML configuration file.
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = __TEST_DOCUMENT
    specified_yaml_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": False}},
    }

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            yaml.dump(specified_yaml_configuration),
            file_name=".pymarkdown.yaml",
            directory=tmp_dir_path,
        ):
            supplied_arguments = [
                "scan-stdin",
            ]

            expected_return_code = 0
            expected_output = ""
            expected_error = ""

            # Act
            with temporary_change_to_directory(tmp_dir_path):
                execute_results = scanner.invoke_main(
                    arguments=supplied_arguments, standard_input_to_use=stdin_to_use
                )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_default_yml():
    """
    Test to make sure that we can supply configuration via a YML configuration file.
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = __TEST_DOCUMENT
    specified_yaml_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": False}},
    }

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            yaml.dump(specified_yaml_configuration),
            file_name=".pymarkdown.yaml",
            directory=tmp_dir_path,
        ):
            supplied_arguments = [
                "scan-stdin",
            ]

            expected_return_code = 0
            expected_output = ""
            expected_error = ""

            # Act
            with temporary_change_to_directory(tmp_dir_path):
                execute_results = scanner.invoke_main(
                    arguments=supplied_arguments, standard_input_to_use=stdin_to_use
                )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_default_json_beats_default_yaml():
    """
    Test to make sure that we can supply configuration via a YAML configuration file.
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = __TEST_DOCUMENT
    specified_json_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": False}},
    }
    specified_yaml_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": True}},
    }

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            specified_json_configuration,
            file_name=".pymarkdown",
            directory=tmp_dir_path,
        ):
            with create_temporary_configuration_file(
                yaml.dump(specified_yaml_configuration),
                file_name=".pymarkdown.yaml",
                directory=tmp_dir_path,
            ):
                supplied_arguments = [
                    "scan-stdin",
                ]

                expected_return_code = 0
                expected_output = ""
                expected_error = ""

                # Act
                with temporary_change_to_directory(tmp_dir_path):
                    execute_results = scanner.invoke_main(
                        arguments=supplied_arguments, standard_input_to_use=stdin_to_use
                    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_bad_json_and_yaml_configuration_file():
    """
    Test to make sure that we error out properly with a file that is
    not JSON and is not YAML.xxx
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = __TEST_DOCUMENT
    specified_configuration = """hallo: 1
bye
"""
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            specified_configuration, file_name="myconfig", directory=tmp_dir_path
        ) as configuration_file:
            supplied_arguments = [
                "--stack-trace",
                "-c",
                configuration_file,
                "scan-stdin",
            ]

            expected_return_code = 1
            expected_output = ""
            expected_error = f"Specified configuration file '{configuration_file}' was not parseable as a JSON file or a YAML file."

            # Act
            execute_results = scanner.invoke_main(
                arguments=supplied_arguments, standard_input_to_use=stdin_to_use
            )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_specific_command_line_and_configuration_file():
    """
    Test to make sure that if a command line setting and a configuration
    file setting are applied, that the command line setting wins as it is
    more specific.
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = __TEST_DOCUMENT
    specified_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": True}},
    }

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            specified_configuration, file_name="myconfig", directory=tmp_dir_path
        ) as configuration_file:
            supplied_arguments = [
                "--strict-config",
                "-s",
                "plugins.md004.enabled=$!False",
                "-c",
                configuration_file,
                "scan-stdin",
            ]

            expected_return_code = 0
            expected_output = ""
            expected_error = ""

            # Act
            execute_results = scanner.invoke_main(
                arguments=supplied_arguments, standard_input_to_use=stdin_to_use
            )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_configuration_file_and_default_configuration_file():
    """
    Test to make sure that any default configuration is overridden by an explicitly
    named configuration file.
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = __TEST_DOCUMENT
    specified_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": False}},
    }
    default_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": True}},
    }

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            specified_configuration, file_name="myconfig", directory=tmp_dir_path
        ) as configuration_file:
            with create_temporary_configuration_file(
                default_configuration, file_name=".pymarkdown", directory=tmp_dir_path
            ):
                supplied_arguments = [
                    "--strict-config",
                    "-c",
                    configuration_file,
                    "scan-stdin",
                ]

                expected_return_code = 0
                expected_output = ""
                expected_error = ""

                # Act
                with temporary_change_to_directory(tmp_dir_path):
                    execute_results = scanner.invoke_main(
                        arguments=supplied_arguments, standard_input_to_use=stdin_to_use
                    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_default_configuration_file_and_alternate_configuration_file():
    """
    Test to make sure that a default configuration file takes precedence over a
    Python standard configuration file.
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = __TEST_DOCUMENT
    default_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": False}},
    }
    alternate_configuration = """
[tool.pymarkdown]
plugins.md004.enabled = true
"""

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            default_configuration, file_name=".pymarkdown", directory=tmp_dir_path
        ):
            with create_temporary_configuration_file(
                alternate_configuration,
                file_name="pyproject.toml",
                directory=tmp_dir_path,
            ):
                supplied_arguments = [
                    "--strict-config",
                    "scan-stdin",
                ]

                expected_return_code = 0
                expected_output = ""
                expected_error = ""

                # Act
                with temporary_change_to_directory(tmp_dir_path):
                    execute_results = scanner.invoke_main(
                        arguments=supplied_arguments, standard_input_to_use=stdin_to_use
                    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_alternate_configuration_file():
    """
    Test to make sure that we can load configuration from a Python standard
    configuration file.
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = __TEST_DOCUMENT
    alternate_configuration = """
[tool.pymarkdown]
plugins.md004.enabled = false
"""

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        with create_temporary_configuration_file(
            alternate_configuration, file_name="pyproject.toml", directory=tmp_dir_path
        ):
            supplied_arguments = [
                "--strict-config",
                "scan-stdin",
            ]

            expected_return_code = 0
            expected_output = ""
            expected_error = ""

            # Act
            with temporary_change_to_directory(tmp_dir_path):
                execute_results = scanner.invoke_main(
                    arguments=supplied_arguments, standard_input_to_use=stdin_to_use
                )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_pyproject_configuration_file_with_bad_log_file_value_type():
    """
    Test to make sure that a standard python configuration file can be used and
    that an error with value types is reported.
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
