---
summary: Instructions on how to start working with PyMarkdown
authors:
  - Jack De Winter
---

# Getting Started

PyMarkdown can be used either directly or through Pre-Commit. Both options rely
on the same underlying Python environment and package management.

The next sections describe how to set up:

- Python (3.10+)
- Pipenv for project-local dependency management

After that, we show how to install PyMarkdown directly and via Pre-Commit.

## Quick Start Guide

If you only need the fastest path to "PyMarkdown is installed and running", use our
[Quick Start: Installation](./quick-starts/installation.md) guide.

This page is for readers who want a more complete setup: why we recommend Pipenv,
how to wire PyMarkdown into Pre‑Commit, and how to verify everything locally before
CI. If you already know some of this, skim or jump to the sections you care about.

## Keeping Things Simple

The examples on this page use simple Markdown files and command lines.
We avoid advanced features here so the instructions stay focused and easy to follow.

For more information on the available command line arguments and more advanced
features of PyMarkdown, check out our [User Guide](./user-guide.md).

## Prerequisites

You can use PyMarkdown in two ways:

- as a direct command-line tool, or
- through Pre-Commit.

Both approaches rely on Python packages, so install the prerequisites below first.

If you already have Python and Pipenv installed, feel free to skip ahead to
[Installing PyMarkdown](#installing-pymarkdown).

### Installing Python

PyMarkdown requires Python 3.10 or later. Verify your version:

```text
python --version
```

If this does not report at least Python 3.10.x, install or upgrade Python from the
[official downloads page](https://www.python.org/downloads/) before continuing.

### Installing Pipenv

We use [Pipenv](https://pipenv.pypa.io/en/latest/) to manage dependencies and recommend
it for PyMarkdown. In most setups, Pipenv is installed globally, and each project
keeps its own `Pipfile` / `Pipfile.lock` and uses `pipenv run` inside a project-local
virtual environment. This pattern also works well in CI/CD.

Verify that Pipenv is installed and check its version with:

```bash
pipenv --version
```

If Pipenv is not installed or not on your PATH, this command fails with an error.
If it is installed, you'll see output like:

```text
pipenv, version 2023.12.1
```

where the noted version is the year-month-date of the latest release. If Pipenv
is not installed, it can be installed by executing the following command:

```bash
pip install --user pipenv
```

If Pipenv is installed but not at the latest version, the `pip install` command
will indicate that a newer release is available. Because Pipenv receives regular
security fixes, we recommend upgrading to the latest version whenever possible.

## Installing PyMarkdown

The examples below use Pipenv-based commands. If you prefer a global installation,
adapt them as follows:

- Replace `pipenv install -d` with `pip install`.
- Replace `pipenv run pymarkdown` with `pymarkdown`.

The rest of the instructions remain the same.

### Installing PyMarkdown With Pipenv

In your project directory, run:

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

Per the Pipenv help text (`pipenv install --help`), the `-d` flag installs both
default and development packages. We use it because PyMarkdown is typically a
development-time tool.

Common patterns:

- `pipenv install -d pymarkdownlnt` – install PyMarkdown as a development dependency
- `pipenv install pymarkdownlnt` – install PyMarkdown as a regular dependency

If you plan to use PyMarkdown outside development, you can safely omit `-d`.

### Installing Via Pre-Commit

[Pre-Commit](https://pre-commit.com/) runs configurable checks before Git commits
and pushes. It operates only in Git repositories.

PyMarkdown integrates directly with Pre-Commit via a hook defined in the file `.pre-commit-config.yaml`,
as shown below. This configuration file will invoke the PyMarkdown linter through
Pre-Commit using PyMarkdown's default configuration. By default, the hook runs on
staged Markdown files for the configured stages (`commit` and `push` in this example).
If you want to always scan the entire repository or only specific paths, you can
adjust the hook's `args` and `files` entries. Later sections show how to verify
and customize that configuration.

Pre-Commit's own documentation covers installation in depth.
For this project, you can install it with:

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

The steps above verify that Pre-Commit is installed, but not that PyMarkdown
runs correctly through Pre-Commit. To test that, create a file named
`.pre-commit-config.yaml` in the project root and add:

```yml
default_stages: [commit, push]

repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: main
      hooks:
          - id: pymarkdown
```

This configuration file will invoke the PyMarkdown linter through Pre-Commit using
PyMarkdown's default configuration. Common customizations include:

- passing `scan --recurse docs` as hook arguments to restrict scanning to documentation
- using a project-specific configuration file via `--config`.

For more complex scenarios, consult the [Pre-Commit](https://pre-commit.com/) documentation
site.

#### Advanced Pre-Commit

The above section only starts to touch on the use of Pre-Commit with PyMarkdown.
For more information and suggestions with respect to Pre-Commit and PyMarkdown,
consult our [Advanced Pre-Commit](./advanced_pre-commit.md) page.

### Verifying The Installation

To verify that your chosen execution path works, follow these steps:

In the root of your project, create a file named `sample.md`.

Add the following contents:

```text
# First Heading
# Another First Heading
```

This sample intentionally violates two Rule Plugins:

1. **MD022:** Headings should be surrounded by blank lines.
1. **MD025:** Multiple top-level headings in the same document

If using PyMarkdown directly, enter the following command line:

```bash
pipenv run pymarkdown scan sample.md
```

If using Pre-Commit, ensure that the file `sample.md` is staged in the project's
Git repository and then enter the following command line:

```bash
pipenv run pre-commit run -a
```

In either case, the output should include the following lines:

```text
sample.md:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```

Each line has the form `file:line:column: rule-id: message (aliases)`. For example,
`MD022` reports missing blank lines around headings and shows the expected and
actual counts. This is the same format PyMarkdown uses in CI logs and Pre-Commit
output, so you can copy these lines directly into issue trackers or tooling.

When you run:

```sh
pipenv run pymarkdown scan sample.md
```

PyMarkdown scans only `sample.md`.

If you instead run:

```sh
pipenv run pymarkdown scan --recurse .
```

PyMarkdown recursively scans all `.md` files under the current directory and reports
all Rule Failures, including the ones from `sample.md`.

By default, the PyMarkdown Pre-Commit hook runs as if you invoked
`scan --recurse .`, scanning all Markdown files in the repository. To narrow
that scope, adjust the hook's `args` and `files` entries in
`.pre-commit-config.yaml`. For advanced configuration examples, see
[Advanced Pre-Commit](./advanced_pre-commit.md).

## CI/CD Pipelines

Once you have PyMarkdown working locally with Pipenv, you can reuse the same setup
in your CI/CD system. In CI, you mirror the local environment and run PyMarkdown
as part of your checks.

When you use Pipenv as a package manager, it creates a `Pipfile` and a `Pipfile.lock`
to track installed packages and their versions. Pipeline environments are typically
not set up in advance. The following sections show how to recreate the same environment
in CI/CD so it matches what is in the repository.

The example below uses GitHub Actions. The same basic steps &mdash; checking out
the repository, setting up Python, installing Pipenv, syncing dependencies, and
running PyMarkdown &mdash; apply to most CI systems.

### GitHub Actions

This section walks through a complete GitHub Actions job that runs PyMarkdown using
Pipenv. If you use another CI platform, skim this example for the overall flow,
then see [Other CI Systems](#other-ci-systems) for a shorter, platform‑agnostic
pattern.

The YAML below is taken from our own
[GitHub main.yml](https://github.com/jackdewinter/pymarkdown/blob/main/.github/workflows/main.yml)
file. It shows the start of the `lint` job we use to validate code changes.

For this example, we made one change: we replaced the
`${{ env.default-python-version }}` expression (defined earlier in `main.yml`) with
the explicit value `3.10`.

```yaml
  lint:

    name: Project Quality Analysis
    runs-on: ubuntu-latest

    steps:

      - name: Checkout Repository
        uses: actions/checkout@v5

      - name: Setup Python 3.10
        uses: actions/setup-python@v5.2.0
        with:
          python-version: 3.10

      - name: Install Pipenv
        run: |
          pip install pipenv==2023.12.1

      - name: Sync With Repository
        run: |
          pipenv update -d
          pipenv graph

      - name: Execute PyMarkdown on Current Docs
        run: pipenv run python ${{github.workspace}}/main.py --config ${{github.workspace}}/clean.json scan ${{github.workspace}} ${{github.workspace}}/docs
```

#### Workflow Setup

The first three steps do the standard setup:

- check out the repository,
- install Python 3.10, and
- install Pipenv.

This mirrors the local setup from [Installing Python](#installing-python) and
[Installing Pipenv](#installing-pipenv). As a result, CI runs PyMarkdown under the
same environment as your development machine. For long‑lived projects, we recommend
pinning the versions of Python and Pipenv you use in CI so that dependency changes
are deliberate, not accidental.

At this point in the job, the repository is cloned and Python and Pipenv are installed.

#### Sync With Repository

The `Sync With Repository` step sets up the project environment:

- `pipenv update -d` creates a virtual environment and installs the packages listed
  in `Pipfile` and `Pipfile.lock`.
- `pipenv graph` prints a list of all installed packages in that environment.

Use `pipenv sync -d` instead of `pipenv update -d` if you want CI to install exactly
the versions recorded in `Pipfile.lock`. This treats the lockfile as the single
source of truth and avoids changing it in CI.

You can usually ignore the `pipenv graph` output. It becomes useful when you are
debugging dependency conflicts in CI.

#### Executing PyMarkdown

After this step completes, subsequent steps can safely invoke Python commands, including
PyMarkdown, inside the configured environment.

For most projects, a simple PyMarkdown step is enough:

```yaml
  - name: Execute PyMarkdown on Current Docs
    run: pipenv run pymarkdown scan --recurse .
```

The example earlier in this section is more complex because this repository runs
PyMarkdown from its own source code. Our CI must test the latest source, not the
last published release, so we:

- invoke PyMarkdown via `main.py` in the repository root, and
- pass `--config ${{github.workspace}}/clean.json` to use a specific configuration
  file.

You only need this style of invocation if you are developing PyMarkdown itself or
a similar tool.

#### Pre-Commit

Of course, if you use PyMarkdown through Pre-Commit, the GitHub Actions step
that you need is even simpler.

```yaml
  - name: Execute Pre-Commit
    run: |
      pipenv run pre-commit run --all-files
```

Using `--all-files` ensures that Pre-Commit runs on every tracked file in the repository,
which is the most common pattern for CI checks.

#### Further Options

This command covers most common GitHub Actions scenarios. If you need more control,
you can:

- point PyMarkdown at a specific configuration file, and/or
- restrict scanning to particular directories.

For example:

```yaml
  - name: Execute PyMarkdown on Docs with Custom Config
    run: pipenv run pymarkdown --config custom_config.json scan --recurse docs
```

We recommend this sequence:

- Iterate on these options locally.
- Commit your configuration to the repository.
- Update the run command to match your local invocation.

For more information on configuration files and available options, refer to the
[User Guide](./user-guide.md).

### Other CI Systems

Most CI platforms can follow the same sequence you saw in the GitHub Actions example:

1. Check out your repository.
2. Install Python 3.10+.
3. Install Pipenv.
4. Run `pipenv update -d` (or `pipenv sync -d`) to install dependencies.
5. Run PyMarkdown:

   ```bash
   pipenv run pymarkdown scan --recurse .
   ```

For example, in GitLab CI:

```yaml
pymarkdown:
  image: python:3.10
  script:
    - pip install pipenv==2023.12.1
    - pipenv update -d
    - pipenv run pymarkdown scan --recurse .
```
