"""
Module to provide tests related to the basic parts of the scanner.
"""
import logging
import os
import runpy
import tempfile
from test.markdown_scanner import MarkdownScanner

from pymarkdown.container_block_processor import ContainerIndices
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.stack_token import StackToken

from .utils import write_temporary_configuration

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


def test_markdown_with_no_parameters():
    """
    Test to make sure we get the simple information if no parameters are supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = []

    expected_return_code = 2
    expected_output = """usage: main.py [-h] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--set SET_CONFIGURATION] [--strict-config] [--stack-trace]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE]
               {plugins,extensions,scan,scan-stdin,version} ...

Lint any found Markdown files.

positional arguments:
  {plugins,extensions,scan,scan-stdin,version}
    plugins             plugin commands
    extensions          extension commands
    scan                scan the Markdown files in the specified paths
    scan-stdin          scan the standard input as a Markdown file
    version             version of the application

optional arguments:
  -h, --help            show this help message and exit
  -e ENABLE_RULES, --enable-rules ENABLE_RULES
                        comma separated list of rules to enable
  -d DISABLE_RULES, --disable-rules DISABLE_RULES
                        comma separated list of rules to disable
  --add-plugin ADD_PLUGIN
                        path to a plugin containing a new rule to apply
  --config CONFIGURATION_FILE, -c CONFIGURATION_FILE
                        path to the configuration file to use
  --set SET_CONFIGURATION, -s SET_CONFIGURATION
                        manually set an individual configuration property
  --strict-config       throw an error if configuration is bad, instead of
                        assuming default
  --stack-trace         if an error occurs, print out the stack trace for
                        debug purposes
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        minimum level required to log messages
  --log-file LOG_FILE   destination file for log messages
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_no_parameters_through_module():
    """
    Test to make sure we get the simple information if no parameters are supplied,
    but through the module interface.
    """

    # Arrange
    scanner = MarkdownScanner(use_module=True)
    supplied_arguments = []

    expected_return_code = 2
    expected_output = """usage: __main.py__ [-h] [-e ENABLE_RULES] [-d DISABLE_RULES]
                   [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
                   [--set SET_CONFIGURATION] [--strict-config] [--stack-trace]
                   [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
                   [--log-file LOG_FILE]
                   {plugins,extensions,scan,scan-stdin,version} ...

Lint any found Markdown files.

positional arguments:
  {plugins,extensions,scan,scan-stdin,version}
    plugins             plugin commands
    extensions          extension commands
    scan                scan the Markdown files in the specified paths
    scan-stdin          scan the standard input as a Markdown file
    version             version of the application

optional arguments:
  -h, --help            show this help message and exit
  -e ENABLE_RULES, --enable-rules ENABLE_RULES
                        comma separated list of rules to enable
  -d DISABLE_RULES, --disable-rules DISABLE_RULES
                        comma separated list of rules to disable
  --add-plugin ADD_PLUGIN
                        path to a plugin containing a new rule to apply
  --config CONFIGURATION_FILE, -c CONFIGURATION_FILE
                        path to the configuration file to use
  --set SET_CONFIGURATION, -s SET_CONFIGURATION
                        manually set an individual configuration property
  --strict-config       throw an error if configuration is bad, instead of
                        assuming default
  --stack-trace         if an error occurs, print out the stack trace for
                        debug purposes
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        minimum level required to log messages
  --log-file LOG_FILE   destination file for log messages
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_no_parameters_through_main():
    """
    Test to make sure we get the simple information if no parameters are supplied,
    but through the main interface.
    """

    # Arrange
    scanner = MarkdownScanner(use_main=True)
    supplied_arguments = []

    expected_return_code = 2
    expected_output = """usage: main.py [-h] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--set SET_CONFIGURATION] [--strict-config] [--stack-trace]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE]
               {plugins,extensions,scan,scan-stdin,version} ...

Lint any found Markdown files.

positional arguments:
  {plugins,extensions,scan,scan-stdin,version}
    plugins             plugin commands
    extensions          extension commands
    scan                scan the Markdown files in the specified paths
    scan-stdin          scan the standard input as a Markdown file
    version             version of the application

optional arguments:
  -h, --help            show this help message and exit
  -e ENABLE_RULES, --enable-rules ENABLE_RULES
                        comma separated list of rules to enable
  -d DISABLE_RULES, --disable-rules DISABLE_RULES
                        comma separated list of rules to disable
  --add-plugin ADD_PLUGIN
                        path to a plugin containing a new rule to apply
  --config CONFIGURATION_FILE, -c CONFIGURATION_FILE
                        path to the configuration file to use
  --set SET_CONFIGURATION, -s SET_CONFIGURATION
                        manually set an individual configuration property
  --strict-config       throw an error if configuration is bad, instead of
                        assuming default
  --stack-trace         if an error occurs, print out the stack trace for
                        debug purposes
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        minimum level required to log messages
  --log-file LOG_FILE   destination file for log messages
"""
    expected_error = ""

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
    expected_output = """usage: main.py [-h] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--set SET_CONFIGURATION] [--strict-config] [--stack-trace]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE]
               {plugins,extensions,scan,scan-stdin,version} ...

Lint any found Markdown files.

positional arguments:
  {plugins,extensions,scan,scan-stdin,version}
    plugins             plugin commands
    extensions          extension commands
    scan                scan the Markdown files in the specified paths
    scan-stdin          scan the standard input as a Markdown file
    version             version of the application

optional arguments:
  -h, --help            show this help message and exit
  -e ENABLE_RULES, --enable-rules ENABLE_RULES
                        comma separated list of rules to enable
  -d DISABLE_RULES, --disable-rules DISABLE_RULES
                        comma separated list of rules to disable
  --add-plugin ADD_PLUGIN
                        path to a plugin containing a new rule to apply
  --config CONFIGURATION_FILE, -c CONFIGURATION_FILE
                        path to the configuration file to use
  --set SET_CONFIGURATION, -s SET_CONFIGURATION
                        manually set an individual configuration property
  --strict-config       throw an error if configuration is bad, instead of
                        assuming default
  --stack-trace         if an error occurs, print out the stack trace for
                        debug purposes
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        minimum level required to log messages
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
    Test to make sure we get help if 'version' is supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["version"]

    version_path = os.path.join(".", "pymarkdown", "version.py")
    version_meta = runpy.run_path(version_path)
    semantic_version = version_meta["__version__"]

    expected_return_code = 0
    expected_output = """{version}
""".replace(
        "{version}", semantic_version
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_direct_args(caplog):
    """
    Test to make sure we can specify the arguments directly.
    """

    # Arrange
    scanner = MarkdownScanner(use_main=False)
    supplied_arguments = ["--log-level", "DEBUG", "scan", "does-not-exist.md"]

    expected_return_code = 1
    expected_output = ""
    expected_error = "Provided path 'does-not-exist.md' does not exist."

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, use_direct_arguments=True
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

    assert "Using direct arguments: [" in caplog.text


def test_markdown_without_direct_args(caplog):
    """
    Test to make sure we can specify the arguments normally.
    """

    # Arrange
    scanner = MarkdownScanner(use_main=False)
    supplied_arguments = ["--log-level", "DEBUG", "scan", "does-not-exist.md"]

    expected_return_code = 1
    expected_output = ""
    expected_error = "Provided path 'does-not-exist.md' does not exist."

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, use_direct_arguments=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

    assert "Using supplied command line arguments." in caplog.text


def test_markdown_with_dash_e_single_by_name():
    """
    Test to make sure we get enable a rule if '-e' is supplied and the name of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "-e",
        "debug-only",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
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
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "-e",
        "MD999",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>completed_file
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_enabled_by_configuration_id():
    """
    Test to make sure we enable a rule by using the rule's id in the
    configuration, with no help from the command line.
    The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"enabled": True}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "--log-level",
            "DEBUG",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
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


def test_markdown_with_enabled_by_configuration_name():
    """
    Test to make sure we enable a rule by using the rule's name in the
    configuration, with no help from the command line.
    The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"debug-only": {"enabled": True}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "--stack-trace",
            "--log-level",
            "DEBUG",
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
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


def test_markdown_with_dash_d_single_by_name():
    """
    Test to make sure we get enable a rule if '-d' is supplied and the name of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    fails normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "-d",
        "single-trailing-newline",
        "scan",
        source_path,
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
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "-d",
        "MD047",
        "scan",
        source_path,
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


def test_markdown_with_dash_d_and_dash_e_single_by_name():
    """
    Test to make sure we get disabled if a rule if '-d' is supplied
    and if 'e' is supplied, both with the name of the rule.
    The test data for MD047 is used as it is a simple file that
    fails normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "-d",
        "single-trailing-newline",
        "-e",
        "single-trailing-newline",
        "scan",
        source_path,
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
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "-x-scan",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadTokenizationError encountered while scanning '{source_path}':
An unhandled error occurred processing the document.
""".replace(
        "{source_path}", source_path
    )

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
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "--log-level",
        "DEBUG",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = """"""

    # Act
    ParserLogger.sync_on_next_call()
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

    # Info messages
    assert "Number of files found: " in caplog.text
    assert f"Determining files to scan for path '{source_path}'." in caplog.text

    # Debug messages
    assert f"Provided path '{source_path}' is a valid file. Adding." in caplog.text


def test_markdown_with_dash_dash_log_level_info(caplog):
    """
    Test to make sure we get the right effect if the `--log-level` flag
    is set for info.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "--log-level",
        "INFO",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    ParserLogger.sync_on_next_call()
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

    # Info messages
    assert "Number of files found: " in caplog.text
    assert f"Determining files to scan for path '{source_path}'." in caplog.text

    # Debug messages
    assert f"Provided path '{source_path}' is a valid file. Adding." not in caplog.text


def test_markdown_with_dash_dash_log_level_invalid(caplog):
    """
    Test to make sure we get the right effect if the `--log-level` flag
    is set for an invalid log level.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "--log-level",
        "invalid",
        "scan",
        source_path,
    ]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py [-h] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--set SET_CONFIGURATION] [--strict-config] [--stack-trace]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE]
               {plugins,extensions,scan,scan-stdin,version} ...
main.py: error: argument --log-level: invalid __log_level_type value: 'invalid'
"""

    # Act
    ParserLogger.sync_on_next_call()
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
    # sourcery skip: extract-method
    """
    Test to make sure we get the right effect if the `--log-level` flag
    is set for info with the results going to a file.
    """

    # Arrange
    temp_file = None
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        log_file_name = temp_file.name

    try:
        scanner = MarkdownScanner()
        supplied_arguments = [
            "--log-level",
            "INFO",
            "--log-file",
            log_file_name,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        ParserLogger.sync_on_next_call()
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )

        with open(log_file_name, encoding="utf-8") as file:
            file_data = file.read().replace("\n", "")

        # Info messages
        assert "Number of files found: " in file_data, f">{file_data}<"
        assert f"Determining files to scan for path '{source_path}'." in file_data

        # Debug messages
        assert (
            f"Provided path '{source_path}' is a valid file. Adding." not in file_data
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
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_arguments = [
        "-x-init",
        "scan",
        source_path,
    ]
    fake_directory = "fredo"
    fake_file = "entities.json"
    fake_path = os.path.join(fake_directory, fake_file)
    abs_fake_path = os.path.abspath(fake_path).replace("\\", "\\\\")

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadTokenizationError encountered while initializing tokenizer:\n"
        + "Named character entity map file '"
        + fake_path
        + "' was not loaded "
        + "([Errno 2] No such file or directory: '"
        + abs_fake_path
        + "').\n"
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
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": 2}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>2
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
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
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": "fred"}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
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


def test_markdown_with_dash_e_single_by_id_and_bad_config_file():
    """
    Test to make sure we get an error if we provide a configuration file that is
    in a json format, but not valid.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"myrule.md999": {"test_value": "fred"}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = (
            "Specified configuration file '"
            + configuration_file
            + "' is not valid (Keys strings cannot contain the separator character '.'.).\n"
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


def test_markdown_with_dash_e_single_by_id_and_non_json_config_file():
    """
    Test to make sure we get an error if we provide a configuration file that is
    not in a json format.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = "not a json file"
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
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
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    configuration_file = "not-exists"
    assert not os.path.exists(configuration_file)
    supplied_arguments = [
        "-e",
        "MD999",
        "-c",
        configuration_file,
        "scan",
        source_path,
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
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"other_test_value": 2}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>2
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
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
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"MD999": {"other_test_value": 9}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
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
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": 10}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
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
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": 20}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = """MD999>>init_from_config
MD999>>test_value>>20
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
"""
        expected_error = """BadPluginError encountered while scanning '{source_path}':
(1,1): Plugin id 'MD999' had a critical failure during the 'next_token' action.
""".replace(
            "{source_path}", source_path
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


# TODO add Markdown parsing of some binary file to cause the tokenizer to throw an exception?


def test_markdown_logger_stack_token_normal_output():
    """
    Test for normal output of the stack token for debug output.
    """

    # Arrange
    stack_token = StackToken("type", extra_data=None)

    # Act
    stack_token_string = str(stack_token)

    # Assert
    assert stack_token_string == "StackToken(type)"


def test_markdown_logger_stack_token_extra_output():
    """
    Test for extra output of the stack token for debug output.
    """

    # Arrange
    stack_token = StackToken("type", extra_data="abc")

    # Act
    stack_token_string = str(stack_token)

    # Assert
    assert stack_token_string == "StackToken(type:abc)"


def test_markdown_logger_container_indices():
    """
    Test for ContainerIndices class for output
    """

    # Arrange
    container_indices = ContainerIndices(1, 2, 3)

    # Act
    container_indices_string = str(container_indices)

    # Assert
    assert (
        container_indices_string
        == "{ContainerIndices:ulist_index:1;olist_index:2;block_index:3}"
    )


def test_markdown_logger_active():
    """
    Since calls to it are commented out most of the time,
    test the debug_with_visible_whitespace function manually.
    """
    configuration_file_name = None
    new_handler = None
    root_logger = None
    file_as_lines = None
    try:
        configuration_file_name = write_temporary_configuration("")
        new_handler = logging.FileHandler(configuration_file_name)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(new_handler)

        assert POGGER.is_enabled_for(logging.DEBUG)
        new_logger = ParserLogger(logging.getLogger(__name__))
        new_logger.debug("simple logging")
    finally:
        if root_logger and new_handler:
            root_logger.removeHandler(new_handler)
            new_handler.close()
        with open(configuration_file_name, encoding="utf-8") as file_to_parse:
            file_as_lines = file_to_parse.readlines()
        if configuration_file_name and os.path.exists(configuration_file_name):
            os.remove(configuration_file_name)

    assert len(file_as_lines) == 1
    assert file_as_lines[0] == "simple logging\n"


def test_markdown_logger_inactive():
    """
    Since calls to it are commented out most of the time,
    test the debug_with_visible_whitespace function manually.
    """
    configuration_file_name = None
    new_handler = None
    root_logger = None
    file_as_lines = None
    try:
        configuration_file_name = write_temporary_configuration("")
        new_handler = logging.FileHandler(configuration_file_name)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.WARNING)
        root_logger.addHandler(new_handler)

        assert POGGER.is_enabled_for(logging.WARNING)
        new_logger = ParserLogger(logging.getLogger(__name__))
        new_logger.debug("simple logging")
    finally:
        if root_logger and new_handler:
            root_logger.removeHandler(new_handler)
            new_handler.close()
        with open(configuration_file_name, encoding="utf-8") as file_to_parse:
            file_as_lines = file_to_parse.readlines()
        if configuration_file_name and os.path.exists(configuration_file_name):
            os.remove(configuration_file_name)

    assert not file_as_lines


def test_markdown_logger_arg_list_not_out_of_sync():
    """
    Since calls to it are commented out most of the time,
    test the debug_with_visible_whitespace function manually.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    assert POGGER.is_enabled_for(logging.WARNING)
    new_logger = ParserLogger(logging.getLogger(__name__))
    new_logger.debug_with_visible_whitespace("one sub $ and one in list", " 1 ")


def test_markdown_logger_arg_list_not_out_of_sync_with_debug():
    """
    Since calls to it are commented out most of the time,
    test the debug_with_visible_whitespace function manually.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    assert POGGER.is_enabled_for(logging.DEBUG)
    new_logger = ParserLogger(logging.getLogger(__name__))
    new_logger.debug_with_visible_whitespace("one sub $ and one in list", " 1 ")


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
        new_logger = ParserLogger(logging.getLogger(__name__))
        new_logger.debug("one sub $ but two in list", 1, 2)
        raise AssertionError("An exception should have been thrown by now.")
    except Exception as this_exception:
        assert (
            str(this_exception)
            == "The number of $ substitution characters does not equal the number of arguments in the list."
        )


# pylint: enable=broad-except


def test_markdown_with_bad_strict_config_type():
    """
    Test to make sure that we can set the strict configuration mode from
    the configuration file, capturing any bad errors.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"mode": {"strict-config": 2}}
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
        expected_error = "Configuration Error: The value for property 'mode.strict-config' must be of type 'bool'."

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_good_strict_config_type():
    """
    Test to make sure that we can set the strict configuration mode from
    the configuration file, capturing any bad errors.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"mode": {"strict-config": True}, "log": {"file": 0}}
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
        expected_error = "Configuration Error: The value for property 'log.file' must be of type 'str'.\n"

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_multiple_errors_reported():
    """
    Test to make sure we properly sort errors from files.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md020",
        "single_paragraph_with_whitespace_at_end.md",
    )
    expected_return_code = 1
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_output = (
        f"{source_path}:1:1: MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)\n"
        + f"{source_path}:1:12: "
        + "MD010: Hard tabs "
        + "[Column: 12] (no-hard-tabs)\n"
        # + f"{source_path}:2:2: "
        # + "MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. "
        # + "(no-multiple-space-closed-atx)\n"
        + f"{source_path}:2:2: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{source_path}:2:2: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + f"{source_path}:2:14: "
        + "MD010: Hard tabs "
        + "[Column: 14] (no-hard-tabs)"
    )

    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_ae_with_invalid_file_extension():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "scan",
        "-ae",
        ".abc",
        file_to_scan,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        f"Provided file path '{file_to_scan}' is not a valid file. Skipping."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_ae_with_valid_file_extension():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        ".txt",
        file_to_scan,
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


def test_markdown_with_dash_ae_with_valid_file_extension_multiple():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = "test/resources/double-line-with-blank-and-trailing.txt"
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        ".txt,.md",
        file_to_scan,
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


def test_markdown_with_dash_ae_with_invalid_file_extension_no_period():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        "md",
        file_to_scan,
    ]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension 'md' must start with a period."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_ae_with_invalid_file_extension_no_alphanum():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        ".*",
        file_to_scan,
    ]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension '.*' must only contain alphanumeric characters after the period."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_ae_with_invalid_file_extension_only_period():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        ".",
        file_to_scan,
    ]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension '.' must have at least one character after the period."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_ae_with_invalid_file_extension_semicolon_as_sep():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        ".md;.txt",
        file_to_scan,
    ]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension '.md;.txt' must only contain alphanumeric characters after the period."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_ae_with_invalid_file_extension_empty():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        "",
        file_to_scan,
    ]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension '' must start with a period."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_scan_stdin_without_triggers():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan-stdin",
    ]

    supplied_standard_input = "test\nme\n"
    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=supplied_standard_input
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_scan_stdin_with_triggers():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan-stdin",
    ]

    supplied_standard_input = "# test"
    expected_return_code = 1
    expected_output = """stdin:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
stdin:1:6: MD047: Each file should end with a single newline character. (single-trailing-newline)"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=supplied_standard_input
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_scan_stdin_with_bad_write():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "-x-stdin",
        "scan-stdin",
    ]

    supplied_standard_input = f"# test{os.linesep}"
    expected_return_code = 1
    expected_output = ""
    expected_error = """OSError encountered while scanning 'stdin':
Temporary file to capture stdin was not written (made up)."""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=supplied_standard_input
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
