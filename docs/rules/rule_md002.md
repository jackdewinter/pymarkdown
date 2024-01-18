# Rule - MD002

| Aliases |
| --- |
| `md002` |
| `first-heading-h1` |
| `first-header-h1` |

| Autofix Available |
| --- |
| No |

## Deprecation

This rule has been deprecated in favor of [Rule md041](https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md041.md).

## Summary

First heading of the document should be a top-level heading.

## Reasoning

### Consistency

In most cases, the top-level heading of a document is used as the title of
that document.  Therefore, the first heading in the document should be a
level 1 header to reflect that reality.

## Examples

### Failure Scenarios

This rule triggers when the first heading in the document is not a
level 1 heading in either an Atx Heading format:

```Markdown
## This isn't an Atx H1 heading
```

or a SetExt Heading format:

```Markdown
This isn't a SetExt H1 heading
---
```

### Correct Scenarios

This rule does not trigger when there is a single level increase between heading items
or any decrease of the heading levels, as follows:

```Markdown
# This is an Atx H1 heading
```

or:

```Markdown
This is a SetExt H1 heading
===
```

Note that configuration may be applied to change the expected top-level of
this rule from its default of `1` to another value.  This should only be done
if an external process is generating the title of the document.
For example, if the `level` configuration value is set to `2`, then the following
document will not trigger this rule:

```Markdown
## This isn't an Atx H1 heading
```

## Configuration

| Prefixes |
| --- |
| `plugins.md002.` |
| `plugins.first-heading-h1.` |
| `plugins.first-header-h1.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the plugin rule is enabled. |
| `level` | `integer` | `1` | Level that is expected from the first heading (Atx or SetExt) in the document. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD002](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md002---first-heading-should-be-a-top-level-heading),
which is in turn inspired by
[this article](https://cirosantilli.com/markdown-style-guide/#top-level-header).

## Fix Description

The reason for not being able to auto-fix this rule is deprecation in favor of
rule [Rule MD041](https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md041.md)
