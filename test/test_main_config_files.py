"""
Module to provide tests related to the basic parts of the scanner.
"""
import os
import tempfile
from test.markdown_scanner import MarkdownScanner

from .utils import write_temporary_configuration


def test_markdown_with_config_no_config():
    """
    Test to make sure that
    """

    # Arrange
    scanner = MarkdownScanner()
    xxx = """# This is a document

* a list
  - a sublist
  - a very long sublist item

this is a very long line
"""

    supplied_arguments = [
        "--strict-config",
        "scan-stdin",
    ]

    expected_return_code = 1
    expected_output = "stdin:4:3: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: dash] (ul-style)"
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=xxx
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_general_command_line():
    """
    Test to make sure that
    """

    # Arrange
    scanner = MarkdownScanner()
    xxx = """# This is a document

* a list
  - a sublist
  - a very long sublist item

this is a very long line
"""

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
        arguments=supplied_arguments, standard_input_to_use=xxx
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_general_command_line_and_specific_command_line():
    """
    Test to make sure that
    """

    # Arrange
    scanner = MarkdownScanner()
    xxx = """# This is a document

* a list
  - a sublist
  - a very long sublist item

this is a very long line
"""

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
        arguments=supplied_arguments, standard_input_to_use=xxx
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_specific_command_line_and_configuration_file():
    """
    Test to make sure that
    """

    # Arrange
    scanner = MarkdownScanner()
    xxx = """# This is a document

* a list
  - a sublist
  - a very long sublist item

this is a very long line
"""
    specified_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": False}},
    }

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        configuration_file = None
        try:
            configuration_file = write_temporary_configuration(
                specified_configuration, file_name="myconfig", directory=tmp_dir_path
            )
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
                arguments=supplied_arguments, standard_input_to_use=xxx
            )
        finally:
            if configuration_file and os.path.exists(configuration_file):
                os.remove(configuration_file)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_config_configuration_file_and_default_configuration_file():
    """
    Test to make sure that
    """

    # Arrange
    scanner = MarkdownScanner()
    xxx = """# This is a document

* a list
  - a sublist
  - a very long sublist item

this is a very long line
"""
    specified_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": False}},
    }
    default_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": True}},
    }

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        configuration_file = None
        default_configuration_file = None
        try:
            configuration_file = write_temporary_configuration(
                specified_configuration, file_name="myconfig", directory=tmp_dir_path
            )
            default_configuration_file = write_temporary_configuration(
                default_configuration, file_name=".pymarkdown", directory=tmp_dir_path
            )
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
            old_current_working_directory = os.getcwd()
            try:
                os.chdir(tmp_dir_path)
                execute_results = scanner.invoke_main(
                    arguments=supplied_arguments, standard_input_to_use=xxx
                )
            finally:
                os.chdir(old_current_working_directory)
        finally:
            if configuration_file and os.path.exists(configuration_file):
                os.remove(configuration_file)
            if default_configuration_file and os.path.exists(
                default_configuration_file
            ):
                os.remove(default_configuration_file)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_default_configuration_file_and_alternate_configuration_file():
    """
    Test to make sure that
    """

    # Arrange
    scanner = MarkdownScanner()
    xxx = """# This is a document

* a list
  - a sublist
  - a very long sublist item

this is a very long line
"""
    default_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"md004": {"enabled": False}},
    }
    alternate_configuration = """
[tool.pymarkdown]
plugins.md004.enabled = true
"""

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        default_configuration_file = None
        alternate_configuration_file = None
        try:
            default_configuration_file = write_temporary_configuration(
                default_configuration, file_name=".pymarkdown", directory=tmp_dir_path
            )
            alternate_configuration_file = write_temporary_configuration(
                alternate_configuration,
                file_name="pyproject.toml",
                directory=tmp_dir_path,
            )
            supplied_arguments = [
                "--strict-config",
                "scan-stdin",
            ]

            expected_return_code = 0
            expected_output = ""
            expected_error = ""

            # Act
            old_current_working_directory = os.getcwd()
            try:
                os.chdir(tmp_dir_path)
                execute_results = scanner.invoke_main(
                    arguments=supplied_arguments, standard_input_to_use=xxx
                )
            finally:
                os.chdir(old_current_working_directory)
        finally:
            if default_configuration_file and os.path.exists(
                default_configuration_file
            ):
                os.remove(default_configuration_file)
            if alternate_configuration_file and os.path.exists(
                alternate_configuration_file
            ):
                os.remove(alternate_configuration_file)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_alternate_configuration_file():
    """
    Test to make sure that
    """

    # Arrange
    scanner = MarkdownScanner()
    xxx = """# This is a document

* a list
  - a sublist
  - a very long sublist item

this is a very long line
"""
    alternate_configuration = """
[tool.pymarkdown]
plugins.md004.enabled = false
"""

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        alternate_configuration_file = None
        try:
            alternate_configuration_file = write_temporary_configuration(
                alternate_configuration,
                file_name="pyproject.toml",
                directory=tmp_dir_path,
            )
            supplied_arguments = [
                "--strict-config",
                "scan-stdin",
            ]

            expected_return_code = 0
            expected_output = ""
            expected_error = ""

            # Act
            old_current_working_directory = os.getcwd()
            try:
                os.chdir(tmp_dir_path)
                execute_results = scanner.invoke_main(
                    arguments=supplied_arguments, standard_input_to_use=xxx
                )
            finally:
                os.chdir(old_current_working_directory)
        finally:
            if alternate_configuration_file and os.path.exists(
                alternate_configuration_file
            ):
                os.remove(alternate_configuration_file)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_pyproject_configuration_file_xxx():
    """
    Test to make sure that
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
        default_configuration_file = None
        try:
            default_configuration_file = write_temporary_configuration(
                default_configuration,
                file_name="pyproject.toml",
                directory=tmp_dir_path,
            )
            supplied_arguments = [
                "--strict-config",
                "scan",
                source_path,
            ]

            expected_return_code = 1
            expected_output = ""
            expected_error = "Configuration Error: The value for property 'log.file' must be of type 'str'.\n"

            # Act
            old_current_working_directory = os.getcwd()
            try:
                os.chdir(tmp_dir_path)
                execute_results = scanner.invoke_main(arguments=supplied_arguments)
            finally:
                os.chdir(old_current_working_directory)

            # Assert
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )
        finally:
            if default_configuration_file and os.path.exists(
                default_configuration_file
            ):
                os.remove(default_configuration_file)
