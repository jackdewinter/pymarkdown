# Rule - MD041

| Property | Value |
| --- | --- |
| Aliases | `md041`, `first-line-heading`, `first-line-h1` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Ensure the first line of a Markdown file is a top-level heading.

## Reasoning

### Correctness

In most cases, the top-level heading of a document is used as the title of
that document.  Therefore, the first heading in the document should be a
level 1 header to reflect that reality.

## Examples

### Failure Scenarios

This rule triggers when the first element in the document is not an ATX or Setext
top-level (`h1`) heading. This is the simplest case: the very first line of the
file is plain paragraph text.

```Markdown
This document does not have a heading
```

> **Explanation**: The first block-level element in the document is a paragraph,
> not a level-1 ATX or Setext heading. Per the rule, the first line of a Markdown
> document must be a top-level heading, so the rule fires on this document.

Unlike the previous example, which begins with plain paragraph text, this document
begins with a YAML front-matter block that does not contain the configured title
field (the front-matter extension must be enabled).

```Markdown
---
subject: sample title
----

This document does not have a heading
```

> **Explanation**: Although the document has front-matter, it does not include a
> `title` key (the default `front_matter_title` value). Because neither the front-matter
> nor the body starts with a level-1 heading, the rule triggers.

Unlike the previous scenarios, this document begins with an HTML comment block;
because `<!--` is not part of the `invisible_tags` configuration, the comment counts
as the first element and no top-level heading is present.

```Markdown
<!--
SPDX-FileCopyrightText: L33tCoder, Inc.

SPDX-License-Identifier: MIT
-->
# This file starts with a level 1 heading
```

> **Explanation**: The first element is an HTML comment. Since `invisible_tags`
> is configured as `link` by default and does not include `!--`, the comment is
> treated as the first visible element, and the rule triggers even though an `h1`
> heading follows it.

Unlike the previous scenarios, which begin with non-heading elements, this document
begins with a heading — but the heading is at level 2 rather than the expected
level 1. The `level` configuration value (default `1`) is what determines the expected
level, so a level-2 first heading does not satisfy the rule.

```Markdown
## This heading is at the wrong level
```

> **Explanation**: The first block-level element is an ATX heading, but it is at
> level 2. The rule's `level` configuration is `1` by default, so the first heading
> must be a level-1 ATX or Setext heading. Because the first heading is at level
> 2, the rule triggers.

Unlike the previous scenarios, this document begins with an HTML block that is not
an `<h1>` block. The rule treats a leading HTML block as the first element, and
only an HTML block whose opening tag is `<h1>` is acknowledged as a valid top-level
heading.

```Markdown
<div align="center">
  <img src="/path/to/image"/>
</div>

# This file starts with a level 1 heading
```

> **Explanation**: The first element is an HTML block whose opening tag is `<div>`,
> not `<h1>`. The rule only acknowledges a leading HTML block as a valid top-level
> heading when its opening tag is `<h1>`. Because the opening tag here is `<div>`,
> the rule triggers even though an h1 ATX heading follows the HTML block.

### Correct Scenarios

This rule does not trigger when the first line of the document is a level-1 ATX
heading, the simplest compliant case.

```Markdown
# This is an Atx H1 heading
```

> **Explanation**: The first element is an ATX heading at level 1, which matches
> the default `level` configuration. The rule's requirement for a top-level heading
> is satisfied, so the rule does not trigger.

Unlike the previous example, which uses an ATX heading, this document satisfies
the rule with a Setext-style level-1 heading.

```Markdown
This is a Setext H1 heading
===
```

> **Explanation**: Setext headings are recognized as top-level headings by this
> rule. The first block-level element is a Setext `h1`, so the rule does not trigger.

Unlike the prior examples, which start directly with a heading, this document starts
with front-matter. The rule still does not trigger because the front-matter block
contains a `title` key (the front-matter extension must be enabled).

```Markdown
---
title: sample title
----

This document has the equivalent of a level-1 heading
because of the `title` field in the front-matter section.
```

> **Explanation**: With the Front-Matter Extension enabled and the default `front_matter_title`
> value of `title`, the rule finds a matching title entry in the front-matter and
> considers the document to have a valid top-level heading. The rule does not trigger.

Unlike the previous scenario, which relied on a front-matter `title`, this document
begins with a `<link>` element. The rule still does not trigger because `link` is
in the default `invisible_tags` list.

```Markdown
<link rel="stylesheet" href="/styles.css">
# This file starts with a level 1 heading
```

> **Explanation**: The `<link>` tag is treated as invisible because `link` is included
> in the default `invisible_tags` value. After skipping it, the first visible element
> is a level-1 ATX heading, so the rule does not trigger.

Unlike the previous scenarios, this document begins with an HTML `<h1>` block (commonly
used for a centered image title on GitHub project pages). The rule acknowledges
a leading HTML block that starts with an `<h1>` token as a valid top-level heading.

```Markdown
<h1 align="center"><img src="/path/to/image"/></h1>
```

> **Explanation**: The first element is an HTML block whose opening tag is `<h1>`.
> PyMarkdown's rule explicitly recognizes this pattern as a valid top-level heading
> (see the [HTML Tags](#html-tags) note), so the rule does not trigger.

## Notes

### Front-Matter

If a Front-Matter element is present in the document and the
[Front-Matter Extension](../extensions/front-matter.md)
is enabled, then rule will look in the metadata provided in the Front-Matter
block for an entry with the exact name as specified under the
`front_matter_title` configuration value. For example, using the
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

### HTML Images As Headings

Most notable with GitHub project pages, documents may use an image for the
title of the document. To support this, a document started with a HTML
block that begins with a valid `h1` token is acknowledged as a valid
top-level document heading:
For more information on this and other allowances for HTML tags at the
start of the document, refer to the [HTML tags](#html-tags) section below.

```Markdown
<h1 align="center"><img src="/path/to/image"/></h1>
```

### HTML Tags

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Available: Version 0.9.32**

Responding to a challenge from [our users](https://github.com/jackdewinter/pymarkdown/issues/1400),
we took another look at why the "invisible" tags were provided in the inspiring
MarkdownLint rule. After our users provided useful examples for us to consider,
we decided that a focused implementation of the rule would also benefit our users.
More information on this is listed below.

In our research, we found that there are two distinct sets of scenarios where it
is useful to have HTML blocks appear before other text is scanned in Markdown documents
for the purposes of this rule.

The first case is when an `h1` HTML block is used to present the
reader with a specially formatted title, often a centered image. This is common
in GitHub repositories where code like the following is used:

```Markdown
<h1 align="center"><img src="/path/to/image"/></h1>

This is a document with the top-level HTML heading satisfied.
```

To allow for this behavior to occur in the presence of an HTML, current and older
versions of this rule look determine if the first element in the document is an
HTML block. If so, the rule checks to see if the HTML block starts with a `h1`
tags and triggers the rule if not.

The second set of scenarios deals with "invisible" tags that can often occur
at the start of Markdown documents. These invisible tags are HTML tags that
affect the produced HTML document without producing a visible and direct impact
on the produced document. Examples of these include:

- applying a style sheet to the document

    - ```Markdown
      <link rel="stylesheet" href="/styles.css">
      # This file starts with a level 1 heading
      ```

- embedding of metadata into the document, such as [REUSE](https://reuse.software/)

    - ```Markdown
      <!--
      SPDX-FileCopyrightText: L33tCoder, Inc.

      SPDX-License-Identifier: MIT
      -->
      # This file starts with a level 1 heading
      ```

In these cases, the `invisible_tags` value is used to determine what HTML tags
this rule considers invisible. As the comment start tag `<!--` is universally
invisible, the internal list is primed with the tag `<!--`. Other HTML tags
to be considered as invisible for the sake of this rule may be added by
specifying a comma-separated set of values in the `invisible_tags` configuration
item. To cover the above scenarios, that list defaults to a value of `link`.

### Changing The Top Level

Configuration may be applied to change the expected top-level of
this rule from its default of `1` to another value. This should only be done
if an external process is generating the title of the document.
For example, if the `level` configuration value is set to `2`, then the following
document will not trigger this rule:

```Markdown
## This isn't an Atx H1 heading
```

## Fix Description

The reason for not being able to auto-fix this rule is context. Given that a top
level was not present in the document, context from the author is needed to determine
what text should be in that heading.

## Configuration

| Prefixes |
| --- |
| `plugins.md041.` |
| `plugins.first-line-heading.` |
| `plugins.first-line-h1.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `level` | `integer` | `1` | Level that is expected from the first heading (Atx or Setext) in the document. |
| `front_matter_title` | `string` | `title` | Name of the Front-Matter field that has the title associated with the document.** |
| `invisible_tags` | `string` | `link` | Comma separated string of HTML tag names to be considered as invisible. |

** Any leading or trailing space characters are removed from the `front_matter_title`
during processing. The `front_matter_title` value is expected to not to have the
`:` at the end. Therefore, a header value of `subject:` would be entered as `subject`.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD041](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md041---first-line-in-a-file-should-be-a-top-level-heading).

### Assumptions

It should be noted that this rule assumes that the Markdown document is
independent of other documents. If the Markdown document being scanned is meant
to be aggregated into a larger document, two paths are available:

1. Use the `level` configuration item to specify another level to start with,
   such as a value of `2`. This configuration would need to match the needs
   of the application that is performing the aggregation.
1. Disable the rule.

### Differences From MarkdownLint Rule

The difference between this rule and the original rule is in the handling of the
HTML comment tag. The original rule dealt with the HTML comment tag as invisible,
only triggering based on any information that occurred after that tag. This rule
was originally implemented to include any special tags, including the HTML comment
tag, in the triggering conditions for this rule.

Considering the evidence presented by users in [Issue 1400](https://github.com/jackdewinter/pymarkdown/issues/1400),
this behavior was changed for version `0.9.32`. While the inspiration for this rule
only counts the comment tag (`<!--`) as invisible, our team added configurable
support for defining tags that this rule considers invisible.
