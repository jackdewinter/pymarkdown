# PyMarkdown

<!-- pyml disable-num-lines 8 line-length-->
|   |   |
|---|---|
|Project|[![Version](https://img.shields.io/pypi/v/pymarkdownlnt.svg)](https://pypi.org/project/pymarkdownlnt)  [![Python Versions](https://img.shields.io/pypi/pyversions/pymarkdownlnt.svg)](https://pypi.org/project/pymarkdownlnt)  ![platforms](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)  [![License](https://img.shields.io/github/license/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/blob/main/LICENSE.txt)  [![GitHub top language](https://img.shields.io/github/languages/top/jackdewinter/pymarkdown)](https://github.com/jackdewinter/pymarkdown)|
|Quality|[![GitHub Workflow Status (event)](https://img.shields.io/github/actions/workflow/status/jackdewinter/pymarkdown/main.yml)](https://github.com/jackdewinter/pymarkdown/actions/workflows/main.yml)  [![Issues](https://img.shields.io/github/issues/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/issues)  [![codecov](https://codecov.io/gh/jackdewinter/pymarkdown/branch/main/graph/badge.svg?token=PD5TKS8NQQ)](https://codecov.io/gh/jackdewinter/pymarkdown)  [![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fpymarkdown%2Fmain%2Fpublish%2Fdependencies.json&query=%24.mkdocs&label=MkDocs) |
|  | ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fpymarkdown%2Fmain%2Fpublish%2Fdependencies.json&query=%24.black&label=Black)  ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fpymarkdown%2Fmain%2Fpublish%2Fdependencies.json&query=%24.flake8&label=Flake8) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fpymarkdown%2Fmain%2Fpublish%2Fdependencies.json&query=%24.pylint&label=PyLint) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fpymarkdown%2Fmain%2Fpublish%2Fdependencies.json&query=%24.mirrors-mypy&label=MyPy) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fpymarkdown%2Fmain%2Fpublish%2Fdependencies.json&query=%24.pyroma&label=PyRoma) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fpymarkdown%2Fmain%2Fpublish%2Fdependencies.json&query=%24.pre-commit&label=Pre-Commit) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fpymarkdown%2Fmain%2Fpublish%2Fdependencies.json&query=%24.sourcery&label=Sourcery) |
|Community|[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/jackdewinter/pymarkdown/graphs/commit-activity) [![Stars](https://img.shields.io/github/stars/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/stargazers)  [![Forks](https://img.shields.io/github/forks/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/network/members)  [![Contributors](https://img.shields.io/github/contributors/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/graphs/contributors)  [![Downloads](https://img.shields.io/pypi/dm/pymarkdownlnt.svg)](https://pypistats.org/packages/pymarkdownlnt)|
|Maintainers|[![LinkedIn](https://img.shields.io/badge/-LinkedIn-black.svg?logo=linkedin&colorB=555)](https://www.linkedin.com/in/jackdewinter/)|

## Jumping Off Points

- **I want a high-level overview.**\
  Stay on this page to learn what PyMarkdown is, why you might use it, what it
  can do, and whether it fits your projects.
- **I've decided to use PyMarkdown and want to start quickly.**\
  Follow our [Quick Start guides](https://pymarkdown.readthedocs.io/en/latest/quick-starts/)
  to learn the core concepts and start linting your Markdown.
- **I'm comfortable with Python and the command line.**\
  Use the [Fast Path for Experienced Python Users](https://pymarkdown.readthedocs.io/en/latest/quick-starts/advanced)
  to set up PyMarkdown quickly. If you get stuck, that page links back to the regular
  Quick Start guides, so you can slow down when needed.
- **I've finished the Quick Starts or want deeper details.**\
  Read the [full documentation](https://pymarkdown.readthedocs.io/en/latest/) for
  advanced options, configuration, and reference material.

## What Is PyMarkdown?

PyMarkdown is primarily a Markdown linter.

**Structure‑aware linting**\
Instead of scanning raw text, the rules analyze tokens that represent your document's
structure: headings, list items, links, and more. With this structure‑aware view,
rules decide based on document layout rather than raw characters.

**Spec‑compliant parsing**\
These tokens come from PyMarkdown's parser, which follows the [GitHub Flavored Markdown](https://github.github.com/gfm/)
and [CommonMark](https://spec.commonmark.org/) specifications. As a result, PyMarkdown
interprets your document like other tools and bases its rules on parsed structure
instead of simple line‑based pattern matching.

Together, these ideas shape how PyMarkdown analyzes your documents.

### Core Concepts

Internally, PyMarkdown is built around three related pieces that implement this
behavior:

- **Rule Engine** – the system that loads rules, decides which ones are enabled,
  and runs them on your documents.
- **Rule Plugins** – small, focused checks (for example, "heading levels" or "list
  indentation") that the Rule Engine runs.
- **Extensions** – optional changes to how Markdown is parsed (such as extra block
  types or link syntaxes) that the Rule Engine takes into account.

## Why Should I Use PyMarkdown?

Use PyMarkdown if:

- you already use spell or grammar checkers,
- you run static analysis before committing code, or
- you want project‑specific Markdown guidelines without much setup.

In those scenarios, PyMarkdown applies consistent, automated checks to your Markdown
documents.

Start with the built‑in rules and default configuration to lint your documents immediately.
To customize PyMarkdown later, use the [User Guide](https://pymarkdown.readthedocs.io/en/latest/user-guide/)
and related pages.

## What Advantages Does PyMarkdown Have Over Other Markdown Linters?

The PyMarkdown project has the following advantages:

- [Consistency](https://pymarkdown.readthedocs.io/en/latest/#consistency) – behaves
  the same across platforms and environments.
- [Portable](https://pymarkdown.readthedocs.io/en/latest/#portable) – runs on Windows,
  macOS, and Linux with the same configuration.
- [Standardized](https://pymarkdown.readthedocs.io/en/latest/#standardized) – follows
  GFM and CommonMark specifications.
- [Flexible](https://pymarkdown.readthedocs.io/en/latest/#flexible) – lets you configure
  rules and behavior.
- [Thoroughly tested](https://pymarkdown.readthedocs.io/en/latest/#thoroughly-tested)
  \– includes extensive test coverage and quality checks.
- [Extensible](https://pymarkdown.readthedocs.io/en/latest/#extensible) – support
  for custom rules and extensions.

Before you install PyMarkdown, make sure your environment meets the basic requirements.

## Getting Started With PyMarkdown

### What Are The Minimum Requirements?

This project requires Python 3.10 or later.

### How Do I Install PyMarkdown?

For a quick start, run these two commands to install PyMarkdown globally and scan
the current directory (`.`):

```sh
pip install pymarkdownlnt
pymarkdown scan .
```

PyMarkdown also fits into different workflows, such as:

- dependency management with Pipenv and a virtual environment
- installation as a development‑only dependency
- integration as a Pre‑Commit hook

For configuration examples for each of these workflows, see the Quick Start guides
linked from [Jumping Off Points](#jumping-off-points).

## What Linting Checks Does PyMarkdown Release With?

PyMarkdown includes dozens of built‑in linting rules (see the full
[Rules Reference](https://pymarkdown.readthedocs.io/en/latest/rules/)).
They cover common concerns such as:

- heading structure
- list formatting
- link validity
- spacing
- line length

Many of these rules will be familiar if you have used other Markdown linters.

### Relationship to Markdown Lint

#### Familiar Rules, Clearer Behavior

Roughly 44 of the 46 built‑in rules are based on rules from the [Markdown Lint](https://github.com/DavidAnson/markdownlint)
project, a de‑facto standard through its VS Code plugin. We keep the original intent
of those rules but adjust their behavior to follow the Markdown specifications more
closely and to handle real‑world documents more reliably.

The goal is to stay familiar to existing Markdown Lint users while providing
clearer, more predictable results.

#### How PyMarkdown's Rule Engine Differs

As described in [Core Concepts](#core-concepts), PyMarkdown separates checks into
small, focused **Rule Plugins** that run inside a centralized **Rule Engine**. Each
plugin implements a single, clearly defined check (for example, "heading levels"
or "list indentation"), and the engine provides full document context.

Some Markdown Lint rules combine several checks into a single rule or ignore the
full document context. This can lead to missed issues and confusing error messages.

#### A Concrete Example

For example, a rule that enforces maximum line length does not also verify whether
the line contains extra internal whitespace. In PyMarkdown, each of these related
checks is handled by its own Rule Plugin:

- one plugin enforces maximum line length, and
- another plugin checks internal whitespace.

Both rules use the same document context, yet each error message focuses on a single
issue. That focus makes it easier to understand and fix reported problems.

#### Summary

PyMarkdown builds on familiar Markdown Lint rules but aligns them with the Markdown
specifications and with typical real‑world documents, so results are more predictable
and useful.

For an overview of everything that is available, see the
[Rules Reference](https://pymarkdown.readthedocs.io/en/latest/rules/)
and the [Extensions Reference](https://pymarkdown.readthedocs.io/en/latest/extensions/).

## How Do I Run This Tool?

Most users rely on:

- **scan** mode, described in the [Scanning Quick Start](https://pymarkdown.readthedocs.io/en/latest/quick-starts/scanning/),
  and
- **fix** mode, described in the [Fixing Quick Start](https://pymarkdown.readthedocs.io/en/latest/quick-starts/fixing/).

In addition to the command‑line modes, PyMarkdown can also be run in these ways:

- easy-to-use built-in hooks for [Pre-Commit](https://pymarkdown.readthedocs.io/en/latest/quick-starts/installation/#install-pymarkdown-through-precommit)
- a simple [API layer](https://pymarkdown.readthedocs.io/en/latest/api/)

For detailed command‑line usage, see:

- the [Quick Start guides](https://pymarkdown.readthedocs.io/en/latest/quick-starts/general/),
  and
- the [Command Line Basics](https://pymarkdown.readthedocs.io/en/latest/user-guide/#command-line-basics)
  section of the User Guide.

## What If It Is Missing A Feature That I Am Looking For?

If PyMarkdown is missing something you need, we are happy to discuss new features.
In practice, most requests fall into two categories:

- extending the Markdown parser to support a new Markdown extension
- extending the Rule Engine to add a new rule or refine an existing one

Building on the [Core Concepts](#core-concepts):

- you add **Rule Plugins** when you want new or refined checks, and
- you add **extensions** when you want PyMarkdown to understand new Markdown constructs.

The Rule Engine is designed around plugins and extensions, so adding new rules or
extensions fits naturally into the existing architecture.

The [Extending PyMarkdown](https://pymarkdown.readthedocs.io/en/latest/development/#extending-pymarkdown)
section
in our "Development Documentation" explains how we add extensions and Rule Plugins
to PyMarkdown. This process acts as a quality safeguard. Features may take longer
to release, but the additional design, implementation, and testing make their behavior
more predictable.

## Where Can I Find More Detailed Information About PyMarkdown?

All detailed documentation is hosted on
[ReadTheDocs](https://pymarkdown.readthedocs.io/en/latest/) and is
updated with each release.
