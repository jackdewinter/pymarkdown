# Fixing Markdown Files

**Important:** Any **autofix** performed by PyMarkdown is purely mechanical and is
designed not to alter the meaning of the content. For a rule to provide a “fix”,
the change must be mechanical, changing the format and not changing the content,
and be completely unambiguous.

## Prerequisites

The following sections assume that you have already [installed PyMarkdown](./installation.md)
and are reasonably comfortable with basic [command line usage](./general.md).
The **fix** mode commands also build on the **scan** mode commands described
in the scanning mode [Quick Start document](./scanning.md).

If you are not comfortable with the content of those documents, use the links above
to get started and review them before continuing with this document.

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

## Remaining Fix Mode Commands

As noted above, the **fix** mode commands instruct PyMarkdown to automatically fix
violations for rules that support **autofix**. These commands use the same format
and infrastructure as the **scan** mode commands described in the scanning mode
[Quick-Start document](./scanning.md). In practice, you can take any **scan** command
and replace the argument `scan` with the argument `fix` without changing anything
else. This was explicitly done to keep the **scan** mode interface and the **fix**
mode interface aligned with each other.

For example, the following command scans the file `sample.md` and applies any fixes
supplied by rules that support **autofix**:

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

## Rules With Autofix

**NOTE:** You don’t need to memorize this list — use it as a reference. It is
also colocated in our [User Guide](../user-guide.md#rules-with-autofix)
for easy reference.

For quick reference, these are the built-in rules that currently support **autofix**
in the latest release. The first column presents the rule's identifier and a link
to that rule's `Fix Description` heading in the documentation. The second column
presents the human-readable identifiers that are also used to identify the rule.
The third column contains a short description of the rule itself. This list may
evolve as new rules are added or existing rules gain or lose **autofix** support.

<!-- pyml disable line-length-->

| Rule Id & Link | Human-Readable Identifier | Short Description |
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

## Fix Mode Example

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

**NOTE:** For this example, it is important that the file ends with a line that
is blank. If this is not the case, the example scan output will not match,
and rule MD047 (which checks for a single trailing newline at the end of the file)
will be reported. Please ensure that the file ends with a blank line.

**NOTE:** In Markdown, a line that starts with 1 to 6 `#` characters, followed by
optional spaces and then text, is called an ATX Heading. In this example, we will
use the term "heading" specifically to refer to this type of heading. For more information
on ATX Headings, refer to the Markdown Guide's [headings](https://www.markdownguide.org/basic-syntax/#headings)
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

If you have followed the instructions properly, you should see scan results that
are similar to:

<!-- pyml disable code-block-style-->
```sh
/home/myself/sample.md:3:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
/home/myself/sample.md:3:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```
<!-- pyml enable code-block-style-->

This matches what we expect because line 3 has a heading that is defined with
multiple spaces after the `#` character, triggering rule MD019 (which checks for
multiple spaces after the `#` character in an ATX heading). That same
heading is also a level 1 heading in a document that already has a level 1 heading
defined on line 1, which triggers rule MD025.

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

If you have followed the instructions properly, you should see output that
is similar to the following example:

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

### What Was Fixed?

Because [Rule MD019](../plugins/rule_md019.md) supports **autofix**, it is able
to reduce the number of spaces between the `#` character and the `A` character
on line 3 to a single space. This fix can be performed because this type of heading
in Markdown allows one or more spaces between the `#` character and the next non-whitespace
character. Therefore, PyMarkdown can safely reduce multiple whitespace characters
to a single whitespace character without changing the content in a way that could
be interpreted differently.

### What Was Not Fixed?

The triggering of [Rule MD025](../plugins/rule_md025.md) is different. As summarized
in that rule's [Fix Description](../plugins/rule_md025.md#fix-description), changing
the heading level of the heading on line 3 is too ambiguous for PyMarkdown to fix
automatically, because PyMarkdown cannot know which heading level you intended for
that heading.

Consider the following questions:

- Did the author intend the heading on line 1 or the heading on line 3 to be the
  “real” level 1 heading?
- If line 1 is the intended level 1 heading, should line 3 be changed to a
  level 2 heading instead?
- What if this file were longer and had more headings after line 3? Should all of
  those headings be promoted by one level, or should they be left alone?

Because there are so many possible interpretations, PyMarkdown cannot safely choose
a single “correct” fix. As a result, resolving the violation of Rule MD025 on
line 3 is something you must do manually in your editor by choosing the appropriate
heading level.

## Where to Go From Here

- [Quick Start - Home](./index.md) - Main starting point for all Quick Start documents
- [Quick Start - Scanning Markdown Files](./scanning.md) - Scanning Markdown files
  with PyMarkdown
