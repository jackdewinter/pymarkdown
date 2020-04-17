"""
Module to provide tests related to the plugin manager for the scanner.
"""
from test.markdown_scanner import MarkdownScanner


def test_markdown_with_dash_dash_add_plugin_and_bad_path():
    """
    Test to make sure we get enable a rule if '--add-plugin' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "--add-plugin",
        "MD047",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = "Plugin path 'MD047' does not exist.\n"

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/plugin_two.py",
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
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/",
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
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/not-a-python-file.txt",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError: Plugin file named 'not-a-python-file.txt' "
        + "cannot be loaded.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/misnamed.py",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError: Plugin file named 'misnamed.py' "
        + "does not contain a class named 'Misnamed'.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_starting_new_file.py",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning 'test/resources/rules/md047/end_with_blank_line.md':
Plugin id 'MDE001' had a critical failure during the 'starting_new_file' action.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_completed_file.py",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning 'test/resources/rules/md047/end_with_blank_line.md':
Plugin id 'MDE002' had a critical failure during the 'completed_file' action.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_next_line.py",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning 'test/resources/rules/md047/end_with_blank_line.md':
Plugin id 'MDE003' had a critical failure during the 'next_line' action.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "--stack-trace",
        "--add-plugin",
        "test/resources/plugins/bad/bad_next_line.py",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while scanning 'test/resources/rules/md047/end_with_blank_line.md':
Plugin id 'MDE003' had a critical failure during the 'next_line' action.
Traceback (most recent call last):
"""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    ) from this_exception
pymarkdown.plugin_manager.BadPluginError: Plugin id 'MDE003' had a critical failure during the 'next_line' action.
""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_constructor():
    """
    Test to make sure we get an error logged if a plugin throws an exception within the constructor function.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_constructor.py",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError: Plugin file named 'bad_constructor.py' threw an exception "
        + "in the constructor for the class 'BadConstructor'.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_details.py",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin class 'BadDetails' had a critical failure loading the plugin details.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "--stack-trace",
        "--add-plugin",
        "test/resources/plugins/bad/bad_details.py",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin class 'BadDetails' had a critical failure loading the plugin details.
Traceback (most recent call last):
"""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output,
        expected_error,
        expected_return_code,
        additional_error=[
            """    raise Exception("bad details")
Exception: bad details

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
""",
            """    raise BadPluginError(class_name=type(plugin_instance).__name__,)
pymarkdown.plugin_manager.BadPluginError: Plugin class 'BadDetails' had a critical failure loading the plugin details.""",
        ],
    )


def test_markdown_with_dash_dash_add_plugin_with_bad_string_detail():
    """
    Test to make sure we get an error logged if a plugin throws an exception that a string detail is bad.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_string_detail_is_int.py",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin class 'BadStringDetailIsInt' returned an improperly typed value for field name 'plugin_description'.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_add_plugin_with_empty_string_detail():
    """
    Test to make sure we get an error logged if a plugin throws an exception that a string detail is empty.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_string_detail_is_empty.py",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin class 'BadStringDetailIsEmpty' returned an empty value for field name 'plugin_description'.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "--add-plugin",
        "test/resources/plugins/bad/bad_boolean_detail_is_int.py",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadPluginError encountered while loading plugins:
Plugin class 'BadBooleanDetailIsInt' returned an improperly typed value for field name 'plugin_enabled_by_default'.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
