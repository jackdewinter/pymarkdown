"""
Module to provide for a local instance of an InProcessExecution class.
"""
import os
import sys
from test.pytest_execute import InProcessExecution

# https://docs.pytest.org/en/latest/goodpractices.html#tests-outside-application-code
sys.path.insert(0, os.path.abspath("pymarkdown"))  # isort:skip
# pylint: disable=wrong-import-position
from pymarkdown.main import PyMarkdownLint  # isort:skip
from pymarkdown.__main__ import main

# pylint: enable=wrong-import-position


class MarkdownScanner(InProcessExecution):
    """
    Class to provide for a local instance of an InProcessExecution class.
    """

    def __init__(self, use_module=False, use_main=False):
        super().__init__()
        self.__use_main = use_main

        self.__entry_point = "__main.py__" if use_module else "main.py"
        resource_directory = os.path.join(os.getcwd(), "test", "resources")
        assert os.path.exists(resource_directory)
        assert os.path.isdir(resource_directory)
        self.resource_directory = resource_directory

    def execute_main(self):
        if self.__use_main:
            main()
        else:
            PyMarkdownLint().main()

    def get_main_name(self):
        return self.__entry_point
