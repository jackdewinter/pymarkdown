"""
Module to provide tests related to the plugin manager for the scanner.
"""
import os
from test.markdown_scanner import MarkdownScanner

from .utils import write_temporary_configuration

# pylint: disable=too-many-lines


def test_markdown_with_plugins_only():
    """
    Test to make sure
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
    Test to make sure we get enable a rule if '--add-plugin' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "MD047",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    Test to make sure we get enable a rule if '--add-plugin' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/plugin_two.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    Test to make sure we get enable a rule if '--add-plugin' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    Test to make sure we get enable a rule if '--add-plugin' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/duplicate_id_debug.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    Test to make sure we get enable a rule if '--add-plugin' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_id.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    Test to make sure we get enable a rule if '--add-plugin' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/duplicate_name_debug.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    Test to make sure we get enable a rule if '--add-plugin' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_name.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    Test to make sure we get enable a rule if '--add-plugin' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/not-a-python-file.txt",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    Test to make sure we get enable a rule if '--add-plugin' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/misnamed.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    Test to make sure we get an error logged if a plugin throws an exception within the starting_new_file function.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_starting_new_file.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning 'test/resources/rules/md047/end_with_blank_line.md':
Plugin id 'MDE001' had a critical failure during the 'starting_new_file' action.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_completed_file():
    """
    Test to make sure we get an error logged if a plugin throws an exception within the completed_file function.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_completed_file.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning 'test/resources/rules/md047/end_with_blank_line.md':
Plugin id 'MDE002' had a critical failure during the 'completed_file' action.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line():
    """
    Test to make sure we get an error logged if a plugin throws an exception within the next_line function.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_next_line.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning 'test/resources/rules/md047/end_with_blank_line.md':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line_with_stack_trace():
    """
    Test to make sure we get an error logged if a plugin throws an exception within the next_line function.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--stack-trace",
        "--add-plugin",
        "test/resources/plugins/bad/bad_next_line.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning 'test/resources/rules/md047/end_with_blank_line.md':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
Actual Line: # This is a test
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
            """    raise Exception("bad next_line")
Exception: bad next_line

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
""",
            """, in next_line
    raise BadPluginError(
pymarkdown.plugin_manager.BadPluginError: (Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line_with_configuration_stack_trace():
    """
    Test to make sure we get an error logged if a plugin throws an exception within the next_line function.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--stack-trace",
        "--add-plugin",
        "test/resources/plugins/bad/bad_next_line.py",
        "--set",
        "log.stack-trace=$!True",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning 'test/resources/rules/md047/end_with_blank_line.md':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
Actual Line: # This is a test
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
            """    raise Exception("bad next_line")
Exception: bad next_line

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
""",
            """, in next_line
    raise BadPluginError(
pymarkdown.plugin_manager.BadPluginError: (Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_next_token():
    """
    Test to make sure we get an error logged if a plugin throws an exception within the next_token function.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_next_token.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning 'test/resources/rules/md047/end_with_blank_line.md':
(1,1): Plugin id 'MDE003' had a critical failure during the 'next_token' action.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_next_token_with_stack_trace():
    """
    Test to make sure we get an error logged if a plugin throws an exception within the next_token function.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--stack-trace",
        "--add-plugin",
        "test/resources/plugins/bad/bad_next_token.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning 'test/resources/rules/md047/end_with_blank_line.md':
(1,1): Plugin id 'MDE003' had a critical failure during the 'next_token' action.
Actual Token: [atx(1,1):1:0:]
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
            """    raise Exception("bad next_token")
Exception: bad next_token

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
""",
            """, in next_token
    raise BadPluginError(
pymarkdown.plugin_manager.BadPluginError: (1,1): Plugin id 'MDE003' had a critical failure during the 'next_token' action.
""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_constructor():
    """
    Test to make sure we get an error logged if a plugin throws an exception within the constructor function.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_constructor.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    Test to make sure we get an error logged if a plugin throws an exception within the details function.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_details.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    Test to make sure we get an error logged if a plugin throws an exception within the details function.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--stack-trace",
        "--add-plugin",
        "test/resources/plugins/bad/bad_details.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
pymarkdown.plugin_manager.BadPluginError: Plugin class 'BadDetails' had a critical failure loading the plugin details.""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_string_detail():
    """
    Test to make sure we get an error logged if a plugin throws an exception that a string detail is bad.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_string_detail_is_int.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {
        "plugins": {
            "additional_paths": "test/resources/plugins/bad/bad_string_detail_is_int.py"
        }
    }
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md047/end_with_blank_line.md",
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
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_string_detail_is_empty.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_boolean_detail_is_int.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    Test to make sure we get an error logged if a plugin throws an exception that a integer detail is bad.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_integer_detail_is_string.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_description.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    Test to make sure we get an error logged if a plugin returns a empty description.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/empty_description.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/blank_description.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_semantic_version.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
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
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_interface_version.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin 'bad_interface_version.py' with an interface version ('2') that is not '1'.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_only():
    """
    Test to make sure
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
  md018  no-missing-space-atx                    True       True       0.5.0
  md019  no-multiple-space-atx                   True       True       0.5.0
  md020  no-missing-space-closed-atx             True       True       0.5.0
  md021  no-multiple-space-closed-atx            True       True       0.5.0
  md022  blanks-around-headings, blanks-around-  True       True       0.5.0
         headers
  md023  heading-start-left, header-start-left   True       True       0.5.0
  md024  no-duplicate-heading, no-duplicate-hea  True       True       0.5.0
         der
  md026  no-trailing-punctuation                 True       True       0.5.0
  md036  no-emphasis-as-heading, no-emphasis-as  True       True       0.5.0
         -header
  md047  single-trailing-newline                 True       True       0.5.0

"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_only_all():
    """
    Test to make sure
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
  md004  ul-style                                False      False      0.0.0
  md005  list-indent                             False      False      0.0.0
  md006  ul-start-left                           False      False      0.0.0
  md007  ul-indent                               False      False      0.0.0
  md009  no-trailing-spaces                      False      False      0.0.0
  md010  no-hard-tabs                            False      False      0.0.0
  md011  no-reversed-links                       False      False      0.0.0
  md012  no-multiple-blanks                      False      False      0.0.0
  md013  line-length                             False      False      0.0.0
  md014  commands-show-output                    False      False      0.0.0
  md018  no-missing-space-atx                    True       True       0.5.0
  md019  no-multiple-space-atx                   True       True       0.5.0
  md020  no-missing-space-closed-atx             True       True       0.5.0
  md021  no-multiple-space-closed-atx            True       True       0.5.0
  md022  blanks-around-headings, blanks-around-  True       True       0.5.0
         headers
  md023  heading-start-left, header-start-left   True       True       0.5.0
  md024  no-duplicate-heading, no-duplicate-hea  True       True       0.5.0
         der
  md025  single-title, single-h1                 False      False      0.0.0
  md026  no-trailing-punctuation                 True       True       0.5.0
  md027  no-multiple-space-blockquote            False      False      0.0.0
  md028  no-blanks-blockquote                    False      False      0.0.0
  md029  ol-prefix                               False      False      0.0.0
  md030  list-marker-space                       False      False      0.0.0
  md031  blanks-around-fences                    False      False      0.0.0
  md032  blanks-around-lists                     False      False      0.0.0
  md033  no-inline-html                          False      False      0.0.0
  md034  no-bare-urls                            False      False      0.0.0
  md035  hr-style                                False      False      0.0.0
  md036  no-emphasis-as-heading, no-emphasis-as  True       True       0.5.0
         -header
  md037  no-space-in-emphasis                    False      False      0.0.0
  md038  no-space-in-code                        False      False      0.0.0
  md039  no-space-in-links                       False      False      0.0.0
  md040  fenced-code-language                    False      False      0.0.0
  md041  first-line-heading, first-line-h1       False      False      0.0.0
  md042  no-empty-links                          False      False      0.0.0
  md043  required-headings, required-headers     False      False      0.0.0
  md044  proper-names                            False      False      0.0.0
  md045  no-alt-text                             False      False      0.0.0
  md046  code-block-style                        False      False      0.0.0
  md047  single-trailing-newline                 True       True       0.5.0
  md048  code-fence-style                        False      False      0.0.0

"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_and_filter_by_id_ends_with_nine():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list", "md*9"]

    expected_return_code = 0
    expected_output = """
  ID     NAMES                  ENABLED    ENABLED    VERSION
                                (DEFAULT)  (CURRENT)

  md019  no-multiple-space-atx  True       True       0.5.0

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
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list", "this-is-not-an-used-identifier"]

    expected_return_code = 0
    expected_output = """No plugin rule identifiers matches the pattern 'this-is-not-an-used-identifier'."""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_list_and_filter_by_name_link():
    """
    Test to make sure
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
    Test to make sure
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
    Test to make sure
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
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "info", "md00001"]

    expected_return_code = 1
    expected_output = "Unable to find a plugin with an id or name of 'md00001'."
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_plugins_info_and_found_filter():
    """
    Test to make sure
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
    Test to make sure
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
    Test to make sure
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
