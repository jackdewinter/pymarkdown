"""
Module to provide tests related to the plugin manager for the scanner.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.utils import (
    ARGPARSE_X,
    assert_file_is_as_expected,
    copy_to_temp_file,
    create_temporary_configuration_file,
    create_temporary_markdown_file,
    generate_path_to_bad_plugin,
    read_contents_of_text_file,
)
from typing import Tuple

# pylint: disable=too-many-lines


def __generate_source_path(
    source_file_name: str, alterate_rule: str = "md047"
) -> Tuple[str, str]:
    source_path = os.path.join(
        "test", "resources", "rules", alterate_rule, source_file_name
    )
    return source_path, os.path.abspath(source_path)


def test_markdown_with_plugins_only(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure "plugins" from the command line shows help
    """

    # Arrange
    supplied_arguments = [
        "plugins",
    ]

    expected_results = ExpectedResults(
        return_code=2,
        expected_output="""usage: main.py plugins [-h] {list,info} ...

positional arguments:
  {list,info}
    list       list the available plugins
    info       information on a specific plugin

{ARGPARSE_X}
  -h, --help   show this help message and exit
""".replace("{ARGPARSE_X}", ARGPARSE_X),
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_and_bad_path(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error if '--add-plugin' is supplied with a bad path.

    This function shadows
    test_api_plugins_add_with_bad_path
    and
    test_markdown_return_code_default_system_error.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    supplied_arguments = [
        "--add-plugin",
        "MD047",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while loading plugins:
Plugin path 'MD047' does not exist.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_and_single_plugin_file(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we add a plugin if '--add-plugin' is supplied with a valid plugin.

    This test shadows
    test_api_plugins_add_with_simple_plugin
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/plugin_two.py",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=0,
        expected_output="""MD998>>init_from_config
MD998>>starting_new_file>>
MD998>>next_line:# This is a test
MD998>>next_line:
MD998>>next_line:The line after this line should be blank.
MD998>>next_line:
MD998>>completed_file
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_and_single_plugin_directory(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we add a plugin if '--add-plugin' is supplied with a valid plugin directory.

    This function shadows
    test_api_plugins_add_with_simple_plugins_by_directory
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    supplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=0,
        expected_output="""MD998>>init_from_config
MD998>>starting_new_file>>
MD998>>next_line:# This is a test
MD998>>next_line:
MD998>>next_line:The line after this line should be blank.
MD998>>next_line:
MD998>>completed_file
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_repeated_identifier(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure we report an error if '--add-plugin' is supplied with a plugin that
    specifies an already present id.

    This function shadows
    test_api_plugins_add_with_repeated_identifier
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("duplicate_id_debug.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""ValueError encountered while initializing plugins:
Unable to register plugin 'duplicate_id_debug.py' with id 'md999' as plugin 'plugin_one.py' is already registered with that id.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_bad_identifier(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure we report an error if '--add-plugin' is supplied with a plugin that
        specifies an invalid id.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_id.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""ValueError encountered while initializing plugins:
Unable to register plugin 'bad_id.py' with id 'debug-only' as id is not a valid id in the form 'aannn' or 'aaannn'.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_repeated_name(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure we report an error if '--add-plugin' is supplied with a plugin that
        specifies an already present name.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("duplicate_name_debug.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""ValueError encountered while initializing plugins:
Unable to register plugin 'duplicate_name_debug.py' with name 'debug-only' as plugin 'plugin_one.py' is already registered with that name.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_bad_name(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure we report an error if '--add-plugin' is supplied with a plugin that
        specifies a bad name.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_name.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""ValueError encountered while initializing plugins:
Unable to register plugin 'bad_name.py' with name 'debug.only' as name is not a valid name in the form 'an-an'.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_and_bad_plugin_file(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we report an error if '--add-plugin' is supplied with a plugin file
        that is not really a plugin file.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("not-a-python-file.txt")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while loading plugins:
Plugin file named 'not-a-python-file.txt' cannot be loaded.\n""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_and_missing_class(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we report an error if '--add-plugin' is supplied with a plugin file
        that does not specify a plugin with the same name.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("misnamed.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while loading plugins:
Plugin file named 'misnamed.py' does not contain a class named 'Misnamed'.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_starting_new_file(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the starting_new_file function.

    This function shadows
    test_api_plugins_add_with_bad_starting_new_file
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_starting_new_file.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error=f"""BadPluginError encountered while scanning '{abs_source_path}':
Plugin id 'MDE001' had a critical failure during the 'starting_new_file' action.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_starting_new_file_with_alternate_output() -> (
    None
):
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the starting_new_file function.
    """

    # Arrange
    scanner = MarkdownScanner(use_main=False, use_alternate_presentation=True)
    source_path, abs_source_path = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_starting_new_file.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error=f"""[pse[[fse[BadPluginError encountered while scanning '{abs_source_path}':
Plugin id 'MDE001' had a critical failure during the 'starting_new_file' action.]]]]
""",
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_completed_file(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the completed_file function.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_completed_file.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error=f"""BadPluginError encountered while scanning '{abs_source_path}':
Plugin id 'MDE002' had a critical failure during the 'completed_file' action.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the next_line function.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_next_line.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error=f"""BadPluginError encountered while scanning '{abs_source_path}':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line_fix(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the next_line function.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_next_line.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "fix",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error=f"""BadPluginError encountered while scanning '{abs_source_path}':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line_with_stack_trace(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the next_line function.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_next_line.py")
    supplied_arguments = [
        "--stack-trace",
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = f"""BadPluginError encountered while scanning '{abs_source_path}':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
Actual Line: # This is a test
Caused by: Exception:
   bad next_line
Traceback (most recent call last):
"""

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

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


def test_markdown_with_dash_dash_add_plugin_with_bad_next_line_with_configuration_stack_trace(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the next_line function.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_next_line.py")
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
    expected_error = f"""BadPluginError encountered while scanning '{abs_source_path}':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
Actual Line: # This is a test
Caused by: Exception:
   bad next_line
Traceback (most recent call last):
"""

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

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


def test_markdown_with_dash_dash_add_plugin_with_bad_next_token(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the next_token function.

    This function shadows
    test_api_plugins_add_with_bad_next_token
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_next_token.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error=f"""BadPluginError encountered while scanning '{abs_source_path}':
(1,1): Plugin id 'MDE003' had a critical failure during the 'next_token' action.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_next_token_with_stack_trace(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the next_token function.

    This function shadows
    test_api_plugins_add_with_bad_next_token_and_stack_trace
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_next_token.py")
    supplied_arguments = [
        "--stack-trace",
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = f"""BadPluginError encountered while scanning '{abs_source_path}':
(1,1): Plugin id 'MDE003' had a critical failure during the 'next_token' action.
Actual Token: [atx(1,1):1:0:]
Caused by: Exception:
   bad next_token
Traceback (most recent call last):
"""

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

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


def test_markdown_with_dash_dash_add_plugin_with_bad_constructor(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the constructor function.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_constructor.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while loading plugins:
Plugin file named 'bad_constructor.py' threw an exception in the constructor for the class 'BadConstructor'.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_details(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the details function.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_details.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while loading plugins:
Plugin class 'BadDetails' had a critical failure loading the plugin details.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_details_with_stack_trace(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        within the details function.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_details.py")
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
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

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


def test_markdown_with_dash_dash_add_plugin_with_bad_string_detail(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception
        that a descirption is bad.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_string_detail_is_int.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while loading plugins:
Plugin class 'BadStringDetailIsInt' returned an improperly typed value for field name 'plugin_description'.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_string_detail_from_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception that a string detail is bad.
    Note: this version loads from configuration.

    This function shadows
    test_api_plugins_add_with_bad_load_due_to_configuration
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_string_detail_is_int.py")
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

        expected_results = ExpectedResults(
            return_code=1,
            expected_error="""\n\nBadPluginError encountered while loading plugins:
Plugin class 'BadStringDetailIsInt' returned an improperly typed value for field name 'plugin_description'.
""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_empty_string_detail(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception that a string detail is empty.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_string_detail_is_empty.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while loading plugins:
Plugin class 'BadStringDetailIsEmpty' returned an empty value for field name 'plugin_description'.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_boolean_detail(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception that a boolean detail is bad.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_boolean_detail_is_int.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while loading plugins:
Plugin class 'BadBooleanDetailIsInt' returned an improperly typed value for field name 'plugin_enabled_by_default'.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_integer_detail(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin throws an exception that an integer detail is bad.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_integer_detail_is_string.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while loading plugins:
Plugin class 'BadIntegerDetailIsString' returned an improperly typed value for field name 'plugin_interface_version'.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_description(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin returns a bad description.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_description.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while loading plugins:
Plugin class 'BadDescription' returned an improperly typed value for field name 'plugin_description'.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_empty_description(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin returns an empty description.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("empty_description.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while loading plugins:
Plugin class 'EmptyDescription' returned an empty value for field name 'plugin_description'.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_blank_description(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin returns a blank description.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("blank_description.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""ValueError encountered while initializing plugins:
Unable to register plugin 'blank_description.py' with a description string that is blank.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_semantic_version(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin returns a bad semantic version.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_semantic_version.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""ValueError encountered while initializing plugins:
Unable to register plugin 'bad_semantic_version.py' with a version string that is not a valid semantic version.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_interface_version(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin returns a bad interface version.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_interface_version.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="""BadPluginError encountered while loading plugins:
Plugin 'bad_interface_version.py' with an interface version ('-1') that is not '1', '2', or '3'.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_plugins_list_only(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure that `plugins list` lists all plugins.
    """

    # Arrange
    supplied_arguments = ["plugins", "list"]

    expected_results = ExpectedResults(
        return_code=0,
        expected_output="""
  ID      NAMES                           ENABLED    ENABLED    VERSION  FIX
                                          (DEFAULT)  (CURRENT)

  md001   heading-increment, header-incr  True       True       0.6.0    Yes
          ement
  md002   first-heading-h1, first-header  False      False      0.6.1    No
          -h1
  md003   heading-style, header-style     True       True       0.6.1    No
  md004   ul-style                        True       True       0.6.0    Yes
  md005   list-indent                     True       True       0.5.2    Yes
  md006   ul-start-left                   False      False      0.5.1    Yes
  md007   ul-indent                       True       True       0.6.1    Yes
  md009   no-trailing-spaces              True       True       0.6.1    Yes
  md010   no-hard-tabs                    True       True       0.6.1    Yes
  md011   no-reversed-links               True       True       0.5.1    No
  md012   no-multiple-blanks              True       True       0.7.0    Yes
  md013   line-length                     True       True       0.6.1    No
  md014   commands-show-output            True       True       0.5.0    No
  md018   no-missing-space-atx            True       True       0.5.1    No
  md019   no-multiple-space-atx           True       True       0.5.1    Yes
  md020   no-missing-space-closed-atx     True       True       0.5.1    No
  md021   no-multiple-space-closed-atx    True       True       0.5.1    Yes
  md022   blanks-around-headings, blanks  True       True       0.6.0    No
          -around-headers
  md023   heading-start-left, header-sta  True       True       0.5.3    Yes
          rt-left
  md024   no-duplicate-heading, no-dupli  True       True       0.6.1    No
          cate-header
  md025   single-title, single-h1         True       True       0.6.1    No
  md026   no-trailing-punctuation         True       True       0.6.0    No
  md027   no-multiple-space-blockquote    True       True       0.5.2    Yes
  md028   no-blanks-blockquote            True       True       0.5.0    No
  md029   ol-prefix                       True       True       0.6.0    Yes
  md030   list-marker-space               True       True       0.6.0    Yes
  md031   blanks-around-fences            True       True       0.7.1    Yes
  md032   blanks-around-lists             True       True       0.5.1    No
  md033   no-inline-html                  True       True       0.6.0    No
  md034   no-bare-urls                    True       True       0.5.1    No
  md035   hr-style                        True       True       0.6.0    Yes
  md036   no-emphasis-as-heading, no-emp  True       True       0.6.0    No
          hasis-as-header
  md037   no-space-in-emphasis            True       True       0.5.2    Yes
  md038   no-space-in-code                True       True       0.5.1    Yes
  md039   no-space-in-links               True       True       0.5.2    Yes
  md040   fenced-code-language            True       True       0.5.0    No
  md041   first-line-heading, first-line  True       True       0.7.1    No
          -h1
  md042   no-empty-links                  True       True       0.5.0    No
  md043   required-headings, required-he  True       True       0.6.1    No
          aders
  md044   proper-names                    True       True       0.7.1    Yes
  md045   no-alt-text                     True       True       0.5.0    No
  md046   code-block-style                True       True       0.7.0    Yes
  md047   single-trailing-newline         True       True       0.5.2    Yes
  md048   code-fence-style                True       True       0.6.0    Yes
  pml100  disallowed-html                 False      False      0.6.0    No
  pml101  list-anchored-indent            False      False      0.6.0    No
  pml102  disallow-lazy-list-indentation  False      False      0.5.0    No  
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_plugins_list_only_all(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure that `plugins list` lists all plugins, even ones
        that may not usually appear.
    """

    # Arrange
    supplied_arguments = ["plugins", "list", "--all"]

    expected_results = ExpectedResults(
        return_code=0,
        expected_output="""
  ID      NAMES                           ENABLED    ENABLED    VERSION  FIX
                                          (DEFAULT)  (CURRENT)

  md001   heading-increment, header-incr  True       True       0.6.0    Yes
          ement
  md002   first-heading-h1, first-header  False      False      0.6.1    No
          -h1
  md003   heading-style, header-style     True       True       0.6.1    No
  md004   ul-style                        True       True       0.6.0    Yes
  md005   list-indent                     True       True       0.5.2    Yes
  md006   ul-start-left                   False      False      0.5.1    Yes
  md007   ul-indent                       True       True       0.6.1    Yes
  md009   no-trailing-spaces              True       True       0.6.1    Yes
  md010   no-hard-tabs                    True       True       0.6.1    Yes
  md011   no-reversed-links               True       True       0.5.1    No
  md012   no-multiple-blanks              True       True       0.7.0    Yes
  md013   line-length                     True       True       0.6.1    No
  md014   commands-show-output            True       True       0.5.0    No
  md018   no-missing-space-atx            True       True       0.5.1    No
  md019   no-multiple-space-atx           True       True       0.5.1    Yes
  md020   no-missing-space-closed-atx     True       True       0.5.1    No
  md021   no-multiple-space-closed-atx    True       True       0.5.1    Yes
  md022   blanks-around-headings, blanks  True       True       0.6.0    No
          -around-headers
  md023   heading-start-left, header-sta  True       True       0.5.3    Yes
          rt-left
  md024   no-duplicate-heading, no-dupli  True       True       0.6.1    No
          cate-header
  md025   single-title, single-h1         True       True       0.6.1    No
  md026   no-trailing-punctuation         True       True       0.6.0    No
  md027   no-multiple-space-blockquote    True       True       0.5.2    Yes
  md028   no-blanks-blockquote            True       True       0.5.0    No
  md029   ol-prefix                       True       True       0.6.0    Yes
  md030   list-marker-space               True       True       0.6.0    Yes
  md031   blanks-around-fences            True       True       0.7.1    Yes
  md032   blanks-around-lists             True       True       0.5.1    No
  md033   no-inline-html                  True       True       0.6.0    No
  md034   no-bare-urls                    True       True       0.5.1    No
  md035   hr-style                        True       True       0.6.0    Yes
  md036   no-emphasis-as-heading, no-emp  True       True       0.6.0    No
          hasis-as-header
  md037   no-space-in-emphasis            True       True       0.5.2    Yes
  md038   no-space-in-code                True       True       0.5.1    Yes
  md039   no-space-in-links               True       True       0.5.2    Yes
  md040   fenced-code-language            True       True       0.5.0    No
  md041   first-line-heading, first-line  True       True       0.7.1    No
          -h1
  md042   no-empty-links                  True       True       0.5.0    No
  md043   required-headings, required-he  True       True       0.6.1    No
          aders
  md044   proper-names                    True       True       0.7.1    Yes
  md045   no-alt-text                     True       True       0.5.0    No
  md046   code-block-style                True       True       0.7.0    Yes
  md047   single-trailing-newline         True       True       0.5.2    Yes
  md048   code-fence-style                True       True       0.6.0    Yes
  md999   debug-only                      False      False      0.0.0    No
  pml100  disallowed-html                 False      False      0.6.0    No
  pml101  list-anchored-indent            False      False      0.6.0    No
  pml102  disallow-lazy-list-indentation  False      False      0.5.0    No
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_plugins_list_after_command_line_disable_all_rules(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that `plugins list` lists all plugins after disabling all rules.
    """

    # Arrange
    supplied_arguments = ["--disable-rules", "*", "plugins", "list"]

    expected_results = ExpectedResults(
        return_code=0,
        expected_output="""
  ID      NAMES                           ENABLED    ENABLED    VERSION  FIX
                                          (DEFAULT)  (CURRENT)

  md001   heading-increment, header-incr  True       False      0.6.0    Yes
          ement
  md002   first-heading-h1, first-header  False      False      0.6.1    No
          -h1
  md003   heading-style, header-style     True       False      0.6.1    No
  md004   ul-style                        True       False      0.6.0    Yes
  md005   list-indent                     True       False      0.5.2    Yes
  md006   ul-start-left                   False      False      0.5.1    Yes
  md007   ul-indent                       True       False      0.6.1    Yes
  md009   no-trailing-spaces              True       False      0.6.1    Yes
  md010   no-hard-tabs                    True       False      0.6.1    Yes
  md011   no-reversed-links               True       False      0.5.1    No
  md012   no-multiple-blanks              True       False      0.7.0    Yes
  md013   line-length                     True       False      0.6.1    No
  md014   commands-show-output            True       False      0.5.0    No
  md018   no-missing-space-atx            True       False      0.5.1    No
  md019   no-multiple-space-atx           True       False      0.5.1    Yes
  md020   no-missing-space-closed-atx     True       False      0.5.1    No
  md021   no-multiple-space-closed-atx    True       False      0.5.1    Yes
  md022   blanks-around-headings, blanks  True       False      0.6.0    No
          -around-headers
  md023   heading-start-left, header-sta  True       False      0.5.3    Yes
          rt-left
  md024   no-duplicate-heading, no-dupli  True       False      0.6.1    No
          cate-header
  md025   single-title, single-h1         True       False      0.6.1    No
  md026   no-trailing-punctuation         True       False      0.6.0    No
  md027   no-multiple-space-blockquote    True       False      0.5.2    Yes
  md028   no-blanks-blockquote            True       False      0.5.0    No
  md029   ol-prefix                       True       False      0.6.0    Yes
  md030   list-marker-space               True       False      0.6.0    Yes
  md031   blanks-around-fences            True       False      0.7.1    Yes
  md032   blanks-around-lists             True       False      0.5.1    No
  md033   no-inline-html                  True       False      0.6.0    No
  md034   no-bare-urls                    True       False      0.5.1    No
  md035   hr-style                        True       False      0.6.0    Yes
  md036   no-emphasis-as-heading, no-emp  True       False      0.6.0    No
          hasis-as-header
  md037   no-space-in-emphasis            True       False      0.5.2    Yes
  md038   no-space-in-code                True       False      0.5.1    Yes
  md039   no-space-in-links               True       False      0.5.2    Yes
  md040   fenced-code-language            True       False      0.5.0    No
  md041   first-line-heading, first-line  True       False      0.7.1    No
          -h1
  md042   no-empty-links                  True       False      0.5.0    No
  md043   required-headings, required-he  True       False      0.6.1    No
          aders
  md044   proper-names                    True       False      0.7.1    Yes
  md045   no-alt-text                     True       False      0.5.0    No
  md046   code-block-style                True       False      0.7.0    Yes
  md047   single-trailing-newline         True       False      0.5.2    Yes
  md048   code-fence-style                True       False      0.6.0    Yes
  pml100  disallowed-html                 False      False      0.6.0    No
  pml101  list-anchored-indent            False      False      0.6.0    No
  pml102  disallow-lazy-list-indentation  False      False      0.5.0    No
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_plugins_list_after_configuration_disable_all_rules(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that `plugins list` lists all plugins after disabling all rules.
    """

    # Arrange
    supplied_arguments = ["plugins", "list"]
    supplied_configuration = {"plugins": {"selectively_enable_rules": True}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = ["-c", configuration_file, "plugins", "list"]

        expected_results = ExpectedResults(
            return_code=0,
            expected_output="""
  ID      NAMES                           ENABLED    ENABLED    VERSION  FIX
                                          (DEFAULT)  (CURRENT)

  md001   heading-increment, header-incr  True       False      0.6.0    Yes
          ement
  md002   first-heading-h1, first-header  False      False      0.6.1    No
          -h1
  md003   heading-style, header-style     True       False      0.6.1    No
  md004   ul-style                        True       False      0.6.0    Yes
  md005   list-indent                     True       False      0.5.2    Yes
  md006   ul-start-left                   False      False      0.5.1    Yes
  md007   ul-indent                       True       False      0.6.1    Yes
  md009   no-trailing-spaces              True       False      0.6.1    Yes
  md010   no-hard-tabs                    True       False      0.6.1    Yes
  md011   no-reversed-links               True       False      0.5.1    No
  md012   no-multiple-blanks              True       False      0.7.0    Yes
  md013   line-length                     True       False      0.6.1    No
  md014   commands-show-output            True       False      0.5.0    No
  md018   no-missing-space-atx            True       False      0.5.1    No
  md019   no-multiple-space-atx           True       False      0.5.1    Yes
  md020   no-missing-space-closed-atx     True       False      0.5.1    No
  md021   no-multiple-space-closed-atx    True       False      0.5.1    Yes
  md022   blanks-around-headings, blanks  True       False      0.6.0    No
          -around-headers
  md023   heading-start-left, header-sta  True       False      0.5.3    Yes
          rt-left
  md024   no-duplicate-heading, no-dupli  True       False      0.6.1    No
          cate-header
  md025   single-title, single-h1         True       False      0.6.1    No
  md026   no-trailing-punctuation         True       False      0.6.0    No
  md027   no-multiple-space-blockquote    True       False      0.5.2    Yes
  md028   no-blanks-blockquote            True       False      0.5.0    No
  md029   ol-prefix                       True       False      0.6.0    Yes
  md030   list-marker-space               True       False      0.6.0    Yes
  md031   blanks-around-fences            True       False      0.7.1    Yes
  md032   blanks-around-lists             True       False      0.5.1    No
  md033   no-inline-html                  True       False      0.6.0    No
  md034   no-bare-urls                    True       False      0.5.1    No
  md035   hr-style                        True       False      0.6.0    Yes
  md036   no-emphasis-as-heading, no-emp  True       False      0.6.0    No
          hasis-as-header
  md037   no-space-in-emphasis            True       False      0.5.2    Yes
  md038   no-space-in-code                True       False      0.5.1    Yes
  md039   no-space-in-links               True       False      0.5.2    Yes
  md040   fenced-code-language            True       False      0.5.0    No
  md041   first-line-heading, first-line  True       False      0.7.1    No
          -h1
  md042   no-empty-links                  True       False      0.5.0    No
  md043   required-headings, required-he  True       False      0.6.1    No
          aders
  md044   proper-names                    True       False      0.7.1    Yes
  md045   no-alt-text                     True       False      0.5.0    No
  md046   code-block-style                True       False      0.7.0    Yes
  md047   single-trailing-newline         True       False      0.5.2    Yes
  md048   code-fence-style                True       False      0.6.0    Yes
  pml100  disallowed-html                 False      False      0.6.0    No
  pml101  list-anchored-indent            False      False      0.6.0    No
  pml102  disallow-lazy-list-indentation  False      False      0.5.0    No  
""",
        )

        # Act
        execute_results = scanner_default.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_plugins_list_after_command_line_disable_all_rules_and_enable_one(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that `plugins list` lists all plugins after disabling all rules.
    """

    # Arrange
    supplied_arguments = [
        "--disable-rules",
        "*",
        "--enable-rules",
        "md010",
        "plugins",
        "list",
    ]

    expected_results = ExpectedResults(
        return_code=0,
        expected_output="""
  ID      NAMES                           ENABLED    ENABLED    VERSION  FIX
                                          (DEFAULT)  (CURRENT)

  md001   heading-increment, header-incr  True       False      0.6.0    Yes
          ement
  md002   first-heading-h1, first-header  False      False      0.6.1    No
          -h1
  md003   heading-style, header-style     True       False      0.6.1    No
  md004   ul-style                        True       False      0.6.0    Yes
  md005   list-indent                     True       False      0.5.2    Yes
  md006   ul-start-left                   False      False      0.5.1    Yes
  md007   ul-indent                       True       False      0.6.1    Yes
  md009   no-trailing-spaces              True       False      0.6.1    Yes
  md010   no-hard-tabs                    True       True       0.6.1    Yes
  md011   no-reversed-links               True       False      0.5.1    No
  md012   no-multiple-blanks              True       False      0.7.0    Yes
  md013   line-length                     True       False      0.6.1    No
  md014   commands-show-output            True       False      0.5.0    No
  md018   no-missing-space-atx            True       False      0.5.1    No
  md019   no-multiple-space-atx           True       False      0.5.1    Yes
  md020   no-missing-space-closed-atx     True       False      0.5.1    No
  md021   no-multiple-space-closed-atx    True       False      0.5.1    Yes
  md022   blanks-around-headings, blanks  True       False      0.6.0    No
          -around-headers
  md023   heading-start-left, header-sta  True       False      0.5.3    Yes
          rt-left
  md024   no-duplicate-heading, no-dupli  True       False      0.6.1    No
          cate-header
  md025   single-title, single-h1         True       False      0.6.1    No
  md026   no-trailing-punctuation         True       False      0.6.0    No
  md027   no-multiple-space-blockquote    True       False      0.5.2    Yes
  md028   no-blanks-blockquote            True       False      0.5.0    No
  md029   ol-prefix                       True       False      0.6.0    Yes
  md030   list-marker-space               True       False      0.6.0    Yes
  md031   blanks-around-fences            True       False      0.7.1    Yes
  md032   blanks-around-lists             True       False      0.5.1    No
  md033   no-inline-html                  True       False      0.6.0    No
  md034   no-bare-urls                    True       False      0.5.1    No
  md035   hr-style                        True       False      0.6.0    Yes
  md036   no-emphasis-as-heading, no-emp  True       False      0.6.0    No
          hasis-as-header
  md037   no-space-in-emphasis            True       False      0.5.2    Yes
  md038   no-space-in-code                True       False      0.5.1    Yes
  md039   no-space-in-links               True       False      0.5.2    Yes
  md040   fenced-code-language            True       False      0.5.0    No
  md041   first-line-heading, first-line  True       False      0.7.1    No
          -h1
  md042   no-empty-links                  True       False      0.5.0    No
  md043   required-headings, required-he  True       False      0.6.1    No
          aders
  md044   proper-names                    True       False      0.7.1    Yes
  md045   no-alt-text                     True       False      0.5.0    No
  md046   code-block-style                True       False      0.7.0    Yes
  md047   single-trailing-newline         True       False      0.5.2    Yes
  md048   code-fence-style                True       False      0.6.0    Yes
  pml100  disallowed-html                 False      False      0.6.0    No
  pml101  list-anchored-indent            False      False      0.6.0    No
  pml102  disallow-lazy-list-indentation  False      False      0.5.0    No  
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_plugins_list_and_filter_by_id_ends_with_nine(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that `plugins list` lists all plugins with the specified id filter.
    """

    # Arrange
    supplied_arguments = ["plugins", "list", "md*9"]

    expected_results = ExpectedResults(
        return_code=0,
        expected_output="""
  ID     NAMES                  ENABLED    ENABLED    VERSION  FIX
                                (DEFAULT)  (CURRENT)

  md009  no-trailing-spaces     True       True       0.6.1    Yes
  md019  no-multiple-space-atx  True       True       0.5.1    Yes
  md029  ol-prefix              True       True       0.6.0    Yes
  md039  no-space-in-links      True       True       0.5.2    Yes

""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_plugins_list_and_filter_by_id_ends_with_non_sequence(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that `plugins list` lists all plugins with the specified id filter
        for a filter that returns no values.
    """

    # Arrange
    supplied_arguments = ["plugins", "list", "this-is-not-an-used-identifier"]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="No plugin rule identifiers matches the pattern 'this-is-not-an-used-identifier'.",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_plugins_list_and_filter_by_name_link(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that `plugins list` lists all plugins with the specified name filter.
    """

    # Arrange
    supplied_arguments = ["plugins", "list", "*header*"]

    expected_results = ExpectedResults(
        return_code=0,
        expected_output="""
  ID     NAMES                            ENABLED    ENABLED    VERSION  FIX
                                          (DEFAULT)  (CURRENT)

  md001  heading-increment, header-incre  True       True       0.6.0    Yes
         ment
  md002  first-heading-h1, first-header-  False      False      0.6.1    No
         h1
  md003  heading-style, header-style      True       True       0.6.1    No
  md022  blanks-around-headings, blanks-  True       True       0.6.0    No
         around-headers
  md023  heading-start-left, header-star  True       True       0.5.3    Yes
         t-left
  md024  no-duplicate-heading, no-duplic  True       True       0.6.1    No
         ate-header
  md036  no-emphasis-as-heading, no-emph  True       True       0.6.0    No
         asis-as-header
  md043  required-headings, required-hea  True       True       0.6.1    No
         ders
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_plugins_list_and_bad_filter(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that `plugins list` errors when provided an overly generic filter.
    """

    # Arrange
    supplied_arguments = ["plugins", "list", "*"]

    expected_results = ExpectedResults(
        return_code=2,
        expected_error="""usage: main.py plugins list [-h] [--all] [list_filter]
main.py plugins list: error: argument list_filter: Value '*' is not a valid pattern for an id or a name.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_results=expected_results,
    )


def test_markdown_with_plugins_info_and_bad_filter(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that `plugins list` errors when provided with a filter
        that is not a valid id or name.
    """

    # Arrange
    supplied_arguments = ["plugins", "info", "abc.def"]

    expected_results = ExpectedResults(
        return_code=2,
        expected_error="""usage: main.py plugins info [-h] info_filter
main.py plugins info: error: argument info_filter: Value 'abc.def' is not a valid id or name.
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_results=expected_results,
    )


def test_markdown_with_plugins_info_and_not_found_filter(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that `plugins list` errors when a valid id or name is not found.
    """

    # Arrange
    supplied_arguments = ["plugins", "info", "md00001"]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error="Unable to find a plugin with an id or name of 'md00001'.",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_results=expected_results,
    )


def test_markdown_with_plugins_info_and_found_filter(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that `plugins info` shows the proper information for the specified plugin.
    """

    # Arrange
    supplied_arguments = ["plugins", "info", "md001"]

    expected_results = ExpectedResults(
        return_code=0,
        expected_output="""
  ITEM               DESCRIPTION

  Id                 md001
  Name(s)            heading-increment,header-increment
  Short Description  Heading levels should only increment by one level at a ti
                     me.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md001.md


  CONFIGURATION ITEM  TYPE    VALUE

  front_matter_title  string  "title"

""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_plugins_info_and_found_filter_no_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that `plugins info` shows the proper information for the specified plugin
        that does not have any configuration.
    """

    # Arrange
    supplied_arguments = ["plugins", "info", "md023"]

    expected_results = ExpectedResults(
        return_code=0,
        expected_output="""  ITEM               DESCRIPTION

  Id                 md023
  Name(s)            heading-start-left,header-start-left
  Short Description  Headings must start at the beginning of the line.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md023.md
""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_plugins_info_and_found_filter_no_configuration_and_no_url(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that `plugins info` shows the proper information for the specified plugin
        that does not have any configuration or url.
    """

    # Arrange
    supplied_arguments = ["plugins", "info", "md999"]

    expected_results = ExpectedResults(
        return_code=0,
        expected_output="""MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1

  ITEM               DESCRIPTION

  Id                 md999
  Name(s)            debug-only
  Short Description  Debug plugin

""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_bad_query_config(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin has an exception during query_config.
    """

    # Arrange
    plugin_path = generate_path_to_bad_plugin("bad_query_config.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "plugins",
        "info",
        "mde007",
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output="""MDE007>>init_from_config
MDE007>>init_from_config""",
        expected_error="""
Unexpected Error(BadPluginError): Plugin id 'MDE007' had a critical failure during the '__handle_argparse_subparser_info' action.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_dash_add_plugin_with_v2_query_config(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure we get an error logged if a plugin has an old query_config.
    """

    # Arrange
    plugin_path = plugin_path = generate_path_to_bad_plugin("old_query_config.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "plugins",
        "info",
        "mde007",
    ]

    expected_results = ExpectedResults(
        return_code=0,
        expected_output="""MDE007>>init_from_config
MDE007>>init_from_config

  ITEM                 DESCRIPTION

  Id                   mde007
  Name(s)              bad-query-config
  Short Description    Test for a old query_config
  Configuration Items  something

""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_plugins_and_alternate_output() -> None:
    """
    Copy of test_md001_bad_improper_atx_heading_incrementing but with output
    redirected.
    """

    # Arrange
    scanner = MarkdownScanner(use_main=False, use_alternate_presentation=True)
    source_path, absolute_source_path = __generate_source_path(
        "improper_atx_heading_incrementing.md", "md001"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""[pso[[psf[{absolute_source_path}:3:1: MD001: Heading levels should only increment by one level at a time. [Expected: h2; Actual: h3] (heading-increment,header-increment)]]]]""",
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_detect_issue_report_in_fix_mode() -> None:
    """
    Make sure to test that the triggering of an issue in fix mode is an exception.
    """

    # Arrange
    scanner = MarkdownScanner(use_main=False, use_alternate_presentation=True)
    source_path, abs_source_path = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_next_line_fix.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "fix",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error=f"""[pse[[fse[BadPluginError encountered while scanning '{abs_source_path}':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.]]]]
""",
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_detect_issue_report_in_fix_mode_with_stack_trace() -> None:
    """
    Make sure to test that the triggering of an issue in fix mode is an exception.
    """

    # Arrange
    scanner = MarkdownScanner(use_main=False, use_alternate_presentation=True)
    source_path, abs_source_path = __generate_source_path("end_with_blank_line.md")
    plugin_path = generate_path_to_bad_plugin("bad_next_line_fix.py")
    supplied_arguments = [
        "--add-plugin",
        plugin_path,
        "--stack-trace",
        "fix",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_error=f"""[pse[[fse[BadPluginError encountered while scanning '{abs_source_path}':
(Line 1): Plugin id 'MDE003' had a critical failure during the 'next_line' action.
Actual Line: # This is a test
Caused by: BadPluginError:
   Plugin MDE003(bad-next-line) reported a triggered rule while in fix mode.]]]]
""",
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_normal_token_error(scanner_default: MarkdownScanner) -> None:
    """
    Test to ensure that we can normally cause tokens to be reported.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md", "md047")
    with copy_to_temp_file(source_path) as temp_source_path:
        plugin_path = generate_path_to_bad_plugin("bad_end_tokens.py")
        supplied_arguments = [
            "--add-plugin",
            plugin_path,
            "scan",
            temp_source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{temp_source_path}:0:0: MDE044: Plugin that triggers on end_tokens. (bad-end-tokens)
{temp_source_path}:0:0: MDE044: Plugin that triggers on end_tokens. (bad-end-tokens)
{temp_source_path}:0:0: MDE044: Plugin that triggers on end_tokens. (bad-end-tokens)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_normal_token_error_not_reported_with_fix(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to test a version of test_markdown_normal_token_error where fix is
    specified, hence the reporting of the rule violation should not occur.
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_blank_line.md", "md047")
    with copy_to_temp_file(source_path) as temp_source_path:
        plugin_path = generate_path_to_bad_plugin("bad_end_tokens.py")
        supplied_arguments = [
            "--add-plugin",
            plugin_path,
            "fix",
            temp_source_path,
        ]

        expected_results = ExpectedResults()

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_fixed_issue_with_debug_on(scanner_default: MarkdownScanner) -> None:
    """
    Test to test

    shadow of test_md047_bad_end_with_no_blank_line_fix_and_debug
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_no_blank_line.md", "md047")
    with copy_to_temp_file(source_path) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md009,md011,md013",
            "-x-fix-debug",
            "fix",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"""md010-before:# This is a test:
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
Fixed: {temp_source_path}"""
        expected_error = ""
        expected_file_contents = read_contents_of_text_file(temp_source_path) + "\n"

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


def test_markdown_fixed_issue_line_with_debug_and_file_debug_on(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to test that file debug provides additional data.
    Note that because of temporary files, the std out comparison is
    fairly involved.

    shadow of test_md047_bad_end_with_no_blank_line_fix_and_debug
    """

    # Arrange
    source_path, _ = __generate_source_path("end_with_no_blank_line.md", "md047")
    with copy_to_temp_file(source_path) as temp_source_path:
        supplied_arguments = [
            "--disable-rules",
            "md009,md011,md013",
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
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

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


def test_markdown_fixed_issue_token_with_debug_and_file_debug_on(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to test that file debug provides additional data.
    Note that because of temporary files, the std out comparison is
    fairly involved.

    shadow of test_md001_bad_improper_atx_heading_incrementing
    """

    # Arrange
    source_path, _ = __generate_source_path(
        "improper_atx_heading_incrementing.md", "md001"
    )
    with copy_to_temp_file(source_path) as temp_source_path:
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
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

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


def test_markdown_plugins_wanting_to_fix_same_token(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that
    """

    # Arrange
    plugin_path = generate_path_to_bad_plugin("bad_fix_atx_token_like_md001.py")

    source_path, _ = __generate_source_path(
        "improper_atx_heading_incrementing.md", "md001"
    )
    with copy_to_temp_file(source_path) as temp_source_path:
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

        expected_results = ExpectedResults(
            return_code=1,
            expected_error=f"""BadPluginFixError encountered while scanning '{temp_source_path}':
Multiple plugins (MDE003 and MD001) have requested a fix for the same field of the same token.""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_plugins_wanting_to_fix_and_replace_same_token(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that
    """

    # Arrange
    plugin_path = generate_path_to_bad_plugin("bad_fix_indented_token_like_md046.py")

    original_file_contents = """~~~Markdown
# fred
~~~
"""
    with create_temporary_markdown_file(original_file_contents) as temp_source_path:

        supplied_arguments = [
            "--set",
            "plugins.md046.style=indented",
            "--add-plugin",
            plugin_path,
            "fix",
            temp_source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_error="""BadPluginFixError encountered while scanning '{path}':
Multiple plugins (MDE003 and MD046) are in conflict about fixing the token.""".replace(
                "{path}", temp_source_path
            ),
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_plugins_wanting_to_replace_same_token(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that
    """

    # Arrange
    plugin_path = generate_path_to_bad_plugin(
        "bad_replace_indented_token_like_md046.py",
    )

    original_file_contents = """~~~Markdown
# fred
~~~

    # fred
"""
    with create_temporary_markdown_file(original_file_contents) as temp_source_path:
        supplied_arguments = [
            "--add-plugin",
            plugin_path,
            "fix",
            temp_source_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_error="""BadPluginFixError encountered while scanning '{path}':
Multiple plugins (MDE003 and MD046) are in conflict about replacing the token.""".replace(
                "{path}", temp_source_path
            ),
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_plugins_wanting_to_fix_unknown_token_stack_trace(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure the rule does trigger with a document with
    only Atx Headings, that when they increase, only increase by 2.
    """

    # Arrange
    plugin_path = generate_path_to_bad_plugin("bad_fix_token_unsupported.py")

    source_path, _ = __generate_source_path(
        "improper_atx_heading_incrementing.md", "md001"
    )
    with copy_to_temp_file(source_path) as temp_source_path:
        supplied_arguments = [
            "--stack-trace",
            "--add-plugin",
            plugin_path,
            "fix",
            temp_source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = f"""

BadPluginFixError encountered while scanning '{temp_source_path}':
Plugin id 'MDE003's 'next_token' action requested a token adjustment to field 'hash_count' that failed.
Traceback (most recent call last):
"""

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output,
            expected_error,
            expected_return_code,
            additional_error=["raise BadPluginFixError( "],
        )
