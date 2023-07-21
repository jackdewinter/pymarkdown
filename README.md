# PyMarkdown

|   |   |
|---|---|
|Project|[![Version](https://img.shields.io/pypi/v/pymarkdownlnt.svg)](https://pypi.org/project/pymarkdownlnt)  [![Python Versions](https://img.shields.io/pypi/pyversions/pymarkdownlnt.svg)](https://pypi.org/project/pymarkdownlnt)  ![platforms](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)  [![License](https://img.shields.io/github/license/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/blob/main/LICENSE.txt)  [![GitHub top language](https://img.shields.io/github/languages/top/jackdewinter/pymarkdown)](https://github.com/jackdewinter/pymarkdown)|
|Quality|[![GitHub Workflow Status (event)](https://img.shields.io/github/actions/workflow/status/jackdewinter/pymarkdown/main.yml?branch=main)](https://github.com/jackdewinter/pymarkdown/actions/workflows/main.yml)  [![Issues](https://img.shields.io/github/issues/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/issues)  [![codecov](https://codecov.io/gh/jackdewinter/pymarkdown/branch/main/graph/badge.svg?token=PD5TKS8NQQ)](https://codecov.io/gh/jackdewinter/pymarkdown)  [![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)  ![snyk](https://img.shields.io/snyk/vulnerabilities/github/jackdewinter/pymarkdown) |
|  |![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/black/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/flake8/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/pylint/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/mypy/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/pyroma/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/pre-commit/main) | ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/pymarkdown/sourcery/main) |
|Community|[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/jackdewinter/pymarkdown/graphs/commit-activity) [![Stars](https://img.shields.io/github/stars/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/stargazers)  [![Forks](https://img.shields.io/github/forks/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/network/members)  [![Contributors](https://img.shields.io/github/contributors/jackdewinter/pymarkdown.svg)](https://github.com/jackdewinter/pymarkdown/graphs/contributors)  [![Downloads](https://img.shields.io/pypi/dm/project_summarizer.svg)](https://pypistats.org/packages/project_summarizer)|
|Maintainers|[![LinkedIn](https://img.shields.io/badge/-LinkedIn-black.svg?logo=linkedin&colorB=555)](https://www.linkedin.com/in/jackdewinter/)|

PyMarkdown is primarily a Markdown Linter.  To ensure that the Markdown
[linting](https://en.wikipedia.org/wiki/Lint_%28software%29)
is accomplished successfully, the rules engine that powers the linter
uses a Markdown parser that is both
[GitHub Flavored Markdown](https://github.github.com/gfm/)
compliant and
[CommonMark](https://spec.commonmark.org/)
compliant.  The rules provided in the base application can be easily extended
by writing new plugins and importing them into the rules engine through simple
configuration options.

The PyMarkdown project has the following advantages:

- Consistency
  - This project can examine multiple files and directories with one invocation,
    ensuring that all detected Markdown files adhere to the same guidelines.
- Portable
  - The linter runs on any system running Python 3.8 or later, with no modifications.
- Standardized
  - The parser that powers the linter is GitHub Flavored Markdown (GFM) compliant.
    Due to that foundation, the parser does not guess how some parsers may handle
    a given situation, as it has a clear set of rules to follow.
- Accurate
  - The parser passes all GFM conformance tests and CommonMark conformance tests.  In
    test scenarios that were not present in either set of tests, the CommonMark
    0.29.2 release was used to determine the correct parsing.
- Flexible
  - Each Markdown document is parsed into an internal token format.  Most of the rules
    and made more efficient by leveraging this token format. Where that is not possible,
    simple regular expressions and simple algorithms are used on a line-by-line basis.
- Thoroughly tested
  - The project currently has over 4100 scenario tests and a coverage percentage of 100%.
- Extensible
  - The parser for the project adheres to the GFM specification and most of
    the rules for the parser leverage the tokens produced by that parser. The
    [rules](/docs/rules.md) themselves are plugins, so they are extensible by default.
    The parser itself will be extended as needed to provide for other Markdown
    [extensions](/docs/extensions.md) as needed.
- Versatile
  - The PyMarkdown linter can be executed from a script on the command line,
    from within another Python program, or using the popular Git Pre-Commit hooks.

## Note

This project is currently in beta, and some of these documented things
may not work 100% as advertised until after the final release.  However,
everything should be close enough to done that if you find something missing,
please let us know.

## GitHub Pre Commit Hooks

If you intend to use the PyMarkdown project as a linter for your
GitHub Pre-Commit hooks, then refer to [this document](/docs/pre-commit.md)
on how to set that up.  Once setup, you can continue reading at the
[How To Use section](#how-to-use) for more information on the options
available for use in your Pre-Commit Hooks.

## Requirements

This project required Python 3.8 or later to function.

## Installation

```text
pip install pymarkdownlnt
```

## How To Use

### If You Get Stuck

Full help support is available by entering

```shell
pymarkdown --help
```

on the command line and pressing enter.  For an individual command,
help is available by following the command or commands with `--help`
as follows:

```shell
pymarkdown scan --help
```

### Prerequisites

Various sections of this document benefit from having concrete examples
to illustrate how things work. For the following sections,
this documentation will assume that there is a file called `example-1.md`
in a directory called `examples` that has the following content:

```Markdown
## This is an example

Just an example.
```

and a file called `example-2.md` in that same directory that has the
following content:

```Markdown
# This is an example

Just an example.

```

If you prefer concrete files, these files are checked into the
[examples directory](https://github.com/jackdewinter/pymarkdown/tree/main/examples) of the GitHub project.

### API Support

While the vast majority of people using this application will use it
through the command line, there is an auto-generated [API document](./docs/api.md)
and [another document](./docs/api-usage.md) on how to use the API.  This support
is very new, but introduced with lots of testing. If there are usability issues
or something you feel is missing, please contact us.

### Basic Scanning

The PyMarkdown linter is executed by calling the project from the
command line and
specifying one or more files and directories to scan for Markdown `.md`
files.  The set of files and/or directories must be prefaced with the
`scan` keyword to denote that scanning is required. For the examples
directory, both this form:

```shell
pymarkdown scan examples
```

and this form:

```shell
pymarkdown scan examples/example-1.md examples/example-2.md
```

can be used to scan both files in the directory.  The only difference
between the two invocations is that the first example will scan every
Markdown `.md` file in the `examples` directory, while the second
invocation will only scan the two specified files.  For clarity purposes,
if the command line specifies the same file multiple times, that file
name will only be added to the list of files to scan once.

If everything is working properly, both of the above scans will
produce the following output:

```text
examples/example-1.md:3:16: MD047: Each file should end with a single newline character. (single-trailing-newline)
```

### Rules

The PyMarkdown project includes 13 out-of-the-box [rules](/docs/rules.md),
with another 29 rules to be added before the
1.0.0 release.  These rules are implemented using a simple plugin
system that is documented in the [developer documentation](/docs/developer.md).
It is these rules that allow the PyMarkdown project to scan
the various Markdown files, looking for bad patterns over that set of
Markdown documents.

Because of the way that the rules are provided, sometimes we
refer to the rules as `rules` and sometimes as `rule plugins`.  A `rule`
is a specific set of conditions that trigger the reporting of a violation
when those conditions occur.  A `rule plugin` is the Python class
and Python file in which the `rule` is supplied to the PyMarkdown application.
Our goal is to try to not use these phrases interchangeably, but we are only
human.  If we do mess up and use the wrong phase, we do apologize.

Note that the initial set of rules are modelled after the 42 rules provided by
David Anson's [Markdown Lint](https://github.com/markdownlint/markdownlint)
project.  This decision was made
to give Markdown authors that use his project in their IDEs (such as
the MarkdownLint plugin for VSCode that I use), a good grounding
in what they can consistently check for.

### Rule Violation Format

Executing either of the above example command lines will produce the following output:

```text
/examples/example-1.md:3:16: MD047: Each file should end with a single newline character. (single-trailing-newline)
```

The format of the output for any rules that are triggered is as follows:

`file-name:line:column: rule-id: description (aliases)`

- `file-name` - Path to the file that triggered the rule.
- `line`/`column` - Position in the file where the rule was triggered.
- `rule-id` - Unique identifier assigned to the rule.
- `description` - Human readable description of the rule.
- `aliases` - One or more aliases used to reference the rule.

For the rule violation that was reported at the start of this section,
the first step in diagnosing
that violation is to look at the file `/examples/example-1.md` at the end of
line 3, which is column 16.  Rule [md047](/docs/rules/rule_md047.md) specifies
that every file should end with a single newline character, which is
what is reported in the violation's description.  Additionally, it reports that this
rule can also be identified by the more human readable alias of
`single-trailing-newline`.

### Basic Configuration

The most frequently used part of the configuration system is the
part that enables and disables specific rules while scanning the
Markdown files.  For example, if you do not like rule md047 which
states that each file must end with a single newline, you can
disable that rule by specifying:

```shell
pymarkdown -d md047 scan /examples
```

or:

```shell
pymarkdown --disable-rules md047 scan /examples
```

The effect of disabling the rule should be evidenced by
the scan no longer reporting any violations of rule md047
against the Markdown file `example-1.md`.

Alternatively, rules can also be enabled.  As the modelled
base rules for this project are based off those rules for David
Anson's project, rule md002 is disable by default in both
projects.  Specifically, rule md002 is disabled by default
as rule md041 provides a better implementation of that rule
that takes front-matter into account.  Until that rule is
implemented, you can enable rule md002 by specifying either:

```shell
pymarkdown -e md002 scan /examples
```

or

```shell
pymarkdown --enable-rules md002 scan /examples
```

The effect of enabling the rule is evidenced by
the scan reporting a violation of Rule md002 against
Markdown file `example-1.md`:

```text
examples/example-1.md:1:1: MD002: First heading of the document should be a top level heading.
 [Expected: h1; Actual: h2] (first-heading-h1, first-header-h1)
examples/example-1.md:3:16: MD047: Each file should end with a single newline character.
(single-trailing-newline)
```

### Extensions

Extensions are any features that are implemented in addition to the base
[GitHub Flavored Markdown](https://github.github.com/gfm/) specification.
These extensions are documented in the [extensions](/docs/extensions.md)
document, including information about how they perform, details on the
extension, and configuration information.

### Advanced Scanning

For more advanced scanning options, please consult the document
on [Advanced Scanning](/docs/advanced_scanning.md).

### Advanced Configuration

For more advanced configuration options, please consult the document
on [Advanced Configuration](/docs/advanced_configuration.md).  This
document includes information on:

- [Command Line Settings](/docs/advanced_configuration.md#command-line-settings)
- [Configuration File Settings](/docs/advanced_configuration.md#configuration-file-settings)
- [Available Configuration Values](/docs/advanced_configuration.md#available-configuration-values)

### Advanced Rule Plugins

For more information of how to query information on the rule plugins
that are currently loaded, please consult the document on
[Advanced Rule Plugins](/docs/advanced_plugins.md).

## Open Issues and Future Plans

During the development phase of this project, it was more useful to have
an actual list of issues to track and prioritize, rather than relying on
GitHub to do all the work. This is the location of the prioritized
[Issues List](/issues.md).

If you find any issues, please report them using the standard GitHub
issues process.  When our team looks at your issue and triages
it, it will be added to our Issues List with the triaged priority.
For us, this provides transparency as to what we are currently working
on, what is up next, and what our plans are for further development.

## When Did Things Change?

The changelog for this project is maintained [at this location](/changelog.md).

## Still Have Questions?

If you still have questions, please consult our
[Frequently Asked Questions](/docs/faq.md) document.

## Contact Information

If you would like to report an issue with the linter, a rule, or
the documentation, please file an issue [using GitHub](https://github.com/jackdewinter/pymarkdown/issues).

If you would like to us to implement a feature that you believe is
important, please file an issue
[using GitHub](https://github.com/jackdewinter/pymarkdown/issues)
that includes what you want to add, why you want to add it,
and why it is important.  Please note that the issue will usually be
the start of a conversation, and be ready for more questions.

If you would like to contribute to the project in a more
substantial manner, please contact me at `jack.de.winter` at `outlook.com`.

## Instructions For Contributing

Developer notes on various topics are kept in the the
[Developer Notes](/docs/developer.md) document.

If you attempting to contribute something to this project,
please follow the steps outlined in the
[CONTRIBUTING.md](/CONTRIBUTING.md)
file.

## Acknowledgements

Currently, as a team of one, there are only two big groups of people to
acknowledge.

The first, and foremost group, is my immediate family. They
have endured me coming out of my office with my head still in the
clouds, explaining things to them so that I can think more clearly.
While they still do not understand what I am talking about with respect
to this project, I am so grateful to them for allowing me to work "my
process" to figure things out.

The second group is the contributors to the
[CommonMark discussion forum](https://talk.commonmark.org/).
While I have raised some issues that were cut and dry, a lot of them
involved significant amount of discussion to figure out what the
right approach is.  Through all those discussions, I rarely, if ever,
felt like they treated me as less than equal, no matter how stupid
my questions were.  For their patience and their professionalism,
thank you.
