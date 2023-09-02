"""
Module to provide tests related to the plugin manager for the scanner.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import (
    assert_file_is_as_expected,
    copy_to_temp_file,
    read_contents_of_text_file,
    write_temporary_configuration,
)

# pylint: disable=too-many-lines


def test_markdown_with_plugins_only():
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

optional arguments:
  -h, --help   show this help message and exit
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_and_bad_path():
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


def test_markdown_with_dash_dash_add_plugin_and_single_plugin_file():
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


def test_markdown_with_dash_dash_add_plugin_and_single_plugin_directory():
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


def test_markdown_with_repeated_identifier():
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


def test_markdown_with_bad_identifier():
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


def test_markdown_with_repeated_name():
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


def test_markdown_with_bad_name():
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


def test_markdown_with_dash_dash_add_plugin_and_bad_plugin_file():
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


def test_markdown_with_dash_dash_add_plugin_and_missing_class():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_starting_new_file():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_starting_new_file_with_alternate_output():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_completed_file():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line_fix():
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
        "-x-fix",
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


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line_with_stack_trace():
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
    raise BadPluginError(
pymarkdown.plugin_manager.bad_plugin_error.BadPluginError: (Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line_with_configuration_stack_trace():
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
    raise BadPluginError(
pymarkdown.plugin_manager.bad_plugin_error.BadPluginError: (Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_next_token():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_next_token_with_stack_trace():
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
    raise BadPluginError(
pymarkdown.plugin_manager.bad_plugin_error.BadPluginError: (1,1): Plugin id 'MDE003' had a critical failure during the 'next_token' action.
""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_constructor():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_details():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_details_with_stack_trace():
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
            """    raise BadPluginError(
pymarkdown.plugin_manager.bad_plugin_error.BadPluginError: Plugin class 'BadDetails' had a critical failure loading the plugin details.""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_string_detail():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_string_detail_from_configuration():
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
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
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
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_dash_dash_add_plugin_with_empty_string_detail():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_boolean_detail():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_integer_detail():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_description():
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


def test_markdown_with_dash_dash_add_plugin_with_empty_description():
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


def test_markdown_with_dash_dash_add_plugin_with_blank_description():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_semantic_version():
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


def test_markdown_with_dash_dash_add_plugin_with_bad_interface_version():
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
Plugin 'bad_interface_version.py' with an interface version ('-1') that is not '1' or '2'.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_only():
    """
    Test to make sure that `plugins list` lists all plugins.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list"]

    expected_return_code = 0
    expected_output = """
  ID     NAMES                                   ENABLED    ENABLED    VERSION
                                                 (DEFAULT)  (CURRENT)

  md001  heading-increment, header-increment     True       True       0.5.0
  md002  first-heading-h1, first-header-h1       False      False      0.5.0
  md003  heading-style, header-style             True       True       0.5.0
  md004  ul-style                                True       True       0.5.0
  md005  list-indent                             True       True       0.5.0
  md006  ul-start-left                           False      False      0.5.0
  md007  ul-indent                               True       True       0.5.0
  md009  no-trailing-spaces                      True       True       0.5.0
  md010  no-hard-tabs                            True       True       0.5.0
  md011  no-reversed-links                       True       True       0.5.0
  md012  no-multiple-blanks                      True       True       0.5.0
  md013  line-length                             True       True       0.5.0
  md014  commands-show-output                    True       True       0.5.0
  md018  no-missing-space-atx                    True       True       0.5.0
  md019  no-multiple-space-atx                   True       True       0.5.0
  md020  no-missing-space-closed-atx             True       True       0.5.0
  md021  no-multiple-space-closed-atx            True       True       0.5.0
  md022  blanks-around-headings, blanks-around-  True       True       0.5.0
         headers
  md023  heading-start-left, header-start-left   True       True       0.5.0
  md024  no-duplicate-heading, no-duplicate-hea  True       True       0.5.0
         der
  md025  single-title, single-h1                 True       True       0.5.0
  md026  no-trailing-punctuation                 True       True       0.5.0
  md027  no-multiple-space-blockquote            True       True       0.5.0
  md028  no-blanks-blockquote                    True       True       0.5.0
  md029  ol-prefix                               True       True       0.5.0
  md030  list-marker-space                       True       True       0.5.0
  md031  blanks-around-fences                    True       True       0.5.0
  md032  blanks-around-lists                     True       True       0.5.0
  md033  no-inline-html                          True       True       0.5.1
  md034  no-bare-urls                            True       True       0.5.0
  md035  hr-style                                True       True       0.5.0
  md036  no-emphasis-as-heading, no-emphasis-as  True       True       0.5.0
         -header
  md037  no-space-in-emphasis                    True       True       0.5.0
  md038  no-space-in-code                        True       True       0.5.0
  md039  no-space-in-links                       True       True       0.5.0
  md040  fenced-code-language                    True       True       0.5.0
  md041  first-line-heading, first-line-h1       True       True       0.5.0
  md042  no-empty-links                          True       True       0.5.0
  md043  required-headings, required-headers     True       True       0.5.0
  md044  proper-names                            True       True       0.5.0
  md045  no-alt-text                             True       True       0.5.0
  md046  code-block-style                        True       True       0.5.0
  md047  single-trailing-newline                 True       True       0.5.0
  md048  code-fence-style                        True       True       0.5.0

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


def test_markdown_with_plugins_list_only_all():
    """
    Test to make sure that `plugins list` lists all plugins, even ones
        that may not usually appear.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list", "--all"]

    expected_return_code = 0
    expected_output = """
  ID     NAMES                                   ENABLED    ENABLED    VERSION
                                                 (DEFAULT)  (CURRENT)

  md001  heading-increment, header-increment     True       True       0.5.0
  md002  first-heading-h1, first-header-h1       False      False      0.5.0
  md003  heading-style, header-style             True       True       0.5.0
  md004  ul-style                                True       True       0.5.0
  md005  list-indent                             True       True       0.5.0
  md006  ul-start-left                           False      False      0.5.0
  md007  ul-indent                               True       True       0.5.0
  md009  no-trailing-spaces                      True       True       0.5.0
  md010  no-hard-tabs                            True       True       0.5.0
  md011  no-reversed-links                       True       True       0.5.0
  md012  no-multiple-blanks                      True       True       0.5.0
  md013  line-length                             True       True       0.5.0
  md014  commands-show-output                    True       True       0.5.0
  md018  no-missing-space-atx                    True       True       0.5.0
  md019  no-multiple-space-atx                   True       True       0.5.0
  md020  no-missing-space-closed-atx             True       True       0.5.0
  md021  no-multiple-space-closed-atx            True       True       0.5.0
  md022  blanks-around-headings, blanks-around-  True       True       0.5.0
         headers
  md023  heading-start-left, header-start-left   True       True       0.5.0
  md024  no-duplicate-heading, no-duplicate-hea  True       True       0.5.0
         der
  md025  single-title, single-h1                 True       True       0.5.0
  md026  no-trailing-punctuation                 True       True       0.5.0
  md027  no-multiple-space-blockquote            True       True       0.5.0
  md028  no-blanks-blockquote                    True       True       0.5.0
  md029  ol-prefix                               True       True       0.5.0
  md030  list-marker-space                       True       True       0.5.0
  md031  blanks-around-fences                    True       True       0.5.0
  md032  blanks-around-lists                     True       True       0.5.0
  md033  no-inline-html                          True       True       0.5.1
  md034  no-bare-urls                            True       True       0.5.0
  md035  hr-style                                True       True       0.5.0
  md036  no-emphasis-as-heading, no-emphasis-as  True       True       0.5.0
         -header
  md037  no-space-in-emphasis                    True       True       0.5.0
  md038  no-space-in-code                        True       True       0.5.0
  md039  no-space-in-links                       True       True       0.5.0
  md040  fenced-code-language                    True       True       0.5.0
  md041  first-line-heading, first-line-h1       True       True       0.5.0
  md042  no-empty-links                          True       True       0.5.0
  md043  required-headings, required-headers     True       True       0.5.0
  md044  proper-names                            True       True       0.5.0
  md045  no-alt-text                             True       True       0.5.0
  md046  code-block-style                        True       True       0.5.0
  md047  single-trailing-newline                 True       True       0.5.0
  md048  code-fence-style                        True       True       0.5.0
  md999  debug-only                              False      False      0.0.0

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


def test_markdown_with_plugins_list_and_filter_by_id_ends_with_nine():
    """
    Test to make sure that `plugins list` lists all plugins with the specified id filter.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list", "md*9"]

    expected_return_code = 0
    expected_output = """
  ID     NAMES                  ENABLED    ENABLED    VERSION
                                (DEFAULT)  (CURRENT)

  md009  no-trailing-spaces     True       True       0.5.0
  md019  no-multiple-space-atx  True       True       0.5.0
  md029  ol-prefix              True       True       0.5.0
  md039  no-space-in-links      True       True       0.5.0

"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_and_filter_by_id_ends_with_non_sequence():
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


def test_markdown_with_plugins_list_and_filter_by_name_link():
    """
    Test to make sure that `plugins list` lists all plugins with the specified name filter.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list", "*header*"]

    expected_return_code = 0
    expected_output = """
  ID     NAMES                                   ENABLED    ENABLED    VERSION
                                                 (DEFAULT)  (CURRENT)

  md001  heading-increment, header-increment     True       True       0.5.0
  md002  first-heading-h1, first-header-h1       False      False      0.5.0
  md003  heading-style, header-style             True       True       0.5.0
  md022  blanks-around-headings, blanks-around-  True       True       0.5.0
         headers
  md023  heading-start-left, header-start-left   True       True       0.5.0
  md024  no-duplicate-heading, no-duplicate-hea  True       True       0.5.0
         der
  md036  no-emphasis-as-heading, no-emphasis-as  True       True       0.5.0
         -header
  md043  required-headings, required-headers     True       True       0.5.0
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_and_bad_filter():
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


def test_markdown_with_plugins_info_and_bad_filter():
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


def test_markdown_with_plugins_info_and_not_found_filter():
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


def test_markdown_with_plugins_info_and_found_filter():
    """
    Test to make sure that `plugins info` shows the proper information for the specified plugin.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "info", "md001"]

    expected_return_code = 0
    expected_output = """  ITEM                 DESCRIPTION

  Id                   md001
  Name(s)              heading-increment,header-increment
  Short Description    Heading levels should only increment by one level at a
                       time.
  Description Url      https://github.com/jackdewinter/pymarkdown/blob/main/do
                       cs/rules/rule_md001.md
  Configuration Items  front_matter_title
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_info_and_found_filter_no_configuration():
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
  Description Url    https://github.com/jackdewinter/pymarkdown/blob/main/docs
                     /rules/rule_md023.md
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_info_and_found_filter_no_configuration_and_no_url():
    """
    Test to make sure that `plugins info` shows the proper information for the specified plugin
        that does not have any configuration or url.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "info", "md999"]

    expected_return_code = 0
    expected_output = """  ITEM               DESCRIPTION

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


def test_markdown_with_plugins_and_alternate_output():
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


def test_markdown_detect_issue_report_in_fix_mode():
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
        "-x-fix",
        "scan",
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


def test_markdown_detect_issue_report_in_fix_mode_with_stack_trace():
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
        "-x-fix",
        "--stack-trace",
        "scan",
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


def test_markdown_normal_token_error():
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


def test_markdown_normal_token_error_not_reported_with_fix():
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
            "-x-fix",
            "scan",
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


def test_markdown_fixed_issue_with_debug_on():
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
            "-x-fix",
            "scan",
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


def test_markdown_fixed_issue_line_with_debug_and_file_debug_on():
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
            "-x-fix",
            "scan",
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


def test_markdown_fixed_issue_token_with_debug_and_file_debug_on():
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
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = """md009-before:# Heading 1:
md010-before:# Heading 1:
md047-before:# Heading 1:
nl-ltw:# Heading 1\\n:
md009-before::
md010-before::
md047-before::
nl-ltw:\\n:
md009-before:## Heading 3:
md010-before:## Heading 3:
md047-before:## Heading 3:
nl-ltw:## Heading 3\\n:
md009-before::
md010-before::
md047-before::
nl-ltw:\\n:
md009-before:We skipped out a 2nd level heading in this document:
md010-before:We skipped out a 2nd level heading in this document:
md047-before:We skipped out a 2nd level heading in this document:
nl-ltw:We skipped out a 2nd level heading in this document\\n:
md009-before::
md010-before::
md047-before::
was_newline_added_at_end_of_file=True
fixed:We skipped out a 2nd level heading in this document\\n:
is_line_empty=True
was_modified=True
nl-ltw::"""
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

        first_section = std_out_split[:12]
        print(first_section)

        assert first_section[0] == ""
        assert first_section[1].startswith("--") and first_section[1].endswith("--")
        assert first_section[2] == initial_file_contents.replace("\n", "\\n")
        assert first_section[3] == "--"
        assert (
            first_section[4]
            == "BEFORE:[atx(3,1):3:0:]:[FixTokenRecord(token_to_fix='[atx(3,1):3:0:]', plugin_id='MD001', plugin_action='next_token', field_name='hash_count', field_value=2)]"
        )
        assert (
            first_section[5]
            == " AFTER:[atx(3,1):2:0:]:[FixTokenRecord(token_to_fix='[atx(3,1):2:0:]', plugin_id='MD001', plugin_action='next_token', field_name='hash_count', field_value=2)]"
        )
        assert first_section[6] == "--"
        assert first_section[7] == ""
        assert first_section[8].startswith("--") and first_section[1].endswith("--")
        assert first_section[9] == expected_file_contents.replace("\n", "\\n")
        assert first_section[10] == "--"
        assert first_section[11].startswith("scan: ")

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

        middle_section = std_out_split[12:-8]
        print("-->")
        print("\n".join(middle_section))
        print("<--")
        split_output = expected_output.splitlines()
        print(split_output)
        assert len(middle_section) == len(split_output)
        for i in range(0, len(split_output)):
            assert middle_section[i] == split_output[i]


def test_markdown_plugins_wanting_to_fix_same_token():
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
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = """BadPluginFixError encountered while scanning '{path}':
More than one plugin has requested a fix for the same field of the same token.""".replace(
            "{path}", temp_source_path
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def test_markdown_plugins_wanting_to_fix_unknown_token():
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
            "--add-plugin",
            plugin_path,
            "-x-fix",
            "--stack-trace",
            "scan",
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
            additional_error="raise BadPluginFixError( ",
        )
