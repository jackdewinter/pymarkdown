"""
Module to provide tests related to the extension manager for the scanner.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.utils import write_temporary_configuration

# pylint: disable=too-many-lines


def test_markdown_with_extensions_only():
    """
    Test to make sure the command line interface to extensions
    only shows the extensions help related information.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "extensions",
    ]

    expected_return_code = 2
    expected_output = """usage: main.py extensions [-h] {list,info} ...

positional arguments:
  {list,info}
    list       list the available extensions
    info       information on a specific extension

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


def test_markdown_with_extensions_list_only():
    """
    Test to make sure the command line interface to extensions
    only shows the installed extensions when asked for a list.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["extensions", "list"]

    expected_return_code = 0
    expected_output = """
  ID                     NAME                   ENABLED    ENABLED    VERSION
                                                (DEFAULT)  (CURRENT)

  front-matter           Front Matter Metadata  False      False      0.5.0
  linter-pragmas         Pragma Linter Instruc  True       True       0.5.0
                         tions
  markdown-disallow-raw  Markdown Disallow Raw  False      False      0.5.0
  -html                   HTML
  markdown-extended-aut  Markdown Extended Aut  False      False      0.5.0
  olinks                 olinks
  markdown-strikethroug  Markdown Strikethroug  False      False      0.5.0
  h                      h
  markdown-task-list-it  Markdown Task List It  False      False      0.5.0
  ems                    ems
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_extensions_list_only_all():
    """
    Test to make sure the command line interface to extensions
    only shows the installed extensions when asked for a list.
    With the -all flag.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["extensions", "list", "--all"]

    expected_return_code = 0
    expected_output = """
  ID                     NAME                   ENABLED    ENABLED    VERSION
                                                (DEFAULT)  (CURRENT)

  front-matter           Front Matter Metadata  False      False      0.5.0
  linter-pragmas         Pragma Linter Instruc  True       True       0.5.0
                         tions
  markdown-disallow-raw  Markdown Disallow Raw  False      False      0.5.0
  -html                   HTML
  markdown-extended-aut  Markdown Extended Aut  False      False      0.5.0
  olinks                 olinks
  markdown-strikethroug  Markdown Strikethroug  False      False      0.5.0
  h                      h
  markdown-tables        Markdown Tables        False      False      0.0.0
  markdown-task-list-it  Markdown Task List It  False      False      0.5.0
  ems                    ems
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_extensions_list_and_filter_by_id_ends_with_r():
    """
    Test to make sure the command line interface to extensions
    only shows the installed extensions when asked for a list.
    With a globbed name.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["extensions", "list", "f*r"]

    expected_return_code = 0
    expected_output = """
  ID            NAME                   ENABLED    ENABLED    VERSION
                                       (DEFAULT)  (CURRENT)

  front-matter  Front Matter Metadata  False      False      0.5.0

"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_extensions_list_and_filter_by_id_ends_with_r_and_configuration_true():
    """
    Test to make sure the command line interface to extensions
    only shows the installed extensions when asked for a list.
    With globbed name and enabled extension.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"extensions": {"front-matter": {"enabled": True}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = ["-c", configuration_file, "extensions", "list", "f*r"]

        expected_return_code = 0
        expected_output = """
  ID            NAME                   ENABLED    ENABLED    VERSION
                                       (DEFAULT)  (CURRENT)

  front-matter  Front Matter Metadata  False      True       0.5.0

"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_extensions_list_and_filter_by_id_ends_with_r_and_configuration_false():
    """
    Test to make sure the command line interface to extensions
    only shows the installed extensions when asked for a list.
    With globbed and disabled extension.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"extensions": {"front-matter": {"enabled": False}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = ["-c", configuration_file, "extensions", "list", "f*r"]

        expected_return_code = 0
        expected_output = """
  ID            NAME                   ENABLED    ENABLED    VERSION
                                       (DEFAULT)  (CURRENT)

  front-matter  Front Matter Metadata  False      False      0.5.0

"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_extensions_error_during_configuration():
    """
    Test to make sure the command line interface to extensions
    shows the exception text when the initialization fails due
    to an exception.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {
        "extensions": {"debug-extension": {"enabled": True, "debug_mode": 1}}
    }
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "--log-level",
            "DEBUG",
            "-c",
            configuration_file,
            "extensions",
            "list",
            "f*r",
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = """Error ExceptionTestException encountered while initializing extensions:
blah
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


def test_markdown_with_extensions_value_error_during_configuration():
    """
    Test to make sure the command line interface to extensions
    shows the exception text when the configuration fails due
    to an exception.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {
        "extensions": {"debug-extension": {"enabled": True, "debug_mode": 2}}
    }
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = ["-c", configuration_file, "extensions", "list", "f*r"]

        expected_return_code = 1
        expected_output = ""
        expected_error = """Configuration error ValueError encountered while initializing extensions:
blah
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


def test_markdown_with_extensions_and_no_error_during_configuration():
    """
    Test to make sure the command line interface to extensions
    list the exception text when the initialization does not fail.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {
        "extensions": {"debug-extension": {"enabled": True, "debug_mode": 0}}
    }
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = ["-c", configuration_file, "extensions", "list", "f*r"]

        expected_return_code = 0
        expected_output = """
  ID            NAME                   ENABLED    ENABLED    VERSION
                                       (DEFAULT)  (CURRENT)

  front-matter  Front Matter Metadata  False      False      0.5.0

"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_extensions_list_and_filter_by_id_ends_with_non_sequence():
    """
    Test to make sure the command line interface to extensions
    lists the matching items (none) when presented with an identifier
    that does not match any extension.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["extensions", "list", "this-is-not-an-used-identifier"]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "No extension identifier matches the pattern 'this-is-not-an-used-identifier'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_extensions_list_and_filter_by_name_link():
    """
    Test to make sure the command line interface to extensions
    lists the matching items when presented with an identifier
    surrounded by wildcards that matches.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["extensions", "list", "*front*"]

    expected_return_code = 0
    expected_output = """
  ID            NAME                   ENABLED    ENABLED    VERSION
                                       (DEFAULT)  (CURRENT)

  front-matter  Front Matter Metadata  False      False      0.5.0

"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_extensions_list_and_bad_filter():
    """
    Test to make sure the command line interface to extensions
    lists presents an error when a bad filter is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["extensions", "list", "*"]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py extensions list [-h] [--all] [list_filter]
main.py extensions list: error: argument list_filter: Value '*' is not a valid pattern for an id.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_extensions_info_and_bad_filter():
    """
    Test to make sure the command line interface to extensions
    lists presents an error when a bad filter is supplied with
    no wildcards.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["extensions", "info", "abc.def"]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py extensions info [-h] info_filter
main.py extensions info: error: argument info_filter: Value 'abc.def' is not a valid id.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_extensions_info_and_not_found_filter():
    """
    Test to make sure the command line interface to extensions
    info presents an error when a bad id is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["extensions", "info", "md00001"]

    expected_return_code = 1
    expected_output = ""
    expected_error = "Unable to find an extension with an id of 'md00001'."

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_extensions_info_and_found_filter():
    """
    Test to make sure the command line interface to extensions
    info presents information when a valid id is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["extensions", "info", "front-matter"]

    expected_return_code = 0
    expected_output = """  ITEM               DESCRIPTION

  Id                 front-matter
  Name               Front Matter Metadata
  Short Description  Allows metadata to be parsed from document front matter.
  Description Url    https://github.com/jackdewinter/pymarkdown/blob/main/docs
                     /extensions/front-matter.md
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
