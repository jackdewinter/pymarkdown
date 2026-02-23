# Scanning Markdown Files

The commands in this section use PyMarkdown’s **scan** mode to check the content
of one or more Markdown files. Any rule violations are reported to the console in
a standard linter-style format.  The output includes the file name, line number,
column number, rule ID, and message, similar to what many code linters use.

For a detailed explanation of that output format (including what each field means
and how to read it), see the [Rule Failure Format](../user-guide.md#rule-failure-format)
section in the User Guide.

## Prerequisites

The following sections assume that you have already [installed PyMarkdown](./installation.md)
and are reasonably comfortable with [command line usage](./general.md). If you are
not, please refer to the links above to help you get started.

## Get Help for the Scan Command

This example command prints help text that describes all the command-line arguments
available in **scan** mode.

For more detailed explanations of how to use **scan** mode, see:

- the [Basic Scanning](../user-guide.md#basic-scanning) section for an overview
  of how PyMarkdown scanning  works in general
- the [Advanced Scanning](../user-guide.md#advanced-scanning) section for specific
  information on **scan** mode options and arguments

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan --help
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan --help
    ```

<!-- pyml enable code-block-style-->

## Scan a Single File

This command scans the file `sample.md` and reports any rule violations that it
finds in that file.

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan sample.md
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan sample.md
    ```

<!-- pyml enable code-block-style-->

## Scan Multiple Files

This command scans the files `sample.md` and `another-sample.md` and reports any
rule violations.

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan sample.md another-sample.md
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan sample.md another-sample.md
    ```

<!-- pyml enable code-block-style-->

## Scan a Directory

This command scans all Markdown files in the current directory (`.`) and reports
any rule violations.

- You can replace `.` with another directory name (for example, `sample`) without
  changing how the command works.
- Trailing `/` characters are optional for directories.

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan .
    ```
    
    or

    ```sh
    pymarkdown scan ./
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan .
    ```

    or

    ```sh
    pipenv run pymarkdown scan ./
    ```

<!-- pyml enable code-block-style-->

## Scan a Directory Recursively

This command scans all Markdown files in the directory `sample/` and in **all of
its subdirectories**, reporting any rule violations that it finds.

- You can use either the long option `--recurse` or the short option `-r` to enable
  recursive scanning.

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan --recurse sample/
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan --recurse sample/
    ```

<!-- pyml enable code-block-style-->

## Scan Glob Paths

Use this command when you want to scan files in directories that match a pattern
instead of listing each path manually. It scans all Markdown files in directories
that match the [glob pattern](https://commandbox.ortusbooks.com/usage/parameters/globbing-patterns)
`**/docs`. In this pattern, `**/` means "match any directory depth under the current
directory". `docs` is the directory name that must appear at the end of the path.
For example, it matches `./docs`, `./project/docs`, and `./project/sub/docs`.

- After the glob pattern is resolved into a list of paths, PyMarkdown filters that
  list. It keeps only files whose names end with `.md`.
- To change which file extensions are scanned, see
  [Alternate Extensions](../user-guide.md#-alternate-extensions-or-ae).

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan **/docs
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan **/docs
    ```

<!-- pyml enable code-block-style-->

## Scan Paths and Exclude Certain Paths and `.gitignore`-Ignored Files

This command scans Markdown files under the glob path `**/docs`, but excludes:

- files ignored by the project’s `.gitignore` file
- files whose names start with `draft_` or `draft-`

These options are useful when you want to enforce rules across most of the project,
but intentionally skip some files. Common examples include draft content, build
artifacts, or temporary files that are listed in .gitignore and are not normally
committed to the repository.

- In **scan** mode, all path arguments must appear at the end of the command line.
  Any options that modify scan behavior must appear between the `scan` keyword and
  the path arguments. In this example, the only path argument is `**/docs`.
- For more information about excluding paths and using `.gitignore`, see:
    - [Excluding Paths](../user-guide.md#-e-exclude-path_exclusions)
    - [Respect .gitignore](../user-guide.md#-respect-gitignore)

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan --respect-gitignore --exclude draft_* --exclude draft-* **/docs
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan --respect-gitignore --exclude draft_* --exclude draft-* **/docs
    ```
<!-- pyml enable code-block-style-->

## Debugging Scan Path Issues

This command shows **which files would be scanned**, without actually running any
rules on those files.

It uses the glob path `**/docs` and excludes files whose names start with `draft_`
or `draft-`. It then prints the list of matching file paths to the console.

- The `--list-files` option is intended specifically for debugging which paths and
  filters are applied before you run the full scan. It helps you experiment with
  **scan** options until they match the files you expect.

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan --list-files --exclude draft_* --exclude draft-* **/docs
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan --list-files --exclude draft_* --exclude draft-* **/docs
    ```
<!-- pyml enable code-block-style-->

## Other Commands

The following commands are available, but were omitted from this quick-start document
because they are too advanced:

- [Scanning From Standard Input](../user-guide.md/#scanning-from-standard-input)
  \- using the **scan-stdin** command to scan Markdown content from the console's
  standard input instead of from a file on disk

## Where to Go From Here?

- [Quick Start - Home](./index.md) - Main starting point for all Quick Start documents
- [Quick Start - Fixing Markdown Files](./fixing.md) - Fixing Markdown files with
  PyMarkdown
