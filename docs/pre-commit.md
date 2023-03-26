# Git Pre-Commit Hooks

Git repositories can take advantage of integration with
the [pre-commit](https://pre-commit.com/) family of
checks and formatters.  There are tons of information
on their website, and if you are using this feature,
we strongly suggest that you read the information at
their site to understand what capabilities you are adding
to your repository before adding this.

Assuming you have read their information or are familiar
with pre-commit hooks, the relevant steps to add this
support are as follows:

## Create a Configuration File

To enable pre-commit hook support in a repository,
the `.pre-commit-config.yaml` file must exist in the
root of that repository and start with the text:

```yaml
default_stages: [commit, push]

repos:
```

## Adding Configuration For PyMarkdown

To specifically add support for PyMarkdown to your
pre-commit hooks, append the following configuration to
the `.pre-commit-config.yaml` file:

```yaml
repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: main
      hooks:
          - id: pymarkdown
```

For a good example of a working `` file, please feel free to look at that file
for any of the PyMarkdown companion projects, as listed below:

- [application_properties](https://github.com/jackdewinter/application_properties/blob/main/.pre-commit-config.yaml)

## Executing The Configuration File

- add on how to add python support locally
- add pointers on pre-commit.io on adding them for CI

## Configuration

Each of the following sections details the pre-commit hook
configuration that is available, and supplies a recommendation
for that configuration value.

### Version of PyMarkdown To Use

When adding a pre-commit hook, you are specifying that you
want to use the code in the specified repository to scan or
format your repository's files.  As repositories have multiple
commits, the pre-commit hook uses the `rev`
value to specify which
[branch or commit](https://pre-commit.com/#pre-commit-configyaml---repos)
to use for the pre-commit check.

In the above section, the `rev` value was set to `main`:

```yaml
repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: main
```

This instructs the pre-commit hooks to use the head commit in
the `main` branch.  Other alternatives are:

```yaml
repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: 0.9.0
```

to use the beta release, tagged with `0.9.0`.  Another possibility
for this value is to specify the exact SHA hash of the commit in the repository.
For the `0.9.0` release, this would be:

```yaml
repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: 47ab4e6e6c57c4187398870ffb9632375975fd64
```

#### Recommendations

The current recommendation is to either set this value
to `main` to pick up the latest changes as they are released,
or `0.9.0` to use the beta release.

### Arguments

The main document has sections (starting with the
[Basic Configuration](https://github.com/jackdewinter/pymarkdown#basic-configuration)
section, dedicated to explaining the various configuration options
available.  All those configuration options are either
specified on the command line or are specified in a configuration
file whose location is specified on the command line.

To add these arguments to the `.pre-commit-config.yaml` file,
locate the `- id: pymarkdown` line in the file and change it
in one of these two ways:

```yaml
repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: main
          - id: pymarkdown
            args: [option1, scan]
```

or:

```yaml
repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: main
      hooks:
          - id: pymarkdown
            args:
                - option1
                - scan
```

where `option1` is one of the specified options.

For arguments that are followed by a specified value, the
argument and the value must be separate `args`, for example
like this:

```yaml
repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: main
      hooks:
          - id: pymarkdown
            args:
                - --disable-rules
                - line-length
                - scan
```

Note that
the default arguments are specified as `[--disable-version,scan]`, instructing
PyMarkdown to perform a scan of any files supplied by the
pre-commit hook without applying any added configuration.
The `--disable-version` flag instructs the application to disable checking
if the current version is the latest version.
Therefore, if any custom arguments are specified, make sure to start the
list with the argument `--disable-version` and end the list with the
argument `scan`.

#### Command Line Arguments Vs Configuration File

As the `.pre-commit-config.yaml` file specifies configuration,
it is possible that any configuration that is needed can be
accomplished using command line arguments.

There are typically four reasons for not using command line arguments for
PyMarkdown:

- conciseness: you prefer to keep any configuration values in a single file
- reusability: you want to reuse those values in other locations, such as scripts
- simplicity: you want to do more complicated configuration without specifying tens of command line options
- single responsibility: you only want pre-commit hook configuration in the file, everything else goes elsewhere
- catch-all: because

If any of those reasons are applicable, then the `args` section
of the `.pre-commit-config.yaml` file should look like this:

```yaml
repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: main
      hooks:
          - id: pymarkdown
            args:
                - --config=.pymarkdown.json
                - scan
```

with a configuration file named `.pymarkdown.json` in the root of
your repository.  With this configuration, all configuration values
will be taken from the supplied JSON file.  Unless there is a change
to the files to be scanned, the PyMarkdown section of the
`.pre-commit-config.yaml` file will never be changed again.

### Enabling or Disabling Rules

As rules can be enabled or disabled on the command line, rules can also be enabled
or disabled in the `.pre-commit-config.yaml` file.

```yaml
repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: main
      hooks:
          - id: pymarkdown
            args:
                - -d
                - MD041,md013
                - scan
```

Note that if presenting the arguments on a single line and there are multiple rules
that are being enabled or disabled, the commma separated list must be enclosed in
quotes.  The quote characters allow Pre-Commit to understand that the comma inside
of the quotes is part of the data, not a character separating the data.

```yaml
repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: main
      hooks:
          - id: pymarkdown
            args: [-d, "MD041,MD013", scan ]
```

### Files To Scan

The pre-commit hooks pass in any files in the repository that match
the specified file types.  For the PyMarkdown project, this value
is set to `markdown`.  By default, this instructs the pre-commit
hooks to can any Markdown file in the commit with PyMarkdown.  The pre-commit
hooks section on [file filtering](https://pre-commit.com/#filtering-files-with-types)
is thorough and should be used as a reference.

The more useful pieces of information from there are as follows.

#### Use Of Regular Expressions

The configuration file specifies both the `exclude` value and the `files`
as regular expressions.  The pre-commit hooks apply these filters to any file names,
using the base of the repository as the root of the file name.
When I cannot create simple expressions in my head, I find
that the site [Regular Expressions 101](https://regex101.com/)
is helpful in getting me to the correct regular expression for my needs.

For example, to specify all the file names in the `docs` directory,
set the value to the regular expression `^docs/`.  If the leading
`^` character is omitted, then any `docs` directory in the repository
would be specified.

#### Including and Excluding Files

Including files into the list of files to scan is accomplished
using the `files` value.  Excluding files from that same list
is conducted using the `exclude` value.  This can be helpful
in narrowing down the list of files to scan.

A simple example of this is the following configuration:

```yaml
repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: main
      hooks:
          - id: pymarkdown
            exclude: ^docs/todo\.md$
            files: ^docs/
```

That configuration instructs the pre-commit hooks to pass
any Markdown files (default) that have a path starting with
`docs/` and do not have a path of exactly `docs/todo.md`.
There is nothing preventing the `exclude` value from
filtering on more than one file.  But because of the
regular expression **start of string** anchor (`^`) and
**end of string** anchor (`$`) and no wildcards between
them, that regular expression can only have one match.

#### An Alternative: Using the Command Line

While not as flexible as Pre-Commit in specifying the files to scan, sometimes
it is just easier to use the command line to specify what to scan.  A good example
is the project's own [configuration](../.pre-commit-config.yaml) with the following
configuration:

```yaml
repos:
  - repo: https://github.com/jackdewinter/pymarkdown
    rev: v0.9.9
    hooks:
      - id: pymarkdown
        pass_filenames: false
        args:
          - --config
          - clean.json
          - scan
          - .
          - ./docs
```

In this case, there are two directories with Markdown to publish that need scanning
and a whole lot of other directories that should not be scanned as they contain
examples of bad Markdown.  Because of this, the configuration explicitly follows
the `scan` argument with `.` for the base project directory and `./docs` for the
documents directory.

The effect of this configuration is that only the `.` and `./docs` directory are
scanned.  However, Pre-Commit automatically appends any eligible file names to the
end of the list of arguments.  As none of the methods from the previous sections
are used to limit that list of files, they are all sent.  As that behavior is not
desired, the `pass_filenames: false` specifier is used.  That specifier instructs
Pre-Commit to not append any file names to the list of arguments. It essentially
informs Pre-Commit: "It's okay, we can do it ourselves."
