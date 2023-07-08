"""
Module to provide for an API to directly communicate with PyMarkdown instead
of using a command line.
"""
import argparse
from dataclasses import dataclass
from typing import Any, List, Optional

from pymarkdown.application_file_scanner import ApplicationFileScanner
from pymarkdown.application_logging import ApplicationLogging
from pymarkdown.main import PyMarkdownLint
from pymarkdown.main_presentation import MainPresentation
from pymarkdown.plugin_manager.plugin_scan_failure import PluginScanFailure


class PyMarkdownApi:
    """
    Module to provide for an API to directly communicate with PyMarkdown instead
    of using a command line.
    """

    __INTERFACE_VERSION = 1

    def __init__(self, inherit_logging: bool = False) -> None:
        self.__inherit_logging = inherit_logging

        self.__log_level = ApplicationLogging.log_level_warning
        self.__log_file_path: Optional[str] = None
        self.__enable_stack_trace = False

    @property
    def application_version(self) -> str:
        """
        Report on the application version.
        """
        return PyMarkdownLint().application_version

    @property
    def interface_version(self) -> int:
        """
        Report on the interface version.
        """
        return PyMarkdownApi.__INTERFACE_VERSION

    def enable_stack_trace(self) -> "PyMarkdownApi":
        """
        Enable the reporting of stack traces for any exceptions caught by the API.
        """
        self.__enable_stack_trace = True
        return self

    def log_debug_and_above(self) -> "PyMarkdownApi":
        """
        Enable logging for the DEBUG level and above.
        """
        return self.log(ApplicationLogging.log_level_debug)

    def log_info_and_above(self) -> "PyMarkdownApi":
        """
        Enable logging for the INFO level and above.
        """
        return self.log(ApplicationLogging.log_level_info)

    def log_warning_and_above(self) -> "PyMarkdownApi":
        """
        Enable logging for the WARN level and above.
        """
        return self.log(ApplicationLogging.log_level_warning)

    def log_error_and_above(self) -> "PyMarkdownApi":
        """
        Enable logging for the ERROR level and above.
        """
        return self.log(ApplicationLogging.log_level_error)

    def log_critical_and_above(self) -> "PyMarkdownApi":
        """
        Enable logging for the CRITICAL level and above.
        """
        return self.log(ApplicationLogging.log_level_critical)

    def log(self, log_level: str) -> "PyMarkdownApi":
        """
        Set the logging level using a string value.
        """
        if not ApplicationLogging.is_valid_log_level_type(log_level):
            log_levels_in_order = ",".join(ApplicationLogging.get_valid_log_levels())
            raise PyMarkdownApiArgumentException(
                "log_level",
                f"Parameter 'log_level' must be one of {log_levels_in_order}",
            )

        if self.__inherit_logging:
            raise PyMarkdownApiNotSupportedException(
                "Set log level functions are not supported in log-inheritance mode."
            )

        self.__log_level = log_level
        return self

    def log_to_file(self, log_file_path: str) -> "PyMarkdownApi":
        """
        Set a file to log any results to.
        """
        self.__verify_string_argument_not_empty("log_file_path", log_file_path)

        if self.__inherit_logging:
            raise PyMarkdownApiNotSupportedException(
                "Set log file function is not supported in log-inheritance mode."
            )

        self.__log_file_path = log_file_path
        return self

    def list_path(
        self,
        path_to_scan: str,
        recurse_if_directory: bool = False,
        alternate_extensions: str = "",
    ) -> "ListPathResult":
        """
        List any files found when scanning the specified path for eligible markdown files.
        """
        self.__verify_string_argument_not_empty("path_to_scan", path_to_scan)

        scan_arguments = self.__build_common_arguments("scan")
        scan_arguments.append("--list-files")
        self.__add_common_scan_arguments(
            scan_arguments, path_to_scan, recurse_if_directory, alternate_extensions
        )

        this_presentation = ApiPresentation()
        scanner_instance = PyMarkdownLint(
            presentation=this_presentation,
            show_stack_trace=self.__enable_stack_trace,
            inherit_logging=self.__inherit_logging,
        )
        return_code = 0
        try:
            scanner_instance.main(scan_arguments)
        except SystemExit as this_exception:
            return_code = (
                int(this_exception.code) if isinstance(this_exception.code, int) else 99
            )

        if return_code != 0:
            self.__generate_exception(this_presentation)
        return ListPathResult(this_presentation.pso[0].split("\n"))

    def scan_path(
        self,
        path_to_scan: str,
        recurse_if_directory: bool = False,
        alternate_extensions: Any = None,
    ) -> "ScanPathResult":
        """
        Scan the provided path for markdown files to scan.
        """
        self.__verify_string_argument_not_empty("path_to_scan", path_to_scan)

        scan_arguments = self.__build_common_arguments("scan")
        if recurse_if_directory:
            scan_arguments.append("--recurse")
        if alternate_extensions:
            self.__verify_string_argument_alternate_extensions(
                "alternate_extensions", alternate_extensions
            )
            scan_arguments.append("-ae")
            scan_arguments.append(alternate_extensions)
        scan_arguments.append(path_to_scan)

        this_presentation = ApiPresentation()
        scanner_instance = PyMarkdownLint(
            presentation=this_presentation,
            show_stack_trace=self.__enable_stack_trace,
            inherit_logging=self.__inherit_logging,
        )
        return_code = 0
        try:
            scanner_instance.main(scan_arguments)
        except SystemExit as this_exception:
            # https://github.com/python/typeshed/issues/8513#issue-1333671093
            return_code = (
                int(this_exception.code) if isinstance(this_exception.code, int) else 99
            )
        print(this_presentation.pragma_errors)
        print(this_presentation.scan_failures)
        assert (
            len(this_presentation.pso) == 0
        )  # should not display for scan_path, but for ext ops and plugin ops
        print(this_presentation.pse)
        if return_code != 0:
            self.__generate_exception(this_presentation)
        return ScanPathResult(
            this_presentation.scan_failures, this_presentation.pragma_errors
        )

    def __generate_exception(self, this_presentation: "ApiPresentation") -> None:
        if not this_presentation.pse:
            return
        last_error_text = this_presentation.pse[-1]
        second_last_error_text = (
            this_presentation.pse[-2].strip("\n")
            if len(this_presentation.pse) > 1
            else ""
        )
        if last_error_text == "\n\nNo matching files found.":
            raise PyMarkdownApiNoFilesFoundException(second_last_error_text)
        raise PyMarkdownApiException(this_presentation.pse[-1].strip("\n"))

    def __add_common_scan_arguments(
        self,
        scan_arguments: List[str],
        path_to_scan: str,
        recurse_if_directory: bool,
        alternate_extensions: str,
    ) -> None:
        if recurse_if_directory:
            scan_arguments.append("--recurse")
        if alternate_extensions:
            self.__verify_string_argument_alternate_extensions(
                "alternate_extensions", alternate_extensions
            )
            scan_arguments.extend(("-ae", alternate_extensions))
        scan_arguments.append(path_to_scan)

    def __build_common_arguments(self, action_to_invoke: str) -> List[str]:
        common_arguments: List[str] = []
        if self.__enable_stack_trace:
            common_arguments.append("--stack-trace")
        if not self.__inherit_logging:
            if self.__log_file_path:
                common_arguments.extend(("--log-file", self.__log_file_path))
            common_arguments.extend(["--log-level", self.__log_level])
        common_arguments.append(action_to_invoke)
        return common_arguments

    def __verify_string_argument_not_empty(
        self, argument_name: str, string_to_validate: str
    ) -> None:
        string_to_validate = string_to_validate.strip()
        if not string_to_validate:
            raise PyMarkdownApiArgumentException(
                argument_name, f"Parameter named '{argument_name}' cannot be empty."
            )

    def __verify_string_argument_alternate_extensions(
        self, argument_name: str, string_to_validate: str
    ) -> None:
        try:
            _ = ApplicationFileScanner.is_valid_comma_separated_extension_list(
                string_to_validate
            )
        except argparse.ArgumentTypeError as this_exception:
            raise PyMarkdownApiArgumentException(
                argument_name,
                f"Parameter named '{argument_name}' is not a valid comma-separated list of extensions.",
            ) from this_exception


@dataclass(frozen=True)
class PragmaError:
    """
    Class to encapsulate the information for a pragma error.
    """

    file_path: str
    line_number: int
    pragma_error: str


@dataclass(frozen=True)
class ScanPathResult:
    """
    Result for the scan_path function.
    """

    scan_failures: List[PluginScanFailure]
    pragma_errors: List[PragmaError]


@dataclass(frozen=True)
class ListPathResult:
    """
    Result for the list_path function.
    """

    matching_files: List[str]


class PyMarkdownApiException(Exception):
    """
    Class to provide for an exception that is thrown by the API layer.
    """

    def __init__(self, reason: str) -> None:
        self.__reason = reason

    @property
    def reason(self) -> str:
        """
        Reported reason why there were no files found to process.
        """
        return self.__reason


class PyMarkdownApiNotSupportedException(PyMarkdownApiException):
    """
    Class to provide for an exception that a given situation is not supported.
    """


class PyMarkdownApiArgumentException(PyMarkdownApiException):
    """
    Class to provide for an argument that an exception is not valid.
    """

    def __init__(self, argument_name: str, reason: str) -> None:
        super().__init__(reason)
        self.__argument_name = argument_name

    @property
    def argument_name(self) -> str:
        """
        Argument that caused this exception to be raised.
        """
        return self.__argument_name


class PyMarkdownApiNoFilesFoundException(PyMarkdownApiException):
    """
    Class to provide for an exception that the invoked API was not able to find at least one file to process.
    """


class ApiPresentation(MainPresentation):
    """
    Class to provide for the output of the PyMarkdown application.
    """

    def __init__(self) -> None:
        self.pso: List[str] = []
        self.pse: List[str] = []
        self.pragma_errors: List[PragmaError] = []
        self.scan_failures: List[PluginScanFailure] = []

    def print_system_output(self, output_string: str) -> None:
        """
        Root function to output to standard out.
        """
        self.pso.append(output_string)

    def print_system_error(self, error_string: str) -> None:
        """
        Root function to output to standard error.
        """
        self.pse.append(error_string)

    def format_scan_error(
        self, next_file: str, this_exception: Exception
    ) -> Optional[str]:
        """
        Format a scan error for display.  Returning a value of None means that
        the function has handled any required output.
        """
        return f"format_scan_error->{type(this_exception).__name__} encountered while scanning '{next_file}':\n{this_exception}"

    def print_pragma_failure(
        self, scan_file: str, line_number: int, pragma_error: str
    ) -> None:
        """
        Print a failure to compile the pragma.
        """
        self.pragma_errors.append(PragmaError(scan_file, line_number, pragma_error))

    def print_scan_failure(self, scan_failure: PluginScanFailure) -> None:
        """
        Print a scan failure for a specific file and location.
        """
        self.scan_failures.append(scan_failure)
