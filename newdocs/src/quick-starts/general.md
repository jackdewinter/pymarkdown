# General Command-Line Usage

This section shows common command-line tasks and how to run them with different
installation methods (a global Python installation or the Pipenv package manager).
The underlying PyMarkdown commands and options are the same in each case; only the
way you start `pymarkdown` differs (for example, running it directly vs. running
it through `pipenv run`).

In other words, you can think of all the examples as using the same PyMarkdown
commands; just pick the "Global Python Install" or "Pipenv Package Manager"
tab that matches how you installed PyMarkdown.

## Command-Line Help

To see a summary of available commands and options for PyMarkdown, use the `--help`
option with no other arguments. You can combine `--help` with a specific command
(for example, `pymarkdown scan --help`) to see the options for that command.

For more detailed explanations of how PyMarkdown works and all available options,
see the [User Guide](../user-guide.md).

<!-- pyml disable code-block-style-->

=== "Global Python Install"

    ```sh
    pymarkdown --help
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown --help
    ```

<!-- pyml enable code-block-style-->

## Get the Version of PyMarkdown Installed

This command displays the installed PyMarkdown version. This is useful for
verifying that you are using the version you expect, especially when you work
on multiple projects or share configuration files with other team members.

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown version
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown version
    ```
<!-- pyml enable code-block-style-->

## Where to Go From Here

- [Quick Start - Home](./index.md) - Main starting point for all Quick Start documents
- [Quick Start - Installation](./installation.md) - How to Install PyMarkdown
- [Quick Start - Scanning Markdown Files](./scanning.md) - Scanning Markdown files
  with PyMarkdown
