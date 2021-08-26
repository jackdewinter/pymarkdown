# Rule - MD001

| Aliases |
| --- |
| `md001` |
| `heading-increment` |
| `header-increment` |

## Summary

Heading levels should only increment by one level at a time.

## Reasoning

Based on information from the
[Web Accessibility  Initiative](https://www.w3.org/WAI/tutorials/page-structure/headings/),
skipping levels (or ranks as they refer to them) in headings can be confusing, even more so
for accessibility related technology.  From a general point of view, as headings with
increasing levels specify more specific information on a given subject, it rarely makes
sense to skip one or more levels.  Allowing levels to be omitted would therefore imply
that one or more levels of specification on a given subject were also omitted.  Therefore,
that behavior of skipping increasing levels is generally not desired.

## Examples

### Failure Scenarios

This rule triggers when a heading level is increased by more than one level, such as:

```Markdown
# Heading 1

### Heading 3
```

In addition, if front-matter is present in the Markdown document with the
[configured field name](#configuration),
that front-matter field may take the place of a level 1 heading. That would cause
the following scenario to report an error:

```Markdown
---
title: my title
---

# Heading 1
```

### Correct Scenarios

This rule does not trigger when there is a single level increase between heading items
or any decrease of the heading levels, as follows:

```Markdown
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

## Another Heading 2

### Another Heading 3
```

If a front-matter field is present with the configured name, a correct document must
start with a level 2 heading, as follows:

```Markdown
---
title: my title
---

## Heading 2
```

## Configuration

| Prefixes |
| --- |
| `plugins.md001.` |
| `plugins.heading-increment.` |
| `plugins.header-increment.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled by default. |
| `front_matter_title` | `string` | `"title"` | Name of the front-matter field that contains the title associated with the document. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD001](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md001---heading-levels-should-only-increment-by-one-level-at-a-time)
and the
[W3C standards](https://www.w3.org/WAI/tutorials/page-structure/headings/).

### Differences From MarkdownLint Rule

The difference between this rule and the original rule is that the
original rule specified a regular expression used to look for the
specific element within a raw front-matter element.  By default, this
was `"^\s*"?title"?\s*[:=]"`.  To maintain simplicity, this rule
simply looks for the value of the front-matter key `title` by default.
