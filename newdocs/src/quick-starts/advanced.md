# Quick Start: Fast Path for Experienced Python Users

This page is a focused, opinionated path to get PyMarkdown installed and scanning
a project quickly. It assumes you already know Python, the command line, and packaging
tools, and you just want to see PyMarkdown running on your code &mdash; without reading
all the docs first.

This is **not** a complete guide. It is a fast run through our Quick Start pages
with the single goal of getting you scanning Markdown as quickly as possible.

If you prefer more explanation, screenshots, or step‑by‑step troubleshooting, use
the links in each **"Running Into Trouble?"** box to jump into the longer guides.

## Is This Guide Right For You?

Ready for a quick "jog" through the installation and example process?
**If so**, this guide is for you.

**If you are not sure if you are ready**, please go to our [Quick Start: Introduction](./index.md)
page. No harm, no foul. We would rather you have a good experience being
introduced to PyMarkdown than be frustrated and giving up on it!

## TL;DR: Fastest Path

If you just want the absolute shortest path to see PyMarkdown work:

```sh
# Install globally
pip install pymarkdownlnt

# Or with Pipenv
pipenv install pymarkdownlnt

# Run once on a sample file
echo -e "# First Heading\n# Another First Heading" > sample.md
pymarkdown scan sample.md
```

Continue reading for explanations and additional options.

- **If the commands above worked**, you can safely skip to:
    - [Pre‑Commit](#pre-commit) if you want to enforce checks on every commit, or
    - [Scan Mode](#scan-mode) to learn how to scan your own files and directories.
- **If they did not work**, read [Prerequisites](#prerequisites) and [Installation](#installation)
  in order.

### Page Overview

This guide is organized as:

1. [Prerequisites](#prerequisites) – skim to confirm assumptions.
2. [Installation](#installation) – jump here for install commands.
3. [Pre‑Commit](#pre-commit) – jump here if you already use pre-commit.
4. [Scan Mode](#scan-mode) – run scans and read the output.
5. [Further Reading](#further-reading) – more configuration and features.

## Prerequisites

Unlike our other Quick Start pages, where we try and keep things as simple as
possible for all users, this page assumes the following:

- comfortable using the command line in your favorite shell and
  understanding commands like "go to your project root directory and run this"
- Python 3.10+ is installed and available on your `PATH`
- knowledge of whether you need to use a **Python package manager** like Pipenv
  to install PyMarkdown, and if you want to install it as a **development-only dependency**
- if you plan to install PyMarkdown via Pre-Commit, basic usage and configuration
  of Pre-Commit

## Installation

### Command Line

Enter one of the following commands at the command line:

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

If you are using Pipenv as your **Python package manager** and would like
to install PyMarkdown as a **development-only dependency**, use the following
command line instead of the one above:

<!-- pyml disable code-block-style-->
```sh
pipenv install -d pymarkdownlnt
```
<!-- pyml enable code-block-style-->

When using a Python package manager other than Pipenv, consult that tool's docs
for adding a dependency. For example:

```sh
# Poetry
poetry add --dev pymarkdownlnt

# uv
uv add --dev pymarkdownlnt
```

In general, the command is of the form:

```sh
<package-manager> add/install [--dev] pymarkdownlnt
```
<!-- pyml enable code-block-style-->

#### Troubleshooting: Installation

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Quick checks**

Before jumping to other docs, verify:

1. `python --version` shows Python 3.10 or higher.
2. `pip show pymarkdownlnt` (or `pipenv graph | grep pymarkdownlnt`) shows
   the package installed.

<!-- pyml disable-next-line no-emphasis-as-heading-->
**More help**

If those checks still fail:

- See [Install PyMarkdown Locally](./installation.md#install-pymarkdown-locally)
  for a **step‑by‑step, environment‑focused install guide**.
- See [Installing PyMarkdown](../getting-started.md#installing-pymarkdown) for
  **virtualenvs, CI setups, and other advanced install scenarios**.

### Pre-Commit

Here you will integrate PyMarkdown into your existing Pre-Commit workflow so that
Markdown checks run automatically with your other project hooks.

Locate the `.pre-commit-config.yaml` file in the root of your project
directory and add the following content under the `repos:` heading. Pin `rev` to
the latest tagged release:

```yaml
- repo: https://github.com/jackdewinter/pymarkdown
  rev: v0.9.36 # replace with the latest tag
  hooks:
    - id: pymarkdown
```

After that, you can run PyMarkdown manually via Pre‑Commit with
`pre-commit run --all-files` to verify that your `.pre-commit-config.yaml` file
change is working properly.

#### Troubleshooting: Pre-Commit

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Quick checks**

First, verify:

1. `pre-commit --version` runs successfully.
2. `pre-commit run --all-files` shows the `pymarkdown` hook in the output (even
   if it fails).

<!-- pyml disable-next-line no-emphasis-as-heading-->
**More help**

If the hook still doesn't run or isn't listed:

- Use [Install PyMarkdown Through Pre‑Commit](./installation.md#install-pymarkdown-through-precommit)
  for a **copy‑paste `.pre-commit-config.yaml`** that is known to work.
- Use [Installing Via Pre‑Commit](../getting-started.md#installing-via-pre-commit)
  for **custom hooks, multiple repos, or complex Pre‑Commit setups**.

## Scan Mode

This section shows you how to:

- [Create A Sample File To Scan](#step-1-create-samplemd)
- [Perform A Scan Of That File](#step-2-scan-the-file)
- [Verify The Scan's Output Is Correct](#step-3-verify-the-output)
- [Learn To Read PyMarkdown's Output Format](#step-4-read-rule-failures)
- [Perform A Scan Of A Directory](#step-5-scan-a-directory)

### Step 1: Create `sample.md`

In a directory of your choice, create a file named `sample.md` with the contents:

```text
# First Heading
# Another First Heading
```

### Step 2: Scan the File

Enter one of the following commands at the command line:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan sample.md
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan sample.md
    ```

<!-- pyml enable code-block-style-->

### Step 3: Verify The Output

You should see output similar to:

```text
sample.md:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```

- The file name may differ.
- Expect three failures with Rule Plugin IDs `MD022` and `MD025`.
- If you see no failures, double‑check that sample.md matches [Step 1](#step-1-create-samplemd).
- If the format looks very different, see [Verifying PyMarkdown Installation](./installation.md#verifying-pymarkdown-installation).

### Step 4: Read Rule Failures

Each line is a single rule failure, using a familiar linter format:

`file-name:line:column: rule-id: description {extra-information} (aliases)`

Breaking that into parts:

- `file-name:line:column:` informs us **which file** caused the Rule Failure and
  **where in the file** the Rule Failure occurred
- `rule-id` is the **primary identifier** of the check reporting the Rule Failure
- `description` is a **human-readable description** of the Rule Failure
- `aliases` are one or more **alternate identifiers** (short, human‑readable names)
  that can be used in place of the **primary identifier**
- `extra-information` is optionally provided to give **additional context** about
  the Rule Failure where needed

If you want a field‑by‑field breakdown of this format, see the [Rule Failure format](../user-guide.md#rule-failure-format)
section.

#### Quick mental model

- Left‑hand side (`file-name:line:column:`) → "where the problem is".
- Middle (`rule-id: description`) → "what Rule Plugin fired and why".
- Right‑hand side (`{extra-information} (aliases)`) → "extra details and alternate
  names".

### Step 5: Scan A Directory

Pick a directory that contains one or more Markdown files (for example, the directory
where you created `sample.md`).

Replace `{directory}` below with either a relative path (such as `.`) or an absolute
path:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan {directory}/
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan {directory}/
    ```

<!-- pyml enable code-block-style-->

To scan `{directory}` and all subdirectories, add `--recurse`:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan --recurse {directory}/
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan --recurse {directory}/
    ```

<!-- pyml enable code-block-style-->

### What You Can Do Now

After completing Steps 1–5, you can:

- create and scan a sample Markdown file,
- interpret PyMarkdown's output, and
- scan a directory (recursively if needed).

From here, jump to [Further Reading](#further-reading) for more advanced usage.

### Troubleshooting: Scanning

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Quick checks**

If `pymarkdown` is not found:

- See [Verifying PyMarkdown Installation](./installation.md#verifying-pymarkdown-installation)
  for **PATH and venv checks**.

If the scan runs but the output is confusing:

- See [How PyMarkdown Reports Rule Failures](./index.md#how-pymarkdown-reports-rule-failures)
  for a visual breakdown.
- See [Basic Scanning](../user-guide.md#basic-scanning) and [Rule Failure Format](../user-guide.md#rule-failure-format)
  for all flags and output options.

<!-- pyml disable-next-line no-emphasis-as-heading-->
**More help**

After you understand the basic output, experienced users often want to:

<!-- pyml disable no-emphasis-as-heading-->
- **Filter or target files** → see [Basic Scanning](../user-guide.md#basic-scanning)
  for globbing and excludes.
- **Integrate into CI** → see [User Guide – Basic Scanning](../user-guide.md#basic-scanning)
  for non‑interactive usage examples.
<!-- pyml enable no-emphasis-as-heading-->

## Further Reading

By following this quick start, you should now be able to install PyMarkdown and
scan Markdown files on your system.

Once you are comfortable scanning Markdown files:

- If you want **PyMarkdown to fix what it can automatically**, see
  [Automatically Fix Certain Rule Failures](./fixing.md).
- If you want **fewer or different checks**, see
  [Rule Plugins: Enabling/Disabling Rules](./rules.md).
- If you need **extra Markdown features** (e.g., tables, math), see
  [Common PyMarkdown Extensions](./extensions.md).

For a full reference of commands and options:

- Start with the [User Guide](../user-guide.md), especially:
    - [Scanning options](../user-guide.md#basic-scanning)
    - [Fixing options](../user-guide.md#basic-fixing)
    - [Configuration basics](../user-guide.md#basic-configuration)
