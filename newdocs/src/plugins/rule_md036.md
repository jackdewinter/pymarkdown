# Rule - MD036

| Property | Value |
| --- | --- |
| Aliases | `md036`, `no-emphasis-as-heading`, `no-emphasis-as-header` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Avoid using emphasis elements as headings.

## Reasoning

### Readability

Users unfamiliar with Markdown may mistakenly use emphasis (e.g., bold or italic) to simulate headings instead of proper heading syntax. Headings provide semantic structure that assistive technologies and parsers rely on, whereas emphasis lacks this meaning.

## Examples

### Failure Scenarios

This rule triggers when a single line of text is entirely within an emphasis element and does not end with configured punctuation.

```Markdown
**My document**

Lorem ipsum dolor sit amet...
```

> **Explanation**: The line `**My document**` is a single paragraph line where the **entirety** of the text is bolded (an emphasis element). It does not end with any punctuation characters configured in `plugins.md036.punctuation`. Therefore, it is flagged as a potential heading misuse.

This scenario also triggers when using italic emphasis markers instead of bold.

```Markdown
_Another section_

Consectetur adipiscing elit, sed do eiusmod.
```

> **Explanation**: Similar to the previous example, `_Another section_` is entirely italicized on a single line without trailing punctuation. The rule catches all emphasis types (bold, italic, etc.), not just bold.

### Correct Scenarios

This rule does not trigger when emphasis spans multiple lines, as the rule only applies to single-line paragraphs.

```Markdown
**My
document**

Lorem ipsum dolor sit amet...
```

> **Explanation**: The emphasized text `**My \n document**` breaks across two lines. The rule specifically targets single-line paragraphs where emphasis mimics a heading. Multi-line emphasis is not considered a heading substitute.

Unlike the previous example, this case includes non-emphasized text on the same line, so the text is not entirely emphasized.

```Markdown
_Almost a section_ heading

Consectetur adipiscing elit, sed do eiusmod.
```

> **Explanation**: The line `_Almost a section_ heading` contains both emphasized (`_Almost a section_`) and plain (` heading`) text. Because the **entirety** of the line is not within an emphasis element, it does not meet the violation criteria.

Unlike the previous examples, this emphasized line ends with a configured punctuation character, exempting it from the rule.

```Markdown
*But this is not a heading!*

Consectetur adipiscing elit, sed do eiusmod.
```

> **Explanation**: The line `*But this is not a heading!*` is entirely emphasized but ends with an exclamation mark (`!`), which is included in the default `punctuation` configuration (`.,;:!?。，；：？`). Lines ending with configured punctuation are excluded from this rule to avoid false positives on exclamations or questions.

## Fix Description

The reason auto-fixing is not available is the inherent uncertainty. The summary for
this rule specifically states:

> Emphasis possibly used instead of a heading element.

As this rule simply advises that it found cases that only appear to be headings
that are created with emphasis, it does not attempt to fix them.

## Configuration

| Prefixes |
| --- |
| `plugins.md036.` |
| `plugins.no-emphasis-as-heading.` |
| `plugins.no-emphasis-as-header.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `punctuation` | `string` | `.,;:!?。，；：？` | Punctuation characters that are considered sentence ending characters. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD036](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md036---emphasis-used-instead-of-a-heading)
and
[this article](https://cirosantilli.com/markdown-style-guide#emphasis-vs-headers).

### Differences From MarkdownLint Rule

The original rule did not work inside of Block Quote elements or List elements.
