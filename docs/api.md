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
    Attributes:
        __inherit_logging (bool): Kept version of the `inherit_logging` parameter.

    Initialize a new instance of the PyMarkdownApi class.

    ### Class variables

    `ApiPresentation`
    :   Class to provide for the output of the PyMarkdown application.

        Attributes:
            pso (List[str]): Lines of system output.
            pse (List[str]): Lines of system error.
            pragma_errors (List[PyMarkdownPragmaError]): List of errors encountered parsing pragmas.
            scan_failures (List[PyMarkdownScanFailure]): List of rule failures encountered during the scan.
            files_fixed (List[str]): List of files fixed.

    ### Instance variables

    `application_version: str`
    :   *Report on the application version.*

        This is the API interface equivalent for the [`pymarkdownlnt version`](../user-guide.md#version-command) command line action.

        Returns:
            The current application version.

        Examples:
            This function queries the current version of PyMarkdown.

            ```python
            from pymarkdown.api import PyMarkdownApi

            print(f"PyMarkdown version = {PyMarkdownApi().application_version}")
            ```

    `interface_version: int`
    :   *Report on the interface version.*

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

    ### Methods

    `add_plugin_path(self, path_to_plugin: str) ‑> api.PyMarkdownApi`
    :   *Adds a plugin path that points to a directory containing plugins or to a single plugin.*

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

    `configuration_file_path(self, path_to_config_file: str) ‑> api.PyMarkdownApi`
    :   *Specifies the configuration file path for this API instance.*

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

    `disable_json5_configuration(self) ‑> api.PyMarkdownApi`
    :   *Disables the JSON5 parser for configuration files, falling back to the standard Python `json` module.*

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

    `disable_rule_by_identifier(self, rule_identifier: str) ‑> api.PyMarkdownApi`
    :   *Disables the rule specified by the provided identifier.*

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

    `enable_continue_on_error(self) ‑> api.PyMarkdownApi`
    :   *Enables continued scanning even if critical errors are encountered in some files.*

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

    `enable_extension_by_identifier(self, extension_identifier: str) ‑> api.PyMarkdownApi`
    :   *Enables the extension specified by the provided identifier.*

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

    `enable_rule_by_identifier(self, rule_identifier: str) ‑> api.PyMarkdownApi`
    :   *Enables the rule specified by the provided identifier.*

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

    `enable_stack_trace(self) ‑> api.PyMarkdownApi`
    :   *Enables the reporting of stack traces for any exceptions caught and reported by the API.*

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

    `enable_strict_configuration(self) ‑> api.PyMarkdownApi`
    :   *Enables strict validation for **all** configuration properties, including those defined in configuration files and those set programmatically.*

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

    `fix_path(self, path_to_scan: str, recurse_if_directory: bool = False, alternate_extensions: str | None = None, exclude_patterns: List[str] | None = None, respect_gitignore: bool = False) ‑> api.PyMarkdownFixResult`
    :   *Scans a provided path for eligible Markdown files and applies automatic fixes for any rule violations that have auto-fix capabilities.*

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

    `fix_string(self, string_to_scan: str) ‑> api.PyMarkdownFixStringResult`
    :   *Scan a provided Markdown string and apply any eligible automatic fixes.*

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

            markdown_content = """# Header

            Paragraph with some text.
            """

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

    `list_path(self, path_to_scan: str, recurse_if_directory: bool = False, alternate_extensions: str | None = None, exclude_patterns: List[str] | None = None, respect_gitignore: bool = False) ‑> api.PyMarkdownListPathResult`
    :   *Scans a provided path for eligible Markdown files without scanning or modifying them.*

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

    `log(self, log_level: str) ‑> api.PyMarkdownApi`
    :   *Sets the logging level using a string value.*

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

    `log_critical_and_above(self) ‑> api.PyMarkdownApi`
    :   *Sets PyMarkdown's logging level to CRITICAL or higher.*

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

    `log_debug_and_above(self) ‑> api.PyMarkdownApi`
    :   *Sets PyMarkdown's logging level to DEBUG or higher.*

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

    `log_error_and_above(self) ‑> api.PyMarkdownApi`
    :   *Sets PyMarkdown's logging level to ERROR or higher.*

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

    `log_info_and_above(self) ‑> api.PyMarkdownApi`
    :   *Sets PyMarkdown's logging level to INFO or higher.*

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

    `log_to_file(self, log_file_path: str) ‑> api.PyMarkdownApi`
    :   *Specifies the file path to which log messages will be written.*

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

    `log_warning_and_above(self) ‑> api.PyMarkdownApi`
    :   *Sets PyMarkdown's logging level to WARNING or higher.*

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

    `scan_path(self, path_to_scan: str, recurse_if_directory: bool = False, alternate_extensions: str | None = None, exclude_patterns: List[str] | None = None, respect_gitignore: bool = False) ‑> api.PyMarkdownScanPathResult`
    :   *Scan a provided path for eligible Markdown files and check them for rule violations and pragma errors.*

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

    `scan_string(self, string_to_scan: str) ‑> api.PyMarkdownScanPathResult`
    :   *Scan a provided Markdown string for rule violations and pragma errors.*

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

            markdown_content = """# Header

            This is a paragraph with some text.
            """

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

    `set_boolean_property(self, property_name: str, property_value: bool) ‑> api.PyMarkdownApi`
    :   *Sets a named configuration property to a boolean value.*

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

    `set_integer_property(self, property_name: str, property_value: int) ‑> api.PyMarkdownApi`
    :   *Sets a named configuration property to an integer value.*

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

    `set_property(self, property_name: str, property_value: Any) ‑> api.PyMarkdownApi`
    :   *Sets a named configuration property to a value.*

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

    `set_string_property(self, property_name: str, property_value: str) ‑> api.PyMarkdownApi`
    :   *Sets a named configuration property to a string value.*

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

`PyMarkdownApiArgumentException(argument_name: str, reason: str)`
:   Class to provide for an argument that an exception is not valid.

    This exception is raised when an argument to a function falls outside of the
    expected behavior for that function.  This can mean that a `str` parameter
    is unexpectedly empty or that the parameter is not one of the allowed values
    for that parameter.

    Attributes:
        reason (str): Reported reason why the action failed.
        argument_name (str): Name of the argument that caused this exception to be raised.

    Initialize a new instance of the PyMarkdownApiArgumentException class.

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

    Initialize a new instance of the PyMarkdownApiException class.

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

    Initialize a new instance of the PyMarkdownApiException class.

    ### Ancestors (in MRO)

    * api.PyMarkdownApiException
    * builtins.Exception
    * builtins.BaseException

`PyMarkdownApiNotSupportedException(reason: str)`
:   Class to provide for an exception that a given situation is not supported.

    This exception is raised when the `PyMarkdownApi` instance
    is created with the `inherit_logging` parameter set to `True`, followed by a call to
    one of the functions that alters the logging behavior of the application.

    Attributes:
        reason (str): Reported reason why the action failed.

    Initialize a new instance of the PyMarkdownApiException class.

    ### Ancestors (in MRO)

    * api.PyMarkdownApiException
    * builtins.Exception
    * builtins.BaseException

`PyMarkdownFixResult(files_fixed: List[str], critical_errors: List[str])`
:   Class containing the results from the [`fix_path`][pymarkdown.api.PyMarkdownApi.fix_path] method.

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
                print(f"\nFixed {len(fix_result.files_fixed)} Markdown file(s):")
                for fixed_file in fix_result.files_fixed:
                    print(f"  - {fixed_file}")
            else:
                print("\nNo Markdown files were fixed.")

            # --- Attribute 2: critical_errors ---
            # These are critical system errors (e.g., file not found, encoding issues)
            # that occurred during remediation, populated due to `enable_continue_on_error`.
            if fix_result.critical_errors:
                print(f"\nFound {len(fix_result.critical_errors)} critical error(s):")
                for error in fix_result.critical_errors:
                    print(f"  - {error}")
                print("-" * 40)
            else:
                print("\nNo critical errors encountered.")
        ```

    ### Instance variables

    `critical_errors: List[str]`
    :   A list of critical error messages encountered during the scan. Populated only if `enable_continue_on_error`
        is present as parameter in the calling method and if it is enabled. Empty if no critical errors occurred.

    `files_fixed: List[str]`
    :   A list of paths to the files that were successfully fixed.

`PyMarkdownFixStringResult(was_fixed: bool, fixed_file: str)`
:   Class to encapsulate the results for the [`fix_string`][pymarkdown.api.PyMarkdownApi.fix_string] method.

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
        original_markdown = """My list
        1. Item 1
         2. Item 2
        3. Item 3
         4. Item 4
        """

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
            print("\n--- Fixed Content ---")
            print(fix_result.fixed_file)
            print("--- End of Fixed Content ---")
        ```

    ### Instance variables

    `fixed_file: str`
    :   The fixed Markdown string, if any fixes were applied. Otherwise, identical to the input string.

    `was_fixed: bool`
    :   Indicates whether the string content was modified by the fix operation.

`PyMarkdownListPathResult(matching_files: List[str])`
:   Class to contain the results of the `list_path` function.

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

    ### Instance variables

    `matching_files: List[str]`
    :   List of filenames that match the specifications of the requested path.

`PyMarkdownPragmaError(file_path: str, line_number: int, pragma_error: str)`
:   A dataclass containing details of a pragma parsing error.

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
            print(f"\nFound {len(scan_result.pragma_errors)} pragma error(s):")
            for error in scan_result.pragma_errors:
                print(f"  - File: {error.file_path}")
                print(f"    Line: {error.line_number}")
                print(f"    Error: {error.pragma_error}")
                print("-" * 40)
        else:
            print("\nNo pragma errors found.")
        ```

    ### Instance variables

    `file_path: str`
    :   The path to the file containing the invalid pragma.

    `line_number: int`
    :   The line number where the pragma is contained.

    `pragma_error: str`
    :   The error message reported by PyMarkdown.

`PyMarkdownScanFailure(scan_file: str, line_number: int, column_number: int, rule_id: str, rule_name: str, rule_description: str, extra_error_information: str | None)`
:   A dataclass containing information about a rule failure from a rule plugin.

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
            print(f"\nFound {len(scan_result.scan_failures)} rule failures(s):")
            for failure in scan_result.scan_failures:
                print(f"  - File: {failure.scan_file}")
                print(f"    Line: {failure.line_number}, Column: {failure.column_number}")
                print(f"    Rule: {failure.rule_id} ({failure.rule_name})")
                print(f"    Desc: {failure.rule_description}")
                if failure.extra_error_information:
                    print(f"    Extra: {failure.extra_error_information}")
                print("-" * 40)
        else:
            print("\nNo rule failures found.")
        ```

    ### Instance variables

    `column_number: int`
    :   Column number of the triggered rule failure.

    `extra_error_information: str | None`
    :   Optional string providing more information on why the rule was triggered.

    `line_number: int`
    :   Line number of the triggered rule failure.

    `rule_description: str`
    :   A detailed description of the rule that triggered the rule failure.

    `rule_id: str`
    :   ID of the rule that triggered the rule failure.

    `rule_name: str`
    :   The names of the rule that triggered the rule failure.

    `scan_file: str`
    :   File that was being scanned when the failure occurred.

    ### Methods

    `partial_equals(self, other: PyMarkdownScanFailure) ‑> bool`
    :   Determine if the key identifying fields are identical in both objects.

        Returns:
            Returns True if the specified fields match, False otherwise.

`PyMarkdownScanPathResult(scan_failures: List[api.PyMarkdownScanFailure], pragma_errors: List[api.PyMarkdownPragmaError], critical_errors: List[str])`
:   This dataclass encapsulated the results from either the [`scan_path`][pymarkdown.api.PyMarkdownApi.scan_path]
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
                print(f"\nFound {len(scan_result.scan_failures)} rule failures(s):")
                # See the example for PyMarkdownScanFailure for more detailed output.
            else:
                print("\nNo rule failures found.")

            # --- Attribute 2: pragma_errors ---
            # These are errors in PyMarkdown pragma commands embedded in the files.
            if scan_result.pragma_errors:
                print(f"\nFound {len(scan_result.pragma_errors)} pragma error(s):")
                # See the example for PyMarkdownPragmaError for more detailed output.
            else:
                print("\nNo pragma errors found.")

            # --- Attribute 3: critical_errors ---
            # These are critical system errors (e.g., file not found, encoding issues)
            # that occurred during scanning, populated due to `enable_continue_on_error`.
            if scan_result.critical_errors:
                print(f"\nFound {len(scan_result.critical_errors)} critical error(s):")
                for error in scan_result.critical_errors:
                    print(f"  - {error}")
                print("-" * 40)
            else:
                print("\nNo critical errors encountered.")
        ```

    ### Instance variables

    `critical_errors: List[str]`
    :   A list of critical error messages encountered during the scan. Populated only if `enable_continue_on_error`
        is present as parameter in the calling method and if it is enabled. Empty if no critical errors occurred.

    `pragma_errors: List[api.PyMarkdownPragmaError]`
    :   A list of [PyMarkdownPragmaError][pymarkdown.api.PyMarkdownPragmaError] objects representing pragma errors.

    `scan_failures: List[api.PyMarkdownScanFailure]`
    :   A list of [PyMarkdownScanFailure][pymarkdown.api.PyMarkdownScanFailure] objects representing rule failures.
