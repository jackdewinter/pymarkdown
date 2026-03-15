# Quick Start: Installation

This guide walks you through installing PyMarkdown so you can run Markdown lint
checks from your command line or through Pre&mdash;Commit, depending on how your
project is set up.

You can run PyMarkdown in two primary ways, depending on how you want to use it
in your workflow:

- as a local command&#x2011;line tool (installed into a Python environment that
  you control and run manually or from a script)
- through Pre&#x2011;Commit (recommended if your project is stored in Git and you
  want automatic checks before each commit)

The underlying checks are the same in both cases; Pre‑Commit simply runs the command‑line
tool for you automatically before each commit.

Most of the Quick Start guides show examples for the local command&#x2011;line tool.
Those command‑line examples are also applicable when configuring PyMarkdown to run
through Pre&#x2011;Commit.

## What You Will Learn

> **Quick Start Guide Single Line Summary**
> This page walks you through a simple example of installing PyMarkdown locally on
> your system or through Pre-Commit, with a checklist to follow for verifying that
> you installed PyMarkdown properly.

On this page, you will learn how to:

- install PyMarkdown locally
- install PyMarkdown with Pre-Commit
- verify that PyMarkdown is installed properly

## Prerequisites

To be successful in setting up PyMarkdown, review the
[Prerequisites](./index.md#prerequisites) on our "Quick Start: Introduction" page.

### Extra requirements for using Pre‑Commit

If you want to use PyMarkdown with Pre‑Commit, you additionally need:

- A local Git repository (a folder where `git status` works).
- Basic Git skills, such as creating commits.

Pre‑Commit runs from the **root directory** of your Git project (the top‑level folder
that contains your repository).

## If You Run Into Issues

This Quick Start guide assumes that you can install PyMarkdown without encountering
any issues. If you do run into problems, the full [installation guide](../getting-started.md)
is always available to help you out.

## Install PyMarkdown Locally

If you prefer to run PyMarkdown directly from the command line, the easiest option
is to install it into your **system Python** with `pip`. If you are not sure what
to choose, use this option. It requires no extra configuration and is the simplest
path to get PyMarkdown running.

You may later decide to use a **virtual environment** for each project. A virtual
environment is an isolated Python setup that keeps your project's packages separate.
Tools like **Pipenv** can create and manage virtual environments for you, but you
do not need them for this Quick Start guide. If "virtual environment" is a new term
for you, you can safely ignore it and continue with the basic installation.

If you are not using a virtual environment (this is the most common case for new
users), run the `pip install` command in your normal terminal session. PyMarkdown
will be installed into your system Python.

For detailed information about installation, prerequisites, and alternative setups,
see the [Getting Started](../getting-started.md) guide. It covers more background
and advanced configuration examples.

Most first‑time users should pick **Global Python Install**.

From the base of your project directory (the same folder where you created `sample.md`),
open a terminal or command prompt and run one of the following:

- If you normally install Python packages with `pip`,
  choose **"Global Python Install"**.
- If you already use **Pipenv** to manage your project,
  choose **"Pipenv Package Manager"**.
- If you have never used either `pip` or Pipenv before,
  choose **"Global Python Install"**.

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pip install pymarkdownlnt
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv install pymarkdownlnt
    ```

<!-- pyml enable code-block-style-->

**Note:** The package name is `pymarkdownlnt` (without the second "i"). This is
the correct name to use with pip and pipenv.

### Note for Pipenv users

If you want PyMarkdown to be treated as a development‑only
tool (used while editing and testing, not when your application runs), install
it with:

<!-- pyml disable code-block-style-->
```sh
pipenv install -d pymarkdownlnt
```
<!-- pyml enable code-block-style-->

If you are unsure whether to use `-d`, use these guidelines:

- For applications or libraries you will deploy or publish: use
  `pipenv install -d pymarkdownlnt`.
- For small personal scripts or experiments, or if you are still not sure: use
  `pipenv install pymarkdownlnt`.

## Install PyMarkdown Through Pre&#x2011;Commit

[Pre‑Commit](https://pre-commit.com/) is a framework for running checks (such
as linters) before each commit. You can think of it as a "to-do list" that Git
runs automatically each time you commit, so tools like PyMarkdown can catch
problems before they enter your history.

Pre‑Commit runs automatic Markdown checks before every commit and helps keep your
Markdown formatting consistent across the project. Because it also supports many
other plugins, it is a go‑to tool for open‑source project maintainers, and we strongly
recommend using it with PyMarkdown.

For your **first setup**, especially if you are new to Pre‑Commit or Git hooks,
follow this order:

1. **Get PyMarkdown working locally.**  
   Complete the **Install PyMarkdown Locally** and **Verifying PyMarkdown Installation**
   sections and make sure `pymarkdown scan sample.md` runs successfully.
2. **Add automation with Pre‑Commit.**  
   Come back to this section and set up Pre‑Commit so the same checks run automatically
   before each commit.

This two‑step approach keeps the number of new concepts small at each stage.

If you already use Pre‑Commit and want to install PyMarkdown through
Pre‑Commit, it typically means adding the following YAML content to
a `.pre-commit-config.yaml` file in your project's root directory. If this
file does not exist yet, create it first following the guidelines at
the [Pre‑Commit](https://pre-commit.com/) homepage.

<!-- pyml disable code-block-style-->

For a minimal quick‑start Pre‑Commit configuration, you can use:

```yaml
- repo: https://github.com/jackdewinter/pymarkdown
  rev: main
  hooks:
    - id: pymarkdown
```

If you prefer a commented version that explains each field:

```yaml
# Quick-start example (okay for local experiments)
- repo: https://github.com/jackdewinter/pymarkdown  # Where to fetch the hook from
  rev: main                                         # Branch or tag to use (main is fine for experiments)
  hooks:
    - id: pymarkdown                                # The PyMarkdown hook that runs the linter
```

For real projects, it is safer to **pin** PyMarkdown to a specific tagged version,
so that your checks do not change unexpectedly when new releases are published.
For example:

```yaml
# Recommended for real projects
- repo: https://github.com/jackdewinter/pymarkdown
  rev: v0.9.0
  hooks:
    - id: pymarkdown
```

<!-- pyml enable code-block-style-->

Here, `rev: v0.9.0` tells Pre‑Commit to use the `v0.9.0` tag of the PyMarkdown repository
instead of always using the latest code.

For more on choosing and pinning versions, see the
[Pinning the PyMarkdown Version](../advanced_pre-commit.md#one-step-further-pinning-the-pymarkdown-version)
section of the Advanced Pre-Commit documentation.

With that YAML content added to your `.pre-commit-config.yaml` file, open a terminal
window, change your directory to your project's root directory, and enter the following
command line:

<!-- pyml disable code-block-style-->
```sh
pre-commit run --all
```
<!-- pyml enable code-block-style-->

This runs all configured Pre-Commit hooks, including PyMarkdown, on every file in
your repository. If you have already completed the **Verifying PyMarkdown Installation**
section, you can think of `pre-commit run --all` as running that same
`pymarkdown scan` check automatically for every file in your repository instead
of just `sample.md`.

The first time you run this command, Pre‑Commit may need to download and install
the PyMarkdown hook. This might take a little longer than future runs. That delay
is normal and does not mean anything is wrong with your setup.

Once configured:

- Pre‑Commit runs PyMarkdown automatically before each commit.
- You can also trigger it manually with `pre-commit run --all` as shown above.

If just adding that content to your `.pre-commit-config.yaml` file does not work,
please go to the more complete [Installing Via Pre&#x2011;Commit](../getting-started.md#installing-via-pre-commit)
section of our Getting Started guide for detailed, step‑by‑step instructions.

### Controlling Which Files Pre‑Commit Scans (Advanced / Optional)

This section is for users who already have Pre‑Commit working and want to fine‑tune
which files are checked.

For your **first installation**, you can safely skip this section. The default behavior
&mdash; Pre‑Commit sending **all files in your project** to PyMarkdown &mdash; is
usually fine.

If you later need to limit checks to Markdown files only or customize which files
are scanned, see the [Advanced Pre‑Commit](../advanced_pre-commit.md) guide for
step‑by‑step examples.

## Verifying PyMarkdown Installation

Use this quick check to confirm that PyMarkdown is installed correctly and that
you can run it from your command&#x2011;line environment without errors. You only
need to perform this check once, after installation or after configuration changes.

<!-- pyml disable list-marker-space-->
<!-- pyml disable code-block-style-->

1. At the base of your project directory (the top‑level folder for your project,
   also called the project root), create a file named `sample.md`. Copy the following
   contents into that file and save it:

    ```text
    # First Heading
    # Another First Heading
    ```

    **Note:** This example intentionally contains two top-level headings and no
    blank lines around them. These formatting problems give PyMarkdown clear issues
    to report when you run the linter, so you can see what Rule Failures look like.

    In your own documents, you should avoid these problems. They are included here
    only so you can see what PyMarkdown reports and how to read the output.

2. From the base of your project directory (the same folder where you created
   `sample.md`), open a terminal or command prompt and run one of the following
   commands, depending on how you installed PyMarkdown:

    === "Global Python Install"

        ```sh
        pymarkdown scan sample.md
        ```

    === "Pipenv Package Manager"

        ```sh
        pipenv run pymarkdown scan sample.md
        ```

3. Run the command and then compare the output from your terminal to the example
   below. You do not need an exact match; you are checking for the same **kind**
   of result:

    - the Rule Plugin IDs (`MD022`, `MD025`)
    - the line numbers (`:1:1` and `:2:1`)
    - the fact that three problems are reported

    If those parts match, your installation is working correctly and PyMarkdown
    is ready to use.

    ```text
    sample.md:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
    sample.md:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
    sample.md:2:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
    ```

4.  If PyMarkdown does not produce output similar to the above, don't worry &mdash;
    this is usually a simple configuration issue. Recheck your installation steps
    and see the [Installation](../getting-started.md#installing-pymarkdown) section
    for additional help.

    As a quick first check, make sure:

    - you are running the command in the same directory as `sample.md`, and
    - you can run `pymarkdown --version` (or `pipenv run pymarkdown --version`)
      without errors.

<!-- pyml enable code-block-style-->
<!-- pyml enable list-marker-space-->

## Where To Go From Here

You should now have PyMarkdown installed on your system.

**Next**, in the Quick Start guides series:

- use the [Quick Start: General Command Line Usage](./general.md) to learn generally
  about PyMarkdown commands

**If** you are comfortable with discovering how to use the command line yourself,
you can decide to skip ahead to one of the following pages:

- Use [Quick Start: Scanning Markdown Files](./scanning.md) to apply scan to real
  projects.
- Use [Quick Start: Fixing Markdown Files](./fixing.md) to learn how to safely apply
  fixes.

**If** you need some review:

- Select [Quick Start: Introduction](./index.md) for an overview of all Quick Start
  documents
