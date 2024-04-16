---
summary: Base information about the PyMarkdown Linter
authors:
  - Jack De Winter
---

# Introduction

## Note To Any Readers

As part of our effort to clean up the project in preparation for a version 1.0.0
release, we are moving our documentation from plain Markdown files hosted on
[GitHub](https://github.com/jackdewinter/pymarkdown) to this new format. Please
bear with us during this transitional period.

## And On with The Show...

PyMarkdown is primarily a Markdown linter. To ensure that the Markdown
[linting](https://en.wikipedia.org/wiki/Lint_%28software%29) is conducted with
the highest attention to detail, our linting rules analyze the tokens produced
by the project's own Markdown parser. The project's Markdown parser aims to be
highly compliant to both the
[GitHub Flavored Markdown](https://github.github.com/gfm/) specification and the
[CommonMark](https://spec.commonmark.org/) specification. This is important as
we estimate that over 90% of the existing parsers are mostly compliant to one of
those two specifications. By our parser adhering to those specifications, we
have a high degree of confidence that the rules we have written are based on
solid information about the structure of the Markdown documents that they are
evaluating. Since the rules have precise information on how compliant parsers
view the structure of a given Markdown document, each rule can make the best
decision possible on whether it should trigger a failure or not.

## Foundational Information

The rest of this document provides information about Markdown, linters, and
reasons to use the PyMarkdown linter for your projects. For any reason,
if you believe you do not need to read this information, please continue to
the section on [What To Do Next](#what-to-do-next).

## What is Markdown?

While [this article](https://www.markdownguide.org/getting-started/) does a
better job at explaining Markdown than we can, we feel confident that we can
provide a summary of what Markdown means to our team. Instead of using complex
editors to author articles and documentation, our team prefers to use the
Markdown language to author our documents. Markdown was designed from the start
to be easily human-readable, adding suggestions to plain text documents that
clarify the organization of each part of the document. It has the bonus that
those suggestions only clarify the document's organization without significantly
detracting from its readability. To illustrate our point, please look at
[this document](https://raw.githubusercontent.com/jackdewinter/pymarkdown/main/newdocs/src/index.md).
That document is the source for this page before any processing needed to get
the document into the form that you are reading now. Except for easily learnable
formatting and annotations, we believe that most people can read a Markdown
document with relative ease.

For our team, there is an added benefit in that it enables us to be more
efficient. When our team writes documentation, we always strive to make each
page of documentation the best it can be. With Markdown, we feel that we can
focus more on the content and organization of the document without concerning
ourselves with the style of the document. To be honest, we know from experience
that if we are concerned with style when authoring a document, we
[rabbit-hole](https://www.merriam-webster.com/dictionary/rabbit%20hole) on the
style to the detriment of the content. Using Markdown, we know we can focus on
our strengths and leave any style decisions for later where we can then apply
those style decisions consistently over the entire document.

## What is a Linter?

As noted above, early software developers established the term
[linting](https://en.wikipedia.org/wiki/Lint_%28software%29) at the dawn of the
age of computers. Stephen C. Johnson needed a tool to spot issues with his code
and filter them out, like a lint trap in a clothes dryer. And while the term may
have weird origins, the name stuck, and the benefits imparted by linters remain
to this day. Each linter is an added process with distinct goals, designed to
check for a specific set of issues in the source code necessary for software
applications.

The best way we have found to explain linters is to explain that their
functionality is analogous to spell checkers and grammar checkers. As a matter
of principle, our team only publishes documentation after running it through
both spell and grammar checkers. This is a parallel to our source code where we
run Python checkers over our source code to ensure that we are adhering to our
own source code guidelines. If we logically extend that one step further to view
documentation as source code, it makes sense that we have a checker that ensures
that our Markdown documents are following similar guidelines. That is where the
PyMarkdown linter fits into the picture for our projects.

## Can It Do Anything Else?

While PyMarkdown is primarily a Markdown linter, the breadth of the application
has grown over the years of its development. In `scan` mode, the linter can
detect Markdown issues using a healthy set of Markdown specific rules. In `fix`
mode, certain Markdown failures can be automatically corrected without external
involvement. While fix mode is a relatively new effort, we believe that it
provides a measurable benefit to our users at a low cost. That is something we
are enormously proud of!

## Why Is This Application Referred to As PyMarkdown and PyMarkdownLnt?

Originally, we thought that PyMarkdown Linter was a good name for the
application. That is until we had to start typing it repeatedly. By that point
we had already registered the package as
[pymarkdownlnt](https://pypi.org/project/pymarkdownlnt/) with the main
[Python Package Index](https://pypi.org/) as there already was another project
named [pymarkdown](https://pypi.org/project/pymarkdown/) that was only released
to once in 2015.

Going forward, we plan to use the PyMarkdown name consistently in any
documentation.

## Why Should You Use PyMarkdown?

The PyMarkdown project has the following advantages:

### Consistency

This project's interface can examine multiple files and directories with a
single invocation, ensuring that all targeted Markdown files adhere to the
provided set of guidelines. This allows users to execute the project from a
[CI/CD](https://en.wikipedia.org/wiki/CI/CD) pipelines to verify the correctness
of documentation within their own repository. For project maintainers looking to
keep projects clean, that is a big advantage.

### Portable

This project runs on any system with Python 3.8 or later, with no modifications.
Before any code changes are merged into the project's `main` branch, every
scenario test is executed against the application. These tests are then repeated
across instances of Linux, Windows, and MacOS machines to detect and fix any
portability issues before the merge is approved. If any problems arise on any
operating system, we address those problems before any users are inconvenienced.

### Standardized

As mentioned above, we strive to keep the project's Markdown parser compliant to
both the [GitHub Flavored Markdown](https://github.github.com/gfm/)
specification and the [CommonMark](https://spec.commonmark.org/) specification.
Utilizing that foundation, the rule engine does not have to guess how a Markdown
parser may handle a given situation. Instead, PyMarkdown's own compliant parser
feeds the rule engine with information on how it handled the document. From
experience, we find that this approach produces more correct results than trying
to use text-based patterns and regular expressions to guess how a Markdown
parser may parse Markdown text.

### Flexible

Before any rules are applied to a Markdown document, that document is first
parsed by the project's Markdown parser into a stream of internal tokens. Each
rule can then decide whether to take advantage of that stream of tokens or to
use a simple line-by-line pattern matching algorithm. That choice is made on a
per-rule basis, using whichever method is the clearest and most efficient for
each rule.

In addition to the internals of the project being flexible, the invocation of
the project to scan Markdown documents is also flexible. The PyMarkdown linter
can be executed from a script on the command line, from within another Python
program, using our simple API, or using the popular Git Pre-Commit hooks.

### Thoroughly Tested

The project currently has over 6750 scenario tests covering 100 percent of the
code. While we encourage our user base to engage us in discussions about the
benefits of scenario testing, code coverage, and other metrics, these metrics
provide our team with the confidence to know we have a solidly tested project.

### Extensible

While the core parts of the Markdown parser are coded within the core of the
project itself, enhancements to that parser are provided using carefully
orchestrated [extensions](./advanced_extensions.md).
These extensions allow for optional behavior to be included by configuration
while keeping the project compliant to the two core specifications. This
flexibility allows the base parser to remain compliant with its specifications
while allowing it to adapt to the needs of the users. If the user does not
require that flexibility offered by the extension, it is simply left disabled.

For the rule engine itself, each of the ever-expanding set of
[rules](./advanced_plugins.md) is
implemented as a plugin. As all rules are implemented as plugins, support for
adding, enabling, and disabling plugins has been present since the start of the
project. The core set of rules are our own implementations of the MD\* rules
provided in the Npm [MarkdownLint](https://github.com/markdownlint/markdownlint)
project.

## What to Do Next?

If any of these advantages appeals to you, we strongly encourage you to evaluate
the PyMarkdown linter out for yourself by continuing to our
[Getting Started](./getting-started.md) page. That page instructs you on how to
install PyMarkdown on your system so you can try it out. Once you have
"[kicked the tires](https://idioms.thefreedictionary.com/kick+the+tires)",
please consider browsing through our [User Guide](./user-guide.md) to see the
benefits provided by our application.

And, if after all that, if you are left thinking "it is almost there, but it
would be great if it did {something}", please read our section on
[Reporting Issues](./usual.md#reporting-issues). We cannot promise that we will
implement every suggestion that you ask for, but we promise to carefully
consider each issue you submit with the respect due to that issue.
