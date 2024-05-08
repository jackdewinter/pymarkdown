---
summary: Guide for users on how to use PyMarkdown.
authors:
  - Jack De Winter
---

# Introduction

The purpose of this User Guide is to help you find information about how to use
the PyMarkdown linter application.  These pages assume you have at least scanned
the
content in the [Introduction](./index.md) document and the [Getting Started](./getting-started.md)
document, gaining a basic understanding of the application in the process. That is
important as this document builds on that foundation to provide you with targeted
information
on a variety of subjects.

If, after reading the documentation and trying something out for yourself, you find
that there is a problem, a lack of documentation, or a feature that you believe
is missing, please consider using the process outlined on our [Reporting Issues](./usual.md#reporting-issues)
page.  We take each submitted issue seriously, hoping to grow our project with
your support.

## Nomenclature

Here are some words and phrases that we use throughout our documentation.

### Markdown Document / Markdown File

A normal text document that includes Markdown annotations.  These documents are
typically stored as Markdown files with a `.md` filename extension.

### Markdown Parser

A main application component that takes a Markdown document and breaks it
down into its
constituent elements.  The Markdown parser emits a stream of Markdown tokens
that can then be used for specific purposes.

### Rule Engine

A main application component that takes a stream of Markdown tokens and executes
a series of actions that are based upon those tokens.  As each of these
actions are rules (see below), the component that controls the
orchestration of those rules is referred to as the Rule Engine
component.

### Rules / Plugin Rules

Python code that extends the Rule Engine (via a plugin mechanism) to
look for a specific behavior on behalf of the user.  Examples of this are
Rule Md010 which looks for hard tabs in the document and Rule Md012 which
looks for consecutive blank lines in the document.

### Rule Ids

Rule ids are a unique identifier that is associated with a given rule.
These rule ids are case-insensitive.  Therefore, the ids `md010`, `MD010`,
and `Md010` all refer to the same rule.  For historical reasons, these
identifiers start with a two or three letter prefix, followed by a
three-numeral suffix.

### Parser Extensions

Python code that directly interacts with the Markdown Parser component to provide
a single enhanced Markdown capability.  Examples of
this are the support for Markdown document front matter, task list items,
and pragmas.

### Triggered

When a rule finds an instance of the specific behavior that it is looking for,
that rule then triggers a failure.  There is no general behavior about the
number of times a rule can be triggered within a single document.

### Failure

When a rule is triggered, the information that the rule produces to provide
specifics about why it was triggered is called a failure. Failures are distinct
from errors in that detecting failures is an expected outcome of executing the
application.

It is worthwhile to note that while these are labelled as "failures", that is
only a general description of that information.  The term failure is used to
denote that a rule found something that does not adhere to the user's specified
guidelines expressed through the rule itself.

### Error

While we try to plan out and test everything, occasionally errors get through.
Errors show that either Python or our own guard code has detected an invalid
condition within our application, one of its extensions, or one of its plugins.

### Scanning and Scan Mode

A single pass of the PyMarkdown application over one or more files using the `scan`
command.
That pass is performed in Scan Mode, with the target of finding any failures
within a Markdown document that was scanned.

### Failure Correction or Fix Mode

Like scan mode above but using the `fix` command.  The Rule Engine asks any rules
that support the automatic
fixing failures to do so.  Note that not all rules support this feature,
for reasons discussed in the section on [Fix Mode](#fix-mode-failure-correction).

## Prerequisites

Since PyMarkdown is a Markdown linter, this documentation assumes that the
user has a working knowledge of Markdown and the annotations used for each element.
If in doubt, the [Markdown Guide](https://www.markdownguide.org/) is a good reference
document, with information on each type of Markdown element and how to use them.
As
the rest of the documentation assumes that you have knowledge of Markdown, it is
strongly
recommended that you at least review the cheat sheet from the Markdown Guide before
continuing.

Note that Parser extensions are exempt from that rule.  Extensions introduce
new or altered behavior into the Markdown Parser. As such, a lack of clarity is introduced
about how each extension interacts with standard Markdown elements. We have tried
to resolve this lack of clarity by having each extension
provide solid documentation on that extension, coupled with examples or links to
examples of
the extension being used.
More information about this can be found in the [Advanced Extensions](./advanced_extensions.md)
document.

In addition, as we were writing the documentation, we found that various sections
of this documentation would benefit from common, concrete examples.  This was also
done to minimize the count of Markdown
examples needed throughout the documentation.  Our hope is that this decision helps
declutter the documentation and make it easier to process for you.

For the rest of the documentation, where possible we refer to a set of example files
stored in a directory
structure of:

```text
base directory
|--- examples
     |--- example1.md
     |--- example2.md
|--- README.md
```

The `README.md` file is present for reference and can be any kind of Markdown
file you would use for your projects.  For the sake of these examples, we
assume that the `README.md` file always scans cleanly.  Within the `examples`
directory are two files: `example-1.md` and `example-2.md`.  The file `example-1.md`
has the content:

```Markdown
## This is an example

Just an example.

```

and the file `example-2.md` has the content:

```Markdown
# This is an example

Just an example.

```

If you prefer concrete files as opposed to code blocks, these files are checked
into the
[examples directory](https://github.com/jackdewinter/pymarkdown/tree/main/examples)
of the GitHub project. When scanned, the file `example-1.md` triggers the `Md041`
rule on line
1 of that document.  When file `example-2.md` is scanned, it does not trigger any
rules.

## Command Line Basics

If you are stuck on what to do when using the command line, it is always beneficial
to enter the following command line:

```txt
pymarkdown --help
```

The resultant text will give you a good understanding of what commands and arguments
are available at the base level.  Note that only arguments that apply to
all commands are listed in this text, followed by the list of current commands.
At present, there are six commands available, returned in alphabetical order:

- `extensions` - Request information on current extensions.
- `fix` - Fix any Markdown files (where possible) in the specified paths.
- `plugins` - Request information on current plugin rules.
- `scan` - Scan any Markdown files in the specified paths.
- `scan-stdin` - Scan the application's standard input as a Markdown file.
- `version` - Return the version of the application.

Three of these commands (`extensions`, `plugins`, and `version`) are inspection
commands,
used to request more information about [installed extensions](#extension-command),
[installed rules](#plugin-command), or to inquire about the [version](#version-command)
of the application.

The remaining commands are action commands.
The `scan` command instructs PyMarkdown to scan any specified files for failures.
The `scan-stdin`
command is a variant of the `scan` command that scans the application's standard
input
for failures instead of being file-based.  The `fix` command is like the `scan`
command, but it instructs
PyMarkdown's rule engine to try to fix any failures.

To figure out the correct arguments to pass to a command, use the following command
line:

```txt
pymarkdown {command} --help
```

with the text `{command}` being replaced with the command you need help with.

That command line is more focused with its help in that it will present you
with helpful information on arguments that change the specific command that you
are
trying to use.  Whether exploring
with the command line or trying to get something specific done, it is a simple,
useful
tool that should not be ignored.

In addition to the commands and their arguments, there are arguments that precede
the commands and apply to all the commands.  These arguments are covered
in the section below on [Basic Configuration](#basic-configuration).

### Basic Scanning

The PyMarkdown linter is executed by calling the project from the command line,
specifying one or more files and directories to scan for Markdown `.md`
files. The list of files and/or directories presented on the command line must
be prefaced with the `scan`
keyword to denote that scanning is needed.

#### Sample Command Lines

The command line for scanning files is very straightforward.  Assuming that
you are in the root directory of the directory structure specified in the
[Prerequisites](#prerequisites) section, two simple command lines are:

```txt
pymarkdown scan examples
```

and:

```txt
pymarkdown scan examples/example-1.md examples/example-2.md
```

The first example will scan every Markdown `.md` file in the `examples` directory,
while the second invocation will only scan the two specified files.  To ensure
that the output is always consistent, if different path arguments specify the same
filename,
that filename will only be added once to the list of files to scan.  In addition,
to ensure that the scanning is done in a predictable order, that list of files to
scan is also sorted into alphabetical order.

After executing either of those command lines from the root directory, the
output to expect from PyMarkdown is:

```text
examples\example-1.md:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
```

#### Rule Failure Format

Our team decided to adopt a failure format
like that of other linters, checkers, and compilers. At their root,
all those tools use the first four fields to show the file scanned, the location
within the file where the failure occurred (line number and column number), and
a unique code for the reported failure is.  From there, the tools all
diverge into their own formats, each format providing the detailed information
relevant to its own tool.

Keeping to that format, the output format for any PyMarkdown failure is as follows:

`file-name:line:column: rule-id: description (aliases)`

Breaking it down into its constituent parts:

- `file-name` - Path to the file that triggered the rule.
- `line`/`column` - Position in the file where the rule was triggered.
- `rule-id` - Unique identifier assigned to the rule.
- `description` - Human readable description of the rule.
- `aliases` - One or more aliases used to reference the rule.

Using the output from the command line `pymarkdown scan examples`, that output
reports one failure that occurred in the file `examples\example-1.md` on line
1 at column 1. The id of the rule that triggered is `MD041`, otherwise known
by the human readable aliases of `first-line-heading` and `first-line-h1`. To
present even more readable text to the reader, the text associated with this
rule's failures is:

> First line in file should be a top level heading

Looking back at the text for `example-1.md`, the first line of that file
is:

```Markdown
## This is an example
```

which shows an ATX Heading with a level of 2.  A simple reading of the
failure text indicates that rule `MD041` is okay with the first line being
a heading, but it wants that heading to be a level 1 or top-level heading.
Looking at the text from `example-2.md`, the first line is:

```Markdown
# This is an example
```

As the `example-2.md` file is not mentioned in the output, it makes sense
that PyMarkdown's rule MD041 did not have any issue with a level 1 ATX Heading,
largely confirming the above assumption.
If desired, we can take the extra step to verify this by looking at the documentation
page for [Rule MD041](https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md041.md#Correctness)
which states:

> In most cases, the top-level heading of a document is used as the title of that
> document. Therefore, the first heading in the document should be a level 1 header
> to reflect that reality.

### Advanced Scanning

While our team believes that the difference between the basic scanning usage of
PyMarkdown and the advanced
scanning usage of PyMarkdown is not large, solid understanding of basic scanning
principles should be learned before going ahead with these concepts.

#### Command Line Arguments

As far as the command line interface for scanning goes, we have tried to make
the advanced options easy to understand.

```txt
usage: pymarkdown scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]

positional arguments:
  path                  one or more paths to examine for eligible Markdown files

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-files      list any eligible Markdown files found on the specified paths and exit
  -r, --recurse         recursively traverse any found directories for matching files
  -ae ALTERNATE_EXTENSIONS, --alternate-extensions ALTERNATE_EXTENSIONS
                        provide an alternate set of file extensions to match against
```

##### --list-files or -l

The `-l` or `--list-files` argument instructs PyMarkdown to only list the files
it
would scan if this argument was not present, and then exit the application.  This
is useful when using more complicated
`path` arguments, ensuring that the list of filenames believed to be specified by
the argument and the expected
list of filenames to scan match each other.

##### --recurse or -r

The `-r` or `--recurse` argument instructs PyMarkdown to recurse into any directories
that it finds after evaluating each path argument.  For example, if the arguments
`scan --recurse .` are provided, then this argument will recursively search for
any
Markdown file in the current directory (path of `.`) or any directory below that
directory.
There is no requirement that a directory have at least one Markdown file before
the search recurses into that directory.

##### --alternate-extensions or -ae

The `-ae` or `--alternate-extensions` argument instructs PyMarkdown to use an alternate
filename extension when looking for Markdown files.  By default, PyMarkdown only
processes files that have an `.md` extension.  This argument allows for that
set of filename extensions to be replaced with a comma-separated list
of filename extensions.  Note that each filename extension must start with a `.`
character,
followed by one or more alphanumeric characters.

##### path

The scan command is constructed to allow one or more path arguments.  If the path
contains a `?` character or a `*` character,
the Python [glob library](https://docs.python.org/3/library/glob.html) is used to
evaluate the argument.  
If the path does not contain a `?` or a `*` character,
then the argument is evaluated as the literal name of a file to scan.
Since recursion is already supported by the
[`--recurse`](#-recurse-or-r) argument, the `recursive` flag to the `glob.glob`
function is not enabled.  

Examples of simple Glob styled matches are:

- `./**` - Match any filenames is this directory or any directory directly below
    this directory.
- `*.md` - Match all filenames ending with `.md` in the current directory. Note
    that this is redundant as PyMarkdown's default is to only process filenames
    ending with `.md`.

Note that unless the `--alternate-extensions` argument is used to change the
allowed
filename extension, only filenames ending with a `.md` extension will be processed.
This was done to allow easy scanning of directories using paths of `.` and `examples`,
instead of having to specify a path of `./*.md`.

#### Scanning From Standard Input

From time to time, it may be necessary to take the output from an application
that generates Markdown and pass it directly into PyMarkdown as standard input.
In that situation, the `scan-stdin` command can be used to accept that input
and scan it as a normal Markdown document.  Note that this command is not like
the
standard `scan` command in that it has no arguments.  This is because all the
arguments
for the `scan` command are used to control the files to scan or to display
information on the files it would have scanned.  With all its data coming
from standard input, the `scan-stdin` command requires no additional arguments.

Note that as a simple workaround, you may decide to pipe that standard input
into a file and then use PyMarkdown to scan that file.  However, we felt
that was inefficient and [kludgy](https://en.wikipedia.org/wiki/Kludge), so this
feature was added.

#### Extensions

Extensions are either features that are implemented in addition to the base
[GitHub Flavored Markdown](https://github.github.com/gfm/) specification or
features specified in the GitHub Flavored Markdown specification as extensions.
These features specifically alter how the Markdown parser breaks the Markdown
document down into its constituent elements.
These extensions are fully documented in the
[Advanced Extensions](./advanced_extensions.md)
document, including information about how they perform, details on the
extension, and configuration information.

##### Pragma Extension

The [Pragma](https://github.com/jackdewinter/pymarkdown/blob/main/docs/extensions/pragmas.md)
extension (id of `linter-pragmas`, enabled by default) allows for the introduction
of special instructions into the Markdown
document.  These instructions can then be used by PyMarkdown to ask for special
treatment
of the document on a scale that is smaller than the entire document.  This feature
is
analogous to the `suppress` or `ignore` features of other linters and checkers.

For example, consider
the following Markdown snippet:

```Markdown
<!--- pyml disable-next-line no-multiple-space-atx-->
#  My Bad Atx Heading
```

The `disable-next-line` Pragma command is useful in that it instructs PyMarkdown's
parser to tell the rule
engine to suppress any failure of the rule `no-multiple-space-atx` on the next
line of the document.
This command is useful in cases where a user
wants to keep a specific rule enabled for the entire document but has a focused
justification for breaking that
rule in a targeted situation. The `disable-num-lines` Pragma command takes this
a step further by telling the
rule engine to ignore the failures for a specific number of lines.

We urge our users to use this feature sparingly but leave it up to their judgement
on how to deal with failures, whether using high-level configuration (see the following
section
on [Plugin Rules](#plugin-rules) )
or using targeted suppressions with pragmas.

##### Document Front-Matter Extension

The [Document Front-Matter](https://github.com/jackdewinter/pymarkdown/blob/main/docs/extensions/front-matter.md)
extension (id of `front-matter` and disabled by default) allows for an optional
YAML front-matter block to be inserted at the first line of the document.
For applications that aggregate Markdown pages into a condensed form (such
as a web site), having such a front-matter block is useful in conveying information
from the Markdown document to that application.  This is indeed the case with the
[MkDocs application](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data)
used to aggregate our Markdown documents into this documentation web site.

For example, depending on the documentation you are trying to write, you could
use the MkDocs application along with a Markdown document with the following
front-matter:

```Markdown
---
title: My First Article
authors:
    - Clark Kent
date: 1938-04-18
---
This is the first paragraph of the document.
```

Without this extension enabled, PyMarkdown would interpret the first line and sixth
line as thematic breaks with the content of lines 2 to 5 being interpreted as a
paragraph.  When MkDocs aggregates this
document, the content it displays starts with the line `This is the first...`,
using the front-matter YAML as metadata. Specifically, it uses the
`title` field for the document and ignores the other fields unless they are used
by
one of the themes.  To ensure that
PyMarkdown does not trigger failures based on the "paragraph content" between the
two "thematic breaks", enabling this extension will treat it the same way
as the aggregating application (MkDocs in this case).

#### Plugin Rules

Plugin rules (usually just referred to as rules) are the code that enables
the rule engine to look for behavior that it believes is sub-optimal.  The scope
of these
rules may vary from detecting long lines in the document
([Rule MD013](https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md013.md)),
to superfluous blank lines in the document
([Rule MD012](https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md012.md)),
to detecting what looks like a missed Markdown ATX Heading annotation
([Rule MD018](https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md018.md)).

For most users, they only need to know how to disable or enable the rules released
with PyMarkdown.
From the command line, disabling a rule is accomplished using
the `-d` or `--disable-rules` argument followed by a comma-separated list of the
rule's id or one of the rule's aliases.  Likewise, enabling a rule is accomplished
using
the `-e` or `--enable-rules` argument followed by a comma-separated list of the
rule's id or one of the rule's aliases.

For example, if you disagree with PyMarkdown that long lines and extra blank lines
in a Markdown document
are bad, you can add the arguments `-d MD012,MD013` before the `scan` argument in
the command line.
Applied to our example directories, the new command line would look like:

```txt
pymarkdown -d MD012,MD013 scan examples
```

If human readable names are preferred, the equivalent command using rule aliases
is:

```txt
pymarkdown -d no-multiple-blanks,line-length scan examples
```

This same pattern also holds true for enabling rules.  However, caution should be
used
when enabling rules.

Our team has taken care to set each enabled rule's defaults so that they do not
conflict
with each other. Therefore, when enabling a rule that is disabled by default, it
may cause a series of competing failures between the two rules. By the term "competing
failures",
we mean that the fixing of failures for one rule causes another rule to have failures,
with
the fixing of those failures causing the initial set of failures to fail again,
and so on.  In that situation,
one of those two competing rules must be disabled to solve the problem.

In addition to enabling and disabling rules, many of the rules have extra configuration
that allow you to adjust their
default values to meet your needs.  Information on how to set that configuration
on
a per rule basis is covered in the document [Advanced Configuration](./advanced_configuration.md#rule-plugins).
For other information
about rules and their capabilities, consult the [Advanced Rules Guide](./advanced_plugins.md).
That guide covers these topics in more detail, including a list of all rules that
are
released with PyMarkdown and detailed information on each rule.

### Basic Configuration

As noted in the above section on [Plugin Rules](#plugin-rules), most users will
either require no configuration or the ability to enable and disable individual
rules.  The ability to disable and enable rules on a document level combined with
the
ability to suppress specific failures using the [Pragma extension](#pragma-extension)
will take care of the needs of most users.

### Advanced Configuration

In contrast to the disclaimer at the start of the [Advanced Scanning](#advanced-scanning)
section, these configuration settings are more geared towards advanced users that
want
to customize their usage of PyMarkdown.  While we will introduce these configuration
concepts in this document, please consult the [Advanced Configuration](./advanced_configuration.md)
document for more thorough descriptions of these features.

#### General Command Line Arguments

PyMarkdown provides a healthy amount of configuration that is independent
of the command used.  The full list of general arguments is:

```text
optional arguments:
  -h, --help            show this help message and exit
  -e ENABLE_RULES, --enable-rules ENABLE_RULES
                        comma separated list of rules to enable
  -d DISABLE_RULES, --disable-rules DISABLE_RULES
                        comma separated list of rules to disable
  --add-plugin ADD_PLUGIN
                        path to a plugin containing a new rule to apply
  --config CONFIGURATION_FILE, -c CONFIGURATION_FILE
                        path to the configuration file to use
  --set SET_CONFIGURATION, -s SET_CONFIGURATION
                        manually set an individual configuration property
  --strict-config       throw an error if configuration is bad, instead of assuming default
  --stack-trace         if an error occurs, print out the stack trace for debug purposes
  --continue-on-error   if a tokenization or plugin error occurs, allow processing to continue
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        minimum level required to log messages
  --log-file LOG_FILE   destination file for log messages
  --return-code-scheme {default,minimal}
                        scheme to choose for selecting the application return code
```

##### --enable-rules/--disable-rules (rules)

The `--enable-rules` and `--disable-rules` arguments instruct the PyMarkdown application
to enable rules or
disable rules for the current execution of the application.  Both arguments require
an extra
argument that specifies a comma-separated list of rules to apply the first argument
to.  This
argument is more fully covered in the [Plugin Rules](#plugin-rules) section above.

##### --add-plugin (rules)

The `--add-plugin` argument is followed by a path to a specially crafted Python
file that
implements a new plugin rule.  This is an advanced topic covered under the
[Developer Guide](./development.md)
section of this documentation.

##### --config (configuration)

The `--config` argument is followed by a path to a configuration file to load
for the current execution of the PyMarkdown application.  While the basic usage
of configuration
files is simple, there are a fair number of interactions to consider
when supplying configuration.  As such, this is more fully covered in the
[Advanced Configuration](./advanced_configuration.md)
document, especially the section on the [configuration files](./advanced_configuration.md#configuration-files).

##### --set  (configuration)

The `--set` argument is followed by a configuration name and configuration value
to explicitly set for
the current execution of the PyMarkdown application.  While the basic usage of configuration
files is typically simple, there are a fair number of interactions to consider
when supplying configuration.  As such, this is more fully covered in the
[Advanced Configuration](./advanced_configuration.md#specific-command-line-settings)
section of this documentation.

##### --strict-config (configuration)

The `--strict-config` argument instructs the configuration system to throw an error
if any aspect of the configuration is not specified correctly. The normal behavior
is
that a configuration value is only applied if it is valid and correctly formatted.
If any configuration values fail those requirements, then the default configuration
value is applied
instead.

While this is good behavior from a fault-tolerance point of view, it can be difficult
to
debug why a configuration value is not being applied properly.  By applying any
configuration in
`strict mode` with the `--strict-config` argument, a more useful error message
will be generated, explaining why the configuration
value was not acceptable.

##### --stack-trace (error reporting)

The `--stack-trace` argument instructs the error reporting system to engage in
two
beneficial behaviors for figuring out the cause of certain errors.  While users
may use
this argument of their own volition, it is more likely that users will be asked
to
run a command line with this flag present to help debug a reported issue.

The two beneficial behaviors that occur are the setting of the pre-initialization
log level
to `DEBUG` and the printing of a stack trace if an application error
is reported.  This information helps the PyMarkdown project team in that it provides
more information that can be used to figure out the cause of a reported issue.

These behaviors do not change any element of processing the Markdown document,
they only change how PyMarkdown reports initial logging and error information.
Also,
while these behaviors do not have any negative side effects, any benefits outside
of providing error reporting are negligible.

##### --continue-on-error (error reporting)

The `--continue-on-error` argument instructs PyMarkdown to log any application errors,
but to keep on going with the processing of Markdown files.  This feature was introduced
for use in a bulk mode where a group of Markdown files are being scanned at once.
With this argument
specified, the PyMarkdown application will report the application error as an error,
and then continue to the next Markdown document.
Without this argument, a single application error will stop the processing for the
entire
group of files.  At the end of processing the entire group, the application returns
the correct return code, telling the calling program that the application error occurred.

The beneficial behavior that occurs here is that scanning for failures
continues
on a large set of files while not ignoring the application error.  What confirmed
our choice to implement this feature was a real-world scenario that occurred near
the end
of one of our testing cycles.  Our team was getting ready to create a new release
and
did our normal PyMarkdown scan of our own documentation... only to find that one
of
our new rules was throwing an AssertionError for a scenario we thought was impossible.
In this situation, we were able to use the `--continue-on-error` argument to
complete our scan all the Markdown files, finding out that another Markdown file
was
also triggering that AssertionError.  That information allowed us to still do our
release
as planned, with resolving that newfound issue being placed at the top of our issues
list.
This was important to us as we were still able to scan the documentation properly,
just not on those two files. And since we had an immediate plan to address the error
in those two files,
we had the confidence to create the release knowing the cause of the error and
the scope of the error.

While these behaviors do not have any negative side effects, any benefits outside
of providing error reporting are negligible.

##### --log-level (logging)

The `--log-level` argument instructs PyMarkdown to set its logging level to one of
the specified values:

- `CRITICAL`
- `ERROR`
- `WARNING`
- `INFO`
- `DEBUG`

By default, the log level for the application is `WARNING`.

##### --log-file (logging)

The `--log-file` argument instructs PyMarkdown to redirect any logging output to
the specified file.  If this file does not already exist, it will be created.

##### --return-code-scheme (observability)

The `--return-code-scheme` argument takes values of `default` and `minimal`.  This
value instructs PyMarkdown to return non-zero error codes that adhere to a given
scheme.

In terms of general results to return, they can be classified into these categories:

| Category | Description |
| --- | --- |
| `SUCCESS`|everything looks good, no errors|
|`NO_FILES_TO_SCAN`|the paths presented to the application generated 0 files to scan|
|`COMMAND_LINE_ERROR`|at least one of the command line arguments was not valid|
|`FIXED_AT_LEAST_ONE_FILE`|at least one file was fixed, changing its content|
|`SCAN_TRIGGERED_AT_LEAST_ONCE`|at least one failure was triggered|
|`SYSTEM_ERROR`|an application error occurred, possibly [stopping the application](#-continue-on-error-error-reporting)|

The chosen schema handles representing each category as a return code.
The `default` scheme assumes that a categories of `COMMAND_LINE_ERROR` and `FIXED_AT_LEAST_ONE_FILE`
are interesting but defaulting all other error return codes to `1`.  The `minimal`
scheme is somewhat the opposite, only treating the categories of `COMMAND_LINE_ERROR`
and `SYSTEM_ERROR` as errors, returning `0` for all other return codes.  The table
for both themes is as follows:

| Category | `default` | `minimal` |
| --- | --- | --- |
| `SUCCESS`|0|0|
|`NO_FILES_TO_SCAN`|1|0|
|`COMMAND_LINE_ERROR`|2|2|
|`FIXED_AT_LEAST_ONE_FILE`|3|0|
|`SCAN_TRIGGERED_AT_LEAST_ONCE`|1|0|
|`SYSTEM_ERROR`|1|1|

### Fix Mode - Failure Correction

Running PyMarkdown in failure correction mode (also known as fix mode) will enable
the rule engine to fix certain failures
instead of just reporting that those errors occurred.

The rule engine can do this with a certain class of failures because
each failure within that class has a logical remedy that can be enacted by the
rule that triggers that failure. For example, Rule MD010 produces a failure for
any tabs found
in a Markdown document.  The remedy for that failure is for that rule to replace
any text characters
within the document with the proper number of space characters.  Rule MD009 produces
a failure if any line in the document is trailed by 1 or more spaces, except for
the hard-line break sequence (two space characters) within a paragraph.  The
remedy for that failure is to remove the trailing spaces at the end of the line.

On the other hand, there are rules such as Rule MD018 which look for possible
typos in the Markdown document.  Rule MD018 specifically looks for a line that
starts with between 1 and 6 hash characters (`#`) followed by alphanumeric
characters instead of space characters.  With those space characters, that
character sequence is an ATX Heading element.  Without at least one space
character after the hash characters, it is just text.

However, there is no obvious choice on how to fix this failure. While it is possible
that the user intended to write the ATX Heading element `# bob` instead of the
text element `#bob`, there is no distinct way to be sure.  To make that
decision, the rule would likely have to incorporate elements of artificial
intelligence to establish the context surrounding the text sequence `#bob`
to determine what was intended.  Without that added context, the rule
cannot properly fix this failure.

<!--- pyml disable-next-line no-duplicate-heading-->
#### Command Line Arguments

Correcting failures is a logical extension of scanning for those same failures.
As such, all the `scan` instructions in the [Basic Scanning](#basic-scanning) and
[Advanced Scanning](#advanced-scanning) sections also apply to Fix mode, except
for [scanning from standard input](#scanning-from-standard-input).

```txt
usage: pymarkdown fix [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]

positional arguments:
  path                  one or more paths to examine for eligible Markdown files

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-files      list any eligible Markdown files found on the specified paths and exit
  -r, --recurse         recursively traverse any found directories for matching files
  -ae ALTERNATE_EXTENSIONS, --alternate-extensions ALTERNATE_EXTENSIONS
                        provide an alternate set of file extensions to match against
```

### Plugin Command

The `plugin` command allows a user to query the presence and current state of any
rule plugin installed within the PyMarkdown application.

```txt
usage: pymarkdown plugins [-h] {list,info} ...

positional arguments:
  {list,info}
    list       list the available plugins
    info       information on a specific plugin

optional arguments:
  -h, --help   show this help message and exit
```

#### List Subcommand

The `list` subcommand produces a columnized list of the properties associated with
each rule plugin.

```text
usage: pymarkdown plugins list [-h] [--all] [list_filter]

positional arguments:
  list_filter  filter

optional arguments:
  -h, --help   show this help message and exit
  --all        show all loaded plugins (default is False)
```

The information returned includes columns for:

- `ID` - identifier of the rule
- `NAMES` - names or aliases associated with the rule
- `ENABLED (DEFAULT)` - whether the rule is enable by default
- `ENABLED (CURRENT)` - whether the current configuration has enabled the rule
- `VERSION` - revision associated with the rule
- `FIX` - whether fix mode is supported for this rule

An optional `list_filter` argument may be added with a simple [glob](https://docs.python.org/3/library/glob.html)
format. This filter is applied to the `ID` field and the `NAMES` field to
reduce the scope of the returned information.  For example,
using an argument of `*single*` as the `list_filter` on the latest build
provides the following output:

```txt
  ID     NAMES                    ENABLED    ENABLED    VERSION  FIX
                                  (DEFAULT)  (CURRENT)

  md025  single-title, single-h1  True       True       0.5.0    No
  md047  single-trailing-newline  True       True       0.5.1    Yes
```

#### Info Subcommand

The `info` subcommand produces an itemized list of names and values associated with
the plugin specified by the required `info_filter` argument.  That argument can
either be the rule's id or one of its aliases.

```text
usage: main.py plugins info [-h] info_filter

positional arguments:
  info_filter  an id

optional arguments:
  -h, --help   show this help message and exit
```

The output of the subcommand presents focused information on the rule in
question.  For example, using an argument of `md001` produces the following
results:

```txt
  ITEM                 DESCRIPTION

  Id                   md001
  Name(s)              heading-increment,header-increment
  Short Description    Heading levels should only increment by one level at a time.
  Description Url      https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md001.md
  Configuration Items  front_matter_title
```

### Extension Command

With only a single difference, the `extension` command follows the same pattern
as the `plugin` command described above.  As extensions have names instead of
aliases, the `info` subcommand for extensions can only take the ID of the extension,
and not an alias.  Otherwise, the use of the command and the data returned
closely mirror the behavior of the `plugins` command.

<!--- pyml disable-next-line no-duplicate-heading-->
#### List Subcommand

The `list` subcommand produces a columnized list of the properties associated with
each extension.

The information returned includes columns for:

- `ID` - identifier of the extension
- `NAMES` - a human readable name for the extension
- `ENABLED (DEFAULT)` - whether the extension is enable by default
- `ENABLED (CURRENT)` - whether the current configuration has enabled the extension
- `VERSION` - revision associated with the extension

```txt
 ID                           NAME                         ENABLED    ENABLED    VERSION
                                                            (DEFAULT)  (CURRENT)

  front-matter                 Front Matter Metadata        False      False      0.5.0
  linter-pragmas               Pragma Linter Instructions   True       True       0.5.0
  markdown-disallow-raw-html   Markdown Disallow Raw HTML   False      False      0.5.0
  markdown-extended-autolinks  Markdown Extended Autolinks  False      False      0.5.0
  markdown-strikethrough       Markdown Strikethrough       False      False      0.5.0
  markdown-task-list-items     Markdown Task List Items     False      False      0.5.0
```

<!--- pyml disable-next-line no-duplicate-heading-->
#### Info Subcommand

The `info` subcommand produces an itemized list of names and values
associated with the extension specified by the required `info_filter` argument.
That argument must be the id of the extension to retrieve information about. For
example, using an argument of `front-matter` produces the following
result:

```txt
  ITEM               DESCRIPTION

  Id                 front-matter
  Name               Front Matter Metadata
  Short Description  Allows metadata to be parsed from document front matter.
  Description Url    https://github.com/jackdewinter/pymarkdown/blob/main/docs/extensions/front-matter.md
```

### Version Command

As noted in the [Getting Started document](./getting-started.md#installation), the
version command simply returns the version of PyMarkdown that is installed using
the form:

```text
{major}.{minor}.{fix}
```
