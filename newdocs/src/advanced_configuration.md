---
summary: More information on configuration and how to apply it.
authors:
  - Jack De Winter
---

# Advanced Configuration

Configuration is how applications handle command-line options, enable features,
and set their values. Early in PyMarkdown's development, we decided to build our
own configuration system that is both reliable and flexible.

## A Note To Begin With

The base documentation for [`application_properties`](https://application-properties.readthedocs.io/en/latest/getting-started/)
was originally adapted from this document. That library now hosts the generic configuration
concepts, while this page explains how they are used in PyMarkdown. Moving the generic
material there let us refine it for broader use while keeping this page focused
on PyMarkdown users.

## Why this Matters

Some users rely mostly on defaults or a few command‑line tweaks. Others experiment
with extensions, Rule Plugins, and settings on the command line, then capture what
works
in configuration files. The rest of this page shows how to combine those approaches
and use PyMarkdown's configuration effectively.

## Skipping Ahead

From this point on, we use the same basic terminology as the `application_properties`
module: configuration item keys (like `log.level`), configuration item values (such
as `INFO`), and configuration sources (command line and configuration files). If
you'd like a more formal definition of these terms, see the module's
[nomenclature section](https://application-properties.readthedocs.io/en/latest/getting-started/#nomenclature),
but it isn't required to follow this document.

To help you either explore configuration concepts or look up specific topics, here
is a roadmap of what this page covers:

- [Configuration File Types](#configuration-file-types)
- [Configuration Sources and Layering](#configuration-sources-and-layering)
- [Set command](#set-command)
- [Strict Configuration Mode](#strict-configuration-mode)
- [Available Configuration Items](#available-configuration-items)
- [Choosing Between Command Line and Configuration Files](#choosing-between-command-line-and-configuration-files)

If a topic isn't listed explicitly, look for nearby categories &mdash; for example,
Rule Plugin configuration is under "Available Configuration Items." Your browser's
page search can also help you find specific keys or terms.

## Configuration File Types

PyMarkdown reads configuration from JSON, YAML, and TOML files via the
[`application_properties`](https://github.com/jackdewinter/application_properties)
package. This document assumes you are comfortable with at least one of these formats.

At a high level:

- JSON/JSON5 uses a single top‑level object with sections like system, log, plugins,
  and extensions.
- YAML uses nested mappings with the same keys.
- TOML uses a `[tool.pymarkdown]` table and dotted keys (for example, `log.level`
  and `plugins.MD013.enabled`).

For full parsing details, see
[Configuration File Types](https://application-properties.readthedocs.io/en/latest/file-types/#configuration-file-types).
The examples below are sufficient for most PyMarkdown configurations.

### Examples

Each of the three file types is presented on its own tab with the same information:

- the names for implicitly loaded configuration files of that type
- suggested names for the explicitly loaded configuration files that use the `--config`
  command-line argument
- a code block with an example configuration file in the specified format

Even though these three files use different formats, they provide identical configuration
data to PyMarkdown. Scenario tests (prefixed with `test_markdown_documentation_advanced_configuration_`)
verify this for each release.

<!-- pyml disable code-block-style-->
=== "JSON"

    **NOTE:** To maintain parity with the other file types, we use a JSON5 parser that allows for inline comments.

    Valid file names for JSON files are:

    - implicitly loaded: `.pymarkdown` in current directory
    - explicitly loaded with `--config`: `anything`, `anything.json`

    ```json
    {
        // Do not allow any files starting with `draft-`
        "system" : {
            "exclude_path" : "draft-*.md"
        },
        "extensions": {
            "markdown-tables": {
                "enabled" : true
            }
        },
        "plugins": {
            "MD013": {
                "enabled": true,
                "line_length": 100
            }
        }
    }
    ```

=== "YAML"

    Valid file names for YAML files are:

    - implicitly loaded: `.pymarkdown.yml` and `.pymarkdown.yaml` in current directory
    - explicitly loaded with `--config`: `anything`, `anything.yml`, `anything.yaml`

    ```yaml
    # Do not allow any files starting with `draft-`
    system:
      exclude_path: "draft-*.md"
    extensions:
      markdown-tables:
        enabled: true
    plugins:
      MD013:
        enabled: true
        line_length: 100
    ```

=== "TOML"

    Valid file names for TOML files are:

    - implicitly loaded: `pyproject.toml` in current directory
    - explicitly loaded with `--config`: `anything`, `anything.toml`

    ```toml
    [tool.pymarkdown]

    # Do not allow any files starting with `draft-`
    system.exclude_path = "draft-*.md"

    extensions.markdown-tables.enabled = true

    plugins.MD013.enabled = true
    plugins.MD013.line_length = 100
    ```

<!-- pyml enable code-block-style-->

When `--config` is given a file whose extension is not `.json`, `.yaml`, `.yml`,
or `.toml`,
`application_properties` tries the formats in order: JSON, then YAML, then TOML.
This allows extensionless or custom‑named files (such as `anything`) to work without
an explicit extension.

### Need More Information

For a deeper explanation of how we evaluate these file types, refer to the `application_properties`
[Configuration File Types](https://application-properties.readthedocs.io/en/latest/file-types/)
documentation.

### Which One Is Best - Addendum for PyMarkdown

In the original documentation, we made the following observation:

> If comments are important to you, then JSON is out.

However, starting with PyMarkdown version `0.9.32` (and `application_properties`
version `0.9.0`), JSON5 support allows comments in JSON files. This feature is enabled
by default. (See [this section](./user-guide.md#-no-json5-configuration) for more
details.)

In practice, there is no single "best" format &mdash; use what fits your team:

- **JSON/JSON5**: stricter and more explicit; good if you want a rigid structure.
- **YAML**: more flexible and forgiving; good if you value readability and brevity.
- **TOML**: a good fit if you already use `pyproject.toml` and want to keep everything
  together.

Most teams are well served by either JSON5 or YAML. If your needs change, it's easy
to convert between formats.

## Configuration Sources and Layering

Most users configure PyMarkdown through command‑line arguments only.

Other users combine multiple configuration sources. For example, they might:

- use an implicit `.pymarkdown` file in the project root for defaults
- pass `--config newdocs.json` to adjust settings in certain subdirectories
- use `--set` for temporary overrides before committing them to a file

PyMarkdown applies these sources in order: earlier sources provide defaults; later
sources override them. This means:

- a `pyproject.toml` setting can be overridden by a local `.pymarkdown` file,
- which can be overridden by a `--config` file,
- which can be overridden by `--set` values,
- which can be overridden by explicit command‑line flags like `--log-level`.

For the exact ordering and override rules used by the configuration library, see
`application_properties`' [Configuration Ordering](https://application-properties.readthedocs.io/en/latest/getting-started/#configuration-ordering-layering).

## Set Command

PyMarkdown provides command-line arguments like `--enable-rule` to enable a given
Rule Plugin. These are [syntactic sugar](https://en.wikipedia.org/wiki/Syntactic_sugar):
most of them are shortcuts for using `--set` directly.

The `--set` argument is followed by another argument in the form of:

<!-- pyml disable code-block-style-->
```text
<configuration item key>=<optional format prefix><configuration item value>
```
<!-- pyml enable code-block-style-->

For example, the `--log-level` argument (described in the ["Logs" section](#logs))
is syntactic sugar for setting the `log.level` configuration item, which controls
the minimum log level. Assuming the second argument is a valid value like `INFO`,
you can achieve the same effect with this `--set` usage:

<!-- pyml disable code-block-style-->
```sh
--set `log.level=INFO`
```
<!-- pyml enable code-block-style-->

In this example, you substitute `log.level` for `<configuration item key>` and `INFO`
for `<configuration item value>`.

On the command line, everything starts as text, but configuration items expect strings,
integers, or booleans. By default, values are treated as strings. To distinguish
values that look numeric from true integers
or booleans, `--set` uses an optional format prefix:

| Prefix | Type | Examples |
| -- | -- | -- |
| (None) | String | `abc` |
| `$#` | Integer | `$#1` or `$#-1` |
| `$!` | Boolean | case-insensitive `$!true`, anything else is false |

For example, skipping ahead a bit to the next section on "Strict Configuration
Mode", that configuration item requires a boolean value, and can be set using the
`--set` command using the following format:

<!-- pyml disable code-block-style-->
```sh
--set `mode.strict-config=$!True`
```
<!-- pyml enable code-block-style-->

## Strict Configuration Mode

When configuration values are wrong, different systems behave differently. Some
silently fall back to defaults; others raise errors immediately.

PyMarkdown supports both approaches via `mode.strict-config`.

- When mode.strict-config is false (the default, when `--strict-config` is not used),
  PyMarkdown ignores configuration errors and uses defaults, allowing runs to complete
  even with bad configuration.
- When mode.strict-config is true (or `--strict-config` is specified), any configuration
  error is reported, and PyMarkdown stops with an explanatory message.

**Note:** You can adjust the "stop on error" behavior with
[Continuing on Errors](#continuing-on-errors). With `mode.strict-config=true`, configuration
errors are still detected and reported, but `--continue-on-error` causes PyMarkdown
to log them and continue scanning instead of stopping. Use this combination carefully:
runs may complete with incorrect or partial results if your configuration is wrong.

## Available Configuration Items

The available configuration items are grouped into:

- [General - `mode.*` + command line](#general) - Global settings.
- [Logs - `log.*`](#logs) - Settings that affect how logging works.
- [System - `system.*`](#system) - Settings that affect the entire system.
- [Rule Plugins - `plugins.*` + command line](#rule-plugins) - Settings that affect
  the various Rule Plugins.
- [Extensions - `extensions.*`](#extensions) - Settings that affect the various
  extensions.
- [Other - command line](#other) - Settings that do not fit into other categories.

Each area starts with a table of items, followed by brief explanations and examples
in all supported formats (command line, `--set`, JSON, YAML, and TOML). Where relevant,
the table links to more detailed documentation in the User's Guide or elsewhere.

### General

These items directly affect the collection of configuration values and how they
are interpreted.

<!-- pyml disable-num-lines 5 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| [(see Configuration File Types)](#configuration-file-types) | `--config {file}`           | String    | Path to the configuration file to use. |
| [(see Set Command)](#set-command)                           | [`--set {key}={value}`](./user-guide.md#-set-configuration) | String    | Manually set an individual configuration property. |
| [`mode.strict-config`](#strict-configuration-mode)          | [`--strict-config`](./user-guide.md#-strict-config-configuration) | Boolean   | Throw an error if the configuration is bad, instead of assuming default values. (Default: `false`) |

These items recap configuration options covered earlier; use the links in the first
column to jump to the detailed explanations.

### Logs

These items affect the logging for PyMarkdown.

<!-- pyml disable-num-lines 5 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| `log.file`        | [--log-file](./user-guide.md#-log-level-with-log-file-logging) | String  | Destination file for log messages. |
| `log.level`       | [--log-level](./user-guide.md#-log-level-with-log-file-logging) | String | Minimum level required to log messages. Valid values are: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, or `DEBUG`. (Default: `WARNING`)  |
| `log.stack-trace` | [--stack-trace](./user-guide.md#-stack-trace-error-reporting) | Boolean | When enabled, prints a stack trace on errors and sets initial logging (config processing) to debug. (Default: `false`) |

#### Basic Logging

These configuration values control how PyMarkdown logs information. The `log.file`
and `log.level` configuration items are straightforward: they set the log level
and control whether messages are written to a file or to standard output (stdout).

<!-- pyml disable code-block-style-->
=== "Command Line"
    ```sh
    --stack-trace --log-file logs/my.log --log-level INFO
    ```
=== "--set Argument"
    ```sh
    --set 'log.stack-trace=true' --set 'log.file=logs/my.log' --set 'log.level=INFO'
    ```
=== "JSON"
    ```json
    {
      "log": {
        "stack-trace": true,
        "file": "logs/my.log",
        "level": "INFO"
      }
    }
    ```
=== "YAML"
    ```yaml
    log:
      stack-trace: true
      file: "logs/my.log"
      level: "INFO"
    ```
=== "TOML"
    ```toml
    [tool.pymarkdown]
    log.stack-trace = true
    log.file = "logs/my.log"
    log.level = "INFO"
    ```
<!-- pyml enable code-block-style-->

#### Stack Traces

The `log.stack-trace` configuration item (and `--stack-trace` flag) enables a stack
trace whenever an error occurs. This is mainly intended for debugging. Because the
configuration manager is initialized early in startup, enabling this flag also turns
on debug-level logging from startup until configuration is fully loaded, so you
see any errors that occur during initialization.

### System

These items configure PyMarkdown's system‑level behavior:

<!-- pyml disable-num-lines 3 line-length-->
| Key | Command Line | Type | Description |
| --- | --- | --- | --- |
| `system.exclude_path` | [`--exclude`](./user-guide.md#-e-exclude-path_exclusions) | String | Comma separated list of relative glob paths to exclude. |

#### Excluding Paths

The `system.exclude_path` configuration item (and its command-line equivalent)
lets you scan a path while excluding one or more glob patterns in a comma-separated
list. It is supported both on the command line and in configuration files (see
[issue 1462](https://github.com/jackdewinter/pymarkdown/issues/1462) for the original
request).

<!-- pyml disable code-block-style-->
=== "Command Line"
    ```sh
    --exclude draft_*.md --exclude draft-*.md
    ```
=== "--set Argument"
    ```sh
    --set 'system.exclude_path=draft_*.md,draft-*.md'
    ```
=== "JSON"
    ```json
    {
      "system": {
        "exclude_path": "draft_*.md,draft-*.md"
      }
    }
    ```
=== "YAML"
    ```yaml
    system:
      exclude_path: "draft_*.md,draft-*.md"
    ```
=== "TOML"
    ```toml
    [tool.pymarkdown]
    system.exclude_path = "draft_*.md,draft-*.md"
    ```
<!-- pyml enable code-block-style-->

### Rule Plugins

These items show the various ways of enabling and disabling Rule Plugins on a global
level:

<!-- pyml disable-num-lines 6 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| *special* | [--enable-rules,-e](./user-guide.md#enabling-and-disabling-rule-plugins)   | String    | Comma separated list of Rule Plugins to enable. |
| *special* | [--disable-rules,-d](./user-guide.md#-enable-rules-disable-rules-rule-plugins)  | String    | Comma separated list of Rule Plugins to disable. |
| [`plugins.selectively_enable_rules`](#selectively-enable-rule-plugins) | -- | Boolean | Specify whether to enable selective enable mode. |
| [`per-file-plugins.ignores`](#per-file-disabling-of-rule-plugins) | -- | Nested | Specify glob paths to match, and Rule Plugins to disable if matched. |

This item points to the Development documentation with instructions for creating
your own plugins:

<!-- pyml disable-num-lines 3 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| [`plugins.additional_paths`](./development.md) | --add-plugin     | String    | Path to a plugin containing a new Rule Plugins to load. |

These items give examples on how specific configuration items can be applied to
Rule Plugins:

<!-- pyml disable-num-lines 4 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| [`plugins.{id}.enabled`](#specific-plugin-settings) | -- | Boolean | Specify whether the Rule Plugin is enabled. |
| [`plugins.{id}.other`](#specific-plugin-settings) | -- | Various | Specify other configuration properties specific to the Rule Plugins. |

For more on plugin behavior (including per‑file suppression and advanced options),
see [Advanced Rule Plugins](./advanced_plugins.md).

#### Enabling/Disabling Rule Plugins

Rule Plugins can be enabled or disabled either through the command line or by using
a configuration file. On the command line, you can use the `--enable-rules` and
`--disable-rules` arguments to specify a comma-separated list of Rule Plugin identifiers
to enable or disable, with the `--set` command available if needed. If you prefer
to manage plugin settings through a configuration file, you can enable Rule Plugins
in the configuration file by setting their `enabled` configuration item to `true`,
as shown in the following examples.

<!-- pyml disable code-block-style-->
=== "Command Line"
    ```sh
    --enable-rules MD013
    # OR
    -e MD013
    ```
=== "--set Argument"
    ```sh
    --set 'plugins.MD013.enabled=$!True'
    ```
=== "JSON"
    ```json
    {
      "plugins": {
        "MD013": {
          "enabled": true
        }
      }
    }
    ```
=== "YAML"
    ```yaml
    plugins:
      MD013:
        enabled: true
    ```
=== "TOML"
    ```toml
    [tool.pymarkdown]
    plugins.MD013.enabled = true
    ```
<!-- pyml enable code-block-style-->

**NOTE:** These examples enable a Rule Plugin. To disable instead, either set the
configuration value to `false` or, on the command line, use `--disable-rules` or
`-d` rather than `--enable-rules` or `-e`.

##### Selectively Enable Rule Plugins

In some situations, you may want to apply only a minimal set of Rule Plugins to
your Markdown
documents. This configuration item enables this selective mode. When set to `True`,
all Rule Plugins are disabled by default, allowing you to explicitly enable only
the Rule Plugins
you want to use. A command-line shortcut, `-d "*"`, is available to disable all
Rule Plugins from the command line.

For instance, if you want PyMarkdown to apply only Rule Plugin `MD007` to a group
of documents,
you would use the following configuration:

<!-- pyml disable code-block-style-->
=== "Command Line"
    ```sh
    --disable-rules "*"
    ```
=== "--set Argument"
    ```sh
    --set 'plugins.selectively_enable_rules=$!True' --set 'plugins.MD007.enabled=$!True'
    ```
=== "JSON"
    ```json
    {
      "plugins": {
        "selectively_enable_rules": true,
        "MD007": {
          "enabled": true
        }
      }
    }
    ```
=== "YAML"
    ```yaml
    plugins:
      selectively_enable_rules: true
      MD007:
        enabled: true
    ```
=== "TOML"
    ```toml
    [tool.pymarkdown]
    plugins.selectively_enable_rules = true
    plugins.MD007.enabled = true
    ```
<!-- pyml enable code-block-style-->

With this configuration, all Rule Plugins are disabled except for `MD007`, regardless
of
the system's default Rule Plugins settings.

##### Per-File Disabling Of Rule Plugins

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Available: Version 0.9.36**

In some cases, you may have a base configuration that enables or disables Rule Plugins
at the project level, but you still need to disable certain Rule Plugins for specific
files.
The `plugins.per-file-ignores` configuration item takes inspiration from the
[Flake8 linter](https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-per-file-ignores)
and the [Ruff linter](https://docs.astral.sh/ruff/settings/#lint_per-file-ignores),
in being able to disable the Rule Plugins belonging to a comma-separated set of
identifiers associated with one ore more matching
paths.

The file paths are specified using the same glob-based syntax as `.gitignore` files
used with the [`--respect-gitignore` command-line argument](./user-guide.md#-respect-gitignore)
and the [`--exclude` command-line argument](./user-guide.md#-e-exclude-path_exclusions).
This feature is strictly for disabling Rule Plugins. It does not enable Rule Plugins
that are
currently disabled.

<!-- pyml disable code-block-style-->
=== "Command Line"
    Not Available
=== "--set Argument"
    Not Available
=== "JSON"
    ```json
    {
        "plugins": {
            "per-file-ignores": {
                "changelog/*.md": "MD013,MD041"
            }
        }
    }
    ```
=== "YAML"
    ```yaml
    plugins:
      per-file-ignores:
        changelog/*.md: "MD013,MD041"
    ```
=== "TOML"
    ```toml
    [tool.pymarkdown]
    plugins.per-file-ignores."changelog/*.md" = "MD013,MD041"
    ```
<!-- pyml enable code-block-style-->

#### Adding Rule Plugins

You can add additional Rule Plugins either temporarily or permanently. For temporary
evaluation, the recommended approach is to use the `--add-plugin` command-line
argument for each plugin you want to add, with each argument followed by the path
to the plugin file. If you want a more permanent setup, use the `plugins.additional_paths`
configuration value with a comma‑separated list of plugin paths. This works well
for both one‑off experiments and long‑term setups.

<!-- pyml disable code-block-style-->
=== "Command Line"
    ```sh
    --add-plugin /path/to/plugin1.py --add-plugin /path/to/plugin2.py
    ```
=== "--set Argument"
    ```sh
    --set 'plugins.additional_paths=/path/to/plugin1.py,/path/to/plugin2.py'
    ```
=== "JSON"
    ```json
    {
      "plugins": {
        "additional_paths": "/path/to/plugin1.py,/path/to/plugin2.py"
      }
    }
    ```
=== "YAML"
    ```yaml
    plugins:
      additional_paths: "/path/to/plugin1.py,/path/to/plugin2.py"
    ```
=== "TOML"
    ```toml
    [tool.pymarkdown]
    plugins.additional_paths = "/path/to/plugin1.py,/path/to/plugin2.py"
    ```
<!-- pyml enable code-block-style-->

For more information regarding creating your own Rule Plugin, consult our
[Developer Guide](./development.md).

#### Specific Plugin Settings

Each Rule Plugin uses its own configuration namespace under `plugins.{rule-id}`.
The primary boolean `plugins.{id}.enabled` determines whether the Rule Plugin is
active, where
`{rule-id}` is the Rule Plugin's identifier. Additional settings for that Rule Plugin
are also stored
under `plugins.{rule-id}.`, so each plugin's options are grouped together.

<!-- pyml disable code-block-style-->
=== "Command Line"
    Not Applicable
=== "--set Argument"
    ```sh
    --set 'plugins.MD013.enabled=$!True' --set 'plugins.MD013.line_length=$#150'
    ```
=== "JSON"
    ```json
    {
      "plugins": {
        "MD013": {
          "enabled": true,
          "line_length" : 150
        }
      }
    }
    ```
=== "YAML"
    ```yaml
    plugins:
      MD013:
        enabled: true
        line_length: 150
    ```
=== "TOML"
    ```toml
    [tool.pymarkdown]
    plugins.MD013.enabled = true
    plugins.MD013.line_length = 150
    ```
<!-- pyml enable code-block-style-->

For a Rule Plugin's available configuration items, start with the
[Advanced Rule Plugins](./advanced_plugins.md)
overview, then use the [Rule Plugins document](./rules.md) for each Rule Plugin's
details.

### Extensions

This item shows how to enable specific extensions:

<!-- pyml disable-num-lines 5 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| *special* | [--enable-extensions](./user-guide.md#enabling-extensions)   | String    | Comma separated list of extensions to enable. |

#### Enable Extensions

Extensions are configured similarly to Rule Plugins, but there are no general
command-line options for enabling or configuring them. Most teams enable
extensions in project‑level configuration files, so additional command‑line
flags were not added.

By default, only the [Pragmas Extension](./extensions/pragmas.md) is enabled, because
it underpins PyMarkdown's Rule Failure Suppression. The two most commonly enabled
additional extensions are:

- [Front-Matter Extension](./extensions/front-matter.md): enables YAML metadata
  at the start of the file.
- [Markdown Tables Extension](./extensions/markdown-tables.md): enables Markdown
  tables.

You can enable both with:

<!-- pyml disable code-block-style-->
=== "Command Line"
    ```sh
    --enable-extensions front-matter,markdown-tables
    ```
=== "--set Argument"
    ```sh
    --set 'extensions.front-matter.enabled=$!True' --set 'extensions.markdown-tables.enabled=$!True'
    ```
=== "JSON"
    ```json
    {
      "extensions": {
        "front-matter": {
          "enabled": true
        },
        "markdown-tables": {
          "enabled": true
        }
      }
    }
    ```
=== "YAML"
    ```yaml
    extensions:
      front-matter:
        enabled: true
      markdown-tables:
        enabled: true
    ```
=== "TOML"
    ```toml
    [tool.pymarkdown]
    extensions.front-matter.enabled = true
    extensions.markdown-tables.enabled = true
    ```
<!-- pyml enable code-block-style-->

For details on available extensions and their settings, see
[Advanced Extensions](./advanced_extensions.md#categories-of-extensions), which
also links to each extension's page.

### Other

These items do not fit nicely into any other category.

<!-- pyml disable-num-lines 4 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| -- | [`--continue-on-error`](./user-guide.md#-continue-on-error-error-reporting) | Boolean | Enable PyMarkdown to continue after application errors. |
| `mode.return_code_scheme` | [`--return-code-scheme`](./user-guide.md#-return-code-scheme-observability) | String | Specify a scheme to use when formulating the return code. |

#### Continuing on Errors

The `--continue-on-error` argument instructs PyMarkdown to log any application errors
but continue processing the remaining Markdown files. It is only supported through
the command line.

When combined with `mode.strict-config=true`, configuration errors are still validated
and reported, but they do not stop the run; they are logged and processing continues.
This can be useful in CI when you need a full report but still want visibility into
invalid configuration.

#### Controlling Return Codes

The `mode.return_code_scheme` configuration item controls PyMarkdown's return codes
by selecting either the `default` or `minimal` scheme. These schemes help scripts
interpret success and failure consistently using the return codes [identified here](./user-guide.md#-return-code-scheme-observability).

<!-- pyml disable code-block-style-->
=== "Command Line"
    ```sh
    --return-code-scheme minimal
    ```
=== "--set Argument"
    ```sh
    --set 'mode.return_code_scheme=minimal'
    ```
=== "JSON"
    ```json
    {
      "mode": {
        "return_code_scheme": "minimal"
      }
    }
    ```
=== "YAML"
    ```yaml
    mode:
      return_code_scheme: "minimal"
    ```
=== "TOML"
    ```toml
    [tool.pymarkdown]
    mode.return_code_scheme = "minimal"
    ```
<!-- pyml enable code-block-style-->

## Choosing Between Command Line and Configuration Files

A common question &mdash; for PyMarkdown and other projects &mdash; is whether to
use configuration files or command-line arguments. The answer depends on your context
and needs.

In practice, your workflow determines whether configuration files or command-line
arguments are better:

- **Configuration files** work best when:
    - You run PyMarkdown from multiple places or scripts.
    - You want a stable, reviewable record of settings.
    - You manage more than a handful of options.
- **Command-line arguments** work best when:
    - You are experimenting with new options.
    - You need temporary overrides for a single run.

In practice, our team stores most settings in a JSON config file and reserves command-line
flags for experiments. Choose a comparable convention for your team and document
it.
