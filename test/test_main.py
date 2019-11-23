"""
Module to provide tests for the CommandProcessor class.
Specifically, these tests verify the general behavior of the class.
"""
import os
import sys
from test.pytest_execute import InProcessExecution

# https://docs.pytest.org/en/latest/goodpractices.html#tests-outside-application-code
sys.path.insert(0, os.path.abspath("."))  # isort:skip
print(os.path.abspath("."))
# pylint: disable=wrong-import-position
from pymarkdown.main import PyMarkdownLint  # isort:skip


class MarkdownScanner(InProcessExecution):
    """
    Local instance.
    """

    def __init__(self):
        super().__init__()
        resource_directory = os.path.join(os.getcwd(), "test", "resources")
        assert os.path.exists(resource_directory)
        assert os.path.isdir(resource_directory)
        self.resource_directory = resource_directory

    def execute_main(self):
        PyMarkdownLint().main()

    def get_main_name(self):
        return "main.py"


def test_markdown_with_no_parameters():
    """
    Test to make sure we get the simple information if no parameters are supplied.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = []

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py [-h] [--version] [-l] path [path ...]
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
    expected_output = """usage: main.py [-h] [--version] [-l] path [path ...]

Lint any found Markdown files.

positional arguments:
  path              One or more paths to scan for eligible files

optional arguments:
  -h, --help        show this help message and exit
  --version         show program's version number and exit
  -l, --list-files  list the markdown files found and exit.
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


def test_markdown_with_dash_l_only():
    """
    Test to make sure we get help if '-l' is supplied without any paths
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = ["-l"]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py [-h] [--version] [-l] path [path ...]
main.py: error: the following arguments are required: path
"""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_bad_path():
    """
    Test to make sure we get help if '-l' is supplied with a bad path.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = ["-l", "my-bad-path"]

    expected_return_code = 1
    expected_output = ""
    expected_error = """Provided path 'my-bad-path' does not exist. Skipping.
No Markdown files found.
"""

    # Act
    execute_results = scanner.invoke_main(
        arguments=suppplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_non_md_directory():
    """
    Test to make sure we get help if '-l' is supplied with a path containing no md files.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = ["-l", "only-text"]

    expected_return_code = 1
    expected_output = ""
    expected_error = """No Markdown files found.
"""

    # Act
    execute_results = scanner.invoke_main(
        arguments=suppplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_md_directory():
    """
    Test to make sure we get help if '-l' is supplied with a path containing a simple md file.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = ["-l", "simple"]

    expected_return_code = 0
    expected_output = """simple/simple.md
""".replace(
        "/", os.path.sep
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=suppplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_non_md_file():
    """
    Test to make sure we get help if '-l' is supplied with a file path that isn't a md file.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = ["-l", "only-text/simple_text_file.txt"]

    expected_return_code = 1
    expected_output = ""
    expected_error = """Provided file path 'only-text/simple_text_file.txt' is not a valid markdown file. Skipping.
No Markdown files found.
"""

    # Act
    execute_results = scanner.invoke_main(
        arguments=suppplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_md_file():
    """
    Test to make sure we get help if '-l' is supplied with a file path that is a simple md file.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = ["-l", "simple/simple.md"]

    expected_return_code = 0
    expected_output = """simple/simple.md
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=suppplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
