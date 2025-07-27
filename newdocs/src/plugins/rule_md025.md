# Rule - MD025

| Property | Value |
| --- | -- |
| Aliases | `md025`, `single-title`, `single-h1` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Multiple top-level headings in the same document.

## Reasoning

### Correctness

While not accepted as the document title in some parsers, the
majority of the parsers consider the top-level heading or
Heading 1 element to be the title of the document.  It follows
that a document cannot have more than one title and allowing
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
[front-matter parsing](../extensions/front-matter.md)
is enabled and a normal top-level heading is parsed, then this rule will trigger:

```text
---
title: this is a title
---

# Top Level
```

### Correct Scenarios

This rule does not trigger if there is only one top-level heading in
the entire document, including any parsed front-matter:

````Markdown
# Top Level

## Used To Be Another Top Level
````

If front-matter parsing is enabled and a front-matter section is present, the
`front_matter_title` configuration item specifies the key in the
front-matter's data map that is considered the title.  If that key is
present in the document's front-matter, then all headings in the
document must be level 2 or below.  For example, if the configuration
item is set to `subject`, then this example is valid:

```text
---
subject: This is a title
---

## Used To Be Another Top Level
```

In certain situations, it is necessary to override the heading level
to check for multiple top-level elements.  In these situations, the
`level` configuration value can be set to specify the heading level
to check against for multiple top-level elements with.

## Fix Description

The reasons for not being able to auto-fix this rule are context and cascading fixes.
On the context front, while there is precedence only the first top level heading
of a document should be honored, we do not currently consider it to be a solid enough
precedent to base a fix on.  In addition, cascading fixes can cause a problem with
the multiple of the top-level heading.  If those offending headings are changed to
a level 2 heading, should any other headings within those headings be similarly
increased?  The ambiguities of both reasons were enough for our team to not consider
any possible fixes for this rule.

## Configuration

| Prefixes |
| --- |
| `plugins.md025.` |
| `plugins.single-title.` |
| `plugins.single-h1.` |

<!-- pyml disable-num-lines 5 line-length-->
| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `front_matter_title` | `string` | `title` | Name of the front-matter field that has the title associated with the document.** |
| `level` | `integer` | `1` | Heading level to be considered as the top-level. |

** Any leading or trailing space characters are removed from the `front_matter_title`
during processing.  This value is expected not to have the `:` at the end. Therefore,
a header value of `subject:` would be entered as `subject`.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD025](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md025---multiple-top-level-headings-in-the-same-document).

### Differences From MarkdownLint Rule

The difference between this rule and the original rule is that the
original rule specified a regular expression used to look for the
specific element within a raw front-matter element.  By default, this
was `"^\s*"?title"?\s*[:=]"`.  To support simplicity, this rule
simply looks for the value of the front-matter key `title` by default.
