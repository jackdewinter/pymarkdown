# Rule - MD041

| Property | Value |
| --- | -- |
| Aliases | `md041`, `first-line-heading`, `first-line-h1` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

First line in file should be a top-level heading.

## Reasoning

### Correctness

In most cases, the top-level heading of a document is used as the title of
that document.  Therefore, the first heading in the document should be a
level 1 header to reflect that reality.

## Examples

### Failure Scenarios

This rule is triggered when the first element in the document is not a
top-level or `h1` heading:

```Markdown
This document does not have a heading
```

### Correct Scenarios

This rule does not trigger when there is a valid top-level heading:

```Markdown
# This is an Atx H1 heading
```

or:

```Markdown
This is a SetExt H1 heading
===
```

Most notable with GitHub project pages, documents may use an image for the
title of the document.  To support this, a document started with a HTML
block that begins with a valid `h1` token is acknowledged as a valid
top-level document heading:

```Markdown
<h1 align="center"><img src="/path/to/image"/></h1>
```

#### Front-Matter

If a Front-Matter element is present in the document and the
[Front-Matter Extension](../extensions/front-matter.md)
is enabled, then rule will look in the metadata provided in the Front-Matter
block for an entry with the exact name as specified under the
`front_matter_title` configuration value.  For example, using the
default configuration value of `title`, the following Markdown
document will not trigger this rule:

```Markdown
---
title: Top Level Heading
---

the document has a valid heading.
```

This searching through the Front-Matter element for a matching
entry can be disabled by setting the `front_matter_title` configuration
value to an empty string (`""`).

#### Changing The Top Level

Configuration may be applied to change the expected top-level of
this rule from its default of `1` to another value.  This should only be done
if an external process is generating the title of the document.
For example, if the `level` configuration value is set to `2`, then the following
document will not trigger this rule:

```Markdown
## This isn't an Atx H1 heading
```

## Fix Description

The reason for not being able to auto-fix this rule is context.  Given that a top
level was not present in the document, context from the author is needed to determine
what text should be in that heading.

## Configuration

| Prefixes |
| --- |
| `plugins.md041.` |
| `plugins.first-line-heading.` |
| `plugins.first-line-h1.` |

<!--- pyml disable-num-lines 5 line-length-->
| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `level` | `integer` | `1` | Level that is expected from the first heading (Atx or SetExt) in the document. |
| `front_matter_title` | `string` | `title` | Name of the front-matter field that has the title associated with the document.** |

** Any leading or trailing space characters are removed from the `front_matter_title`
during processing.  The `front_matter_title` value is expected to not to have the
`:` at the end. Therefore, a header value of `subject:` would be entered as `subject`.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD041](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md041---first-line-in-a-file-should-be-a-top-level-heading).

### Differences From MarkdownLint Rule

The difference between this rule and the original rule is in
the handling of the HTML comment tag.  The original rule dealt with
the HTML comment tag and other special tags as invisible, only
triggering based on any information that occurred after that
tag.  This rule is implemented to include any special tags,
including the HTML comment tag, in the triggering conditions for
this rule.
