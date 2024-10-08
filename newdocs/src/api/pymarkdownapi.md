# `api` Module

This module is used to interact with the PyMarkdown application through a programmatic
Python interface, instead of through the command line.  This API Listing assumes
familiarity with the PyMarkdown linter and its command line interface.  For a more
descriptive and easy to follow guide to this API, please check out our
[API Support document](../api.md).

Our current process is to add new functions to the API in response to requests
from our users. If you have need of any other API members to expose functionality
that already exists through the command line, please follow our
[feature request process](../usual.md).

---

## Main API

::: pymarkdown.api.PyMarkdownApi
    handler: python
    options:
      heading_level: 3
      show_docstring_examples: true
      filters:
      - "scan_.*"
      - "fix_.*"
      - "list_.*"
      - "application_version"
      - "interface_version"

### Modifiers

All modifiers can be chained together without requiring separate statements.

For example, the following statement is a fluent example of how to use these modifiers
in a function chain:

```Python
  PyMarkdownApi().enable_stack_trace().log_debug_and_above().fix_string("something")
```

More in-depth information about each of these modifiers is
available in our User's Guide section on
[General Command Line Arguments](../user-guide.md#general-command-line-arguments).

::: pymarkdown.api.PyMarkdownApi
    handler: python
    options:
      heading_level: 4
      show_docstring_examples: true
      show_docstring_description: true
      show_docstring_classes: false
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
      members: []

---

::: pymarkdown.api.PyMarkdownScanFailure
    handler: python
    options:
      heading_level: 3
      members: []

---

::: pymarkdown.api.PyMarkdownPragmaError
    handler: python
    options:
      heading_level: 3
      members: []

---

## Fix Results

::: pymarkdown.api.PyMarkdownFixResult
    handler: python
    options:
      heading_level: 3
      members: []

---

::: pymarkdown.api.PyMarkdownFixStringResult
    handler: python
    options:
      heading_level: 3
      members: []

---

## List Results

::: pymarkdown.api.PyMarkdownListPathResult
    handler: python
    options:
      heading_level: 3
      members: []

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
