---
summary: Instructions on how to start working with PyMarkdown
authors:
  - Jack De Winter
---

# Getting Started

There are two main paths to executing the PyMarkdown linter: either installing
it on your system or installing it via the [Pre-Commit](https://pre-commit.com/)
application. Which one you use depends on your own preferences as well as the
requirements of the project that you are working on. Our project supports both
paths equally.

## Keeping Things Simple

To keep the examples on this page simple and easy to follow, we have expressly
chosen to use Markdown documents and command lines that are simple. For this
same reason, we do not show any of our more advanced features, instead focusing
on keeping our examples clear and concise.

For more information on the available command line arguments and more advanced
features of PyMarkdown, check out our [user guide](./user-guide.md).

## Prerequisites

Both execution paths require the use of Python packages. As such, please ensure
that the following prerequisites are installed on your system before going
ahead.

If you are familiar with Python and the PipEnv package manager, and have already
installed them on your system, feel free to skip ahead to the section on
[installing PyMarkdown](#installation).

### Installing Python

Regardless of which execution path you take to use the PyMarkdown application,
Python must be installed on your system. The quickest way to check if Python is
installed and the version installed is to execute the following command:

```bash
python --version
```

If Python is not installed or is not available, an error will be returned saying
that it could not find the `python` application. If Python is installed, output
will be returned in the form of:

```text
Python {major}.{minor}.{fix}
```

The PyMarkdown application requires Python 3.9 or later to function. This means
that the output from above must show a major version of `3` and a minor version
of `8` or higher.

If Python is not installed, the
[Python home page](https://www.python.org/downloads/) provides release
information for all three major platforms and instructions on how you can
install Python on your system using the application tools native to the desired
operating system and shell. If all else fails, a quick Internet search should
reveal tutorials on how to install Python for every operating system.

### Installing PipEnv

Whether you are executing Python applications or developing Python applications,
we heavily suggest using a package manager such as
[PipEnv](https://pipenv.pypa.io/en/latest/) for managing your Python packages.
Unless you have a compelling argument for installing the package globally, we
believe that having all information about the packages needed for a project
within that project is always the best course of action. As an added benefit, if
the project involves a CI/CD pipeline, there are well-known patterns to use the
PipEnv files in CI/CD pipelines, reducing the amount of extra coding needed for
the pipeline.

Our project uses the PipEnv package manager, which is the package manager that
we suggest to our users because of its
[ease of use](https://www.linkedin.com/pulse/choosing-right-python-dependency-management-tool-pipenv-sanne/).
As PipEnv is used across projects, it is typically installed globally. The
compelling argument here is that each project needs a package manager to be
available to bootstrap itself. If it is not installed globally, projects would
find themselves in a
[chicken-and-egg](https://en.wikipedia.org/wiki/Chicken_or_the_egg) situation.

Assuming you choose PipEnv as your package manager, the following command will
figure out if PipEnv is installed and which version of PipEnv is installed:

```bash
pipenv --version
```

Like the check to see if Python itself was installed, if PipEnv is not installed
or is not available, an error will be returned saying that it could not find the
`pipenv` application. If PipEnv is installed, output will be returned in the
form of:

```text
pipenv, version 2023.12.1
```

where the noted version is the year-month-date of the latest release. If PipEnv
is not installed, it can be installed by executing the following command:

```bash
pip install --user pipenv
```

If PipEnv is installed but not at the latest version, executing the above
`pip install` command will show if a new release of PipEnv is available. If a
new release is available, the output will detail how to install the newer
release. As security fixes are made to PipEnv a couple of times a year, we
strongly encourage users to always upgrade to the latest version of PipEnv.

## Installation

As noted in the above section on [Installing PipEnv](#installing-pipenv), our
team sincerely believes that using a package manager for managing packages is
the best approach. Therefore, to keep all our examples clean and uncluttered, we
have chosen to use PipEnv in all our examples of command lines that install or
execute Python packages.

If instead you decide to install these packages globally on your system, replace
the text `pipenv install -d` in the command line examples with the text
`pip install`. In addition, for command lines that show how to execute
PyMarkdown, replace the text `pipenv run pymarkdown` in the command line
examples with the text `pymarkdown`.

### Installing Via PipEnv

Installing the PyMarkdown linter is as easy as going to your project directory
and entering the following command line:

```bash
pipenv install -d pymarkdownlnt
```

To confirm that the PyMarkdown linter is installed for the project, enter the
following command line:

```bash
pipenv run pymarkdown version
```

If PyMarkdown was installed properly, output will be returned in the form of:

```text
{major}.{minor}.{fix}
```

For more information on why you need to install a package named `pymarkdownlnt`
instead of `pymarkdown`, please [read here](./index.md#why-is-this-application-referred-to-as-pymarkdown-and-pymarkdownlnt).

#### What Is The `-d` For?

Per the PipEnv help text (`pipenv install --help`), the `-d` is used to install
both development packages and default packages. That was a bit confusing to us
at first, but thankfully articles like
[this article](https://realpython.com/pipenv-guide/#example-usage) clarified our
usage of `-d`.

A summary of that article is that there are differences between
the packages needed while using the application in production and the packages
needed while developing the application.
As PyMarkdown typically falls into the development category, the `-d` on the
command line installs the `pymarkdownlnt` package as a development package. If
you plan to use the PyMarkdown linter in a non-development setting, you may
remove the `-d` from the command line without any negative side effects. For
more information, please read the above article, as it presents a clear picture
of how to use PipEnv in various scenarios.

### Installing Via Pre-Commit

Outlined on their home page, [Pre-Commit](https://pre-commit.com/) was created
to solve the problem of being able to customize a set of tools to execute prior
to committing any changes to a Git repository. Because of that requirement, the
Pre-Commit tool only works in Git repositories. However, this is usually not an
issue for our users. We believe that most of our users are serious about using
code analysis tools for scanning their projects and those projects are already
contained with a Git repository.  For any project worth scanning, it
makes good sense to have the project within a source repository, and Git is one of
the most popular ones.  As such, this requirement does not seem like a bad
one from our point of view.

While the install instructions are covered more completely on the Pre-Commit
home page, the base installation process mirrors that of installing PyMarkdown
itself. Enter the following command line:

```bash
pipenv install -d pre-commit
```

To confirm that the Pre-Commit tool is installed for the project, enter the
following command line:

```bash
pipenv run pre-commit --version
```

To which output should be returned in the form of:

```text
pre-commit {major}.{minor}.{fix}
```

The above steps will evaluate that you installed Pre-Commit successfully, but not
that you installed PyMarkdown successfully through Pre-Commit. To do that,
create a file named `.pre-commit-config.yaml` in the root of the project
directory and add this text to that file:

```yml
default_stages: [commit, push]

repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: main
      hooks:
          - id: pymarkdown
```

This file provides the configuration for the Pre-Commit application to use
PyMarkdown. This configuration tells Pre-Commit where to get the Pre-Commit hook
to execute from (the GitHub repository for PyMarkdown), the revision of that Git
repository, and the id associated with the hook. This configuration file will
invoke the PyMarkdown linter through Pre-Commit with its default configuration,
described in the next section.

#### Advanced Pre-Commit

The above section only starts to touch on the use of Pre-Commit with PyMarkdown.
For more information and suggestions with respect to Pre-Commit and PyMarkdown,
consult our [Advanced Pre-Commit](./advanced_pre-commit.md) page.

### Verifying The Installation

The easiest way to verify that your choice of execution path is working
correctly is to create a sample file in the root directory of your project
called `sample.md`. In that file, place the following contents:

```text
# First Heading
# Another First Heading
```

This document is purposefully constructed to trigger two failures:

1. MD022: Headings should be surrounded by blank lines.
1. MD025: Multiple top-level headings in the same document

If using PyMarkdown directly, enter the following command line:

```bash
pipenv run pymarkdown scan sample.md
```

If using Pre-Commit, ensure that the file `sample.md` is staged in the project's
Git repository and then enter the following command line:

```bash
pipenv run pre-commit run -a
```

In either case, as noted above, the output content should have the following
lines:

```text
sample.md:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```

For the PyMarkdown direct scenario, the above text is the only output that the
application should produce. That is because PyMarkdown was specifically told to
only scan the file `sample.md` in the current directory. If you replace the
command line arguments `scan sample.md` with the arguments `scan --recurse .`,
then PyMarkdown will recursively search for any Markdown file (any file with a
`.md` extension) starting with the current directory. PyMarkdown will then sort
the filenames in alphabetical order, scan each file, and report any failures
that were triggered. The above text is guaranteed to be in the resultant output
as the file `sample.md` is in the base directory. However, as it may not be the
only Markdown file with failures that is scanned, the above output may be
preceded or followed by failures from other Markdown files.

For the Pre-Commit scenario, the default behavior is to act as if the supplied
arguments were the `scan --recurse .` arguments used in the above adjusted
scenario. As the Pre-Commit tool is largely used to scan entire repositories
before a Git commit, defaulting its behavior to scanning any Markdown file in
the repository made the most sense. And while that is the default behavior, it
can be overridden by explicitly supplying the proper configuration in the
Pre-Commit configuration file, `.pre-commit-config.yaml`. However, those
configuration options are more advanced and will be covered later in the
documentation.

## CI/CD Pipelines

When using PipEnv as a package manager, it creates a `Pipfile` and a
`Pipfile.lock` to track the packages that are installed along with their current
versions. Pipeline environments are typically not setup in advance, so the
following sections illustrate how to set up the environment in the CI/CD
pipeline to match what is in the repository.

### GitHub Actions

Taken from our own
[GitHub main.yml](https://github.com/jackdewinter/pymarkdown/blob/main/.github/workflows/main.yml)
file, this is the start of the `lint` job that we use to validate our code
changes. For the sake of a clean example, the only change we made to the code
snippet below was to replace the `${{ env.default-python-version }}` reference
to an environment variable with that variable's value `3.9`, specified earlier in
the `main.yml` file.

```yaml
  lint:

    name: Project Quality Analysis
    runs-on: ubuntu-latest

    steps:

      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python 3.9
        uses: actions/setup-python@v5.2.0
        with:
          python-version: 3.9

      - name: Install PipEnv
        run: |
          pip install pipenv==2023.12.1

      - name: Sync With Repository
        run: |
          pipenv update -d
          pipenv graph
```

The first step in the job, `Checkout Repository`, is to checkout the repository.
This will pull the files from the Git repository for whichever branch the
GitHub Actions task is being executed on.
This is essential as most jobs act on changes to their repositories and that
context must be set up before any other steps are defined. The next step,
`Setup Python 3.9`, installs the specified version of Python for the pipeline's
use, mirroring the steps taken in the [Installing Python](#installing-python)
section above. The third step, `Install PipEnv`, continues that process by
mirroring the [Installing PipEnv](#installing-pipenv) process outlined above.

At that point in the job, the project repository is cloned with the correct
versions of Python and PipEnv installed. This allows the pipeline to execute the
`Sync With Repository` step to install any Python packages that are indicated by
the project's `Pipfile` and `Pipfile.lock` files. The command `pipenv update -d`
tells PipEnv to create a virtual environment for Python and to install any
packages outlined in the `Pipfile` and `Pipfile.lock` files to that virtual
environment. To aid in any potential issues that may arise, we include the
command `pipenv graph` to output a listing of all packages installed into that
virtual environment. While that output is not often needed, it is extremely
beneficial to have it already in place when it is needed for debugging issues.

With this setup completed, the next step can invoke python commands with the
confidence that the environment was properly created. In our `lint` job, we
execute eight other steps before getting to our own step that executes
PyMarkdown in the pipeline:

```yaml
  - name: Execute PyMarkdown on Current Docs
    run: pipenv run python ${{github.workspace}}/main.py --config ${{github.workspace}}/clean.json scan ${{github.workspace}} ${{github.workspace}}/docs
```

That probably looks a bit complicated, but in our case that is needed. As our
project is THE PyMarkdown project, we need to use the latest version of
PyMarkdown and not the version of the latest release. Therefore, we want to
directly invoke the application using the `main.py` file found in the root
directory. Along with that, we need to use the
`--config ${{github.workspace}}/clean.json` arguments to specify a configuration
file to alter the behavior of PyMarkdown.

We presented the above example in the interest of transparency, to show you how
we use PyMarkdown ourselves. Our own invocation step for PyMarkdown is not a
typical example due to those specific needs. For most cases, the best starting
place for a PyMarkdown step is the following:

```yaml
  - name: Execute PyMarkdown on Current Docs
    run: pipenv run pymarkdown scan --recurse .
```

This will cover most scenarios for using PyMarkdown in a GitHub Actions
pipeline. While the pipelines tend to get a bit more complicated, it is rarely
more than specifying a configuration file or specific directories to
scan.  We find that as people use the project locally, they start to experiment
with it more, finding the setting that works right for them and their project.
Once those configuration settings are committed to the repository, it is a
simple task to update the above `run` command line to match how you run
PyMarkdown locally.

Of course, if you use PyMarkdown through Pre-Commit, the GitHub Actions step
that you need is even simpler.

```yaml
  - name: Execute Pre-Commit
    run: |
      pipenv run pre-commit run --all
```
