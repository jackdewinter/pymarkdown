# docvet: ignore[missing-examples, missing-cross-references]
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
class PyMarkdownApi:  # docvet: ignore[missing-examples]
    """
    Module to provide for an API to directly communicate with PyMarkdown instead
    of using a command line.

    Args:
        inherit_logging: If True, inherit the logging settings from the calling
            application.  If False, will use the `log_*` functions to specify the
            logging properties.
    Attributes:
        __inherit_logging (bool): Kept version of the `inherit_logging` parameter.
    """

    __INTERFACE_VERSION = 1

    def __init__(self, inherit_logging: bool = False) -> None:
        """
        Initialize a new instance of the PyMarkdownApi class.
        """
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
        *Scan a provided path for eligible Markdown files and check them for rule violations and pragma errors.*

        This is the API interface equivalent for the [`pymarkdown scan`](../user-guide.md#basic-scanning) command line action.

        This method is the second step in the recommended End-to-End Workflow. See `list_path` for how to determine eligible files.

        See the [End-to-End Workflow](./pymarkdownapi.md#recommended-end-to-end-workflow) in the class documentation for the recommended pattern of using this method to scan for rule failures.

        Args:
            path_to_scan: The path to scan. Can be a file, a directory, or a glob pattern.
                If a relative path is provided, it is resolved against the current working directory.
            recurse_if_directory: If `path_to_scan` is a directory, setting this to `True`
                includes all subdirectories in the scan.
            alternate_extensions: An optional comma-separated list of file extensions to scan.
                If not `None` and not an empty string, this list **replaces** the default `.md` extension entirely.
                Defaults to `.md` if `None` or an empty string is passed.
            exclude_patterns: If provided, glob patterns to exclude files or directories.
                Patterns are resolved relative to the **current working directory**, not the `path_to_scan` parameter.
                Exclusions are determined by the union of patterns in `exclude_patterns` and `.gitignore`
                files (if `respect_gitignore` is `True`). If a file matches any pattern in either list,
                it is excluded from the scan.
            respect_gitignore: If `True`, respect any `.gitignore` files found when scanning
                according to standard Git rules.

        Returns:
            A [PyMarkdownScanPathResult][pymarkdown.api.PyMarkdownScanPathResult] object if the scan completes without raising an exception.

                - `scan_failures`: A list of [PyMarkdownScanFailure][pymarkdown.api.PyMarkdownScanFailure] objects. This list is empty if no rule
                  violations were found. Each object in the list is a rule failure found in an eligible file.
                - `pragma_errors`: A list of [PyMarkdownPragmaError][pymarkdown.api.PyMarkdownPragmaError] objects. This list is empty if no pragma
                  issues were found. Each object in the list is a failure to parse a Pragma command embedded within an eligible file.
                - `critical_errors`: Present only if `enable_continue_on_error` is enabled. If disabled, critical errors result in an exception being raised, and this list is never populated in the returned object.

        Raises:
            PyMarkdownApiArgumentException: If `path_to_scan` is empty or if `alternate_extensions`
                does not contain a valid list of file extensions.  Valid file extensions start with
                a single period character and are followed by one or more ASCII alphanumeric characters.
            PyMarkdownApiNoFilesFoundException: If no eligible files were found.
            PyMarkdownApiException: Raised for unexpected internal errors, such as invalid configuration files, plugin loading failures, or unhandled I/O errors.
                **Note on `enable_continue_on_error`**: If this option is enabled, certain **System Errors** are not raised as exceptions. Instead, they are collected in the `critical_errors` list of the returned [PyMarkdownScanPathResult][pymarkdown.api.PyMarkdownScanPathResult] object.

        Examples:
            ##### Recommended Workflow: Scanning for Violations.

            This example demonstrates the core scanning step of the recommended workflow.
            It assumes you have already discovered your files using `list_path` with the same
            path arguments. This ensures that the configuration and file targeting are consistent.

            ```python
            # SNIPPET: Part 2 of the End-to-End Workflow
            # Assumes: api and path are defined from the previous step.

            try:
                # IMPORTANT: Use the EXACT same path and recurse arguments as list_path
                scan_result = api.scan_path(path, recurse_if_directory=recurse)
            except PyMarkdownApiException as e:
                print(f"Scan failed: {e}")
                return

            if scan_result.scan_failures:
                print(f"Found {len(scan_result.scan_failures)} issues.")
            ```
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

        this_presentation = PyMarkdownApi.ApiPresentation()
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
        *Scan a provided Markdown string for rule violations and pragma errors.*

        This is the API interface equivalent for scanning a Markdown document provided via standard input (stdin),
        similar to the [`pymarkdown scan-stdin`](../user-guide.md#scanning-from-standard-input) command line action.

        This method is the alternative to `scan_path` for cases where the Markdown content is available as a string
        rather than a file on disk. It is typically used if the actual scanning content is provided dynamically or simply as a standalone check for generated Markdown strings.

        Args:
            string_to_scan: The Markdown string to scan.
                This string is interpreted directly as the content of a Markdown document.

        Returns:
            A [PyMarkdownScanPathResult][pymarkdown.api.PyMarkdownScanPathResult] object if the scan completes without raising an exception.

                - `scan_failures`: A list of [PyMarkdownScanFailure][pymarkdown.api.PyMarkdownScanFailure] objects. This list is empty if no rule
                  violations were found. Each object in the list is a rule failure found in the provided string.
                - `pragma_errors`: A list of [PyMarkdownPragmaError][pymarkdown.api.PyMarkdownPragmaError] objects. This list is empty if no pragma
                  issues were found. Each object in the list is a failure to parse a Pragma command embedded within the provided string.
                - `critical_errors`: Present only if `enable_continue_on_error` is enabled. If disabled, critical errors result in an exception being raised, and this list is never populated in the returned object.

        Raises:
            PyMarkdownApiArgumentException: If `string_to_scan` is empty.
            PyMarkdownApiException: Raised for unexpected internal errors, such as invalid configuration files, plugin loading failures, or unhandled processing errors.
                **Note on `enable_continue_on_error`**: If this option is enabled, certain **System Errors** are not raised as exceptions. Instead, they are collected in the `critical_errors` list of the returned [PyMarkdownScanPathResult][pymarkdown.api.PyMarkdownScanPathResult] object.

        Examples:
            ##### Scanning a String for Violations.

            This example demonstrates scanning a Markdown string directly without needing a file path.

            ```python
            from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

            markdown_content = \"\"\"# Header

            This is a paragraph with some text.
            \"\"\"

            try:
                scan_result = api.scan_string(markdown_content)
            except PyMarkdownApiException as e:
                print(f"Scan failed: {e}")
                return

            if scan_result.scan_failures:
                print(f"Found {len(scan_result.scan_failures)} issues.")
            else:
                print("All clear!")
            ```
        """
        self.__verify_string_argument_not_empty("path_to_scan", string_to_scan)

        scan_arguments = self.__build_common_arguments("scan-stdin")

        this_presentation = PyMarkdownApi.ApiPresentation()
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
        alternate_extensions: Optional[str] = None,
        exclude_patterns: Optional[List[str]] = None,
        respect_gitignore: bool = False,
    ) -> "PyMarkdownFixResult":
        """
        *Scans a provided path for eligible Markdown files and applies automatic fixes for any rule violations that have auto-fix capabilities.*

        This is the API interface equivalent for the [`pymarkdown fix`](../user-guide.md#basic-fixing) command line action.

        This method is typically the final step in the End-to-End Workflow, applied after identifying issues via `scan_path`.

        See the [End-to-End Workflow](./pymarkdownapi.md#recommended-end-to-end-workflow) in the class documentation for the recommended pattern of using this method to fix any rule violations for plugin rules that support the auto-fix capability.

        Note: This method **permanently modifies the source files in place**. Automatic fixing will only be applied for rule plugins supporting the auto-fix capability.

        Args:
            path_to_scan: The path to scan. Can be a file, a directory, or a glob pattern.
                If a relative path is provided, it is resolved against the current working directory.
            recurse_if_directory: If `path_to_scan` is a directory, setting this to `True`
                includes all subdirectories in the scan.
            alternate_extensions: An optional comma-separated list of file extensions to scan.
                If not `None` and not an empty string, this list **replaces** the default `.md` extension entirely.
                Defaults to `.md` if `None` or an empty string is passed.
            exclude_patterns: If provided, glob patterns to exclude files or directories.
                Patterns are resolved relative to the **current working directory**, not the `path_to_scan` parameter.
                Exclusions are determined by the union of patterns in `exclude_patterns` and `.gitignore`
                files (if `respect_gitignore` is `True`). If a file matches any pattern in either list,
                it is excluded from the scan.
            respect_gitignore: If `True`, respect any `.gitignore` files found when scanning
                according to standard Git rules.

        Returns:
            A [PyMarkdownFixResult][pymarkdown.api.PyMarkdownFixResult] object containing **only** the files that were successfully modified and written to disk, along with any critical errors encountered.

                - `files_fixed`: A list of strings containing the paths of files that were modified and written to disk. Files that were scanned but had no auto-fixable issues, or where all violations were non-auto-fixable, are not included in this list.
                - `critical_errors`: Present only if `enable_continue_on_error` is enabled. If disabled, critical errors result in an exception being raised, and this list is never populated in the returned object.

        Raises:
            PyMarkdownApiArgumentException: If `path_to_scan` is empty or if `alternate_extensions`
                does not contain a valid list of file extensions.  Valid file extensions start with
                a single period character and are followed by one or more ASCII alphanumeric characters.
            PyMarkdownApiNoFilesFoundException: If no eligible files were found.
            PyMarkdownApiException: Raised for unexpected internal errors, such as invalid configuration files, plugin loading failures, or unhandled I/O errors.
                **Note on `enable_continue_on_error`**: If this option is enabled, certain **System Errors** are not raised as exceptions. Instead, they are collected in the `critical_errors` list of the returned [PyMarkdownFixResult][pymarkdown.api.PyMarkdownFixResult] object.

        Examples:
            ##### Recommended Workflow: Fixing Issues.

            This example demonstrates the final step in the recommended workflow: applying automatic fixes.
            It assumes you have already discovered files with `list_path` and scanned them with `scan_path`
            (see those docstrings for earlier steps). This ensures that the configuration and file targeting
            are consistent between the scan and fix operations.

            ```python
            # SNIPPET: Part 3 of the End-to-End Workflow
            # Assumes: api and path are defined from the previous steps.

            try:
                # IMPORTANT: Use the EXACT same path and recurse arguments as list_path/scan_path
                fix_result = api.fix_path(path, recurse_if_directory=recurse)
            except PyMarkdownApiException as e:
                print(f"Fix failed: {e}")
                return

            if fix_result.files_fixed:
                print(f"Fixed: {fix_result.files_fixed}")
            ```
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

        this_presentation = PyMarkdownApi.ApiPresentation()
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
        *Scan a provided Markdown string and apply any eligible automatic fixes.*

        This is the API interface equivalent of:

        - writing the provided `string_to_scan` contents to a temporary file
        - applying a the `pymarkdown fix ` command line to the temporary file
        - reading the fixed contents of the temporary file into the `fixed_file` attribute of the [PyMarkdownFixStringResult][pymarkdown.api.PyMarkdownFixStringResult] object

        This method is the alternative to `fix_path` for cases where the Markdown content is available as a string rather than a file on disk. It allows for programmatic fixing of generated or dynamically created Markdown content.

        Note: This method **does not modify the original string argument passed in**. Instead, it returns a result object containing the fixed string content in memory.

        Args:
            string_to_scan: The Markdown string to scan and fix.
                This string is interpreted directly as the content of a Markdown document.

        Returns:
            A [PyMarkdownFixStringResult][pymarkdown.api.PyMarkdownFixStringResult] object containing:

                - `was_fixed`: A boolean indicating whether any fixes were applied to the document.
                - `fixed_file`: The Markdown string content with any eligible fixes applied. If no fixes were applied, this is identical to the input `string_to_scan`.

        Raises:
            PyMarkdownApiArgumentException: If `string_to_scan` is empty.
            PyMarkdownApiException: Raised for unexpected internal errors, such as invalid configuration files, plugin loading failures, or unhandled processing errors.

        Examples:
            ##### Fixing a String.

            This example demonstrates fixing a Markdown string directly.

            ```python
            from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

            markdown_content = \"\"\"# Header

            Paragraph with some text.
            \"\"\"

            try:
                fix_result = api.fix_string(markdown_content)
            except PyMarkdownApiException as e:
                print(f"Fix failed: {e}")
                return

            if fix_result.was_fixed:
                print("Fixes were applied.")
                print(fix_result.fixed_file)
            else:
                print("No fixes needed.")
            ```
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

            this_presentation = PyMarkdownApi.ApiPresentation()
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
        alternate_extensions: Optional[str] = None,
        exclude_patterns: Optional[List[str]] = None,
        respect_gitignore: bool = False,
    ) -> "PyMarkdownListPathResult":
        """
        *Scans a provided path for eligible Markdown files without scanning or modifying them.*

        This is the API interface equivalent for the [`pymarkdown scan --list-files`](../user-guide.md#-list-files-or-l) command line action.

        This method is usually the first step in the End-to-End Workflow, used to determine the files that will be processed
        later using the `scan_path` and `fix_path` methods.

        See the [End-to-End Workflow](./pymarkdownapi.md#recommended-end-to-end-workflow) in the class documentation for the recommended pattern of using this method to prepare for scanning.

        The filtering process for determining which files to scan (covered more thoroughly detailed in the [Path](../user-guide.md#path) section of the User's Guide)
        follows these steps:

        1. **Discovery:** `path_to_scan` and `recurse_if_directory` determine the initial set of files to be examined for eligibility.
        2. **Eligibility:** Files are filtered by extension (default `.md`), optionally overridden by `alternate_extensions`.
        3. **Exclusion:** `exclude_patterns` and `respect_gitignore` further narrow the file list.

        Args:
            path_to_scan: The path to scan. Can be a file, a directory, or a glob pattern.
                If a relative path is provided, it is resolved against the current working directory.
            recurse_if_directory: If `path_to_scan` is a directory, setting this to `True`
                includes all subdirectories in the scan.
            alternate_extensions: An optional comma-separated list of file extensions to scan.
                If not `None` and not an empty string, this list **replaces** the default `.md` extension entirely.
                Defaults to `.md` if `None` or an empty string is passed.
            exclude_patterns: If provided, glob patterns to exclude files or directories.
                Patterns are resolved relative to the **current working directory**, not the `path_to_scan` parameter.
                Exclusions are determined by the union of patterns in `exclude_patterns` and `.gitignore`
                files (if `respect_gitignore` is `True`). If a file matches any pattern in either list,
                it is excluded from the scan.
            respect_gitignore: If `True`, respect any `.gitignore` files found when scanning
                according to standard Git rules.

        Returns:
            A [PyMarkdownListPathResult][pymarkdown.api.PyMarkdownListPathResult] object containing:

                - `matching_files`: A list of strings containing the paths of files that would be scanned if the same arguments were presented to the `scan_path` method.

        Raises:
            PyMarkdownApiArgumentException: If `path_to_scan` is empty or if `alternate_extensions`
                does not contain a valid list of file extensions.  Valid file extensions start with
                a single period character and are followed by one or more ASCII alphanumeric characters.
            PyMarkdownApiNoFilesFoundException: If no eligible files were found.
            PyMarkdownApiException: Raised for unexpected internal errors, such as invalid configuration files, plugin loading failures, or unhandled I/O errors.

        Examples:
            ##### Recommended Workflow: Discovering Files.

            The following example is the first part of the workflow demonstrated in the [PyMarkdownApi][pymarkdown.api.PyMarkdownApi] examples. It prepares the file list for [`scan_path`][pymarkdown.api.PyMarkdownApi.scan_path].

            ```python
            # SNIPPET: Part 1 of the End-to-End Workflow
            # Assumes: api = PyMarkdownApi()
            # Assumes: path = "docs/"
            # Assumes: recurse = False

            try:
                list_result = api.list_path(path, recurse_if_directory=recurse)
            except PyMarkdownApiNoFilesFoundException:
                print("No files found.")
                return

            if list_result.matching_files:
                print(f"Discovered {len(list_result.matching_files)} files.")
            ```
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

        this_presentation = PyMarkdownApi.ApiPresentation()
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
        *Report on the application version.*

        This is the API interface equivalent for the [`pymarkdownlnt version`](../user-guide.md#version-command) command line action.

        Returns:
            The current application version.

        Examples:
            This function queries the current version of PyMarkdown.

            ```python
            from pymarkdown.api import PyMarkdownApi

            print(f"PyMarkdown version = {PyMarkdownApi().application_version}")
            ```
        """
        return PyMarkdownLint().application_version

    @property
    def interface_version(self) -> int:
        """
        *Report on the interface version.*

        The history of the interface versions and what they support is as follows:

        | Version | Description |
        | ------- | ----------- |
        |    1    | Initial version. |

        Returns:
            The current plugin interface version. The current plugin interface version is `1`.

        Examples:
            This function queries the current version of this API.

            ```python
            from pymarkdown.api import PyMarkdownApi

            print(f"PyMarkdown API version = {PyMarkdownApi().interface_version}")
            ```
        """
        return PyMarkdownApi.__INTERFACE_VERSION

    def disable_rule_by_identifier(self, rule_identifier: str) -> "PyMarkdownApi":
        """
        *Disables the rule specified by the provided identifier.*

        This is the API interface equivalent for the [`--disable-rules`](../user-guide.md#-enable-rules-disable-rules-rule-plugins) command line argument.
        In advanced scenarios, providing `*` as the rule_identifier will disable all rules as documented in the
        [Selectively Enable Rule Plugins](../advanced_configuration.md#selectively-enable-rule-plugins) section.

        Args:
            rule_identifier (str): The unique identifier of the rule to disable.

        Raises:
            PyMarkdownApiArgumentException: If `rule_identifier` is empty.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example disables a single rule by one of its identifiers.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .disable_rule_by_identifier("md031")
                    .scan_path("file.md")
            )
            ```
        """
        self.__verify_string_argument_not_empty("rule_identifier", rule_identifier)

        self.__disable_rule_identifiers.append(rule_identifier)
        return self

    def enable_rule_by_identifier(self, rule_identifier: str) -> "PyMarkdownApi":
        """
        *Enables the rule specified by the provided identifier.*

        This is the API interface equivalent for the [`--enable-rules`](../user-guide.md#-enable-rules-disable-rules-rule-plugins) command line argument.

        Args:
            rule_identifier (str): The unique identifier of the rule to enable.

        Raises:
            PyMarkdownApiArgumentException: If `rule_identifier` is empty.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example enables a single rule by one of its identifiers.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .enable_rule_by_identifier("md031")
                    .scan_path("file.md")
            )
            ```
        """
        self.__verify_string_argument_not_empty("rule_identifier", rule_identifier)

        self.__enable_rule_identifiers.append(rule_identifier)
        return self

    def enable_extension_by_identifier(
        self, extension_identifier: str
    ) -> "PyMarkdownApi":
        """
        *Enables the extension specified by the provided identifier.*

        This is the API interface equivalent for the [`--enable-extensions`](../user-guide.md#enabling-extensions) command line argument.

        Args:
            extension_identifier (str): The unique identifier of the extension to enable.

        Raises:
            PyMarkdownApiArgumentException: If `extension_identifier` is empty.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example enables a single extension by its identifier.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .enable_extension_by_identifier("front-matter")
                    .scan_path("file.md")
            )
            ```
        """
        self.__verify_string_argument_not_empty(
            "extension_identifier", extension_identifier
        )

        self.__enable_extension_identifiers.append(extension_identifier)
        return self

    def configuration_file_path(self, path_to_config_file: str) -> "PyMarkdownApi":
        """
        *Specifies the configuration file path for this API instance.*

        This is the API interface equivalent for the [`--config`](../user-guide.md#-config-configuration) command line argument.

        Args:
            path_to_config_file (str): The file path to the configuration file to use.

        Raises:
            PyMarkdownApiArgumentException: If `path_to_config_file` is empty.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example sets the path to the configuration file to use.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .configuration_file_path("pymarkdown.cfg")
                    .scan_path("file.md")
            )
            ```
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
        *Sets a named configuration property to a boolean value.*

        This is the API interface equivalent for the [`--set`](../user-guide.md#-set-configuration) command line argument.
        The method automatically formats the value with the `$!` prefix, as per the
        configuration advanced [Set Command](../advanced_configuration.md/#set-command) documentation.

        Args:
            property_name (str): The full hierarchical name of the property to set.
            property_value (bool): The boolean value to assign to the property.

        Raises:
            PyMarkdownApiArgumentException: If `property_name` is empty or if `property_value` is not a boolean.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example sets a boolean value for a specific configuration item.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .set_boolean_property("plugins.md007.enabled", True)
                    .scan_path("file.md")
            )
            ```
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
        *Sets a named configuration property to an integer value.*

        This is the API interface equivalent for the [`--set`](../user-guide.md#-set-configuration) command line argument.
        The method automatically formats the value with the `$#` prefix, as per the
        configuration advanced [Set Command](../advanced_configuration.md/#set-command) documentation.

        Args:
            property_name (str): The full hierarchical name of the property to set.
            property_value (int): The integer value to assign to the property.

        Raises:
            PyMarkdownApiArgumentException: If `property_name` is empty or if `property_value` is not an integer.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example sets an integer value for a specific configuration item.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .set_integer_property("plugins.md007.code_block_line_length", 160)
                    .scan_path("file.md")
            )
            ```
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
        *Sets a named configuration property to a string value.*

        This is the API interface equivalent for the [`--set`](../user-guide.md#-set-configuration) command line argument.

        Args:
            property_name (str): The full hierarchical name of the property to set.
            property_value (str): The string value to assign to the property.

        Raises:
            PyMarkdownApiArgumentException: If `property_name` is empty or if `property_value` is not a string.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example sets a string value for a specific configuration item.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .set_string_property("plugins.heading-style-h1.style", "consistent")
                    .scan_path("file.md")
            )
            ```
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
        *Sets a named configuration property to a value.*

        This is the API interface equivalent for the [`--set`](../user-guide.md#-set-configuration) command line argument.

        Note: If at all possible, the other three `set_*_property` methods should be used
        as they ensure that the correct type of value is set as the configuration item
        value.  This method converts any value provided in `property_value` to its string representation before assigning it to the configuration item.

        Args:
            property_name (str): The full hierarchical name of the property to set.
            property_value (Any): The value to assign to the property. It will be converted to a string.

        Raises:
            PyMarkdownApiArgumentException: If `property_name` is empty.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example sets a configuration item's value to a string representation of the provided argument.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .set_property("plugins.heading-style-h1.style", 1)
                    .scan_path("file.md")
            )
            ```
        """
        self.__verify_string_argument_not_empty("property_name", property_name)

        self.__set_properties.append(f"{property_name}={str(property_value)}")
        return self

    def enable_strict_configuration(self) -> "PyMarkdownApi":
        """
        *Enables strict validation for **all** configuration properties, including those defined in configuration files and those set programmatically.*

        This is the API interface equivalent for the [`--strict-config`](../user-guide.md#-strict-config-configuration) command line argument.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example enables strict adherence to configuration requirements.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .enable_strict_configuration()
                    .scan_path("file.md")
            )
            ```
        """
        self.__enable_strict_configuration = True
        return self

    def log_debug_and_above(self) -> "PyMarkdownApi":
        """
        *Sets PyMarkdown's logging level to DEBUG or higher.*

        This is the API interface equivalent for the [`--log-level`](../user-guide.md#-log-level-with-log-file-logging) command line argument
        with the accompanying argument set to DEBUG. This method is often used in conjunction with the `log_to_file` method to configure both the detail level and output destination.

        Raises:
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example sets the logging level to DEBUG.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .log_debug_and_above()
                    .log_to_file("pymarkdown.log")
                    .scan_path("file.md")
            )
            ```
        """
        return self.log(ApplicationLogging.log_level_debug)

    def log_info_and_above(self) -> "PyMarkdownApi":
        """
        *Sets PyMarkdown's logging level to INFO or higher.*

        This is the API interface equivalent for the [`--log-level`](../user-guide.md#-log-level-with-log-file-logging) command line argument
        with the accompanying argument set to INFO. This method is often used in conjunction with the `log_to_file` method to configure both the detail level and output destination.

        Raises:
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example sets the logging level to INFO.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .log_info_and_above()
                    .log_to_file("pymarkdown.log")
                    .scan_path("file.md")
            )
            ```
        """
        return self.log(ApplicationLogging.log_level_info)

    def log_warning_and_above(self) -> "PyMarkdownApi":
        """
        *Sets PyMarkdown's logging level to WARNING or higher.*

        This is the API interface equivalent for the [`--log-level`](../user-guide.md#-log-level-with-log-file-logging) command line argument
        with the accompanying argument set to WARNING. This method is often used in conjunction with the `log_to_file` method to configure both the detail level and output destination.

        Raises:
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example sets the logging level to WARNING.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .log_warning_and_above()
                    .log_to_file("pymarkdown.log")
                    .scan_path("file.md")
            )
            ```
        """
        return self.log(ApplicationLogging.log_level_warning)

    def log_error_and_above(self) -> "PyMarkdownApi":
        """
        *Sets PyMarkdown's logging level to ERROR or higher.*

        This is the API interface equivalent for the [`--log-level`](../user-guide.md#-log-level-with-log-file-logging) command line argument
        with the accompanying argument set to ERROR. This method is often used in conjunction with the `log_to_file` method to configure both the detail level and output destination.

        Raises:
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example sets the logging level to ERROR.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .log_error_and_above()
                    .log_to_file("pymarkdown.log")
                    .scan_path("file.md")
            )
            ```
        """
        return self.log(ApplicationLogging.log_level_error)

    def log_critical_and_above(self) -> "PyMarkdownApi":
        """
        *Sets PyMarkdown's logging level to CRITICAL or higher.*

        This is the API interface equivalent for the [`--log-level`](../user-guide.md#-log-level-with-log-file-logging) command line argument
        with the accompanying argument set to CRITICAL. This method is often used in conjunction with the `log_to_file` method to configure both the detail level and output destination.

        Raises:
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example sets the logging level to CRITICAL.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .log_critical_and_above()
                    .log_to_file("pymarkdown.log")
                    .scan_path("file.md")
            )
            ```
        """
        return self.log(ApplicationLogging.log_level_critical)

    def log(self, log_level: str) -> "PyMarkdownApi":
        """
        *Sets the logging level using a string value.*

        This is the API interface equivalent for the [`--log-level`](../user-guide.md#-log-level-with-log-file-logging) command line argument.
        This method is often used in conjunction with the `log_to_file` method to configure both the detail level and output destination.

        Args:
            log_level (str): One of "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG".

        Raises:
            PyMarkdownApiArgumentException: If `log_level` is not one of the allowed values.
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example sets the logging level to INFO.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .log("INFO")
                    .log_to_file("pymarkdown.log")
                    .scan_path("file.md")
            )
            ```
        """
        if not ApplicationLogging.is_valid_log_level_type(log_level):
            log_levels_in_order = ",".join(ApplicationLogging.get_valid_log_levels())
            raise PyMarkdownApiArgumentException(
                "log_level",
                f"Parameter 'log_level' must be one of {log_levels_in_order}",
            )

        if self.__inherit_logging:
            raise PyMarkdownApiNotSupportedException(
                "Set log level methods are not supported in log-inheritance mode."
            )

        self.__log_level = log_level
        return self

    def log_to_file(self, log_file_path: str) -> "PyMarkdownApi":
        """
        *Specifies the file path to which log messages will be written.*

        This is the API interface equivalent for the [`--log-file`](../user-guide.md#-log-level-with-log-file-logging) command line argument.
        This method is typically used with one of the other `log*` modifiers to set the logging level to write to the file specified by
        this method.

        Args:
            log_file_path (str): The file path where log messages will be written.

        Raises:
            PyMarkdownApiArgumentException: If `log_file_path` is empty.
            PyMarkdownApiNotSupportedException: If invoked after `inherit_logging` was set
                when creating the `PyMarkdownApi` instance.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example directs logging messages to the specified file.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .log("INFO")
                    .log_to_file("pymarkdown.log")
                    .scan_path("file.md")
            )
            ```
        """
        self.__verify_string_argument_not_empty("log_file_path", log_file_path)

        if self.__inherit_logging:
            raise PyMarkdownApiNotSupportedException(
                "Set log file method is not supported in log-inheritance mode."
            )

        self.__log_file_path = log_file_path
        return self

    def add_plugin_path(self, path_to_plugin: str) -> "PyMarkdownApi":
        """
        *Adds a plugin path that points to a directory containing plugins or to a single plugin.*

        This is the API interface equivalent for the [`--add-plugin`](../user-guide.md#-add-plugin-rule-plugins) command line argument.

        Args:
            path_to_plugin (str): The path to a plugin directory or a single plugin file.

        Raises:
            PyMarkdownApiArgumentException: If `path_to_plugin` is empty.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example demonstrates how to add a plugin path for PyMarkdown to use.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .add_plugin_path("my_plugin.py")
                    .scan_path("file.md")
            )
            ```
        """
        self.__verify_string_argument_not_empty("path_to_plugin", path_to_plugin)

        self.__plugin_paths_to_add.append(path_to_plugin)
        return self

    def enable_stack_trace(self) -> "PyMarkdownApi":
        """
        *Enables the reporting of stack traces for any exceptions caught and reported by the API.*

        This is the API interface equivalent for the [`--stack-trace`](../user-guide.md#-stack-trace-error-reporting) command line argument.

        This provides additional details about the nature of any reported exception.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example enables the reporting of stack traces in case of a raised exception.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .enable_stack_trace()
                    .scan_path("file.md")
            )
            ```
        """
        self.__enable_stack_trace = True
        return self

    def disable_json5_configuration(self) -> "PyMarkdownApi":
        """
        *Disables the JSON5 parser for configuration files, falling back to the standard Python `json` module.*

        This is the API interface equivalent for the [`--no-json5`](../user-guide.md#-no-json5-configuration) command line argument.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example disables the use of the JSON5 parser for configuration files.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .disable_json5_configuration()
                    .scan_path("file.md")
            )
            ```
        """
        self.__disable_json5_configuration = True
        return self

    def enable_continue_on_error(self) -> "PyMarkdownApi":
        """
        *Enables continued scanning even if critical errors are encountered in some files.*

        This is the API interface equivalent for the [`--continue-on-error`](../user-guide.md#-continue-on-error-error-reporting) command line argument.

        This method is primarily intended for debugging or reporting when critical errors occur during file processing.
        It is not intended for general error handling or regular use.
        When a critical error occurs, the exception is normally raised immediately.
        This modifier allows processing to continue by returning the exception details in the `critical_errors` field of the result object instead.

        It is recommended to use this only when debugging critical errors for reporting purposes, not for production stability.
        It allows you to report the critical exception to the development team and how to reproduce it via our [usual reporting process](../usual.md) while the team investigates the issue and releases a code change.

        Returns:
            Returns `self` to allow for method chaining.

        Examples:
            This example allows scanning to continue even if critical errors occur, such as
            encountering a file that cannot be read. The errors are collected in the
            `critical_errors` attribute of the returned result object.

            ```python
            from pymarkdown.api import PyMarkdownApi

            scan_result = (
                PyMarkdownApi()
                    .enable_continue_on_error()
                    .scan_path("file.md")
            )
            ```
        """
        self.__enable_continue_on_error = True
        return self

    def __handle_scan_results(
        self, return_code: int, this_presentation: "PyMarkdownApi.ApiPresentation"
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
        self, return_code: int, this_presentation: "PyMarkdownApi.ApiPresentation"
    ) -> "PyMarkdownFixResult":
        assert (
            not this_presentation.pso
        ), "should not display for scan_path, but for ext ops and plugin ops"
        if return_code not in [0, 1, 3] and not self.__enable_continue_on_error:
            raise PyMarkdownApiException(this_presentation.pse[-1].strip("\n"))
        return PyMarkdownFixResult(this_presentation.files_fixed, this_presentation.pse)

    def __generate_scan_exception(
        self, this_presentation: "PyMarkdownApi.ApiPresentation"
    ) -> None:
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

    class ApiPresentation(MainPresentation):  # docvet: ignore[missing-examples]
        """
        Class to provide for the output of the PyMarkdown application.

        Attributes:
            pso (List[str]): Lines of system output.
            pse (List[str]): Lines of system error.
            pragma_errors (List[PyMarkdownPragmaError]): List of errors encountered parsing pragmas.
            scan_failures (List[PyMarkdownScanFailure]): List of rule failures encountered during the scan.
            files_fixed (List[str]): List of files fixed.
        """

        def __init__(self) -> None:
            """
            Initialize a new instance of the __ApiPresentation class.
            """
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


# pylint: enable=too-many-instance-attributes,too-many-public-methods


@dataclass(frozen=True)
class PyMarkdownScanFailure:  # docvet: ignore[missing-examples]
    """
    A dataclass containing information about a rule failure from a rule plugin.

    This is the API interface encapsulation of the [Rule Failure Format](../user-guide.md#rule-failure-format),
    providing an instance of this class instead of outputting the information to standard output.

    Each instance represents a single rule failure encountered in a Markdown file during the execution of the
    [`scan_path`][pymarkdown.api.PyMarkdownApi.scan_path] method or the
    [`scan_string`][pymarkdown.api.PyMarkdownApi.scan_string] method.
    The encapsulated fields provide the following details about the scan failure:

    - the location where the scan failure occurred
    - the specific location within that location that triggered the scan failure
    - the exact rule that was triggered

    If applicable, extra information about why the rule triggered may be included in the `extra_error_information` field.
    This information is rule-dependent and is
    intended to provide extra clarity about the specific rule failure.

    For more information consult the [Rule Failure Format](../user-guide.md#rule-failure-format)
    section of our User's Guide.

    Attributes:
        scan_file (str): Path to the file containing the failure.
        line_number (int): Line number of the triggered rule failure.
        column_number (int): Column number of the triggered rule failure.
        rule_id (str): ID of the rule that triggered the rule failure.
        rule_name (str): The names of the rule that triggered the rule failure.
        rule_description (str): A detailed description of the rule that triggered the rule failure.
        extra_error_information (Optional[str]): Optional string providing more information on why the rule was triggered.

    Examples:
        This example shows outputting information on the number of rule failures, and for each
        rule failure found, the information from each attribute of the rule failure.

        ```python
        from pymarkdown.api import PyMarkdownApi

        api = PyMarkdownApi()
        scan_result = api.scan_path("docs/")

        if scan_result.scan_failures:
            print(f"\\nFound {len(scan_result.scan_failures)} rule failures(s):")
            for failure in scan_result.scan_failures:
                print(f"  - File: {failure.scan_file}")
                print(f"    Line: {failure.line_number}, Column: {failure.column_number}")
                print(f"    Rule: {failure.rule_id} ({failure.rule_name})")
                print(f"    Desc: {failure.rule_description}")
                if failure.extra_error_information:
                    print(f"    Extra: {failure.extra_error_information}")
                print("-" * 40)
        else:
            print("\\nNo rule failures found.")
        ```
    """

    scan_file: str
    """File that was being scanned when the failure occurred."""
    line_number: int
    """Line number of the triggered rule failure."""
    column_number: int
    """Column number of the triggered rule failure."""
    rule_id: str
    """ID of the rule that triggered the rule failure."""
    rule_name: str
    """The names of the rule that triggered the rule failure."""
    rule_description: str
    """A detailed description of the rule that triggered the rule failure."""
    extra_error_information: Optional[str]
    """Optional string providing more information on why the rule was triggered."""

    def partial_equals(self, other: "PyMarkdownScanFailure") -> bool:
        """
        Determine if the key identifying fields are identical in both objects.

        Returns:
            Returns True if the specified fields match, False otherwise.
        """
        return (
            self.scan_file == other.scan_file
            and self.line_number == other.line_number
            and self.column_number == other.column_number
            and self.rule_id == other.rule_id
        )


@dataclass(frozen=True)
class PyMarkdownPragmaError:  # docvet: ignore[missing-examples]
    """
    A dataclass containing details of a pragma parsing error.

    This is the API interface encapsulation for [Pragma Errors](../extensions/pragmas.md#pragma-commands),
    returning an instance of this object rather than outputting the information to standard output.

    Each instance of this class specifies a single Pragma Error encountered during
    the execution of the [`scan_path`][pymarkdown.api.PyMarkdownApi.scan_path] method
    or the [`scan_string`][pymarkdown.api.PyMarkdownApi.scan_string] method.

    The encapsulated fields provide the following details about the pragma error:

    - the location where the pragma error occurred
    - the position within that location that triggered the pragma error
    - specific details about the error detected by PyMarkdown

    Note: When dealing with the output from the `scan_path` method, the location is always
    a path to the file when the error occurred.  When dealing with the output from the `scan_string` method, the
    location is always set to `in-memory`.

    More information on Pragmas and
    their use is available [here](../user-guide.md#pragma-extension).

    Attributes:
        file_path (str): The path to the file containing the invalid pragma.
        line_number (int): The line number where the pragma is contained.
        pragma_error (str): The error message reported by PyMarkdown.

    Examples:
        This example shows outputting information on the number of Pragma Errors, and for each
        Pragma Error found, the information from each attribute of the Pragma Error.

        ```python
        from pymarkdown.api import PyMarkdownApi

        api = PyMarkdownApi()
        scan_result = api.scan_path("docs/")

        if scan_result.pragma_errors:
            print(f"\\nFound {len(scan_result.pragma_errors)} pragma error(s):")
            for error in scan_result.pragma_errors:
                print(f"  - File: {error.file_path}")
                print(f"    Line: {error.line_number}")
                print(f"    Error: {error.pragma_error}")
                print("-" * 40)
        else:
            print("\\nNo pragma errors found.")
        ```
    """

    file_path: str
    """The path to the file containing the invalid pragma."""
    line_number: int
    """The line number where the pragma is contained."""
    pragma_error: str
    """The error message reported by PyMarkdown."""


@dataclass(frozen=True)
class PyMarkdownScanPathResult:  # docvet: ignore[missing-examples]
    """
    This dataclass encapsulated the results from either the [`scan_path`][pymarkdown.api.PyMarkdownApi.scan_path]
    or [`scan_string`][pymarkdown.api.PyMarkdownApi.scan_string] methods.

    The attributes provide details on rule failures, pragma parsing errors, and any critical errors encountered during the scan.

    Attributes:
        scan_failures (List[PyMarkdownScanFailure]): A list of [PyMarkdownScanFailure][pymarkdown.api.PyMarkdownScanFailure] objects representing rule failures.
        pragma_errors (List[PyMarkdownPragmaError]): A list of [PyMarkdownPragmaError][pymarkdown.api.PyMarkdownPragmaError] objects representing pragma errors.
        critical_errors (List[str]): A list of critical error messages encountered during the scan.

    Examples:
        This example shows outputting information on the number of each class of
        failure, along with details for each critical error reported.  Note that
        examples showing the details for the Rule Failures and Pragma Errors are
        provided in the [PyMarkdownScanFailure][pymarkdown.api.PyMarkdownScanFailure]
        and [PyMarkdownPragmaError][pymarkdown.api.PyMarkdownPragmaError] examples.

        ```python
        from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

        # 1. Setup the API and enable 'continue_on_error' to ensure critical_errors are
        # populated instead of raising an exception immediately. This allows us to
        # demonstrate all 3 attributes.
        api = PyMarkdownApi().enable_continue_on_error()

        # 2. Perform the scan
        try:
            scan_result = (
                api.scan_path("docs/", recurse_if_directory=True)
            )
        except PyMarkdownApiException as e:
            print(f"Scan failed with critical error: {e}")
            scan_result = None

        if scan_result:
            # --- Attribute 1: scan_failures ---
            if scan_result.scan_failures:
                print(f"\\nFound {len(scan_result.scan_failures)} rule failures(s):")
                # See the example for PyMarkdownScanFailure for more detailed output.
            else:
                print("\\nNo rule failures found.")

            # --- Attribute 2: pragma_errors ---
            # These are errors in PyMarkdown pragma commands embedded in the files.
            if scan_result.pragma_errors:
                print(f"\\nFound {len(scan_result.pragma_errors)} pragma error(s):")
                # See the example for PyMarkdownPragmaError for more detailed output.
            else:
                print("\\nNo pragma errors found.")

            # --- Attribute 3: critical_errors ---
            # These are critical system errors (e.g., file not found, encoding issues)
            # that occurred during scanning, populated due to `enable_continue_on_error`.
            if scan_result.critical_errors:
                print(f"\\nFound {len(scan_result.critical_errors)} critical error(s):")
                for error in scan_result.critical_errors:
                    print(f"  - {error}")
                print("-" * 40)
            else:
                print("\\nNo critical errors encountered.")
        ```
    """

    scan_failures: List[PyMarkdownScanFailure]
    """
    A list of [PyMarkdownScanFailure][pymarkdown.api.PyMarkdownScanFailure] objects representing rule failures.
    """
    pragma_errors: List[PyMarkdownPragmaError]
    """
    A list of [PyMarkdownPragmaError][pymarkdown.api.PyMarkdownPragmaError] objects representing pragma errors.
    """
    critical_errors: List[str]
    """
    A list of critical error messages encountered during the scan. Populated only if `enable_continue_on_error`
    is present as parameter in the calling method and if it is enabled. Empty if no critical errors occurred.
    """


@dataclass(frozen=True)
class PyMarkdownFixResult:  # docvet: ignore[missing-examples]
    """
    Class containing the results from the [`fix_path`][pymarkdown.api.PyMarkdownApi.fix_path] method.

    This is the API interface encapsulation for the result of executing the
    [`pymarkdown fix`](../user-guide.md#basic-fixing) command.

    The only information that PyMarkdown provides about the fixed documents is the names of the documents that were fixed.  As such, this result
    simply provides the path names for any fixed Markdown files.

    Attributes:
        files_fixed (List[str]): A list of paths to the files that were successfully fixed.
        critical_errors (List[str]):  A list of critical error messages encountered during the scan.

    Examples:
        This example shows outputting information on the number of files fixed
        and the number of critical errors reported.

        ```python
        from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

        # 1. Setup the API and enable 'continue_on_error' to ensure critical_errors are
        # populated instead of raising an exception immediately.
        api = PyMarkdownApi().enable_continue_on_error()

        # 2. Try and remediate any issues.
        try:
            fix_result = (
                api.fix_path("docs/", recurse_if_directory=True)
            )
        except PyMarkdownApiException as e:
            print(f"Fix failed with critical error: {e}")
            fix_result = None

        if fix_result:
            # --- Attribute 1: files_fixed ---
            if fix_result.files_fixed:
                print(f"\\nFixed {len(fix_result.files_fixed)} Markdown file(s):")
                for fixed_file in fix_result.files_fixed:
                    print(f"  - {fixed_file}")
            else:
                print("\\nNo Markdown files were fixed.")

            # --- Attribute 2: critical_errors ---
            # These are critical system errors (e.g., file not found, encoding issues)
            # that occurred during remediation, populated due to `enable_continue_on_error`.
            if fix_result.critical_errors:
                print(f"\\nFound {len(fix_result.critical_errors)} critical error(s):")
                for error in fix_result.critical_errors:
                    print(f"  - {error}")
                print("-" * 40)
            else:
                print("\\nNo critical errors encountered.")
        ```
    """

    files_fixed: List[str]
    """
    A list of paths to the files that were successfully fixed.
    """
    critical_errors: List[str]
    """
    A list of critical error messages encountered during the scan. Populated only if `enable_continue_on_error`
    is present as parameter in the calling method and if it is enabled. Empty if no critical errors occurred.
    """


@dataclass(frozen=True)
class PyMarkdownFixStringResult:  # docvet: ignore[missing-examples]
    """
    Class to encapsulate the results for the [`fix_string`][pymarkdown.api.PyMarkdownApi.fix_string] method.

    This is the API interface encapsulation for the result of executing the `pymarkdown fix` command
    against a temporarily file that contains a string that was passed to the `fix_string` method.

    This result contains information about fixes applied to the input string, interpreted as a Markdown document.

    Attributes:
        was_fixed (bool): Indicates whether the string content was modified by the fix operation.
        fixed_file (str): The fixed Markdown string, if any fixes were applied. Otherwise, identical to the input string.

    Examples:
        This example shows a Markdown string being passed into the `fix_string` method
        and fixes being applied to that string before it returns.

        ```python
        from pymarkdown.api import PyMarkdownApi

        # 1. Initialize the API
        api = PyMarkdownApi()

        # 2. Define a Markdown string with potential issues
        original_markdown = \"\"\"My list
        1. Item 1
         2. Item 2
        3. Item 3
         4. Item 4
        \"\"\"

        # 3. Call fix_string
        # Note: We enable specific rules to demonstrate "fixing" behavior.
        # `md005`/`list-indent` will align all list items
        try:
            fix_result = api.fix_string(original_markdown)
        except Exception as e:
            print(f"An error occurred: {e}")
            fix_result = None

        # 4. Inspect the result attributes
        if fix_result:
            # --- Attribute 1: was_fixed ---
            # This boolean indicates if the returned 'fixed_file' is different from the input.
            if fix_result.was_fixed:
                print("The Markdown content was successfully fixed.")
            else:
                print("No fixes were necessary. The content is already clean.")

            # --- Attribute 2: fixed_file ---
            # This contains the corrected Markdown string.
            print("\\n--- Fixed Content ---")
            print(fix_result.fixed_file)
            print("--- End of Fixed Content ---")
        ```
    """

    was_fixed: bool
    """
    Indicates whether the string content was modified by the fix operation.
    """

    fixed_file: str
    """
    The fixed Markdown string, if any fixes were applied. Otherwise, identical to the input string.
    """


@dataclass(frozen=True)
class PyMarkdownListPathResult:  # docvet: ignore[missing-examples]
    """
    Class to contain the results of the `list_path` function.

    This object returns a list of files that PyMarkdown understands to be eligible
    for scanning, without having scanned those files.

    Attributes:
        matching_files (List[str]): List of filenames that match the specifications of the requested path.

    Examples:
        This example shows outputting information on the number of eligible files
        found.

        ```python
        from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

        # 1. Initialize the API.
        api = PyMarkdownApi()

        # 2. Look for files along our stated path.
        try:
            list_result = (
                api.list_path("docs/", recurse_if_directory=True)
            )
        except PyMarkdownApiNoFilesFoundException as e:
            print("No matching files were found.")
            return

        # 3. Print the information contained in list_result.
        print(f"Number of matching files: {len(list_result.matching_files)}")
        for file_path in list_result.matching_files:
            print(f"  - {file_path}")
        ```
    """

    matching_files: List[str]
    """List of filenames that match the specifications of the requested path."""


class PyMarkdownApiException(Exception):  # docvet: ignore[missing-examples]
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
        """
        Initialize a new instance of the PyMarkdownApiException class.
        """
        self.__reason = reason

    @property
    def reason(self) -> str:
        """
        Reported reason why the action failed.
        """
        return self.__reason


class PyMarkdownApiNotSupportedException(  # docvet: ignore[missing-examples]
    PyMarkdownApiException
):
    """
    Class to provide for an exception that a given situation is not supported.

    This exception is raised when the `PyMarkdownApi` instance
    is created with the `inherit_logging` parameter set to `True`, followed by a call to
    one of the functions that alters the logging behavior of the application.

    Attributes:
        reason (str): Reported reason why the action failed.
    """


class PyMarkdownApiArgumentException(  # docvet: ignore[missing-examples]
    PyMarkdownApiException
):
    """
    Class to provide for an argument that an exception is not valid.

    This exception is raised when an argument to a function falls outside of the
    expected behavior for that function.  This can mean that a `str` parameter
    is unexpectedly empty or that the parameter is not one of the allowed values
    for that parameter.

    Attributes:
        reason (str): Reported reason why the action failed.
        argument_name (str): Name of the argument that caused this exception to be raised.
    """

    def __init__(self, argument_name: str, reason: str) -> None:
        """
        Initialize a new instance of the PyMarkdownApiArgumentException class.
        """
        super().__init__(reason)
        self.__argument_name = argument_name

    @property
    def argument_name(self) -> str:
        """
        Name of the argument that caused this exception to be raised.
        """
        return self.__argument_name


class PyMarkdownApiNoFilesFoundException(  # docvet: ignore[missing-examples]
    PyMarkdownApiException
):
    """
    Class to provide for an exception that the invoked API was not able to find at least one file to process.

    This is raised as an exception if at least one file to scan or fix is
    not encountered.  As the PyMarkdown application is a scanning application,
    not finding a single Markdown document to scan is typically an exceptional
    case.

    Attributes:
        reason (str): Reported reason why the action failed.
    """
