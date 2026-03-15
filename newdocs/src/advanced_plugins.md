---
summary: Base information about the PyMarkdown Linter2
authors:
  - Jack De Winter
---

# Advanced Rule Plugins

You may already have seen Rule Plugins in the [User Guide](./user-guide.md#rule-plugins),
in [Basic Fixing](./user-guide.md#basic-fixing), and in [Advanced Configuration](./advanced_configuration.md#rule-plugins).
Those pages focus on **using** Rule Plugins in day‑to‑day workflows:

- where Rule Plugins are applied,
- how to enable or disable them, and
- how to run fixes.

This page focuses on how Rule Plugins work as a **system**:

- what a Rule Plugin is,
- how Rule Plugins expose rules to PyMarkdown,
- how configuration layers interact, and
- how to suppress or tune specific Rule Plugins for your project.

Use the pages above when you want to run PyMarkdown effectively; use this page when
you need to understand how the Rule Engine and configuration model fit together.

A rule is an analyzer: code that reads the stream of information from the
[PyMarkdown parser](./user-guide.md#markdown-parser) and triggers a failure when
it detects behavior that violates the rule.

A Rule Plugin is the Python module that exposes a rule to PyMarkdown. By following
a defined structure, the plugin lets PyMarkdown locate the rule, load it, and treat
it as a built‑in extension.

## Skipping Ahead

To help you quickly find what you need, here is a roadmap of what this page covers:

- [Why Our Rule Plugins Look the Way They Do](#why-our-rule-plugins-look-the-way-they-do)
- [Working With Rule Plugins](#working-with-rule-plugins)
    - [Rule Plugin Ids](#rule-plugin-ids)
    - [Rule Plugin Configuration](#rule-plugin-configuration)
        - [Rule Plugin Configuration With Multiple Layers](#rule-plugin-configuration-with-multiple-layers)
        - [Specific Rule Plugin Configuration](#specific-rule-plugin-configuration)
- [List Rule Plugins from the Command Line](#list-rule-plugins-from-the-command-line)
- [Suppressing Rule Failures (Pragmas)](#suppressing-rule-failures-pragmas)
- [Compiled List of Rule Plugins](#compiled-list-of-rule-plugins)
- [Rule Plugin Configuration for Specific Parsers](#rule-plugin-configuration-for-specific-parsers)
    - [Python-Markdown](#python-markdown)

## Why Our Rule Plugins Look the Way They Do

Many of our Rule Plugins closely parallel David Anson's
[MarkdownLint](https://github.com/DavidAnson/markdownlint) project, which is
widely used in editors such as VSCode. We intentionally align with those rules
where it makes sense, but we refine their structure.

As described in our
[README.md](https://github.com/jackdewinter/pymarkdown#what-linting-checks-does-pymarkdown-release-with),
PyMarkdown emphasises Rule Plugins, each with a single, clear responsibility. Rather
than
one Rule Plugin with multiple behaviors, we prefer multiple Rule Plugins, each handling
one
concern. This approach increases the number of Rule Plugins we maintain, but keeps
each Rule Plugin focused
and predictable.

## Working With Rule Plugins

### Rule Plugin Ids

Each Rule Plugin has a primary identifier associated with it. Primary identifiers
follow a fixed pattern: a 2–3 letter prefix and a 3‑digit suffix. Each Rule Plugin
can also have one or more names.
Each name can contain alphabetic characters and the `-` character. This combination
of primary identifier and names is referred to as the Rule Plugin's identifiers.
These identifiers are guaranteed to be unique within an instance of PyMarkdown.
In most cases, you can use them interchangeably.

### Rule Plugin Configuration

The core details of this topic are covered in the
[Advanced Configuration](./advanced_configuration.md)
documentation. That document is your **reference** for all configuration keys and
formats.

This page complements the reference with a focus on the **behavior** of Rule Plugin
configuration:

- how more complex configuration setups behave across layers, and
- how configuration items for Rule Plugins interact in practice.

At a high level, PyMarkdown merges configuration from three sources: built‑in defaults,
configuration files, and command‑line overrides.
Later sources override earlier ones. When multiple values are present for the same
setting, the "closest" source (usually the command line) wins.

See also: [Rule Plugins in Advanced Configuration](./advanced_configuration.md#rule-plugins)
for the full list of available configuration options.

#### Rule Plugin Configuration With Multiple Layers

To make that precedence concrete, this section walks through a **multi-layer example**
that shows how enable/disable decisions are made when configuration files and command‑line
options conflict.

**Note:** This example uses all three configuration layers to illustrate their interaction.

Most real‑world PyMarkdown configurations use two layers or fewer.

Let us start with a configuration file called `config.json` with contents:

```json
{
    "plugins": {
        "MD011": {
            "enabled": true,
        },
        "MD012": {
            "enabled": true,
        },
        "MD013": {
            "enabled": false
        }
    }
}
```

and a command line of (newlines inserted for readability):

```bash
pipenv run pymarkdown --disable-rules MD011 \
                      --set 'plugins.MD011.enabled=$!True' \
                      --set 'plugins.MD012.enabled=$!False' \
                      --config config.json \
                      scan -r .
```

Therefore, after applying all configuration layers:

- `MD011`
    - `config.json`: enabled
    - `--set`: explicitly enabled
    - `--disable-rules MD011`: disabled
    - **Final:** disabled by `--disable-rules`

- `MD012`
    - `config.json`: enabled
    - `--set 'plugins.MD012.enabled=$!False'`: disabled
    - **Final:** disabled by `--set`

- `MD013`
    - `config.json`: disabled
    - No overrides
    - **Final:** disabled by `config.json`

This matches the precedence rules in [Configuration Sources and Layering](./advanced_configuration.md#configuration-sources-and-layering).

#### Specific Rule Plugin Configuration

The previous example focused on **whether** a Rule Plugin is enabled or disabled
across
multiple configuration layers. In many projects, you also need to control **how**
individual Rule Plugins behave via their own settings.
The [Advanced Configuration](./advanced_configuration.md#specific-plugin-settings)
documentation explains that each Rule Plugin exposes its own configuration items
under the `plugins.<identifier>.*` namespace, and this section provides concrete
examples of using those settings.

While Rule Plugin enablement can use the `--enable-rules` and `--disable-rules`
[syntactic sugar](https://en.wikipedia.org/wiki/Syntactic_sugar) options,
Rule Plugin configuration items must always be set explicitly, either via `--set`
on the command line or in a configuration file.

For this example, we will configure a commonly changed setting: `line_length`. First,
we'll show where the `line-length` plugin's options live in each format, then we'll
add the `line_length` value there.

We start with the following configuration, which only controls whether the Rule Plugin
is enabled:

<!-- pyml disable code-block-style-->
=== "Command Line"
    Not Applicable
=== "--set Argument"
    ```sh
    --set 'plugins.line-length.enabled=$!True'
    ```
=== "JSON"
    ```json
    {
      "plugins": {
        "line-length": {
          "enabled": true
        }
      }
    }
    ```
=== "YAML"
    ```yaml
    plugins:
      line-length:
        enabled: true
    ```
=== "TOML"
    ```toml
    [tool.pymarkdown]
    plugins.line-length.enabled = true
    ```
<!-- pyml enable code-block-style-->

Here, we leverage the [Rule Plugin Ids](#rule-plugin-ids) section to use one of
the other identifiers for the Rule Plugin. Both `MD013` and `line-length` are valid
identifiers, but the human‑readable form is often easier to scan in configuration
files.

A pragmatic rule of thumb is:

- use the **short id** (`MD013`) when you are scripting, debugging, or comparing
  against other tools, and
- use the **name** (`line-length`) when you want configuration files to be self‑documenting.

You can use either the primary identifier `MD013` or one of the other identifiers,
but be consistent within a given file. The [Configuration](./plugins/rule_md013.md#configuration)
section for Rule Plugin `MD013` explains that `line_length` is the main setting
that controls the maximum accepted line length.
We can now
extend
the previous configuration with a `line_length` value of `100`:

<!-- pyml disable code-block-style-->
=== "Command Line"
    Not Applicable
=== "--set Argument"
    ```sh
    --set 'plugins.line-length.enabled=$!True' \
    --set 'plugins.line-length.line_length=$#100'
    ```
=== "JSON"
    ```json
    {
      "plugins": {
        "line-length": {
          "enabled": true,
          "line_length": 100
        }
      }
    }
    ```
=== "YAML"
    ```yaml
    plugins:
      line-length:
        enabled: true
        line_length: 100
    ```
=== "TOML"
    ```toml
    [tool.pymarkdown]
    plugins.line-length.enabled = true
    plugins.line-length.line_length = 100
    ```
<!-- pyml enable code-block-style-->

With these patterns, you can apply the same `plugins.<identifier>.*` structure to
any Rule Plugin's configuration items.

## List Rule Plugins from the Command Line

Once you know how to configure individual Rule Plugins, the next step is to
**discover which Rule Plugins exist and what their identifiers are**. Rule Plugins
are
managed from the command line via the [Plugin Command](./user-guide.md#plugin-command).
For full details, refer to the user guide; this document assumes familiarity with
that command. Use the `list` subcommand to discover Rule Plugins, and `info` to
retrieve
detailed information about them.

## Suppressing Rule Failures (Pragmas)

[Rule Failures](./user-guide.md#rule-failure) are generated in response to a Rule
Plugin
triggering because of its coded rule. Earlier in this document, we described rules
as analyzers that look for specific patterns in the Markdown document.
Therefore, any reported failure is the direct result of a rule detecting content
it considers incorrect in the Markdown document.

Most Rule Failures are accurate and should be fixed by the author. However, Rule
Failures
can also occur when the author intentionally wrote the Markdown that way, and that
is where [Pragmas](./extensions/pragmas.md) are useful.

This section shows **practical patterns** for using Pragmas with Rule Plugins. For
the full syntax, all Pragma commands, and edge cases, see the dedicated
[Pragmas extension documentation](./extensions/pragmas.md).

### What Are Pragmas?

[Pragmas](https://en.wikipedia.org/wiki/Directive_(programming)) are constructs
that tell a language implementation how to interpret the code or data it is processing.
In PyMarkdown, we borrow this idea to mark sections of the Markdown document that
should be treated differently before the parser sees them.

In the following example, without the Pragma line (starting with `<!--`),
PyMarkdown reports a failure of the `no-multiple-space-atx` (or `MD019`) Rule Plugin.
That line specifically informs PyMarkdown to ignore Rule Failures for the Rule Plugin
`no-multiple-space-atx` on the line that follows it.

```Markdown
some paragraph

<!-- pyml disable-next-line no-multiple-space-atx-->
#  My Bad Atx Heading

some other paragraph
```

### A More Realistic Example

As a more realistic case, consider how we handle suppressions in our [changelog](./changelog.md).
We structured the file with a simple format that records changes for each release.
Any new entries go in the "Unversioned" section at the top.

```Markdown
## Unversioned - In Main, Not Released

### Added

- None

### Fixed

- None

### Changed

- None
```

When we build
a release, we change the "Unversioned" name and date and add this template to
the top of the file. The resulting changelog looks like:

```Markdown
## Unversioned - In Main, Not Released

### Added

- None

### Fixed

- None

### Changed

- None

## Version vX.Y.Z - Release Date: 2023-12-25

### Added

- None

### Fixed

- None

### Changed

- None
```

With no additional configuration, `changelog.md` produces `no-duplicate-heading`
Rule Failures for each repeated `Added`, `Fixed`, and `Changed` heading.

Before we moved the changelog from its [old location](https://github.com/jackdewinter/pymarkdown/blob/main/changelog.md)
to its [new location](https://github.com/jackdewinter/pymarkdown/blob/main/newdocs/src/changelog.md),
we had to address these Rule Failures. We did so by disabling the `no-duplicate-heading`
Rule Plugin for the entire project. Disabling the Rule Plugin globally was not an
ideal solution.

After relocating the changelog, we re‑enabled `no-duplicate-heading`. We also updated
the top `Unversioned` section to use Pragmas for targeted suppression.

```Markdown
## Unversioned - In Main, Not Released

<!-- pyml disable-next-line no-duplicate-heading-->
### Added

- None

<!-- pyml disable-next-line no-duplicate-heading-->
### Fixed

- None

<!-- pyml disable-next-line no-duplicate-heading-->
### Changed

- None
```

#### Enter the Enable and Disable Pragma Commands

With version `0.9.30` came the addition of the `enable` and `disable` commands
[for Pragmas](./extensions/pragmas.md#disable-command-and-enable-command). After
the coding and testing was completed for that feature, we made an edit to our
`changelog.md` file that looked like this:

```Markdown
## Unversioned - In Main, Not Released

<!-- pyml disable no-duplicate-heading-->
### Added
<!-- pyml enable no-duplicate-heading-->

- None

<!-- pyml disable no-duplicate-heading-->
### Fixed
<!-- pyml enable no-duplicate-heading-->

- None

<!-- pyml disable no-duplicate-heading-->
### Changed
<!-- pyml enable no-duplicate-heading-->

- None
```

We found that approach added too much visual clutter because of the repeated
`disable`/`enable` lines. A single `disable` at the top of the file also proved
unsuitable. It disabled the Rule Plugin for the entire changelog instead of only
the repeated
headings.

Because `disable-next-line` keeps the intent local with little visual noise, we
retained that pattern. Treat it as an example of one effective approach. Then choose
the Pragma pattern that best matches your team's conventions and desired scope.

## Compiled List of Rule Plugins

The [Rules Documentation](./rules.md) is the **index of all Rule Plugins** that
are released
with PyMarkdown.
The list is regenerated for every release, so it always reflects the current set
of rules and their Rule Plugins.

Use that list when you need to:

- **Discover identifiers** (`MD013`, `line-length`, etc.) for a Rule Plugin you
  want to configure
- **Jump to full Rule Plugin documentation** to see reasoning, examples, and configuration
- **Scan multiple Rule Plugins at once** for summary, **autofix** capability, and
  default enabled state

In practice:

- Start from this page when you want to understand *how* rule plugins behave and
  how they interact with configuration.
- Jump to the [Rule Plugin Documentation](./rules.md) when you already know *which*
  Rule Plugin you care about. Use it when you need the Rule Plugin's **full specification**.

Combined with the examples on this page, the [Rule Plugins Documentation](./rules.md)
gives
you the identifiers, links, and Rule Plugins details you need to configure your project
effectively.

### Rule Plugin Documentation Structure

We apply the following pattern to every Rule Plugins's documentation to keep the
structure
consistent and make key information easy to locate.

- Introduction (implicit)
    - Details aliases, whether the **autofix** capability is available, and whether
      the Rule Plugin is enabled by default.
- Deprecation (optional)
    - Indicates that the Rule Plugin was removed and, when applicable, points to
      a replacement Rule Plugin.
- Summary
    - Text line presented by the Rule Plugin when a failure occurs.
- Reasoning
    - A defined basis for implementing this Rule Plugin: Consistency, Readability,
      Simplicity, Correctness, or Portability
- Examples
    - Examples that demonstrate when Rule Failures occurs and when Rule Failures
      do not occur.
- Fix Description
    - Explains what change results from the automatic fix; otherwise, explains why
      no fix is implemented.
- Configuration
    - The collection of settings that are present for this Rule Plugin.
- Origination of rule and Rule Plugin
    - Details of what prompted this rule to initially be created.
- Differences From MarkdownLint Rule (optional)
    - When derived from a MarkdownLint rule, documents the differences and the rationale
      for them.

## Rule Plugin Configuration for Specific Parsers

The configuration techniques above apply regardless of which Markdown parser you
use. However, some parsers differ enough from GitHub Flavored Markdown that you'll
want to swap or tune specific Rule Plugins to align with their behavior.

While most parsers follow the [GitHub Flavored Markdown](https://github.github.com/gfm/)
specification and do not require any configuration
items to be specially set for them, there are exceptions.

### Python-Markdown

Because PyMarkdown is written in Python, we started by evaluating
[Python-Markdown](https://python-markdown.github.io/), which also powers [MkDocs](https://www.mkdocs.org/),
the tool used for this documentation. If you are not using Python-Markdown or MkDocs,
you can skim or skip this section.

Python-Markdown is largely compliant, but it documents several differences on its
[home page](https://python-markdown.github.io/#differences). The biggest difference
is that the Python-Markdown team passionately believes that
all Unordered List Indents should be 4 characters.

These differences mean PyMarkdown must accommodate Markdown parsers that are
slightly non-compliant with the GitHub Flavored Markdown specification. For
Python-Markdown, we address this by providing
[Rule Plugin Pml101](./plugins/rule_pml101.md), `list-anchored-indent`, which is
a
configuration-compatible variant of the [`ul-indent` Rule Plugin](./plugins/rule_md007.md).
The `list-anchored-indent` Rule Plugin adjusts list indentation specifically to match
Python-Markdown's expectations.

If you need to understand exactly how list indentation is interpreted, read the
[`list-anchored-indent` Rule Plugin documentation](./plugins/rule_pml101.md) and
compare
it with
the [`ul-indent` Rule Plugin](./plugins/rule_md007.md). If you only need the recommended
settings, the configuration below is sufficient.

Therefore, to accommodate Python-Markdown, the following configuration is suggested:

<!-- pyml disable code-block-style-->

=== "Command Line"
    Not Applicable
=== "--set Argument"
    ```sh
    --set 'plugins.ul-indent.enabled=$!False' \
    --set 'plugins.list-anchored-indent.enabled=$!True'
    ```
=== "JSON"
    ```json
    {
      "plugins": {
        "ul-indent" : {
          "enabled": false
        },
        "list-anchored-indent" : {
          "enabled": true
        }
      }
    }
    ```
=== "YAML"
    ```yaml
    plugins:
      ul-indent:
        enabled: false
      list-anchored-indent:
        enabled: true
    ```
=== "TOML"
    ```toml
    [tool.pymarkdown]
    plugins.ul-indent.enabled = false
    plugins.list-anchored-indent.enabled = true
    ```
<!-- pyml enable code-block-style-->
