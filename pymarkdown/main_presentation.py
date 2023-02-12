"""
Module to provide for the output of the PyMarkdown application.
"""
import sys
from typing import Optional

from pymarkdown.plugin_manager.plugin_scan_failure import PluginScanFailure


class MainPresentation:
    """
    Class to provide for the output of the PyMarkdown application.
    """

    def print_system_output(self, output_string: str) -> None:
        """
        Root function to output to standard out.
        """
        print(output_string, file=sys.stdout)

    def print_system_error(self, error_string: str) -> None:
        """
        Root function to output to standard error.
        """
        print(error_string, file=sys.stderr)

    def format_scan_error(
        self, next_file: str, this_exception: Exception
    ) -> Optional[str]:
        """
        Format a scan error for display.  Returning a value of None means that
        the function has handled any required output.
        """
        return f"{type(this_exception).__name__} encountered while scanning '{next_file}':\n{this_exception}"

    def print_pragma_failure(
        self, scan_file: str, line_number: int, pragma_error: str
    ) -> None:
        """
        Print a failure to compile the pragma.
        """
        self.print_system_error(f"{scan_file}:{line_number}:1: INLINE: {pragma_error}")

    def print_scan_failure(self, scan_failure: PluginScanFailure) -> None:
        """
        Print a scan failure for a specific file and location.
        """
        self.print_system_output(
            f"{scan_failure.scan_file}:{scan_failure.line_number}:{scan_failure.column_number}: "
            + f"{scan_failure.rule_id}: {scan_failure.rule_description}{scan_failure.extra_error_information} ({scan_failure.rule_name})"
        )
