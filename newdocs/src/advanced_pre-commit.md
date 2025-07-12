---
summary: How to use the pre-commit tool with the PyMarkdown application.
authors:
  - Jack De Winter
---

# Pre-Commit

As projects and teams race to deliver projects with built-in quality delivered
at a
respectable price, the [Pre-Commit](https://pre-commit.com/) framework and its
extended family of linters has become one of the de facto standards of teams
everywhere.  In their home page's introduction, their team talks about
how they struggled to add different tools to allow their code reviewers:

> "to focus on the architecture of a change while not wasting time with trivial
> style nitpicks"

Their belief is that you should be able to use the best-in-class linters and formatters,
even if that linter is written in another language.  And if that linter requires
something extra to be installed, such as installing Node for a linter written
in Javascript, Pre-Commit vows to manage that for you as well.

When dealing with Pre-Commit, it helps to think of the linters in two categories:
checkers and formatters.  The [PyLint linter](https://github.com/PyCQA/pylint) provided
by
the PyCQA team is a checker.  As a checker, it will scan through the repository
as instructed,
reporting any issues, returning a failure code to indicate that there were issues.
In comparison, the [Black](https://github.com/psf/black) linter
provided by the Black team is a Python formatter.  Just like a checker, it follows
the same
scan-report process.  However, before it reports any issues, it tries to address
those
issues on behalf of the caller before it returns the failure code.  In Black's case,
it is uncompromising and will always format Python
files with respect to standard Python coding guidelines.  If it had to fix even
one character of the Python file, it will do so and make sure you know that it fixed
something.

With an [exhaustive collection](https://pre-commit.com/hooks.html) of checkers and
formatters, Pre-Commit is the tool to use for any kind of linting need.
It can also be a bit intimidating at first, with tons of choices to choose from.
And we are glad to say that we are one of those choices!

## Basic Integration

We believe that our [Getting Started](./getting-started.md#installing-via-pre-commit)
documentation does a wonderful
job in describing how to set PyMarkdown up as part of Pre-Commit.  Instead of repeating
ourselves, we direct you to look there and see what a basic configuration
of Pre-Commit looks like for PyMarkdown.

When you are done, come back here so that we can go over the basics in more detail.

### What Are Hooks?

In Pre-Commit parlance, a `hook` is an external repository with instructions on
how to execute a specific linter through Pre-Commit.  Hooks can be created in any
one of [21 languages](https://pre-commit.com/#supported-languages), not including
the `local` hook for running scripts
local to your own system.  Depending on the repository, it is not unheard of
to have multiple hooks in a single external repository.  This is true of Pre-Commits'
own
[hook repository](https://github.com/pre-commit/pre-commit-hooks) which hosts over
20 hooks in a single repository.

### Creating a Pre-Commit Configuration File

After [installing Pre-Commit](./getting-started.md#installing-via-pre-commit) to
your project, the next step is to provide
Pre-Commit with its `.pre-commit-config.yaml` configuration file.  Note that this
file must exist in the root of the repository, otherwise Pre-Commit will not be
able to
locate it.

At the start of the configuration file, there are 6 top-level options that you may
choose,
followed by the `repos` section.  Those [top-level options](https://pre-commit.com/#pre-commit-configyaml---top-level)
can be used if you need them, but our team has only found a handful of times where
it was necessary.  For the most part, this code snippet:

```yaml
repos:
```

is all that you need.

### Pointing To PyMarkdown

To add support for PyMarkdown to the Pre-Commit configuration file, append the following
configuration to
the end of the `.pre-commit-config.yaml` file:

```yaml
  - repo: https://github.com/jackdewinter/pymarkdown
    rev: main
    hooks:
      - id: pymarkdown
```

The text at the same level as the `repo` item is the
[hook repository information](https://pre-commit.com/#pre-commit-configyaml---repos).
Essentially, the main parts of this text specify a public Git URL where the external
repository is located, followed by the `rev` or revision of the repository to use
for
the hook.  Valid values are the name of a branch (such as `main`), the name of a
tag
(such as `v1.2.3`), or a Git commit hash. Following the hook repository information
is the `hooks` section.  This section is
where the name of the hook within that repository is specified.  And since our
hook name is `pymarkdown`, we specify that as the id of the hook to execute.

#### One Step Further

Even though the above example specifies the `main` branch, our team would like you
to consider changing
`main` to a specific tag pointing to the latest build of PyMarkdown.  This is a
slightly more
advanced process, but it will help your project team keep track of the project's
dependencies.
This will incur extra work each time a new release of PyMarkdown is published, but
it gives your project team
explicit control of when to upgrade their dependencies.  We do try our hardest to
make everything backwards compatible,
but we are human, and we do sometime make mistakes. By pinning the version down,
your team will be able to upgrade
to the latest version and evaluate it at their own pace, without it becoming an
emergency.

The upgrade process is mostly simple.  The first thing to do is to locate the tag
of the
latest release of PyMarkdown. That information is located on
the [Releases Page](https://github.com/jackdewinter/pymarkdown/releases) to the
left
of the version with a green `latest` tag beside the title, usually located at the
top of
the page.  To the left of the release information, there is a sidebar with the date,
who created the release, the tag of that release, and the short hash for the commit
that the tag is associated with.  The tag will begin with a `v` character followed
by
three integers separated by the `.` character.  With the text from the tag, modify
the text `rev: main` in the configuration will with that tag text.  For example,
if the tag is `v0.9.18`, then that text should now read `rev: v0.9.18`.

If you are not sure that you are on the latest version of PyMarkdown or want
an easier way to update your hooks, you are in luck.
The following command line:

```text
pipenv run pre-commit autoupdate
```

will scan your `.pre-commit-config.yaml` file and update and the `rev` field to
the
tag for the latest release for every hook in your configuration file.  You have
a choice of either
checking each hook's repository manually or running that command every so often.
You can even create a new job for your CI/CD pipeline that installs
Python, PipEnv, and Pre-Commit before executing that command line.  If it returns
a non-zero value, you can decide how to handle the output.

For example, about once a month we run this command to see if anything needs updating.
If so, we test with the new values to see if there are any issues with our own machines
before committing those changes to the repository.  There the changes are further
tested
on all three operating systems before we merge it with the `main` branch.  That
is our
process.

#### Another Option

An even more advanced option is to use the commit hash (short form or long form)
of the
Git commit that you want to use.  We do not recommend this outside of its use in
helping to debug an issue.  You may be
asked by our team to specify a hash instead of the text `main` or a specific tag
value. Setting the
`rev` value to a specific hash value allows your configuration to target a specific
commit between releases. Since a tag just points Git to a specific commit, there
is no difference between using the tag `v0.9.18` for
[release 0.9.18](https://github.com/jackdewinter/pymarkdown/releases/tag/v0.9.18)
or its hash of `1f7755e` or `1f7755e3752fa8ae0b6f5cdea794bdce6dfa0d47`.  However,
from a
usability viewpoint, we feel that reading `v0.9.18` is more descriptive than `1f7755e`.

The reason that this method should be used for debugging only should be obvious.
While we do intermediate testing between releases, we typically do extra testing
before
publishing a new release of PyMarkdown.  By using a commit hash that is not a release,
you are using a version of PyMarkdown that may be in an intermediate state. As a
non-release
of PyMarkdown, if you report any problems with a hashed revision, we are going
to direct
you to specify the latest release before we triage any issues that you found.

To repeat, we strongly recommend only using a `rev` value that is a hash when
collaborating with our team to diagnose and debug an issue.

### Specifying A Configuration File

This section relates to configuration files, as they are described in the
document on [Advanced Configuration](./advanced_configuration.md#configuration-files).
If you have not read that document to understand how PyMarkdown handles
configuration files, please read that document before proceeding.  Note that
while we can specify configuration files with [different internal formats](https://application-properties.readthedocs.io/en/latest/file-types/#configuration-file-types),
the following configuration examples are going to specify a JSON configuration file
named `pymarkdown.json`.

The easiest way to use PyMarkdown configuration files is to specify one of the
[default configuration files](https://application-properties.readthedocs.io/en/latest/file-types/#default-configuration-files).
The PyMarkdown application looks for these configuration files with predetermined
names
in the directory that PyMarkdown is executed from.  As Pre-Commit has no concept
of
changing the working directory before or during execution, this only works if the
PyMarkdown configuration file is in the root directory of the repository.

If that is not the case, you must specify the configuration file as an argument to
the `pymarkdown` hook.  While we will explain this in more depth in the following
sections, the code snippet for specifying a configuration file of `pymarkdown.json`
is:

```yaml
    - id: pymarkdown
      args:
        - --config=pymarkdown.json
        - scan
```

From the Advanced Configuration documentation, keep in mind that the `--config`
argument
specifies a path to the configuration file from the current directory.  As Pre-Commit
always executes from the root directory of the repository, if your configuration
file is not in the root directory, you must specify a relative path from the root
directory:

```yaml
    - id: pymarkdown
      args:
        - --config=docs/src/pymarkdown.json
        - scan
```

Note that for portability reasons, you should never specify a full path to the
configuration file.

## Advanced Integration

The Pre-Commit tool has been well vetted by many users.  While it may not seem like
it has all the bells and whistles needed, the Pre-Commit configuration operations
on a per-hook basis are extensive. To support all those hooks, the Pre-Commit team
has had to be innovative in providing a solid set of ways to specify configuration
for the many supported hooks.  The outcome of this is that
the [Configuration Hook Arguments](https://pre-commit.com/#pre-commit-configyaml---hooks)
section of their document can be a bit daunting to understand.  To help mitigate
that
feeling, we present our simplistic take on how to use Pre-Commit hooks, specifically
geared towards PyMarkdown.

### Hook Argument Breakdown

Hook arguments are the method by which you pass command line arguments into the various
hooks from the Pre-Commit configuration file. As a user, they allow you to change
the behavior of the hook to suit your needs.  But to understand how to add new arguments,
we believe you need to understand how to change a PyMarkdown command line into hook
arguments for PyMarkdown.

Each command line to translate can be broken down into three parts:
what to invoke, what arguments to use, and what files to send to the hook. To
provide concrete examples for translation, we will use the following command line
from the Getting Started document's [Verifying The Installation](./getting-started.md#verifying-the-installation)
as the foundation for our example:

```bash
pipenv run pymarkdown scan sample.md
```

However, since that command line only scans one file and Pre-Commit is typically
used to scan
entire projects, we have changed the example slightly to mimic that behavior
by scanning all files recursively:

```bash
pipenv run pymarkdown scan -r .
```

What to invoke is the most important part of that command line, and that is covered
by the hook's own
configuration with Pre-Commit.  Using either of the above examples as a guideline,
Pre-Commit
follows its own processes to replicate the effect of the text `pipenv run pymarkdown`.
That part
simply makes sure that the PyMarkdown application is properly invoked by Pre-Commit.

The next two parts of that command line specify what arguments to use when PyMarkdown
is invoked
and what files to send to the hook.  From a Pre-Commit perspective, there are arguments
that you want to pass to the hook that alter the hook's behavior
and there are arguments to specify what files to scan by the hook.  This
is an important distinction as Pre-Commit specifically manages what files to pass
into
a given hook.  In our example above, anything after the word `scan` is used to specify
the files to scan.

That leaves us with the remainder of the command line, which dictates how the user
wants to configure the PyMarkdown application.  While this text in our example
only includes the word `scan`, the text could have just as easily specified a
configuration file:

```bash
pipenv run pymarkdown --config=docs/src/pymarkdown.json scan -r .
```

In that case, the configuration part of that command line is
`--config=docs/src/pymarkdown.json scan` and the file specification part of the
command line
is `-r .`. As the PyMarkdown hook specification takes care of the first part, we
will
now focus on those other two parts: the hook arguments and hook file specification.

### Hook Arguments

As mentioned above, hook arguments are used to specify the configuration
to pass to PyMarkdown. For example, the command line from above:

```bash
pipenv run pymarkdown --config=docs/src/pymarkdown.json scan -r .
```

translates into the Pre-Commit configuration for the PyMarkdown hook:

```yaml
    - id: pymarkdown
      args: [--config=docs/src/pymarkdown.json, scan]
```

OR

```yaml
    - id: pymarkdown
      args: [--config, docs/src/pymarkdown.json, scan]
```

OR

```yaml
    - id: pymarkdown
      args:
        - --config
        - docs/src/pymarkdown.json
        - scan
```

Each of these examples are valid YAML, the language used by Pre-Commit for their
configuration file. In each case, the command line is translated into an acceptable
form of the Pre-Commit hook `args` configuration item. The first example is a literal
translation of the command
line, including the "merged" `--config` argument and that argument's path parameter.
The second and third examples are equivalent to each other, and are programmatically
the same as the first example, just with the `--config` argument and its path
parameter pulled apart.

One crucial factor is that each of those argument lists end with the `scan` command.
If one of the [six commands](./user-guide.md#command-line-basics) is not present
at the end
of the hook arguments list, PyMarkdown will interpret the first filename
as the command to execute... and will cause an error. Unless you are working
on something esoteric, the only two commands that should appear at the end of
the `args` value are the `scan` command and the `fix` command.

Note that the PyMarkdown hook is configured with a default argument list of `[scan]`.
That
default ensures that at the very least, if no arguments are present, PyMarkdown
is invoked in scan mode with no
configuration changes.

### Hook File Specification

By default, the configuration for the PyMarkdown Pre-Commit hook
specifies a value of `types: [markdown]`.  This instructs Pre-Commit's
[filter mechanism](https://pre-commit.com/#pre-commit-configyaml---hooks) to only
send
filenames to this hook that are of type `markdown`, according to the Python
library [identify](https://github.com/pre-commit/identify). This is talked about
more in Pre-Commits documentation on [file filtering](https://pre-commit.com/#filtering-files-with-types).
For Markdown, it simply looks for any files with a `.md` extension.

While sticking with this default will satisfy most scenarios, there are a handful
of scenarios that require slightly different file specifications. In those cases,
knowledge of
the following Pre-Commit hook arguments will be useful:

- `pass_filenames` - whether to pass a list of filenames to the hook
- `types` (treat as `types_and`) - ANDed list of required types for files to include
  in filename list sent to the hook
- `types_or` - ORed list of required types for files to include in filename list
  sent to the hook
- `exclude_types` - list of types to remove from the filename list sent to the hook
- `files` - a singular regular expression matching the files to add to the filename
  list
- `exclude` - a singular regular expression matching the files to remove from the
  filename list

#### `pass_filenames`

This option, which defaults to `true`, tells Pre-Commit whether to construct a list
of filenames and to pass it to the hook application.  This is essentially a big
switch that controls whether the other options in the above list are actioned on.
A good example of why you may want to do this is in the section below on
[Using the Command Line Effectively](#using-the-command-line-effectively).

#### `types`, `types_or`, and `files`

The `types` and `types_or` options specify different operations to do with file
types, as identified
by the Python `identify` package. The `files` option specifies a singular regular
expression used as a filter for the filenames.  All three of these options are
ANDed together to create the final list.  That is to say that unless the option
is set
to an empty value (which indicates acceptance of any file), each non-empty value
will reduce the count of items in the list.

For example, the only value of these three that is set as a default by the PyMarkdown
hook is the `types` field, set to `[markdown]`.  By following the above rule, we
can
surmise that any file with an `.md` extension in the repository will be scanned.
Therefore,
to restrict that scan to only Markdown files in the `/newdocs` directory, we simply
need to
add:

```yaml
    - id: pymarkdown
      files: ^newdocs/
```

which will filter the filenames to only allow files that start (`^` character)
with the text sequence `newdocs/`.

Note that our team often has difficulties remembering all the options available
for regular expressions.  We find pages such as the [Regular Expressions 101](https://regex101.com/)
page useful as a reference when building our regular expressions.

#### `exclude` and `exclude_types`

These options are like their `files` and `types` counterparts but are
used to restrict the files passed to the Pre-Commit hook.  To extend our above example,
say that we want to scan all the Markdown files in the `/newdocs` directory except
for
the `todo.md` file in that directory, which we already know is a problem.  Using
the `exclude` option, we can
restrict the filename list as follows:

```yaml
    - id: pymarkdown
      files: ^newdocs/
      exclude: ^newdocs/todo\.md$
```

## Configuration Files

Since we have had conversations with people regarding command line arguments
versus configuration files, we thought we would share our thoughts with you
on these subjects.

### Command Line Arguments Vs Configuration File

As part of our documentation on [Advanced Configuration](./advanced_configuration.md#command-line-vs-configuration-file),
we delve into this topic, providing our views on why to choose configuration files
over command line arguments.  There is no cut-and-dried answer that we can provide
for everyone.  Your own team's context is important.

From our team's perspective, we prefer to have the configuration settings for an
application
in a configuration file specific to that application.  While we understand that
it
means there are more files to deal with, it gives us confidence to know that each
configuration file has a distinct responsibility to the owning application.  That
is our context.  You and your team need to
determine what is important to you, make sure you have good reasons for doing so,
and make sure your projects follow that decision.

### Using the Command Line Effectively

While many things can be dealt with using a configuration file, there are times
that you
cannot get away from using it.
A good example of this
is the project's own [configuration](https://github.com/jackdewinter/pymarkdown/blob/main/.pre-commit-config.yaml)
that contains the following PyMarkdown configuration:

```yaml
    - id: pymarkdown
      pass_filenames: false
      args:
        - --config
        - clean.json
        - scan
        - .
        - ./docs
    - id: pymarkdown
      pass_filenames: false
      args:
        - --config
        - newdocs/clean.json
        - scan
        - ./newdocs/src
```

In the first case, there are two directories with Markdown to publish that need
scanning
and a whole lot of other directories that should not be scanned as they contain
examples of bad Markdown.  Because of this, the configuration explicitly follows
the `scan` argument with `.` to specify the base project directory and `./docs`
to specify the
documents directory.  Note that while configuration can be placed in a configuration
file, the paths to scan cannot.  As such, we use a configuration file to keep
the command line clean, allowing us to focus on the files we need to scan.

The effect of the above configuration is that PyMarkdown should only scan the `.`
and `./docs` directory.  However, Pre-Commit normally appends any eligible file
names to the end of the list of arguments.  Without the `pass_filenames: false`
specifier,
the arguments Pre-Commit would pass to PyMarkdown would be the `.` directory, the
`./docs` directory, and any eligible Markdown file in the repository.  It essentially
informs Pre-Commit: "It's okay, we can do it ourselves." This works well in this
case as
our arguments specify exactly what we want to scan.

The second case is just a repeat of the first case, with a different configuration
file and a different directory to scan.  For this case, we are moving from standard
Markdown files for documentation (`/docs` directory) to processing our documentation
through [MkDocs](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data)
and hosting it on [ReadTheDocs](https://pymarkdown.readthedocs.io/en/latest/).
As MkDocs has extra requirements, it makes sense that we have a separate
configuration file and scan specifically for that directory.

## Things To Watch Out For

In responding to user issues, we believe that how Pre-Commit
interacts with the PyMarkdown linter may not be intuitive.  Here are the behaviors
that initially caused us to be confused, and our process for how we worked through
these issues.

### Scanning Markdown Files with Alternate Extensions From Pre-Commit

This issue was brought to us by a user wanting to apply our PyMarkdown linter to
`.qmd` files using Pre-Commit.  With helpful pointers from our user, our research
verified
that [Quarto](https://quarto.org/docs/get-started/hello/vscode.html) uses Markdown
files with the `.qmd` extension.  Quarto then interprets these files to produce
the requested output in a variety of formats.  Given that Quarto files appear to
be plain Markdown files, following our documentation to instruct the PyMarkdown
linter to scan Quarto files should be easy.

We started out with basic tests first by placing the user's example `test.qmd`
file and `README.md` file into a test directory, scanning the directory using the
PyMarkdown command line to establish a known baseline.  After we verified that the
`test.qmd` file was being scanned and not the `README.md` file, we introduced simple
issues that we knew PyMarkdown can detect to both files.  As we predicted, PyMarkdown
detected the issues in the `test.qmd` files but not the `README.md` file.

With that simple test completed and passing, we took an independent approach to verify
our user's findings.  We started with the example provided in the section
[Pointing To PyMarkdown](#pointing-to-pymarkdown):

```yaml
  - repo: https://github.com/jackdewinter/pymarkdown
    rev: main
    hooks:
      - id: pymarkdown
```

Using that example as a base, we applied the logic from the
[Hook Argument Breakdown](#hook-argument-breakdown)
section, specifically the [--alternate-extensions or -ae](./user-guide.md#-alternate-extensions-or-ae)
flag of the `scan` action, and added the `args` element to produce:

```yaml
  - repo: https://github.com/jackdewinter/pymarkdown
    rev: main
    hooks:
      - id: pymarkdown
        args:
          - scan
          - --alternate-extension=.qmd
```

Placing that content into a `.pre-commit-config.yaml` file located in the same directory
as the other two files, we then executed Pre-Commit in that directory.  Using our
independent approach, we ended up at the same location as our user, with this response:

```text
Provided file path 'README.md' is not a valid file. Skipping.
```

After scratching our heads for a while, we remembered that in the
[Creating New Hooks](https://pre-commit.com/#creating-new-hooks)
section of the Pre-Commit homepage, we needed to setup the `.pre-commit-hooks.yaml`
file as follows:

```yaml
- id: pymarkdown
  name: PyMarkdown
  description: "PyMarkdown - GitHub Flavored Markdown and CommonMark Compliant Linter"
  language: python
  language_version: python3
  entry: pymarkdown
  args: [scan]
  types: [markdown]
```

This configuration specifically tells Pre-Commit to only pass files that it identifies
as `markdown` to the PyMarkdown scanner. Pre-Commit does this by using the [identify](https://github.com/pre-commit/identify)
package which defines `markdown` files by their `md` extension.  This means that
unless we provide something to override that configuration, Pre-Commit will only
pass files in the repository that have a `md` extension to PyMarkdown.

Therefore, to address this problem, our solution included two connected changes
to tell Pre-Commit to pass files with the `.qmd` extension to PyMarkdown.
The first change was adding this element at the same level as the `args` element:

```yaml
      files: .*\.qmd$
```

This specifically tells Pre-Commit that it should send any files that match that
regular expression to PyMarkdown.  For those not fluent in "regex": `.*` = any character
any number of times; `\.` = a `.` character (escaped), `qmd` = the characters themselves,
and `$` anchors the expression to the end of the string.  In short, look for any
filenames that explicitly end with the characters `.qmd`.

But that was only half of the solution.  Through research, we found that Pre-Commit
processes the `type` filter on eligible files before applying any `files` or `exclude`
filters.  Following that discovery, we determined that we needed to override the
`types` element we setup in our PyMarkdown hook.  This forces Pre-Commit to collect
all ligible paths, filter that list down to paths that represent files, and then
apply our existing `qmd` file filter to end up with our desired list of Quarto files.
Therefore, we needed to add this element at the same level as the `files` element:

```yaml
      types: [file]
```

We crossed our fingers, and everything worked!  We proceeded to run more thorough
tests on this configuration to be sure, but everything worked out.
