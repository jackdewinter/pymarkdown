# Quick Start: Fixing Markdown Files

Now that you are familiar with [Quick Start: Scanning Markdown Files](./scanning.md),
the previous page in our Quick Start guide series that showed how to *find* Rule
Failures, let's move on to fixing some of those reported Rule Failures.

If you have not read the scanning Quick Start guide yet, we recommend visiting
it first
so the examples in this page make sense.

On the previous page, you learned how to use PyMarkdown to *scan* files and report
Rule Failures. On this page, you will use PyMarkdown to *fix* some of those Rule
Failures automatically, using Rule Plugins that support the **autofix** capability.

**Important:** Any fixing performed by PyMarkdown in **fix** mode is purely mechanical.
It is designed not to change the meaning of your content.

A Rule Plugin can only offer the **autofix** capability if the change:

- adjusts formatting, not the wording or meaning, and
- is completely unambiguous.

For example, removing extra spaces after a `#` in a heading is safe, but rewriting
a heading from "Overview" to "Introduction" is not.

Once you know how to scan for Rule Failures, letting PyMarkdown fix the ones that
support the **autofix** capability is the obvious next step. It helps you reduce
or eliminate Rule
Failures more quickly, and the process is easy to automate in scripts.

## What You Will Learn

> **Quick Start Guide Single Line Summary**
> This page leverages your knowledge on scanning with PyMarkdown to explain
> how PyMarkdown's **fix** mode works to automatically correct Rule Failures.

On this page, you will:

- run your first `fix` command with PyMarkdown
- identify which Rule Plugins currently support the **autofix** capability
- work through a complete `fix` example on a single file:
    - scan the file
    - fix the file
    - interpret what was fixed, what was not fixed, and why
- apply the `fix` command to multiple files or directories

## Prerequisites

The following sections assume that you have already [installed PyMarkdown](./installation.md)
and can run basic commands from a terminal (for example, changing directories and
running `pymarkdown`). The **fix** mode commands also build on what you learned about
the **scan** mode commands described on the [Quick Start: Scanning Markdown Files](./scanning.md)
page.

If any of that feels unfamiliar, use the links above to walk through those pages
first, then return here when you are ready to try fixing files.

## Get Help for the `fix` Command

Just like the `help` command for **scan** mode, the `fix` command with the `--help`
option prints help text for the command-line options and arguments available in
**fix** mode.

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown fix --help
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown fix --help
    ```

<!-- pyml enable code-block-style-->

## Fix Mode Commands

The **fix** mode commands automatically fix any Rule Failures for Rule Plugins
that support
the **autofix** capability. They:

- use the same options and arguments as **scan** mode commands
- differ only in the subcommand name: `scan` vs `fix`

In practice, you can take any scan command and replace `scan` with `fix`. For example,
the following command applies available fixes to the file `sample.md`:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown fix sample.md
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown fix sample.md
    ```

and this command applies fixes to all files in any directories named `docs` under
the current directory:

=== "Global Python Install"

    ```sh
    pymarkdown fix **/docs
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown fix **/docs
    ```

<!-- pyml enable code-block-style-->

Aside from the fact that commands starting with `scan` run in **scan** mode and
commands starting with `fix` run in **fix** mode, the **scan** mode and **fix**
mode commands are otherwise identical.

## Rule Plugins With Autofix

When you run `pymarkdown scan`, you'll see Rule IDs like `MD019` or `MD025` in the
output. Some of those Rule Plugins support the **autofix** capability and can be
fixed automatically;
others cannot.

For quick reference, these are the built-in Rule Plugins that currently support
the **autofix** capability
in the latest release. It is presented
here so those users following along with these examples in their own directories
can understand what Rule Failures they should expect to get fixed.

**NOTE:** Don't memorize this list &mdash; use it as a reference. For this Quick
Start guide, you only need to know that some Rule Plugins in your scan output can
be fixed
automatically.
The full list is also available in our [User Guide](../user-guide.md#rule-plugins-with-autofix)
for easy reference.

<!-- pyml disable line-length-->

| Rule ID & Link | Human-Readable Identifier | Short Description |
| -- | -- | -- |
| [MD001](../plugins/rule_md001.md#fix-description) | `heading-increment`, `header-increment` | Heading levels should only increment by one level at a time. |
| [MD004](../plugins/rule_md004.md#fix-description) | `ul-style` | Inconsistent Unordered List Start style. |
| [MD005](../plugins/rule_md005.md#fix-description) | `list-indent` | Inconsistent indentation for list items at the same level. |
| [MD007](../plugins/rule_md007.md#fix-description) | `ul-indent` | Unordered list indentation. |
| [MD009](../plugins/rule_md009.md#fix-description) | `no-trailing-spaces` | Trailing spaces. |
| [MD010](../plugins/rule_md010.md#fix-description) | `no-hard-tabs` | Hard tabs. |
| [MD013](../plugins/rule_md013.md#fix-description) | `line-length` | Line length. |
| [MD019](../plugins/rule_md019.md#fix-description) | `no-multiple-space-atx` | Multiple spaces are present after hash character on Atx Heading. |
| [MD021](../plugins/rule_md021.md#fix-description) | `no-multiple-space-closed-atx` | Multiple spaces are present inside hash characters on Atx Closed Heading. |
| [MD023](../plugins/rule_md023.md#fix-description) | `heading-start-left`,`header-start-left` | Headings must start at the beginning of the line. |
| [MD027](../plugins/rule_md027.md#fix-description) | `no-multiple-space-blockquote` | Multiple spaces after blockquote symbol. |
| [MD029](../plugins/rule_md029.md#fix-description) | `ol-prefix` | Ordered list item prefix. |
| [MD030](../plugins/rule_md030.md#fix-description) | `list-marker-space` | Spaces after list markers. |
| [MD035](../plugins/rule_md035.md#fix-description) | `hr-style` | Horizontal rule style. |
| [MD037](../plugins/rule_md037.md#fix-description) | `no-space-in-emphasis` | Spaces inside emphasis markers. |
| [MD038](../plugins/rule_md038.md#fix-description) | `no-space-in-code` | Spaces inside code span elements. |
| [MD039](../plugins/rule_md039.md#fix-description) | `no-space-in-links` | Spaces inside link text. |
| [MD044](../plugins/rule_md044.md#fix-description) | `proper-names` | Proper names should have the correct capitalization. |
| [MD046](../plugins/rule_md046.md#fix-description) | `code-block-style` | Code block style. |
| [MD047](../plugins/rule_md047.md#fix-description) | `single-trailing-newline` | Each file should end with a single newline character. |
| [MD048](../plugins/rule_md048.md#fix-description) | `code-fence-style` | Code fence style should be consistent throughout the document. |

<!-- pyml enable line-length-->

This list may evolve as new Rule Plugins are added or existing Rule Plugins gain
or lose **autofix**
support. For each Rule Plugin, the first column links to the Rule Plugin's
`Fix Description` in
the documentation, the second column lists human-readable identifiers, and the third
column gives a short description.

## Fix a Single File

Now that you have seen how to run `pymarkdown fix` and which Rule Plugins support
the **autofix** capability,
let's walk through a complete example on a single file.

### Create a File to Scan

For this example, open a console and change to a directory where you
have permission to create files. In this example, we
will refer to that directory as `/home/myself`. Then start the editor of your choice
in that directory and create a file named `sample.md` whose contents are two headings:

<!-- pyml disable code-block-style-->
```Markdown
# Heading 1

#  Another Heading 1
```
<!-- pyml enable code-block-style-->

**NOTE:** Make sure `sample.md` ends with a blank line so your scan results match
the example in this Quick Start guide.

**NOTE:** In Markdown, a line that starts with 1 to 6 `#` characters, followed
by one or more spaces and then text, is called an ATX Heading. Both headings in
`sample.md` are ATX headings of this form. In this example, we will use the term
"heading" specifically to refer to this type of heading. For more background, you
can later refer to the Markdown Guide's [headings](https://www.markdownguide.org/basic-syntax/#headings)
documentation.

### Scan the File

After following those directions, go to the console and type the following
command to scan the file:

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

When you run the above scan command, the output should show two specific Rule Failures
(`MD019` and `MD025`). If your file does not end with a blank line, you may also
see
Rule Plugin `MD047`, which checks for a single trailing newline at the end of the
file.
If `MD047` appears, add a blank line at the end of `sample.md`, save, and run the
scan again.

<!-- pyml disable code-block-style-->
```sh
/home/myself/sample.md:3:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
/home/myself/sample.md:3:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```
<!-- pyml enable code-block-style-->

This matches what we expect. Line 3 has a heading with multiple spaces after the
`#` character, which triggers Rule Plugin `MD019` (extra spaces after `#` in an
ATX heading).
The same heading is also a level‑1 heading in a document that already has a level‑1
heading on line 1, which triggers Rule Plugin `MD025`.

### Fixing the File

After verifying that your scan results match the output specified above, go
back to your console and type the following command to fix the same file:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown fix sample.md
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown fix sample.md
    ```
<!-- pyml enable code-block-style-->

After running that command, you should see output similar to:

<!-- pyml disable code-block-style-->
```bash
Fixed: /home/myself/sample.md
```
<!-- pyml enable code-block-style-->

and if you open the `sample.md` file, you will notice the change to the
heading on line 3:

<!-- pyml disable code-block-style-->
```Markdown
# Heading 1

# Another Heading 1
```
<!-- pyml enable code-block-style-->

To see which Rule Failures remain, run the scan command from the [Scan the File](#scan-the-file)
section again. The returned output should validate that the Rule Failure for `MD019`
was fixed.

<!-- pyml disable code-block-style-->
```sh
/home/myself/sample.md:3:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```
<!-- pyml enable code-block-style-->

### What Was Fixed?

Because [Rule Plugin MD019](../plugins/rule_md019.md) supports the **autofix** capability,
it can reduce
the spaces between the `#` character and the next character on line 3 to a single
space. In Markdown, this type of heading allows one or more spaces after the `#`,
so PyMarkdown can safely collapse multiple spaces into one without changing the
meaning of the heading.

### What Was Not Fixed?

The situation for [Rule Plugin MD025](../plugins/rule_md025.md) is different. As
described
in that Rule Plugin's [Fix Description](../plugins/rule_md025.md#fix-description),
changing
the level of the heading on line 3 is too ambiguous for PyMarkdown to fix automatically,
because it cannot tell which level you intended.

Consider the following questions:

- Did the author intend the heading on line 1 or the heading on line 3 to be the
  "real" level 1 heading?
- If line 1 is the intended level 1 heading, should line 3 be changed to a
  level 2 heading instead?
- What if this file were longer and had more headings after line 3? Should all of
  those headings be promoted by one level, or should they be left alone?

Because there are so many possible interpretations, PyMarkdown cannot safely choose
a single "correct" fix. As a result, resolving the violation of Rule `MD025` on
line 3 is something you must do manually in your editor by choosing the appropriate
heading level. A simple approach is:

- pick a single `#` heading as the main document title
- change any additional `#` headings to `##` (or deeper) to reflect the structure
  you want

You can take this above approach with any of the unfixed Rule Failures to whittle
away at the list of manual fixes you need to apply.

## Fix Multiple Files or Directories

The example above used a single file, `sample.md`. In real projects, you'll usually
want to fix many files at once. Since `fix` and `scan` share the same options, you
can reuse the same command patterns from the scanning Quick Start guide.

Earlier, in the [Scan Glob Paths](./scanning.md#scan-glob-paths) section, you saw
that `**/docs` means "all docs directories under the current directory".

To apply any available fixes with the same pattern, first scan:

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

Review the reported Rule Failures, then run:

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

to apply fixes for any Rule Plugins that support the **autofix** capability to
all matching files.

## Where to Go From Here

If you followed along with the examples on your own files, you have:

- run `pymarkdown scan` and then `pymarkdown fix` on an individual file
- learned that calling patterns learned for the `scan` command work with the `fix`
  command

Depending on what you want to do next, choose one of:

**Next**, in the Quick Start guide series:

- Use [Quick Start: Managing Rule Plugins](./rules.md) to learn how to turn specific
  Rule Plugins on or off

**If** you want to skip ahead, you can go to the following page:

- Use [Quick Start: Enabling PyMarkdown Extensions](./extensions.md) to learn how
  to add extra features via extensions

**If** you need some review:

- Select [Quick Start: Introduction](./index.md) for an overview of all Quick Start
  documents
- Select [Quick Start: Scanning Markdown Files](./scanning.md) for a refresher on
  how to scan files for Rule Failures
