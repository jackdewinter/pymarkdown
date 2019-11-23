"""
Module to provide tests for the CommandProcessor class.
Specifically, these tests verify the general behavior of the class.
"""
import os
import sys
import traceback
import io

# https://docs.pytest.org/en/latest/goodpractices.html#tests-outside-application-code
sys.path.insert(0, os.path.abspath("."))  # isort:skip
print(os.path.abspath("."))
# pylint: disable=wrong-import-position
from pymarkdown.main import PyMarkdownLint  # isort:skip
from test.pytest_execute import InProcessExecution

class Xx(InProcessExecution):
    def efg(self):
        PyMarkdownLint().main()
    def ghi(self):
        return "main.py"

def test_markdown_with_no_parameters():
    """
    Test to make sure we get the simple information if no parameters are supplied.
    """

    # Arrange
    suppplied_arguments = []

    expected_return_code = 2
    expected_output = ""
    expected_error =\
"""usage: main.py [-h] [--version] [-l] path [path ...]
main.py: error: the following arguments are required: path
"""    

    # Act
    execute_results = Xx().abc(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(expected_output, expected_error, expected_return_code)

def test_markdown_with_dash_h():
    """
    Test to make sure we get help if '-h' is supplied.
    """

    # Arrange
    suppplied_arguments = ['-h']

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
    execute_results = Xx().abc(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(expected_output, expected_error, expected_return_code)


def test_markdown_with_dash_dash_help():
    """
    Test to make sure we get help if '--help' is supplied.
    """

    # Arrange
    suppplied_arguments = ['--help']

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
    execute_results = Xx().abc(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(expected_output, expected_error, expected_return_code)


def test_markdown_with_dash_dash_version():
    """
    Test to make sure we get help if '--version' is supplied.
    """

    # Arrange
    suppplied_arguments = ['--version']

    expected_return_code = 0
    expected_output = """main.py 0.1.0
"""
    expected_error = ""

    # Act
    execute_results = Xx().abc(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(expected_output, expected_error, expected_return_code)

