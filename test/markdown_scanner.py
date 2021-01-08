"""
Module to provide for a local instance of a InProcessExecution class.
"""
import os
import sys
from test.pytest_execute import InProcessExecution

# https://docs.pytest.org/en/latest/goodpractices.html#tests-outside-application-code
sys.path.insert(0, os.path.abspath("pymarkdown"))  # isort:skip
# pylint: disable=wrong-import-position
from pymarkdown.main import PyMarkdownLint  # isort:skip

# pylint: enable=wrong-import-position


class MarkdownScanner(InProcessExecution):
    """
    Class to provide for a local instance of a InProcessExecution class.
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
