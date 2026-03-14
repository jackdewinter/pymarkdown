---
summary: Guide for users on how to use PyMarkdown.
authors:
  - Jack De Winter
---

# Basic Concepts

This User Guide explains how to use the PyMarkdown linter in day‑to‑day work and
how its main components fit together.

If you already use PyMarkdown regularly and are comfortable with the basics from
[Introduction](./index.md) and [Getting Started](./getting-started.md), you can:

- skim [Nomenclature](#nomenclature) to confirm terminology, then
- jump to [Command Line Basics](#command-line-basics) for CLI structure, or
- go directly to [Basic Fixing](#basic-fixing) and [Extensions](#extensions) for
  **fix** mode and parser extensions.

These pages assume you have at least scanned the content
in the [Introduction](./index.md) document (high‑level overview) and the
[Getting Started](./getting-started.md) document (installation and first runs),
and that you are already comfortable running PyMarkdown on one or more files,
including invoking it from the command line with different options.
This User Guide builds on that foundation instead of repeating it.

This document builds on that foundation to provide targeted information on:

- how the command‑line interface works,
- how Rule Plugins are evaluated,
- how extensions interact with the Markdown parser, and
- how the Rule Engine and parser cooperate during scan and fix operations.

For the canonical definitions of scan and fix behavior, see:

- [Scanning and Scan Mode](#scanning-and-scan-mode) – what a scan run does and does
  not do.
- [Correcting Rule Failures With Fix Mode](#correcting-rule-failures-with-fix-mode)
  – how fixes are produced and applied.

Later sections assume you are familiar with those definitions.

If you would like more hands‑on practice before diving into this guide, work through
the
task‑oriented examples in our [Quick Start guides](./quick-starts/index.md). They
focus on
short, practical scenarios (scan, fix, configuration) that make the concepts in
this User Guide easier to follow.

However, we know we are not perfect. If, after reading the documentation and trying
something out for yourself, you find that there is a problem, a lack of documentation,
or a feature that you believe is missing, please use the process outlined on our
[Reporting Issues](./usual.md) page. We take each submitted issue
seriously and use that feedback to refine Rule Plugins, improve configuration behavior,
and extend the documentation, hoping to grow our project with your support.

## Nomenclature

Here are some words and phrases that we use throughout our documentation.

If you are already familiar with PyMarkdown's terminology (Markdown Parser, Rule
Engine,
Rule Plugins, Rule Failures vs Errors, Scan Mode vs Fix Mode), you can skim this
section
and then jump ahead to [Prerequisites](#prerequisites) and the shared examples.

### Markdown Document / Markdown File

A normal text document that includes Markdown annotations. These documents are typically
stored as Markdown files with a `.md` filename extension.

### Markdown Parser

A core application component that takes a Markdown document and breaks it into Markdown
elements such as headings, lists, code fences, block quotes, and inline emphasis.
The Markdown parser emits a stream of Markdown tokens that can then
be used for specific purposes. In normal operation (**scan** mode), parser extensions
run first
and may adjust or augment that Markdown token stream. The Rule Engine then consumes
the resulting
tokens in a well‑defined order to analyze the document, report Rule Failures, and,
in
**fix** mode, propose content changes.

### Rule Engine

A main application component that takes the stream of Markdown tokens and executes
a series of actions that are based upon those tokens. Each of these actions is implemented
as a rule (see below), and the component that controls the registration, ordering,
and execution of those rules is referred to as the Rule Engine.

### Rules / Rule Plugins

Rule Plugins are the Python code that extends the Rule Engine (via a plugin mechanism)
to look for a
specific behavior on behalf of the user. The Rule Plugins themselves act as mediators
between the logic that enacts a given rule and the Rule Engine that is using the
rule.
Basically, the rule is the logic behind a given check and the Rule Plugin is the
container
around that check.

Each Rule Plugin typically register handlers for specific
token types or parser events, receive those tokens in a deterministic order, and
may expose configuration options that control their behavior (for example, which
paths to ignore or what thresholds to enforce). The rule itself then takes that
information to look for a specific pattern. Looking for that pattern may include
examining a single
token in isolation, maintaining per-document or per-file state, or even correlating
information
across multiple tokens (for example, to compute heading levels or track list nesting).
Examples of this are Rule Plugin `MD010` which looks for hard tabs in the document
and
Rule Plugin `MD012` which looks for consecutive blank lines in the document. In
the built-in
Rule Plugin set:

- the `MD` prefix is used for Rule Plugins that align with rules introduced by `markdownlint`
- the `PML` prefix is used for Rule Plugins introduced by the PyMarkdown application
  to address new requests and scenarios

Additional prefixes may be introduced for other Rule Plugin families over time.

### Rule IDs

Rule IDs are unique identifiers that are associated with a given Rule Plugin. These
Rule
IDs are case-insensitive. Therefore, the Rule IDs `md010`, `MD010`, and `Md010`
all refer
to the same Rule Plugin. For historical reasons, these identifiers start with a
two- or
three-letter prefix, followed by a three-digit suffix, and the combination of prefix
and suffix is unique across all Rule Plugins and across all Rule Plugin families.
These ids are
what you see in command-line output, and they form the canonical identifiers used
in configuration files, logs, and most tooling integrations.

### Parser Extensions

Python code that directly interacts with the Markdown Parser component to provide
a single enhanced Markdown capability. Extensions can introduce new or optional
token types, adjust how existing Markdown constructs are parsed, or add support
for commonly used non-standard syntax (such as task list items, Front-Matter blocks,
or Pragma-style directives that influence parsing or linting behavior). In practice,
a parser extension runs before the Rule Engine sees any tokens, so its changes to
the Markdown token stream are fully visible to every rule, including both built-in
and custom
Rule Plugins. This means that enabling or disabling an extension can change which
tokens a rule sees, how those tokens are structured, and even whether a Rule Plugin
triggers
at all for a given construct, without the rule's logic changing.

### Triggered

When a rule finds an instance of the specific behavior that it is looking for, the
containing Rule Plugin then triggers a failure. There is no general behavior about
the number of times
a rule can be triggered within a single document; some rules report every occurrence,
while others may only report the first occurrence or aggregate multiple issues into
a single failure. The exact triggering behavior for a rule is determined by the
rule's implementation and, in some cases, its configuration options, including options
that suppress reporting in certain regions or for certain patterns.

### Rule Failure

When a rule is triggered, the information that the Rule Plugin produces to provide
specifics
about why it was triggered is called a Rule Failure. A Rule Failure usually includes
at least
the Rule ID, a description, and a location (file, line, and column), and may also
include rule-specific extra data that downstream tools can consume. Rule Failures
are
distinct from errors in that detecting Rule Failures is an expected outcome of executing
the application and indicates a style or policy violation in your Markdown content,
not a defect in PyMarkdown itself or in a rule implementation.

Conceptually, a failure simply means "this content did not meet the constraints
of your configured
Rule Plugins." The rule's logic, combined with configuration (files, command‑line
options,
and any supported Pragmas), defines those guidelines. When a rule reports a failure,
it is signaling a style or policy violation in your Markdown, not an internal error
in PyMarkdown.

### Error

While we try to plan out and test everything, occasionally errors get through. Errors
show that either Python or our own guard code has detected an invalid condition
within our application, one of its extensions, or one of its plugins, such as an
uncaught exception, an assertion failure, or misuse of the public APIs by a custom
Rule Plugin or extension. These conditions are treated as abnormal and typically
cause
the current invocation of PyMarkdown to fail fast (with a non-zero exit code) unless
you have explicitly enabled `--continue-on-error`, in which case the error is reported
but scanning of the remaining files continues.

### Scanning and Scan Mode

A single pass of the PyMarkdown application over one or more files using the `scan`
command. That pass is performed in **scan** mode, with the goal of finding any Rule
Failures
within each Markdown document that was scanned. In **scan** mode, Rule Plugins are
allowed
to emit Rule Failures but are not allowed to modify the document; the original file
contents
remain unchanged. This behavior is intentional so that scan can be safely used in
CI pipelines and read-only environments without any risk of modifying source files.

### Correcting Rule Failures With Fix Mode

Like **scan** mode above but using the `fix` command. The Rule Engine asks any Rule
Plugins
that have the **autofix** capability to automatically fix the Rule Failure they
reported and to
return updated content for the affected regions of the document. The Rule Engine
then merges all accepted fixes into a new version of the file content and writes
that content back to disk. Note that not all Rule Plugins support this feature,
for reasons
discussed in the section on [Basic Fixing](#basic-fixing), which describes how the
`fix`
command executes in **fix** mode, how conflicting or overlapping fixes are resolved,
and how that differs from a normal scan.

## Prerequisites

Since PyMarkdown is a Markdown linter, this documentation assumes that the user
has a working knowledge of Markdown and the annotations used for each element.
In particular, you should already be comfortable with headings, lists, code fences,
links, images, block quotes, and inline emphasis. If in doubt, the [Markdown Guide](https://www.markdownguide.org/)
is a good reference document, with information on each type of Markdown element
and how to use them. As the rest of the documentation assumes that you have knowledge
of Markdown, it is strongly recommended that you at least review the cheat sheet
from the Markdown Guide before continuing.

Note that parser extensions are exempt from that assumption. Because extensions
can change how documents are parsed, their effect on specific Rule Plugins is not
always
obvious. To address this, each extension includes documentation and examples that
show how it affects the Markdown token stream and, when relevant, Rule Plugin behavior.
More information
about the available extensions, the additional tokens they introduce,
and how they interact with Rule Plugins can be found in the [Advanced Extensions](./advanced_extensions.md)
document. That guide serves as a reference for each extension, covering its purpose,
how it changes the parser's Markdown token stream, and any configuration options
or interactions
with specific Rule Plugins. For a high‑level overview before diving into that reference,
see the [Extensions](#extensions) section later in this User Guide.

To avoid repeating similar Markdown snippets throughout this guide, we standardized
on a small set of example files.

For the rest of the documentation, we refer to this directory structure:

```text
base directory
|--- examples
     |--- example-1.md
     |--- example-2.md
|--- README.md
```

The `README.md` file is present for reference and can be any kind of Markdown file
you would use for your projects. For the sake of these examples, we assume that
the `README.md` file always scans cleanly under the default configuration so that
any reported Rule Failures come only from the example files. Within the `examples`
directory
are two files: `example-1.md` and `example-2.md`. The file `example-1.md` has the
content:

```Markdown
## This is an example

Just an example.

```

and the file `example-2.md` has the content:

```Markdown
# This is an example

Just an example.

```

If you prefer concrete files instead of code blocks, these examples are checked
into the [examples directory](https://github.com/jackdewinter/pymarkdown/tree/main/examples)
 of the GitHub project.

These two files are intentionally constructed to demonstrate [Rule MD041](./plugins/rule_md041.md):

- `example-1.md` starts with a level 2 ATX heading and, under the default configuration,
  triggers MD041 on line 1 because the first heading in the file is not level 1.
- `example-2.md` starts with a level 1 ATX heading and does not trigger MD041, because
  its first heading satisfies the Rule Plugin's requirement.

You will see these two files reused in later sections whenever we need simple, stable
examples of heading-related behavior.

## Command Line Basics

**NOTE**: If you are looking for some quick help on how to get started with the
PyMarkdown command line, read our [Quick Start - General Command-Line Usage](./quick-starts/general.md)
guide. If you already understand the basics from that document, you can treat this
section as the reference for how the command-line interface is structured: which
subcommands exist, how to access per-command help, and where command-specific
options are described. For detailed information on how **fix** mode behaves internally
and which Rule Plugins have the **autofix** capability, see [Basic Fixing](#basic-fixing).

If you are unsure what to do on the command line, run:

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

### Return Codes

In the most basic sense, return codes are straightforward: a return code of `0`
means everything succeeded, and a non-`0` return code means there were problems.
Linters complicate that simple model because calling scripts often want to distinguish
between "success" (`0`), "something bad happened but the tool itself is fine" (`1`),
and "something is configured wrong or the tool failed" (`2`).

The available schemes, and how to configure them, are described in the
[Return Code Scheme](#-return-code-scheme-observability) section under Basic
Configuration.

### Available Groups of Commands

When you run the base command with `--help`, the output first lists global arguments
that apply to every command, followed by the available subcommands. At present,
there are six subcommands, displayed in alphabetical order:

- `extensions` - Request information on current extensions.
- `fix` - Fix any Markdown files (where possible) in the specified paths.
- `plugins` - Request information on current Rule Plugins.
- `scan` - Scan any Markdown files in the specified paths.
- `scan-stdin` - Scan the application's standard input as a Markdown file.
- `version` - Return the version of the application.

Conceptually, three of these (extensions, plugins, and version) are inspection commands
used to query the current setup (installed extensions, installed Rule Plugins, and
the application
version).

The other three (scan, scan-stdin, and fix) are action commands that analyze or
modify Markdown files.
The `scan` command instructs PyMarkdown
to scan any specified files for Rule Failures and return a non-zero exit code if
any
Rule Failures are found. The `scan-stdin` command is a variant of the `scan` command
that reads the application's standard input and scans that input as if it were in
a file. The `fix` command is like the `scan` command, but it instructs PyMarkdown's
Rule Engine to try to fix any Rule Failures and write the updated content back to
disk,
potentially changing multiple files in a single invocation.

To see options specific to a single command (instead of the global help), run:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown {command} --help
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown {command} --help
    ```

<!-- pyml enable code-block-style-->

Replace `{command}` with the command you want details about. This per‑command help
shows only the arguments for that command, which is useful both when exploring the
CLI and when fine‑tuning a particular invocation.

In addition to the commands and their arguments, there are arguments that precede
the commands and apply to all the commands. For example:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown --config my-config.json scan examples
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown --config my-config.json scan examples
    ```

<!-- pyml enable code-block-style-->

These arguments are covered in the section
below on [Basic Configuration](#basic-configuration).

### Basic Scanning

**NOTE**: If you are looking for some quick help on how to get started with using
PyMarkdown to scan Markdown files from the command line, read our
[Quick Start: Scanning Markdown Files](./quick-starts/scanning.md) guide.

The PyMarkdown linter is executed by calling the project from the command line,
specifying one or more files and directories to scan for Markdown `.md` files.
The list of files and/or directories presented on the command line must be prefaced
with the `scan` keyword to denote that scanning is needed.

#### Sample Command Lines

The command line for scanning files is very straightforward. Assuming you are in
the `base directory` from [Prerequisites](#prerequisites), two simple command lines
are:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan examples
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan examples
    ```

<!-- pyml enable code-block-style-->

and:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan examples/example-1.md examples/example-2.md
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan examples/example-1.md examples/example-2.md
    ```

<!-- pyml enable code-block-style-->

The first example will scan every Markdown `.md` file in the `examples` directory,
while the second invocation will only scan the two specified files.

To make behavior predictable, PyMarkdown also:

- removes duplicate files if different path arguments resolve to the same filename,
  and
- sorts the final list of files to scan into alphabetical order before any Rule Plugins
  are executed.

This ensures that Rule Plugin behavior and output ordering do not depend on the exact
combination or ordering of path arguments on the command line.

To understand this output, see [Rule Failure Format](#rule-failure-format). That
section breaks
down each part of a line like:

```text
examples\example-1.md:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
```

This failure and its format is described in the following section.

#### Rule Failure Format

Our team decided to adopt a failure format similar to that of other linters, checkers,
and compilers. In all of those tools, the first fields identify the file, the location
within the file (line and column), and a unique code for the reported failure.
After that, each tool diverges into its own format to provide additional details
that are specific to that tool.

Keeping to that format, the output format for any PyMarkdown failure is as follows:

`file-name:line:column: rule-id: description {extra-information} (aliases)`

For the formal definition and behavior of a Rule Failure, see [Rule Failure](#rule-failure).

Breaking it down into its constituent parts:

- `file-name` - Path to the file that triggered the Rule Plugin.
    - This is the path as resolved by PyMarkdown after all globbing, recursion,
      and filtering (for example, `--exclude` and `--respect-gitignore`) have been
      applied.
- `line`/`column` - Position in the file where the Rule Plugin was triggered.
    - Uses a 1-based line index and a 1-based column index that align with what
      you see in a typical text editor.
- `rule-id` - Unique identifier assigned to the Rule Plugin, such as `MD013`.
    - These identifiers follow the pattern described under [Rule Ids](#rule-ids)
      and are stable across versions unless a Rule Plugin is explicitly deprecated
      and replaced. Any such deprecations are called out in the Rule Plugin documentation.
- `description` - Human readable summary of the failure.
    - Intended to be short enough to consume directly from logs or CI output without
      always needing to open the Rule Plugin documentation.
- `extra-information` - Optional information the provides more context regarding
  the Rule Feialure being reported.
- `aliases` - One or more aliases used to reference the Rule Plugin in configuration,
  Pragmas, and command line options.
    - These aliases are the same strings you can pass to `--enable-rules` / `--disable-rules`
      (see [Basic Configuration](#basic-configuration)) and to Pragma directives
      (see [Pragma Extension](#pragma-extension)).

Using the output from the command line from the last section, that scan output reports
one failure that occurred in the file `examples\example-1.md` on line 1 at
column 1. The Rule Id of the Rule Plugin that triggered it is `MD041`, also known
by the human
readable aliases `first-line-heading` and `first-line-h1`. The text associated with
this Rule Plugin's Rule Failure is:

> First line in file should be a top level heading

Looking back at the text for `example-1.md`, the first line of that file
is:

```Markdown
## This is an example
```

which shows an ATX Heading with a level of 2. A simple reading of the failure text
indicates that Rule Plugin `MD041` is okay with the first line being a heading,
but it
wants that heading to be a level 1 or top-level heading. Looking at the text from
`example-2.md`, the first line is:

```Markdown
# This is an example
```

As the `example-2.md` file is not mentioned in the output, it makes sense that PyMarkdown's
Rule Plugin `MD041` did not have any issue with a level 1 ATX Heading, largely confirming
the above assumption that the application of Rule Plugin `MD041` matches its stated
intent.

To confirm how MD041 behaves:

- For the Rule Plugin's design and examples, read [Rule Plugin MD041](./plugins/rule_md041.md#reasoning).
- To see how MD041 is configured in your installation (and whether it supports **fix**
  mode), run `pymarkdown plugins info MD041`; the [Plugin Command](#plugin-command)
  section shows sample output.

### Advanced Scanning

Advanced scanning builds directly on the basic scanning behavior described in the
[Basic Scanning](#basic-scanning) section and the command structure introduced under
[Command Line Basics](#command-line-basics). Before enabling these advanced options,
you should be comfortable with core concepts such as paths, globbing, recursion,
and Rule Failure output. With that background, the advanced options are easier to
predict and configure correctly.

Conceptually, advanced scanning options control two things:

- how PyMarkdown discovers candidate files, and
- how it filters that list down to the files it will actually scan.

#### Command Line Arguments

As far as the command line interface for scanning goes, we have tried to make the
advanced options easy to understand. The rest of this section shows the pymarkdown
scan usage synopsis and then describes each advanced flag in turn.

```txt
usage: pymarkdown scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS]
          [-e PATH_EXCLUSIONS] [--respect-gitignore]
          path [path ...]

positional arguments:
  path                  one or more paths to examine for eligible Markdown files

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-files      list any eligible Markdown files found on the specified paths and exit
  -r, --recurse         recursively traverse any found directories for matching files
  -ae ALTERNATE_EXTENSIONS, --alternate-extensions ALTERNATE_EXTENSIONS
                        provide an alternate set of file extensions to match against
  -e, --exclude PATH_EXCLUSIONS
                        one or more paths to exclude from the search. Can be a
                        glob pattern.
  --respect-gitignore   respect any setting in the local .gitignore file.
```

##### --list-files or -l

The `-l` or `--list-files` argument instructs PyMarkdown to only list the files
it would scan if this argument was not present, and then exit the application without
scanning those files. This is useful when using more complicated `path` arguments,
because it lets you confirm that the filenames you expect match the ones PyMarkdown
will scan.

It is especially helpful when debugging path or exclude patterns in scripts and
continuous integration (CI) pipelines, where you may not see or log the exact list
of resolved files but still want to verify how PyMarkdown's path resolution and
filtering logic behaves. Our team treats `--list-files` as the "dry run" mode of
the scanner: it shows you what would be processed without actually running any Rule
Plugins.
Combined with the [`--return-code-scheme`](#-return-code-scheme-observability) options
from
[Basic Configuration](#basic-configuration), you can decide whether a `--list-files`
"dry run"
should fail CI. For example, using the `minimal` scheme lets you run
`pymarkdown scan --list-files`
in pipelines without treating "no files to scan" as an error.

##### --recurse or -r

Use `--recurse` when you want PyMarkdown to search entire directory trees under
the starting paths. In this mode, every subdirectory is visited before any filtering
is applied.

After traversal, PyMarkdown applies extension filtering and any `--exclude` or `--respect-gitignore`
arguments to decide which files to scan. This design keeps the discovery logic simple
but means the runtime cost grows with the total number of directories. To keep scans
fast in large repositories, combine `--recurse` with `--exclude` to skip build outputs,
third-party code, or other non-source directories.

##### --alternate-extensions or -ae

The `-ae` or `--alternate-extensions` argument instructs PyMarkdown to use an alternate
set of filename extensions when looking for Markdown files. By default, PyMarkdown
only processes files that have an `.md` extension. This argument allows for that
set of filename extensions to be replaced with a comma-separated list of filename
extensions.

Each filename extension:

- must start with a `.` character, and
- must be followed by one or more alphanumeric characters.

The resulting set of extensions is applied uniformly to all discovered files, whether
they were found via explicit paths, glob patterns, or recursion. When you specify
`--alternate-extensions`, that set completely replaces the default `.md`‑only behavior.
For example, `--alternate-extensions=.mdown,.markdown` causes `.md` files to be
ignored. To keep `.md` files in scope, you must include `.md` in the list, such
as `--alternate-extensions=.md,.mdown,.markdown`.

In summary:

- The default extension set is `.md` only.
- `--alternate-extensions` replaces, rather than augments, that set.
- The replacement applies to all discovered files during the current invocation,
  regardless of which directories or paths are being scanned.

##### -e, --exclude PATH_EXCLUSIONS

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Available: Version 0.9.30**

The `-e` or `--exclude` argument removes matching files and directories from the
set that PyMarkdown would otherwise scan. You can specify this option multiple times,
once per pattern, which is useful when patterns contain characters that make a comma-separated
list hard to read or parse.

At a high level, `--exclude` behaves like a set of `.gitignore-style` patterns applied
**after** PyMarkdown discovers candidate paths.

Internally, PyMarkdown evaluates these patterns using the [py-walk](https://github.com/pacha/py-walk)
package:

- It first expands the path arguments (including any globs and recursion) into a
  list of candidate paths.
- It then passes that list to py-walk's matcher.
- Any path that matches an exclude pattern is removed from the final list of files
  to scan.

If you are unsure why a file is being skipped or included, combine `--exclude`
with `--list-files` (described above) to see which paths survive filtering, and
compare that list against your configuration from [Basic Configuration](#basic-configuration).

##### --respect-gitignore

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Available: Version 0.9.35**

The `--respect-gitignore` flag tells PyMarkdown to ask Git which files are ignored,
so `.gitignore` rules are applied exactly as they would be by Git itself. With this
flag enabled, any file that Git marks as ignored is excluded from scanning.

When you use `--respect-gitignore`, PyMarkdown must be able to run the Git executable.
If Git is not available or returns an error, PyMarkdown treats that as a failure
instead of silently ignoring the flag. This ensures that your scan results always
reflect the same ignore rules that Git applies to the repository.

In CI environments where Git is not available or the extra startup cost is unacceptable,
prefer
multiple `--exclude` patterns instead of `--respect-gitignore`. To control how these
situations
affect pipeline status, adjust [`--return-code-scheme`](#-return-code-scheme-observability)
in
[Basic Configuration](#basic-configuration); for example, the `minimal` scheme avoids
failing
builds solely because no files were scanned.

##### path

The scan command accepts one or more path arguments. Paths that contain a `?` or
`*` character are passed to Python's [glob module](https://docs.python.org/3/library/glob.html)
and treated as glob patterns; paths without wildcards are treated as literal files
or directories. Recursive traversal is controlled exclusively by `--recurse`, so
PyMarkdown does not use `glob.glob(..., recursive=True)`.

This behavior is consistent with the basic examples in [Basic Scanning](#basic-scanning),
where `pymarkdown scan examples` and `pymarkdown scan examples/example-1.md` both
rely on the same glob rules and extension filtering, just with different initial
paths.

By default, PyMarkdown only processes files whose names end with `.md`. This means
you can scan a directory by passing `.` or `examples` instead of writing `./*.md`.

Conceptually, PyMarkdown uses two stages to decide which files to scan:

- **Discovery:** globs and path arguments (along with `--recurse`) determine which
  filesystem entries are considered at all.
- **Filtering:** the extension filter (the default `.md` set, or your `--alternate-extensions`)
  and any exclude mechanisms (`--exclude` and `--respect-gitignore`) decide which
  of those entries are treated as Markdown candidates.

The advanced flags in this section simply modify one of these two steps: they either
change how entries are discovered or how the discovered entries are filtered.

In practice, this separation makes it easier to combine broad globs with narrow
filtering. For example, you can use `**/*` to discover all files and then rely on
the extension filter to limit which files are actually parsed and linted, instead
of encoding that logic into complex glob patterns.

#### Scanning From Standard Input

From time to time, it may be necessary to take the output from an application that
generates Markdown and pass it directly into PyMarkdown as standard input. In that
situation, use the `scan-stdin` command to accept that input and scan it as a normal
Markdown document.

`scan-stdin` differs from `scan` in one key respect: it has no positional (path)
arguments because all content comes from standard input. Everything else is the
same. All general command-line options (such as configuration and Rule Plugin enable/disable
arguments) still apply and are interpreted exactly as they are for the `scan` command,
including configuration file loading, any `--enable-rules` or `--disable-rules`
arguments, and the return code scheme.

In practice, you can treat `scan-stdin` as another input source for the Rule Engine
rather than a separate mode with different behavior.

Here is a really simple example of this command in action. Assuming that we have
a simple program called "my-program" that generates Markdown as its output, we can
invoke PyMarkdown in this manner:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    my-program some-args | pymarkdown scan-stdin
    ```

=== "Pipenv Package Manager"

    ```sh
    my-program some-args | pipenv run pymarkdown scan-stdin
    ```

<!-- pyml enable code-block-style-->

Note that as a simple workaround, you may decide to pipe that standard input into
a file and then use PyMarkdown to scan that file. However, we felt that was inefficient
and [kludgy](https://en.wikipedia.org/wiki/Kludge), so this feature was added.

### Basic Fixing

**NOTE**: If you are looking for some quick help on how to get started with using
PyMarkdown to scan Markdown files from the command line, read our
[Quick Start: Fixing Markdown Files](./quick-starts/fixing.md) guide. If you already
understand the basics from that document, you can treat this section as the
reference for how **fix** mode behaves internally and which Rule Plugins have the
**autofix**
capability.

If you are already comfortable with how `scan` works from
[Basic Scanning](#basic-scanning) and [Advanced Scanning](#advanced-scanning),
you can treat this section as "what changes when you use `fix` instead of `scan`".

The two main differences are:

- Not every Rule Plugin supports the **autofix** capability called to fix issues.
  The criteria for allowing a Rule Plugin to modify files are listed in
  [Strict Rules for a Rule Plugin to Have the Autofix Ability](#strict-rules-for-a-rule-plugin-to-have-the-autofix-ability).
- PyMarkdown will only emit a small amount of information when it applies fixes,
  informing you only that content within a given file was fixed, not specifically
  what content was fixed.

Because of these differences, you should treat **fix** mode as a mechanical assistant
for well-defined formatting changes rather than a general-purpose "auto-correct"
for arbitrary Markdown problems.

#### Strict Rules for A Rule Plugin To Have The Autofix Ability

Before coding the **autofix** capability for any Rule Plugin, the Rule Plugin author
must be able to answer these questions in the positive:

- Is the proposed fix a purely mechanical change that is easily documented and predictable?
- According to the [GitHub Flavored Markdown](https://github.github.com/gfm)
  specification, does the fix only change formatting, without changing the content?
- Is the proposed fix unambiguous even when applied repeatedly across the document
  (that is, deterministic and idempotent, with no hidden side effects)?

If any of these answers is not "yes", that Rule Plugin is not allowed to support
the **autofix** capability. In particular:

- Rule Plugins must not silently rewrite content in a way that could change the
  document's meaning.
- Running `pymarkdown fix` multiple times on the same file must yield the same result;
  once all fixes are applied, subsequent runs must not introduce further changes.

Any fix that depends on guessing the author's intent typically introduces complex,
brittle logic and is hard to prove safe. Because Markdown has many edge cases, we
treat those intent‑dependent fixes as too risky and do not allow them to possess
**autofix** capabilities.

##### Examples

###### Positive - Rule Plugin MD019 - no-multiple-space-atx

[Rule Plugin MD019](./plugins/rule_md019.md), or `no-multiple-space-atx`, looks
for extra
spaces between the `#` characters and the heading text in an ATX heading.

This behavior follows the [GitHub Flavored Markdown ATX heading specification](https://github.github.com/gfm/#atx-headings):

> The opening sequence of # characters must be followed by a space or by the end
> of line.

Rule Plugin `MD019` treats cases where "followed by a space" becomes "followed by
many
spaces" as Rule Failures.

For a Rule Plugin to possess the **autofix** capability, all three requirements
are satisfied. The fix collapses any run
of multiple spaces between the opening `#` sequence and the heading text to a single
space. This change only affects formatting and does not alter the content. Its behavior
is fully deterministic and idempotent: once the excess spaces are removed, running
**fix** mode again does not change the heading.

###### Negative - Rule Plugin MD025

In contrast to Rule Plugin `MD019`, [Rule Plugin MD025](./plugins/rule_md025.md)
(`single-title`)
enforces that each Markdown document has a single title. In practice, this means:

- The document has exactly one level‑1 heading, or
- The document has a title field in its [Front-Matter](./extensions/front-matter.md#summary),
  which PyMarkdown also treats as the document title when the Front-Matter Extension
  is enabled.

When we considered adding the **autofix** capability for `MD025`, we quickly ran
into a problem. Deciding
which heading represents the "real" title requires guessing the author's intent.
For example, if a document has multiple level‑1 headings, the Rule Plugin cannot
reliably
determine which one to keep or how to adjust the others.

Because any automatic change would involve choosing which title the author "really"
intended, `MD025` fails the third requirement: the fix would not be unambiguous
or safe to apply everywhere. As a result, `MD025` is intentionally detection‑only.
It reports Rule Failures, but any fixes should be made manually or by higher‑level
refactoring tools rather than via PyMarkdown's **fix** mode.

#### Rule Plugins With Autofix

**NOTE:** You don't need to memorize this list &mdash; use it as a reference. It
is also colocated in our
[Quick Start: Fixing Markdown Files](./quick-starts/fixing.md#rule-plugins-with-autofix)
guides.

For quick reference, these are the built-in Rule Plugins that currently support
the **autofix**
capability in the latest released version of PyMarkdown:

- The first column presents the Rule Plugins's Rule ID and a link to that Rule Plugin's
  `Fix Description` heading in the documentation.
- The second column presents the human-readable identifiers that are also used to
  identify the Rule Plugin.
- The third column contains a short description of the Rule Plugin itself.

Because this list can change between releases, treat it as a version dependency.
Before relying on
**fix** mode in CI or other automation:

- Pin the PyMarkdown version (check with [`pymarkdown version`](#version-command)).
- Verify fix support for the Rule Plugins you care about using
  [`pymarkdown plugins list`](#list-subcommand)
  or [`pymarkdown plugins info <rule>`](#info-subcommand).
- After upgrading, review this table or the per‑rule documentation to confirm which
  Rule Plugins still
  support the **autofix** capability.

These steps help you avoid unexpected changes in fix behavior when you move between
PyMarkdown versions.

<!-- pyml disable line-length-->

| Rule ID & Link | Human-Readable Identifier | Short Description |
| -- | -- | -- |
| [MD001](./plugins/rule_md001.md#fix-description) | `heading-increment`, `header-increment` | Heading levels should only increment by one level at a time. |
| [MD004](./plugins/rule_md004.md#fix-description) | `ul-style` | Inconsistent Unordered List Start style. |
| [MD005](./plugins/rule_md005.md#fix-description) | `list-indent` | Inconsistent indentation for list items at the same level. |
| [MD007](./plugins/rule_md007.md#fix-description) | `ul-indent` | Unordered list indentation. |
| [MD009](./plugins/rule_md009.md#fix-description) | `no-trailing-spaces` | Trailing spaces. |
| [MD010](./plugins/rule_md010.md#fix-description) | `no-hard-tabs` | Hard tabs. |
| [MD013](./plugins/rule_md013.md#fix-description) | `line-length` | Line length. |
| [MD019](./plugins/rule_md019.md#fix-description) | `no-multiple-space-atx` | Multiple spaces are present after hash character on Atx Heading. |
| [MD021](./plugins/rule_md021.md#fix-description) | `no-multiple-space-closed-atx` | Multiple spaces are present inside hash characters on Atx Closed Heading. |
| [MD023](./plugins/rule_md023.md#fix-description) | `heading-start-left`,`header-start-left` | Headings must start at the beginning of the line. |
| [MD027](./plugins/rule_md027.md#fix-description) | `no-multiple-space-blockquote` | Multiple spaces after blockquote symbol. |
| [MD029](./plugins/rule_md029.md#fix-description) | `ol-prefix` | Ordered list item prefix. |
| [MD030](./plugins/rule_md030.md#fix-description) | `list-marker-space` | Spaces after list markers. |
| [MD035](./plugins/rule_md035.md#fix-description) | `hr-style` | Horizontal rule style. |
| [MD037](./plugins/rule_md037.md#fix-description) | `no-space-in-emphasis` | Spaces inside emphasis markers. |
| [MD038](./plugins/rule_md038.md#fix-description) | `no-space-in-code` | Spaces inside code span elements. |
| [MD039](./plugins/rule_md039.md#fix-description) | `no-space-in-links` | Spaces inside link text. |
| [MD044](./plugins/rule_md044.md#fix-description) | `proper-names` | Proper names should have the correct capitalization. |
| [MD046](./plugins/rule_md046.md#fix-description) | `code-block-style` | Code block style. |
| [MD047](./plugins/rule_md047.md#fix-description) | `single-trailing-newline` | Each file should end with a single newline character. |
| [MD048](./plugins/rule_md048.md#fix-description) | `code-fence-style` | Code fence style should be consistent throughout the document. |

<!-- pyml enable line-length-->

#### Fix Examples

The [Fix a Single File](./quick-starts/fixing.md#fix-a-single-file) section in our
Quick Start guide covers the practical steps for applying **fix** mode to a
single file, including how fixes are reported and how to re-scan for Rule Failures
after applying **fix** mode.
This section focuses on how that behavior fits into the broader Rule Engine model.
Internally, **fix** mode uses the same Rule Engine as **scan** mode (see [Basic Scanning](#basic-scanning)):
every enabled Rule Plugin runs, but only Rule Plugins listed in
[Rule Plugins With Autofix](#rule-plugins-with-autofix)
are allowed
to modify content. After a fix run, a follow‑up scan should report only:

- Rule Failures from Rule Plugins that do not support the **autofix** capability,
  or
- issues that cannot be fixed automatically.

For a concrete walkthrough of this pattern, see [Fix a Single File](./quick-starts/fixing.md#fix-a-single-file).

Remember that only the Rule Plugins listed in [Rule Plugins With Autofix](#rule-plugins-with-autofix)
can modify files; all other enabled Rule Plugins still behave as scan-only checks.
In practice, this means you can safely run pymarkdown fix over a directory tree
and expect only well‑defined, mechanical formatting changes from those **autofix**
capable Rule Plugins.

Other command lines that are more complex are:

- find all Markdown files in any `docs` directory and fix them if possible:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown fix **/docs
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown fix **/docs
    ```

<!-- pyml enable code-block-style-->

- find all Markdown files that do not have the `draft` prefix in any `docs` directory,
  focusing only on files that will be commited to the Git repository and fix them
  if possible, so that only "publishable" documentation in tracked paths is subject
  to enforcement:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown fix --respect-gitignore --exclude draft_* --exclude draft-* **/docs
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown fix --respect-gitignore --exclude draft_* --exclude draft-* **/docs
    ```
<!-- pyml enable code-block-style-->

### Extensions

Extensions are features that go beyond the base [GitHub Flavored Markdown](https://github.github.com/gfm/)
(GFM) specification. Some are defined there as optional extensions; others are additional
features implemented by PyMarkdown.

These features change how the Markdown parser breaks a document into its constituent
elements. Enabling an extension can introduce new element types (for example, table
cells) or reinterpret existing structures (for example, treating a YAML block as
Front-Matter instead of a paragraph). In turn, this affects which tokens the Rule
Engine receives and which Rule Plugins may trigger.

Because of these effects, advanced configurations should be tested with representative
documents. This ensures that Rule Plugin behavior, reported positions, and any apparent
"missing" or "extra" Rule Failures still align with your expectations.

In this section, we provide only high-level information about each extension to
give you solid footing before diving into the detailed reference.

For more detailed information on configuring extensions (for example, enabling them
via configuration
files rather than the command line), see [Advanced Configuration – Extensions](./advanced_configuration.md#extensions).
For a complete behavioral reference for each extension &mdash; including tokens
added and interactions with
Rule Plugins &mdash; see [Advanced Extensions](./advanced_extensions.md).

#### Enabling Extensions

On the command line, use `--enable-extensions` followed by a comma-separated list
of extension identifiers to enable those extensions. As all extensions other than
the [Pragma extension](#pragma-extension) are disabled by default, there is no command
line ability to disable extensions, only enable them.

#### Specification Extensions

Some parts of the GitHub Flavored Markdown specification are defined as optional
extensions that a GFM-compliant parser may support.

If you enable one of these extensions, PyMarkdown will recognize the corresponding
syntax in your Markdown and apply the changes defined by that extension when parsing
the document. These are most useful when:

- Your documentation already uses GFM-style tables, task lists, or strikethrough.
- You want PyMarkdown to lint raw HTML usage more strictly according to GFM's
  disallowed HTML rules.
- You need link detection that matches GFM's extended autolink behavior.

The five specification extensions are:

<!-- pyml disable-num-lines 7 line-length-->
| Extension | GFM Link | Description |
| --- | --- | --- |
| [Tables](./advanced_extensions.md#markdown-tables) | [GFM](https://github.github.com/gfm/#tables-extension-) | Tables using the \| character. |
| [Task List Items](./advanced_extensions.md#task-list-items) | [GFM](https://github.github.com/gfm/#task-list-items-extension-) | Task list items using the `[` and `]` characters in list markers. |
| [Strikethrough](./advanced_extensions.md#strikethrough) | [GFM](https://github.github.com/gfm/#strikethrough-extension-) | Strikethrough using the `~` character. |
| [Extended Autolink](./advanced_extensions.md#autolinks-extended) | [GFM](https://github.github.com/gfm/#autolinks-extension-) | Extended autolink rules. |
| [Disallowed HTML](./advanced_extensions.md#disallowed-raw-html) | [GFM](https://github.github.com/gfm/#disallowed-raw-html-extension-) | HTML elements that are purposefully disallowed as being dangerous. |

**NOTE:** The links in the first column all point into the [Advanced Extensions](./advanced_extensions.md)
reference, where you can find detailed behavior, examples, and any extension‑specific
configuration.

Note that these are extensions to the specification itself. Parsers may not support
these extensions, or only support them with specific configuration enabled. This
will vary on a parser-by-parser basis.

#### Requested Extensions

Unlike the specification extensions, these extensions do not originate from a formal
Markdown specification. They were added to PyMarkdown to address practical needs
that came up in real-world use.

In broad terms:

- The Front-Matter Extension treats a leading YAML block as metadata and removes
  it from the Markdown token stream, aligning PyMarkdown's view of the document
  with tools
  like MkDocs.
- The Pragma Extension allows inline instructions in comments to enable or disable
  specific Rule Plugins over selected line ranges, without changing how the Markdown
  itself is parsed.

<!-- pyml disable-num-lines 4 line-length-->
| Extension | Enabled By Default | Description |
| --- | --- | --- |
| [Front-Matter](./extensions/front-matter.md) | No | YAML Front-Matter for files. |
| [Pragmas](./extensions/pragmas.md) | Yes | Pragmas to control triggering of Rule Plugins within files. |

##### Front-Matter Extension

The [Front-Matter](./extensions/front-matter.md) extension (id of `front-matter`
and disabled by default) allows for an optional YAML Front-Matter block to be inserted
at the first line of the document. For applications that aggregate Markdown pages
into a condensed form (such as a web site), having such a Front-Matter block is
useful in conveying information from the Markdown document to that application.
This is indeed the case with the [MkDocs application](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data)
used to aggregate our Markdown documents into this documentation web site.

For example, depending on the documentation you are trying to write, you could use
the MkDocs application along with a Markdown document with the following Front-Matter:

```Markdown
---
title: My First Article
authors:
    - Clark Kent
date: 1938-04-18
---
This is the first paragraph of the document.
```

Without this extension enabled, PyMarkdown interprets the first and sixth lines as
thematic breaks and treats lines 2 through 5 as a paragraph. When MkDocs aggregates
this document, it instead displays content starting at `This is the first...` and
uses the Front-Matter YAML purely as metadata. In particular, MkDocs uses the title
field as the document title and ignores the other fields unless they are referenced
by a theme.

This matches the behavior of the [MkDocs application](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data),
which uses the Front-Matter block as metadata and starts rendering at the first
Markdown paragraph.
To align with that, when this extension is enabled PyMarkdown treats the Front-Matter
block as metadata
and removes it from the Markdown token stream that rules evaluate.

When this extension is enabled:

- Rules effectively "start" at the first line after the Front-Matter.
- Line and column positions in Rule Failures are still computed relative to the original
  file, not to a version with Front-Matter stripped, so diagnostics stay aligned
  with the on‑disk file while matching what an aggregating tool such as MkDocs renders.

##### Pragma Extension

The [Pragma](./extensions/pragmas.md) extension (id of `linter-pragmas`, enabled
by default) allows for the introduction of special instructions into the Markdown
document. These instructions can then be used by PyMarkdown to ask for special treatment
for parts of the document rather than the entire document. This feature is analogous
to the `suppress` or `ignore` features of other linters and checkers.

**Important Note:** Pragmas are implemented as an extension because they modify the
Markdown document **before** it reaches the parser and then remove themselves. As
a result, Pragmas are not visible to the Markdown parser at all.

Instead, Pragmas only affect the behavior of the Rule Engine. They dynamically
enable or disable Rule Plugin triggering over specific line ranges. They do not change
the underlying Markdown content or how it is parsed.

This design guarantees that Pragmas never alter the Markdown structure (for example,
heading levels or list nesting). Pragmas only control which parser outputs the Rule
Engine processes and therefore which Rule Failures are emitted or suppressed for
a given
region of the document.

To see how this works in practice, consider the following Markdown snippet:

```Markdown
#  My Bad Atx Heading
```

When scanned, this file will trigger a `MD019` (or `no-multiple-space-atx`) failure
due to the two spaces between the `#` character and the following `M` character.
The Pragmas in the examples below only change whether that failure is reported;
they do not change the content of the heading or how it is parsed.

The first is the simplest: disable it only for the [next line](./extensions/pragmas.md/#disable-next-line-command):

```Markdown
<!-- pyml disable-next-line no-multiple-space-atx-->
#  My Bad Atx Heading
```

The second disables the Rule Plugin for a specific [number of lines](./extensions/pragmas.md/#disable-num-lines-command):

```Markdown
<!-- pyml disable-num-lines 1 blanks-around-fences-->
#  My Bad Atx Heading
```

The final example disables the Rule Plugin for an [entire region](./extensions/pragmas.md#disable-command-and-enable-command),
then re‑enables it. The linked sections provide the full syntax and edge‑case behavior
for each Pragma type.

```Markdown
<!-- pyml disable no-multiple-space-atx-->
#  My Bad Atx Heading
<!-- pyml enable no-multiple-space-atx-->
```

Care must be taken when using these Pragmas to disable triggering of Rule Failures
by the Rule Engine. There are three things to keep in mind:

- Pragmas can only *disable* and *enable* the triggering of Rule Failures for Rule
  Plugins that are already enabled. In other words, in the above example, Rule Plugin
  `MD019` must already be enabled for the Pragma to have any effect.
- More specific Pragmas (`disable-next-line` and `disable-num-lines`) are applied
  first, and then the region Pragmas (`disable` and `enable`). Because of this precedence,
  we do not suggest using both forms of Pragmas in the same document, as it can
  be difficult to reason about which Pragma is currently in effect.
- Region Pragmas (`disable` and `enable`) do not stack. You can have two disable
  region Pragmas that disable Rule Plugin `MD019`, and a single matching enable region
  Pragma reactivates that Rule Plugin, rather than requiring one enable per disable.

These keep Pragma evaluation simple and predictable: PyMarkdown effectively tracks
a single on/off state per Rule Plugin based on the most recent applicable region
Pragma and then applies any more specific one-line Pragmas on top of that for the
affected lines, without maintaining a nested stack of disable/enable scopes.

#### Extension Examples

The two most frequently enabled extensions are for Markdown Tables and for
Front-Matter. Most Markdown implementations support tables, and many systems that
consume
Markdown and aggregate it into other formats use YAML Front-Matter to carry extra
information about the documents being aggregated.

Modifying our simple example of scanning all Markdown files in every `docs` directory,
we get the following command line, which explicitly enables only the extensions
needed for Front-Matter and tables while leaving other extensions at their existing
enabled/disabled defaults:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown --enable-extensions front-matter,markdown-tables scan **/docs
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown --enable-extensions front-matter,markdown-tables scan **/docs
    ```
<!-- pyml enable code-block-style-->

For more advanced information &mdash; such as the exact tokens each extension introduces
and how those tokens
interact with specific rules &mdash; see [Advanced Extensions](./advanced_extensions.md).

### Rule Plugins

Rule Plugins are the code containers for the rules that power PyMarkdown's scanning
ability.
Those Rule Plugins allow the Rule
Engine to look for Markdown patterns or structures that it considers sub-optimal.

#### What Rule Plugins Do

Unlike extensions, which modify or enrich the parser's Markdown token stream, rules
only consume those tokens
and report Rule Failures (or propose fixes in **fix** mode). Their scope ranges
from detecting long lines in
the document ([Rule Plugin MD013](./plugins/rule_md013.md)), through identifying
superfluous blank lines
([Rule Plugin MD012](./plugins/rule_md012.md)), to detecting what looks like a missed
Markdown ATX Heading
annotation ([Rule Plugin MD018](./plugins/rule_md018.md)).

For configuration details &mdash; such as enabling/disabling specific Rule Plugins
or changing their options &mdash; see
[Advanced Configuration – Rule Plugins](./advanced_configuration.md#rule-plugins).

For a deeper look at each Rule Plugin's behavior, rationale, and examples, use
[Advanced Rule Plugins](./advanced_plugins.md).

#### Enabling And Disabling Rule Plugins

Instead of starting from the complete [Rule Plugins list](./rules.md), most users
begin by scanning their repository and then selectively turning Rule Plugins on
or off based on what they see. This subsection focuses on how to enable or disable
Rule Plugins from the command line; later sections and references cover configuration
files and per‑line suppression with Pragmas.

On the command line, use `-d` or `--disable-rules` with a comma-separated list of
Rule IDs or aliases to disable Rule Plugins, and `-e` or `--enable-rules` to enable
them. Rules may be disabled by default for two main reasons:

- They introduce new behavior or apply only in niche scenarios.
- They have been replaced by a newer Rule Plugin, and we avoid enabling two competing
  implementations of the same check at the same time.

##### Example

For example, if you prefer not to enforce long lines and extra blank lines in a
Markdown document, you can disable the corresponding Rule Plugins by id or by alias:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    # disable by Rule Plugin id
    pymarkdown -d MD012,MD013 scan examples
    
    # or, disable by Rule Plugin aliases:
    pymarkdown -d no-multiple-blanks,line-length scan examples
    ```

=== "Pipenv Package Manager"

    ```sh
    # disable by Rule Plugin id
    pipenv run pymarkdown -d MD012,MD013 scan examples

    # or, disable by Rule Plugin aliases:
    pipenv run pymarkdown -d no-multiple-blanks,line-length scan examples
    ```
<!-- pyml enable code-block-style-->

##### A Word Of Caution

Use caution when enabling Rule Plugins that are disabled by default.

By design, the default set of enabled Rule Plugins does not conflict with itself.
When you enable additional Rule Plugins, you can sometimes create competing Rule
Failures between two Rule Plugins. This means that fixing the Rule Failures reported
by Rule Plugin A causes Rule Plugin B to report new Rule Failures, and fixing Rule
Plugin B's Rule Failures causes Rule Plugin A to start reporting
Rule Failures again, creating a back‑and‑forth loop.

If you encounter this loop, the practical solution is to disable one of the two
Rule Plugins so they no longer conflict.

In addition to enabling and disabling Rule Plugins, many Rule Plugins have configuration
options that let you adjust their default values to match your needs.

Use:

- [Enabling/Disabling Rule Plugins](./advanced_configuration.md#enablingdisabling-rule-plugins)
  to control rule behavior project‑wide via configuration files.
- [Suppressing Rule Failures (Pragmas)](./advanced_plugins.md#suppressing-rule-failures-pragmas)
  for local, in‑document exceptions where disabling a Rule Plugin globally would
  be too broad.

##### A Word Of Caution

Use caution when enabling rules that are disabled by default.

By design, the default set of enabled rules does not conflict with itself. When
you enable additional rules, you can sometimes create competing failures between
two rules. This means that fixing the failures reported by rule A causes rule B
to report new failures, and fixing rule B’s failures causes rule A to start reporting
failures again, creating a back‑and‑forth loop.

This section focuses on configuration options that apply regardless of which command
you run. Earlier sections described flags specific to individual commands (such
as `scan`, `scan-stdin`, and `fix`), along with extensions and Rule Plugins. Here
we step back and look at general command‑line arguments that shape how PyMarkdown
behaves for every command.

Note that most of these command-line arguments are part of configuration items that
allow them to be used from a configuration file.  To examine the full list of configuration
options for PyMarkdown, see [Available Configuration Items](./advanced_configuration.md#available-configuration-items)
in the Advanced Configuration document. This section focuses on the most commonly
used command‑line flags; the Advanced Configuration reference is the complete catalog.

We thought it was a bit too heavy to start there, as most users start their
configuration journey with command-line arguments.  Instead, we decided to focus
this part of the user guide on the command-line arguments that configure PyMarkdown
directly.

#### General Command Line Arguments

PyMarkdown provides a healthy amount of configuration that is independent of the
command used. The full list of general arguments is:

```text
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
  --return-code-scheme {default,minimal}
                        scheme to choose for selecting the application return code
```

#### At a Glance: Common Configuration Flags

<!-- pyml disable no-emphasis-as-heading-->
- **Rule Plugin and Extension Selection**
    - `--enable-rules`, `--disable-rules` – turn individual Rule Plugins on or off.
    - `--enable-extensions` – enable specific parser extensions.

- **Configuration Files and Overrides**
    - `--config` – load a configuration file.
    - `--set` – override a single configuration property.
    - `--strict-config` – treat invalid configuration as an error.
    - `--no-json5` – use the standard JSON parser instead of JSON5.

- **Error Handling and Debugging**
    - `--stack-trace` – print stack traces on application errors.
    - `--continue-on-error` – log errors but continue scanning other files.

- **Logging**
    - `--log-level`, `--log-file` – control log verbosity and destination.

- **Exit Codes**
    - `--return-code-scheme` – choose how outcomes map to process exit codes.
<!-- pyml enable no-emphasis-as-heading-->

#### Rule Plugin and Extension Selection

##### --enable-rules/--disable-rules (Rule Plugins)

The `--enable-rules` and `--disable-rules` arguments control which Rule Plugins
the Rule Engine runs for the current execution. For a conceptual overview of
Rule Plugins themselves, see the [Rule Plugins](#rule-plugins) section.
In the context of Basic Configuration, they are general flags that work with any
command (for example, `scan`, `fix`, or `scan-stdin`).
Both arguments require an extra argument that specifies a comma-separated list of
identifiers to which the corresponding option applies. An example that disables
Rule Plugins `MD012` and `MD013` is:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown --disable-rules MD012,MD013 scan examples
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown --disable-rules MD012,MD013 scan examples
    ```
<!-- pyml enable code-block-style-->

##### --enable-extensions (extensions)

The `--enable-extensions` arguments instructs the PyMarkdown application to enable
one or more extensions. This argument is followed by a comma-separated string with
the identifiers of the extensions to enable. An example that enables the two most
frequently enabled extensions, `front-matter` and `markdown-tables`, is:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown --enable-extensions front-matter,markdown-tables scan examples
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown --enable-extensions front-matter,markdown-tables scan examples
    ```
<!-- pyml enable code-block-style-->

##### --add-plugin (Rule Plugins)

The `--add-plugin` argument is followed by a path to a specially crafted Python
file that implements a new Rule Plugin. This is an advanced topic covered under
the [Developer Guide](./development.md) documentation, which explains how to write,
package, and test custom Rule Plugins.

#### Configuration Files and Overrides

##### --config (configuration)

The `--config` argument is followed by a path to a configuration file to load for
the current execution of the PyMarkdown application. An example of providing a configuration
file named `my-config.json` in JSON format to PyMarkdown is:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown --config my-config.json scan examples
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown --config my-config.json scan examples
    ```
<!-- pyml enable code-block-style-->

Note that PyMarkdown currently supports configuration files specified through this
`--config` argument as well as automatically searching for predefined configuration
files in specific locations. It currently supports configuration files in the JSON,
YAML, and TOML formats. While the basic usage of configuration files is simple,
there are important details about supported formats, search locations, how multiple
files are merged, and how command-line overrides interact with them. These topics
are covered in detail in [Advanced Configuration](./advanced_configuration.md),
which also documents the precedence between built‑in defaults, config files, and
`--set` overrides.

##### --set (configuration)

The `--set` argument is followed by a single configuration item name and a single
configuration item value to explicitly set for the current execution of the PyMarkdown
application. The structure of configuration names and the full configuration model
are described in [Advanced Configuration](./advanced_configuration.md). For example,
setting the property `plugins.MD029.style` to `zero` can be executed as:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown --set 'plugins.MD029.style=zero' scan examples
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown --set 'plugins.MD029.style=zero' scan examples
    ```
<!-- pyml enable code-block-style-->

While not always required, care should be taken to properly escape the sequence of
`<configuration item name>=<configuration item value>`.  For example, if you are
trying to set `system.exclude_path` to `draft-*.md`, you need to escape it properly
to prevent the shell you are working with from trying to expand the value `draft-*.md`
instead of passing it to PyMarkdown.

##### --strict-config (configuration)

The `--strict-config` argument tells the configuration system to treat any invalid
or incorrectly formatted configuration as an error.

By default, only valid values are applied; invalid values are silently ignored and
the corresponding defaults are used. With `--strict-config`, any invalid configuration
causes an immediate error with a clear explanation, and the application stops
instead of running with unintended defaults.

This stricter behavior makes it easier to see why a setting is not taking effect,
because any problems are surfaced immediately instead of being silently ignored.

##### --no-json5 (configuration)

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Available: Version 0.9.32**

The version 0.9.32 release addressed a long-standing
[issue](https://github.com/jackdewinter/pymarkdown/issues/1378) by adding support
for comments in JSON configuration files. To achieve that, PyMarkdown now defaults
to using the JSON5 parser, which has a clear specification and is backward compatible
with the standard JSON specification.

If you believe your JSON configuration file is not being parsed correctly by JSON5
(for example, due to edge-case numeric or string formats), use the `--no-json5`
switch. This reverts parsing back to the standard JSON parser from the Python
standard library.

#### Error Handling and Debugging

##### --stack-trace (error reporting)

The `--stack-trace` argument adjusts error reporting to make debugging easier. It
has two effects:

- Sets the pre-initialization log level to `DEBUG`.
- Prints a stack trace if an application error is reported.

This additional information is especially useful for initialization or configuration
problems that occur before normal logging is fully configured.  When reporting issues,
attaching output from a run with `--stack-trace` and `--log-level DEBUG` (written
to a log file) can significantly reduce the time needed to diagnose the problem.

These behaviors do not change how Markdown documents are processed; they only affect
logging and error reporting.

##### --continue-on-error (error reporting)

The `--continue-on-error` argument instructs PyMarkdown to log any application errors
but continue processing the remaining Markdown files. With this flag enabled, each
application error is reported and processing moves on to the next file. Without it,
the first application error stops the entire run. At the end, the application still
returns a non-zero code to indicate that at least one application error occurred.

This flag is designed to improve robustness when scanning large sets of files. For
example, near the end of a testing cycle, a new Rule Plugin triggered an unexpected
`AssertionError` on two documentation files. Using `--continue-on-error`, we were
able to complete scanning all other files, confirm the scope of the problem, and
still get a non-zero return code while planning a fix for those specific documents.

#### Logging

##### --log-level with --log-file (logging)

The `--log-level` argument instructs PyMarkdown to set its logging level to one
of the specified values:

- `CRITICAL`
- `ERROR`
- `WARNING`
- `INFO`
- `DEBUG`

By default, the log level for the application is `WARNING`. The `--log-file` argument
instructs PyMarkdown to redirect any logging output to the specified file. If this
file does not already exist, it will be created.

These options are often combined to capture detailed debug logs in a file without
cluttering standard output or error, as in the example below.

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown --log-level DEBUG --log-file app.log scan examples
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown --log-level DEBUG --log-file app.log scan examples
    ```
<!-- pyml enable code-block-style-->

#### Exit Codes

##### --return-code-scheme (observability)

Use the `--return-code-scheme` argument to control when PyMarkdown returns a non-zero
exit code:

- Use `default` if you want CI or scripts to fail when:
    - no files were scanned,
    - Rule Failures were reported, or
    - files were fixed.

- Use `minimal` if you only want CI to fail for:
    - invalid command-line usage, or
    - internal application errors.

Formally, the `--return-code-scheme` argument controls how PyMarkdown converts
high-level outcomes into process exit codes. It accepts two values:

- `default`
- `minimal`

PyMarkdown first classifies each run into one of these outcome categories:

- `SUCCESS` – everything looks good, no errors.
- `NO_FILES_TO_SCAN` – the paths provided produced zero files to scan.
- `COMMAND_LINE_ERROR` – at least one command-line argument was not valid.
- `FIXED_AT_LEAST_ONE_FILE` – at least one file was fixed, changing its content.
- `SCAN_TRIGGERED_AT_LEAST_ONCE` – at least one failure was triggered.
- `SYSTEM_ERROR` – an application error occurred, possibly stopping the run early.

Then, the chosen scheme maps those categories to exit codes:

- With `default`:
    - `COMMAND_LINE_ERROR` returns `2`.
    - `FIXED_AT_LEAST_ONE_FILE` returns `3`.
    - All other non-success outcomes return `1`.

- With `minimal`:
    - Only `COMMAND_LINE_ERROR` and `SYSTEM_ERROR` return non-zero.
    - All other outcomes (including "no files to scan" and "no Rule Failures reported")
      return `0`.

In practice, use `default` when you want CI and scripts to treat Rule Failures
and fixes as hard failures, and use `minimal` when you only want CI to fail on misconfiguration
or internal errors. In larger CI setups, this is often combined with
`--log-level INFO` and `--log-file` so that you can inspect detailed logs even when
the pipeline treats Rule Failures as non‑blocking.

### Information Commands

Earlier we grouped `plugins`, `extensions`, and `version` as inspection commands
that help you understand how PyMarkdown is configured. This section shows how to
use those commands in more detail.

#### Plugin Command

The `plugins` command allows a user to query the presence and current state of any
Rule Plugin installed within the PyMarkdown application.

```txt
usage: pymarkdown plugins [-h] {list,info} ...

positional arguments:
  {list,info}
    list       list the available plugins
    info       information on a specific plugin

optional arguments:
  -h, --help   show this help message and exit
```

##### List Subcommand

The `list` subcommand produces a columnized list of the properties associated with
each Rule Plugin.

```text
usage: pymarkdown plugins list [-h] [--all] [list_filter]

positional arguments:
  list_filter  filter

optional arguments:
  -h, --help   show this help message and exit
  --all        show all loaded plugins (default is False)
```

The information returned includes columns for:

- `ID` - identifier of the Rule Plugin
- `NAMES` - names or aliases associated with the Rule Plugin
- `ENABLED (DEFAULT)` - whether the Rule Plugin is enabled by default
- `ENABLED (CURRENT)` - whether the current configuration has enabled the Rule Plugin
- `VERSION` - revision associated with the Rule Plugin
- `FIX` - whether **fix** mode is supported for this Rule Plugin

You can think of `plugins list` as a live view of how your Rule Plugin configuration
as described in the [Rule Plugins](#rule-plugins) section has been applied. If
`ENABLED (CURRENT)` does not match your expectations, re‑check your `--enable-rules`,
`--disable-rules`, and configuration file settings.

An optional `list_filter` argument may be added with a simple [glob](https://docs.python.org/3/library/glob.html)
format. This filter is applied to the `ID` field and the `NAMES` field to
reduce the scope of the returned information. For example,
using an argument of `*single*` as the `list_filter` on the latest build
provides the following output:

```txt
  ID     NAMES                    ENABLED    ENABLED    VERSION  FIX
                                  (DEFAULT)  (CURRENT)

  md025  single-title, single-h1  True       True       0.5.0    No
  md047  single-trailing-newline  True       True       0.5.1    Yes
```

##### Info Subcommand

The `info` subcommand produces an itemized list of names and values associated with
the plugin specified by the required `info_filter` argument. That argument can either
be the Rule ID or one of its aliases.

```text
usage: main.py plugins info [-h] info_filter

positional arguments:
  info_filter  an identifier

optional arguments:
  -h, --help   show this help message and exit
```

The output of the subcommand presents focused information on the Rule Plugin in question.
For example, using an argument of `MD005` produces the following results:

```txt
  ITEM                 DESCRIPTION

  Id                 md005
  Name(s)            list-indent
  Short Description  Inconsistent indentation for list items at the same level
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md005.md
```

In addition to this, any Rule Plugins that adhere to interface version 3 of the plugin
specification will also display information on any current configuration for that
Rule Plugin. For example, using an argument of `MD001` produces the following results:

```txt
  ITEM                 DESCRIPTION

  Id                 md001
  Name(s)            heading-increment,header-increment
  Short Description  Heading levels should only increment by one level at a time.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md001.md


  CONFIGURATION ITEM  TYPE    VALUE

  front_matter_title  string  "title"
```

In addition to the normal text in the first section, a second section is used to
convey information about the current settings for any configuration items for the
current Rule Plugin. This additional section helps when diagnosing configuration
issues for specific Rule Plugins.

#### Extensions Command

With only a single difference, the `extensions` command follows the same pattern
as the `plugin` command described above. As extensions have names instead of aliases,
the `info` subcommand for extensions can only take the ID of the extension, and
not an alias. Otherwise, the use of the command and the data returned closely mirror
the behavior of the `plugins` command.

<!-- pyml disable-next-line no-duplicate-heading-->
##### List Subcommand

The `list` subcommand produces a columnized list of the properties associated with
each extension.

The information returned includes columns for:

- `ID` - identifier of the extension
- `NAMES` - a human readable name for the extension
- `ENABLED (DEFAULT)` - whether the extension is enabled by default
- `ENABLED (CURRENT)` - whether the current configuration has enabled the extension
- `VERSION` - revision associated with the extension

Use `extensions list` to verify how your extension configuration from the [Extensions](#extensions)
section is being applied in practice. If an extension you expected to be enabled
still shows `False` under `ENABLED (CURRENT)`, check for typos in its identifier
or in your `--enable-extensions` argument.

```txt
 ID                           NAME                         ENABLED    ENABLED    VERSION
                                                            (DEFAULT)  (CURRENT)

  front-matter                 Front Matter Metadata        False      False      0.5.0
  linter-pragmas               Pragma Linter Instructions   True       True       0.5.0
  markdown-disallow-raw-html   Markdown Disallow Raw HTML   False      False      0.5.0
  markdown-extended-autolinks  Markdown Extended Autolinks  False      False      0.5.0
  markdown-strikethrough       Markdown Strikethrough       False      False      0.5.0
  markdown-tables              Markdown Tables              False      False      0.1.0
  markdown-task-list-items     Markdown Task List Items     False      False      0.5.0
```

<!-- pyml disable-next-line no-duplicate-heading-->
##### Info Subcommand

The `info` subcommand produces an itemized list of names and values associated with
the extension specified by the required `info_filter` argument. That argument must
be the ID of the extension to retrieve information about. For example, using an
argument of `front-matter` as the extension ID produces the following result:

```txt
  ITEM               DESCRIPTION

  ID                 front-matter
  Name               Front-Matter Metadata
  Short Description  Allows metadata to be parsed from document Front-Matter.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/extensions/front-matter/
```

#### Version Command

As the simplest of the information commands, the `version` command reports which
PyMarkdown build you are running. As noted in the [Getting Started document](./getting-started.md#installing-pymarkdown),
it simply returns the installed version in the form:

As noted in the [Missing link], it simply returns the installed version in the form:

```txt
{major}.{minor}.{fix}
```

A common troubleshooting pattern is to run `pymarkdown version`, then use
`pymarkdown plugins list --all` and `pymarkdown extensions list` to capture both
the version and your current Rule Plugin/extension configuration before filing an
issue or comparing results with another developer.
