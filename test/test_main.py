"""
Module to provide tests related to the basic parts of the scanner.
"""
import logging
import os
import tempfile
from test.markdown_scanner import MarkdownScanner

from pymarkdown.parser_logger import ParserLogger

from .utils import write_temporary_configuration

POGGER = ParserLogger(logging.getLogger(__name__))


def test_markdown_with_no_parameters():
    """
    Test to make sure we get the simple information if no parameters are supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = []

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py [-h] [--version] [-l] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--stack-trace]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE]
               path [path ...]
main.py: error: the following arguments are required: path
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_h():
    """
    Test to make sure we get help if '-h' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["-h"]

    expected_return_code = 0
    expected_output = """usage: main.py [-h] [--version] [-l] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--stack-trace]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE]
               path [path ...]

Lint any found Markdown files.

positional arguments:
  path                  One or more paths to scan for eligible files

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -l, --list-files      list the markdown files found and exit
  -e ENABLE_RULES, --enable-rules ENABLE_RULES
                        comma separated list of rules to enable
  -d DISABLE_RULES, --disable-rules DISABLE_RULES
                        comma separated list of rules to disable
  --add-plugin ADD_PLUGIN
                        path to a plugin containing a new rule to apply
  --config CONFIGURATION_FILE, -c CONFIGURATION_FILE
                        path to a configuration file
  --stack-trace         if an error occurs, print out the stack trace for
                        debug purposes
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        minimum level for any log messages
  --log-file LOG_FILE   destination file for log messages
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_version():
    """
    Test to make sure we get help if '--version' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["--version"]

    expected_return_code = 0
    expected_output = """main.py 0.1.0
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_e_single_by_name():
    """
    Test to make sure we get enable a rule if '-e' is supplied and the name of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "-e",
        "debug-only",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 0
    expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx:::False]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>completed_file
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_e_single_by_id():
    """
    Test to make sure we get enable a rule if '-e' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "-e",
        "MD999",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 0
    expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx:::False]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>completed_file
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_d_single_by_name():
    """
    Test to make sure we get enable a rule if '-d' is supplied and the name of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    fails normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "-d",
        "single-trailing-newline",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_d_single_by_id():
    """
    Test to make sure we get enable a rule if '-d' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    fails normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "-d",
        "MD047",
        "test/resources/rules/md047/end_with_no_blank_line.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_x_scan():
    """
    Test to make sure we get simulate a test scan exception if the `-x-scan` flag
    is set.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "-x-scan",
        "test/resources/rules/md047/end_with_no_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadTokenizationError encountered while scanning 'test/resources/rules/md047/end_with_no_blank_line.md':
An unhandled error occurred processing the document.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_dash_log_level_debug(caplog):
    """
    Test to make sure we get the right effect if the `--log-level` flag
    is set for debug.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--log-level",
        "DEBUG",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = """"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

    # Info messages
    assert "Number of files found: " in caplog.text
    assert (
        "Determining files to scan for path "
        + "'test/resources/rules/md047/end_with_blank_line.md'."
        in caplog.text
    )

    # Debug messages
    assert (
        "Provided path 'test/resources/rules/md047/end_with_blank_line.md' "
        + "is a valid file. Adding."
        in caplog.text
    )


def test_markdown_with_dash_dash_log_level_info(caplog):
    """
    Test to make sure we get the right effect if the `--log-level` flag
    is set for info.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--log-level",
        "INFO",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

    # Info messages
    assert "Number of files found: " in caplog.text
    assert (
        "Determining files to scan for path "
        + "'test/resources/rules/md047/end_with_blank_line.md'."
        in caplog.text
    )

    # Debug messages
    assert (
        "Provided path 'test/resources/rules/md047/end_with_blank_line.md' "
        + "is a valid file. Adding."
        not in caplog.text
    )


def test_markdown_with_dash_dash_log_level_invalid(caplog):
    """
    Test to make sure we get the right effect if the `--log-level` flag
    is set for an invalid log level.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--log-level",
        "invalid",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py [-h] [--version] [-l] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--stack-trace]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE]
               path [path ...]
main.py: error: argument --log-level: invalid log_level_type value: 'invalid'
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

    # Info messages
    assert "Number of scanned files found: " not in caplog.text
    assert (
        "Determining files to scan for path "
        + "'test/resources/rules/md047/end_with_blank_line.md'."
        not in caplog.text
    )

    # Debug messages
    assert (
        "Provided path 'test/resources/rules/md047/end_with_blank_line.md' "
        + "is a valid Markdown file. Adding."
        not in caplog.text
    )


def test_markdown_with_dash_dash_log_level_info_with_file():
    """
    Test to make sure we get the right effect if the `--log-level` flag
    is set for info with the results going to a file.
    """

    # Arrange
    temp_file = None
    try:
        temp_file = tempfile.NamedTemporaryFile()
        log_file_name = temp_file.name
    finally:
        if temp_file:
            temp_file.close()

    try:
        scanner = MarkdownScanner()
        supplied_arguments = [
            "--log-level",
            "INFO",
            "--log-file",
            log_file_name,
            "test/resources/rules/md047/end_with_blank_line.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )

        with open(log_file_name) as file:
            file_data = file.read().replace("\n", "")

        # Info messages
        assert "Number of files found: " in file_data
        assert (
            "Determining files to scan for path "
            + "'test/resources/rules/md047/end_with_blank_line.md'."
            in file_data
        )

        # Debug messages
        assert (
            "Provided path 'test/resources/rules/md047/end_with_blank_line.md' "
            + "is a valid file. Adding."
            not in file_data
        )
    finally:
        if os.path.exists(log_file_name):
            os.remove(log_file_name)


def test_markdown_with_dash_x_init():
    """
    Test to make sure we get simulate a test initialization exception if the
    `-x-init` flag is set.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "-x-init",
        "test/resources/rules/md047/end_with_no_blank_line.md",
    ]
    fake_directory = "fredo"
    abs_fake_directory = os.path.abspath(fake_directory).replace("\\", "\\\\")

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadTokenizationError encountered while initializing tokenizer:\n"
        + "Named character entity map file '"
        + fake_directory
        + "\\entities.json' was not loaded "
        + "([Errno 2] No such file or directory: '"
        + abs_fake_directory
        + "\\\\entities.json').\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_e_single_by_id_and_good_config():
    """
    Test to make sure we get enable a rule if '-e' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD999": {"test_value": 2}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "test/resources/rules/md047/end_with_blank_line.md",
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>2
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx:::False]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>completed_file
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


def test_markdown_with_dash_e_single_by_id_and_bad_config():
    """
    Test to make sure we get enable a rule if '-e' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD999": {"test_value": "fred"}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "test/resources/rules/md047/end_with_blank_line.md",
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx:::False]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>completed_file
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


def test_markdown_with_dash_e_single_by_id_and_non_json_config_file():
    """
    Test to make sure we get an error if we provide a configuration file that is
    not in a json format.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = "not a json file"
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "test/resources/rules/md047/end_with_blank_line.md",
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = (
            "Specified configuration file '"
            + configuration_file
            + "' is not a valid JSON file (Expecting value: line 1 column 1 (char 0)).\n"
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_dash_e_single_by_id_and_non_present_config_file():
    """
    Test to make sure we get an error if we provide a configuration file that is
    not in a json format.
    """

    # Arrange
    scanner = MarkdownScanner()
    configuration_file = "not-exists"
    assert not os.path.exists(configuration_file)
    supplied_arguments = [
        "-e",
        "MD999",
        "-c",
        configuration_file,
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "Specified configuration file 'not-exists' was not loaded "
        + "([Errno 2] No such file or directory: 'not-exists').\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_e_single_by_id_and_good_select_config():
    """
    Test to make sure we get enable a rule if '-e' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD999": {"other_test_value": 2}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "test/resources/rules/md047/end_with_blank_line.md",
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>2
MD999>>starting_new_file>>
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx:::False]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>completed_file
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


def test_markdown_with_dash_e_single_by_id_and_bad_select_config():
    """
    Test to make sure we get enable a rule if '-e' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD999": {"other_test_value": 9}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "test/resources/rules/md047/end_with_blank_line.md",
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx:::False]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>completed_file
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


def test_markdown_with_dash_e_single_by_id_and_config_causing_config_exception():
    """
    Test to make sure if we tell the test plugin to throw an exception during the
    call to `initialize_from_config`, that it is handled properly.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD999": {"test_value": 10}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "test/resources/rules/md047/end_with_blank_line.md",
        ]

        expected_return_code = 1
        expected_output = """MD999>>init_from_config
MD999>>test_value>>10
MD999>>other_test_value>>1
"""
        expected_error = """BadPluginError encountered while configuring plugins:
Plugin id 'MD999' had a critical failure during the 'apply_configuration' action.
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


def test_markdown_with_dash_e_single_by_id_and_config_causing_next_token_exception():
    """
    Test to make sure if we tell the test plugin to throw an exception during the
    call to `next_token`, that it is handled properly.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD999": {"test_value": 20}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "test/resources/rules/md047/end_with_blank_line.md",
        ]

        expected_return_code = 1
        expected_output = """MD999>>init_from_config
MD999>>test_value>>20
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>token:[atx(1,1):1:0:]
"""
        expected_error = """BadPluginError encountered while scanning 'test/resources/rules/md047/end_with_blank_line.md':
Plugin id 'MD999' had a critical failure during the 'next_token' action.
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


# TODO add Markdown parsing of some binary file to cause the tokenizer to throw an exception?


# pylint: disable=broad-except
def test_markdown_logger_arg_list_out_of_sync():
    """
    Test to verify that if we don't have the same number of
    $ characters in the string as arguments in the list, an
    exception with be thrown.
    """

    # Arrange
    try:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        assert POGGER.is_enabled_for(logging.DEBUG)
        POGGER.debug("one sub $ but two in list", 1, 2)
        assert False, "An exception should have been thrown by now."
    except Exception as this_exception:
        assert (
            str(this_exception)
            == "The number of $ substitution characters does not equal the number of arguments in the list."
        )


# pylint: enable=broad-except
