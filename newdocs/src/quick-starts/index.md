# Quick Start: Introduction

This collection of Quick Start guides is a hands-on introduction to PyMarkdown,
a Markdown linter that checks your Markdown files for common issues. These guides
are designed for people who are new to PyMarkdown and want a practical way
to start using it in a real project without reading the entire reference first.

These Quick Start guides are **not** a complete reference to every configuration
option or advanced feature that PyMarkdown supports. When you are ready for more
detail, follow the links in this guide to jump to more in-depth sections of the
documentation site.

The main goal of these guides is simple: provide **quick, clear, and actionable**
steps to get you started using PyMarkdown.

You can read this introduction and the rest of the pages in the Quick Start series
listed at the end of this page
in about **20-30 minutes** and then try PyMarkdown on a real project.

## Where to Start

> **Quick Start Guide Single Line Summary**
> This page provides a high-level overview of what PyMarkdown is, how it can
> scan/lint your Markdown files; also providing a solid starting point to the
> other Quick Start guides in the series.

Not sure where to begin?

- I'm just exploring what PyMarkdown is &mdash; **read** the [project's ReadMe File](https://github.com/jackdewinter/pymarkdown)
  to see a quick overview and example usage.

- I've decided to try PyMarkdown on my project &mdash; **stay** in this Quick Start
  introduction to get PyMarkdown running on your machine.

- I'm already using PyMarkdown and want advanced details &mdash; **jump** to the
  [main documentation](../user-guide.md) for full configuration and reference details.

- I'm an advanced user who is not already using PyMarkdown, but I want to get it
  working on my machine as fast as possible; **follow** the
  [Quick Start: Fast Path for Experienced Python Users](./advanced.md) for simplified
  and compressed instructions.

## Call Out To Readers

Our team decided to create these Quick Start guides to provide new users with
a simple introduction to PyMarkdown and how it can help them on their projects.
We will do our best to keep these up-to-date, but we have two asks of you, the reader:

1. If you see something that you believe is incorrect, please [report an issue](../usual.md).
   Please be precise with what the problem is, where you see it, and suggestions
   for improvement.
2. If there is a topic that you believe could be covered more completely in
   a new Quick Start guide, please [report an issue](../usual.md). Our goal as
   project members is to help new users onboard and become efficient with their
   use of PyMarkdown as easily as possible.

## What You Will Learn

In this documentation, you will learn:

- what PyMarkdown is, at a high level
- PyMarkdown's main concepts &mdash; scanning and fixing Markdown documents
- the basic prerequisites you need for the rest of the Quick Start guides

**Note:** This introduction emphasizes concepts &mdash; what PyMarkdown does and
why &mdash; rather than step‑by‑step commands. To run these examples yourself,
use the Quick Start guides linked in the [Where To Go From Here](#where-to-go-from-here)
section.

## What Does PyMarkdown Do

PyMarkdown is a command-line tool that scans your Markdown files and checks them
against a documented set of rules and best practices for Markdown. It is often called
a linter: a program that analyzes Markdown text and reports problems in your documents.
In practical terms, it helps you keep your Markdown clean, consistent, and easy
to read.

If you are already comfortable with Markdown and linting tools, feel free to skim
this section. If not, these brief definitions will make the rest of the guide clearer,
and they are all you need to follow the Quick Start guides.

- **Markdown** is a simple formatting syntax you can embed in a text file. These
  formatting markers keep your text file readable while also enabling certain applications
  to translate that text file into other formats, most commonly HTML. If you are
  not familiar with Markdown or want a refresher, see the [Markdown Guide](https://www.markdownguide.org/)
  for a gentle introduction to Markdown syntax and basic concepts.
- **Markdown files** are plain text files, typically with a `.md` extension, that
  contain Markdown-formatted text.
- **Linters** are tools that analyze your files and report potential problems in
  your documents or code. They help you catch style and formatting issues, as well
  as patterns that might confuse readers or tools that process your files (for example,
  static site generators or documentation builders).
- **Rules** are individual checks that a linter runs to detect specific, named patterns
  in your documents (for example, "headings must be surrounded by blank lines").
- A **Rule Plugin** is a container that holds a single rule that performs a check.
  In most cases, we will refer to the Rule Plugins rather than the rules themselves.
- **Rule Identifiers** are unique for each Rule Plugin. The primary identifier is
  the Rule ID (a short
  code such as `MD001`), and one or more aliases that are human-readable
  and look like `heading-blank-lines`. You can also refer to these identifiers in
  reports and documentation. All Rule Plugin identifiers are case‑insensitive.

PyMarkdown has two modes that you will use most often, and they are designed to
be used in this order:

- **scan** – analyzes Markdown files and reports any Rule Failures without changing
  the files. Use this first when you only want to see what needs to be fixed. It
  is a safe, read‑only way to see what PyMarkdown has found before you make any
  changes.
- **fix** – analyzes Markdown files and, for Rule Plugins that support the **autofix**
  capability, automatically
  updates the files to resolve those Rule Failures. Use this second, after you review
  the scan results and are comfortable letting PyMarkdown make safe, mechanical
  formatting changes (such as adjusting whitespace or line breaks) instead of fixing
  everything by hand.

Most people start with **scan** mode to understand what PyMarkdown reports, then
begin using **fix** mode once they are familiar with the kinds of changes it makes.

## Scan Mode

In this step, you will learn how to run **scan** and interpret its output.

In **scan** mode, PyMarkdown runs an extensive collection of built‑in Rule Plugins
against
your Markdown files by default &mdash; for example, checking heading spacing or
list formatting. Each Rule Plugin checks for a specific pattern or problem, so you
do not
need to remember every Rule Plugin by name.

### How PyMarkdown Reports Rule Failures

For each time that a Rule Plugin reports a failure, PyMarkdown
reports:

- which file caused the failure
- where in the file the violation occurred (line and column)
- an explanation of the failure
- sometimes extra data to clarify the error. For example, PyMarkdown may show the
  expected versus actual number of spaces or the heading level. This extra detail
  helps you understand exactly how to fix the problem.

Below is a relatively simple example of **scan** mode's output, showing three Rule
Failures.
This shows what you can expect, followed by a line-by-line explanation.

If you have not used linters or command-line tools like this before, the output
can look dense.

> **Beginner tip:** Don't worry if this looks confusing at first. We'll break down
> each piece of the first line so you can learn the pattern.

```text
sample.md:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```

### How to Interpret Reported Rule Failures

At first glance, this output may look daunting, but each line follows a predictable
pattern. In this section, you will learn how to read any line of scan output and
quickly identify the file, line, Rule Plugin, and the change you need to make.

Focusing on the first failure (the first line of output):

- the text `sample.md:1:1:` tells us **which file caused the failure** and
  **where in the file the failure occurred**.
- the text `MD022` is the **primary identifier** for this failure, and
  `Headings should be surrounded by blank lines.` provides a **human-readable description**
  of the failure.
    - If you are looking for a shorter but still human-readable description of the
      failure, the text `(blanks-around-headings,blanks-around-headers)` provides
      **aliases** (short, human‑readable names) for the Rule Plugin that owns
      the failure.
- the text `[Expected: 1; Actual: 0; Below]` shows the details of the failure. It
  tells you that PyMarkdown expected 1 blank line below the heading, but found 0.

### Practice Reading PyMarkdown Output

This output format may be unfamiliar at first, but it follows a tried‑and‑true style
used by many linters and other tools. After you scan your Markdown files a few times
and work through the examples in this guide, reading this output should feel natural.

When you see output like this for your own files, a simple way to read it is:

- Look at the **file name and line number** (e.g., `sample.md:1:1`) to jump to the
  right spot in that Markdown document.
- Read the **description** (e.g., `Headings should be surrounded by blank lines.`)
  to understand the failure.
- Use the **extra details** (e.g., `[Expected: 1; Actual: 0; Below]`) to see exactly
  what to change.

After you apply this pattern to your own files a few times, reading PyMarkdown's
output will feel much faster and more natural. For instance, you will be able to
open `sample.md`, jump straight to line 1, and add a blank line below the heading
to satisfy the `Expected: 1` detail. Over time, you will build confidence in what
each failure means and how to fix it in your Markdown files.

### Scan Mode Summary

By now, you should be able to:

- read the basic scan output format
  (`file:line:column: rule: description [details] (identifiers)`),
- locate the right spot in a Markdown file using the file name and line number,
  and
- use the description and extra details to work out the exact edit you need to make
  in the file.

Next, you will see how **fix** mode can automatically apply some of these changes
for you.

## Fix Mode

In this final step, you will learn how to use **fix** mode to apply safe formatting
changes.

In **fix** mode, PyMarkdown automatically fixes Rule Failures, but only for Rule
Plugins that
support the **autofix** capability. These plugins can safely adjust formatting,
such as whitespace
and line breaks, without changing the meaning of your text.
Any change that might affect the content or structure of what you are saying is
always left to you.

If a Rule Plugin does not support the **autofix** capability, its documentation
explains why PyMarkdown
cannot change it automatically and suggests how you can fix that type of Rule Failure
by hand.
In most cases, a Rule Plugin does not support **autofix** when fixing the problem
would require rewriting
your content or could change its meaning.

### Scan The File

A good way to try fix mode is to create a new file, add the following content, and
then scan it. Given this file, named `sample.md`:

<!-- pyml disable code-block-style-->
```Markdown
# Heading 1

#  Another Heading 1
```
<!-- pyml enable code-block-style-->

When scanned, it will give the following output:

<!-- pyml disable code-block-style-->
```sh
sample.md:3:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
sample.md:3:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```
<!-- pyml enable code-block-style-->

Using the same method as illustrated in the previous section on
[How PyMarkdown Reports Rule Failures](#how-pymarkdown-reports-rule-failures), you
should
be able to read that this file's line 3 has two issues: an Atx Heading with an extra
space (`no-multiple-space-atx`) and two level-1 headings (`single-title`).

### After Applying Fix Mode

After executing PyMarkdown on that `sample.md` file in **fix** mode, that file will
then have the contents:

<!-- pyml disable code-block-style-->
```Markdown
# Heading 1

# Another Heading 1
```
<!-- pyml enable code-block-style-->

This is because the first Rule Plugin, `MD019` or `no-multiple-space-atx` supports
the
**autofix** capability
while the second Rule Plugin `MD025` or `single-title` does not support the **autofix**
capability. As
`no-multiple-space-atx` supports the **autofix** capability, it remedied the failure
by reducing
the number of spaces after the `#` to a single character.

For completeness, if you scan `sample.md` again after running **fix** mode, only
one failure will be reported.

<!-- pyml disable code-block-style-->
```sh
sample.md:3:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```
<!-- pyml enable code-block-style-->

This pattern &mdash; scan to see all issues, then fix to apply only safe formatting
changes &mdash; is the recommended way to use PyMarkdown on your projects.

## What Is The Usual Usage Pattern For PyMarkdown?

At a high level, in normal use, you will usually:

- run **scan** to see all Rule Failures in your Markdown files,
- review the results and decide what to fix,
- run **fix** to apply safe formatting changes automatically, and
- make any remaining content or structural edits by hand.

If you are not sure if you have fixed all Rule Failures, you simply restart with
the
first item on that list and work through the list again until you are happy with
the results from **scan** mode.

## Prerequisites

You do not need to be an expert in Python or tooling to use these Quick Start guides.

### Required

These are the basics you should be comfortable with before using the Quick Start
guides.

- **Running commands such as `pymarkdown scan sample.md` in a terminal or command
  prompt**
  You will execute PyMarkdown from a terminal, command prompt, or shell window.

- **Basic Python installation concepts**
  You should have Python installed (version 3.10 or later), and either:
    - be able to install packages with `pip`, or
    - be able to use a tool such as `pipenv` to manage a virtual environment for
      your project.

### Optional, but helpful

These tools are not required, but they can automate PyMarkdown in your workflow.

- **Git and Pre‑Commit**
  If you want PyMarkdown to run automatically each time you commit changes, you
  can set it up with Pre‑Commit, a tool that manages pre-commit hooks in your Git
  repositories.
  
To do this, you should:

- have a Git repository for your project, and
- be comfortable installing and configuring [Pre‑Commit](https://pre-commit.com/)
  for that repository.

## Wrap-Up

If any of these topics are unfamiliar, you can still follow the examples in this
guide and run PyMarkdown from the command line. At minimum, you only need to:

- open a terminal or command prompt,
- run the example commands that we show you, and
- read the output that PyMarkdown prints.

You do not need to master these tools before trying PyMarkdown for the first time.

## Where To Go From Here

**A common path** through the Quick Start guides (and a good first-time learning
order) is:

- [Quick Start: Installation](./installation.md) - How to Install PyMarkdown
- [Quick Start: General Command Line Usage](./general.md) - Use of PyMarkdown from
  the command line
- [Quick Start: Scanning Markdown Files](./scanning.md) - Scanning Markdown files
with PyMarkdown
- [Quick Start: Fixing Markdown Files](./fixing.md) - Safely fixing Markdown files

**If you have solid Python and command line skills** and just want to try PyMarkdown
out as efficiently as possible:

- [Quick Start: Fast Path for Experienced Python Users](./advanced.md) - No frills
  guide to getting started with PyMarkdown

**After you are comfortable with the basics** (installing PyMarkdown, running `scan`,
and optionally using `fix` on a sample file), you can explore:

- [Quick Start: Managing Rule Plugins](./rules.md) - Enabling PyMarkdown Rule Plugins
- [Quick Start: Enabling PyMarkdown Extensions](./extensions.md) - Enabling PyMarkdown
  extensions
