# PyMarkdown

|   |   |
|---|---|
|Project|[![Version](https://img.shields.io/pypi/v/pymarkdownlnt.svg)](https://pypi.org/project/pymarkdownlnt)  [![Python Versions](https://img.shields.io/pypi/pyversions/pymarkdownlnt.svg)](https://pypi.org/project/pymarkdownlnt)  ![platforms](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)  [![License](https://img.shields.io/github/license/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/blob/main/LICENSE.txt)  [![GitHub top language](https://img.shields.io/github/languages/top/jackdewinter/pymarkdown)](https://github.com/jackdewinter/pymarkdown)|
|Quality|[![GitHub Workflow Status (event)](https://img.shields.io/github/actions/workflow/status/jackdewinter/pymarkdown/main.yml?branch=main)](https://github.com/jackdewinter/pymarkdown/actions/workflows/main.yml)  [![Issues](https://img.shields.io/github/issues/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/issues)  [![codecov](https://codecov.io/gh/jackdewinter/pymarkdown/branch/main/graph/badge.svg?token=PD5TKS8NQQ)](https://codecov.io/gh/jackdewinter/pymarkdown)  [![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)  ![snyk](https://img.shields.io/snyk/vulnerabilities/github/jackdewinter/pymarkdown) |
|  |![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/dev/black/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/dev/flake8/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/dev/pylint/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/dev/mypy/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/dev/pyroma/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/dev/pre-commit/main) ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/dev/sourcery/main) |
|Community|[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/jackdewinter/pymarkdown/graphs/commit-activity) [![Stars](https://img.shields.io/github/stars/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/stargazers)  [![Forks](https://img.shields.io/github/forks/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/network/members)  [![Contributors](https://img.shields.io/github/contributors/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/graphs/contributors)  [![Downloads](https://img.shields.io/pypi/dm/pymarkdownlnt.svg)](https://pypistats.org/packages/pymarkdownlnt)|
|Maintainers|[![LinkedIn](https://img.shields.io/badge/-LinkedIn-black.svg?logo=linkedin&colorB=555)](https://www.linkedin.com/in/jackdewinter/)|

## What Is PyMarkdown?

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

## Why Should I Use PyMarkdown?

We go into this in more detail in our [project documentation](https://pymarkdown.readthedocs.io/en/latest/),
but here is the short version.

Do you use spell checkers and grammer checkers for your emails, instant messages,
and documents?

Do you use static code analysis tools to verify that you are committing your best
source code to your projects?

Do you want to be able to customize your guidelines on a per-project basis with
little effort?

If the answer to any of those questions is "Yes", then we encourage you to
consider using our PyMarkdown linter to check you Markdown documents against
a configurable set of rules that you specify.  We start you off with a common
set of rules and configuration settings, but you are able to enable, disable,
and configure rules to correspond to what you want the Markdown guidelines
to be for your project.

## What Advantages Does PyMarkdown Have Over Other Markdown Linters?

The PyMarkdown project has the following advantages:

- [Consistency](https://pymarkdown.readthedocs.io/en/latest/#consistency)
- [Portable](https://pymarkdown.readthedocs.io/en/latest/#portable)
- [Standardized](https://pymarkdown.readthedocs.io/en/latest/#standardized)
- [Flexible](https://pymarkdown.readthedocs.io/en/latest/#flexible)
- [Thoroughly tested](https://pymarkdown.readthedocs.io/en/latest/#thoroughly-tested)
- [Extensible](https://pymarkdown.readthedocs.io/en/latest/#extensible)

## What Are The Minimum Requirements?

This project required Python 3.10 or later to function.

## What Linting Checks Does PyMarkdown Release With?

The PyMarkdown project is released with 46 out-of-the-box rules to check your
Markdown with.  Roughly 44 of those rules are our version of the rules provided
by the [Markdown Lint](https://github.com/DavidAnson/markdownlint) project.
We purposefully made the decision to implement those rules as they are somewhat
of a standard due to Markdown Lint being a plugin for VSCode.

The reason that we state "our version of the rules" is because we believe that
some of the rules are either overly complicated or were not catching all use
cases properly.  Our philosophy is that each Plugin Rule should perform one
check and one check only... no side-effect checks.  We also believe that some
of the Markdown Lint rules do not understand the context of the document properly,
leading to misses for their rules.  Our architecture was created to ensure that
we always have access to the context of any Markdown element that was scanned.

Basically, we want to support the worldwide users of Markdown by enabling
PyMarkdown to have the best rules possible.  And to do this on the behalf of
our users, we feel that we need to make our own decisions on what a rule is.

## How Do I Run This Tool?

The PyMarkdown application is primarily a command line tool for linting, so
many features boil down to expressing them in the form of commands.

However, we also expose the following other ways to execute the PyMarkdown application:

- easy-to-use built-in hooks for [Pre-Commit](https://pymarkdown.readthedocs.io/en/latest/getting-started/#installing-via-pre-commit)
- a simple [API layer](https://pymarkdown.readthedocs.io/en/latest/api/)

For more information on the Pymarkdown application and its command lines,
please [look here](https://pymarkdown.readthedocs.io/en/latest/).

## What If It Is Missing A Feature That I Am Looking For?

Our project team is very open to discussing any features that you would like to
see in this project.  The two most frequent requests we get are to extend our Markdown
parser to include a new extension or to extend our our Rule Engine to support
a new rule or a variation of an existing rule.

Extending our Markdown parser to accomodate widely supported Markdown elements
is one of the goals of our project.  However, implementing an extension takes time,
especially when it comes to testing the extension.  When we start working on an
extension, we usually forecast a 1-3 month window for the extension, with subreleases
along the way for people to try out.

Extending our Rule Engine to support new rules is built in to the foundation of
the Rule Engine itself with our Rule Plugins.  Most of the time, we are able to
work on those in parallel
with other work and other testing, so that helps out as well.  But they still take
time.  With the addition of our new [Fix Mode](https://pymarkdown.readthedocs.io/en/latest/user-guide/#fix-mode-failure-correction),
adding the ability to automatically fix any issues takes even longer to complete
properly.

Neither of the last two paragraphs should be considered negative in the least.
We are just trying to explain that new features take time and why they take
time.  The good news is that we are in the process of documenting the Rule Plugin
creation
process to the point where other people can work on them and submit them for consideration.
Look out for that in the near future!

## Where Can I Find More Detailed Information About PyMarkdown?

Our documentation is hosted at [ReadTheDocs](https://pymarkdown.readthedocs.io/en/latest/)
and is kept up-to-date.
