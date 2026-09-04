# Rule - MD012

| Property | Value |
| --- | --- |
| Aliases | `md012`, `no-multiple-blanks` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

Do not use multiple consecutive blank lines.

## Reasoning

### Simplicity

Multiple consecutive blank lines are visually redundant in Markdown, as parsers treat them identically to a single blank line. Using only one blank line improves readability and file cleanliness without affecting document structure.

## Examples

### Failure Scenarios

This rule triggers when there are more than the configured maximum number of consecutive blank lines between elements.

```Markdown
this is a line


this is another line
```

> **Explanation**: This example has two consecutive blank lines between the paragraphs. The default maximum is `1`, so exceeding this limit triggers the rule.

Unlike the previous example, this scenario demonstrates multiple blank lines inside a block quote element.

```Markdown
> first paragraph
>
>
> second paragraph
```

> **Explanation**: This example has two consecutive blank lines within a block quote. While some older tools ignored this case, this rule enforces consistency across all document structures. The multiple blank lines are still visually redundant and trigger the rule even when nested inside quotes.

This scenario differs from the first by showing a document configured with a higher `maximum` value, where the blank lines exceed that custom limit.

```Markdown
this is a line



this is another line
```

> **Explanation**: This example has three consecutive blank lines between paragraphs. If the rule is configured with `maximum: 2`, this would trigger because the count (3) exceeds the configured maximum (2). This demonstrates that the rule respects custom configuration values rather than only the default of `1`.

### Correct Scenarios

This rule does not trigger when the number of consecutive blank lines is within the configured maximum.

```Markdown
this is a line

this is another line
```

> **Explanation**: This example has only one blank line between the paragraphs. Since the default maximum is `1`, this complies with the rule.

This scenario differs from the first by showing a document configured with a higher `maximum` value, where the number of blank lines meets but does not exceed that custom limit.

```Markdown
this is a line


this is another line
```

> **Explanation**: This example has two consecutive blank lines between paragraphs. If the rule is configured with `maximum: 2`, this complies with the rule because the count (2) does not exceed the configured maximum (2).

Unlike the previous examples, this scenario demonstrates a block quote with only one blank line, mirroring the failure case but in compliance with the rule.

```Markdown
> first paragraph
>
> second paragraph
```

> **Explanation**: This example has only one blank line within a block quote. Since the default maximum is `1`, this complies with the rule. This demonstrates that the rule enforces consistency across all document structures while still allowing a single blank line for readability.

## Fix Description

The implementation for this feature is tracked [with this issue](https://github.com/jackdewinter/pymarkdown/issues/933).

## Configuration

| Prefixes |
| --- |
| `plugins.md012.` |
| `plugins.no-multiple-blanks.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `maximum` | `integer` | `1` | Number of blank lines to exceed before this rule triggers |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD012](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md012---multiple-consecutive-blank-lines).

### Differences From MarkdownLint Rule

The first difference was that the original rule did not fire with blank lines placed
within Block Quote elements, such as this example:

```Markdown
> block quote before
>
>
> block quote after
```
