"""
Module to provide for a local instance of an InProcessExecution class.
"""
import os
import sys
from test.pytest_execute import InProcessExecution
from typing import Optional

from pymarkdown.general.main_presentation import MainPresentation
from pymarkdown.plugin_manager.plugin_scan_failure import PluginScanFailure

# https://docs.pytest.org/en/latest/goodpractices.html#tests-outside-application-code
sys.path.insert(0, os.path.abspath("pymarkdown"))  # isort:skip
# pylint: disable=wrong-import-position
from pymarkdown.main import PyMarkdownLint  # isort:skip
from pymarkdown.__main__ import main

# pylint: enable=wrong-import-position


class AlternateMainPresentation(MainPresentation):
    """
    Alternate presentation class to test that an alternate presentation
    can be effected.
    """

    def print_system_output(self, output_string: str) -> None:
        """
        Root function to output to standard out.
        """
        print("[pso[" + output_string + "]]", file=sys.stdout)

    def print_system_error(self, error_string: str) -> None:
        """
        Root function to output to standard error.
        """
        print("[pse[" + error_string + "]]", file=sys.stderr)

    def format_scan_error(
        self, next_file: str, this_exception: Exception
    ) -> Optional[str]:
        """
        Format a scan error for display.  Returning a value of None means that
        the function has handled any required output.
        """
        scan_error = (
            "[fse[" + super().format_scan_error(next_file, this_exception) + "]]"
        )
        self.print_system_error(scan_error)

    def print_pragma_failure(
        self, scan_file: str, line_number: int, pragma_error: str
    ) -> None:
        """
        Print a failure to compile the pragma.
        """
        self.print_system_error(
            f"[ppf[{scan_file}:{line_number}:1: INLINE: {pragma_error}]]"
        )

    def print_scan_failure(self, scan_failure: PluginScanFailure) -> None:
        """
        Print a scan failure for a specific file and location.
        """
        self.print_system_output(
            f"[psf[{scan_failure.scan_file}:{scan_failure.line_number}:{scan_failure.column_number}: "
            + f"{scan_failure.rule_id}: {scan_failure.rule_description}{scan_failure.extra_error_information} ({scan_failure.rule_name})]]"
        )


class MarkdownScanner(InProcessExecution):
    """
    Class to provide for a local instance of an InProcessExecution class.
    """

    def __init__(
        self, use_module=False, use_main=False, use_alternate_presentation=False
    ):
        super().__init__()
        self.__use_main = use_main
        self.__use_alternate_presentation = use_alternate_presentation

        self.__entry_point = "__main.py__" if use_module else "main.py"
        resource_directory = os.path.join(os.getcwd(), "test", "resources")
        assert os.path.exists(resource_directory)
        assert os.path.isdir(resource_directory)
        self.resource_directory = resource_directory

    def execute_main(self, direct_arguments=None):
        if self.__use_main:
            main()
        else:
            presentation_to_use = (
                AlternateMainPresentation()
                if self.__use_alternate_presentation
                else None
            )
            PyMarkdownLint(presentation=presentation_to_use).main(
                direct_args=direct_arguments
            )

    def get_main_name(self):
        return self.__entry_point
