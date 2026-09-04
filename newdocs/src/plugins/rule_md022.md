# Rule - MD022

| Property | Value |
| --- | --- |
| Aliases | `md022`, `blanks-around-headings`, `blanks-around-headers` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

Headings should be surrounded by blank lines.

## Reasoning

### Readability

Blank lines around headings improve readability by visually separating headings from surrounding content, making document structure clearer for readers.

## Examples

### Failure Scenarios

This rule triggers when a heading is immediately followed by text without a required blank line, or immediately preceded by text without a required blank line.

```Markdown
Section text.
## Heading 2
Section text.
```

> **Explanation**: The heading `## Heading 2` is directly preceded by `"Section text."` without a blank line in between, and directly followed by `"Section text."` without a blank line after. The rule requires blank lines around headings for readability and consistent parsing.

### Correct Scenarios

This rule does not trigger when headings are properly surrounded by blank lines.

```Markdown
Section text.
## Heading 2
Section text.
```

> **Explanation**: The heading `## Heading 2` is correctly surrounded by blank lines on both sides. There is a blank line before the heading and a blank line after the heading, satisfying the rule's requirements.

Unlike the previous example, this case shows a heading at the beginning of the document with no preceding content.

```Markdown
# Heading 1

Section text.
```

> **Explanation**: The heading `# Heading 1` is at the start of the document, so there is no preceding text that needs a blank line before it. There is a blank line after the heading before `Section text.`, which satisfies the rule.

Unlike the previous example, this case shows multiple headings where the last heading is at the end of the document with no following content.

```Markdown
# Heading 1

Section text.

## Heading 2
```

> **Explanation**: The heading `## Heading 2` is at the end of the document, so there is no following text that needs a blank line after it.

## Fix Description

The implementation for this feature is tracked [with this issue](https://github.com/jackdewinter/pymarkdown/issues/815).

## Configuration

| Prefixes |
| --- |
| `plugins.md022.` |
| `plugins.blanks-around-headings.` |
| `plugins.blanks-around-headers.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `lines_above` | `integer` | `1` | Number of lines that are expected before any heading element. |
| `lines_below` | `integer` | `1` | Number of lines that are expected after any heading element. |

If either the `lines_above` or `lines_below` values are set to anything other than
`0` or `1`,
[Rule md012](./rule_md012.md)
will also need to be set to avoid having that rule fire.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD022](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md022---headings-should-be-surrounded-by-blank-lines).

### Differences From MarkdownLint Rule

The differences between this rule and the inspiring rule are largely
cosmetic.  In scenarios where the heading is part of a Block Quote or
a List, the column number was changed to reflect the start of the
heading element itself, not the start of the line.  In addition, the
original rule did not correctly assess a handful of boundary scenarios with
Thematic Break elements and HTML Block elements before and after the
heading elements.
