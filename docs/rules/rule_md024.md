# Rule - MD024

| Aliases |
| --- |
| `md024` |
| `no-duplicate-heading` |
| `no-duplicate-header` |

## Summary

Multiple headings cannot contain the same content.

## Reasoning

### Correctness

While not common to the default installation of most parsers, a common extension
to those parsers is to generate an `id` attribute for the heading element and/or
an anchor tag based on the content of the heading element.  Therefore, having
two or more headings with the same text may confuse those generators, producing
poor results for those anchors.

## Examples

### Failure Scenarios

This rule triggers when there are multiple headings that have the same text:

```Markdown
# Heading Text

## Heading Text
```

### Correct Scenarios

This rule does not trigger when each heading has distinct text:

```Markdown
# Heading 1

## Heading 2
```

A strict comparison is performed, so even an extra space character:

```Markdown
# Heading  Text

## Heading Text
```

or a change in capitalization is enough to avoid this rule triggering:

```Markdown
# Heading TEXT

## Heading Text
```

In certain Markdown documents, such as `changelog.md` files, non-sibling
headings may purposefully have the same text.  As this is the desired
behavior, the `siblings_only` or `allow_different_nesting` configuration value
can be set to `True` to allow this Markdown document to not trigger this rule:

```Markdown
# Change log

## 1.0.0

### Features

## 2.0.0

### Features
```

## Configuration

| Prefixes |
| --- |
| `plugins.md024.` |
| `plugins.no-duplicate-heading.` |
| `plugins.no-duplicate-header.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `siblings_only` | `boolean` | `False` | Whether the plugin rule allows the same text on sibling headings. |
| `allow_different_nesting` | `boolean` | `False` | Whether the plugin rule allows the same text within different nesting hierarchies. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD024](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md024---multiple-headings-with-the-same-content).
