Module api
==========

Module to provide for an API to directly communicate with PyMarkdown instead
of using a command line.

Classes
-------

`PyMarkdownApi(inherit_logging: bool = False)`
:   Module to provide for an API to directly communicate with PyMarkdown instead
    of using a command line.

    ### Instance variables

    `application_version: str`
    :   Report on the application version.

    `interface_version: int`
    :   Report on the interface version.

    ### Methods

    `add_plugin_path(self, path_to_plugin: str) ‑> api.PyMarkdownApi`
    :   Add a plugin path that points to a directory with plugins or a single plugin.

    `configuration_file_path(self, path_to_config_file: str) ‑> api.PyMarkdownApi`
    :   Set the path to the configuration file to use.

    `disable_rule_by_identifier(self, rule_identifier: str) ‑> api.PyMarkdownApi`
    :   Disable a given rule by its identifier.

    `enable_rule_by_identifier(self, rule_identifier: str) ‑> api.PyMarkdownApi`
    :   Enable a given rule by its identifier.

    `enable_stack_trace(self) ‑> api.PyMarkdownApi`
    :   Enable the reporting of stack traces for any exceptions caught by the API.

    `enable_strict_configuration(self) ‑> api.PyMarkdownApi`
    :   Enable strict configuration for any requested properties, either through configuration files or manual setting.

    `fix_path(self, path_to_scan: str, recurse_if_directory: bool = False, alternate_extensions: Any = None) ‑> api.PyMarkdownFixResult`
    :   Scan the provided path for markdown files to fix.

    `fix_string(self, string_to_scan: str) ‑> api.PyMarkdownFixStringResult`
    :   Scan a string passed into the API.

    `list_path(self, path_to_scan: str, recurse_if_directory: bool = False, alternate_extensions: str = '') ‑> api.PyMarkdownListPathResult`
    :   List any files found when scanning the specified path for eligible markdown files.

    `log(self, log_level: str) ‑> api.PyMarkdownApi`
    :   Set the logging level using a string value.

    `log_critical_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the CRITICAL level and above.

    `log_debug_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the DEBUG level and above.

    `log_error_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the ERROR level and above.

    `log_info_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the INFO level and above.

    `log_to_file(self, log_file_path: str) ‑> api.PyMarkdownApi`
    :   Set a file to log any results to.

    `log_warning_and_above(self) ‑> api.PyMarkdownApi`
    :   Enable logging for the WARN level and above.

    `scan_path(self, path_to_scan: str, recurse_if_directory: bool = False, alternate_extensions: Any = None) ‑> api.PyMarkdownScanPathResult`
    :   Scan the provided path for markdown files to scan.

    `scan_string(self, string_to_scan: str) ‑> api.PyMarkdownScanPathResult`
    :   Scan a string passed into the API.

    `set_boolean_property(self, property_name: str, property_value: bool) ‑> api.PyMarkdownApi`
    :   Set a named configuration property to a given boolean value.

    `set_integer_property(self, property_name: str, property_value: int) ‑> api.PyMarkdownApi`
    :   Set a named configuration property to a given integer value.

    `set_property(self, property_name: str, property_value: Any) ‑> api.PyMarkdownApi`
    :   Set a named configuration property to a given value.  Whatever is passed in as
        the property_value parameter is traslated into a string.

    `set_string_property(self, property_name: str, property_value: str) ‑> api.PyMarkdownApi`
    :   Set a named configuration property to a given string value.

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
