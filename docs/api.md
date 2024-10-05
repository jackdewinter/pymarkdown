# Module api

Create a new instance of the `PyMarkdownApi` class.

<!-- pyml disable-next-line header-increment-->#### Parameters

- *inherit_logging* - If True, will inherit the logging settings
    from the calling application.  If False, will use the `log_*`
    functions to specify the logging properties.

## Classes

`PyMarkdownApi(inherit_logging: bool = False)`
:   Module to provide for an API to directly communicate with PyMarkdown instead
    of using a command line.

    ### Instance variables

    `application_version: str`
    :   Report on the application version.
        
        #### Returns
        - A `str` with the current application version.

    `interface_version: int`
    :   Report on the interface version.
        
        #### Returns
        - An `int` with the current plugin interface version.

    ### Methods

    `add_plugin_path(self, path_to_plugin: str) ‑> api.PyMarkdownApi`
    :   Add a plugin path that points to a directory with plugins or a single plugin.
        
        #### Parameters
        - *path_to_plugin* - Path to an additional plugin to load.
        
        #### Exceptions
        - `PyMarkdownApiArgumentException` if *path_to_plugin* is empty.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `configuration_file_path(self, path_to_config_file: str) ‑> api.PyMarkdownApi`
    :   Set the path to the configuration file to use.
        
        #### Parameters
        - *path_to_config_file* - Path to the configuration file to use.
        
        #### Exceptions
        - `PyMarkdownApiArgumentException` if *path_to_config_file* is empty.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `disable_rule_by_identifier(self, rule_identifier: str) ‑> api.PyMarkdownApi`
    :   Disable a single rule by one of its identifiers.
        
        #### Parameters
        - *rule_identifier* - Identifier for the rule to disable.
        
        #### Exceptions
        - `PyMarkdownApiArgumentException` if *rule_identifier* is empty.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `enable_rule_by_identifier(self, rule_identifier: str) ‑> api.PyMarkdownApi`
    :   Enable a single rule by one of its identifiers.
        
        #### Parameters
        - *rule_identifier* - Identifier for the rule to disable.
        
        #### Exceptions
        - `PyMarkdownApiArgumentException` if *rule_identifier* is empty.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `enable_stack_trace(self) ‑> api.PyMarkdownApi`
    :   Enable the reporting of stack traces for any exceptions caught by the API.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `enable_strict_configuration(self) ‑> api.PyMarkdownApi`
    :   Enable strict configuration for any requested properties, either through configuration files or manual setting.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `fix_path(self, path_to_scan: str, recurse_if_directory: bool = False, alternate_extensions: Any = None) ‑> api.PyMarkdownFixResult`
    :   Fix any eligible Markdown files found on the provided path that have scan failures that
        can be automatically fixed.
        
        #### Parameters
        - *path_to_scan* - If *path_to_scan* is a directory, scan within that directory for
          eligible Markdown files.  If *path_to_scan* is a file, determine if the file is
          an eligible Markdown file.
        - *recurse_if_directory* - If *path_to_scan* is a directory and *recurse_if_directory*
          if `True`, also scan any directories within the specified directory.
        - *alternate_extensions* - Optionally specify one or more comma-separated file
          extensions.  Files with these file extensions are also considered to be eligible
          files to scan.
        
        #### Exceptions
        - `PyMarkdownApiArgumentException` if *path_to_scan* is empty or if *alternate_extensions*
          does not contain a valid list of file extensions.  Valid file extensions start with a single
          period character and are followed by one or more ASCII alphanumeric characters.
        - `PyMarkdownApiNoFilesFoundException` if no eligible files were found.
        - `PyMarkdownApiException` if some other error was found.
        
        #### Returns
        - An instance of `PyMarkdownFixResult` containing the path to any files that were fixed.

    `fix_string(self, string_to_scan: str) ‑> api.PyMarkdownFixStringResult`
    :   Scan a string passed into the API.

    `list_path(self, path_to_scan: str, recurse_if_directory: bool = False, alternate_extensions: str = '') ‑> api.PyMarkdownListPathResult`
    :   List any eligible files found when scanning the specified path for eligible markdown files.
        
        #### Parameters
        - *path_to_scan* - If *path_to_scan* is a directory, scan within that directory for
          eligible Markdown files.  If *path_to_scan* is a file, determine if the file is
          an eligible Markdown file.
        - *recurse_if_directory* - If *path_to_scan* is a directory and *recurse_if_directory*
          if `True`, also scan any directories within the specified directory.
        - *alternate_extensions* - Optionally specify one or more comma-separated file
          extensions.  Files with these file extensions are also considered to be eligible
          files to scan.
        
        #### Exceptions
        - `PyMarkdownApiArgumentException` if *path_to_scan* is empty or if *alternate_extensions*
          does not contain a valid list of file extensions.  Valid file extensions start with a single
          period character and are followed by one or more ASCII alphanumeric characters.
        - `PyMarkdownApiNoFilesFoundException` if no eligible files were found.
        - `PyMarkdownApiException` if some other error was found.
        
        #### Returns
        - An instance of `PyMarkdownListPathResult` containing eligible Markdown files
          that would normally be scanned.

    `log(self, log_level: str) ‑> api.PyMarkdownApi`
    :   Set the logging level using a string value.
        
        #### Parameters
        - *log_level* - One of "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG".
        
        #### Exceptions
        - `PyMarkdownApiArgumentException` if *log_level* is not one of the allowed values.
        - `PyMarkdownApiNotSupportedException` if invoked after *inherit_logging* was set
          when creating the `PyMarkdownApi` instance.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `log_critical_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the CRITICAL level and above.
        
        #### Exceptions
        - `PyMarkdownApiNotSupportedException` if invoked after *inherit_logging* was set
          when creating the `PyMarkdownApi` instance.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `log_debug_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the DEBUG level and above.
        
        #### Exceptions
        - `PyMarkdownApiNotSupportedException` if invoked after *inherit_logging* was set
          when creating the `PyMarkdownApi` instance.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `log_error_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the ERROR level and above.
        
        #### Exceptions
        - `PyMarkdownApiNotSupportedException` if invoked after *inherit_logging* was set
          when creating the `PyMarkdownApi` instance.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `log_info_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the INFO level and above.
        
        #### Exceptions
        - `PyMarkdownApiNotSupportedException` if invoked after *inherit_logging* was set
          when creating the `PyMarkdownApi` instance.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `log_to_file(self, log_file_path: str) ‑> api.PyMarkdownApi`
    :   Set a file to log any results to.
        
        #### Parameters
        - *log_file_path* - Path to the file to write the logs to.
        
        #### Exceptions
        - `PyMarkdownApiArgumentException` if *log_file_path* is empty.
        - `PyMarkdownApiNotSupportedException` if invoked after *inherit_logging* was set
          when creating the `PyMarkdownApi` instance.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `log_warning_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the WARN level and above.
        
        #### Exceptions
        - `PyMarkdownApiNotSupportedException` if invoked after *inherit_logging* was set
          when creating the `PyMarkdownApi` instance.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `scan_path(self, path_to_scan: str, recurse_if_directory: bool = False, alternate_extensions: Any = None) ‑> api.PyMarkdownScanPathResult`
    :   Scan any eligible Markdown files found on the provided path.
        
        #### Parameters
        - *path_to_scan* - If *path_to_scan* is a directory, scan within that directory for
          eligible Markdown files.  If *path_to_scan* is a file, determine if the file is
          an eligible Markdown file.
        - *recurse_if_directory* - If *path_to_scan* is a directory and *recurse_if_directory*
          if `True`, also scan any directories within the specified directory.
        - *alternate_extensions* - Optionally specify one or more comma-separated file
          extensions.  Files with these file extensions are also considered to be eligible
          files to scan.
        
        #### Exceptions
        - `PyMarkdownApiArgumentException` if *path_to_scan* is empty or if *alternate_extensions*
          does not contain a valid list of file extensions.  Valid file extensions start with a single
          period character and are followed by one or more ASCII alphanumeric characters.
        - `PyMarkdownApiNoFilesFoundException` if no eligible files were found.
        - `PyMarkdownApiException` if some other error was found.
        
        #### Returns
        - An instance of `PyMarkdownScanPathResult` containing any scan failures or pragma errors
          encountered when scanning the eligible files on the provided path.

    `scan_string(self, string_to_scan: str) ‑> api.PyMarkdownScanPathResult`
    :   Scan a string passed into the API.

    `set_boolean_property(self, property_name: str, property_value: bool) ‑> api.PyMarkdownApi`
    :   Set a named configuration property to a given boolean value.
        
        #### Parameters
        - *property_name* - Full hierarchical name of the property to set.
        - *property_value* - `True` or `False` boolean value to set the property to.
        
        #### Exceptions
        - `PyMarkdownApiArgumentException` if *property_name* is empty or if
          *property_value* is not a `bool` value.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `set_integer_property(self, property_name: str, property_value: int) ‑> api.PyMarkdownApi`
    :   Set a named configuration property to a given integer value.
        
        #### Parameters
        - *property_name* - Full hierarchical name of the property to set.
        - *property_value* - Integer value to set the property to.
        
        #### Exceptions
        - `PyMarkdownApiArgumentException` if *property_name* is empty or if
          *property_value* is not an `int` value.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `set_property(self, property_name: str, property_value: Any) ‑> api.PyMarkdownApi`
    :   Set a named configuration property to a given value.  Whatever is passed in as
        the property_value parameter is translated into a string.
        
        #### Parameters
        - *property_name* - Full hierarchical name of the property to set.
        - *property_value* - Value to set the property to after applying a string
          transformation to the value.
        
        #### Exceptions
        - `PyMarkdownApiArgumentException` if *property_name* is empty.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

    `set_string_property(self, property_name: str, property_value: str) ‑> api.PyMarkdownApi`
    :   Set a named configuration property to a given string value.
        
        #### Parameters
        - *property_name* - Full hierarchical name of the property to set.
        - *property_value* - String value to set the property to.
        
        #### Exceptions
        - `PyMarkdownApiArgumentException` if *property_name* is empty or if
          *property_value* is not a `str` value.
        
        #### Returns
        - An instance of `PyMarkdownApi` to allow for function chaining.

`PyMarkdownApiArgumentException(argument_name: str, reason: str)`
:   Class to provide for an argument that an exception is not valid.

    ### Ancestors (in MRO)

    * api.PyMarkdownApiException
    * builtins.Exception
    * builtins.BaseException

    ### Instance variables

    `argument_name: str`
    :   Argument that caused this exception to be raised.

`PyMarkdownApiException(reason: str)`
:   Class to provide for an exception that is thrown by the API layer.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * api.PyMarkdownApiArgumentException
    * api.PyMarkdownApiNoFilesFoundException
    * api.PyMarkdownApiNotSupportedException

    ### Instance variables

    `reason: str`
    :   Reported reason why there were no files found to process.

`PyMarkdownApiNoFilesFoundException(reason: str)`
:   Class to provide for an exception that the invoked API was not able to find at least one file to process.

    ### Ancestors (in MRO)

    * api.PyMarkdownApiException
    * builtins.Exception
    * builtins.BaseException

`PyMarkdownApiNotSupportedException(reason: str)`
:   Class to provide for an exception that a given situation is not supported.

    ### Ancestors (in MRO)

    * api.PyMarkdownApiException
    * builtins.Exception
    * builtins.BaseException

`PyMarkdownFixResult(files_fixed: List[str])`
:   Result for the fix_path function.

    ### Class variables

    `files_fixed: List[str]`
    :   List of zero or more files that were fixed.

`PyMarkdownFixStringResult(was_fixed: bool, fixed_file: str)`
:   Result for the fix_string function.

    ### Class variables

    `fixed_file: str`
    :

    `was_fixed: bool`
    :   Whether the file was fixed.

`PyMarkdownListPathResult(matching_files: List[str])`
:   Result for the list_path function.

    ### Class variables

    `matching_files: List[str]`
    :   List of filenames that match the specifications of the requested path.

`PyMarkdownPragmaError(file_path: str, line_number: int, pragma_error: str)`
:   Class to encapsulate the information for a pragma error.

    ### Class variables

    `file_path: str`
    :   Path to the file that contains the improperly constructed pragma.

    `line_number: int`
    :   Line number where the pragma is contained.

    `pragma_error: str`
    :   Specific information about the error.

`PyMarkdownScanFailure(scan_file: str, line_number: int, column_number: int, rule_id: str, rule_name: str, rule_description: str, extra_error_information: Optional[str])`
:   Class to contain information about a failure reported by one of the rule plugins.

    ### Class variables

    `column_number: int`
    :   Column number of the triggered rule failure.

    `extra_error_information: Optional[str]`
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

`PyMarkdownScanPathResult(scan_failures: List[api.PyMarkdownScanFailure], pragma_errors: List[api.PyMarkdownPragmaError])`
:   Result for the scan_path function.

    ### Class variables

    `pragma_errors: List[api.PyMarkdownPragmaError]`
    :   List of zero or more PyMarkdownPragmaError objects.

    `scan_failures: List[api.PyMarkdownScanFailure]`
    :   List of zero or more PyMarkdownScanFailure objects.
