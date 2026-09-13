# `api` Module

This module provides a programmatic Python interface for interacting with the PyMarkdown
application, bypassing the command line. Readers should be familiar with the PyMarkdown
linter and its command-line interface, since the API wraps these existing tools.

The API expands based on user requests for new functionality. If you need API access
to existing command-line functionality, please submit a feature request via our
[feature request process](../usual.md).

---

## API Action Methods

PyMarkdownApi provides five primary API action methods and two version properties
as its core functionality.
Together, these APIs form the core of most common
workflows in applying PyMarkdown to a set of Markdown files.

The primary questions users typically ask when applying the API are:

- What Markdown files can I scan?
- Are there any rule failures in those Markdown files?
- Can I automatically fix any of those rule failures?

These questions form the basis for the primary workflow described below.

Although other workflows exist, this primary sequence covers the most common use
cases for Markdown documents.
This `discovery -> lint -> remediate` workflow allows users to verify their Markdown
files against their desired formatting standards.

We cover the primary API elements here. Configuration is handled by the
[API Modifier Methods](#api-modifier-methods) described below.

### Recommended End-to-End Workflow

The following workflow demonstrates the recommended usage of the API methods in
sequence. Each method's docstring provides detailed examples for that specific step.
  
```python
import sys
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiArgumentException, PyMarkdownApiNoFilesFoundException

# 0. Establish foundation.
path_to_scan = "docs/"
recurse_if_directory = False
api = PyMarkdownApi(inherit_logging=False).log_to_file("scan.log")

# 1. Discover
try:
    list_result = (
        api.list_path(path_to_scan, recurse_if_directory=recurse_if_directory)
    )
except PyMarkdownApiNoFilesFoundException:
    print(f"No files found in path '{path_to_scan}'.")
    sys.exit(1)

print(f"Found {len(list_result.matching_files)} files to scan.")

# 2. Scan
try:
    scan_result = (
        api.scan_path(path_to_scan, recurse_if_directory=recurse_if_directory)
    )
except PyMarkdownApiException as e:
    print(f"Scan failed: {e}")
    sys.exit(5)

if not scan_result.scan_failures and not scan_result.pragma_errors and not scan_result.critical_errors:
    print("All clear!")
    sys.exit(0)

print(f"Found {len(scan_result.scan_failures)} Rule Failures.")
print(f"Found {len(scan_result.pragma_errors)} Pragma Errors.")
print(f"Found {len(scan_result.critical_errors)} Critical Failures.")
if scan_result.critical_errors:
    sys.exit(5)

# 3. Fix
if not scan_result.scan_failures:
    sys.exit(0)

try:
    fix_result = (
        api.fix_path(path_to_scan, recurse_if_directory=recurse_if_directory)
    )
    if fix_result.critical_errors:
        print(f"Found {len(scan_result.critical_errors)} Critical Failures.")
        sys.exit(5)
    if fix_result.files_fixed:
        print(f"Fixed {len(fix_result.files_fixed)} files.")
        sys.exit(3)
    sys.exit(4)
except PyMarkdownApiException as e:
    print(f"Fix failed: {e}")
    sys.exit(5)
```

::: pymarkdown.api.PyMarkdownApi
    handler: python
    options:
      heading_level: 3
      show_docstring_examples: true
      show_signature: true
      annotations_path: source
      members:
      - list_path
      - scan_path
      - fix_path
      - scan_string
      - fix_string
      - interface_version
      - application_version

## API Modifier Methods

Modifier methods apply configuration to the PyMarkdown API, altering how the
[API Action Methods](#api-action-methods) process Markdown files.
Each
modifier in this section is modeled after a specific command line argument used
to alter PyMarkdown's behavior. Furthermore, each modifier's documentation includes
an explicit reference to that corresponding CLI argument.
Because of this direct mapping, all modifiers support method chaining, allowing
configurations to be applied in a fluent, sequential manner, analogous to specifying
multiple command-line arguments.

For example, the following statement is a fluent example of how to use these modifiers
in a function chain:

```Python
  fix_result = (
    PyMarkdownApi()
      .enable_stack_trace()
      .log_debug_and_above()
      .fix_string("something")
  )
```

The examples use `scan_path` primarily for consistency; however, modifiers are compatible
with all action methods.

::: pymarkdown.api.PyMarkdownApi
    handler: python
    options:
      heading_level: 3
      show_docstring_examples: true
      show_docstring_description: true
      show_docstring_classes: false
      show_docstring_attributes: false
      docstring_options:
        ignore_init_summary: false
      merge_init_into_class: true
      filters:
      - "!scan_.*"
      - "!fix_.*"
      - "!list_.*"
      - "!application_version"
      - "!interface_version"

---

## Scan Results

::: pymarkdown.api.PyMarkdownScanPathResult
    handler: python
    options:
      heading_level: 3
      show_docstring_attributes: false
      members: ["scan_failures", "pragma_errors", "critical_errors"]

---

::: pymarkdown.api.PyMarkdownScanFailure
    handler: python
    options:
      show_docstring_attributes: false
      heading_level: 3
      members: [scan_file, line_number, column_number, rule_id, rule_name, rule_description,
        extra_error_information]

---

::: pymarkdown.api.PyMarkdownPragmaError
    handler: python
    options:
      show_docstring_attributes: false
      heading_level: 3
      members: [file_path, line_number, pragma_error]

---

## Fix Results

::: pymarkdown.api.PyMarkdownFixResult
    handler: python
    options:
      heading_level: 3
      show_docstring_attributes: false
      members: [files_fixed, critical_errors]

---

::: pymarkdown.api.PyMarkdownFixStringResult
    handler: python
    options:
      heading_level: 3
      show_docstring_attributes: false
      members: [was_fixed, fixed_file]

---

## List Results

::: pymarkdown.api.PyMarkdownListPathResult
    handler: python
    options:
      heading_level: 3
      show_docstring_attributes: false
      members: [matching_files]

---

## Exceptions

::: pymarkdown.api.PyMarkdownApiException
    handler: python
    options:
      heading_level: 3
      members: []

---

::: pymarkdown.api.PyMarkdownApiArgumentException
    handler: python
    options:
      heading_level: 3
      members: []

---

::: pymarkdown.api.PyMarkdownApiNoFilesFoundException
    handler: python
    options:
      heading_level: 3
      members: []

---

::: pymarkdown.api.PyMarkdownApiNotSupportedException
    handler: python
    options:
      heading_level: 3
      members: []

---
