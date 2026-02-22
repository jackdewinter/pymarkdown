---
summary: Base information about the PyMarkdown Linter
authors:
  - Jack De Winter
---

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
as you become more comfortable with PyMarkdown and ant to go beyond the basics.

## Core PyMarkdown Concepts

PyMarkdown is primarily a Markdown linter. To ensure that the Markdown
[linting](https://en.wikipedia.org/wiki/Lint_%28software%29) is conducted with the
highest attention to detail, our linting rules analyze the tokens produced by the
project's own Markdown parser. The project's Markdown parser aims to be highly compliant
with both the [GitHub Flavored Markdown](https://github.github.com/gfm/) specification
and the [CommonMark](https://spec.commonmark.org/) specification. This is important
because we estimate that over 90% of existing Markdown parsers are mostly compliant
with one of those two specifications. Because our parser adheres to those specifications,
we have a high degree of confidence that the rules we have written are based on
accurate information about the structure of the Markdown documents that they are
evaluating. Since the rules have precise information on how compliant parsers view
the structure of a given Markdown document, each rule can make the best decision
possible on whether it should trigger a failure. That decision is based on how that
failure relates to how other compliant parsers will interpret the same document
and how your Markdown will render in popular tools and platforms.

## Background and Foundational Information

The rest of this document provides background information about Markdown, linters,
and reasons to use the PyMarkdown linter for your projects. If you already understand
these topics, continue on to the section on [What to Do Next](#what-to-do-next).

## What is Markdown?

While [this introductory article](https://www.markdownguide.org/getting-started/)
does a better job of explaining Markdown than we can, we feel confident that we
can provide a summary of what Markdown means to our team in practice. Instead of
using complex editors to author articles and documentation, our team prefers to
use the Markdown language to write our documents. Markdown was designed from the
start to be easily human-readable, adding only simple markers to plain-text documents
that clarify the structure of each part of the document. These markers clarify the
document's organization without significantly detracting from its readability. To
illustrate our point, please look at the raw Markdown source for
[this page](https://raw.githubusercontent.com/jackdewinter/pymarkdown/main/newdocs/src/index.md).
That file is the unprocessed source for this page, before any processing is applied
to convert it into the form that you are reading now. Except for a few easily learnable
formatting markers and annotations, we believe that most people can read a Markdown
document with relative ease. This makes it easier to compare the raw Markdown to
the rendered page that they are currently viewing.

For our team, there is an added benefit in that using Markdown enables us to be
more efficient. When our team writes documentation, we always strive to make each
page of documentation the best it can be. With Markdown, we feel that we can focus
more on the content and organization of the document without concerning ourselves
with the style of the document. From experience, we know that if we focus on style
when authoring a document, we [rabbit-hole](https://www.merriam-webster.com/dictionary/rabbit%20hole)
on the style to the detriment of the content. Using Markdown, we know we can focus
on our strengths as writers and leave any style decisions for later, where we can
then apply those decisions consistently across the entire document.

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
to have a checker for it as well. That checker should ensure that our Markdown documents
follow guidelines for quality and consistency similar to the ones we use for our
source code. That is where the PyMarkdown linter fits into the picture for our projects.

## Can It Do Anything Else?

While PyMarkdown is primarily a Markdown linter, the breadth of the application
has grown over the years of its development. In `scan` mode, the linter can
detect Markdown issues using a robust set of Markdown-specific rules. In `fix`
mode, certain Markdown issues can be automatically corrected without external
involvement or manual editing. While fix mode is a relatively new part of the project,
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
Utilizing that foundation, the rule engine does not have to guess how a Markdown
parser may handle a given situation. Instead, PyMarkdown's own compliant parser
feeds the rule engine with information on how it handled the document. From
experience, we find that this approach produces more accurate results than trying
to use text-based patterns and regular expressions to guess how a Markdown
parser may parse Markdown text.

### Flexible

Before any rules are applied to a Markdown document, the document is first parsed
by the project's Markdown parser into a stream of internal tokens (small, structured
pieces of the document, such as headings, paragraphs, or links) that represent the
structure and content of the document. Each rule can then decide whether to take
advantage of that stream of tokens or to use a simple line-by-line pattern matching
algorithm. That choice is made on a per-rule basis, using whichever method is the
clearest and most efficient for each rule.

In addition to the internals of the project being flexible, the ways you can invoke
the project to scan Markdown documents are also flexible. The PyMarkdown linter
can be executed from a script on the command line, from within another Python program
using our simple API to integrate PyMarkdown into your own tooling, or using the
popular Git Pre-Commit hooks.

### Thoroughly Tested

The project currently has over 8000 scenario tests (tests that run PyMarkdown against
realistic Markdown documents), covering 100 percent of the code base. We encourage
our user base to discuss the benefits of scenario testing, code coverage (how much
of the code is exercised by tests), and other metrics (quantitative measures of
code and test quality). Together, these metrics provide our team with the confidence
to know we have a solidly tested project that behaves predictably when analyzing
Markdown documents, even as the codebase evolves. As a result, you can rely on consistent
behavior over time and across different nvironments.

### Extensible

While the core parts of the Markdown parser are coded within the core of the project
itself, enhancements to that parser are provided using carefully orchestrated [extensions](./advanced_extensions.md)
(optional add-ons that change or extend how the parser behaves). These extensions
allow optional behavior to be included by configuration while keeping the project
compliant with the two core specifications. This flexibility allows the base parser
to remain compliant with its specifications while still adapting to the needs of
its users by enabling additional, opt-in behavior. If a user does not require the
flexibility offered by an extension, that extension is simply left disabled. In
that case, the parser continues to follow the default specification-compliant behavior
that matches GitHub Flavored Markdown and CommonMark, which is what most users encounter
on popular platforms such as GitHub and many documentation sites.

For the rule engine (the part of PyMarkdown that runs all the linting rules) itself,
each rule in the ever-expanding set of [rules](./advanced_plugins.md) is implemented
as a plugin (a small, self-contained component that adds a specific rule). Because
all rules are implemented as plugins, support for adding, enabling, and disabling
plugins has been present since the start of the project. The core set of rules are
our own implementations of the `MD*` rules provided in the npm [markdownlint](https://github.com/DavidAnson/markdownlint)
project. As a result, users familiar with "markdownlint" will recognize many of
the rule names and behaviors. This makes it easier to transition between existing
Markdown linting setups and PyMarkdown, especially if you are already using the
Node-based markdownlint in your projects and want to move to a Python-based tool.

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
section on [Reporting Issues](./usual.md#reporting-issues). We cannot promise that
we will implement every suggestion that you ask for. However, we do promise to carefully
consider each issue you submit, to explain our decision when possible, and to treat
your contribution with the respect it deserves as part of the PyMarkdown community.
