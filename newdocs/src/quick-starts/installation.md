# Installation

You can run PyMarkdown in two primary ways, depending on how you want to use it
in your workflow:

- through Pre&#x2011;Commit (recommended if your project is stored in Git and you
  want automatic checks before each commit)
- as a local command&#x2011;line tool (installed into a Python environment that
  you control and run manually or from a script)

Most of the Quick Start guides show examples for the local command&#x2011;line tool.
Those command‑line examples are also applicable when configuring PyMarkdown to run
through Pre&#x2011;Commit. However, please read the section below before attempting
any non-standard configuration, because there are important details to understand
first.

## If You Run Into Issues

This Quick Start guide assumes that you can install PyMarkdown without encountering
any issues. If you do run into problems, the full [installation guide](../getting-started.md)
is always available to help you out.

## Use PyMarkdown Through Pre&#x2011;Commit

[Pre&#x2011;Commit](https://pre-commit.com/) is a framework for running checks (such
as linters) before each commit. We strongly recommend using Pre‑Commit with PyMarkdown
because it provides automatic Markdown checks before every commit and helps keep
your Markdown formatting consistent across the project.

If you already use Pre&#x2011;Commit and do not need a separate local installation
of PyMarkdown, skip ahead to the
[Installing Via Pre&#x2011;Commit](../getting-started.md#installing-via-pre-commit)
section for detailed, step‑by‑step instructions.

**Important note:** In a typical setup, Pre&#x2011;Commit passes
**all files in your project** (not just Markdown files) to each configured tool
by default.

More specifically, each `repo` entry in `.pre-commit-config.yaml` will send every
file under the project root (recursively) to the tool (such as PyMarkdown), unless
you restrict the file set with additional Pre&#x2011;Commit settings (for example,
`files` or `exclude`). In this guide, the "project root" is the directory that contains
both your `.git` folder and your `.pre-commit-config.yaml` file.

PyMarkdown's defaults for Pre‑Commit are designed for this "scan all files under
the project root" behavior. By default, PyMarkdown focuses on Markdown files, so
this default setup works correctly for most projects without any extra configuration.

If you need to change these defaults, read the
[Advanced Pre&#x2011;Commit](../advanced_pre-commit.md) documentation first. Changing
Pre‑Commit's file selection settings or PyMarkdown's configuration without understanding
how Pre&#x2011;Commit and PyMarkdown interact can lead to surprising behavior, such
as scanning the wrong files, skipping files you expect to be checked, or running
PyMarkdown less often than you intended.

## Install PyMarkdown Locally

If you prefer to run PyMarkdown directly from the command line, install it into
a Python environment. That environment can be your system&#x2011;wide Python installation,
but in most cases we recommend using a virtual environment created with a tool like
Pipenv or another virtual environment manager.

For additional information about installing PyMarkdown, its prerequisites, and alternative
installation options, see the [Getting Started](../getting-started.md) guide. It
provides more background and advanced configuration examples.

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pip install pymarkdownlnt
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv install pymarkdownlnt
    ```

<!-- pyml enable code-block-style-->

**Note:** If you use a package manager (such as `pipenv`) that separates "development"
dependencies from "runtime" dependencies (for example, packages that are only needed
while you are editing or checking files), you may need to add an option such as
`-d` (for "development") to the install command. This ensures that PyMarkdown is
installed as a development-time tool rather than a library that ships with your
application. See your package manager’s documentation for the exact option name
and usage.

## Verifying PyMarkdown Installation

Use this quick check to confirm that PyMarkdown is installed correctly and that
you can run it from your command&#x2011;line environment without errors. You only
need to perform this check once, after installation or after configuration changes.

<!-- pyml disable code-block-style-->

1. At the base of your project directory (the top‑level folder for your project,
   also called the project root), create a file named `sample.md`.2. Copy the following
   contents into that file and save it:

    ```text
    # First Heading
    # Another First Heading
    ```

    **Note:** This example intentionally contains two top-level headings and no
    blank lines around them. These deliberate formatting problems give PyMarkdown
    clear issues to report when you run the linter, so you can see what rule violations
    look like in practice. Your own documents should avoid these issues; they are
    included here only so you can see what PyMarkdown reports and how to interpret
    the output.

2. From the base of your project directory, run one of the following commands, depending
   on how you installed PyMarkdown:

    === "Global Python Install"

        ```sh
        pymarkdown scan sample.md
        ```

    === "Pipenv Package Manager"

        ```sh
        pipenv run pymarkdown scan sample.md
        ```

3. Compare the output from your command against the following text. The exact wording
   may differ slightly between versions, but the rule IDs and the line and column
   information in your output should match what is shown here:

    ```text
    sample.md:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
    sample.md:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
    sample.md:2:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
    ```

4. If PyMarkdown does not produce output similar to the above (for example, output
   that does not list rule IDs and line numbers, no output at all, or error messages
   about the command), recheck your installation steps and see the [Installation](../getting-started.md#installation)
   section for additional help. Although the exact wording and formatting of the
   messages may vary by version, for each problem that is found you should always
   see a rule ID, a line number, and a short description of the issue. This example
   is mainly a **sanity check** that your installation is working and that PyMarkdown
   can scan files correctly.

<!-- pyml enable code-block-style-->

## Where To Go From Here

- [Quick Start - Home](./index.md) - Main starting point for all Quick Start documents
- [Quick Start - General Command Line Usage](./general.md) - Use of PyMarkdown from
  the command line
- [Quick Start - Scanning Markdown Files](./scanning.md) - Scanning Markdown files
  with PyMarkdown
- [Quick Start - Fixing Markdown Files](./fixing.md) - Fixing Markdown files
  with PyMarkdown
