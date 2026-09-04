# Rule - MD028

| Property | Value |
| --- | --- |
| Aliases | `md028`, `no-blanks-blockquote` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Do not include blank lines inside block quotes.

## Reasoning

### Consistency

Blank lines inside block quotes can cause different Markdown parsers to interpret the content as separate block quotes or mixed block quote/paragraph structures. Avoiding blank lines ensures the block quote is parsed as a single, continuous unit, improving document consistency across tools and readers.

## Examples

### Failure Scenarios

This rule triggers when there are one or more blank lines between two block quote sections:

```Markdown
> This is one section of a block quote

> This is the other section.
```

> **Explanation**: This example violates the rule because there is a blank line between the two block quote sections. The blank line causes the block quotes to be treated as separate sections, which can lead to inconsistent parsing across different Markdown parsers.

Unlike the previous example, this scenario demonstrates how Markdown's laziness rules can cause a paragraph that appears standalone to be absorbed into the preceding block quote, followed by a blank line before the next block quote section.

```Markdown
> This is one section of a block quote
This looks like its own paragraph but is really part of the above block quote.

> This is the other section.
```

> **Explanation**: This example violates the rule because, due to Markdown's laziness rules, the paragraph starting with "This looks like" is actually part of the previous block quote. The blank line before the second block quote section causes the parser to treat the subsequent block quote as a separate section, leading to inconsistent parsing.

### Correct Scenarios

This rule does not trigger when there is no blank line between block quote sections, keeping them as a single continuous block quote.

```Markdown
> This is one section of a block quote
# Not A Blank Line
> This is the other section.
```

> **Explanation**: This example satisfies the rule because there is no blank line between the block quote sections. They are treated as a single continuous block quote, avoiding parser inconsistencies.

This scenario differs from the previous one by including a blank line after the first block quote, but the blank line is followed by a regular paragraph (not another block quote), so the rule does not trigger.

```Markdown
> This is one section of a block quote

This is its own paragraph.
> This is the other section.
```

> **Explanation**: This example satisfies the rule because, although there is a blank line after the first block quote section, the blank line is followed by a regular paragraph element, not another block quote. The rule only triggers when blank lines appear directly between consecutive block quote sections.

This scenario includes an additional blank line between the intervening paragraph and the second block quote, unlike the previous example which had no blank line between the paragraph and the second block quote.

```Markdown
> This is one section of a block quote

This is its own paragraph.

> This is the other section.
```

> **Explanation**: This example satisfies the rule because, although there is a blank line after the first block quote section, it is followed by a regular paragraph (not another block quote). The rule only triggers when blank lines separate block quote sections from each other, not when they separate block quotes from other elements.

## Fix Description

The reason for not being able to auto-fix this rule is clarity. Given the Markdown
example from above:

```Markdown
> This is one section of a block quote
This looks like its own paragraph but is really part of the above block quote.

> This is the other section.
```

it is unclear if the second line that starts with `This looks like` is part of
the block quote or if it is in its own paragraph following the block quote. As the
context of that line is not clear, any fix to that line would also be unclear.

## Configuration

| Prefixes |
| --- |
| `plugins.md028.` |
| `plugins.no-blanks-blockquote.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD028](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md028---blank-line-inside-blockquote).
