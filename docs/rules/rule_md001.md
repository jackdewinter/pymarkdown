# Rule - MD001

| Aliases |
| --- |
| `md001` |
| `heading-increment` |
| `header-increment` |

| Autofix Available |
| --- |
| Yes |

## Summary

Heading levels should only increment by one level at a time.

## Reasoning

### Readability

Based on information from the
[Web Accessibility  Initiative](https://www.w3.org/WAI/tutorials/page-structure/headings/),
skipping levels (or ranks as they refer to them) in headings can be confusing, even more so
for accessibility related technology.  From a general point of view, as headings with
increasing levels specify more specific information on a given subject, it rarely makes
sense to skip one or more levels.  Allowing levels to be omitted would therefore imply
that one or more levels of specification on a given subject were also omitted.  Therefore,
skipping increasing levels is not desired.

## Examples

### Failure Scenarios

This rule triggers when a heading level is increased by more than one level, such as:

```Markdown
# Heading 1

### Heading 3
```

If front-matter is present at the start of the Markdown document and
the
[Front Matter Extension](https://github.com/jackdewinter/pymarkdown/blob/main/docs/extensions/front-matter.md)
is enabled, then special Front Matter handling is enabled. If this
special handling is enabled and if the field specified by the `front_matter_title`
configuration value is present in the Front Matter, then that field
is interpreted by this rule as an implicit Level 1 Heading element.
Therefore, if that field is present in the Front Matter element,
then the following scenario reports an error:

```Markdown
---
title: my title
---

### Heading 3
```

as the Heading element level went from 1 for the implicit element
to 3 for the explicit Atx Heading element.

### Correct Scenarios

This rule does not trigger when there is a single level increase between heading items
or any decrease of the heading levels:

```Markdown
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

## Another Heading 2

### Another Heading 3
```

If a front-matter field is present with the configured name, a correct document must
start with a level 2 heading:

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
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `front_matter_title` | `string` | `title` | Name of the front-matter field that contains the title associated with the document. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD001](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md001---heading-levels-should-only-increment-by-one-level-at-a-time)
and the
[W3C standards](https://www.w3.org/WAI/tutorials/page-structure/headings/).

### Differences From MarkdownLint Rule

The difference between this rule and the original rule is that the
original rule specified a regular expression used to look for the
specific element within a raw front-matter element.  By default, this
was `"^\s*"?title"?\s*[:=]"`.  To support simplicity, this rule
simply looks for the value of the front-matter key `title` by default.

## Fix Description

The heading count (number of `#` characters) is adjusted to match what is expected.
