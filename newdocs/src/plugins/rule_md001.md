# Rule - MD001

| Property | Value |
| --- | -- |
| Aliases | `md001`, `heading-increment`, `header-increment` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Heading levels should only increment by one level at a time.

## Reasoning

### Readability

Based on information from the
[Web Accessibility  Initiative](https://www.w3.org/WAI/tutorials/page-structure/headings/),
skipping levels (or ranks as they refer to them) in headings can be confusing, even
more so for accessibility related technology.  From a general point of view, as
headings with increasing levels specify more focused information on a given subject,
it rarely makes sense for a document to skip heading levels, and therefore, information.

## Examples

### Failure Scenarios

This rule triggers when a heading level is increased by more than one level, such
as:

```Markdown
# Heading 1

### Heading 3
```

This changes for the very first heading if front-matter is present at the start
of the Markdown document and the [Front-Matter Extension](../extensions/front-matter.md)
is enabled.  In that case, the value of the `front_matter_title` configuration item
(defaulting to `title`) specifies the case-insensitive name of the front-matter
metadata item to consider as the title of the document.  If that field is present
in the metadata, it is understood that it will be used as the document's level 1
heading. In this case, anything except a level 2 heading will cause a failure.

This is shown in the following Markdown document, if the `front_matter_title` configuration
item is set to its default of `title`:

```Markdown
---
title: my title
---

### Heading 3
```

### Correct Scenarios

This rule does not trigger when there is a single level increase between heading
items or any decrease of the heading levels:

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

## Fix Description

The heading count (number of `#` characters) is adjusted to match what is expected.

## Configuration

| Prefixes |
| --- |
| `plugins.md001.` |
| `plugins.heading-increment.` |
| `plugins.header-increment.` |

<!--- pyml disable-num-lines 4 line-length-->
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
simply looks for the value of the front-matter key `title` by default,
as the PyMarkdown parser loads the YAML front-matter and retains its
values.
