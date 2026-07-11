# API Support

This document provides practical examples for the PyMarkdown Python API (PyMarkdownApi).
It assumes familiarity with the PyMarkdown CLI.

## Getting Started

This document provides self-contained Python examples for each PyMarkdownApi method.
Copy each script, modify it, and run it to see the results immediately.

For a complete reference of all API methods and parameters, see the [API Listing](./api/pymarkdownapi.md).

Also, in order to give you more experience with the PyMarkdownApi interface and
how to use it, we have included "Try This" boxes after many of the examples. Copy
the provided examples to a new file for experimentation. This preserves the original
reference while allowing you to test custom configurations.

## Pre-requisites

- [PyMarkdown installed](./getting-started.md)
- Familiarity with Python scripting and virtual environments
- Familiarity with the PyMarkdown CLI

If you need help with any of these, see the [Quick Start guides](./quick-starts/index.md).

## What Is the PyMarkdownApi?

The PyMarkdownApi enables Python-based orchestration of PyMarkdown scanning workflows,
offering an alternative to command-line execution.

## API Versioning and Stability

The PyMarkdownApi is currently at **interface version `1`**. This version is considered
stable for production use. Future updates within v1 will focus on adding non-breaking
features and fixing bugs.

Any **breaking changes** (e.g., removing or renaming an existing method, changing
a method's signature) will result in the interface version being incremented.

For example:

- **Non-Breaking (v1 stable):** Adding a new optional parameter to `scan_path` or
  adding a new method like `list_files_by_type`.
- **Breaking (v2 required):** Renaming `scan_path` to `scan_files`, or changing
  the return type of `list_path` from a list to a generator.

Always check both `api.interface_version` and `api.application_version` if your
code relies on specific API behaviors to ensure compatibility with the installed
PyMarkdown version.

!!! note "Dependency Management Context"
    Runtime version checking allows your application to adapt to new features. However,
    it is strongly recommended to pin your PyMarkdown version in your dependencies
    (e.g., `pymarkdownlnt==0.9.38` in `requirements.txt`) to ensure deterministic
    behavior across development, staging, and production environments.

    Runtime version checks should primarily be used for **feature gating** (e.g.,
    "Use new feature X if v1.2+ is available, otherwise fall back to legacy method Y"),
    not for general stability.

If you need to support different API versions or ensure compatibility with future
PyMarkdown releases, you should always check the current interface version at runtime.

!!! tip "Detecting API Version"
    You can determine the active API version by calling the `interface_version`
    property. This is useful if your application needs to adapt to new features
    in future major releases:

    <a id="api-version-check-py"></a>

    ````python title="api_version_check.py"
    from pymarkdown.api import PyMarkdownApi
    import re
    
    def parse_version(version_str:str) -> tuple:
        """Simple parser for 'major.minor.patch' string versions."""
        return tuple(map(int, re.match(r"(\d+)\.(\d+)\.(\d+)", version_str).groups()))

    api = PyMarkdownApi()

    # Check both interface version and application version for full compatibility
    print(f"API Interface Version: {api.interface_version}")
    print(f"PyMarkdown Application Version: {api.application_version}")

    app_version = parse_version(api.application_version)
    if app_version >= (0, 9, 38) and api.interface_version < 2:
        print("Running on API v1 with supported application version.")
    elif api.interface_version >= 2:
        print("Running on API v2 or later.")
    else:
        print("Running on an unsupported or older API version.")
    ````

!!! tip "Feature Gating"
    Use the interface version to safely enable new features without breaking support
    for older versions:

    <a id="api-feature-gating-py"></a>

    ````python title="api_feature_gating.py"
    from pymarkdown.api import PyMarkdownApi
    import re
    
    def parse_version(version_str:str) -> tuple:
        """Simple parser for 'major.minor.patch' string versions."""
        return tuple(map(int, re.match(r"(\d+)\.(\d+)\.(\d+)", version_str).groups()))

    path_to_scan = "docs/"
    api = PyMarkdownApi(inherit_logging=False)
    app_version = parse_version(api.application_version)

    # Check both interface version and application version for safe feature gating
    # Verify the application version matches expectations before trusting interface version
    if app_version >= (0, 9, 38) and api.interface_version >= 2:
        # Use new, optimized method available in newer versions
        result = api.new_advanced_scan(path_to_scan)
    else:
        # Fall back to standard method for older PyMarkdown versions
        result = api.scan_path(path_to_scan)

    # Simple print statement to show the result.
    print(result)
    ````

## CLI vs. API: Key Differences

| Feature | PyMarkdown CLI | PyMarkdownApi |
| :--- | :--- | :--- |
| **Primary Output** | Text printed to `stdout` or `stderr`. | Structured Python objects (e.g., `PyMarkdownScanPathResult`). |
| **Error Handling** | Uses exit codes (0 for success, 1+ for issues). | Raises `PyMarkdownApiException` for critical errors; returns lists for Rule Failures. |
| **Pre-Scan Validation** | Limited; scans and reports in one pass. | Allows pre-scan validation (e.g., checking `list_result.matching_files` before scanning). |
| **Customization** | Command-line flags and configuration files. | Programmatic method calls and Python data structures. |
| **Integration** | Standalone execution. | Embeddable in larger Python applications or scripts. |

!!! tip "Why Does This Matter?"
    Understanding these differences helps you design better automation. For example,
    because the API returns structured data, you can easily filter, sort, or summarize
    results without parsing text output. You can also make decisions based on the
    results (e.g., "Only fix files if no critical errors occurred") before taking
    action.

!!! note "API Design Philosophy: Single Responsibility"
    Each PyMarkdownApi method is designed to do one thing well:

    - **`list_path`** only finds eligible files.
    - **`scan_path`** only identifies Rule Failures and errors.
    - **`fix_path`** only applies automatic fixes.

    This modularity allows you to mix and match these steps in your own workflows.
    For example, you can scan files without fixing them, or fix files without re-scanning
    them first. This offers greater control than a single "scan-and-fix" operation,
    which might obscure intermediate results or force unnecessary processing.

For more information on the specific methods available in this version, see the
[API Listing](./api/pymarkdownapi.md). If you require additional API methods to
expose command-line functionality not currently available, please follow our
[feature request process](./usual.md).

## Api Configuration Methods

The `PyMarkdownApi` object provides numerous methods to configure scanning behavior.
These methods are grouped into the following categories:

- **Rule/Plugin Selection:** Enable, disable, or load plugins.
- **Configuration Properties:** Set boolean, integer, or string properties.
- **Error Handling:** Configure stack traces and error continuation.
- **Logging:** Control log levels and destinations.

For a complete list of configuration methods and their parameters, see the
[API Listing](./api.md#api-configuration-methods). The following example demonstrates
configuring the API via method chaining. It extends the [`api_scan_string.py`](#api-scan-string-py)
example by adding rule disabling and property configuration before execution.

<!-- pyml disable-next-line no-inline-html-->
<a id="api-configuration-py"></a>

<!-- pyml disable code-block-style-->
````python title="api_configuration.py"
import sys
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

string_to_scan = """## Heading 1

This is a test line that exceeds the new 50 character limit
to trigger the MD013 Rule Plugin for demonstration purposes.
"""

api = ( PyMarkdownApi(inherit_logging=False)
    .disable_rule_by_identifier("MD041")
    .set_integer_property("plugins.MD013.line_length", 50)
    .log_to_file("scan.log")
)
try:
    scan_result = api.scan_string(string_to_scan)
except PyMarkdownApiException as e:
    print(f"Scan failed: {e}")
    sys.exit(1)

if not scan_result.scan_failures and not scan_result.pragma_errors and not scan_result.critical_errors:
    print("All clear!")
    sys.exit(0)

print(f"Found {len(scan_result.scan_failures)} Rule Failures.")
print(f"Found {len(scan_result.pragma_errors)} Pragma Errors.")
print(f"Found {len(scan_result.critical_errors)} Critical Errors.")
if scan_result.critical_errors:
    sys.exit(1)
for next_failure in scan_result.scan_failures:
    print(next_failure)
````
<!-- pyml enable code-block-style-->

When you execute the script, you should see the following output:

<!-- pyml disable code-block-style,line-length -->
````text title="Standard Output"
Found 1 Rule Failures.
Found 0 Pragma Errors.
Found 0 Critical Errors.
PyMarkdownScanFailure(scan_file='in-memory', line_number=3, column_number=1, rule_id='MD013', rule_name='line-length', rule_description='Line length', extra_error_information=' [Expected: 50, Actual: 59]')
````
<!-- pyml enable code-block-style, line-length -->

This example is a standard example of scanning a given string as a Markdown document
and identifying any issues with that document. Of particular interest are the calling
of the `disable_rule_by_identifier` method and the `set_integer_property` method.
The calling of the `disable_rule_by_identifier` method disables the `MD041` Rule
Plugin (`first-line-heading`) to allow the document to start with a sub-heading.
The calling of the `set_integer_property` method sets the maximum line length from
its default of `80` to a new value of `50`. In effect, the Rule Failure from `MD041`
is suppressed by disabling the entire Rule Plugin, while a new Rule Failure for
`MD013` is introduced by reducing the trigger threshold.

!!! tip "Try This"
    1. Copy the example above into a file on your system called `api_configuration.py`.
    2. Execute the script as-is.
    3. Verify that only the `MD013` Rule Failure is reported by the script.

    **Bonus Points**

    1. Read the descriptions of one or more of the [Rules](./rules.md).
    2. Modify the `string_to_scan` variable in the script to trigger one specific
       Rule Plugin that you read about in the previous point.
    3. Execute the script and verify that the rule is triggered properly.
    4. Experiment and iterate with different rules to understand the rules better.

## Common Workflows

When designing your integration, consider the following high-level patterns:

- **Simple Scanning:** Use `scan_string` for in-memory documents or `scan_path`
  for simple directory scans.
- **Discovery-Scan-Fix:** Use `list_path` before `scan_path` and `fix_path` to ensure
  you are operating on the correct files. This is critical for maintaining consistency
  between discovery and execution.
- **CI/CD Integration:** Use `enable_strict_configuration()` and `enable_continue_on_error()`
  to ensure your CI checks are robust and informative.

### Common Path Parameters

The methods `list_path`, `scan_path`, and `fix_path` all share the same path discovery
logic. Use these parameters to control which files are processed:

| Discovery&nbsp;Parameter&nbsp;Name | Type | Description |
| :--- | :--- | :--- |
| `path_to_scan` | `str` | The root path to scan (file or directory). |
| `recurse_if_directory` | `bool` | If `True`, scans subdirectories recursively. |
| `alternate_extensions` | `str` | Comma-separated list of extensions (e.g., `".md,.qmd"`). Replaces default `.md`. |
| `exclude_patterns` | `List[str]` | Glob patterns to exclude from the scan. |
| `respect_gitignore` | `bool` | If `True`, honors `.gitignore` rules. |

**Consistency Rule:** Always pass the **same values** for these parameters to
`list_path`, `scan_path`, and `fix_path` to ensure you are scanning, reporting,
and fixing the exact same set of files.

#### Key Concepts in Discovery

The `list_path`, `scan_path`, and `fix_path` methods share a consistent three-phase
discovery process:

1. **Discovery:** `path_to_scan` and `recurse_if_directory` determine the initial
   set of files to be examined for eligibility.
2. **Eligibility:** Files are filtered by extension (default `.md`), optionally
   overridden by `alternate_extensions`.
3. **Exclusion:** `exclude_patterns` and `respect_gitignore` further narrow the
   file list.

#### File Discovery

The first two parameters listed above are the `path_to_scan` parameter which is
required, and the optional `recurse_if_directory` parameters, representing the *discovery*
phase. These parameters are the PyMarkdownApi interface equivalents of the [`path`](./user-guide.md#path)
command-line component and the [`--recurse`](./user-guide.md#-recurse-or-r) command-line
flag. These two parameters work together for *file discovery* to expand the list
of files that may be eligible for further processing by PyMarkdown.

If the `path_to_scan` parameter specifies a directory and the `recurse_if_directory`
parameter is set to `True`, then PyMarkdown additionally looks for any eligible
Markdown files in directories under that directory as well.

#### File Eligibility

If you use the `alternate_extensions` parameter with a comma-separated string (e.g.,
`".md,.qmd"`), you override the default list (`".md"`) entirely.

#### File Exclusion

The final file exclusion phase removes specific paths from the eligible file list.
The `exclude_patterns` and `respect_gitignore` parameters control this behavior,
serving as the PyMarkdownApi equivalents for the [`--exclude`](./user-guide.md#-e-exclude-path_exclusions)
and [`--respect-gitignore`](./user-guide.md#-respect-gitignore) command-line options.

The `exclude_patterns` parameter specifies zero or more paths to exclude from eligibility.
Each entry can be a file path, directory path, or glob pattern. This is particularly
useful for ignoring specific files or directories, such as those containing generated
content or historical data. In the PyMarkdown repository, `exclude_patterns=["./docs"]`
is used for this exact purpose.

When `respect_gitignore=True`, PyMarkdown calls `git check-ignore` to determine
file eligibility. It honors the project's `.gitignore` rules.

#### Why Is This Important?

Because `list_path`, `scan_path`, and `fix_path` use identical discovery logic,
you can chain them confidently using the same parameters for each:

1. `list_path` finds eligible files.
2. `scan_path` checks them for failures.
3. `fix_path` applies fixes.

Using the same parameters across all three ensures you operate on the exact same
file set.

### Scanning Markdown Files

While other workflows exist, a single primary workflow covers the most common use
cases for scanning Markdown documents. That workflow is:
**discovery &rarr; lint &rarr; remediate**.
This simple workflow allows users to answer these questions:

- What Markdown files can I scan?
- Are there any Rule Failures in those Markdown files?
- Can I automatically fix any of those Rule Failures?

Answering these questions forms the basis for the primary workflow.

This primary workflow is referred to in the [Recommended End-to-End Workflow](./api/pymarkdownapi.md#recommended-end-to-end-workflow)
section of the API Listing document. To provide better understanding of what
is involved, this document uses that example as a starting point for a more
comprehensive understanding of the PyMarkdownApi.

What follows is a step-by-step breakdown of the workflow, with added explanations
inserted to provide more information on what is happening and the options available
to you.

#### Step 1: Setup

Define shared parameters once and pass them to all three methods (`list_path`, `scan_path`,
`fix_path`) to ensure consistent file discovery.

For these first examples, we start with the following foundation:

<!-- pyml disable-next-line no-inline-html-->
<a id="api-setup-py"></a>

<!-- pyml disable code-block-style-->
````python title="api_setup.py"
import sys
from pymarkdown.api import PyMarkdownApi,PyMarkdownApiNoFilesFoundException

# 0. Establish foundation.

# Use a relative path to keep logs near the script execution context.
path_to_scan = "docs/"
# Start with non-recursive scanning to avoid unexpectedly scanning subdirectories.
recurse_if_directory = False

# Create the API instance.
# inherit_logging=False is used here because this is a standalone script,
# ensuring PyMarkdown manages its own logging lifecycle without interfering
# with any potential external logger.
api = PyMarkdownApi(inherit_logging=False).log_to_file("scan.log")
````
<!-- pyml enable code-block-style-->

!!! tip "Try This"
    1. Copy the example above into a file on your system called `api_setup.py`.
    2. Locate a directory on your system that contains Markdown files (`.md` extension).
    3. Set the `path_to_scan` variable to the full path of that directory.
    4. Execute the script.

The parameters are configured in the following order:

- `path_to_scan` - relative to the current working directory, the path to scan for
  Markdown files
- `recurse_if_directory` - whether to recurse into a directory if `path_to_scan`
  specifies a directory
- `api` - instance of the PyMarkdownApi interface to interact with

If everything is working correctly, the script will execute and exit without printing
anything to the console.

##### Adding Logging

The following table summarizes the recommended logging configurations based on
your use case:

| Use Case | Configuration |
| :--- | :--- |
| **Standalone Script** | `PyMarkdownApi(inherit_logging=False).log_to_file("my_app.log")` |
| **Library / Application** | `PyMarkdownApi(inherit_logging=True)` |

When using `inherit_logging=False`, you can customize the log level:

- **Debugging:** Set log level to `DEBUG` to trace internal plugin behavior.
- **Troubleshooting:** Provide log files to the PyMarkdown team for issue analysis.
- **Production:** Keep default `INFO` level to reduce output noise.

For **standalone scripts**, use the `log_to_file` method to direct output to a file,
preventing log messages from polluting standard output.

<!-- pyml disable-next-line no-inline-html-->
<a id="api-logging-script-py"></a>

<!-- pyml disable code-block-style-->
````python title="api_logging_script.py"
from pymarkdown.api import PyMarkdownApi

api = PyMarkdownApi(inherit_logging=False).log_to_file("scan.log")
````
<!-- pyml enable code-block-style-->

For **integrated applications** that already configure logging, use `inherit_logging=True`.
This delegates all logging decisions to the host application.

<!-- pyml disable-next-line no-inline-html-->
<a id="api-logging-application-py"></a>

<!-- pyml disable code-block-style-->
````python title="api_logging_application.py"
from pymarkdown.api import PyMarkdownApi

api = PyMarkdownApi(inherit_logging=True)
````
<!-- pyml enable code-block-style-->

##### Handling Errors

In standalone scripts, catching `PyMarkdownApiException` directly is sufficient.
However, in larger applications, you may want to wrap this exception in a custom
error class to provide context specific to your application.

<!-- pyml disable-next-line no-inline-html-->
<a id="api-error-wrapping-py"></a>

<!-- pyml disable code-block-style-->
````python title="api_error_wrapping.py"
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

class MyMarkdownToolException(Exception):
    """Custom exception for the Markdown tool."""
    pass

def scan_with_custom_error_handling(path):
    try:
        api = PyMarkdownApi(inherit_logging=False)
        api.scan_path(path)
    except PyMarkdownApiException as e:
        # Wrap the API exception to preserve the chain but add context
        raise MyMarkdownToolException(f"Failed to scan {path}: {e}") from e
````
<!-- pyml enable code-block-style-->

This pattern allows your application to catch `MyMarkdownToolException` at a higher
level while preserving the original `PyMarkdownApiException` as the `__cause__`.

Another approach is to use the [`enable_continue_on_error`](./api/pymarkdownapi.md#pymarkdown.api.PyMarkdownApi.enable_continue_on_error)
method to redirect any exceptions to the `critical_errors` attribute of several
of the methods. This approach has some benefits and some drawbacks.

This approach allows overall processing to continue even if the specific process
terminates. It is most beneficial when a critical error occurs in a Rule Plugin:
scanning for that single file stops, but other files continue to be processed.
Using `enable_continue_on_error`, the critical error is recorded in the `critical_errors`
attribute of the returned object, but the process of scanning any other files continues.
This allows your API call to complete and report information about every Markdown
file, not just the Markdown files that were scanned before an Exception was thrown.

This ability to bypass bad Rule Plugins has a trade-off: you lose access to the
original Exception object. The `critical_errors` attribute only contains string
representations of the error output, so no additional context is available.

#### Step 2: Discovery

The discovery stage is where the API is used to determine the set of eligible files
that PyMarkdown is going to scan for Rule Failures. The purpose of this stage is
to provide some insight to what PyMarkdown is going to scan once we progress to
later stages.

!!! note "Why separate Discovery from Scanning?"
    We separate `list_path` from `scan_path` to give you control over the workflow.
    By discovering files first, you can:

    1. **Validation:** You can use `list_path` to verify exactly which files will
       be touched before committing to a scan.
    2. **Conditional Fixing:** You might only want to run `fix_path` if `scan_path`
       returns zero `pragma_errors`, ensuring you don't accidentally modify files
       with structural issues.
    3. **Reporting:** You can generate detailed reports of *what* is wrong (`scan_failures`)
       before applying any changes.

From the "Recommended End-to-End Workflow", including the discovery stage, the
script now contains:

<!-- pyml disable-next-line no-inline-html-->
<a id="api-list-path-py"></a>

<!-- pyml disable code-block-style-->
````python title="api_list_path.py"
import sys
from pymarkdown.api import PyMarkdownApi,PyMarkdownApiNoFilesFoundException

# 0. Establish foundation.
path_to_scan = "docs/"
recurse_if_directory = False
api = PyMarkdownApi(inherit_logging=False).log_to_file("scan.log")

# 1. Discover.

# list_path performs three phases guided by its parameters: Discovery (finding files),
# Eligibility (filtering by extension), and Exclusion (applying exclude_patterns).
# This example only shows the Discovery phase.
try:
    list_result = (
        api.list_path(path_to_scan, recurse_if_directory=recurse_if_directory)
    )
except PyMarkdownApiNoFilesFoundException:
    print(f"No files found in path '{path_to_scan}'.")
    sys.exit(0)

print(f"Found {len(list_result.matching_files)} files to scan.")
````
<!-- pyml enable code-block-style-->

??? note "Changes from previous [`api_setup.py`](#api-setup-py) example"
    - Added `PyMarkdownApiNoFilesFoundException` import.
    - Added the `1. Discover.` section which:
        - Calls the `list_path` method to discover files.
        - Added handling of `PyMarkdownApiNoFilesFoundException` to handle empty
          results.
        - Quick output to inform users of how many eligible Markdown files were
          found.

The [`list_path`](./api/pymarkdownapi.md#pymarkdown.api.PyMarkdownApi.list_path)
method raises a `PyMarkdownApiNoFilesFoundException` if no files match the provided
criteria. The example catches this exception to handle empty results gracefully.
If no exception is raised, the script outputs the number of matched files.

!!! tip "Try This"
    1. Copy the example above into a file on your system called `api_list_path.py`.
    2. Modify the value for `path_to_scan` in the script to the value you used
       in the [`api_setup.py`](#api-setup-py) example.
    3. Execute the script.

    **Bonus Points**

    1. Modify the script to print out each path in the `list_result.matching_files`
       attribute, one path per line.
    2. Execute the script.
    3. Verify that the output from the script correctly specifies the number of
       Markdown files in the specified directory, as well as the correct paths to
       those files.

##### Listing Files With All Five Parameters

Here is an example showing all five parameters in a small, ready-to-run example.
The following example applies the `list_path` parameters described previously.

<!-- pyml disable-next-line no-inline-html-->
<a id="api-list-path-advanced-parameters-py"></a>

<!-- pyml disable code-block-style-->
````python title="api_list_path_advanced_parameters.py"
from pymarkdown.api import PyMarkdownApi,PyMarkdownApiNoFilesFoundException

path_to_scan = "docs/"
recurse_if_directory = False
alternate_extensions = ".md,.qmd"
exclude_patterns = ["draft-*.md"]
respect_gitignore = True
api = PyMarkdownApi(inherit_logging=False).log_to_file("scan.log")

# list_path performs three phases guided by its parameters: Discovery (finding files),
# Eligibility (filtering by extension), and Exclusion (applying exclude_patterns).
# This example only shows parameters for all phases being applied.
try:
    list_result = (
        api.list_path(path_to_scan,
            recurse_if_directory=recurse_if_directory,
            # provide alternate extension to use instead of just .md
            alternate_extensions=alternate_extensions,
            # remove files matching this pattern from the list
            exclude_patterns=exclude_patterns,
            # invoke `git` to find out which files `git` itself ignores
            respect_gitignore=respect_gitignore
        )
    )
except PyMarkdownApiNoFilesFoundException:
    print(f"No files found in path '{path_to_scan}'.")
    sys.exit(0)

print(f"Found {len(list_result.matching_files)} files to scan.")
````
<!-- pyml enable code-block-style-->

??? note "Changes from previous [`api_list_path.py`](#api-list-path-py) example"
    - Added three new parameters to the `list_path` call:
        - `alternate_extensions` to provide alternate extensions to scan for.
        - `exclude_patterns` to provide a list of patterns to exclude from the
          list of returned files.
        - `respect_gitignore` to request that `git` remove any files in the list
          according to any project `.gitignore` files.

These changes simply add the parameters `alternate_extensions`, `exclude_patterns`,
and `respect_gitignore`, along with the variables that feed them. While this example
only shows what is possible with the `list_path` method, in subsequent examples,
the `scan_path` and `fix_path` methods should be passed the same set of parameters
and their variables, to be consistent.

!!! tip "Try This"
    1. Copy the example above into a file on your system called `api_list_path_advanced_parameters.py`.
    2. Modify the value for `path_to_scan` in the script to the value you used in
       the [`api_list_path.py`](#api-list-path-py) example.
    3. Execute the script.

    **Bonus Points**

    1. Copy the changes you created to print out each found path on a separate line
       from your copy of the [`api_list_path.py`](#api-list-path-py) example.
    2. Execute the script.
    3. Examine the contents of the directory specified by the `path_to_scan` variable.
    4. Experiment and iterate with different values for the other four parameters.
       Before executing the script, hypothesize what you believe the effects on
       the output will be.
    5. Execute the script and verify if your hypothesis was correct.
    6. Repeat from Step 4 forwards until you have a good grasp what effect changing
       those parameters has.

At this point, you should be able to use the PyMarkdownApi (or the PyMarkdown
command line that it is modelled on) to select only the Markdown files that you
want to process going forward. Next, is moving from discovery to scanning.

#### Step 3: Scanning

The scan stage is where the API is used to determine if any of the eligible Markdown
file have any Rule Failures. For most users of PyMarkdown, this is the main purpose
they are using the application: to lint their Markdown files to follow best practices
for Markdown documents.

**Why scan before fixing?**

Performing a scan before attempting fixes allows you to make informed decisions:

1. **Conditional Logic:** You might only want to fix files if there are no critical
   errors, or if the number of Rule Failures is below a certain threshold.
2. **Reporting:** You can generate detailed reports of *what* is wrong before applying
   any changes, ensuring you don't accidentally modify files that shouldn't be touched.
3. **Safety:** If `scan_path` reveals critical system errors (e.g., permission issues),
   you can abort the process before `fix_path` potentially causes further issues.

From the "Recommended End-to-End Workflow", including the discovery stage and the
scan stage, the script is now:

<!-- pyml disable-next-line no-inline-html-->
<a id="api-scan-path-py"></a>

<!-- pyml disable code-block-style-->
````python title="api_scan_path.py"
import sys
from pymarkdown.api import PyMarkdownApi,PyMarkdownApiNoFilesFoundException,PyMarkdownApiException

# 0. Establish foundation.
path_to_scan = "docs/"
recurse_if_directory = False
api = PyMarkdownApi(inherit_logging=False).log_to_file("scan.log")

# 1. Discover.
try:
    list_result = (
        api.list_path(path_to_scan, recurse_if_directory=recurse_if_directory)
    )
except PyMarkdownApiNoFilesFoundException:
    print(f"No files found in path '{path_to_scan}'.")
    sys.exit(0)

print(f"Found {len(list_result.matching_files)} files to scan.")

# 2. Scan
try:
    # `scan_path` applies rules and returns failures, pragma errors, and critical errors.
    # Note: Pass same discovery params as list_path for consistency.
    scan_result = (
        api.scan_path(path_to_scan, recurse_if_directory=recurse_if_directory)
    )
except PyMarkdownApiException as e:
    print(f"Scan failed: {e}")
    sys.exit(1)

# Check for any type of issue: Rule Failures, Pragma Errors, or critical errors.
if not scan_result.scan_failures and not scan_result.pragma_errors and not scan_result.critical_errors:
    print("All clear!")
    sys.exit(0)

# For simplicity, just print out the number of items present in each category.
print(f"Found {len(scan_result.scan_failures)} Rule Failures.")
print(f"Found {len(scan_result.pragma_errors)} Pragma Errors.")
print(f"Found {len(scan_result.critical_errors)} Critical Errors.")

# Critical Errors indicate a system-level problem, so we exit immediately.
if scan_result.critical_errors:
    sys.exit(1)
````
<!-- pyml enable code-block-style-->

??? note "Changes from previous [`api_list_path.py`](#api-list-path-py) example"
    - Added the `2. Scan` section which:
        - Calls the `scan_path` method to scan files.
        - Handles any raised `PyMarkdownApiException` errors.
        - Print messages to standard output to inform user of what failures and
          errors were found.

<!-- pyml disable line-length-->
!!! note "Critical Distinction: System Errors vs. Rule Failures"
    | Error Type | Example | Handling |
    | :--- | :--- | :--- |
    | **Critical System Error** | Permission denied, Encoding error | `try/except PyMarkdownApiException` OR `enable_continue_on_error()` with `scan_result.critical_errors` |
    | **Pragma Error** | Invalid [Pragma format](./advanced_plugins.md#suppressing-rule-failures-pragmas) | Check `scan_result.pragma_errors` (never raises exception) |
    | **Rule Failure** | MD013, MD041 | Check `scan_result.scan_failures` (never raises exception) |

    > **Pro Tip:** When catching `PyMarkdownApiException`, always use
    > `raise ... from e` (exception chaining) to preserve the original stack trace.
    > This is crucial for debugging, as the root cause (e.g., file not found) is
    > often buried in the inner exception.
<!-- pyml enable line-length-->

Added to the new example is the call to the [`scan_path`](./api/pymarkdownapi.md#pymarkdown.api.PyMarkdownApi.scan_path)
method, including exception handling and rudimentary reporting of the results returned
into the `scan_result` variable. Note that `scan_path` uses the same discovery parameters
as `list_path` (see [Common Path Parameters](#common-path-parameters)). This allows
you to correlate the number of files found with the number of failures reported.

Note: If critical errors occur, consider terminating the scan immediately. Since
most Rule Plugins share code between scanning and fixing, errors during scanning
**likely cause** similar errors during fixing. Therefore, the script reports all
failures but stops execution if **we detect** any critical errors.

#### Interpreting Results

The [`scan_path`](./api/pymarkdownapi.md#pymarkdown.api.PyMarkdownApi.scan_path)
method returns a [`PyMarkdownScanPathResult`](./api/pymarkdownapi.md#pymarkdown.api.PyMarkdownScanPathResult)
object. Its primary attributes, mapped to CLI equivalents, are:

| ScanPathResult Attribute | Type | CLI Equivalent | Description |
| :--- | :--- | :--- | :--- |
| `scan_failures` | `List[PyMarkdown ScanFailure]` | Formatted failure lines in stdout/stderr | Standard Rule Failures (e.g., `MD041`). |
| `pragma_errors` | `List[PyMarkdown PragmaError]` | Pragma warning/error lines | Invalidly formatted [Pragmas](./advanced_plugins.md#suppressing-rule-failures-pragmas). |
| `critical_errors` | `List[str]` | Critical error messages (stderr) | System-level errors (e.g., file not found, encoding issues). |

!!! tip "Key Distinction: Rule Failures vs. Pragma Errors"
    It is important to understand the **source** of these errors to know how to
    resolve them:

    - **`scan_failures`** come from **Rule Plugins** (e.g., `MD013` or `line-length`).
      These are issues with the *content* of your Markdown.
    - **`pragma_errors`** come from **PyMarkdown's core parser**. These are issues
      with the Pragma commands you might have embedded in your file to supress Rule Failures.
    - **`critical_errors`** are internal **system errors** (e.g., file encoding
      issues) that prevented scanning, not issues with your Markdown.

The PyMarkdownApi returns these lists in order: `scan_failures` (normal), `pragma_errors`
(unusual), and `critical_errors` (rare). Although we perform thorough testing, some
issues may remain undetected. When this occurs, PyMarkdown captures one or more
strings in the `critical_errors` list. It is important to use our [reporting process](./usual.md)
to report these strings. Include the captured strings and the setup required to
generate them. That information helps our team identify the issues causing those
critical errors, allowing us to fix them.

The remaining two lists contain errors found directly in the Markdown documents.
The `scan_failures` list reports Rule Failures from Rule Plugins as `PyMarkdownScanFailure`
instances, containing data from the [Rule Failure Format](./user-guide.md#rule-failure-format)
used by the command-line.
The `pragma_errors` list contains `PyMarkdownPragmaError` instances for each invalidly
formed [Pragma](./advanced_plugins.md#suppressing-rule-failures-pragmas). Each item
in these two list gives enough information to the user to allow them to resolve
the reported issue, although they may need to reference the documentation of Pragmas
or the specific Rule Plugin being reported to properly understand what the reported
issue is.

##### Example

For most Python applications and scripts, just informing the user that they have
issues in their Markdown documents is not enough: you need to display the items
in those lists. While omitted from the original example for brevity, a more complete
scanning script would remove the final lines from the [`api_scan_path.py`](#api-scan-path-py)
example, and replace them with code similar in nature to the following `api_scan_path_details.py`
example.

<!-- pyml disable-next-line no-inline-html-->
<a id="api-scan-path-details-py"></a>

<!-- pyml disable code-block-style-->
````python title="api_scan_path_details.py"
import sys
from pymarkdown.api import PyMarkdownApi,PyMarkdownApiException,PyMarkdownApiNoFilesFoundException

# 0. Establish foundation.
path_to_scan = "docs/"
recurse_if_directory = False
api = PyMarkdownApi(inherit_logging=False).log_to_file("scan.log")

# 1. Discover.
try:
    list_result = (
        api.list_path(path_to_scan, recurse_if_directory=recurse_if_directory)
    )
except PyMarkdownApiNoFilesFoundException:
    print(f"No files in {path_to_scan}")
    sys.exit(0)

print(f"Found {len(list_result.matching_files)} files to scan.")

# 2. Scan
try:
    scan_result = (
        api.scan_path(path_to_scan, recurse_if_directory=recurse_if_directory)
    )
except PyMarkdownApiException as e:
    print(f"Scan failed: {e}")
    sys.exit(1)

# --- Attribute 1: scan_failures ---
# scan_failures contain Rule Failures. We track 'any_failures' to determine exit code.
any_failures = False
if scan_result.scan_failures:
    any_failures = True
    print(f"\nFound {len(scan_result.scan_failures)} Rule Failures(s):")
    for failure in scan_result.scan_failures:

        # These attributes are essential for locating and understanding the failure.
        print(f"  - File: {failure.scan_file}")
        print(f"    Line: {failure.line_number}, Column: {failure.column_number}")
        print(f"    Rule: {failure.rule_id} ({failure.rule_name})")
        print(f"    Desc: {failure.rule_description}")

        # extra_error_information may contain additional context for the failure.
        if failure.extra_error_information:
            print(f"    Extra: {failure.extra_error_information}")
        print("-" * 40)
else:
    print("\nNo Rule Failures found.")

# --- Attribute 2: pragma_errors ---
# pragma_errors indicate issues with Pragma (`<!-- pyml`) commands in the markdown.
if scan_result.pragma_errors:
    any_failures = True
    print(f"\nFound {len(scan_result.pragma_errors)} pragma error(s):")
    for error in scan_result.pragma_errors:
        print(f"  - File: {error.file_path}")
        print(f"    Line: {error.line_number}")

        # pragma_error describes the specific syntax issue.
        print(f"    Error: {error.pragma_error}")
        print("-" * 40)
else:
    print("\nNo pragma errors found.")

# --- Attribute 3: critical_errors ---
# critical_errors are system-level failures (e.g., encoding issues) and require immediate attention.
if scan_result.critical_errors:
    print(f"\nFound {len(scan_result.critical_errors)} critical error(s):")
    for error in scan_result.critical_errors:
        print(f"  - {error}")
    print("-" * 40)
    sys.exit(1)
else:
    print("\nNo critical errors encountered.")

# Exit with error code if any failures (rule or pragma) were found.
sys.exit(2 if any_failures else 0)
````
<!-- pyml enable code-block-style-->

??? note "Changes from previous `api_scan_path.py` example"
    - Replaced the information messages written to standard output with
      verbose output of each Rule Failure, Pragma Error, and Critical Error.

While the example is now lengthy, it reports on each attribute of each element
returned in the three lists. Given this information, you can identify and fix each
reported issue in your Markdown documents, reporting any critical errors using the
[standard reporting process](./usual.md) to assist with debugging.

!!! tip "Try This"
    1. Copy the example above into a file on your system called `api_scan_path_details.py`.
    2. Modify the value for `path_to_scan` in the script to the value you used in
       the [`api_list_path.py`](#api-list-path-py) example.
    3. Execute the script.
    4. Verify that each Rule Failure reported by the script is an actual failure
       in the specified file.

    **Bonus Points**

    1. Modify the output format for the Rule Failures into a more concise format
       of your choosing.
    2. Execute the script.
    3. Manually alter the contents of the target Markdown files to resolve the
       specified Rule Failure.
    4. Execute the script.
    5. Use the script output to verify that all Rule Failures are no longer reported.
       If any were missed, go to Step 5 and repeat until all Rule Failures are fixed.

#### Step 4: Fixing

The fix stage is where we apply any Rule Plugins that support the [**autofix**](./user-guide.md#basic-fixing)
capability. By definition, any Rule Plugin that ships with PyMarkdown adheres to
[strict rules](./user-guide.md#strict-rules-for-a-rule-plugin-to-have-the-autofix-ability)
governing what Rule Failures may be automatically fixed. Because of this, PyMarkdown
can fix files without worrying about changing the meaning of a Markdown document.

**Why is fixing separate from scanning?**

Separating scan and fix allows you to:

- Inspect failures before modifying files.
- Re-scan with different configs without re-discovering files.
- Maintain clear separation of concerns for testing.

From the "Recommended End-to-End Workflow", including the discovery stage and the
scan stage, the script is now:

<!-- pyml disable-next-line no-inline-html-->
<a id="api-fix-path-py"></a>

<!-- pyml disable code-block-style-->
````python title="api_fix_path.py"
import sys
from pymarkdown.api import PyMarkdownApi,PyMarkdownApiException,PyMarkdownApiNoFilesFoundException

# 0. Establish foundation.
path_to_scan = "docs/"
recurse_if_directory = False
api = PyMarkdownApi(inherit_logging=False).log_to_file("scan.log")

# 1. Discover.
try:
    list_result = (
        api.list_path(path_to_scan, recurse_if_directory=recurse_if_directory)
    )
except PyMarkdownApiNoFilesFoundException:
    print(f"No files found in path '{path_to_scan}'.")
    sys.exit(0)

print(f"Found {len(list_result.matching_files)} files to scan.")

# 2. Scan
try:
    scan_result = (
        api.scan_path(path_to_scan, recurse_if_directory=recurse_if_directory)
    )
except PyMarkdownApiException as e:
    print(f"Scan failed: {e}")
    sys.exit(1)

if not scan_result.scan_failures and not scan_result.pragma_errors and not scan_result.critical_errors:
    print("All clear!")
    sys.exit(0)

print(f"Found {len(scan_result.scan_failures)} Rule Failures.")
print(f"Found {len(scan_result.pragma_errors)} Pragma Errors.")
print(f"Found {len(scan_result.critical_errors)} Critical Errors.")
if scan_result.critical_errors:
    sys.exit(1)

# 3. Fix
if scan_result.scan_failures:
    try:
        fix_result = (
            api.fix_path(path_to_scan, recurse_if_directory=recurse_if_directory)
        )
        if fix_result.critical_errors:
            print(f"Found {len(scan_result.critical_errors)} Critical Errors.")
            sys.exit(1)
        if fix_result.files_fixed:
            print(f"Fixed {len(fix_result.files_fixed)} files.")
    except PyMarkdownApiException as e:
        print(f"Fix failed: {e}")
        sys.exit(1)
````
<!-- pyml enable code-block-style-->

??? note "Changes from previous [`api_scan_path.py`](#api-scan-path-py) example"
    - Added the `3. Fix` section which:
        - If no Rule Failures are present in `scan_failures`, skip further processing.
        - Calls the `fix_path` method to fix any files that it can.
        - Added exception handling for the new call.
        - Print messages to standard output to inform user of what files had fixes
          applied to them and what errors were found.

The `fix_path` method uses the same discovery logic as `list_path` and `scan_path`
([Common Path Parameters](#common-path-parameters)), ensuring it targets the exact
same files.

Because only Rule Plugins with **autofix** capabilities can modify documents, `fix_path`
may not reduce the failure count for all rules. Check the [Rule Plugins With Autofix](./user-guide.md#rule-plugins-with-autofix)
section for a list of supported Rule Plugins.

!!! tip "Try This"
    1. Copy the example above into a file on your system called `api_fix_path.py`.
    2. Modify the value for `path_to_scan` in the script to the value you used in
       the [`api_list_path.py`](#api-list-path-py) example.
    3. Using the table in [this section](./user-guide.md#rule-plugins-with-autofix)
       as a guide, predict which of the Rule Failures reported by the
       [`api_scan_path_details.py`](#api-scan-path-details-py) script should be
       fixed.
    4. Execute the script.
    5. Validate your list of predicted fixes against what was actually fixed.

### Alternative: In-Memory Scanning With `scan_string`

This section covers string-based scanning, which uses similar methods but operates
on in-memory content rather than files. Instead of dealing with the `list_path`
method and the parameter required to specify which file to scan, the `scan_string`
and `fix_string` methods simply take a single string to process.

As a result of that simplification, the complete example is more compact:

<!-- pyml disable-next-line no-inline-html-->
<a id="api-scan-string-py"></a>

<!-- pyml disable code-block-style-->
````python title="api_scan_string.py"
import sys
from pymarkdown.api import PyMarkdownApi,PyMarkdownApiException

string_to_scan = """# Heading 1
# Heading 2
"""

api = PyMarkdownApi(inherit_logging=False).log_to_file("scan.log")
try:
    scan_result = api.scan_string(string_to_scan)
except PyMarkdownApiException as e:
    print(f"Scan failed: {e}")
    sys.exit(1)

if not scan_result.scan_failures and not scan_result.pragma_errors and not scan_result.critical_errors:
    print("All clear!")
    sys.exit(0)

print(f"Found {len(scan_result.scan_failures)} Rule Failures.")
print(f"Found {len(scan_result.pragma_errors)} Pragma Errors.")
print(f"Found {len(scan_result.critical_errors)} Critical Errors.")
if scan_result.critical_errors:
    sys.exit(1)

if scan_result.scan_failures:
    try:
        # fix_string returns a PyMarkdownFixStringResult object.
        fix_result = api.fix_string(string_to_scan)

        # Check the 'was_fixed' attribute to see if any changes were made.
        if not fix_result.was_fixed:
            print("No fixes were applied to the Markdown content.")
            sys.exit(0)

        # Access 'fixed_file' to get the modified content.
        print("One or more fixes were applied to the Markdown content.")
        print("\n--- Fixed Content ---")
        print(fix_result.fixed_file)
        print("--- End of Fixed Content ---")
    except PyMarkdownApiException as e:
        print(f"Fix failed: {e}")
````
<!-- pyml enable code-block-style-->

Unlike `fix_path` which returns a list of fixed files, `fix_string` returns a
`PyMarkdownFixStringResult` object where `was_fixed` indicates success and `fixed_file`
contains the modified Markdown content. Because of this change, the block that immediately
follows the `fix_string` call was changed. If PyMarkdown did not apply changes,
it says so and exits. Otherwise, it outputs that at least one thing was fixed, along
with the changes to the string.

!!! tip "Try This"
    1. Copy the example above into a file on your system called `api_scan_string.py`.
        - Note how this script mirrors [`api_scan_path.py`](#api-scan-path-py) but
          replaces `path_to_scan` with `string_to_scan`.
        - This demonstrates that the configuration steps (logging, error handling)
          remain identical regardless of the input source.
    2. Execute the script as-is.
    3. Modify the `string_to_scan` value to purposefully trigger one of the Rule
       Plugins [described here](./rules.md) and to trigger its **autofix** capability,
       if the Rule Plugin supports it.
    4. Execute the script, validating that the new `string_to_scan` value behaved
       as you intended.
    5. Experiment and iterate, going back to Step 3, to learn about other rules.

### CI/CD Integration

When to Choose the API over the CLI for CI/CD:

- **Conditional Logic:** You need to run PyMarkdown only on changed files (e.g.,
  using `git diff` to filter input). The CLI cannot natively accept a file list
  from another command without complex shell piping.
- **Custom Reporting:** You need to transform PyMarkdown results into JSON, Slack
  messages, or Jira tickets. Parsing CLI stdout is fragile; the API provides structured
  objects.
- **Multiple Configurations:** You need to scan the same files with different Rule
  Plugin sets in parallel (e.g., strict vs. relaxed modes) within the same pipeline
  stage.

The following shows one way to set up a robust CI/CD check script using the API,
using [Pre-Commit](https://pre-commit.com/). Running the API via Pre-Commit provides
instant feedback during development, catching issues before they hit CI. This saves
CI minutes and reduces friction for contributors by failing fast on local machines.

First, add this script to your `.pre-commit-config.yaml`:

<!-- pyml disable-next-line no-inline-html-->
<a id="-pre-commit-config-yaml"></a>

<!-- pyml disable code-block-style-->
````yaml title=".pre-commit-config.yaml"
repos:
    - repo: local
    hooks:
        - id: pymarkdown-api
        name: PyMarkdown API Check
        # This is the command to run the script from the command line.
        entry: python pymarkdown_check.py
        language: python
        types: [markdown]
        pass_filenames: false
````
<!-- pyml enable code-block-style-->

!!! note "Pre-Commit"
    The Pre-Commit application runs simple workflows, usually linters and formatters,
    on your repository in CI/CD workflows and on `git commit` calls. If you need
    more context, refer to our advanced documentation on
    [Pre-Commit](./advanced_pre-commit.md).

This `.pre-commit-config.yaml` file is what Pre-Commit uses to configure hooks.
In this case, you are specifying that you want to execute a local Python script
as your Pre-Commit hook.

After you have that change in the project's `.pre-commit-config.yaml` file, create
a script `pymarkdown_check.py` that uses `api.scan_path` or `api.scan_string`. Make
sure it exits with `sys.exit(1)` if `scan_result.scan_failures`, `scan_result.pragma_errors`
or `scan_result.critical_errors` are non-empty.

To satisfy those conditions, you can create a new `pymarkdown_check.py` file with
the following content:

<!-- pyml disable-next-line no-inline-html-->
<a id="pymarkdown-check-py"></a>

<!-- pyml disable code-block-style-->
````python title="pymarkdown_check.py"
from pymarkdown.api import PyMarkdownApi,PyMarkdownApiException

api = (
    PyMarkdownApi(inherit_logging=False)
    .enable_strict_configuration()  # Fail if config is wrong
    .log_to_file("scan.log")        # Send logs to log files
    .enable_continue_on_error()     # Report all issues, not just the first
)
path_to_scan = "docs/**

try:
    scan_result = (
        api.scan_path(path_to_scan, recurse_if_directory=True)
    )
except PyMarkdownApiException as e:
    print(f"Scan failed: {e}")
    sys.exit(1)

if not scan_result.scan_failures and not scan_result.pragma_errors and not scan_result.critical_errors:
    print("All clear!")
    sys.exit(0)

print(f"Found {len(scan_result.scan_failures)} Rule Failures.")
print(f"Found {len(scan_result.pragma_errors)} Pragma Errors.")
print(f"Found {len(scan_result.critical_errors)} Critical Errors.")
sys.exit(1)
````
<!-- pyml enable code-block-style-->

??? note "Changes from previous `api_scan_path.py` example"
    - Extra configuration methods called when creating `PyMarkdownApi` instance

This script ensures that your CI pipeline gets comprehensive feedback on configuration
issues, document failures, and other errors. If there are reasons to do custom filtering
of the results or custom invocations of the PyMarkdownApi itself, it is often easier
to do that in a programming language like Python, instead of a scripting language.

!!! tip "Testing Your CI Integration"
    When writing unit tests for your own scripts that use `PyMarkdownApi`, you can
    mock the API instances since it uses a class-based interface. This makes it
    straightforward to replace `PyMarkdownApi` with `MagicMock` or a custom stub
    in your test suite.

    - **Mocking Results:** Ensure your mocks return valid result objects (e.g.,
      `PyMarkdownScanPathResult`) with populated attributes (`scan_failures`,
      `pragma_errors`, etc.) to avoid `AttributeError` during testing.
    - **Mocking Exceptions:** To test your error handling paths, configure your
      mock to raise `PyMarkdownApiException` as needed.

    This approach allows you to verify your own logic (e.g., how you aggregate results
    or handle exit codes) without relying on the actual linter execution in every
    test run.

!!! tip "Try This"
    1. Copy the configuration file from above into the `.pre-commit-config.yaml`
       file in your project's root directory.
        - Note that if the file exists, insert the text after the `repos:` line
          into your existing `.pre-commit-config.yaml` file.
    2. Copy the example above into the file `pymarkdown_check.py` in your project's
       root directory.
    3. Execute the script from the command line to ensure it works.
    4. Execute Pre-Commit from the root of the project using
       `pre-commit run --all-files` and verify it produces the same results.

    **Bonus Points**

    1. Introduce other modifications covered in this page to the `pymarkdown_check.py`
       script, to customize it to your needs.

## Wrap up

This document demonstrated how to use the PyMarkdownApi, including its classes and
methods. At this point you should be able to replicate any functionality provided
by the PyMarkdown CLI using the PyMarkdownApi. If you have not tried all of the
"Try This" boxes, now is a good time to gain the extra experience that the actions
within those boxes present.

If we have not covered an important part of the interface for new PyMarkdownAPI
users, please use our [feature request process](./usual.md) to suggest improvements.
