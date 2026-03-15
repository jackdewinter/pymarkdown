---
summary: How to use the pre-commit tool with the PyMarkdown application.
authors:
  - Jack De Winter
---

# Advanced Pre-Commit

As teams push to ship high‑quality software quickly, the [Pre-Commit](https://pre-commit.com/)
framework and its linters have become a de facto standard. On the project's home
page, the authors describe struggling to add tooling so reviewers can:

> "to focus on the architecture of a change while not wasting time with trivial
> style nitpicks"

The goal is to let you use best‑in‑class linters and formatters regardless of the
language they are written in. When a tool has extra dependencies &mdash; such as
Node.js for a JavaScript linter &mdash; Pre‑Commit installs and manages those dependencies
for you.

Pre‑Commit hooks generally fall into two categories:

- **Checkers:** report problems but do not modify files.
- **Formatters:** rewrite files to follow specific rules.

For example, [PyLint linter](https://github.com/PyCQA/pylint) acts as a checker
and returns a failure code when it finds issues. [Black](https://github.com/psf/black)
is a formatter: it reformats Python files and then reports what it changed.

The PyLint linter is to Python what PyMarkdown is to Markdown. With over a hundred
rules, PyLint checks every line and fails if your code violates its rules.

Black is uncompromising: it always reformats Python files to its standard style.
If it changes even a single character, it reports that change.

Pre‑Commit provides an [exhaustive catalog](https://pre-commit.com/hooks.html) of
checkers and formatters that cover most linting tasks. Because there are so many
options, choosing the right hooks can be daunting at first. PyMarkdown is one of
the available hooks.

## Basic Integration

The [Installing Via Pre-Commit](./getting-started.md#installing-via-pre-commit)
section of the Getting Started guide shows how to configure PyMarkdown as a
Pre‑Commit hook. Rather than repeat that material here, use that section for the
basic setup.

### How Examples Relate to Pre-Commit Environments

Throughout this document, we use command lines prefixed with `pipenv run` in our
examples. That prefix is just a stand-in for the work that Pre-Commit does behind
the scenes:

- Pre-Commit creates a dedicated virtual environment for each hook.
- It installs and runs PyMarkdown inside that environment.

So, when you see:

```bash
pipenv run pymarkdown scan -r .
```

you can mentally read it as "Pre-Commit runs pymarkdown scan -r . in its own virtual
environment."

### What Are Hooks?

In Pre-Commit parlance, a `hook` is usually an external repository with instructions
on how to execute a specific linter through Pre-Commit. Hooks can be created in
any one of [21 languages](https://pre-commit.com/#supported-languages), not including
the `local` hook for running scripts
local to your own system. A single external repository can define multiple hooks,
and many hook repositories use this pattern. This is true of Pre-Commit's
own [hook repository](https://github.com/pre-commit/pre-commit-hooks) which hosts
over 20 hooks in a single repository.

### Creating a Pre-Commit Configuration File

After [installing Pre-Commit](./getting-started.md#installing-via-pre-commit), the
next step is to create a `.pre-commit-config.yaml` file in the repository root.
Pre-Commit always runs hooks from the root and only looks for the configuration
file there; if you place it elsewhere, Pre-Commit will not find it.

A `.pre-commit-config.yaml` file begins with six optional [top-level settings](https://pre-commit.com/#pre-commit-configyaml---top-level),
followed by the `repos` section. For most PyMarkdown setups, you can ignore those
top-level settings and focus on `repos`.

Specifically looking at the `repos` value at the top, a minimal, working configuration
looks like:

```yaml
repos:
  - repo: https://github.com/jackdewinter/pymarkdown
    rev: v0.9.18
    hooks:
      - id: pymarkdown
```

You can add top-level settings later if you need global controls such as default
stages or default language versions.

### Adding the PyMarkdown Hook to `.pre-commit-config.yaml`

To add support for PyMarkdown to the Pre-Commit configuration file, append the
following configuration to
the end of the `.pre-commit-config.yaml` file:

```yaml
  - repo: https://github.com/jackdewinter/pymarkdown
    rev: main
    hooks:
      - id: pymarkdown
```

The hook repository information includes the Git URL and the `rev` to use (branch,
tag, or commit hash). The following `hooks` section names the hooks from that repository.
For this project, we use the hook with `id: pymarkdown`.

#### One Step Further - Pinning the PyMarkdown Version

Even though the above example specifies the `main` branch, our team would like you
to consider changing `main` to a specific tag pointing to the latest build of
PyMarkdown. That practice is called "pinning a version."

Pinning is a slightly more advanced step, but it gives your team explicit control
over when PyMarkdown changes. You must update the tag manually when a new release
comes out, yet in return you decide exactly when to adopt each version.

We work hard to keep changes backwards compatible, but occasional mistakes are unavoidable.
By pinning the version, your team can move to new releases when your team is ready,
instead of treating every update as an urgent change.

To find the tag for the latest release:

1. Open the [Releases page](https://github.com/jackdewinter/pymarkdown/releases).
2. Look for the release with the green `latest` tag.
3. In the sidebar next to that release, copy the tag name (for example, `v0.9.18`).
4. Use that value in your `.pre-commit-config.yaml`:

   ```yaml
      rev: v0.9.18
   ```

#### Checking for Updates

To check for newer PyMarkdown versions and update your hooks automatically, run:

```text
pipenv run pre-commit autoupdate
```

This scans your `.pre-commit-config.yaml` file and updates each hook's `rev` field
to the tag for its latest release. You can either check each hook's repository manually
or run this command periodically.

Our practice is to run this command roughly once a month, test any updated hooks
locally, validate them on all three operating systems, and only then merge into
our `main` branch.

### Telling Pre-Commit Which PyMarkdown Configuration File to Use

This subsection shows how to tell Pre-Commit which PyMarkdown configuration file
to use, whether the file is in the repository root or in a subdirectory.

The details rely on concepts from [Advanced Configuration](./advanced_configuration.md#configuration-file-types).
If you have not read that document yet, it may be useful to review it before continuing.

Although PyMarkdown supports several configuration formats, the examples in this
section use a JSON file named `pymarkdown.json`.

#### Using a Default Configuration File at the Repository Root

The easiest way to use PyMarkdown configuration files is to specify one of the
[default configuration files](https://application-properties.readthedocs.io/en/latest/file-types/#default-configuration-files).
PyMarkdown looks for default configuration files in the current working directory.
Because Pre‑Commit runs hooks from the repository root and does not change directories,
automatic discovery only works when the PyMarkdown configuration file is in the
repository root. In that case, the configuration shown in the previous section is
sufficient.

#### Using a Configuration File in a Subdirectory

If your configuration file is not in the repository root, you must pass it explicitly
as an argument to the PyMarkdown hook.

For example, to use a file named `pymarkdown.json` in the current directory, configure
the hook as:

```yaml
    - id: pymarkdown
      args:
        - --config=pymarkdown.json
        - scan
```

From the [Advanced Configuration](./advanced_configuration.md#configuration-sources-and-layering)
documentation, keep in mind:

- The `--config` argument takes a path relative to the current working directory.
- When Pre-Commit runs, the current working directory is the repository root.
- You should never use absolute paths in `.pre-commit-config.yaml`.

Putting this together, if your `pymarkdown.json` file lives under `docs/src/`, configure
the hook as:

```yaml
    - id: pymarkdown
      args:
        - --config=docs/src/pymarkdown.json
        - scan
```

For portability, do not specify absolute paths to the configuration file in `.pre-commit-config.yaml`.

At this point, you can run PyMarkdown from Pre-Commit with a basic configuration.
Next, we'll look at how to mirror your existing CLI workflows in hooks, refine file
selection, and choose between hook arguments and configuration files.

## Advanced Integration

Once you have a basic PyMarkdown/Pre-Commit integration in place, the next step
is to refine how Pre-Commit calls PyMarkdown.

In this Advanced Integration section, you will:

- Map your existing `pymarkdown` command lines into hook configurations.
- Control which files Pre-Commit passes to PyMarkdown.
- Decide where to put PyMarkdown's configuration (hook args vs config file).

Pre-Commit supports many hooks and configuration patterns, and the
[Configuration Hook Arguments](https://pre-commit.com/#pre-commit-configyaml---hooks)
section covers more options that you typically need. This section focuses only
on the subset that matters for PyMarkdown.

### Pre-Commit 101

Each command line to translate can be broken down into three parts:

1. What to invoke
2. Which files to send to the hook
3. What arguments to use

Given a command like:

```bash
pipenv run pymarkdown --config docs/src/pymarkdown.json scan -r .
```

The translation recipe is:

1. Drop the `pipenv run pymarkdown` part; Pre-Commit handles that.
2. Drop the file-selection part (`-r .`); Pre-Commit handles file selection.
3. Put everything in between into the hook's `args` list.

Minimal equivalent hook:

```yaml
  - repo: https://github.com/jackdewinter/pymarkdown
    rev: main
    hooks:
      - id: pymarkdown
        args:
          - --config
          - docs/src/pymarkdown.json
          - scan
```

The following subsections walk through each of these in turn.
When in doubt, remember:

- If it controls **what** runs → it's part of the hook definition or `id`.
- If it controls **which** files → it belongs in Pre-Commit's filters, not in `args`.
- If it controls **how** PyMarkdown behaves → it belongs in `args` or your config
  file.

#### What To Invoke

The "what to invoke" part of the command line is handled by the hook configuration
in `.pre-commit-config.yaml`. From our example:

```bash
pipenv run pymarkdown scan -r .
```

the part that matters for the hook is `pipenv run pymarkdown scan`. In a hook, that
becomes:

```yaml
    - id: pymarkdown
      args:
        - scan
```

Pre-Commit takes care of environment setup and calling pymarkdown; the hook only
needs to specify the arguments.

#### Which Files To Send

Because of our team's Pre-Commit setup for PyMarkdown, the default behavior of the
**published** `pymarkdown` hook is to pass every Markdown file in the repository
to PyMarkdown. This default is defined in the hook itself as:

```yaml
    - id: pymarkdown
      types: [markdown]
```

In other words, you get `types: [markdown]` automatically when you use the pymarkdown
hook; you do not need to add it to your own `.pre-commit-config.yaml`.

The `types: [markdown]` setting tells Pre-Commit's filter mechanism to send only
files that the identify library classifies as Markdown. In practice, that means
any file with a `.md` extension is passed to PyMarkdown, which matches the effect
of running `pymarkdown scan -r .` on the command line.

For many projects, the default behavior is enough. When you need to focus on specific
directories, exclude generated files, or add non‑`.md` Markdown sources, you will
need more precise control over the file list.

For those cases, these Pre-Commit hook arguments are useful:

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

##### `pass_filenames`

This option, which defaults to `true`, tells Pre-Commit whether to construct a list
of filenames and to pass it to the hook application. This is essentially a big
switch that controls whether the other options in the above list are actioned on.

With the default of `true` for `pass_filenames` and no additional filters in your
`.pre-commit-config.yaml`, Pre-Commit passes to PyMarkdown whatever the hook's own
`types` setting allows. For the published `pymarkdown` hook, that is:

```yaml
    types: [markdown]
```

Note that if you plan on using PyMarkdown's comment-line arguments to control which
files are scanned, as opposed to working with Pre-Commit's arguments, you need to
set `pass_filenames` to `false`, as in:

```yaml
    - id: pymarkdown
      pass_filenames: false
      args:
        - --config
        - clean.json
        - scan
        - .
        - ./docs
```

##### `types`, `types_or`, and `files`

The `types` and `types_or` options filter files based on the types reported by the
Python `identify` package. The `files` option filters filenames using a single regular
expression. Pre‑Commit applies these three filters together: a file must match all
non‑empty filters to be included. If one of these options is left empty, it does
not filter the list.

For example, the PyMarkdown hook sets `types: [markdown]` by default. To restrict
that to only Markdown files in the `/newdocs` directory, add:

```yaml
    - id: pymarkdown
      files: ^newdocs/
```

With both types: [markdown] and `files: ^newdocs/` in effect, Pre-Commit passes
only Markdown files in the `newdocs/` directory to PyMarkdown. In other words, a
file must be both Markdown and located under `newdocs/` to be included.

If you do not work with regular expressions regularly, tools like
[Regular Expressions 101](https://regex101.com/) are helpful when designing the
pattern used in the files argument.

##### `exclude` and `exclude_types`

These options mirror `files` and `types`, but they remove files from the list passed
to the hook. For example, suppose we want to scan all Markdown files under `/newdocs`
except `todo.md`, which we intentionally allow to remain broken.
Using
the `exclude` option, we can
restrict the filename list as follows:

```yaml
    - id: pymarkdown
      files: ^newdocs/
      exclude: ^newdocs/todo\.md$
```

#### What Arguments To Use

The remaining command-line arguments determine how PyMarkdown behaves under Pre-Commit.
In the earlier example in [What To Invoke](#what-to-invoke), the only argument was
`scan`. You can extended this list with options such as `--config`, just as you
would on the command line.

In this example:

```bash
pipenv run pymarkdown --config docs/src/pymarkdown.json scan -r .
```

- Pre-Commit replaces `pipenv run pymarkdown` (see [What To Invoke](#what-to-invoke)).
- Pre-Commit also takes care of `-r .` (see [What Files To Send](#which-files-to-send)).

In `args`, include:

- Flags and options you would normally pass to `pymarkdown` (for example, `--config`,
`--alternate-extension`, `scan` or `fix`).

Do **not** include:

- The `pymarkdown` executable itself or any environment runner (`pipenv run`).
- File or directory arguments when you are relying on Pre-Commit's file selection.

##### Using Configuration Files vs Args

Conceptually, the hook's `args` section should mirror your usual PyMarkdown command
line, excluding the file selection portion. In practice, you can choose between
putting options in `args` or in a configuration file.

A simple rule of thumb:

- Use **configuration files** for project‑wide, long‑lived behavior:
    - Rule Plugin choices and Rule Plugin tuning
    - ignore lists
    - documentation‑tool‑specific settings (for example, MkDocs vs Quarto)
- Use **hook args** for environment‑ or hook‑specific behavior:
    - choosing `scan` vs `fix`
    - pointing to a particular configuration file (for example, `--config=docs/src/pymarkdown.json`)
    - temporary experiments or one‑off options

Keeping most behavior in a configuration file makes it easier to see and review:
a clearly named `pymarkdown.json` or `pymarkdown.yaml` usually sits alongside your
documentation source files, instead of being buried in `.pre-commit-config.yaml`.

##### YAML Forms for Args

Regardless of which options you choose, you must express the hook arguments as a
YAML list inside `.pre-commit-config.yaml`.

YAML supports two equivalent ways to write the same list of arguments:

**Inline list:**

```yaml
    - id: pymarkdown
      args: [--config, docs/src/pymarkdown.json, scan]
```

**Block list:**

```yaml
    - id: pymarkdown
      args:
        - --config
        - docs/src/pymarkdown.json
        - scan
```

Both forms represent the same arguments you would type on the command line. Each
space-separated token (`--config`, `docs/src/pymarkdown.json`, `scan`) becomes a
separate list element. The only requirement is that the `scan` argument appears
at the end.

##### Common Pitfall: Forgetting the `Scan` Command

PyMarkdown requires a command argument (`scan` or `fix`). Without it, the first
filename is misread as a command and the run fails. The default hook uses scan
alone; when you customize `args`, always end the list with a valid command.

## How We Use Pre-Commit in our Pipelines

This section applies the earlier concepts to our own pipelines. It walks through
our PyMarkdown Pre-Commit configuration so you can see how we combine hook arguments,
file selection, and configuration files in a real project.
The relevant portion of our project's own [configuration](https://github.com/jackdewinter/pymarkdown/blob/main/.pre-commit-config.yaml)
is:

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

In the first example, we scan our root directory (specified with `.`)
and our previous `docs` directory (specified with `./docs`) using a simple
configuration in `clean.json`. That `clean.json` configuration file contains
the basic Rule Plugins that apply to most of our repository.

Because the PyMarkdown repository intentionally contains "bad" Markdown for test
cases, we limit scanning to those directories. We set `pass_filenames: false` to
tell Pre-Commit that PyMarkdown will decide which directories to scan, and then
list those directories explicitly after the `scan` argument.

The second example is similar to the first, but uses a different configuration
file and a different directory to scan. Here, we are moving from standard Markdown
documentation in `/docs` to documentation processed by
[MkDocs](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data) and
hosted on [ReadTheDocs](https://pymarkdown.readthedocs.io/en/latest/).

Because MkDocs has different requirements, we keep its settings in a separate
configuration file and scan only the `./newdocs/src` directory with that configuration.

## Things To Watch Out For

Some parts of the Pre-Commit integration with PyMarkdown are not obvious at first.
In this section, we highlight the behaviors that tend to cause confusion and explain
how to handle them.

### Scanning Markdown Files with Alternate Extensions From Pre-Commit

#### The Problem: `.qmd` Files Are Not Being Scanned

A user reported that `.qmd` files were not being scanned by our Pre-Commit hook.
[Quarto](https://quarto.org/docs/get-started/hello/vscode.html) uses `.qmd` files
as Markdown sources, so they should be compatible with PyMarkdown. At first glance,
following our documentation should have been enough to scan these files.

#### Verifying Baseline Behavior with the CLI

We first verified the baseline behavior from the command line:

- Place the user's `test.qmd` and a `README.md` file into a test directory.
- Run PyMarkdown on that directory from the CLI to confirm that `test.qmd` is
  scanned and `README.md` is ignored.
- Introduce simple issues that PyMarkdown can detect into both files and verify
  that it reports only the issues in `test.qmd`.

As we predicted, PyMarkdown detected the issues in the `test.qmd` files but not
the `README.md` file.

#### Translating the Baseline to Pre-Commit

With that simple test completed and passing, we took an independent approach to verify
our user's findings. We started with the example provided in the section
[Adding the PyMarkdown Hook to `.pre-commit-config.yaml`](#adding-the-pymarkdown-hook-to-pre-commit-configyaml):

```yaml
  - repo: https://github.com/jackdewinter/pymarkdown
    rev: main
    hooks:
      - id: pymarkdown
```

Using that example as a base, we applied the logic from the [What Arguments To Use](#what-arguments-to-use)
section. In particular, we added the [--alternate-extensions or -ae](./user-guide.md#-alternate-extensions-or-ae)
flag for the scan action via the hook's args element:

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
as the other two files, we then executed Pre-Commit in that directory. Using our
independent approach, we ended up at the same location as our user, with this response:

```text
Provided file path 'README.md' is not a valid file. Skipping.
```

#### Understanding Why It Fails

The failure occurs because the published PyMarkdown hook configures Pre‑Commit to
pass only Markdown files (`types: [markdown]`). Unless you change that setting,
Pre-Commit sends only `.md` files to PyMarkdown, even if PyMarkdown itself is
capable of handling `.qmd` files.

The root cause is the built‑in `types: [markdown]` setting in the published pymarkdown
hook. Even if you do not specify types in your local `.pre-commit-config.yaml`,
that default still applies.

#### Final Configuration for `.qmd` Files

To ensure that `.qmd` files are passed to PyMarkdown, we made two related changes
to the hook configuration. The first change was adding this element at the same
level as the `args` element:

```yaml
      files: .*\.qmd$
```

This tells Pre-Commit to send any file whose name ends with .qmd:

- `.*` – any characters, any number of times
- `\.qmd` – the literal `.qmd` suffix
- `$` – end of the string

**Tip:** if you do not work with regular expressions regularly, online regex tools
are very helpful when designing the pattern for the files argument.

But that was only half of the solution. Through research, we found that Pre-Commit
processes the `types` filter on eligible files before applying any `files` or `exclude`
filters. Because the published `pymarkdown` hook ships with `types: [markdown]`,
we needed to override that default and replace it with `types: [file]` so our
`files: .*\.qmd$` pattern would be applied. This forces Pre-Commit to collect
all eligible paths, filter that list down to paths that represent files, and then
apply our existing `qmd` file filter to end up with our desired list of Quarto files.
Therefore, we needed to add this element at the same level as the `files` element:

```yaml
      types: [file]
```

We validated this configuration with additional tests and confirmed that it behaves
as described. The configuration
that worked for our user was:

```yaml
  - repo: https://github.com/jackdewinter/pymarkdown
    rev: main
    hooks:
      - id: pymarkdown
        files: .*\.qmd$
        types: [file]
        args:
          - scan
          - --alternate-extension=.qmd
```
