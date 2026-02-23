---
summary: Guide for users on how to use PyMarkdown.
authors:
  - Jack De Winter
---

# Basic Concepts

The purpose of this User Guide is to help you find detailed information about how
to use the PyMarkdown linter application in your day‑to‑day work and how its main
components fit together. These pages assume you have at least scanned the content
in the [Introduction](./index.md) document and the [Getting Started](./getting-started.md)
document, and that you are already comfortable running PyMarkdown on one or more
files, including invoking it from the command line with different options. That
is important because this document builds on that foundation to provide you with
targeted information on a variety of subjects, including how the command‑line interface
works, how rules are evaluated, how extensions interact with the Markdown parser,
and how the Rule Engine and parser cooperate during scan and fix operations. For
the canonical definitions of these modes and their behavior, see
[Scanning and Scan Mode](#scanning-and-scan-mode) and
[Failure Correction of Fix Mode](#failure-correction-or-fix-mode).

If you need a bit more experience before digging into this document, we invite you
to read and try out the examples in our [Quick Start](./quick-starts/index.md) guides.
Those guides should provide you with the foundation necessary to understand some
of the more difficult concepts in this document.

However, we know we are not perfect. If, after reading the documentation and trying
something out for yourself, you find that there is a problem, a lack of documentation,
or a feature that you believe is missing, please use the process outlined on our
[Reporting Issues](./usual.md#reporting-issues) page. We take each submitted issue
seriously and use that feedback to refine rules, improve configuration behavior,
and extend the documentation, hoping to grow our project with your support.

## Nomenclature

Here are some words and phrases that we use throughout our documentation.

### Markdown Document / Markdown File

A normal text document that includes Markdown annotations. These documents are typically
stored as Markdown files with a `.md` filename extension.

### Markdown Parser

A main application component that takes a Markdown document and breaks it down into
its constituent elements (headings, lists, code fences, block quotes, inline emphasis,
and so on). The Markdown parser emits a stream of Markdown tokens that can then
be used for specific purposes. In normal operation, parser extensions run first
and may adjust or augment that token stream, and then the Rule Engine consumes the
resulting tokens in a well-defined order to analyze the document, report failures,
or (in fix mode) propose content changes.

### Rule Engine

A main application component that takes a stream of Markdown tokens and executes
a series of actions that are based upon those tokens. Each of these actions is implemented
as a rule (see below), and the component that controls the registration, ordering,
and execution of those rules is referred to as the Rule Engine.

### Rules / Plugin Rules

Python code that extends the Rule Engine (via a plugin mechanism) to look for a
specific behavior on behalf of the user. Rules typically register handlers for specific
token types or parser events, receive those tokens in a deterministic order, and
may expose configuration options that control their behavior (for example, which
paths to ignore or what thresholds to enforce).  A rule handler may examine a single
token in isolation, maintain per-document or per-file state, or correlate information
across multiple tokens (for example, to compute heading levels or track list nesting).
Examples of this are Rule `MD010` which looks for hard tabs in the document and
Rule `MD012` which looks for consecutive blank lines in the document. In the built-in
rule set:

- the `MD` prefix is used for rules that align with rules introduced by `markdownlint`
- the `PML` prefix is used for rules introduced by the PyMarkdown application to
  address new requests and scenarios

Additional prefixes may be introduced for other rule families over time.

### Rule Ids

Rule ids are unique identifiers that are associated with a given rule. These rule
ids are case-insensitive. Therefore, the ids `md010`, `MD010`, and `Md010` all refer
to the same rule. For historical reasons, these identifiers start with a two- or
three-letter prefix, followed by a three-digit suffix, and the combination of prefix
and suffix is unique across all rules and across all rule families. These ids are
what you see in command-line output, and they form the canonical identifiers used
in configuration files, logs, and most tooling integrations.

### Parser Extensions

Python code that directly interacts with the Markdown Parser component to provide
a single enhanced Markdown capability. Extensions can introduce new or optional
token types, adjust how existing Markdown constructs are parsed, or add support
for commonly used non-standard syntax (such as task list items, front matter blocks,
or pragma-style directives that influence parsing or linting behavior). In practice,
a parser extension runs before the Rule Engine sees any tokens, so its changes to
the token stream are fully visible to every rule, including both built-in and custom
plugin rules. This means that enabling or disabling an extension can change which
tokens a rule sees, how those tokens are structured, and even whether a rule triggers
at all for a given construct, without the rule itself changing.

### Triggered

When a rule finds an instance of the specific behavior that it is looking for, that
rule then triggers a failure. There is no general behavior about the number of times
a rule can be triggered within a single document; some rules report every occurrence,
while others may only report the first occurrence or aggregate multiple issues into
a single failure. The exact triggering behavior for a rule is determined by the
rule’s implementation and, in some cases, its configuration options, including options
that suppress reporting in certain regions or for certain patterns.

### Failure

When a rule is triggered, the information that the rule produces to provide specifics
about why it was triggered is called a failure. A failure usually includes at least
the rule id, a description, and a location (file, line, and column), and may also
include rule-specific extra data that downstream tools can consume. Failures are
distinct from errors in that detecting failures is an expected outcome of executing
the application and indicates a style or policy violation in your Markdown content,
not a defect in PyMarkdown itself or in a rule implementation.

It is worth noting that while these are labelled as "failures", that is only a general
description of that information. The term failure is used to denote that a rule found
something that does not adhere to the user's specified guidelines expressed through
the rule itself, typically as configured through configuration files, command-line
options, or inline pragmas (when supported by the rule).

### Error

While we try to plan out and test everything, occasionally errors get through. Errors
show that either Python or our own guard code has detected an invalid condition
within our application, one of its extensions, or one of its plugins, such as an
uncaught exception, an assertion failure, or misuse of the public APIs by a custom
rule or extension. These conditions are treated as abnormal and typically cause
the current invocation of PyMarkdown to fail fast (with a non-zero exit code) unless
you have explicitly enabled `--continue-on-error`, in which case the error is reported
but scanning of the remaining files continues.

### Scanning and Scan Mode

A single pass of the PyMarkdown application over one or more files using the `scan`
command. That pass is performed in Scan Mode, with the goal of finding any failures
within each Markdown document that was scanned. In Scan Mode, rules are allowed
to emit failures but are not allowed to modify the document; any proposed fixes
from rules that support autofix are ignored, and the original file contents on disk
remain unchanged. This behavior is intentional so that scan can be safely used in
CI pipelines and read-only environments without any risk of modifying source files.

### Failure Correction or Fix Mode

Like scan mode above but using the `fix` command. The Rule Engine asks any rules
that support **autofix** to automatically fix the failures they reported and to
return updated content for the affected regions of the document. The Rule Engine
then merges all accepted fixes into a new version of the file content and writes
that content back to disk. Note that not all rules support this feature, for reasons
discussed in the section on [Fix Mode](#basic-fixing), which describes how the `fix`
command executes in **fix mode**, how conflicting or overlapping fixes are resolved,
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

Note that parser extensions are exempt from that rule. Because extensions can change
how documents are parsed, their effect on specific rules is not always obvious.
To address this, each extension includes documentation and examples that show how
it affects the token stream and, when relevant, rule behavior. We have tried to
address this by having each extension provide solid documentation on that extension,
coupled with examples or links to examples that show how the extension affects the
token stream that rules consume and, in some cases, the rule behavior itself. More
information about the available extensions, the additional tokens they introduce,
and how they interact with rules can be found in the [Advanced Extensions](./advanced_extensions.md)
document. That guide serves as a reference for each extension, covering its purpose,
how it changes the parser’s token stream, and any configuration options or interactions
with specific rules.

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
any reported failures come only from the example files.. Within the `examples` directory
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
  its first heading satisfies the rule's requirement.

You will see these two files reused in later sections whenever we need simple, stable
examples of heading-related behavior.

## Command Line Basics

**NOTE**: If you are looking for some quick help on how to get started with the
PyMarkdown command line, read our [Quick Start - General Command-Line Usage](./quick-starts/general.md)
guide.

If you are stuck on what to do when using the command line, it is always beneficial
to enter the following command line:

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

By default, PyMarkdown adopts that three-level return code scheme. For power users,
you can override this behavior and choose a different scheme that controls whether
certain categories of results (such as "files were fixed" or "only style failures
occurred") cause a non-zero exit code. The available schemes are described in
[Return Code Scheme](#-return-code-scheme-observability).

### Available Groups of Commands

When you run the base command with `--help`, the output lists all arguments that
apply to every command, followed by the available commands. At present, there are
six commands, displayed in alphabetical order:

- `extensions` - Request information on current extensions.
- `fix` - Fix any Markdown files (where possible) in the specified paths.
- `plugins` - Request information on current plugin rules.
- `scan` - Scan any Markdown files in the specified paths.
- `scan-stdin` - Scan the application's standard input as a Markdown file.
- `version` - Return the version of the application.

Three of these commands (`extensions`, `plugins`, and `version`) are inspection
commands, used to request more information about [installed extensions](#extension-command),
[installed rules](#plugin-command), and to inquire about the [version](#version-command)
of the application.

The remaining commands are action commands. The `scan` command instructs PyMarkdown
to scan any specified files for failures and return a non-zero exit code if any
failures are found. The `scan-stdin` command is a variant of the `scan` command
that reads the application's standard input and scans that input as if it were in
a file. The `fix` command is like the `scan` command, but it instructs PyMarkdown's
Rule Engine to try to fix any failures and write the updated content back to disk,
potentially changing multiple files in a single invocation.

To figure out the correct arguments to pass to a command, run:

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

Replace `{command}` with the command you want details about.

This help output focuses on options specific to that command, making it useful both
when exploring the CLI and when you need to fine-tune a particular invocation.

In addition to the commands and their arguments, there are arguments that precede
the commands and apply to all the commands. These arguments are covered in the section
below on [Basic Configuration](#basic-configuration).

### Basic Scanning

**NOTE**: If you are looking for some quick help on how to get started with using
PyMarkdown to scan Markdown files from the command line, read our
[Quick Start - Scanning Markdown Files](./quick-starts/scanning.md) guide.

The PyMarkdown linter is executed by calling the project from the command line,
specifying one or more files and directories to scan for Markdown `.md` files.
The list of files and/or directories presented on the command line must be prefaced
with the `scan` keyword to denote that scanning is needed.

#### Sample Command Lines

The command line for scanning files is very straightforward. Assuming that you are
in the root directory of the directory structure specified in the [Prerequisites](#prerequisites)
section, two simple command lines are:

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
while the second invocation will only scan the two specified files. To ensure that
the output is always consistent, if different path arguments specify the same filename,
that filename will only be added once to the list of files to scan. In addition,
to ensure that the scanning is done in a predictable order, that list of files to
scan is also sorted into alphabetical order before any rules are executed, so that
rule behavior and output ordering do not depend on the exact combination or ordering
of path arguments on the command line.

After executing either of those command lines from the root directory, the output
to expect from PyMarkdown is:

```text
examples\example-1.md:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
```

This failure and its format is described in the following section.

#### Rule Failure Format

Our team decided to adopt a failure format like that of other linters, checkers,
and compilers. At their root, all those tools use the first four fields to show
the file scanned, the location within the file where the failure occurred (line
number and column number), and a unique code for the reported failure. From there,
the tools all diverge into their own formats, each format providing the detailed
information relevant to its own tool.

Keeping to that format, the output format for any PyMarkdown failure is as follows:

`file-name:line:column: rule-id: description (aliases)`

Breaking it down into its constituent parts:

- `file-name` - Path to the file that triggered the rule.
    - This will be the path as resolved by PyMarkdown after all globbing, recursion,
      and filtering (for example, `--exclude` and `--respect-gitignore`) have been
      applied.
- `line`/`column` - Position in the file where the rule was triggered.
    - Uses a 1-based line index and a 1-based column index that match what PyMarkdown
      reports consistently across rules and align with what you see if you open
      the file in a typical text editor.
- `rule-id` - Unique identifier assigned to the rule, such as MD013.
    - This id is stable across versions unless a rule is explicitly deprecated and
      replaced, in which case the deprecation is called out in the rule documentation.
- `description` - Human readable description of the rule.
    - Intended to be a short summary of the failure that can be consumed directly
      from logs or CI output without needing to cross-reference the rule documentation.
- `aliases` - One or more aliases used to reference the rule in configuration, pragmas,
  and command line options.
    - These are the same strings you can pass to `--enable-rules` / `--disable-rules`
      and to pragma directives, remaining stable for a rule across releases unless
      otherwise documented.

Using the output from the command line from the last section, that scan output reports
one failure that occurred in the file `examples\example-1.md` on line 1 at
column 1. The id of the rule that triggered is `MD041`, otherwise known by the human
readable aliases of `first-line-heading` and `first-line-h1`. To present even more
readable text to the reader, the text associated with this rule's failures is:

> First line in file should be a top level heading

Looking back at the text for `example-1.md`, the first line of that file
is:

```Markdown
## This is an example
```

which shows an ATX Heading with a level of 2. A simple reading of the failure text
indicates that rule `MD041` is okay with the first line being a heading, but it
wants that heading to be a level 1 or top-level heading. Looking at the text from
`example-2.md`, the first line is:

```Markdown
# This is an example
```

As the `example-2.md` file is not mentioned in the output, it makes sense that PyMarkdown's
rule MD041 did not have any issue with a level 1 ATX Heading, largely confirming
the above assumption that the application of rule `MD041` matches its stated intent.
If desired, we can take the extra step to verify this by looking at the documentation
page for [Rule MD041](./plugins/rule_md041.md#reasoning) which states:

> In most cases, the top-level heading of a document is used as the title of that
> document. Therefore, the first heading in the document should be a level 1 header
> to reflect that reality.

### Advanced Scanning

Advanced scanning builds directly on basic scanning behavior in PyMarkdown. Before
using these options, you should understand the basic concepts (paths, globbing,
recursion, and rule failure output). With that foundation, the advanced options
are much easier to reason about and are less likely to behave in ways that seem
"mysterious".

#### Command Line Arguments

As far as the command line interface for scanning goes, we have tried to make the
advanced options easy to understand.

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
ensuring that the list of filenames believed to be specified by the argument and
the expected list of filenames to scan match each other. It is especially helpful
when debugging path or exclude patterns in scripts and continuous integration (CI)
pipelines, where you may not see or log the exact list of resolved files, but still
want to verify how PyMarkdown's path resolution and filtering logic behaves. Our
team treats `--list-files` as the "dry run" mode of the scanner: it shows you what
would be processed without actually running any rules.

##### --recurse or -r

Use `--recurse` when you want PyMarkdown to search entire directory trees under
the starting paths. In this mode, every subdirectory is visited before any filtering
is applied.

After traversal, PyMarkdown applies extension filtering and any `--exclude` or `--respect-gitignore`
rules to decide which files to scan. This design keeps the discovery logic simple
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
- It then passes that list to py-walk’s matcher.
- Any path that matches an exclude pattern is removed from the final list of files
  to scan.

##### --respect-gitignore

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Available: Version 0.9.35**

The `--respect-gitignore` flag tells PyMarkdown to ask Git which files are ignored,
so `.gitignore` rules are applied exactly as they would be by Git itself. With this
flag enabled, any file that Git marks as ignored is excluded from scanning.

When you use `--respect-gitignore`, PyMarkdown must be able to run the Git executable.
If Git is not available or returns an error, PyMarkdown treats that as a failure
and does not silently ignore the flag. This guarantees that your scan results always
reflect the same ignore rules that Git applies to the repository.

Because PyMarkdown shells out to Git and parses its output, `--respect-gitignore`
adds some startup overhead while it computes the list of files to scan. If that
extra cost is unacceptable, or Git is not available in your environment (for example,
in some minimal CI containers), use multiple `--exclude` arguments instead to approximate
the relevant `.gitignore` patterns.

##### path

The scan command accepts one or more path arguments. Paths that contain a `?` or
`*` character are passed to Python’s [glob module](https://docs.python.org/3/library/glob.html)
and treated as glob patterns; paths without wildcards are treated as literal files
or directories. Recursive traversal is controlled exclusively by `--recurse`, so
PyMarkdown does not use `glob.glob(..., recursive=True)`.

By default, PyMarkdown only processes files whose names end with `.md`. This means
you can scan a directory by passing `.` or `examples` instead of writing `./*.md`.

Conceptually, PyMarkdown uses two stages:

- **Discovery:** globs and path arguments determine which filesystem entries are
  considered at all.
- **Filtering:** the extension filter (the default `.md` set, or your `--alternate-extensions`)
  decides which of those entries are treated as Markdown candidates.

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
same. All general command-line options (such as configuration and rule enable/disable
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
[Quick Start - Fixing Markdown Files](./quick-starts/fixing.md) guide.

The documentation for fixing Markdown files using PyMarkdown is very similar to
the documentation for scanning Markdown files. The two main differences are:

- not every rule supports the **autofix** ability used to fix issues, because many
  rules cannot propose a deterministic fix without inferring the author’s intent
- PyMarkdown will only emit a small amount of information when it applies fixes,
  informing you only that content within a given file was fixed, not specifically
  what content was fixed.

Because of these differences, you should treat autofix as a mechanical assistant
for well-defined formatting changes rather than a general-purpose "auto-correct"
for arbitrary Markdown problems.

#### Strict Rules for A Rule To Have The Autofix Ability

Before coding the **autofix** ability for any rule, the rule author must be able
to answer these questions in the positive:

- is the proposed fix a purely mechanical fix that is easily documented and predictable?
- according to the [Github Flavored Markdown](https://github.github.com/gfm) specification
  or other specifications, does the fix only change format, abstaining from changing
  the content in any way?
- is the proposed fix absent of any ambiguity in its application, even when applied
  repeatedly across an entire document (that is, is the fix idempotent and free of
  hidden side effects)?

If any of these answers is not "yes", that rule is not allowed to support **autofix**.

This restriction is a deliberate policy choice for rule authors. The Rule Engine
itself is technically capable of more complex changes, but we do not permit rules
to use that flexibility when it would make fixes unpredictable.

In practice, rules must not silently rewrite content in a way that could change
the document's meaning.

They must also behave the same way if `pymarkdown fix` is run multiple times on
the same file. In other words, a well‑designed **autofix** implementation is deterministic
and idempotent: the same inputs always produce the same outputs, and running the
fix again does not introduce further changes.

These constraints exist so that **autofix** implementations remain simple, transparent,
and easy to review.

When a fix depends on guessing the author's intent, it usually:

- Introduces intricate conditional logic and rule‑specific exceptions.
- Makes it difficult to determine whether the fix is safe in all cases.

To avoid those problems, we explicitly disallow that kind of complex, intent‑dependent
**autofix** behavior.

Because Markdown has many element types and edge cases, it is hard to remove ambiguity
completely. Any **autofix** that tries to infer the author’s intent would be risky
and unpredictable.

For that reason, we deliberately disallow **autofix** behaviors that depend on guessing
intent.

##### Examples

###### Positive - Rule MD019 - no-multiple-space-atx

[Rule MD019](./plugins/rule_md019.md), or `no-multiple-space-atx`, looks for extra
spaces between the `#` characters and the heading text in an ATX heading. From the
[Github Flavored Markdown](https://github.github.com/gfm/#atx-headings) specification:

> The opening sequence of # characters must be followed by a space or by the end
> of line.

Rule `MD019` treats cases where "followed by a space" becomes "followed by many
spaces" as violations.

For **autofix**, all three requirements are satisfied. The fix collapses any run
of multiple spaces between the opening `#` sequence and the heading text to a single
space. This change only affects formatting and does not alter the content. Its behavior
is fully deterministic and idempotent: once the excess spaces are removed, running
autofix again does not change the heading.

###### Negative - Rule MD025

In contrast to Rule `MD019`, [Rule MD025](./plugins/rule_md025.md) (`single-title`)
enforces that each Markdown document has a single title. In practice, this means:

- The document has exactly one level‑1 heading, or
- The document has a title field in its [front-matter](./extensions/front-matter.md#summary),
  which PyMarkdown also treats as the document title.

When we considered adding autofix for `MD025`, we quickly ran into a problem. Deciding
which heading represents the "real" title requires guessing the author's intent.
For example, if a document has multiple level‑1 headings, the rule cannot reliably
determine which one to keep or how to adjust the others.

Because any automatic change would involve that kind of intent‑dependent choice,
`MD025` does not meet all three **autofix** requirements. The rule still provides
useful detection, but fixes are expected to be applied manually or by higher‑level
refactoring tools rather than via PyMarkdown’s **autofix** mechanism.

#### Rules With Autofix

**NOTE:** You don’t need to memorize this list — use it as a reference. It is also
colocated in our [Quick Start](./quick-starts/fixing.md#rules-with-autofix) guides
for easy reference.

For quick reference, these are the built-in rules that currently support **autofix**
in the latest released version of PyMarkdown:

- The first column presents the rule's identifier and a link to that rule's
  `Fix Description` heading in the documentation.
- The second column presents the human-readable identifiers that are also used to
  identify the rule.
- The third column contains a short description of the rule itself.

This list can change between releases as rules are added or as existing rules gain
or lose **autofix** support. That means the set of rules that can modify files is
version‑dependent.

When you rely on **autofix** in automated workflows:

- Treat the **autofix** capabilities of each rule as part of PyMarkdown’s public
  API.
- Pin the PyMarkdown version in your tooling.
- On each upgrade, review this table (or the per‑rule documentation) to confirm
  which rules can still modify files.

Following these steps helps you avoid unexpected changes in fix behavior when you
move between PyMarkdown versions.

<!-- pyml disable line-length-->

| Rule Id & Link | Human-Readable Identifier | Short Description |
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

The [Fix Mode Example](./quick-starts/fixing.md#fix-mode-example) in our Quick Starts
guide outlines most of the practical details you need to know about applying **fix**
mode to a single file, including how fixes are reported and how failures are re-scanned
after changes. Internally, fix mode uses the same Rule Engine as scan mode, but
rules that support autofix are allowed to emit modifications to the document instead
of only reporting failures. You can then call PyMarkdown again in **scan** mode
over the fixed files, but that scan should only report failures for rules that
do not support autofix or for issues that cannot be fixed automatically.

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
  if possible, so that only “publishable” documentation in tracked paths is subject
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
specification. Some are defined by that specification as optional extensions; others
are additional features implemented by PyMarkdown.

These features change how the Markdown parser breaks a document into its constituent
elements. In practice, enabling an extension can introduce new element types (for
example, table cells) or reinterpret existing structures (for example, treating
a YAML block as front matter instead of a paragraph), which in turn affects which
tokens the Rule Engine receives and which rules may trigger.

Because of these effects, advanced configurations should be tested with representative
documents. This ensures that rule behavior, reported positions, and any apparent
"missing" or "extra" failures still align with your expectations.

These extensions are fully documented in the
[Advanced Extensions](./advanced_extensions.md) document. That guide describes how
each extension behaves, how it is implemented, and how to configure it.

In this section, we provide only high-level information about each extension so that
you can proceed with solid footing before diving into the detailed reference.

#### Specification Extensions

Some parts of the GitHub Flavored Markdown specification are defined as optional
extensions that a GFM-compliant parser may support.

If you enable one of these extensions, PyMarkdown will recognize the corresponding
syntax in your Markdown and apply the rules defined by that extension when parsing
the document. These are most useful when:

- Your documentation already uses GFM-style tables, task lists, or strikethrough.
- You want PyMarkdown to lint raw HTML usage more strictly according to GFM’s
  disallowed HTML rules.
- You need link detection that matches GFM’s extended autolink behavior.

The five specification extensions are:

<!-- pyml disable-num-lines 7 line-length-->
| Extension | GFM Link | Description |
| --- | --- | --- |
| [Tables](./extensions/markdown-tables.md) | [GFM](https://github.github.com/gfm/#tables-extension-) | Tables using the \| character. |
| [Task List Items](./extensions//task-list-items.md) | [GFM](https://github.github.com/gfm/#task-list-items-extension-) | Task list items using the `[` and `]` characters in list markers. |
| [Strikethrough](./extensions/strikethrough.md) | [GFM](https://github.github.com/gfm/#strikethrough-extension-) | Strikethrough using the `~` character. |
| [Extended Autolink](./extensions/extended-autolinks.md) | [GFM](https://github.github.com/gfm/#autolinks-extension-) | Extended autolink rules. |
| [Disallowed HTML](./extensions/disallowed-raw-html.md) | [GFM](https://github.github.com/gfm/#disallowed-raw-html-extension-) | HTML elements that are purposefully disallowed as being dangerous. |

Note that these are extensions to the specification itself. Parsers may not support
these extensions, or only support them with specific configuration enabled. This
will vary on a parser-by-parser basis.

#### Requested Extensions

Unlike the specification extensions, these extensions do not originate from a formal
Markdown specification. They were added to PyMarkdown to address practical needs
that came up in real-world use.

In broad terms:

- The front-matter extension treats a leading YAML block as metadata and removes
  it from the token stream, aligning PyMarkdown’s view of the document with tools
  like MkDocs.
- The pragma extension allows inline instructions in comments to enable or disable
  specific rules over selected line ranges, without changing how the Markdown itself
  is parsed.

<!-- pyml disable-num-lines 4 line-length-->
| Extension | Enabled By Default | Description |
| --- | --- | --- |
| [Front-Matter](./extensions/front-matter.md) | No | YAML Front Matter for files. |
| [Pragmas](./extensions/pragmas.md) | Yes | Pragmas to control triggering of rules within files. |

##### Front-Matter Extension

The [Document Front-Matter](./extensions/front-matter.md) extension (id of `front-matter`
and disabled by default) allows for an optional YAML front-matter block to be inserted
at the first line of the document. For applications that aggregate Markdown pages
into a condensed form (such as a web site), having such a front-matter block is
useful in conveying information from the Markdown document to that application.
This is indeed the case with the [MkDocs application](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data)
used to aggregate our Markdown documents into this documentation web site.

For example, depending on the documentation you are trying to write, you could use
the MkDocs application along with a Markdown document with the following front-matter:

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
uses the front-matter YAML purely as metadata. In particular, MkDocs uses the title
field as the document title and ignores the other fields unless they are referenced
by a theme.

To align with that behavior, enabling this extension causes PyMarkdown to treat
the front-matter block as metadata and remove it from the stream of Markdown elements
that rules evaluate.

When this extension is enabled:

- Rules effectively "start" at the first line after the front matter.
- Line and column positions in failures are still computed relative to the original
file, not to a version with front matter stripped.

In practice, this keeps diagnostics aligned
with the on-disk file while also matching what an aggregating tool such as MkDocs
renders.

##### Pragma Extension

The [Pragma](./extensions/pragmas.md) extension (id of `linter-pragmas`, enabled
by default) allows for the introduction of special instructions into the Markdown
document. These instructions can then be used by PyMarkdown to ask for special treatment
for parts of the document rather than the entire document. This feature is analogous
to the `suppress` or `ignore` features of other linters and checkers.

**Important Note:** Pragmas are implemented as an extension because they modify the
Markdown document **before** it reaches the parser and then remove themselves.

As a result, pragmas are not visible to the Markdown parser at all.

Instead, pragmas only affect the behavior of the Rules Engine. They dynamically
enable or disable rule triggering over specific line ranges. They do not change
the underlying Markdown content.

This design guarantees that pragmas never alter how Markdown is parsed. For example,
they do not affect heading structure or list nesting. Pragmas only control which
parser outputs the Rules Engine processes, and that control determines which failures
are emitted or suppressed for a given region of the document.

For example, consider the following Markdown snippet:

```Markdown
#  My Bad Atx Heading
```

When scanned, this file will trigger a `MD019` (or `no-multiple-space-atx`) failure
due to the two spaces between the `#` character and the following `M` character.
While this is obviously a contrived example, if we wanted to suppress the triggering
of the rule on this line, we have two main options.

The first is the simplest: disable it only for the [next line](./extensions/pragmas.md/#disable-next-line-command):

```Markdown
<!-- pyml disable-next-line no-multiple-space-atx-->
#  My Bad Atx Heading
```

The second is a slight alteration to the simple case, disabling the rule for a specific
[number of lines](./extensions/pragmas.md/#disable-num-lines-command):

```Markdown
<!-- pyml disable-num-lines 1 blanks-around-fences-->
#  My Bad Atx Heading
```

The final example is more of a "heavy hammer": disable it for an
[entire region](./extensions/pragmas.md#disable-command-and-enable-command), enabling
it at the end of that region.

```Markdown
<!-- pyml disable no-multiple-space-atx-->
#  My Bad Atx Heading
<!-- pyml enable no-multiple-space-atx-->
```

Care must be taken when using these pragmas to disable triggering of failures by
the Rule Engine. There are three things to keep in mind:

- Pragmas can only *disable* and *enable* the triggering of failures for rules that
  are already enabled. In other words, in the above example, Rule `MD019` must already
  be enabled for the pragma to have any effect.
- More specific pragmas (`disable-next-line` and `disable-num-lines`) are applied
  first, and then the region pragmas (`disable` and `enable`). Because of this precedence,
  we do not suggest using both forms of pragmas in the same document, as it can
  be difficult to reason about which pragma is currently in effect.
- Region pragmas (`disable` and `enable`) do not stack. You can have two disable
  region pragmas that disable rule `MD019`, and a single matching enable region
  pragma reactivates that rule, rather than requiring one enable per disable.

These keep pragma evaluation simple and predictable: PyMarkdown effectively tracks
a single on/off state per rule based on the most recent applicable region pragma
and then applies any more specific one-line pragmas on top of that for the affected
lines, without maintaining a nested stack of disable/enable scopes.

#### Extension Examples

The two most frequently enabled extensions are for Markdown Tables and for Front
Matter. Most Markdown implementations support tables, and many systems that consume
Markdown and aggregate it into other formats use YAML Front Matter to carry extra
information about the documents being aggregated.

Modifying our simple example of scanning all Markdown files in every `docs` directory,
we get the following command line, which explicitly enables only the extensions
needed for front matter and tables while leaving other extensions at their existing
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

For more advanced information about extensions and how they impact the Markdown
parser, check out the [Advanced Extensions](./advanced_extensions.md) document.

### Plugin Rules

Plugin rules (usually just referred to as rules) are the code that enables the Rule
Engine to look for Markdown patterns or structures that it considers sub-optimal.
Their scope ranges from detecting long lines in the document
([Rule MD013](./plugins/rule_md013.md)),
through identifying superfluous blank lines
([Rule MD012](./plugins/rule_md012.md)),
to detecting what looks like a missed Markdown ATX Heading annotation
([Rule MD018](./plugins/rule_md018.md)).

#### Enabling And Disabling Rules

Instead of looking at a [long list of rules](./rules.md) that describe every rule
provided by PyMarkdown, most users scan a set of files in their repository and decide
that they do not want a rule to be enabled. Reasons will vary from "not right now,
I'll fix it later" to "I really do not agree with that", but the request remains
the same: how do I disable that behavior?

On the command line, use `-d` or `--disable-rules` with a comma-separated list of
rule ids or aliases to disable rules, and `-e` or `--enable-rules` to enable them.
Rules may be disabled by default for two main reasons:

- They introduce new behavior or apply only in niche scenarios.
- They have been replaced by a newer rule, and we avoid enabling two competing implementations
  of the same check at the same time.

##### Example

For example, if you disagree with PyMarkdown that long lines and extra blank lines
in a Markdown document are bad, you can disable the corresponding rules by id or
by alias:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown -d MD012,MD013 scan examples
    # or, using rule aliases:
    pymarkdown -d no-multiple-blanks,line-length scan examples    ```
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown -d MD012,MD013 scan examples
    # or, using rule aliases:
    pipenv run pymarkdown -d no-multiple-blanks,line-length scan examples
    ```
<!-- pyml enable code-block-style-->

##### A Word Of Caution

Use caution when enabling rules that are disabled by default.

By design, the default set of enabled rules does not conflict with itself. When
you enable additional rules, you can sometimes create competing failures between
two rules. This means that fixing the failures reported by rule A causes rule B
to report new failures, and fixing rule B’s failures causes rule A to start reporting
failures again, creating a back‑and‑forth loop.

If you encounter this loop, the practical solution is to disable one of the two
rules so they no longer conflict.

In addition to enabling and disabling rules, many rules have extra configuration
that lets you adjust their default values to match your needs.

For more detail:

- See [Advanced Configuration](./advanced_configuration.md#rule-plugins) for how
  to set configuration on a per‑rule basis.
- See the [Advanced Rules Guide](./advanced_plugins.md) for a complete list of built‑in
  rules and detailed information about what each rule checks.

### Basic Configuration

This section focuses on configuration options that apply regardless of which command
you run. Earlier sections already covered scanning, fixing, extensions, and plugin
rules; here we’ll look at general command-line arguments that shape how PyMarkdown
behaves.

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

##### --enable-rules/--disable-rules (rules)

The `--enable-rules` and `--disable-rules` arguments instruct the PyMarkdown application
to enable or disable specific rules for the current execution of the application.
Both arguments require an extra argument that specifies a comma-separated list of
rules to which the corresponding option applies. An example that disables rules
`MD012` and `MD013` is:

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

##### --add-plugin (rules)

The `--add-plugin` argument is followed by a path to a specially crafted Python
file that implements a new plugin rule. This is an advanced topic covered under
the [Developer Guide](./development.md) section of this documentation.

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
are covered in detail in [Advanced Configuration](./advanced_configuration.md).

##### --set (configuration)

The `--set` argument is followed by a single configuration name and a single configuration
value to explicitly set for the current execution of the PyMarkdown application.
The structure of configuration names and the full configuration model are described
in [Advanced Configuration](./advanced_configuration.md). For example, setting the
property `plugins.md029.style` to `zero` can be executed as:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown --set plugins.md029.style=zero scan examples
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown --set plugins.md029.style=zero scan examples
    ```
<!-- pyml enable code-block-style-->

##### --strict-config (configuration)

The `--strict-config` argument tells the configuration system to treat any invalid
or incorrectly formatted configuration as an error.

By default, only valid values are applied; invalid values are silently ignored and
the corresponding defaults are used. With `--strict-config`, any invalid configuration
causes an immediate error with a clear explanation, and the application stops
instead of running with unintended defaults.

This stricter behavior makes it easier to see why a setting is not taking effect,
because any problems are surfaced immediately instead of being silently ignored.

#### --no-json5 (configuration)

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

##### --stack-trace (error reporting)

The `--stack-trace` argument adjusts error reporting to make debugging easier. It
has two effects:

- Sets the pre-initialization log level to `DEBUG`.
- Prints a stack trace if an application error is reported.

This additional information is especially useful for initialization or configuration
problems that occur before normal logging is fully configured.

These behaviors do not change how Markdown documents are processed; they only affect
logging and error reporting.

##### --continue-on-error (error reporting)

The `--continue-on-error` argument instructs PyMarkdown to log any application errors
but continue processing the remaining Markdown files. With this flag enabled, each
application error is reported and processing moves on to the next file. Without it,
the first application error stops the entire run. At the end, the application still
returns a non-zero code to indicate that at least one application error occurred.

This flag is designed to improve robustness when scanning large sets of files. For
example, near the end of a testing cycle, a new rule triggered an unexpected
`AssertionError` on two documentation files. Using `--continue-on-error`, we were
able to complete scanning all other files, confirm the scope of the problem, and
still get a non-zero return code while planning a fix for those specific documents.

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

##### --return-code-scheme (observability)

Use the `--return-code-scheme` argument to control when PyMarkdown returns a non-zero
exit code:

- Use `default` if you want CI or scripts to fail when:
    - no files were scanned,
    - failures were reported, or
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
    - All other outcomes (including “no files to scan” and “failures reported”)
    return `0`.

### Information Commands

#### Plugin Command

The `plugin` command allows a user to query the presence and current state of any
rule plugin installed within the PyMarkdown application.

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
each rule plugin.

```text
usage: pymarkdown plugins list [-h] [--all] [list_filter]

positional arguments:
  list_filter  filter

optional arguments:
  -h, --help   show this help message and exit
  --all        show all loaded plugins (default is False)
```

The information returned includes columns for:

- `ID` - identifier of the rule
- `NAMES` - names or aliases associated with the rule
- `ENABLED (DEFAULT)` - whether the rule is enabled by default
- `ENABLED (CURRENT)` - whether the current configuration has enabled the rule
- `VERSION` - revision associated with the rule
- `FIX` - whether fix mode is supported for this rule

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
be the rule's id or one of its aliases.

```text
usage: main.py plugins info [-h] info_filter

positional arguments:
  info_filter  an identifier

optional arguments:
  -h, --help   show this help message and exit
```

The output of the subcommand presents focused information on the rule in question.
For example, using an argument of `md005` produces the following results:

```txt
  ITEM                 DESCRIPTION

  Id                 md005
  Name(s)            list-indent
  Short Description  Inconsistent indentation for list items at the same level
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md005.md
```

In addition to this, any rules that adhere to interface version 3 of the plugin
specification will also display information on any current configuration for that
rule. For example, using an argument of `md001` produces the following results:

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
current rule. This additional section helps when diagnosing configuration issues
for specific rules.

#### Extension Command

With only a single difference, the `extension` command follows the same pattern
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
be the id of the extension to retrieve information about. For example, using an
argument of `front-matter` as the extension id produces the following result:

```txt
  ITEM               DESCRIPTION

  Id                 front-matter
  Name               Front Matter Metadata
  Short Description  Allows metadata to be parsed from document front matter.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/extensions/front-matter/
```

#### Version Command

As noted in the [Getting Started document](./getting-started.md#installation), the
`version` command simply returns the version of PyMarkdown that is installed using
the form:

```text
{major}.{minor}.{fix}
```
