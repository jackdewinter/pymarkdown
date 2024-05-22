# `api` Module

This module is used to interact with the PyMarkdown application through a
programmatic Python interface, instead of through the command line.

Currently, only the `scan` and `scan --list` commands are presented through
this API, as they were the ones most heavily requested. If you need any other APIs
to functionality exposed through the command line, please follow our
[feature request process](../usual.md).

## Main API

::: pymarkdown.api.PyMarkdownApi
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_root_full_path: false
      show_symbol_type_heading: true
      members_order: source

## List Results

::: pymarkdown.api.PyMarkdownListPathResult
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_root_full_path: false

## Scan Results

::: pymarkdown.api.PyMarkdownScanPathResult
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_root_full_path: false

---

::: pymarkdown.api.PyMarkdownScanFailure
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_root_full_path: false

---

::: pymarkdown.api.PyMarkdownPragmaError
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_root_full_path: false

## Exceptions

::: pymarkdown.api.PyMarkdownApiException
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_root_full_path: false

---

::: pymarkdown.api.PyMarkdownApiArgumentException
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_root_full_path: false

---

::: pymarkdown.api.PyMarkdownApiNoFilesFoundException
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_root_full_path: false

---

::: pymarkdown.api.PyMarkdownApiNotSupportedException
    handler: python
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_root_full_path: false
