"""
Module to provide tests related to the plugin manager for the scanner.
"""
from test.markdown_scanner import MarkdownScanner


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
    info       information of specific plugins

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
        "test/resources/plugins/bad/plugin_three.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """ValueError encountered while initializing plugins:
Unable to register plugin 'plugin_three.py' with id 'md999' as plugin 'plugin_one.py' is already registered with that id."""

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
        "test/resources/plugins/bad/plugin_five.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """ValueError encountered while initializing plugins:
Unable to register plugin 'plugin_five.py' with id 'debug-only' as id is not a valid id in the form 'aannn' or 'aaannn'."""

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
        "test/resources/plugins/bad/plugin_four.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """ValueError encountered while initializing plugins:
Unable to register plugin 'plugin_four.py' with name 'debug-only' as plugin 'plugin_one.py' is already registered with that name."""

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
        "test/resources/plugins/bad/plugin_six.py",
        "scan",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """ValueError encountered while initializing plugins:
Unable to register plugin 'plugin_six.py' with name 'debug.only' as name is not a valid name in the form 'an-an'."""

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
Plugin id 'MDE003' had a critical failure during the 'next_line' action.
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
Plugin id 'MDE003' had a critical failure during the 'next_line' action.
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


def test_markdown_with_plugins_list_only():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["plugins", "list"]

    expected_return_code = 0
    expected_output = """
  ID     NAMES                            ENABLED (DEFAULT)  ENABLED (CURRENT)

  md001  heading-increment, header-incre  True               True
         ment
  md002  first-heading-h1, first-header-  False              False
         h1
  md003  heading-style, header-style      True               True
  md004  ul-style                         False              False
  md005  list-indent                      False              False
  md006  ul-start-left                    False              False
  md007  ul-indent                        False              False
  md009  no-trailing-spaces               False              False
  md010  no-hard-tabs                     False              False
  md011  no-reversed-links                False              False
  md012  no-multiple-blanks               False              False
  md013  line-length                      False              False
  md014  commands-show-output             False              False
  md018  no-missing-space-atx             True               True
  md019  no-multiple-space-atx            True               True
  md020  no-missing-space-closed-atx      True               True
  md021  no-multiple-space-closed-atx     True               True
  md022  blanks-around-headings, blanks-  True               True
         around-headers
  md023  heading-start-left, header-star  True               True
         t-left
  md024  no-duplicate-heading, no-duplic  True               True
         ate-header
  md025  single-title, single-h1          False              False
  md026  no-trailing-punctuation          True               True
  md027  no-multiple-space-blockquote     False              False
  md028  no-blanks-blockquote             False              False
  md029  ol-prefix                        False              False
  md030  list-marker-space                False              False
  md031  blanks-around-fences             False              False
  md032  blanks-around-lists              False              False
  md033  no-inline-html                   False              False
  md034  no-bare-urls                     False              False
  md035  hr-style                         False              False
  md036  no-emphasis-as-heading, no-emph  True               True
         asis-as-header
  md037  no-space-in-emphasis             False              False
  md038  no-space-in-code                 False              False
  md039  no-space-in-links                False              False
  md040  fenced-code-language             False              False
  md041  first-line-heading, first-line-  False              False
         h1
  md042  no-empty-links                   False              False
  md043  required-headings, required-hea  False              False
         ders
  md044  proper-names                     False              False
  md045  no-alt-text                      False              False
  md046  code-block-style                 False              False
  md047  single-trailing-newline          True               True
  md048  code-fence-style                 False              False

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
  ID     NAMES                  ENABLED (DEFAULT)  ENABLED (CURRENT)

  md009  no-trailing-spaces     False              False
  md019  no-multiple-space-atx  True               True
  md029  ol-prefix              False              False
  md039  no-space-in-links      False              False

"""
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
    supplied_arguments = ["plugins", "list", "*link*"]

    expected_return_code = 0
    expected_output = """
  ID     NAMES              ENABLED (DEFAULT)  ENABLED (CURRENT)

  md011  no-reversed-links  False              False
  md039  no-space-in-links  False              False
  md042  no-empty-links     False              False

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
    expected_error = """usage: main.py plugins list [-h] [list_filter]
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
    expected_output = """Id:md001
Name(s):heading-increment,header-increment
Description:Heading levels should only increment by one level at a time"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
