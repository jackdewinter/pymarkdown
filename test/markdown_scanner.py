"""
Module to provide for a local instance of an InProcessExecution class.
"""

import os
import sys
from test.pytest_execute import InProcessExecution
from typing import List, Optional

from typing_extensions import override

from pymarkdown.general.base_presentation import BasePresentation
from pymarkdown.plugin_manager.plugin_scan_failure import PluginScanFailure

# https://docs.pytest.org/en/latest/goodpractices.html#tests-outside-application-code
sys.path.insert(0, os.path.abspath("pymarkdown"))  # isort:skip
# pylint: disable=wrong-import-position
from pymarkdown.main import PyMarkdownLint  # isort:skip
from pymarkdown.__main__ import main

# pylint: enable=wrong-import-position


class AlternateMainPresentation(BasePresentation):
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

    # pylint: disable=useless-return

    def format_scan_error(
        self,
        next_file: str,
        this_exception: Exception,
        show_extended_information: bool = False,
        allow_shortcut: bool = False,
    ) -> Optional[str]:
        """
        Format a scan error for display.  Returning a value of None means that
        the function has handled any required output.
        """
        if allow_shortcut:
            formatted_error = f"{next_file}:0:0: {this_exception}"
        else:
            formatted_error = f"{type(this_exception).__name__} encountered while scanning '{next_file}':\n{this_exception}"
            if show_extended_information:
                current_cause = this_exception.__cause__
                while current_cause:
                    formatted_error += f"\nCaused by: {type(current_cause).__name__}:\n   {current_cause}"
                    current_cause = current_cause.__cause__

        scan_error = "[fse[" + (formatted_error if formatted_error else "") + "]]"
        self.print_system_error(scan_error)
        return None

    # pylint: enable=useless-return

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
            + f"{scan_failure.rule_id}: {scan_failure.rule_description}{scan_failure.extra_error_information} ({scan_failure.rule_name}) "
            + f"{scan_failure.rule_url}]]"
        )

    def print_fix_message(self, file_fixed: str) -> None:
        self.print_system_output(f"[pfm[{file_fixed}]]")


class MarkdownScanner(InProcessExecution):
    """
    Class to provide for a local instance of an InProcessExecution class.
    """

    def __init__(
        self,
        use_module: bool = False,
        use_main: bool = False,
        use_alternate_presentation: bool = False,
    ) -> None:
        super().__init__()
        self.__use_main = use_main
        self.__use_alternate_presentation = use_alternate_presentation

        self.__entry_point = "__main.py__" if use_module else "main.py"
        resource_directory = os.path.join(os.getcwd(), "test", "resources")
        assert os.path.exists(resource_directory)
        assert os.path.isdir(resource_directory)
        self.resource_directory = resource_directory

    @override
    def execute_main(self, direct_arguments: Optional[List[str]] = None) -> None:
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

    @override
    def get_main_name(self) -> str:
        return self.__entry_point
