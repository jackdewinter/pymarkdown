# Rule - MD037

| Property | Value |
| --- | --- |
| Aliases | `md037`, `no-space-in-emphasis` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Do not use spaces inside emphasis markers.

## Reasoning

### Correctness

This rule detects cases where spaces inside emphasis markers (`*` or `**`) prevent parsers from rendering text as bold or italic. Most parsers require emphasis characters to directly adjoin the emphasized text; internal whitespace breaks this rendering. Therefore, this rule flags matched pairs of emphasis characters where whitespace appears immediately inside the opening or closing marker.

Note: This rule does not currently handle nested emphasis cases (e.g., `***` for bold italics).

## Examples

### Failure Scenarios

This rule triggers when matching emphasis characters occur within the same paragraph with Unicode whitespace around either of the emphasis characters. The obvious case is:

```Markdown
this is ** not some ** bold text
```

> **Explanation**: This example fails because there are spaces immediately inside both the opening (`**`) and closing (`**`) emphasis markers. The rule requires that emphasis characters directly adjoin the text being emphasized.

Unlike the previous example, this case has whitespace only before the opening emphasis marker.

```Markdown
this is ** not some** bold text
```

> **Explanation**: This example fails because there is a space immediately inside the opening emphasis marker (`**`). Even though the closing marker is correct, the presence of internal whitespace on one side is sufficient to trigger the rule.

Unlike the previous example, this case has whitespace only after the closing emphasis marker.

```Markdown
this is **not some ** bold text
```

> **Explanation**: This example fails because there is a space immediately inside the closing emphasis marker (`**`). Even though the opening marker is correct, the presence of internal whitespace on one side is sufficient to trigger the rule.

Unlike the previous examples, this case uses single asterisks (*) for italics instead of double asterisks (**) for bold.

```Markdown
this is * not some * italic text
```

> **Explanation**: This example fails because there are spaces immediately inside both the opening (`*`) and closing (`*`) emphasis markers. The rule applies to both single and double emphasis markers, requiring that they directly adjoin the emphasized text.

### Correct Scenarios

This rule does not trigger when there is no whitespace present on the inside of the emphasis markers.

```Markdown
this is **some** bold text
```

> **Explanation**: This example passes because the emphasis markers (`**`) directly adjoin the text "some" without any internal whitespace. This is the correct format for emphasis.

Unlike the previous example, this case uses single asterisks (`*`) for italics instead of double asterisks (`**`) for bold.

```Markdown
this is *some* italic text
```

> **Explanation**: This example passes because the emphasis markers (`*`) directly adjoin the text "some" without any internal whitespace. This is the correct format for italics, and the rule does not trigger when emphasis is properly formatted.

Unlike the previous examples, this case contains multiple emphasized sections within the same paragraph.

```Markdown
this is **bold** and *italic* text in one line
```

> **Explanation**: This example passes because both emphasis pairs (`**` and `*`) directly adjoin their respective text without any internal whitespace. The rule evaluates each pair independently, and both are correctly formatted.

## Fix Description

Within the block of emphasized text, any leading and trailing whitespace is removed.

## Configuration

| Prefixes |
| --- |
| `plugins.md037.` |
| `plugins.no-space-in-emphasis.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD037](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md037---spaces-inside-emphasis-markers).

### Differences From MarkdownLint Rule

The original rule did not distinguish between probable emphasis situations
and emphasis sequences. Therefore, text such as `this * is not * emphasis`
triggered on both the first and the second emphasis characters.
This rule looks for scenarios where there are a matched pair of emphasis
characters, instead of just looking for those individual characters.
