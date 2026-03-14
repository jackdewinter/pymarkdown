# Quick Start: Scanning Markdown Files

The commands in this section use PyMarkdown's scan mode to check the content of
one or more Markdown files. Any problems it finds are reported to the console in
a standard linter-style format.

In PyMarkdown, a rule is a specific style or formatting check (for example, "headings
must increase by one level at a time" or "lists must be consistently formatted").
Those rules are contained within Rule Plugins, which manage the interface between
the individual rules themselves and PyMarkdown's Rule Engine.  In most cases, you
can think of them as one and the same.

A Rule Failure is any place in a Markdown file that does not comply with a Rule Plugin.
PyMarkdown reports each failure with the file name, line number, column number,
Rule ID, and a short message, similar to many code linters.

This concept was first introduced in the [Quick Start: Introduction](./index.md)
page, under the section [How PyMarkdown Reports Failures](./index.md#how-pymarkdown-reports-rule-failures).
If you are not yet confident reading Rule Failures, review that section now or keep
it open as a reference while you work through this page.

## What You Will Learn

> **Quick Start Guide Single Line Summary**
> This page teaches the various ways in which you can use PyMarkdown from the
> command line to scan for Rule Failures in your Markdown documents, increasing
> your confidence in using PyMarkdown as a scanning tool.

On this page, you will learn how to:

- scan a single Markdown file
- scan multiple Markdown files
- scan any Markdown files in a directory
- scan any Markdown files under a directory (recursively)
- scan "glob" paths
- scan paths and exclude certain paths and `.gitignore`-ignored files
- debugging scan path issues

After finishing this page, you should be comfortable running `pymarkdown scan` on
your own projects.

## Prerequisites

The following sections assume that you have already [installed PyMarkdown](./installation.md)
and are reasonably comfortable with [command line usage](./general.md). If you are
not, please refer to the links above to help you get started.

As noted in the introductory paragraph, make sure you can read PyMarkdown Rule Failures
before you continue. When you run these example commands on your own project, you
may see several Rule Failures. If the output still feels confusing, revisit the
[How PyMarkdown Reports Rule Failures](./index.md#how-pymarkdown-reports-rule-failures)
section,
then return here.

If the output feels overwhelming: That's normal the first time you scan an existing
project. For now, don't worry about fixing everything. Focus on finishing this page
and getting comfortable with scans. The next Quick Start guide covers how to clean
things up safely.

## Scan a Single File

This command scans the file `sample.md` and reports any Rule Failures that it
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

After scanning a single file, the next step is scanning a small set of files.

This command scans the files `sample.md` and `another-sample.md` and reports any
problems it finds. Use this when you want to check a small set of specific files.

If you want to ensure **all** Markdown files under a directory are clean, even
ones you didn't just edit, prefer the directory scan shown in [Scan a Directory](#scan-a-directory)
instead.

> **Tip:** Listing individual files is great for quick checks, but directory
> scans are usually the better long‑term habit for real projects.

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
any problems it finds.

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
its subdirectories**, reporting any problems that it finds.

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
instead of listing each path manually. It first finds directories that match the
glob pattern `**/docs`, then scans all Markdown files inside those directories.

In this pattern, `**/` means "match any directory depth under the current
directory". `docs` is the directory name that must appear at the end of the path.

If you want a deeper overview of globbing, you can skim a short guide such as
[this globbing guide](https://commandbox.ortusbooks.com/usage/parameters/globbing-patterns),
but you don't need it to follow this Quick Start guide.

After the glob pattern is resolved into a list of paths, PyMarkdown filters that
list. It keeps only files whose names end with `.md`. Changing which file extensions
are scanned is an advanced option. For details, see
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

- files ignored by the project's `.gitignore` file
- files whose names start with `draft_` or `draft-`

These options are useful when you want to enforce Rule Plugins across most of the
project,
but intentionally skip some files. Typical use cases include:

- scanning all documentation but excluding draft articles whose filenames start
  with `draft_` or `draft-`
- scanning a repo without touching generated files (for example, build output or
  temporary files covered by `.gitignore`)

Think of `--respect-gitignore` and `--exclude` as ways to tell PyMarkdown, "treat
these files as if they don't exist for this scan."

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

For more information about excluding paths and using `.gitignore`, see:

- [Excluding Paths](../user-guide.md#-e-exclude-path_exclusions)
- [Respect .gitignore](../user-guide.md#-respect-gitignore)

### How to Read PyMarkdown Commands

A good pattern to remember is:

<!-- pyml disable code-block-style-->
```text
pymarkdown scan [options that change behavior] [path1] [path2] ...
```
<!-- pyml enable code-block-style-->

Put all options right after scan, then list one or more paths at the end. In the
example below, `**/docs` is the only path; everything before it changes how the
scan behaves.

## Debugging Scan Path Issues

Sometimes pymarkdown scan reports Rule Failures in files you didn't expect. Other
times,
it seems to ignore your `--exclude` options.

In both cases, the `--list-files` option helps you see exactly which files are included
in the scan.

The `--list-files` option shows you which files would be scanned, but does not execute
any Rule Plugins. This makes it safe and fast to experiment with your glob patterns
and
exclude settings.

It's common to be surprised by which files a glob pattern matches. Think of
`--list-files` as a preview mode: you see exactly which files would be scanned,
without any analysis or changes to the files themselves.

For example:

- If `pymarkdown scan **/docs` reports Rule Failures in a directory you did not expect,
rerun the command as `pymarkdown scan --list-files **/docs` to see the exact
paths being matched. This helps you debug the pattern without guessing.
- If `--exclude draft_*` seems to have no effect, run
`pymarkdown scan --list-files --exclude draft_* **/docs` to confirm which draft
files are still being picked up.

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

The following commands are available, but they are aimed at more advanced use cases,
so they are not covered in this Quick Start guide. If you're just getting started,
you can safely skip this section now and come back later when you need more flexible
workflows.

- [Scanning From Standard Input](../user-guide.md/#scanning-from-standard-input)
    - useful when you want to pipe Markdown content directly from another tool
      (for example, `cat file.md | pymarkdown scan-stdin`)

## Where to Go From Here?

If you followed along with the examples on your own files, you have:

- run `pymarkdown scan` on individual files, directories, and glob patterns
- experimented with excludes and `.gitignore` handling
- learned how to debug which files are being scanned

**Next**, in the Quick Start guide series:

- Use [Quick Start: Fixing Markdown Files](./fixing.md) to learn how to safely apply
  fixes.

**If** you do not intend to use PyMarkdown's **fix** mode to automatically fix some
of the Rule Failures, you can decide to skip ahead to one of the following pages:

- Use [Quick Start: Managing Rule Plugins](./rules.md) to learn how to enable and
  disable PyMarkdown's Rule Plugins
- Use [Quick Start: Enabling PyMarkdown Extensions](./extensions.md) to learn how
  to enable PyMarkdown's extensions

**If** you need some review:

- Select [Quick Start: Introduction](./index.md) for an overview of all Quick Start
  guides
- Select [Quick Start: Installation](./installation.md) for the steps required to
  install PyMarkdown
- Select [Quick Start: General Command Line Usage](./general.md) for information
  on the general use of PyMarkdown and the command line
- Select [Quick Start: Scanning Markdown Files](./scanning.md) to learn how to scan
  Markdown files with PyMarkdown
