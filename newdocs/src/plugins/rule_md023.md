# Rule - MD023

| Property | Value |
| --- | --- |
| Aliases | `md023`, `heading-start-left`, `header-start-left` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Start every heading at the beginning of the line.

## Reasoning

### Correctness

Leading whitespace before a heading marker makes the same heading render
differently across parsers, breaking the document outline and confusing
human readers and accessibility tools that rely on a predictable heading
hierarchy.

## Examples

### Failure Scenarios

This rule triggers when one or more whitespace characters precede an Atx heading
marker.

```Markdown
  # This heading has leading whitespace
```

> **Explanation**: This example fails because the Atx heading marker (`#`) is preceded
> by two leading spaces. The rule requires headings to start at the very beginning
> of the line with no leading whitespace.

Unlike the previous Atx heading example, this scenario shows leading whitespace
on both lines of a Setext heading title.

```Markdown
  This heading has leading whitespace
  ===================================
```

> **Explanation**: This example fails because the Setext heading title line is preceded
> by leading spaces. The rule requires that the heading content start at the beginning
> of the line.

Unlike the previous examples which show leading whitespace on both lines, this scenario
shows leading whitespace on the Setext underline.

```Markdown
This heading has leading whitespace
  ===================================
```

> **Explanation**: This example fails because the Setext underline (`===`) is preceded
> by leading spaces. The rule requires the underline to start at the beginning of
> the line.

Unlike the previous examples which demonstrate single-line Setext headings, this
scenario shows leading whitespace on an intermediate line of a multi-line Setext
heading title.

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

> **Explanation**: This example fails because one line of the multi-line Setext
> heading title containing "this line" has leading whitespace. The rule requires
> that *every* line of the heading content start at the beginning of the line.

Unlike the previous examples which demonstrate headings at the document root level,
this scenario shows a heading with leading whitespace nested inside a block quote.

```Markdown
>  # This heading has leading whitespace
```

> **Explanation**: This example fails because the Atx heading marker (`#`) is preceded
> by leading whitespace even though it is inside a block quote. The rule requires
> that headings start at the beginning of the line regardless of nesting context.

Unlike the previous examples which demonstrate headings at the document root level
or inside block quotes, this scenario shows a heading with leading whitespace nested
inside a list item.

```Markdown
+  # This heading has leading whitespace
```

> **Explanation**: This example fails because the Atx heading marker (`#`) is preceded
> by leading whitespace even though it is inside a list item. The rule requires
> that headings start at the beginning of the line regardless of nesting context.

### Correct Scenarios

This rule does not trigger when there are no whitespace characters preceding the
Atx heading.

```Markdown
# This is a good heading
```

> **Explanation**: This example passes because the Atx heading element starts at
> the very beginning of the line with no leading whitespace.

Unlike the previous Atx heading example, this scenario demonstrates a Setext
heading that starts at the beginning of the line with no leading whitespace.

```Markdown
This is also a good heading
==========================
```

> **Explanation**: This example passes because the Setext heading element starts
> at the very beginning of the line with no leading whitespace.

Unlike the previous examples which demonstrate headings at the document root
level, this scenario shows an Atx heading inside a block quote with no leading
whitespace after the block-quote marker.

```Markdown
> # This is a good heading
```

> **Explanation**: This example passes because the Atx heading marker (`#`) follows
> the block-quote marker (`>`) and its single space character with no additional
> leading whitespace, so the heading content starts at the beginning of the line
> relative to the block-quote context.

Unlike the previous examples which demonstrate headings at the document root level
or inside block quotes, this scenario shows an Atx heading inside a list item with
no leading whitespace after the list-item marker.

```Markdown
+ # This is a good heading
```

> **Explanation**: This example passes because the Atx heading marker (`#`) follows
> the list-item marker (`+`) and its single space character with no additional leading
> whitespace, so the heading content starts at the beginning of the line relative
> to the list-item context.

## Fix Description

The autofix removes any leading whitespace that appears before the `#`
marker of an Atx heading, before the title text of a Setext heading, or
before the `===` / `---` boundary line of a Setext heading, so that every
part of the heading starts at the beginning of the line.

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
rule would not trigger if there was any leading space on multi-line Setext heading
elements after the first line or on the
boundary line (`===` or `---`) itself.

In addition, because multi-line Setext Headings were not
considered properly in the original rule, any failure scenarios
only reported a problem with the first line of the Setext Heading
text. To make this more general and to avoid having multiple
Rule Failures being reported for a single Setext Heading element,
the reported position was moved to the start of the boundary
line of the Setext Heading element.
