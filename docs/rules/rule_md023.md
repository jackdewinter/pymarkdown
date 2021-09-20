# Rule - MD023

| Aliases |
| --- |
| `md023` |
| `heading-start-left` |
| `header-start-left` |

## Summary

Headings must start at the beginning of the line.

## Reasoning

### Correctness

During research, more than half the parsers failed to detect a heading element
if it is preceded by any leading whitespace.  In those cases, the text is
parsed as normal text within a Paragraph element.  By removing any leading
whitespaces, any heading elements that were missed before were then properly
recognized.

## Examples

### Failure Scenarios

This rule triggers when one or more whitespace characters precedes
the Heading element:

```Markdown
  # This is a bad heading

  This is also a bad heading
  ==========================

This is also a bad heading
  ==========================

  This is also a bad heading
==========================
```

With respect to multiple line SetExt Heading elements, this rule triggers
when any line within the SetExt Heading element has leading spaces:

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

### Correct Scenarios

This rule does not trigger when there are no whitespace characters
preceding any Heading elements:

```Markdown
# This is a bad heading

This is also a bad heading
==========================
```

## Configuration

| Prefixes |
| --- |
| `plugins.md023.` |
| `plugins.heading-start-left.` |
| `plugins.header-start-left.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD023](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md023---headings-must-start-at-the-beginning-of-the-line).

### Differences From MarkdownLint Rule

While the Atx Heading elements in the original rule only had one
small syntactic issue (reporting the start of the line for a failure
scenario instead of the start of the token), SetExt Heading elements
did not perform as well.

When a failure scenario for the original rule was present in a
Block Quote element, the original rule would trigger correctly.
However, when the same spacing was provided for a List element,
the original rule would not trigger.  In addition, the original
rule would not trigger if there was any leading space on multiple
line SetExt Heading elements after the first line or on the
boundary line (`===` or `---`) itself.

In addition, because multiple line SetExt Headings were not
considered properly in the original rule, any failure scenarios
only reported a problem with the first line of the SetExt Heading
text.  To make this more general and to avoid having multiple
failures being reported for a single SetExt Heading element,
the reported position was moved to the start of the boundary
line of the SetExt Heading element.
