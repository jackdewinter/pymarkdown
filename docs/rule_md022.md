# Rule - MD022

| Aliases |
| --- |
| `md022` |
| `blanks-around-headings` |
| `blanks-around-headers` |

## Summary

Headings should be surrounded by blank lines.

## Reasoning

From a readability point of view, it makes sense to have at least a single
line before and after a heading to visually separate it from the rest of
the content.  In addition, some parsers do not handle an Atx Heading element
properly unless there is a blank line before it.

## Examples

### Failure Scenarios

This rule triggers when the configured number of blank lines before (above)
or after (below) any heading element is not present.  The configured number
of blank lines defaults to `1` in both cases.

```Markdown
# Heading 1
Section text.

Still section 1 text.
## Heading 2
```

### Correct Scenarios

This rule does not trigger when the configured number of blank lines appear
on both side of the heading element.  In the special case of the first heading
in the document, that heading does not require any blank lines before it, but
only in the scenario where there are no other elements Markdown elements before it.

```Markdown
# Heading 1

Section text.

Still section 1 text.

## Heading 2

Next section text.
```

## Configuration

| Prefixes |
| --- |
| `plugins.md022.` |
| `plugins.blanks-around-headings.` |
| `plugins.blanks-around-headers.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled by default. |
| `lines_above` | `integer` | `1` | Number of lines that are expected before any heading element. |
| `lines_below` | `integer` | `1` | Number of lines that are expected after any heading element. |

If either the `lines_above` or `lines_below` values are set to anything other than
`0` or `1`,
[Rule md012](https://github.com/jackdewinter/pymarkdown/blob/main/docs/rule_md012.md)
will also need to be set to avoid having that rule fire.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD022](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md022---headings-should-be-surrounded-by-blank-lines).

### Differences From MarkdownLint Rule

The differences between this rule and the inspiring rule were largely
cosmetic.  In scenarios where the heading is part of a Block Quote or
a List, the column number was changed to reflect the start of the
heading element itself, not the start of the line.  In addition, the
original rule failed to correct assess some boundary scenarios with
Thematic Break elements and HTML Block elements before and after the
heading elements.
