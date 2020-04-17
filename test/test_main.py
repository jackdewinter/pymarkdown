"""
Module to provide tests related to the basic parts of the scanner.
"""
from test.markdown_scanner import MarkdownScanner


def test_markdown_with_no_parameters():
    """
    Test to make sure we get the simple information if no parameters are supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = []

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py [-h] [--version] [-l] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--stack-trace]
               path [path ...]
main.py: error: the following arguments are required: path
"""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = ["-h"]

    expected_return_code = 0
    expected_output = """usage: main.py [-h] [--version] [-l] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--stack-trace]
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
  --stack-trace         if an error occurs, print out the stack trace for
                        debug purposes
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = ["--version"]

    expected_return_code = 0
    expected_output = """main.py 0.1.0
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "-e",
        "debug-only",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 0
    expected_output = """MD999>>init_from_config
MD999>>starting_new_file>>
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>token:[atx:1:0:]
MD999>>token:[text:This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK:]
MD999>>token:[para:]
MD999>>token:[text:The line after this line should be blank.:]
MD999>>token:[end-para]
MD999>>token:[BLANK:]
MD999>>completed_file
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "-e",
        "MD999",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 0
    expected_output = """MD999>>init_from_config
MD999>>starting_new_file>>
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>token:[atx:1:0:]
MD999>>token:[text:This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK:]
MD999>>token:[para:]
MD999>>token:[text:The line after this line should be blank.:]
MD999>>token:[end-para]
MD999>>token:[BLANK:]
MD999>>completed_file
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "-d",
        "single-trailing-newline",
        "test/resources/rules/md047/end_with_blank_line.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

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
    suppplied_arguments = [
        "-d",
        "MD047",
        "test/resources/rules/md047/end_with_no_blank_line.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_x():
    """
    Test to make sure we get enable a rule if '-d' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    fails normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "-x",
        "test/resources/rules/md047/end_with_no_blank_line.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """BadParsingError encountered while scanning 'test/resources/rules/md047/end_with_no_blank_line.md':
File was not translated from Markdown text to Markdown tokens.
"""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


# TODO add Markdown parsing of some binary file to cause the tokenizer to throw an exception?
