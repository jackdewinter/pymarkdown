# Quick Start: General Command-Line Usage

This section shows common command-line tasks and how to run them with different
installation methods (a global Python installation or the Pipenv package manager).

If you are not sure whether you installed PyMarkdown with Pipenv, you probably
used a global Python installation. In that case, use the **Global Python Install**
examples.

If you installed using `pipenv install pymarkdown`, use the **Pipenv Package Manager**
examples instead.

In both cases, the underlying PyMarkdown commands and options are the same; only
the way you start `pymarkdown` differs (for example, running it directly vs. running
it through `pipenv run`).

Use this page as your first stop for command-line usage; the concepts here are reused
in most of the Quick Start guides listed at the bottom of the page.

All examples on this page work the same way for both installation methods; select
the tab that matches how you installed PyMarkdown.

## What You Will Learn

> **Quick Start Guide Single Line Summary**
> This page teaches the core command-line skills required for the other Quick Start
> guides, illustrating how to run PyMarkdown and how to discover help for any
> command.

On this page, you will learn how to:

- check which version of PyMarkdown is installed, and
- use `--help` to discover available commands and options.

If you already feel comfortable running PyMarkdown commands, you can skim this page:
read the section titles and examples, and only dive into parts that are new to you.

If you are new to PyMarkdown or new to the command line, **read each section in
order and run the commands as you go**. Each example adds one new idea to the previous
one. Learning them in order will make the other Quick Start guides much easier to
follow.

## Prerequisites

This page assumes that:

- you have installed PyMarkdown by following
  [Quick Start: Installation](./installation.md), and
- you have verified that you can run PyMarkdown from your command line
  (for example, by running `pymarkdown version` and seeing a version number).

If you have not done that yet, complete
[Quick Start: Installation](./installation.md) first. When you can successfully
run `pymarkdown version`, come back to this page and continue with
**Using the Version Command**.

## Using the Version Command

This command displays the installed PyMarkdown version. This is useful for
verifying that you are using the version you expect, especially when you work
on multiple projects or share configuration files with other team members.

Run the following command in a terminal or command prompt:

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

This will return a version number similar to:

<!-- pyml disable code-block-style-->
```text
0.9.35
```
<!-- pyml enable code-block-style-->

## Using General Command-Line Help

To see a summary of available commands and options for PyMarkdown, use the `--help`
option with no other arguments.

Run the following command in a terminal or command prompt:

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

When you run this command, you will see output similar to the following:

<!-- pyml disable code-block-style-->
```text
usage: main.py [-h] [-e ENABLE_RULES] [-d DISABLE_RULES] [--enable-extensions ENABLE_EXTENSIONS] [--add-plugin ADD_PLUGIN]
               [--config CONFIGURATION_FILE] [--set SET_CONFIGURATION] [--strict-config] [--no-json5] [--stack-trace]
               [--continue-on-error] [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}] [--log-file LOG_FILE]
               [--return-code-scheme {default,minimal,explicit}]
               {extensions,fix,plugins,scan,scan-stdin,version} ...

Lint any found Markdown files.

positional arguments:
  {extensions,fix,plugins,scan,scan-stdin,version}
    extensions          extension commands
    fix                 fix the Markdown files in any specified paths
    plugins             plugin commands
    scan                scan the Markdown files in any specified paths
    scan-stdin          scan the standard input as a Markdown file
    version             version of the application

options:
  -h, --help            show this help message and exit
  -e, --enable-rules ENABLE_RULES
                        comma separated list of rules to enable
  -d, --disable-rules DISABLE_RULES
                        comma separated list of rules to disable
  --enable-extensions ENABLE_EXTENSIONS
                        comma separated list of extensions to enable
  --add-plugin ADD_PLUGIN
                        path to a plugin containing a new rule to apply
  --config, -c CONFIGURATION_FILE
                        path to the configuration file to use
  --set, -s SET_CONFIGURATION
                        manually set an individual configuration property
  --strict-config       throw an error if configuration is bad, instead of assuming default
  --no-json5            use stdlib's json reader instead of new JSON5 json reader
  --stack-trace         if an error occurs, print out the stack trace for debug purposes
  --continue-on-error   if a tokenization or plugin error occurs, allow processing to continue
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        minimum level required to log messages
  --log-file LOG_FILE   destination file for log messages
  --return-code-scheme {default,minimal,explicit}
                        scheme to choose for selecting the application return code
```
<!-- pyml enable code-block-style-->

When you run `pymarkdown --help` for now:

- Focus on the **positional commands** (`scan`, `scan-stdin`, `fix`, `plugins`,
  `extensions`, `version`). These are the main actions PyMarkdown can perform.
- Just skim the **options** section so you know it is there. You do not need to
  learn every flag yet.

As you get used to PyMarkdown, you can use this help output as a quick reference
when you forget a command or option.

Use `pymarkdown --help` to see all available commands, then use
`pymarkdown <command> --help` to see the detailed options for a specific command
(as shown in the next section).

For more information on what all these commands and flags are, please read our
[General Command Line Arguments](../user-guide.md#general-command-line-arguments)
section of the User Guide.

## Using Command-Specific Help

Use `pymarkdown --help` to list all commands. Then, for any command in that list,
run `pymarkdown <command> --help` (for example, `pymarkdown scan --help` or
`pymarkdown fix --help`) to see its options.

For the `scan` command, run the following command in a terminal or command prompt:

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

When executed, this will return the following information:

<!-- pyml disable code-block-style-->
```text
usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] [-e PATH_EXCLUSIONS] [--respect-gitignore] path [path ...]

positional arguments:
  path                  one or more paths to examine for eligible Markdown files

options:
  -h, --help            show this help message and exit
  -l, --list-files      list any eligible Markdown files found on the specified paths and exit
  -r, --recurse         recursively traverse any found directories for matching files
  -ae, --alternate-extensions ALTERNATE_EXTENSIONS
                        provide an alternate set of file extensions to match against
  -e, --exclude PATH_EXCLUSIONS
                        one or more paths to exclude from the search. Can be a glob pattern.
  --respect-gitignore   respect any setting in the local .gitignore file.
```
<!-- pyml enable code-block-style-->

Most of the time, you will use the `scan` command together with a few key
options to scan projects, include subdirectories, and skip unwanted folders:

- run `pymarkdown scan .` to scan all Markdown files in the current directory
  (the folder you are "in" when you run the command).
- add `-r` (the `--recurse` option from the help output) to scan subdirectories,
  for example `pymarkdown scan -r .` to scan an entire project.
- use `-e` (the `--exclude` option) to skip build or output directories (for example,
  `-e dist,node_modules`) that you do not control.

The remaining options are for advanced use cases. When you need finer control
over what to scan or how to configure PyMarkdown, see the detailed descriptions
in the user guide.

To go deeper on the commands you will use most often, see:

- [Quick Start: Scanning Markdown Files](./scanning.md)
- [Quick Start: Fixing Markdown Files](./fixing.md)

To see a full overview of these commands and how they are grouped, read
[Available Groups of Commands](../user-guide.md#available-groups-of-commands).

## Where to Go From Here

You now know how to run PyMarkdown and how to discover help for any command.

**Next**, in the Quick Start guide series:

- Use [Quick Start: Scanning Markdown Files](./scanning.md) to apply scan to real
  projects.

**After** you are comfortable with that:

- Use [Quick Start: Fixing Markdown Files](./fixing.md) to learn how to safely apply
  fixes.

**If** you need some review:

- Select [Quick Start: Introduction](./index.md) for an overview of all Quick Start
  guides
- Select [Quick Start: Installation](./installation.md) for the steps required to
  install PyMarkdown
