"""
Module to provide for the output of the PyMarkdown application.
"""

from abc import ABC, abstractmethod
from typing import Optional

from pymarkdown.plugin_manager.plugin_scan_failure import PluginScanFailure


class BasePresentation(ABC):
    """
    Class to provide for the output of the PyMarkdown application.
    """

    @abstractmethod
    def print_system_output(self, output_string: str) -> None:
        """
        Root function to output to standard out.
        """

    @abstractmethod
    def print_system_error(self, error_string: str) -> None:
        """
        Root function to output to standard error.
        """

    @abstractmethod
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

    @abstractmethod
    def print_pragma_failure(
        self, scan_file: str, line_number: int, pragma_error: str
    ) -> None:
        """
        Print a failure to compile the pragma.
        """

    @abstractmethod
    def print_scan_failure(self, scan_failure: PluginScanFailure) -> None:
        """
        Print a scan failure for a specific file and location.
        """

    @abstractmethod
    def print_fix_message(self, file_fixed: str) -> None:
        """
        Print a message indicating that a given file has been fixed.
        """
