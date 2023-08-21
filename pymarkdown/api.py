"""
Module to provide for an API to directly communicate with PyMarkdown instead
of using a command line.
"""
import argparse
from dataclasses import dataclass
from typing import Any, List, Optional

from pymarkdown.application_file_scanner import ApplicationFileScanner
from pymarkdown.application_logging import ApplicationLogging
from pymarkdown.general.main_presentation import MainPresentation
from pymarkdown.main import PyMarkdownLint
from pymarkdown.plugin_manager.plugin_scan_failure import PluginScanFailure


# pylint: disable=too-many-instance-attributes,too-many-public-methods
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
        self.__enable_strict_configuration = False
        self.__plugin_paths_to_add: List[str] = []
        self.__configuration_path: Optional[str] = None
        self.__enable_rule_identifiers: List[str] = []
        self.__disable_rule_identifiers: List[str] = []
        self.__set_properties: List[str] = []

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

    def add_plugin_path(self, path_to_plugin: str) -> "PyMarkdownApi":
        """
        Add a plugin path that points to a directory with plugins or a single plugin.
        """
        self.__verify_string_argument_not_empty("path_to_plugin", path_to_plugin)

        self.__plugin_paths_to_add.append(path_to_plugin)
        return self

    def configuration_file_path(self, path_to_config_file: str) -> "PyMarkdownApi":
        """
        Set the path to the configuration file to use.
        """
        self.__verify_string_argument_not_empty(
            "path_to_config_file", path_to_config_file
        )

        self.__configuration_path = path_to_config_file
        return self

    def set_boolean_property(
        self, property_name: str, property_value: bool
    ) -> "PyMarkdownApi":
        """
        Set a named configuration property to a given boolean value.
        """
        self.__verify_string_argument_not_empty("property_name", property_name)
        if not isinstance(property_value, bool):
            raise PyMarkdownApiArgumentException(
                "property_value",
                "The property value 'property_value' was not passed as a boolean.",
            )

        self.__set_properties.append(f"{property_name}=$!{property_value}")
        return self

    def set_integer_property(
        self, property_name: str, property_value: int
    ) -> "PyMarkdownApi":
        """
        Set a named configuration property to a given integer value.
        """
        self.__verify_string_argument_not_empty("property_name", property_name)
        if not isinstance(property_value, int):
            raise PyMarkdownApiArgumentException(
                "property_value",
                "The property value 'property_value' was not passed as an integer.",
            )

        self.__set_properties.append(f"{property_name}=$#{property_value}")
        return self

    def set_string_property(
        self, property_name: str, property_value: str
    ) -> "PyMarkdownApi":
        """
        Set a named configuration property to a given string value.
        """
        self.__verify_string_argument_not_empty("property_name", property_name)
        if not isinstance(property_value, str):
            raise PyMarkdownApiArgumentException(
                "property_value",
                "The property value 'property_value' was not passed as a string.",
            )

        self.__set_properties.append(f"{property_name}=$${property_value}")
        return self

    def set_property(self, property_name: str, property_value: Any) -> "PyMarkdownApi":
        """
        Set a named configuration property to a given value.  Whatever is passed in as
        the property_value parameter is traslated into a string.
        """
        self.__verify_string_argument_not_empty("property_name", property_name)

        self.__set_properties.append(f"{property_name}={str(property_value)}")
        return self

    def enable_strict_configuration(self) -> "PyMarkdownApi":
        """
        Enable strict configuration for any requested properties, either through configuration files or manual setting.
        """
        self.__enable_strict_configuration = True
        return self

    def disable_rule_by_identifier(self, rule_identifier: str) -> "PyMarkdownApi":
        """
        Disable a given rule by its identifier.
        """
        self.__verify_string_argument_not_empty("rule_identifier", rule_identifier)

        self.__disable_rule_identifiers.append(rule_identifier)
        return self

    def enable_rule_by_identifier(self, rule_identifier: str) -> "PyMarkdownApi":
        """
        Enable a given rule by its identifier.
        """
        self.__verify_string_argument_not_empty("rule_identifier", rule_identifier)

        self.__enable_rule_identifiers.append(rule_identifier)
        return self

    def list_path(
        self,
        path_to_scan: str,
        recurse_if_directory: bool = False,
        alternate_extensions: str = "",
    ) -> "PyMarkdownListPathResult":
        """
        List any files found when scanning the specified path for eligible markdown files.
        """
        self.__verify_string_argument_not_empty("path_to_scan", path_to_scan)

        scan_arguments = self.__build_common_arguments("scan")
        scan_arguments.append("--list-files")
        self.__add_common_scan_arguments(
            scan_arguments, path_to_scan, recurse_if_directory, alternate_extensions
        )

        this_presentation = _ApiPresentation()
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
        return PyMarkdownListPathResult(this_presentation.pso[0].split("\n"))

    def scan_path(
        self,
        path_to_scan: str,
        recurse_if_directory: bool = False,
        alternate_extensions: Any = None,
    ) -> "PyMarkdownScanPathResult":
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

        this_presentation = _ApiPresentation()
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
        return self.__handle_scan_results(return_code, this_presentation)

    def __handle_scan_results(
        self, return_code: int, this_presentation: "_ApiPresentation"
    ) -> "PyMarkdownScanPathResult":
        assert (
            len(this_presentation.pso) == 0
        )  # should not display for scan_path, but for ext ops and plugin ops
        if return_code != 0:
            self.__generate_exception(this_presentation)
        return PyMarkdownScanPathResult(
            this_presentation.scan_failures, this_presentation.pragma_errors
        )

    def scan_string(
        self,
        string_to_scan: str,
    ) -> "PyMarkdownScanPathResult":
        """
        Scan a string passed into the API.
        """
        self.__verify_string_argument_not_empty("path_to_scan", string_to_scan)

        scan_arguments = self.__build_common_arguments("scan-stdin")

        this_presentation = _ApiPresentation()
        scanner_instance = PyMarkdownLint(
            presentation=this_presentation,
            show_stack_trace=self.__enable_stack_trace,
            inherit_logging=self.__inherit_logging,
            string_to_scan=string_to_scan,
        )
        return_code = 0
        try:
            scanner_instance.main(scan_arguments)
        except SystemExit as this_exception:
            # https://github.com/python/typeshed/issues/8513#issue-1333671093
            return_code = (
                int(this_exception.code) if isinstance(this_exception.code, int) else 99
            )
        return self.__handle_scan_results(return_code, this_presentation)

    def __generate_exception(self, this_presentation: "_ApiPresentation") -> None:
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
        if self.__enable_strict_configuration:
            common_arguments.append("--strict-config")

        if not self.__inherit_logging:
            if self.__log_file_path:
                common_arguments.extend(("--log-file", self.__log_file_path))
            common_arguments.extend(["--log-level", self.__log_level])

        if self.__configuration_path:
            common_arguments.extend(["--config", self.__configuration_path])

        for next_property in self.__set_properties:
            common_arguments.extend(("--set", next_property))
        for next_path in self.__plugin_paths_to_add:
            common_arguments.extend(("--add-plugin", next_path))
        if self.__enable_rule_identifiers:
            rules_to_enable = "".join(
                f",{next_identifier}"
                for next_identifier in self.__enable_rule_identifiers
            )
            common_arguments.extend(("--enable-rules", rules_to_enable))
        if self.__disable_rule_identifiers:
            rules_to_disable = "".join(
                f",{next_identifier}"
                for next_identifier in self.__disable_rule_identifiers
            )
            common_arguments.extend(("--disable-rules", rules_to_disable))

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


# pylint: enable=too-many-instance-attributes,too-many-public-methods


@dataclass(frozen=True)
class PyMarkdownScanFailure:
    """
    Class to contain information about a failure reported by one of the rule plugins.
    """

    scan_file: str
    """File that was being scanned when the failure occurred."""
    line_number: int
    """Line number of the triggered rule failure."""
    column_number: int
    """Column number of the triggered rule failure."""
    rule_id: str
    """ID of the rule that was triggered."""
    rule_name: str
    """Name(s) of the rule that was triggered."""
    rule_description: str
    """Longer description of the rule that was triggered."""
    extra_error_information: Optional[str]
    """Optional string providing more information on why the rule was triggered."""

    def partial_equals(self, other: "PyMarkdownScanFailure") -> bool:
        """
        Decide if special fields are the same from both items.
        """
        return (
            self.scan_file == other.scan_file
            and self.line_number == other.line_number
            and self.column_number == other.column_number
            and self.rule_id == other.rule_id
        )


@dataclass(frozen=True)
class PyMarkdownPragmaError:
    """
    Class to encapsulate the information for a pragma error.
    """

    file_path: str
    """Path to the file that contains the improperly constructed pragma."""
    line_number: int
    """Line number where the pragma is contained."""
    pragma_error: str
    """Specific information about the error."""


@dataclass(frozen=True)
class PyMarkdownScanPathResult:
    """
    Result for the scan_path function.
    """

    scan_failures: List[PyMarkdownScanFailure]
    """
    List of zero or more PyMarkdownScanFailure objects.
    """
    pragma_errors: List[PyMarkdownPragmaError]
    """
    List of zero or more PyMarkdownPragmaError objects.
    """


@dataclass(frozen=True)
class PyMarkdownListPathResult:
    """
    Result for the list_path function.
    """

    matching_files: List[str]
    """List of filenames that match the specifications of the requested path."""


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


class _ApiPresentation(MainPresentation):
    """
    Class to provide for the output of the PyMarkdown application.
    """

    def __init__(self) -> None:
        self.pso: List[str] = []
        self.pse: List[str] = []
        self.pragma_errors: List[PyMarkdownPragmaError] = []
        self.scan_failures: List[PyMarkdownScanFailure] = []

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

    # def format_scan_error(
    #     self,
    #     next_file: str,
    #     this_exception: Exception,
    #     show_extended_information: bool = False,
    # ) -> Optional[str]:
    #     """
    #     Format a scan error for display.  Returning a value of None means that
    #     the function has handled any required output.
    #     """
    #     return super().format_scan_error(
    #         next_file, this_exception, show_extended_information
    #     )

    def print_pragma_failure(
        self, scan_file: str, line_number: int, pragma_error: str
    ) -> None:
        """
        Print a failure to compile the pragma.
        """
        self.pragma_errors.append(
            PyMarkdownPragmaError(scan_file, line_number, pragma_error)
        )

    def print_scan_failure(self, scan_failure: PluginScanFailure) -> None:
        """
        Print a scan failure for a specific file and location.
        """
        local_copy = PyMarkdownScanFailure(
            scan_file=scan_failure.scan_file,
            line_number=scan_failure.line_number,
            column_number=scan_failure.column_number,
            rule_id=scan_failure.rule_id,
            rule_name=scan_failure.rule_name,
            rule_description=scan_failure.rule_description,
            extra_error_information=scan_failure.extra_error_information,
        )
        self.scan_failures.append(local_copy)
