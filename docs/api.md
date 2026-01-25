# Module api

Create a new instance of the `PyMarkdownApi` class.

## Classes

`PyMarkdownApi(inherit_logging: bool = False)`
:   Module to provide for an API to directly communicate with PyMarkdown instead
    of using a command line.

    Args:
        inherit_logging: If True, inherit the logging settings from the calling
            application.  If False, will use the `log_*` functions to specify the
            logging properties.

    ### Instance variables

    `application_version: str`
    :   Report on the application version.

        Returns:
            The current application version.

        Examples:
            This function queries the current version of PyMarkdown.

                from pymarkdown.api import PyMarkdownApi

                print(f"PyMarkdown version = {PyMarkdownApi().application_version}")

    `interface_version: int`
    :   Report on the interface version.

        Returns:
            The current plugin interface version.

        Examples:
            This function queries the current version of this API.

                from pymarkdown.api import PyMarkdownApi

                print(f"PyMarkdown API version = {PyMarkdownApi().interface_version}")

    ### Methods

    `add_plugin_path(self, path_to_plugin: str) ‑> api.PyMarkdownApi`
    :   Add a plugin path that points to a directory with plugins or a single plugin.

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

    `configuration_file_path(self, path_to_config_file: str) ‑> api.PyMarkdownApi`
    :   Set the path to the configuration file to use.

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

    `disable_json5_configuration(self) ‑> api.PyMarkdownApi`
    :   Disable the use of the JSON5 parser for configuration files, instead
        using the base json parser from the Python standard library.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function disables the use of the JSON5 parser for configuration files.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().disable_json5_configuration().scan_path("file.md")

    `disable_rule_by_identifier(self, rule_identifier: str) ‑> api.PyMarkdownApi`
    :   Disable a single rule by one of its identifiers.

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

    `enable_continue_on_error(self) ‑> api.PyMarkdownApi`
    :   Enable the scanning of multiple files to continue, even if some of the files
        have critical errors.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function disables the use of the JSON5 parser for configuration files.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().disable_json5_configuration().scan_path("file.md")

    `enable_extension_by_identifier(self, extension_identifier: str) ‑> api.PyMarkdownApi`
    :   Enable a single extension by its identifier.

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

    `enable_rule_by_identifier(self, rule_identifier: str) ‑> api.PyMarkdownApi`
    :   Enable a single rule by one of its identifiers.

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

    `enable_stack_trace(self) ‑> api.PyMarkdownApi`
    :   Enable the reporting of stack traces for any exceptions caught by the API.
        If this modifier is present, additional information will be recorded as
        to the exact nature of any reported exception.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function enable stack trace support in case of a raised exception.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().enable_stack_trace().scan_path("file.md")

    `enable_strict_configuration(self) ‑> api.PyMarkdownApi`
    :   Enable strict configuration for any requested properties, either through configuration files or manual setting.

        Returns:
            An instance of `PyMarkdownApi` to allow for function chaining.

        Examples:
            This function enforces strict adherence to configuration requirements.

                from pymarkdown.api import PyMarkdownApi

                PyMarkdownApi().enable_strict_configuration().scan_path("file.md")

    `fix_path(self, path_to_scan: str, recurse_if_directory: bool = False, alternate_extensions: Any = None, exclude_patterns: List[str] | None = None, respect_gitignore: bool = False) ‑> api.PyMarkdownFixResult`
    :   Fix any eligible Markdown files found on the provided path that have scan failures that
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

    `fix_string(self, string_to_scan: str) ‑> api.PyMarkdownFixStringResult`
    :   Scan the specified string as a Markdown document and apply any eligible fixes.

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

                markdown_string = "# Markdown\n\nIs cool!\n"

                try:
                    fix_result = PyMarkdownApi().fix_string(markdown_string)
                    print(f"Applied fixes?  {fix_result.was_fixed}")
                    print(f"Fixed Markdown: {fix_result.fixed_file}")
                except PyMarkdownApiException as this_exception:
                    print(f"API Exception: {this_exception}", file=sys.stderr)

    `list_path(self, path_to_scan: str, recurse_if_directory: bool = False, alternate_extensions: str = '', exclude_patterns: List[str] | None = None, respect_gitignore: bool = False) ‑> api.PyMarkdownListPathResult`
    :   List any eligible files found when scanning the specified path for eligible markdown files.
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

    `log(self, log_level: str) ‑> api.PyMarkdownApi`
    :   Set the logging level using a string value.

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

    `log_critical_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the CRITICAL level and above.

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

    `log_debug_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the DEBUG level and above.

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

    `log_error_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the ERROR level and above.

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

    `log_info_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the INFO level and above.

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

    `log_to_file(self, log_file_path: str) ‑> api.PyMarkdownApi`
    :   Set a file to log any results to.

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

    `log_warning_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the WARN level and above.

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

    `scan_path(self, path_to_scan: str, recurse_if_directory: bool = False, alternate_extensions: str | None = None, exclude_patterns: List[str] | None = None, respect_gitignore: bool = False) ‑> api.PyMarkdownScanPathResult`
    :   Scan any eligible Markdown files found on the provided path.  For more information,
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

    `scan_string(self, string_to_scan: str) ‑> api.PyMarkdownScanPathResult`
    :   Scan the specified string as a Markdown document.

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

                markdown_string = "# Markdown\n\nIs cool!\n"

                try:
                    scan_result = PyMarkdownApi().scan_string(markdown_string)
                    print(f"Scan Failures: {scan_result.scan_failures}")
                    print(f"Pragma Errors: {scan_result.pragma_errors}")
                except PyMarkdownApiException as this_exception:
                    print(f"API Exception: {this_exception}", file=sys.stderr)

    `set_boolean_property(self, property_name: str, property_value: bool) ‑> api.PyMarkdownApi`
    :   Set a named configuration property to a given boolean value.

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

    `set_integer_property(self, property_name: str, property_value: int) ‑> api.PyMarkdownApi`
    :   Set a named configuration property to a given integer value.

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

    `set_property(self, property_name: str, property_value: Any) ‑> api.PyMarkdownApi`
    :   Set a named configuration property to a given value.  Whatever is passed in as
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

    `set_string_property(self, property_name: str, property_value: str) ‑> api.PyMarkdownApi`
    :   Set a named configuration property to a given string value.

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

`PyMarkdownApiArgumentException(argument_name: str, reason: str)`
:   Class to provide for an argument that an exception is not valid.

    This exception is raised when an argument to a function falls outside of the
    expected behavior for that function.  This can mean that a `str` parameter
    is unexpectedly empty or that the parameter is not one of the allowed values
    for that parameter.

    Attributes:
        reason (str): Reported reason why the action failed.
        argument_name(str): Name of the argument that caused this exception to be raised.

    ### Ancestors (in MRO)

    * api.PyMarkdownApiException
    * builtins.Exception
    * builtins.BaseException

    ### Instance variables

    `argument_name: str`
    :   Name of the argument that caused this exception to be raised.

`PyMarkdownApiException(reason: str)`
:   Class to provide for an exception that is thrown by the API layer.

    This base PyMarkdown application exception is explicitly thrown when a unexpected error occurs that
    is not categorized as one of the other application exceptions.  Where possible, child classes of
    this class should be used to provide more specific information regarding the nature of the
    exception.

    Attributes:
        reason (str): Reported reason why the action failed.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * api.PyMarkdownApiArgumentException
    * api.PyMarkdownApiNoFilesFoundException
    * api.PyMarkdownApiNotSupportedException

    ### Instance variables

    `reason: str`
    :   Reported reason why the action failed.

`PyMarkdownApiNoFilesFoundException(reason: str)`
:   Class to provide for an exception that the invoked API was not able to find at least one file to process.

    This is raised as an exception if at least one file to scan or fix is
    not encountered.  As the PyMarkdown application is a scanning application,
    not finding a single Markdown document to scan is typically an exceptional
    case.

    Attributes:
        reason (str): Reported reason why the action failed.

    ### Ancestors (in MRO)

    * api.PyMarkdownApiException
    * builtins.Exception
    * builtins.BaseException

`PyMarkdownApiNotSupportedException(reason: str)`
:   Class to provide for an exception that a given situation is not supported.

    The most frequent raising of this exception is when the `PyMarkdownApi` instance
    is created with the *inherit_logging* set to `True`, followed by a call to
    one of the functions that alters the logging behavior of the application.

    Attributes:
        reason (str): Reported reason why the action failed.

    ### Ancestors (in MRO)

    * api.PyMarkdownApiException
    * builtins.Exception
    * builtins.BaseException

`PyMarkdownFixResult(files_fixed: List[str], critical_errors: List[str])`
:   Result for the fix_path function.

    The only information that PyMarkdown provides about scanned and fixed
    documents are the names of the documents that were fixed.  As such, this result
    simply provides those same Markdown file names.

    Attributes:
        files_fixed (List[str]): List of zero or more files that were fixed.

    ### Instance variables

    `critical_errors: List[str]`
    :   List of zero or more critical errors that were encountered during the fixing of the files. Only
        set if `enable_continue_on_error` was set when the `fix_path` function was invoked.
        If no critical errors were encountered, this list is empty.

    `files_fixed: List[str]`
    :   List of zero or more files that were fixed.

`PyMarkdownFixStringResult(was_fixed: bool, fixed_file: str)`
:   Result for the fix_string function.

    Focusing on a singular Markdown document, this object returns an indication
    of whether fixes were applied along with the fixed document.

    Attributes:
        was_fixed (bool): Whether the string, interpretted as a Markdown document, was fixed.
        fixed_file (str): String that was passed into the `fix_string` function, with any fixes applied to it.

    ### Instance variables

    `fixed_file: str`
    :   String that was passed into the `fix_string` function, with any fixes applied
        to it.

    `was_fixed: bool`
    :   Whether the string was fixed.

`PyMarkdownListPathResult(matching_files: List[str])`
:   Result for the list_path function.

    This object returns a list of files that PyMarkdown understands to be eligible
    for scanning, without having scanned those files.

    Attributes:
        matching_files (List[str]): List of filenames that match the specifications of the requested path.

    ### Instance variables

    `matching_files: List[str]`
    :   List of filenames that match the specifications of the requested path.

`PyMarkdownPragmaError(file_path: str, line_number: int, pragma_error: str)`
:   Class to encapsulate the information for a pragma error.

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

    ### Instance variables

    `file_path: str`
    :   Path to the file that contains the improperly constructed pragma.

    `line_number: int`
    :   Line number where the pragma is contained.

    `pragma_error: str`
    :   Specific information about the error.

`PyMarkdownScanFailure(scan_file: str, line_number: int, column_number: int, rule_id: str, rule_name: str, rule_description: str, extra_error_information: str | None)`
:   Class to contain information about a failure reported by one of the rule plugins.

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

    ### Instance variables

    `column_number: int`
    :   Column number of the triggered rule failure.

    `extra_error_information: str | None`
    :   Optional string providing more information on why the rule was triggered.

    `line_number: int`
    :   Line number of the triggered rule failure.

    `rule_description: str`
    :   Longer description of the rule that was triggered.

    `rule_id: str`
    :   ID of the rule that was triggered.

    `rule_name: str`
    :   Name(s) of the rule that was triggered.

    `scan_file: str`
    :   File that was being scanned when the failure occurred.

    ### Methods

    `partial_equals(self, other: PyMarkdownScanFailure) ‑> bool`
    :   Decide if special fields are the same from both items.

`PyMarkdownScanPathResult(scan_failures: List[api.PyMarkdownScanFailure], pragma_errors: List[api.PyMarkdownPragmaError], critical_errors: List[str])`
:   Result for the `scan_path` and `scan_string` functions.

    As both `PyMarkdownScanFailure` objects and `PyMarkdownPragmaError` objects
    contain location and additional failure/error information, this result
    object is a simple pair of lists containing failure information.

    Attributes:
        scan_failures (List[PyMarkdownScanFailure]): Zero or more `PyMarkdownScanFailure` objects.
        pragma_errors (List[PyMarkdownPragmaError]): Zero or more `PyMarkdownPragmaError` objects.

    ### Instance variables

    `critical_errors: List[str]`
    :   List of zero or more critical errors that were encountered during the scan. Only
        set if `enable_continue_on_error` was set when the `scan_path` or `scan_string`
        function was invoked.  If no critical errors were encountered, this list is empty.

    `pragma_errors: List[api.PyMarkdownPragmaError]`
    :   List of zero or more `PyMarkdownPragmaError` objects.

    `scan_failures: List[api.PyMarkdownScanFailure]`
    :   List of zero or more `PyMarkdownScanFailure` objects.
