# Rule - MD023

| Property | Value |
| --- | --- |
| Aliases | `md023`, `heading-start-left`, `header-start-left` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Headings must start at the beginning of the line.

## Reasoning

### Correctness

Headings with leading whitespace may be misrendered as plain text by some Markdown parsers, breaking the document outline and confusing human readers and accessibility tools that rely on proper heading hierarchy.

## Examples

### Failure Scenarios

This rule triggers when one or more whitespace characters precedes the Heading element, including the title line of a Setext heading, the underline of a Setext heading, or both.

```Markdown
  # This is a bad heading

  This is also a bad heading
  ==========================

This is also a bad heading
  ==========================

  This is also a bad heading
==========================
```

> **Explanation**: This example fails because leading whitespace is present on the Atx heading marker, the Setext heading title, and the Setext heading underline. The rule requires headings to start at the beginning of the line without any leading spaces.

Unlike the previous examples which show leading spaces on the first line or underline, this scenario shows leading spaces on an intermediate line of a multi-line Setext heading title.

```Markdown
This
heading
is
good
except
for
  this line
==========================
```

> **Explanation**: This example fails because the Setext heading title spans multiple lines, and one of those lines ("  this line") has leading whitespace. The rule requires that *every* line of the heading content (and the underline) starts at the beginning of the line.

Unlike the previous examples which demonstrate headings at the document root level, this scenario shows a heading with leading whitespace nested inside a block quote.

```Markdown
>  # This is a bad heading
```

> **Explanation**: This example fails because the Atx heading marker (`#`) is preceded by leading whitespace even though it is inside a block quote. The rule requires that headings start at the beginning of the line regardless of nesting context.

Unlike the previous examples which demonstrate headings at the document root level or inside block quotes, this scenario shows a heading with leading whitespace nested inside a list item.

```Markdown
+  # This is a bad heading
```

> **Explanation**: This example fails because the Atx heading marker (`#`) is preceded by leading whitespace even though it is inside a list item. The rule requires that headings start at the beginning of the line regardless of nesting context.

### Correct Scenarios

This rule does not trigger when there are no whitespace characters preceding the Atx heading.

```Markdown
# This is a good heading
```

> **Explanation**: This example passes because the Atx heading element starts at the very beginning of the line with no leading whitespace.

Unlike the previous Atx heading example, this scenario demonstrates a Setext heading that correctly starts at the beginning of the line with no leading whitespace.

```Markdown
This is also a good heading
==========================
```

> **Explanation**: This example passes because the Setext heading element starts at the very beginning of the line with no leading whitespace.

## Fix Description

Any leading spaces at the start of an Atx Heading element or within any part of
a Setext Heading element are removed.

## Configuration

| Prefixes |
| --- |
| `plugins.md023.` |
| `plugins.heading-start-left.` |
| `plugins.header-start-left.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD023](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md023---headings-must-start-at-the-beginning-of-the-line).

### Differences From MarkdownLint Rule

While the Atx Heading elements in the original rule only had one
small syntactic issue (reporting the start of the line for a failure
scenario instead of the start of the token), Setext Heading elements
did not perform as well.

When a failure scenario for the original rule was present in a
Block Quote element, the original rule would trigger correctly.
However, when the same spacing was provided for a List element,
the original rule would not trigger. In addition, the original
rule would not trigger if there was any leading space on multiple
line Setext Heading elements after the first line or on the
boundary line (`===` or `---`) itself.

In addition, because multiple line Setext Headings were not
considered properly in the original rule, any failure scenarios
only reported a problem with the first line of the Setext Heading
text. To make this more general and to avoid having multiple
Rule Failures being reported for a single Setext Heading element,
the reported position was moved to the start of the boundary
line of the Setext Heading element.
