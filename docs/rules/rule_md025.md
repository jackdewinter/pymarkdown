# Rule - MD025

| Aliases |
| --- |
| `md025` |
| `single-title` |
| `single-h1` |

## Summary

Multiple top-level headings in the same document.

## Reasoning

### Correctness

While not accepted as the document title in some parsers, the
majority of the parsers consider the top-level heading or
Heading 1 element to be the title of the document.  It follows
that a document cannot have more than one title, and allowing
multiple Heading 1 elements would force the parser to choose
which element was the title.

## Examples

### Failure Scenarios

This rule is triggered when more than one top-level heading is
found in the same document:

````Markdown
# Top Level

# Another Top Level
````

This rule does not perceive any difference between Atx Heading elements
and SetExt Heading elements, so the following document will also trigger
the rule:

```Markdown
# Top Level

Another Top Level
===
```

In addition, if
[front-matter parsing](https://github.com/jackdewinter/pymarkdown/blob/main/docs/extensions/front-matter.md)
is enabled and a normally top-level heading is parsed, then this rule will trigger:

```text
---
title: this is a title
---

# Top Level
```

### Correct Scenarios

This rule does not trigger if there is only top-level heading in
the entire document, including any parsed front-matter:

````Markdown
# Top Level

## Used To Be Another Top Level
````

If a front-matter parsing and a front-matter section is present, the
`front_matter_title` configuration value specifies the key in the
front-matter's data map that is considered the title.  If that key
present in the document's front-matter, then all headings in the
document must be level 2 or below.  For example, if the configuration
value is set to `subject`, then this example is valid:

```text
---
subject: This is a title
---

## Used To Be Another Top Level
```

In certain situations, it is necessary to override the heading level
to check for multiples top-level elements.  In these situations, the
`level` configuration value can be set to specify the heading level
to check against for multiples.

## Configuration

| Prefixes |
| --- |
| `plugins.md025.` |
| `plugins.single-title.` |
| `plugins.single-h1.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `front_matter_title` | `string` | `title` | Name of the front-matter field that has the title associated with the document. |
| `level` | `integer` | `1` | Heading level to be considered as the top-level. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD025](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md025---multiple-top-level-headings-in-the-same-document).

### Differences From MarkdownLint Rule

The difference between this rule and the original rule is that the
original rule specified a regular expression used to look for the
specific element within a raw front-matter element.  By default, this
was `"^\s*"?title"?\s*[:=]"`.  To support simplicity, this rule
simply looks for the value of the front-matter key `title` by default.
