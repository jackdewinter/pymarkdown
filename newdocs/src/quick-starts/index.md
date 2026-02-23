# Quick Start Introduction

This collection of Quick Start guides is a hands-on introduction to PyMarkdown,
a Markdown linter that checks your Markdown files for common issues. These guides
focus on the few essential concepts you need to start using PyMarkdown in a real
project so you can improve your documents.

These Quick Start guides are **not** a complete reference to every configuration
option or advanced feature that PyMarkdown supports. When you are ready for more
detail, follow the links in this guide to jump to more in-depth sections of the
documentation site. The main goal of these guides is simple: provide
**quick, clear, and actionable** steps to get you started using PyMarkdown.

## Where to Start

If you are looking for a high-level overview of PyMarkdown &mdash; what it is and
why you should use it &mdash; the [main README.md file](http://github.com/jackdewinter/PyMarkdown)
is a great place to start learning how PyMarkdown works, what it can do, and whether
it is a good fit for your projects.

If you have decided to use PyMarkdown for your Markdown linting needs, continue
with this Quick Start introduction to get started quickly and learn the core concepts
of installing, configuring, and using PyMarkdown on your own Markdown files.

If you have already viewed our Quick Start guides, or simply want more information
on PyMarkdown and its capabilities, [start reading here](https://pymarkdown.readthedocs.io/en/latest/)
to explore the full documentation for advanced options, configuration details, and
reference material.

## Purpose: What PyMarkdown Does

PyMarkdown is a command-line tool that scans your Markdown files and checks them
against a documented set of rules and best practices for Markdown. It is often called
a linter: a program that analyzes Markdown text and reports problems in your documents.
In practical terms, it helps you keep your Markdown clean, consistent, and easy
to read.

- **Markdown** is a simple formatting syntax you can embed in a text file. These
  formatting markers keep your text file readable while also enabling certain applications
  to translate that text file into other formats, most commonly HTML. If you are
  not familiar with Markdown or want a refresher, see the [Markdown Guide](https://www.markdownguide.org/)
  for a gentle introduction to Markdown syntax and basic concepts.
- **Markdown files** are plain text files, typically with a `.md` extension, that
  contain Markdown-formatted text.
- **Linters** are tools that analyze your files and report potential problems in
  your documents or code. They help you spot style issues, formatting problems,
  or patterns that might cause confusion for readers or for other tools that process
  your files, such as static site generators or documentation builders that turn
  your Markdown into websites or documentation.
- **Rules** are individual checks that a linter runs to detect specific, named
  patterns in your documents (for example, "headings must be surrounded by blank
  lines"). Each rule has two kinds of identifiers: a primary identifier and one
  or more alternate, human‑readable identifiers. The primary identifier is a short
  code such as `MD001`, and an alternate identifier might look like `heading-blank-lines`.
  You use these identifiers when configuring PyMarkdown or running it from the command
  line&mdash;for example, to enable, disable, or fine-tune specific rules, or to
  refer to specific rules in reports and documentation. All rule identifiers are
  case‑insensitive.

PyMarkdown has two main modes you will use most often, and they are designed to
be used in this order:

- **scan** – analyzes Markdown files and reports any rule violations without changing
  the files. Use this first when you only want to see what needs to be fixed; it
  is a safe, read‑only way to see what PyMarkdown has found in your files before
  you make any changes.
- **fix** – analyzes Markdown files and, for rules that support **autofix**, automatically
  updates the files to resolve those violations. Use this second, after you have
  reviewed the scan results and are comfortable letting PyMarkdown make safe, mechanical
  formatting changes (such as adjusting whitespace or line breaks) for you instead
  of fixing everything by hand. In other words, start with **scan**, then move on
  to **fix** once you trust the changes it makes.

Most people start with **scan** mode to understand what PyMarkdown reports, then
begin using **fix** mode once they are familiar with the kinds of changes it makes.

### Scan Mode

In **scan** mode, PyMarkdown runs an extensive collection of built‑in rules against
your Markdown files by default &mdash; for example, checking heading spacing or
list formatting. Each rule checks for a specific pattern or problem, so you do not
need to remember every rule by name. For each rule that is violated, PyMarkdown
reports:

- which file caused the violation
- where in the file the violation occurred (line and column)
- an explanation of the issue
- sometimes extra data to clarify the error. For example, PyMarkdown may show the
  expected versus actual number of spaces or the heading level. This extra detail
  helps you understand exactly how to fix the problem.

Here is a relatively simple example of scan output, copied from Step 4 of our
[Verifying PyMarkdown Installation](./installation.md#verifying-pymarkdown-installation)
section in the Quick Start guide for PyMarkdown Installation:

```text
sample.md:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```

While this output may look daunting at first, it is intended to describe everything
that you need to know about each reported issue in a concise manner. Focusing
on the first issue (the first line of output):

- the text `sample.md:1:1:` tells us **which file caused the violation** and
  **where in the file the violation occurred**.
- the text `MD022` is the primary rule identifier for this issue, and
  `Headings should be surrounded by blank lines.` provides a human-readable description
  of the issue.
    - If you are looking for a shorter but still human-readable description of the
      issue, the text `(blanks-around-headings,blanks-around-headers)` provides
      alternate identifiers (short, human‑readable names) for the rule that owns
      the issue.
- to help you understand details about the issue, the text
  `[Expected: 1; Actual: 0; Below]` lets you know that PyMarkdown was expecting
  the heading to have 1 blank line below the heading, but encountered 0 blank lines.

This output format may be unfamiliar at first, but it is a tried-and-true format
used by many linters and other tools. After you scan your Markdown files and follow
a few real-world examples, you should quickly get he hang of it.

### Fix Mode

In **fix** mode, PyMarkdown automatically fixes violations, but only for rules that
support **autofix**. These are rules that can safely modify your Markdown files
without changing their meaning. In practice, this usually means adjusting whitespace,
line breaks, or other formatting details&mdash;not rewriting your text or changing
the intent of your content.

If a rule does not support **autofix**, its documentation explains why PyMarkdown
cannot change it automatically and suggests how you can fix it manually instead.
In most cases, PyMarkdown skips autofix because fixing the issue would require rewriting
your content in a way that might change its meaning, which PyMarkdown rules are
not allowed to do. This design ensures that autofix only performs safe, mechanical
formatting changes, not edits that change what you are saying or how your document
is structured.

## Prerequisites

You do not need to be an expert in Python or tooling to use these Quick Start guides,
but you should be reasonably comfortable with basic use of:

- **Running commands in a terminal or command prompt**
  You will run commands such as `pymarkdown scan sample.md` yourself from a terminal,
  command prompt, or shell window.

- **Basic Python installation concepts**
  You should have Python installed (version 3.10 or later), and either:
    - be able to install packages with `pip`, or
    - be able to use a tool such as `pipenv` to manage a virtual environment for
      your project.

- **(Optional) Git and Pre‑Commit**
  If you want PyMarkdown to run automatically each time you commit changes, you
  can set it up with Pre‑Commit, a tool that manages pre-commit hooks in your Git
  repositories.
  
  To do this, you should:
    - have a Git repository for your project, and
    - be comfortable installing and configuring [Pre‑Commit](https://pre-commit.com/)
      for that repository.

If any of these topics are unfamiliar, you can still follow the examples in this
guide and run PyMarkdown from the command line. You may want to review a short tutorial
on your operating system’s terminal, Python installation, or Git/Pre‑Commit before
setting up PyMarkdown in a real project, but that review is not required just to
try the commands in these Quick Start guides.

## Where To Go From Here

- [Quick Start - Installation](./installation.md) - How to Install PyMarkdown
- [Quick Start - General Command Line Usage](./general.md) - Use of PyMarkdown from
  the command line
- [Quick Start - Scanning Markdown Files](./scanning.md) - Scanning Markdown files
  with PyMarkdown
- [Quick Start - Fixing Markdown Files](./fixing.md) - Fixing Markdown files with
  PyMarkdown
