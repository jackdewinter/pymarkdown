"""
Module to provide tests related to the plugin manager for the scanner.
"""

import os
import sys
from test.markdown_scanner import MarkdownScanner
from test.utils import (
    assert_file_is_as_expected,
    copy_to_temp_file,
    create_temporary_configuration_file,
    read_contents_of_text_file,
)

# pylint: disable=too-many-lines

if sys.version_info < (3, 10):
    ARGPARSE_X = "optional arguments:"
else:
    ARGPARSE_X = "options:"


def test_markdown_with_plugins_only() -> None:
    """
    Test to make sure "plugins" from the command line shows help
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "plugins",
    ]

    expected_return_code = 2
    expected_output = """usage: main.py plugins [-h] {list,info} ...

positional arguments:
  {list,info}
    list       list the available plugins
    info       information on a specific plugin

{ARGPARSE_X}
  -h, --help   show this help message and exit
""".replace(
        "{ARGPARSE_X}", ARGPARSE_X
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_and_bad_path() -> None:
    """
    Test to make sure we get an error if '--add-plugin' is supplied with a bad path.

    This function shadows
    test_api_plugins_add_with_bad_path
    and
    test_markdown_return_code_default_system_error.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "--add-plugin",
        "MD047",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while loading plugins:\n"
        + "Plugin path 'MD047' does not exist.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_and_single_plugin_file() -> None:
    """
    Test to make sure we add a plugin if '--add-plugin' is supplied with a valid plugin.

    This test shadows
    test_api_plugins_add_with_simple_plugin
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/plugin_two.py",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = """MD998>>init_from_config
MD998>>starting_new_file>>
MD998>>next_line:# This is a test
MD998>>next_line:
MD998>>next_line:The line after this line should be blank.
MD998>>next_line:
MD998>>completed_file
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_and_single_plugin_directory() -> None:
    """
    Test to make sure we add a plugin if '--add-plugin' is supplied with a valid plugin directory.

    This function shadows
    test_api_plugins_add_with_simple_plugins_by_directory
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = """MD998>>init_from_config
MD998>>starting_new_file>>
MD998>>next_line:# This is a test
MD998>>next_line:
MD998>>next_line:The line after this line should be blank.
MD998>>next_line:
MD998>>completed_file
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_repeated_identifier() -> None:
    """
    Test to make sure we report an error if '--add-plugin' is supplied with a plugin that
    specifies an already present id.

    This function shadows
    test_api_plugins_add_with_repeated_identifier
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "duplicate_id_debug.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """ValueError encountered while initializing plugins:
Unable to register plugin 'duplicate_id_debug.py' with id 'md999' as plugin 'plugin_one.py' is already registered with that id."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_bad_identifier() -> None:
    """
    Test to make sure we report an error if '--add-plugin' is supplied with a plugin that
        specifies an invalid id.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join("test", "resources", "plugins", "bad", "bad_id.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """ValueError encountered while initializing plugins:
Unable to register plugin 'bad_id.py' with id 'debug-only' as id is not a valid id in the form 'aannn' or 'aaannn'."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_repeated_name() -> None:
    """
    Test to make sure we report an error if '--add-plugin' is supplied with a plugin that
        specifies an already present name.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "duplicate_name_debug.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """ValueError encountered while initializing plugins:
Unable to register plugin 'duplicate_name_debug.py' with name 'debug-only' as plugin 'plugin_one.py' is already registered with that name."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_bad_name() -> None:
    """
    Test to make sure we report an error if '--add-plugin' is supplied with a plugin that
        specifies a bad name.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join("test", "resources", "plugins", "bad", "bad_name.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """ValueError encountered while initializing plugins:
Unable to register plugin 'bad_name.py' with name 'debug.only' as name is not a valid name in the form 'an-an'."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_and_bad_plugin_file() -> None:
    """
    Test to make sure we report an error if '--add-plugin' is supplied with a plugin file
        that is not really a plugin file.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "not-a-python-file.txt"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while loading plugins:\n"
        + "Plugin file named 'not-a-python-file.txt' cannot be loaded.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_and_missing_class() -> None:
    """
    Test to make sure we report an error if '--add-plugin' is supplied with a plugin file
        that does not specify a plugin with the same name.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join("test", "resources", "plugins", "bad", "misnamed.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while loading plugins:\n"
        + "Plugin file named 'misnamed.py' does not contain a class named 'Misnamed'.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_starting_new_file() -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the starting_new_file function.

    This function shadows
    test_api_plugins_add_with_bad_starting_new_file
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_starting_new_file.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning '{source_path}':
Plugin id 'MDE001' had a critical failure during the 'starting_new_file' action.
""".replace(
        "{source_path}", source_path
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_starting_new_file_with_alternate_output() -> (
    None
):
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the starting_new_file function.
    """

    # Arrange
    scanner = MarkdownScanner(use_main=False, use_alternate_presentation=True)
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_starting_new_file.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """[pse[[fse[BadPluginError encountered while scanning '{source_path}':
Plugin id 'MDE001' had a critical failure during the 'starting_new_file' action.]]]]
""".replace(
        "{source_path}", source_path
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_completed_file() -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the completed_file function.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_completed_file.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning '{source_path}':
Plugin id 'MDE002' had a critical failure during the 'completed_file' action.
""".replace(
        "{source_path}", source_path
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line() -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the next_line function.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_next_line.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning '{source_path}':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
""".replace(
        "{source_path}", source_path
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line_fix() -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the next_line function.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_next_line.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "fix",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning '{source_path}':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
""".replace(
        "{source_path}", source_path
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line_with_stack_trace() -> (
    None
):
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the next_line function.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_next_line.py"
    )
    supplied_arguments = [
        "--stack-trace",
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning '{source_path}':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
Actual Line: # This is a test
Caused by: Exception:
   bad next_line
Traceback (most recent call last):
""".replace(
        "{source_path}", source_path
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output,
        expected_error,
        expected_return_code,
        additional_error=[
            """    raise Exception("bad next_line")
Exception: bad next_line

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
""",
            """, in next_line
    raise BadPluginError(""",
            """pymarkdown.plugin_manager.bad_plugin_error.BadPluginError: (Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line_with_configuration_stack_trace() -> (
    None
):
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the next_line function.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_next_line.py"
    )
    supplied_arguments = [
        "--stack-trace",
        "--add-plugin",
        plugin_path,
        "--set",
        "log.stack-trace=$!True",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning '{source_path}':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
Actual Line: # This is a test
Caused by: Exception:
   bad next_line
Traceback (most recent call last):
""".replace(
        "{source_path}", source_path
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output,
        expected_error,
        expected_return_code,
        additional_error=[
            """    raise Exception("bad next_line")
Exception: bad next_line

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
""",
            """, in next_line
    raise BadPluginError(""",
            """pymarkdown.plugin_manager.bad_plugin_error.BadPluginError: (Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_next_token() -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the next_token function.

    This function shadows
    test_api_plugins_add_with_bad_next_token
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_next_token.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning '{source_path}':
(1,1): Plugin id 'MDE003' had a critical failure during the 'next_token' action.
""".replace(
        "{source_path}", source_path
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_next_token_with_stack_trace() -> (
    None
):
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the next_token function.

    This function shadows
    test_api_plugins_add_with_bad_next_token_and_stack_trace
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_next_token.py"
    )
    supplied_arguments = [
        "--stack-trace",
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning '{source_path}':
(1,1): Plugin id 'MDE003' had a critical failure during the 'next_token' action.
Actual Token: [atx(1,1):1:0:]
Caused by: Exception:
   bad next_token
Traceback (most recent call last):
""".replace(
        "{source_path}", source_path
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output,
        expected_error,
        expected_return_code,
        additional_error=[
            """    raise Exception("bad next_token")
Exception: bad next_token

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
""",
            """, in next_token
    raise BadPluginError(""",
            """
pymarkdown.plugin_manager.bad_plugin_error.BadPluginError: (1,1): Plugin id 'MDE003' had a critical failure during the 'next_token' action.
""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_constructor() -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the constructor function.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_constructor.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while loading plugins:\n"
        + "Plugin file named 'bad_constructor.py' threw an exception in the constructor for the class 'BadConstructor'.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_details() -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the details function.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join("test", "resources", "plugins", "bad", "bad_details.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin class 'BadDetails' had a critical failure loading the plugin details.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_details_with_stack_trace() -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the details function.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join("test", "resources", "plugins", "bad", "bad_details.py")
    supplied_arguments = [
        "--stack-trace",
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin class 'BadDetails' had a critical failure loading the plugin details.
Traceback (most recent call last):
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output,
        expected_error,
        expected_return_code,
        additional_error=[
            """    raise Exception("bad details")
Exception: bad details

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
""",
            """    raise BadPluginError(""",
            """pymarkdown.plugin_manager.bad_plugin_error.BadPluginError: Plugin class 'BadDetails' had a critical failure loading the plugin details.""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_string_detail() -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        that a descirption is bad.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_string_detail_is_int.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin class 'BadStringDetailIsInt' returned an improperly typed value for field name 'plugin_description'.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_string_detail_from_configuration() -> (
    None
):
    """
    Test to make sure we get an error logged if a plugin throws an exception that a string detail is bad.
    Note: this version loads from configuration.

    This function shadows
    test_api_plugins_add_with_bad_load_due_to_configuration
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_string_detail_is_int.py"
    )
    supplied_configuration = {"plugins": {"additional_paths": plugin_path}}
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
        expected_error = """\n\nBadPluginError encountered while loading plugins:
Plugin class 'BadStringDetailIsInt' returned an improperly typed value for field name 'plugin_description'.
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_dash_dash_add_plugin_with_empty_string_detail() -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception that a string detail is empty.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_string_detail_is_empty.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin class 'BadStringDetailIsEmpty' returned an empty value for field name 'plugin_description'.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_boolean_detail() -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception that a boolean detail is bad.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_boolean_detail_is_int.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin class 'BadBooleanDetailIsInt' returned an improperly typed value for field name 'plugin_enabled_by_default'.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_integer_detail() -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception that an integer detail is bad.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_integer_detail_is_string.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin class 'BadIntegerDetailIsString' returned an improperly typed value for field name 'plugin_interface_version'.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_description() -> None:
    """
    Test to make sure we get an error logged if a plugin returns a bad description.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_description.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin class 'BadDescription' returned an improperly typed value for field name 'plugin_description'.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_empty_description() -> None:
    """
    Test to make sure we get an error logged if a plugin returns an empty description.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "empty_description.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin class 'EmptyDescription' returned an empty value for field name 'plugin_description'.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_blank_description() -> None:
    """
    Test to make sure we get an error logged if a plugin returns a blank description.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "blank_description.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """ValueError encountered while initializing plugins:
Unable to register plugin 'blank_description.py' with a description string that is blank.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_semantic_version() -> None:
    """
    Test to make sure we get an error logged if a plugin returns a bad semantic version.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_semantic_version.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """ValueError encountered while initializing plugins:
Unable to register plugin 'bad_semantic_version.py' with a version string that is not a valid semantic version.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_interface_version() -> None:
    """
    Test to make sure we get an error logged if a plugin returns a bad interface version.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_interface_version.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin 'bad_interface_version.py' with an interface version ('-1') that is not '1', '2', or '3'.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_only() -> None:
    """
    Test to make sure that `plugins list` lists all plugins.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list"]

    expected_return_code = 0
    expected_output = """
  ID      NAMES                           ENABLED    ENABLED    VERSION  FIX
                                          (DEFAULT)  (CURRENT)

  md001   heading-increment, header-incr  True       True       0.6.0    Yes
          ement
  md002   first-heading-h1, first-header  False      False      0.6.0    No
          -h1
  md003   heading-style, header-style     True       True       0.6.0    No
  md004   ul-style                        True       True       0.6.0    Yes
  md005   list-indent                     True       True       0.5.2    Yes
  md006   ul-start-left                   False      False      0.5.1    Yes
  md007   ul-indent                       True       True       0.6.1    Yes
  md009   no-trailing-spaces              True       True       0.6.0    Yes
  md010   no-hard-tabs                    True       True       0.6.0    Yes
  md011   no-reversed-links               True       True       0.5.0    No
  md012   no-multiple-blanks              True       True       0.7.0    Yes
  md013   line-length                     True       True       0.6.0    No
  md014   commands-show-output            True       True       0.5.0    No
  md018   no-missing-space-atx            True       True       0.5.0    No
  md019   no-multiple-space-atx           True       True       0.5.1    Yes
  md020   no-missing-space-closed-atx     True       True       0.5.0    No
  md021   no-multiple-space-closed-atx    True       True       0.5.1    Yes
  md022   blanks-around-headings, blanks  True       True       0.6.0    No
          -around-headers
  md023   heading-start-left, header-sta  True       True       0.5.2    Yes
          rt-left
  md024   no-duplicate-heading, no-dupli  True       True       0.6.0    No
          cate-header
  md025   single-title, single-h1         True       True       0.6.0    No
  md026   no-trailing-punctuation         True       True       0.6.0    No
  md027   no-multiple-space-blockquote    True       True       0.5.1    Yes
  md028   no-blanks-blockquote            True       True       0.5.0    No
  md029   ol-prefix                       True       True       0.6.0    Yes
  md030   list-marker-space               True       True       0.6.0    Yes
  md031   blanks-around-fences            True       True       0.7.0    Yes
  md032   blanks-around-lists             True       True       0.5.1    No
  md033   no-inline-html                  True       True       0.6.0    No
  md034   no-bare-urls                    True       True       0.5.1    No
  md035   hr-style                        True       True       0.6.0    Yes
  md036   no-emphasis-as-heading, no-emp  True       True       0.6.0    No
          hasis-as-header
  md037   no-space-in-emphasis            True       True       0.5.1    Yes
  md038   no-space-in-code                True       True       0.5.1    Yes
  md039   no-space-in-links               True       True       0.5.2    Yes
  md040   fenced-code-language            True       True       0.5.0    No
  md041   first-line-heading, first-line  True       True       0.7.0    No
          -h1
  md042   no-empty-links                  True       True       0.5.0    No
  md043   required-headings, required-he  True       True       0.6.0    No
          aders
  md044   proper-names                    True       True       0.7.0    Yes
  md045   no-alt-text                     True       True       0.5.0    No
  md046   code-block-style                True       True       0.7.0    Yes
  md047   single-trailing-newline         True       True       0.5.1    Yes
  md048   code-fence-style                True       True       0.6.0    Yes
  pml100  disallowed-html                 False      False      0.6.0    No
  pml101  list-anchored-indent            False      False      0.6.0    No
  
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_only_all() -> None:
    """
    Test to make sure that `plugins list` lists all plugins, even ones
        that may not usually appear.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list", "--all"]

    expected_return_code = 0
    expected_output = """
  ID      NAMES                           ENABLED    ENABLED    VERSION  FIX
                                          (DEFAULT)  (CURRENT)

  md001   heading-increment, header-incr  True       True       0.6.0    Yes
          ement
  md002   first-heading-h1, first-header  False      False      0.6.0    No
          -h1
  md003   heading-style, header-style     True       True       0.6.0    No
  md004   ul-style                        True       True       0.6.0    Yes
  md005   list-indent                     True       True       0.5.2    Yes
  md006   ul-start-left                   False      False      0.5.1    Yes
  md007   ul-indent                       True       True       0.6.1    Yes
  md009   no-trailing-spaces              True       True       0.6.0    Yes
  md010   no-hard-tabs                    True       True       0.6.0    Yes
  md011   no-reversed-links               True       True       0.5.0    No
  md012   no-multiple-blanks              True       True       0.7.0    Yes
  md013   line-length                     True       True       0.6.0    No
  md014   commands-show-output            True       True       0.5.0    No
  md018   no-missing-space-atx            True       True       0.5.0    No
  md019   no-multiple-space-atx           True       True       0.5.1    Yes
  md020   no-missing-space-closed-atx     True       True       0.5.0    No
  md021   no-multiple-space-closed-atx    True       True       0.5.1    Yes
  md022   blanks-around-headings, blanks  True       True       0.6.0    No
          -around-headers
  md023   heading-start-left, header-sta  True       True       0.5.2    Yes
          rt-left
  md024   no-duplicate-heading, no-dupli  True       True       0.6.0    No
          cate-header
  md025   single-title, single-h1         True       True       0.6.0    No
  md026   no-trailing-punctuation         True       True       0.6.0    No
  md027   no-multiple-space-blockquote    True       True       0.5.1    Yes
  md028   no-blanks-blockquote            True       True       0.5.0    No
  md029   ol-prefix                       True       True       0.6.0    Yes
  md030   list-marker-space               True       True       0.6.0    Yes
  md031   blanks-around-fences            True       True       0.7.0    Yes
  md032   blanks-around-lists             True       True       0.5.1    No
  md033   no-inline-html                  True       True       0.6.0    No
  md034   no-bare-urls                    True       True       0.5.1    No
  md035   hr-style                        True       True       0.6.0    Yes
  md036   no-emphasis-as-heading, no-emp  True       True       0.6.0    No
          hasis-as-header
  md037   no-space-in-emphasis            True       True       0.5.1    Yes
  md038   no-space-in-code                True       True       0.5.1    Yes
  md039   no-space-in-links               True       True       0.5.2    Yes
  md040   fenced-code-language            True       True       0.5.0    No
  md041   first-line-heading, first-line  True       True       0.7.0    No
          -h1
  md042   no-empty-links                  True       True       0.5.0    No
  md043   required-headings, required-he  True       True       0.6.0    No
          aders
  md044   proper-names                    True       True       0.7.0    Yes
  md045   no-alt-text                     True       True       0.5.0    No
  md046   code-block-style                True       True       0.7.0    Yes
  md047   single-trailing-newline         True       True       0.5.1    Yes
  md048   code-fence-style                True       True       0.6.0    Yes
  md999   debug-only                      False      False      0.0.0    No
  pml100  disallowed-html                 False      False      0.6.0    No
  pml101  list-anchored-indent            False      False      0.6.0    No
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_after_command_line_disable_all_rules() -> None:
    """
    Test to make sure that `plugins list` lists all plugins after disabling all rules.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["--disable-rules", "*", "plugins", "list"]

    expected_return_code = 0
    expected_output = """
  ID      NAMES                           ENABLED    ENABLED    VERSION  FIX
                                          (DEFAULT)  (CURRENT)

  md001   heading-increment, header-incr  True       False      0.6.0    Yes
          ement
  md002   first-heading-h1, first-header  False      False      0.6.0    No
          -h1
  md003   heading-style, header-style     True       False      0.6.0    No
  md004   ul-style                        True       False      0.6.0    Yes
  md005   list-indent                     True       False      0.5.2    Yes
  md006   ul-start-left                   False      False      0.5.1    Yes
  md007   ul-indent                       True       False      0.6.1    Yes
  md009   no-trailing-spaces              True       False      0.6.0    Yes
  md010   no-hard-tabs                    True       False      0.6.0    Yes
  md011   no-reversed-links               True       False      0.5.0    No
  md012   no-multiple-blanks              True       False      0.7.0    Yes
  md013   line-length                     True       False      0.6.0    No
  md014   commands-show-output            True       False      0.5.0    No
  md018   no-missing-space-atx            True       False      0.5.0    No
  md019   no-multiple-space-atx           True       False      0.5.1    Yes
  md020   no-missing-space-closed-atx     True       False      0.5.0    No
  md021   no-multiple-space-closed-atx    True       False      0.5.1    Yes
  md022   blanks-around-headings, blanks  True       False      0.6.0    No
          -around-headers
  md023   heading-start-left, header-sta  True       False      0.5.2    Yes
          rt-left
  md024   no-duplicate-heading, no-dupli  True       False      0.6.0    No
          cate-header
  md025   single-title, single-h1         True       False      0.6.0    No
  md026   no-trailing-punctuation         True       False      0.6.0    No
  md027   no-multiple-space-blockquote    True       False      0.5.1    Yes
  md028   no-blanks-blockquote            True       False      0.5.0    No
  md029   ol-prefix                       True       False      0.6.0    Yes
  md030   list-marker-space               True       False      0.6.0    Yes
  md031   blanks-around-fences            True       False      0.7.0    Yes
  md032   blanks-around-lists             True       False      0.5.1    No
  md033   no-inline-html                  True       False      0.6.0    No
  md034   no-bare-urls                    True       False      0.5.1    No
  md035   hr-style                        True       False      0.6.0    Yes
  md036   no-emphasis-as-heading, no-emp  True       False      0.6.0    No
          hasis-as-header
  md037   no-space-in-emphasis            True       False      0.5.1    Yes
  md038   no-space-in-code                True       False      0.5.1    Yes
  md039   no-space-in-links               True       False      0.5.2    Yes
  md040   fenced-code-language            True       False      0.5.0    No
  md041   first-line-heading, first-line  True       False      0.7.0    No
          -h1
  md042   no-empty-links                  True       False      0.5.0    No
  md043   required-headings, required-he  True       False      0.6.0    No
          aders
  md044   proper-names                    True       False      0.7.0    Yes
  md045   no-alt-text                     True       False      0.5.0    No
  md046   code-block-style                True       False      0.7.0    Yes
  md047   single-trailing-newline         True       False      0.5.1    Yes
  md048   code-fence-style                True       False      0.6.0    Yes
  pml100  disallowed-html                 False      False      0.6.0    No
  pml101  list-anchored-indent            False      False      0.6.0    No
  
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_after_configuration_disable_all_rules() -> None:
    """
    Test to make sure that `plugins list` lists all plugins after disabling all rules.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list"]
    supplied_configuration = {"plugins": {"selectively_enable_rules": True}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = ["-c", configuration_file, "plugins", "list"]

        expected_return_code = 0
        expected_output = """
  ID      NAMES                           ENABLED    ENABLED    VERSION  FIX
                                          (DEFAULT)  (CURRENT)

  md001   heading-increment, header-incr  True       False      0.6.0    Yes
          ement
  md002   first-heading-h1, first-header  False      False      0.6.0    No
          -h1
  md003   heading-style, header-style     True       False      0.6.0    No
  md004   ul-style                        True       False      0.6.0    Yes
  md005   list-indent                     True       False      0.5.2    Yes
  md006   ul-start-left                   False      False      0.5.1    Yes
  md007   ul-indent                       True       False      0.6.1    Yes
  md009   no-trailing-spaces              True       False      0.6.0    Yes
  md010   no-hard-tabs                    True       False      0.6.0    Yes
  md011   no-reversed-links               True       False      0.5.0    No
  md012   no-multiple-blanks              True       False      0.7.0    Yes
  md013   line-length                     True       False      0.6.0    No
  md014   commands-show-output            True       False      0.5.0    No
  md018   no-missing-space-atx            True       False      0.5.0    No
  md019   no-multiple-space-atx           True       False      0.5.1    Yes
  md020   no-missing-space-closed-atx     True       False      0.5.0    No
  md021   no-multiple-space-closed-atx    True       False      0.5.1    Yes
  md022   blanks-around-headings, blanks  True       False      0.6.0    No
          -around-headers
  md023   heading-start-left, header-sta  True       False      0.5.2    Yes
          rt-left
  md024   no-duplicate-heading, no-dupli  True       False      0.6.0    No
          cate-header
  md025   single-title, single-h1         True       False      0.6.0    No
  md026   no-trailing-punctuation         True       False      0.6.0    No
  md027   no-multiple-space-blockquote    True       False      0.5.1    Yes
  md028   no-blanks-blockquote            True       False      0.5.0    No
  md029   ol-prefix                       True       False      0.6.0    Yes
  md030   list-marker-space               True       False      0.6.0    Yes
  md031   blanks-around-fences            True       False      0.7.0    Yes
  md032   blanks-around-lists             True       False      0.5.1    No
  md033   no-inline-html                  True       False      0.6.0    No
  md034   no-bare-urls                    True       False      0.5.1    No
  md035   hr-style                        True       False      0.6.0    Yes
  md036   no-emphasis-as-heading, no-emp  True       False      0.6.0    No
          hasis-as-header
  md037   no-space-in-emphasis            True       False      0.5.1    Yes
  md038   no-space-in-code                True       False      0.5.1    Yes
  md039   no-space-in-links               True       False      0.5.2    Yes
  md040   fenced-code-language            True       False      0.5.0    No
  md041   first-line-heading, first-line  True       False      0.7.0    No
          -h1
  md042   no-empty-links                  True       False      0.5.0    No
  md043   required-headings, required-he  True       False      0.6.0    No
          aders
  md044   proper-names                    True       False      0.7.0    Yes
  md045   no-alt-text                     True       False      0.5.0    No
  md046   code-block-style                True       False      0.7.0    Yes
  md047   single-trailing-newline         True       False      0.5.1    Yes
  md048   code-fence-style                True       False      0.6.0    Yes
  pml100  disallowed-html                 False      False      0.6.0    No
  pml101  list-anchored-indent            False      False      0.6.0    No
  
"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_with_plugins_list_after_command_line_disable_all_rules_and_enable_one() -> (
    None
):
    """
    Test to make sure that `plugins list` lists all plugins after disabling all rules.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "*",
        "--enable-rules",
        "md010",
        "plugins",
        "list",
    ]

    expected_return_code = 0
    expected_output = """
  ID      NAMES                           ENABLED    ENABLED    VERSION  FIX
                                          (DEFAULT)  (CURRENT)

  md001   heading-increment, header-incr  True       False      0.6.0    Yes
          ement
  md002   first-heading-h1, first-header  False      False      0.6.0    No
          -h1
  md003   heading-style, header-style     True       False      0.6.0    No
  md004   ul-style                        True       False      0.6.0    Yes
  md005   list-indent                     True       False      0.5.2    Yes
  md006   ul-start-left                   False      False      0.5.1    Yes
  md007   ul-indent                       True       False      0.6.1    Yes
  md009   no-trailing-spaces              True       False      0.6.0    Yes
  md010   no-hard-tabs                    True       True       0.6.0    Yes
  md011   no-reversed-links               True       False      0.5.0    No
  md012   no-multiple-blanks              True       False      0.7.0    Yes
  md013   line-length                     True       False      0.6.0    No
  md014   commands-show-output            True       False      0.5.0    No
  md018   no-missing-space-atx            True       False      0.5.0    No
  md019   no-multiple-space-atx           True       False      0.5.1    Yes
  md020   no-missing-space-closed-atx     True       False      0.5.0    No
  md021   no-multiple-space-closed-atx    True       False      0.5.1    Yes
  md022   blanks-around-headings, blanks  True       False      0.6.0    No
          -around-headers
  md023   heading-start-left, header-sta  True       False      0.5.2    Yes
          rt-left
  md024   no-duplicate-heading, no-dupli  True       False      0.6.0    No
          cate-header
  md025   single-title, single-h1         True       False      0.6.0    No
  md026   no-trailing-punctuation         True       False      0.6.0    No
  md027   no-multiple-space-blockquote    True       False      0.5.1    Yes
  md028   no-blanks-blockquote            True       False      0.5.0    No
  md029   ol-prefix                       True       False      0.6.0    Yes
  md030   list-marker-space               True       False      0.6.0    Yes
  md031   blanks-around-fences            True       False      0.7.0    Yes
  md032   blanks-around-lists             True       False      0.5.1    No
  md033   no-inline-html                  True       False      0.6.0    No
  md034   no-bare-urls                    True       False      0.5.1    No
  md035   hr-style                        True       False      0.6.0    Yes
  md036   no-emphasis-as-heading, no-emp  True       False      0.6.0    No
          hasis-as-header
  md037   no-space-in-emphasis            True       False      0.5.1    Yes
  md038   no-space-in-code                True       False      0.5.1    Yes
  md039   no-space-in-links               True       False      0.5.2    Yes
  md040   fenced-code-language            True       False      0.5.0    No
  md041   first-line-heading, first-line  True       False      0.7.0    No
          -h1
  md042   no-empty-links                  True       False      0.5.0    No
  md043   required-headings, required-he  True       False      0.6.0    No
          aders
  md044   proper-names                    True       False      0.7.0    Yes
  md045   no-alt-text                     True       False      0.5.0    No
  md046   code-block-style                True       False      0.7.0    Yes
  md047   single-trailing-newline         True       False      0.5.1    Yes
  md048   code-fence-style                True       False      0.6.0    Yes
  pml100  disallowed-html                 False      False      0.6.0    No
  pml101  list-anchored-indent            False      False      0.6.0    No
  
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_and_filter_by_id_ends_with_nine() -> None:
    """
    Test to make sure that `plugins list` lists all plugins with the specified id filter.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list", "md*9"]

    expected_return_code = 0
    expected_output = """
  ID     NAMES                  ENABLED    ENABLED    VERSION  FIX
                                (DEFAULT)  (CURRENT)

  md009  no-trailing-spaces     True       True       0.6.0    Yes
  md019  no-multiple-space-atx  True       True       0.5.1    Yes
  md029  ol-prefix              True       True       0.6.0    Yes
  md039  no-space-in-links      True       True       0.5.2    Yes

"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_and_filter_by_id_ends_with_non_sequence() -> None:
    """
    Test to make sure that `plugins list` lists all plugins with the specified id filter
        for a filter that returns no values.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list", "this-is-not-an-used-identifier"]

    expected_return_code = 1
    expected_output = ""
    expected_error = "No plugin rule identifiers matches the pattern 'this-is-not-an-used-identifier'."

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_and_filter_by_name_link() -> None:
    """
    Test to make sure that `plugins list` lists all plugins with the specified name filter.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list", "*header*"]

    expected_return_code = 0
    expected_output = """
  ID     NAMES                            ENABLED    ENABLED    VERSION  FIX
                                          (DEFAULT)  (CURRENT)

  md001  heading-increment, header-incre  True       True       0.6.0    Yes
         ment
  md002  first-heading-h1, first-header-  False      False      0.6.0    No
         h1
  md003  heading-style, header-style      True       True       0.6.0    No
  md022  blanks-around-headings, blanks-  True       True       0.6.0    No
         around-headers
  md023  heading-start-left, header-star  True       True       0.5.2    Yes
         t-left
  md024  no-duplicate-heading, no-duplic  True       True       0.6.0    No
         ate-header
  md036  no-emphasis-as-heading, no-emph  True       True       0.6.0    No
         asis-as-header
  md043  required-headings, required-hea  True       True       0.6.0    No
         ders
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_and_bad_filter() -> None:
    """
    Test to make sure that `plugins list` errors when provided an overly generic filter.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list", "*"]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py plugins list [-h] [--all] [list_filter]
main.py plugins list: error: argument list_filter: Value '*' is not a valid pattern for an id or a name.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_info_and_bad_filter() -> None:
    """
    Test to make sure that `plugins list` errors when provided with a filter
        that is not a valid id or name.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "info", "abc.def"]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py plugins info [-h] info_filter
main.py plugins info: error: argument info_filter: Value 'abc.def' is not a valid id or name.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_info_and_not_found_filter() -> None:
    """
    Test to make sure that `plugins list` errors when a valid id or name is not found.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "info", "md00001"]

    expected_return_code = 1
    expected_output = ""
    expected_error = "Unable to find a plugin with an id or name of 'md00001'."

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_info_and_found_filter() -> None:
    """
    Test to make sure that `plugins info` shows the proper information for the specified plugin.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "info", "md001"]

    expected_return_code = 0
    expected_output = """
  ITEM               DESCRIPTION

  Id                 md001
  Name(s)            heading-increment,header-increment
  Short Description  Heading levels should only increment by one level at a ti
                     me.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md001.md


  CONFIGURATION ITEM  TYPE    VALUE

  front_matter_title  string  "title"

"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_info_and_found_filter_no_configuration() -> None:
    """
    Test to make sure that `plugins info` shows the proper information for the specified plugin
        that does not have any configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "info", "md023"]

    expected_return_code = 0
    expected_output = """  ITEM               DESCRIPTION

  Id                 md023
  Name(s)            heading-start-left,header-start-left
  Short Description  Headings must start at the beginning of the line.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md023.md
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_info_and_found_filter_no_configuration_and_no_url() -> (
    None
):
    """
    Test to make sure that `plugins info` shows the proper information for the specified plugin
        that does not have any configuration or url.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "info", "md999"]

    expected_return_code = 0
    expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1

  ITEM               DESCRIPTION

  Id                 md999
  Name(s)            debug-only
  Short Description  Debug plugin

"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_query_config() -> None:
    """
    Test to make sure we get an error logged if a plugin has an exception during query_config.
    """

    # Arrange
    scanner = MarkdownScanner()
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_query_config.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "plugins",
        "info",
        "mde007",
    ]

    expected_return_code = 1
    expected_output = """MDE007>>init_from_config
MDE007>>init_from_config"""
    expected_error = """
Unexpected Error(BadPluginError): Plugin id 'MDE007' had a critical failure during the '__handle_argparse_subparser_info' action."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_v2_query_config() -> None:
    """
    Test to make sure we get an error logged if a plugin has an old query_config.
    """

    # Arrange
    scanner = MarkdownScanner()
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "old_query_config.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "plugins",
        "info",
        "mde007",
    ]

    expected_return_code = 0
    expected_output = """MDE007>>init_from_config
MDE007>>init_from_config

  ITEM                 DESCRIPTION

  Id                   mde007
  Name(s)              bad-query-config
  Short Description    Test for a old query_config
  Configuration Items  something

"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_and_alternate_output() -> None:
    """
    Copy of test_md001_bad_improper_atx_heading_incrementing but with output
    redirected.
    """

    # Arrange
    scanner = MarkdownScanner(use_main=False, use_alternate_presentation=True)
    source_path = os.path.join("test", "resources", "rules", "md001") + os.sep
    supplied_arguments = [
        "scan",
        f"{source_path}improper_atx_heading_incrementing.md",
    ]

    expected_return_code = 1
    expected_output = (
        f"[pso[[psf[{source_path}improper_atx_heading_incrementing.md:3:1: "
        + "MD001: Heading levels should only increment by one level at a time. "
        + "[Expected: h2; Actual: h3] (heading-increment,header-increment)]]]]\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_detect_issue_report_in_fix_mode() -> None:
    """
    Make sure to test that the triggering of an issue in fix mode is an exception.
    """

    # Arrange
    scanner = MarkdownScanner(use_main=False, use_alternate_presentation=True)
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_next_line_fix.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "fix",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """[pse[[fse[BadPluginError encountered while scanning '{source_path}':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.]]]]
""".replace(
        "{source_path}", source_path
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_detect_issue_report_in_fix_mode_with_stack_trace() -> None:
    """
    Make sure to test that the triggering of an issue in fix mode is an exception.
    """

    # Arrange
    scanner = MarkdownScanner(use_main=False, use_alternate_presentation=True)
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_next_line_fix.py"
    )
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "--stack-trace",
        "fix",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """[pse[[fse[BadPluginError encountered while scanning '{source_path}':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
Actual Line: # This is a test
Caused by: BadPluginError:
   Plugin MDE003(bad-next-line) reported a triggered rule while in fix mode.]]]]
""".replace(
        "{source_path}", source_path
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_normal_token_error() -> None:
    """
    Test to ensure that we can normally cause tokens to be reported.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join("test", "resources", "rules", "md047", "end_with_blank_line.md")
    ) as temp_source_path:
        plugin_path = os.path.join(
            "test", "resources", "plugins", "bad", "bad_end_tokens.py"
        )
        supplied_arguments = [
            "--add-plugin",
            plugin_path,
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = """{path}:0:0: MDE044: Plugin that triggers on end_tokens. (bad-end-tokens)
{path}:0:0: MDE044: Plugin that triggers on end_tokens. (bad-end-tokens)
{path}:0:0: MDE044: Plugin that triggers on end_tokens. (bad-end-tokens)""".replace(
            "{path}", temp_source_path
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output,
            expected_error,
            expected_return_code,
        )


def test_markdown_normal_token_error_not_reported_with_fix() -> None:
    """
    Test to test a version of test_markdown_normal_token_error where fix is
    specified, hence the reporting of the rule violation should not occur.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join("test", "resources", "rules", "md047", "end_with_blank_line.md")
    ) as temp_source_path:
        plugin_path = os.path.join(
            "test", "resources", "plugins", "bad", "bad_end_tokens.py"
        )
        supplied_arguments = [
            "--add-plugin",
            plugin_path,
            "fix",
            temp_source_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output,
            expected_error,
            expected_return_code,
        )


def test_markdown_fixed_issue_with_debug_on() -> None:
    """
    Test to test

    shadow of test_md047_bad_end_with_no_blank_line_fix_and_debug
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join("test", "resources", "rules", "md047", "end_with_no_blank_line.md")
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md009",
            "-x-fix-debug",
            "fix",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = """md010-before:# This is a test:
md047-before:# This is a test:
nl-ltw:# This is a test\\n:
md010-before::
md047-before::
nl-ltw:\\n:
md010-before:The line after this line should be blank.:
md047-before:The line after this line should be blank.:
was_newline_added_at_end_of_file=False
fixed:\\n:
is_line_empty=False
was_modified=True
nl-ltw:The line after this line should be blank.:
cf-ltw:\\n:
FixLineRecord(source='completed_file', line_number=4, plugin_id='md047')
Fixed: {path}""".replace(
            "{path}", temp_source_path
        )
        expected_error = ""
        expected_file_contents = read_contents_of_text_file(temp_source_path) + "\n"

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


def test_markdown_fixed_issue_line_with_debug_and_file_debug_on() -> None:
    """
    Test to test that file debug provides additional data.
    Note that because of temporary files, the std out comparison is
    fairly involved.

    shadow of test_md047_bad_end_with_no_blank_line_fix_and_debug
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join("test", "resources", "rules", "md047", "end_with_no_blank_line.md")
    ) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md009",
            "-x-fix-file-debug",
            "-x-fix-debug",
            "fix",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = """md010-before:# This is a test:
md047-before:# This is a test:
nl-ltw:# This is a test\\n:
md010-before::
md047-before::
nl-ltw:\\n:
md010-before:The line after this line should be blank.:
md047-before:The line after this line should be blank.:
was_newline_added_at_end_of_file=False
fixed:\\n:
is_line_empty=False
was_modified=True
nl-ltw:The line after this line should be blank.:
cf-ltw:\\n:
FixLineRecord(source='completed_file', line_number=4, plugin_id='md047')"""
        expected_error = ""
        initial_file_contents = read_contents_of_text_file(temp_source_path)
        expected_file_contents = initial_file_contents + "\n"

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        assert execute_results.std_err.getvalue() == expected_error
        assert (
            execute_results.return_code == expected_return_code
        ), f"Actual error code ({execute_results.return_code}) and expected error code ({expected_return_code}) differ."
        assert_file_is_as_expected(temp_source_path, expected_file_contents)

        std_out_split = execute_results.std_out.getvalue().splitlines()

        first_section = std_out_split[:4]
        print(first_section)
        assert first_section[0] == ""
        assert first_section[1].startswith("--") and first_section[1].endswith("--")
        assert first_section[2] == initial_file_contents.replace("\n", "\\n")
        assert first_section[3] == "--"

        last_section = std_out_split[-7:]
        print(last_section)
        assert last_section[0] == ""
        assert last_section[1].startswith("--") and last_section[1].endswith("--")
        assert last_section[2] == expected_file_contents.replace("\n", "\\n")
        assert last_section[3] == "--"
        assert last_section[4].startswith("Copy ")
        assert last_section[5].startswith("Remove:")
        assert last_section[6] == f"Fixed: {temp_source_path}"

        middle_section = std_out_split[4:-7]
        print(middle_section)
        split_output = expected_output.splitlines()
        print(split_output)
        assert len(middle_section) == len(split_output)
        for i in range(0, len(split_output)):
            assert middle_section[i] == split_output[i]


def test_markdown_fixed_issue_token_with_debug_and_file_debug_on() -> None:
    """
    Test to test that file debug provides additional data.
    Note that because of temporary files, the std out comparison is
    fairly involved.

    shadow of test_md001_bad_improper_atx_heading_incrementing
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md001",
            "improper_atx_heading_incrementing.md",
        )
    ) as temp_source_path:
        original_file_contents = """# Heading 1

### Heading 3

We skipped out a 2nd level heading in this document
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "-x-fix-file-debug",
            "-x-fix-debug",
            "fix",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_error = ""
        initial_file_contents = read_contents_of_text_file(temp_source_path)
        expected_file_contents = """# Heading 1

## Heading 3

We skipped out a 2nd level heading in this document
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        assert execute_results.std_err.getvalue() == expected_error, (
            "Error results were: " + execute_results.std_err.getvalue()
        )
        assert (
            execute_results.return_code == expected_return_code
        ), f"Actual error code ({execute_results.return_code}) and expected error code ({expected_return_code}) differ."
        assert_file_is_as_expected(temp_source_path, expected_file_contents)

        std_out_split = execute_results.std_out.getvalue().splitlines()
        print(std_out_split)

        first_section = std_out_split[:4]
        print(first_section)

        assert first_section[0] == ""
        assert first_section[1].startswith("--") and first_section[1].endswith("--")
        assert first_section[2] == initial_file_contents.replace("\n", "\\n")
        assert first_section[3] == "--"

        last_section = std_out_split[-8:]
        print(last_section)
        assert last_section[0] == ""
        assert last_section[1].startswith("--") and last_section[1].endswith("--")
        assert last_section[2] == expected_file_contents.replace("\n", "\\n")
        assert last_section[3] == "--"
        assert last_section[4].startswith("Copy ")
        assert last_section[5].startswith("Remove:")
        assert last_section[6].startswith("Remove:")
        assert last_section[7] == f"Fixed: {temp_source_path}"

        # middle_section = std_out_split[4:-8]
        # print("-->")
        # print("\n".join(middle_section))
        # print("<--")
        # split_output = expected_output.splitlines()
        # print(split_output)
        # assert len(middle_section) == len(split_output)
        # for i in range(0, len(split_output)):
        #     assert middle_section[i] == split_output[i]


def test_markdown_plugins_wanting_to_fix_same_token() -> None:
    """
    Test to make sure that
    """

    # Arrange
    scanner = MarkdownScanner()
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_fix_atx_token_like_md001.py"
    )

    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md001",
            "improper_atx_heading_incrementing.md",
        )
    ) as temp_source_path:
        original_file_contents = """# Heading 1

### Heading 3

We skipped out a 2nd level heading in this document
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--add-plugin",
            plugin_path,
            "fix",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = """BadPluginFixError encountered while scanning '{path}':
Multiple plugins (MDE003 and MD001) have requested a fix for the same field of the same token.""".replace(
            "{path}", temp_source_path
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_plugins_wanting_to_fix_and_replace_same_token() -> None:
    """
    Test to make sure that
    """

    # Arrange
    scanner = MarkdownScanner()
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_fix_indented_token_like_md046.py"
    )

    original_file_contents = """~~~Markdown
# fred
~~~
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:

        supplied_arguments = [
            "--set",
            "plugins.md046.style=indented",
            "--add-plugin",
            plugin_path,
            "fix",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = """BadPluginFixError encountered while scanning '{path}':
Multiple plugins (MDE003 and MD046) are in conflict about fixing the token.""".replace(
            "{path}", temp_source_path
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_plugins_wanting_to_replace_same_token() -> None:
    """
    Test to make sure that
    """

    # Arrange
    scanner = MarkdownScanner()
    plugin_path = os.path.join(
        "test",
        "resources",
        "plugins",
        "bad",
        "bad_replace_indented_token_like_md046.py",
    )

    original_file_contents = """~~~Markdown
# fred
~~~

    # fred
"""
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--add-plugin",
            plugin_path,
            "fix",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = """BadPluginFixError encountered while scanning '{path}':
Multiple plugins (MDE003 and MD046) are in conflict about replacing the token.""".replace(
            "{path}", temp_source_path
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_plugins_wanting_to_fix_unknown_token_stack_trace() -> None:
    """
    Test to make sure the rule does trigger with a document with
    only Atx Headings, that when they increase, only increase by 2.
    """

    # Arrange
    scanner = MarkdownScanner()
    plugin_path = os.path.join(
        "test", "resources", "plugins", "bad", "bad_fix_token_unsupported.py"
    )

    with copy_to_temp_file(
        os.path.join(
            "test",
            "resources",
            "rules",
            "md001",
            "improper_atx_heading_incrementing.md",
        )
    ) as temp_source_path:
        supplied_arguments = [
            "--stack-trace",
            "--add-plugin",
            plugin_path,
            "fix",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = """

BadPluginFixError encountered while scanning '{path}':
Plugin id 'MDE003's 'next_token' action requested a token adjustment to field 'hash_count' that failed.
Traceback (most recent call last):
""".replace(
            "{path}", temp_source_path
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output,
            expected_error,
            expected_return_code,
            additional_error=["raise BadPluginFixError( "],
        )
