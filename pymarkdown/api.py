"""
Create a new instance of the `PyMarkdownApi` class.
"""

import argparse
import os
import tempfile
from dataclasses import dataclass
from typing import Any, List, Optional

from application_file_scanner import ApplicationFileScanner

from pymarkdown.application_logging import ApplicationLogging
from pymarkdown.general.main_presentation import MainPresentation
from pymarkdown.main import PyMarkdownLint
from pymarkdown.plugin_manager.plugin_scan_failure import PluginScanFailure

# pylint: disable=too-many-lines


# pylint: disable=too-many-instance-attributes,too-many-public-methods
class PyMarkdownApi:
    """
    Module to provide for an API to directly communicate with PyMarkdown instead
    of using a command line.

    Args:
        inherit_logging: If True, inherit the logging settings from the calling
            application.  If False, will use the `log_*` functions to specify the
            logging properties.
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
        self.__enable_extension_identifiers: List[str] = []
        self.__set_properties: List[str] = []
        self.__disable_json5_configuration = False
        self.__enable_continue_on_error = False

    # pylint: disable=too-many-arguments
    def scan_path(
        self,
        path_to_scan: str,
        recurse_if_directory: bool = False,
        alternate_extensions: Optional[str] = None,
        exclude_patterns: Optional[List[str]] = None,
        respect_gitignore: bool = False,
    ) -> "PyMarkdownScanPathResult":
        """
        Scan any eligible Markdown files found on the provided path.  For more information,
        check out our User's Guide sections on [Basic Scanning](../user-guide.md#basic-scanning)
        and [Command Line Arguments](../user-guide.md#command-line-arguments).

        Args:
            path_to_scan (str): If `path_to_scan` is a directory, scan within that directory for
                eligible Markdown files.  If `path_to_scan` is a file, determine if the file is
                an eligible Markdown file before proceeding with the scan.
            recurse_if_directory (bool): If `path_to_scan` is a directory and `recurse_if_directory`
                if ``True``, also scan any directories within the specified directory.
            alternate_extensions (str, optional): Optionally specify one or more comma-separated file
                extensions. Files with these file extensions are also considered to be eligible
                files to scan.
            exclude_patterns (List[str], optional): Optionally specify one or more glob-style patterns
                to exclude files or directories from being scanned.
            respect_gitignore (bool): If ``True``, respect any `.gitignore` files found when scanning
                according to standard Git rules.

        Raises:
            PyMarkdownApiArgumentException: If `path_to_scan` is empty or if `alternate_extensions`
                does not contain a valid list of file extensions.  Valid file extensions start with
                a single period character and are followed by one or more ASCII alphanumeric characters.
            PyMarkdownApiNoFilesFoundException: If no eligible files were found.
            PyMarkdownApiException: If some other error was found.

        Returns:
            An instance of `PyMarkdownScanPathResult` containing any scan failures or pragma errors
                encountered when scanning the eligible files on the provided path.

        Examples:
            This example scans a specific Markdown file `file.md` for any
            issues.  Both good results (printing of the two properties of `scan_result`) and
            bad results (printing the exception information) are properly handled.

                from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

                try:
                    scan_result = PyMarkdownApi().scan_path("file.md")
                    print(f"Scan Failures: {scan_result.scan_failures}")
                    print(f"Pragma Errors: {scan_result.pragma_errors}")
                except PyMarkdownApiException as this_exception:
                    print(f"API Exception: {this_exception}", file=sys.stderr)

            By replacing the line with `scan_path` with:

                scan_result = PyMarkdownApi().scan_path("./docs", recurse_if_directory=True)

            the code will now scan for any `*.md` files in the `./docs` directory and in
            any directories under the `./docs` directory.
        """
        self.__verify_string_argument_not_empty("path_to_scan", path_to_scan)

        scan_arguments = self.__build_common_arguments("scan")
        self.__add_common_scan_arguments(
            scan_arguments,
            path_to_scan,
            recurse_if_directory,
            alternate_extensions,
            exclude_patterns=exclude_patterns,
            respect_gitignore=respect_gitignore,
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
            # https://github.com/python/typeshed/issues/8513#issue-1333671093
            return_code = (
                int(this_exception.code) if isinstance(this_exception.code, int) else 99
            )
            if return_code == 1:
                raise PyMarkdownApiNoFilesFoundException(
                    "No matching files found."
                ) from this_exception
        return self.__handle_scan_results(return_code, this_presentation)

    # pylint: enable=too-many-arguments

    def scan_string(
        self,
        string_to_scan: str,
    ) -> "PyMarkdownScanPathResult":
        """
        Scan the specified string as a Markdown document.

        Args:
            string_to_scan (str): String to interpret as a Markdown document.

        Raises:
            PyMarkdownApiArgumentException: If `string_to_scan` is empty.
            PyMarkdownApiException: If some other error was found.

        Returns:
            An instance of `PyMarkdownScanPathResult` containing any scan failures or pragma errors
                encountered when scanning the Markdown document.

        Examples:
            This example is a simplified form of the `scan_path` example that accepts a
            string to scan instead

                from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

                markdown_string = \"# Markdown\\n\\nIs cool!\\n\"

                try:
                    scan_result = PyMarkdownApi().scan_string(markdown_string)
                    print(f"Scan Failures: {scan_result.scan_failures}")
                    print(f"Pragma Errors: {scan_result.pragma_errors}")
                except PyMarkdownApiException as this_exception:
                    print(f"API Exception: {this_exception}", file=sys.stderr)
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

    # pylint: disable=too-many-arguments
    def fix_path(
        self,
        path_to_scan: str,
        recurse_if_directory: bool = False,
        alternate_extensions: Any = None,
        exclude_patterns: Optional[List[str]] = None,
        respect_gitignore: bool = False,
    ) -> "PyMarkdownFixResult":
        """
        Fix any eligible Markdown files found on the provided path that have scan failures that
        can be automatically fixed.

        Args:
            path_to_scan (str): If ``path_to_scan`` is a directory, scan within that directory for
                eligible Markdown files.  If `path_to_scan` is a file, determine if the file is
                an eligible Markdown file before proceeding with the scan and fix.
            recurse_if_directory (bool): If `path_to_scan` is a directory and `recurse_if_directory`
                if ``True``, also scan any directories within the specified directory.
            alternate_extensions (str, optional): Optionally specify one or more comma-separated file
                extensions. Files with these file extensions are also considered to be eligible
                files to scan.
            exclude_patterns (List[str], optional): Optionally specify one or more glob-style patterns
                to exclude files or directories from being scanned.
            respect_gitignore (bool): If ``True``, respect any `.gitignore` files found when scanning
                according to standard Git rules.

        Raises:
            PyMarkdownApiArgumentException: If `path_to_scan` is empty or if `alternate_extensions`
                does not contain a valid list of file extensions.  Valid file extensions start with
                a single period character and are followed by one or more ASCII alphanumeric characters.
            PyMarkdownApiNoFilesFoundException: If no eligible files were found.
            PyMarkdownApiException: If some other error was found.

        Returns:
            An instance containing any eligible files that were fixed.

        Examples:
            This function is syntactically equivalent to calling the `scan_path` function
            except for its return value.

                from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

                try:
                    fix_result = PyMarkdownApi().fix_path("file.md")
                    print(f"Fixed file paths: {fix_result.files_fixed}")
                except PyMarkdownApiException as this_exception:
                    print(f"API Exception: {this_exception}", file=sys.stderr)
        """
        self.__verify_string_argument_not_empty("path_to_scan", path_to_scan)

        scan_arguments = self.__build_common_arguments("fix")
        self.__add_common_scan_arguments(
            scan_arguments,
            path_to_scan,
            recurse_if_directory,
            alternate_extensions,
            exclude_patterns=exclude_patterns,
            respect_gitignore=respect_gitignore,
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
            # https://github.com/python/typeshed/issues/8513#issue-1333671093
            return_code = (
                int(this_exception.code) if isinstance(this_exception.code, int) else 99
            )
        return self.__handle_fix_results(return_code, this_presentation)

    # pylint: enable=too-many-arguments

    def fix_string(
        self,
        string_to_scan: str,
    ) -> "PyMarkdownFixStringResult":
        """
        Scan the specified string as a Markdown document and apply any eligible fixes.

        Args:
            string_to_scan (str): String to interpret as a Markdown document.

        Raises:
            PyMarkdownApiArgumentException: If `string_to_scan` is empty.
            PyMarkdownApiException: If some other error was found.

        Returns:
            An instance containing the original document with any fixes applied.

        Examples:
            This function is syntactically equivalent to calling the `scan_string` function
            except for its return value.

                from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

                markdown_string = \"# Markdown\\n\\nIs cool!\\n\"

                try:
                    fix_result = PyMarkdownApi().fix_string(markdown_string)
                    print(f"Applied fixes?  {fix_result.was_fixed}")
                    print(f"Fixed Markdown: {fix_result.fixed_file}")
                except PyMarkdownApiException as this_exception:
                    print(f"API Exception: {this_exception}", file=sys.stderr)
        """
        self.__verify_string_argument_not_empty("string_to_scan", string_to_scan)

        temp_file = None
        try:
            with tempfile.NamedTemporaryFile(
                "wt", suffix=".md", encoding="utf-8", delete=False
            ) as temp_file:
                temp_file.write(string_to_scan)

            scan_arguments = self.__build_common_arguments("fix")
            scan_arguments.append(temp_file.name)

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
                    int(this_exception.code)
                    if isinstance(this_exception.code, int)
                    else 99
                )
            fix_result = self.__handle_fix_results(return_code, this_presentation)
            with open(temp_file.name, "rt", encoding="utf-8") as fixed_file:
                return PyMarkdownFixStringResult(
                    bool(fix_result.files_fixed), fixed_file.read()
                )
        finally:
            if temp_file and os.path.isfile(temp_file.name):  # pragma: no cover
                os.remove(temp_file.name)

    # pylint: disable=too-many-arguments
    def list_path(
        self,
        path_to_scan: str,
        recurse_if_directory: bool = False,
        alternate_extensions: str = "",
        exclude_patterns: Optional[List[str]] = None,
        respect_gitignore: bool = False,
    ) -> "PyMarkdownListPathResult":
        """
        List any eligible files found when scanning the specified path for eligible markdown files.
        This function is provided for debugging situations to provide confidence that one or more
        Markdown files are indeed being scanned by PyMarkdown.

        Args:
            path_to_scan (str): If ``path_to_scan`` is a directory, scan within that directory for
                eligible Markdown files.  If `path_to_scan` is a file, determine if the file is
                an eligible Markdown file.
            recurse_if_directory (bool): If `path_to_scan` is a directory and `recurse_if_directory`
                if ``True``, also scan any directories within the specified directory.
            alternate_extensions (str, optional): Optionally specify one or more comma-separated file
                extensions. Files with these file extensions are also considered to be eligible
                files to scan.
            exclude_patterns (List[str], optional): Optionally specify one or more glob-style patterns
                to exclude files or directories from being scanned.
            respect_gitignore (bool): If ``True``, respect any `.gitignore` files found when scanning
                according to standard Git rules.

        Raises:
            PyMarkdownApiArgumentException: If `path_to_scan` is empty or if `alternate_extensions`
                does not contain a valid list of file extensions.  Valid file extensions start with
                a single period character and are followed by one or more ASCII alphanumeric characters.
            PyMarkdownApiNoFilesFoundException: If no eligible files were found.
            PyMarkdownApiException: If some other error was found.

        Returns:
            An instance containing eligible Markdown files that would have normally be scanned.

        Examples:
            This example generates a list of the files that PyMarkdown will scan if the `scan_path`
            function is invoked with the same parameters.

                from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

                try:
                    scan_result = PyMarkdownApi().list_path("./docs", recurse_if_directory=True)
                    print(scan_result.matching_files)
                except PyMarkdownApiException as this_exception:
                    print(f"API Exception: {this_exception}", file=sys.stderr)
        """
        self.__verify_string_argument_not_empty("path_to_scan", path_to_scan)

        scan_arguments = self.__build_common_arguments("scan")
        scan_arguments.append("--list-files")
        self.__add_common_scan_arguments(
            scan_arguments,
            path_to_scan,
            recurse_if_directory,
            alternate_extensions,
            exclude_patterns=exclude_patterns,
            respect_gitignore=respect_gitignore,
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
            self.__generate_scan_exception(this_presentation)
        return PyMarkdownListPathResult(this_presentation.pso[0].split("\n"))

    # pylint: enable=too-many-arguments

    @property
    def application_version(self) -> str:
        """
        Report on the application version.

        Returns:
            The current application version.

        Examples:
            This function queries the current version of PyMarkdown.

                from pymarkdown.api import PyMarkdownApi

                print(f"PyMarkdown version = {PyMarkdownApi().application_version}")
        """
        return PyMarkdownLint().application_version

    @property
    def interface_version(self) -> int:
        """
        Report on the interface version.

        Returns:
            The current plugin interface version.

        Examples:
            This function queries the current version of this API.

                from pymarkdown.api import PyMarkdownApi

                print(f"PyMarkdown API version = {PyMarkdownApi().interface_version}")
        """
        return PyMarkdownApi.__INTERFACE_VERSION

    def disable_rule_by_identifier(self, rule_identifier: str) -> "PyMarkdownApi":
        """
        Disable a single rule by one of its identifiers.

        Args:
            rule_identifier (str): Identifier for the rule to disable.

        Raises:
            PyMarkdownApiArgumentException: If `rule_identifier` is empty.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function disables a single rule by one of its identifiers.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().disable_rule_by_identifier("md031").scan_path("file.md")
        """
        self.__verify_string_argument_not_empty("rule_identifier", rule_identifier)

        self.__disable_rule_identifiers.append(rule_identifier)
        return self

    def enable_rule_by_identifier(self, rule_identifier: str) -> "PyMarkdownApi":
        """
        Enable a single rule by one of its identifiers.

        Args:
            rule_identifier (str): Identifier for the rule to enable.

        Raises:
            PyMarkdownApiArgumentException: If `rule_identifier` is empty.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function enables a single rule by one of its identifiers.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().enable_rule_by_identifier("md031").scan_path("file.md")
        """
        self.__verify_string_argument_not_empty("rule_identifier", rule_identifier)

        self.__enable_rule_identifiers.append(rule_identifier)
        return self

    def enable_extension_by_identifier(
        self, extension_identifier: str
    ) -> "PyMarkdownApi":
        """
        Enable a single extension by its identifier.

        Args:
            extension_identifier (str): Identifier for the extension to enable.

        Raises:
            PyMarkdownApiArgumentException: If `extension_identifier` is empty.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function enables a single extension by its identifier.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().enable_extension_by_identifier("front-matter").scan_path("file.md")
        """
        self.__verify_string_argument_not_empty(
            "extension_identifier", extension_identifier
        )

        self.__enable_extension_identifiers.append(extension_identifier)
        return self

    def configuration_file_path(self, path_to_config_file: str) -> "PyMarkdownApi":
        """
        Set the path to the configuration file to use.

        Args:
            path_to_config_file (str): Path to the configuration file to use.

        Raises:
            PyMarkdownApiArgumentException: If `path_to_config_file` is empty.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function specifies a file containing configuration information.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().path_to_config_file("pymarkdown.cfg").scan_path("file.md")
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

        Args:
            property_name (str): Full hierarchical name of the property to set.
            property_value (bool): `True` or `False` boolean value to set the property to.

        Raises:
            PyMarkdownApiArgumentException: If `property_name` is empty or if `property_value` is not a `bool` value.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function sets a boolean value for a specific configuration item.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().set_boolean_property("plugins.md007.enabled", True).scan_path("file.md")
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

        Args:
            property_name (str): Full hierarchical name of the property to set.
            property_value (int): Integer value to set the property to.

        Raises:
            PyMarkdownApiArgumentException: If `property_name` is empty or if `property_value` is not an `int` value.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function sets a integer value for a specific configuration item.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().set_integer_property("plugins.md007.code_block_line_length", 160).scan_path("file.md")
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

        Args:
            property_name (str): Full hierarchical name of the property to set.
            property_value (str): String value to set the property to.

        Raises:
            PyMarkdownApiArgumentException: If `property_name` is empty or if `property_value` is not an `str` value.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function sets a string value for a specific configuration item.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().set_string_property("plugins.heading-style-h1.style", "consistent").scan_path("file.md")
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
        the property_value parameter is translated into a string.

        If at all possible, the other three `set_x_property` functions should be used
        as they ensure that the correct type of value is set as the configuration item
        value.  This function translated ANY value for the `property_value` argument
        into a `str` before setting it as the configuration item value.

        Args:
            property_name (str): Full hierarchical name of the property to set.
            property_value (Any): Value to set the property to after applying a string
                transformation to the value.

        Raises:
            PyMarkdownApiArgumentException: If `property_name` is empty.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function sets a value, translated into a string, for a specific configuration item.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().set_property("plugins.heading-style-h1.style", 1).scan_path("file.md")
        """
        self.__verify_string_argument_not_empty("property_name", property_name)

        self.__set_properties.append(f"{property_name}={str(property_value)}")
        return self

    def enable_strict_configuration(self) -> "PyMarkdownApi":
        """
        Enable strict configuration for any requested properties, either through configuration files or manual setting.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function enforces strict adherence to configuration requirements.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().enable_strict_configuration().scan_path("file.md")
        """
        self.__enable_strict_configuration = True
        return self

    def log_debug_and_above(self) -> "PyMarkdownApi":
        """
        Enable logging for the DEBUG level and above.

        Raises:
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function sets the logging level for PyMarkdown to anything that
            is at `DEBUG` logging level or above.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().log_debug_and_above().scan_path("file.md")
        """
        return self.log(ApplicationLogging.log_level_debug)

    def log_info_and_above(self) -> "PyMarkdownApi":
        """
        Enable logging for the INFO level and above.

        Raises:
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function sets the logging level for PyMarkdown to anything that
            is at `INFO` logging level or above.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().log_info_and_above().scan_path("file.md")
        """
        return self.log(ApplicationLogging.log_level_info)

    def log_warning_and_above(self) -> "PyMarkdownApi":
        """
        Enable logging for the WARN level and above.

        Raises:
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function sets the logging level for PyMarkdown to anything that
            is at `WARNING` logging level or above.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().log_warning_and_above().scan_path("file.md")
        """
        return self.log(ApplicationLogging.log_level_warning)

    def log_error_and_above(self) -> "PyMarkdownApi":
        """
        Enable logging for the ERROR level and above.

        Raises:
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function sets the logging level for PyMarkdown to anything that
            is at `ERROR` logging level or above.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().log_error_and_above().scan_path("file.md")
        """
        return self.log(ApplicationLogging.log_level_error)

    def log_critical_and_above(self) -> "PyMarkdownApi":
        """
        Enable logging for the CRITICAL level and above.

        Raises:
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function sets the logging level for PyMarkdown to anything that
            is at `CRITICAL` logging level or above.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().log_critical_and_above().scan_path("file.md")
        """
        return self.log(ApplicationLogging.log_level_critical)

    def log(self, log_level: str) -> "PyMarkdownApi":
        """
        Set the logging level using a string value.

        Args:
            log_level (str): One of "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG".

        Raises:
            PyMarkdownApiArgumentException: If `log_level` is not one of the allowed values.
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function sets the logging level for PyMarkdown to anything that
            is at `INFO` logging level or above.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().log("INFO").scan_path("file.md")
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

        Args:
            log_file_path (str): Path to the file to write the logs to.

        Raises:
            PyMarkdownApiArgumentException: If `log_file_path` is empty.
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function writes any logging messages to the specified file.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().log_to_file("file.log").scan_path("file.md")
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

        Args:
            path_to_plugin (str): Path to an additional plugin to load.

        Raises:
            PyMarkdownApiArgumentException: If `path_to_plugin` is empty.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function informs PyMarkdown to use a new plugin.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().add_plugin_path("my_plugin.py").scan_path("file.md")
        """
        self.__verify_string_argument_not_empty("path_to_plugin", path_to_plugin)

        self.__plugin_paths_to_add.append(path_to_plugin)
        return self

    def enable_stack_trace(self) -> "PyMarkdownApi":
        """
        Enable the reporting of stack traces for any exceptions caught by the API.
        If this modifier is present, additional information will be recorded as
        to the exact nature of any reported exception.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function enable stack trace support in case of a raised exception.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().enable_stack_trace().scan_path("file.md")
        """
        self.__enable_stack_trace = True
        return self

    def disable_json5_configuration(self) -> "PyMarkdownApi":
        """
        Disable the use of the JSON5 parser for configuration files, instead
        using the base json parser from the Python standard library.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function disables the use of the JSON5 parser for configuration files.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().disable_json5_configuration().scan_path("file.md")
        """
        self.__disable_json5_configuration = True
        return self

    def enable_continue_on_error(self) -> "PyMarkdownApi":
        """
        Enable the scanning of multiple files to continue, even if some of the files
        have critical errors.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function disables the use of the JSON5 parser for configuration files.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().disable_json5_configuration().scan_path("file.md")
        """
        self.__enable_continue_on_error = True
        return self

    def __handle_scan_results(
        self, return_code: int, this_presentation: "_ApiPresentation"
    ) -> "PyMarkdownScanPathResult":
        assert (
            not this_presentation.pso
        ), "should not display for scan_path, but for ext ops and plugin ops"
        if return_code != 0 and not self.__enable_continue_on_error:
            self.__generate_scan_exception(this_presentation)
        return PyMarkdownScanPathResult(
            this_presentation.scan_failures,
            this_presentation.pragma_errors,
            this_presentation.pse,
        )

    def __handle_fix_results(
        self, return_code: int, this_presentation: "_ApiPresentation"
    ) -> "PyMarkdownFixResult":
        assert (
            not this_presentation.pso
        ), "should not display for scan_path, but for ext ops and plugin ops"
        if return_code not in [0, 1, 3] and not self.__enable_continue_on_error:
            raise PyMarkdownApiException(this_presentation.pse[-1].strip("\n"))
        return PyMarkdownFixResult(this_presentation.files_fixed, this_presentation.pse)

    def __generate_scan_exception(self, this_presentation: "_ApiPresentation") -> None:
        if not this_presentation.pse:
            return
        if this_presentation.pse[-1] == "\n\nNo matching files found.":
            raise PyMarkdownApiNoFilesFoundException("No matching files found.")
        raise PyMarkdownApiException(this_presentation.pse[-1].strip("\n"))

    # pylint: disable=too-many-arguments
    def __add_common_scan_arguments(
        self,
        scan_arguments: List[str],
        path_to_scan: str,
        recurse_if_directory: bool,
        alternate_extensions: Optional[str],
        exclude_patterns: Optional[List[str]] = None,
        respect_gitignore: bool = False,
    ) -> None:
        if recurse_if_directory:
            scan_arguments.append("--recurse")

        if respect_gitignore:
            scan_arguments.append("--respect-gitignore")

        if alternate_extensions:
            self.__verify_string_argument_alternate_extensions(
                "alternate_extensions", alternate_extensions
            )
            scan_arguments.extend(("-ae", alternate_extensions))

        if exclude_patterns:
            for next_pattern in exclude_patterns:
                scan_arguments.extend(("--exclude", next_pattern))

        scan_arguments.append(path_to_scan)

    # pylint: enable=too-many-arguments

    def __build_common_arguments(self, action_to_invoke: str) -> List[str]:

        # Note: `--return-code-scheme` is not included as a configurable option
        #       as the api requires explicit information about what happened.
        common_arguments: List[str] = ["--return-code-scheme", "explicit"]

        if self.__disable_json5_configuration:
            common_arguments.append("--no-json5")
        if self.__enable_continue_on_error:
            common_arguments.append("--continue-on-error")
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
        if self.__enable_extension_identifiers:
            common_arguments.extend(
                ("--enable-extensions", ",".join(self.__enable_extension_identifiers))
            )

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

    Each instance of this class specifies a single scan failure that was encountered
    within the specified Markdown document.  Using the encapsulated fields, the following
    pieces of information about that scan failure can be determined:

    - the location where the scan failure occurred
    - the specific location within that location that triggered the scan failure
    - the exact rule that was triggered

    Optionally, depending on the rule, extra information may be present in the
    `extra_error_information` field.  This information is rule-dependent and is
    intended to provide extra clarity on why the rule was triggered.

    For more information consult the [Rule Failure Format](../user-guide.md#rule-failure-format)
    section of our User's Guide.

    Attributes:
        scan_file (str): Path to the file containing the failure.
        line_number (int): Line number of the triggered rule failure.
        column_number (int): Column number of the triggered rule failure.
        rule_id (str): ID of the rule that was triggered.
        rule_name (str): Name(s) of the rule that was triggered.
        rule_description (str): Longer description of the rule that was triggered.
        extra_error_information (Optional[str]): String providing more information on why the rule was triggered.
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

    Each instance of this class specifies a single pragma failure that was encountered
    within the specified Markdown document.  Using the encapsulated fields, the following
    pieces of information about that pragma error can be determined:

    - the location where the pragma error occurred
    - the specific location within that location that triggered the pragma error
    - specific information on why PyMarkdown generated the pragma error

    More information on Pragmas and
    their use are available [here](../user-guide.md#pragma-extension).

    Attributes:
        file_path (str): Path to the file that contains the improperly constructed pragma.
        line_number (int): Line number where the pragma is contained.
        pragma_error (str): Specific information about the error.
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
    Result for the `scan_path` and `scan_string` functions.

    As both `PyMarkdownScanFailure` objects and `PyMarkdownPragmaError` objects
    contain location and additional failure/error information, this result
    object is a simple pair of lists containing failure information.

    Attributes:
        scan_failures (List[PyMarkdownScanFailure]): Zero or more `PyMarkdownScanFailure` objects.
        pragma_errors (List[PyMarkdownPragmaError]): Zero or more `PyMarkdownPragmaError` objects.
    """

    scan_failures: List[PyMarkdownScanFailure]
    """
    List of zero or more `PyMarkdownScanFailure` objects.
    """
    pragma_errors: List[PyMarkdownPragmaError]
    """
    List of zero or more `PyMarkdownPragmaError` objects.
    """
    critical_errors: List[str]
    """
    List of zero or more critical errors that were encountered during the scan. Only
    set if `enable_continue_on_error` was set when the `scan_path` or `scan_string`
    function was invoked.  If no critical errors were encountered, this list is empty.
    """


@dataclass(frozen=True)
class PyMarkdownFixResult:
    """
    Result for the fix_path function.

    The only information that PyMarkdown provides about scanned and fixed
    documents are the names of the documents that were fixed.  As such, this result
    simply provides those same Markdown file names.

    Attributes:
        files_fixed (List[str]): List of zero or more files that were fixed.
    """

    files_fixed: List[str]
    """
    List of zero or more files that were fixed.
    """
    critical_errors: List[str]
    """
    List of zero or more critical errors that were encountered during the fixing of the files. Only
    set if `enable_continue_on_error` was set when the `fix_path` function was invoked.
    If no critical errors were encountered, this list is empty.
    """


@dataclass(frozen=True)
class PyMarkdownFixStringResult:
    """
    Result for the fix_string function.

    Focusing on a singular Markdown document, this object returns an indication
    of whether fixes were applied along with the fixed document.

    Attributes:
        was_fixed (bool): Whether the string, interpretted as a Markdown document, was fixed.
        fixed_file (str): String that was passed into the `fix_string` function, with any fixes applied to it.
    """

    was_fixed: bool
    """
    Whether the string was fixed.
    """

    fixed_file: str
    """
    String that was passed into the `fix_string` function, with any fixes applied
    to it.
    """


@dataclass(frozen=True)
class PyMarkdownListPathResult:
    """
    Result for the list_path function.

    This object returns a list of files that PyMarkdown understands to be eligible
    for scanning, without having scanned those files.

    Attributes:
        matching_files (List[str]): List of filenames that match the specifications of the requested path.
    """

    matching_files: List[str]
    """List of filenames that match the specifications of the requested path."""


class PyMarkdownApiException(Exception):
    """
    Class to provide for an exception that is thrown by the API layer.

    This base PyMarkdown application exception is explicitly thrown when a unexpected error occurs that
    is not categorized as one of the other application exceptions.  Where possible, child classes of
    this class should be used to provide more specific information regarding the nature of the
    exception.

    Attributes:
        reason (str): Reported reason why the action failed.
    """

    def __init__(self, reason: str) -> None:
        self.__reason = reason

    @property
    def reason(self) -> str:
        """
        Reported reason why the action failed.
        """
        return self.__reason


class PyMarkdownApiNotSupportedException(PyMarkdownApiException):
    """
    Class to provide for an exception that a given situation is not supported.

    The most frequent raising of this exception is when the `PyMarkdownApi` instance
    is created with the *inherit_logging* set to `True`, followed by a call to
    one of the functions that alters the logging behavior of the application.

    Attributes:
        reason (str): Reported reason why the action failed.
    """


class PyMarkdownApiArgumentException(PyMarkdownApiException):
    """
    Class to provide for an argument that an exception is not valid.

    This exception is raised when an argument to a function falls outside of the
    expected behavior for that function.  This can mean that a `str` parameter
    is unexpectedly empty or that the parameter is not one of the allowed values
    for that parameter.

    Attributes:
        reason (str): Reported reason why the action failed.
        argument_name(str): Name of the argument that caused this exception to be raised.
    """

    def __init__(self, argument_name: str, reason: str) -> None:
        super().__init__(reason)
        self.__argument_name = argument_name

    @property
    def argument_name(self) -> str:
        """
        Name of the argument that caused this exception to be raised.
        """
        return self.__argument_name


class PyMarkdownApiNoFilesFoundException(PyMarkdownApiException):
    """
    Class to provide for an exception that the invoked API was not able to find at least one file to process.

    This is raised as an exception if at least one file to scan or fix is
    not encountered.  As the PyMarkdown application is a scanning application,
    not finding a single Markdown document to scan is typically an exceptional
    case.

    Attributes:
        reason (str): Reported reason why the action failed.
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
        self.files_fixed: List[str] = []

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

    def print_fix_message(self, file_fixed: str) -> None:
        """
        Print a message indicating that a given file has been fixed.
        """
        self.files_fixed.append(file_fixed)
