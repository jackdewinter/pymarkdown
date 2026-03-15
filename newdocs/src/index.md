# Introduction

## Note to New Readers

As part of our effort to prepare for the upcoming version 1.0.0 release, we are
moving our documentation from plain Markdown files hosted on [GitHub](https://github.com/jackdewinter/pymarkdown)
to this new centralized documentation site that you are currently reading. We
appreciate your patience as we complete this transition.

## Where to Start

If you are looking for a high-level overview of PyMarkdown &mdash; what it is, why
you might use it, and what it can do &mdash; the [main README.md file](http://github.com/jackdewinter/PyMarkdown)
is a great place to start and to decide whether PyMarkdown is a good fit for your
project, your workflow, and your team.

If you have decided to use PyMarkdown for your Markdown linting needs, read our
[Quick Start guides](https://pymarkdown.readthedocs.io/en/latest/quick-starts/)
to get started quickly and learn the core concepts of installing, configuring, and
using PyMarkdown on your own Markdown files.

If you have already viewed our Quick Start guides, or simply want more information
on PyMarkdown and its capabilities, continue reading. By using the contents located
on the left and right sidebars, you can quickly navigate to information about advanced
options, configuration details, and other reference material that you can explore
as you become more comfortable with PyMarkdown and want to go beyond the basics.

## Core PyMarkdown Concepts

PyMarkdown is primarily a Markdown linter. It scans your Markdown files and checks
them against a set of rules to find potential problems and style issues.

To do this, PyMarkdown uses its own Markdown parser instead of relying on regular
expressions or ad‑hoc text patterns. This parser is designed to follow the
[GitHub Flavored Markdown](https://github.github.com/gfm/) and
[CommonMark](https://spec.commonmark.org/) specifications, which many other
Markdown tools also follow.

Because our rules work with the structured output of this parser, they can reason
about headings, lists, links, and other elements in the same way that typical
Markdown renderers do. This helps ensure that the issues they report match how
your documents will be interpreted on common platforms.

## Background and Foundational Information

The rest of this document provides background information about Markdown, linters,
and reasons to use the PyMarkdown linter for your projects. If you already understand
these topics, continue on to the section on [What to Do Next](#what-to-do-next).

## What is Markdown?

Markdown is a plain‑text format with simple markers that indicate structure, such
as headings, lists, and links. These markers keep the text readable while making
it easy for tools to turn it into HTML or other formats. If you look at the raw
Markdown for [this page](https://raw.githubusercontent.com/jackdewinter/pymarkdown/main/newdocs/src/index.md),
you will see that, apart from a few simple markers, it reads like normal text.

Our team prefers Markdown because it lets us focus on content instead of layout.
When we write documentation, we can concentrate on what we want to say and how it
is organized. We defer visual style decisions until later, when we can apply them
consistently across the site.

## What Is a Linter?

As noted above, early software developers established the term
[linting](https://en.wikipedia.org/wiki/Lint_%28software%29) near the dawn of modern
software development. Stephen C. Johnson needed a tool to spot issues with his code
and filter them out, like a lint trap in a clothes dryer. Although the term may
have unusual origins, the name stuck, and the benefits imparted by linters remain
to this day. A linter is an additional process with distinct goals, designed to
check for a specific set of issues in the source code that powers a software application
or system.

We have found that the easiest way to explain linters is to say that their functionality
is analogous to spell checkers and grammar checkers. As a matter of principle, our
team only publishes documentation after running it through both spell and grammar
checkers. This parallels our source code, where we run Python checkers over our
source code to ensure that we are adhering to our own source code guidelines. If
we extend that idea to view documentation as a kind of source code, it makes sense
to have a checker for it as well. That checker should help keep our Markdown documents
consistent and easy to read, just like the tools we use for our source code. That
is where the PyMarkdown linter fits into the picture for our projects.

## Can It Do Anything Else?

While PyMarkdown is primarily a Markdown linter, the breadth of the application
has grown over the years of its development. In **scan** mode, the linter can
detect Markdown issues using a robust set of Markdown-specific rules. In **fix**
mode, certain Markdown issues can be automatically corrected without external
involvement or manual editing. While **fix** mode is a relatively new part of the
project,
we believe that it provides a measurable benefit to our users by reducing the effort
required to clean up documents. That combination is something we are enormously
proud of!

## Why Is This Application Referred to as PyMarkdown and PyMarkdownLnt?

Originally, we thought that "PyMarkdown Linter" was a good name for the application
&mdash; until we had to start typing it repeatedly. By that point, we had already
registered the package on the [Python Package Index (PyPI)](https://pypi.org/)
as ["pymarkdownlnt"](https://pypi.org/project/pymarkdownlnt/), because there already
was another project named ["pymarkdown"](https://pypi.org/project/pymarkdown/) that
was only released once in 2015. The "lnt" suffix in "pymarkdownlnt" is a shortened
form of "linter".

Going forward, we plan to use the "PyMarkdown" name consistently in all documentation
to reduce confusion between the project name and the package name "pymarkdownlnt".

## Why Use PyMarkdown?

The PyMarkdown project has the following advantages:

### Consistency

This project's interfaces (primarily a command-line interface) can examine multiple
files and directories with a single run, ensuring that all targeted Markdown files
adhere to the provided set of guidelines. This allows users to execute the project
within a [CI/CD](https://en.wikipedia.org/wiki/CI/CD) pipeline to verify the correctness
of documentation within their own repositories. For project maintainers, this is
a big advantage because it helps keep their projects well-structured, consistent,
and free of common Markdown issues.

### Portable

This project runs on any system that has Python 3.10 or later installed, without
requiring any modifications to the PyMarkdown code itself. Before any code changes
are merged into the project's "main" branch, every scenario test (tests that run
PyMarkdown against realistic Markdown examples) is executed against the application.
These tests are then repeated across Linux, Windows, and macOS environments to detect
and resolve any portability issues before the merge is approved. If any problems
arise on any supported operating system, we address those problems before any users
are inconvenienced.

### Standardized

As mentioned above, we strive to keep the project's Markdown parser compliant with
both the [GitHub Flavored Markdown](https://github.github.com/gfm/)
specification and the [CommonMark](https://spec.commonmark.org/) specification.
Utilizing that foundation, the Rule Engine does not have to guess how a Markdown
parser may handle a given situation. Instead, PyMarkdown's own compliant parser
feeds the Rule Engine with information on how it handled the document. From
experience, we find that this approach produces more accurate results than trying
to use text-based patterns and regular expressions to guess how a Markdown
parser may parse Markdown text.

### Flexible

You can run PyMarkdown in several ways, depending on your workflow. It supports
direct command‑line use, integration into your own Python tools, and Git Pre‑Commit
hooks that run automatically before each commit.

Behind the scenes, PyMarkdown's rules can either work with a structured view of
your document or use simpler line‑by‑line checks. For more details about how this
works, see the [User Guide](./user-guide.md#nomenclature) sections on the parser
and Rule Engine.

### Thoroughly Tested

We track how thoroughly PyMarkdown is tested and use that information to guide
our development. By regularly running tests on real Markdown documents and monitoring
how much of the code they exercise, we can detect problems early and avoid surprising
changes in behavior.

As a result, PyMarkdown remains a reliable tool for checking your Markdown documents,
even as the project continues to evolve.

### Extensible

PyMarkdown lets you turn optional features on and off as needed. Parser extensions
allow you to enable extra Markdown behaviors (such as tables or front matter) while
still staying compatible with the core Markdown specifications.

Rules are also extensible. Each rule is contained with a Rule Plugin that can be
enabled, disabled,
or replaced. The built‑in set includes Python versions of many `MD*` rules from
the npm [markdownlint](https://github.com/DavidAnson/markdownlint) project, which
makes it easier to switch to PyMarkdown if you already use markdownlint today.

## What to Do Next?

If any of these advantages appeal to you, we strongly encourage you to evaluate
the PyMarkdown linter for yourself by continuing to our [Getting Started](./getting-started.md)
page or our [Quick Start guides](./quick-starts/index.md). Both of these options
provide clear, step-by-step instructions on how you can install PyMarkdown on your
system and run it on your own documents. This lets you try it out in a real-world
context, such as your project's README files, contributor guides, or other documentation.
Once you have "[kicked the tires](https://idioms.thefreedictionary.com/kick+the+tires)"
on PyMarkdown, please consider browsing through our [User Guide](./user-guide.md)
to see the benefits provided by our application in more detail, including configuration
options, rule customization, examples, and advanced usage patterns that can help
you tailor PyMarkdown to your specific projects and documentation standards.

If, after trying PyMarkdown on your own documents and workflows, you are left thinking
"it is almost there, but it would be great if it did {something}", please read our
section on [Reporting Issues](./usual.md). We cannot promise that
we will implement every suggestion that you ask for. However, we do promise to carefully
consider each issue you submit, to explain our decision when possible, and to treat
your contribution with the respect it deserves as part of the PyMarkdown community.
