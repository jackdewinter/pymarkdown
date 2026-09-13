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

Users unfamiliar with Markdown may mistakenly use emphasis (e.g., bold or italic)
to simulate headings instead of proper heading syntax. Headings provide semantic
structure that assistive technologies and parsers rely on, whereas emphasis lacks
this meaning.

## Examples

### Failure Scenarios

This rule triggers when a single line of text is entirely within an emphasis element
and does not end with configured punctuation.

```Markdown
**My document**

Lorem ipsum dolor sit amet...
```

> **Explanation**: The line `**My document**` is a single paragraph line where the
> **entirety** of the text is bold (an emphasis element). It does not end with any
> punctuation characters configured in `plugins.md036.punctuation`. Therefore, it
> is flagged as a potential heading misuse.

Unlike the previous example, this case uses italic emphasis markers (`_..._`) instead
of bold, demonstrating that the rule catches all emphasis types.

```Markdown
_Another section_

Consectetur adipiscing elit, sed do eiusmod.
```

> **Explanation**: Similar to the previous example, `_Another section_` is entirely
> italicized on a single line without trailing punctuation. The rule catches all
> emphasis types (bold, italic, etc.), not just bold.

Unlike the previous examples, this case uses asterisk (`*...*`) style italic markers,
confirming that the rule catches emphasis regardless of whether underscores or asterisks
are used as the delimiters.

```Markdown
*Yet another section*

Consectetur adipiscing elit, sed do eiusmod.
```

> **Explanation**: The line `*Yet another section*` is entirely italicized on a
> single line without trailing punctuation. Because asterisk-based emphasis is treated
> identically to underscore-based emphasis, the same violation criteria apply even
> though the delimiters (`*`) differ.

Unlike the previous examples, this case places the emphasized line inside a list
item, confirming that the rule is not limited to top-level paragraphs.

```Markdown
- **My item**
- Another item
```

> **Explanation**: The line `**My item**` is a single line where the entirety of
> the text is bold and does not end with a configured punctuation character. Even
> though it is nested inside a list, the rule still applies — the list context does
> not exempt the line. The rule flags it for the same criteria as the earlier examples
> (single line, entirely emphasized, no configured trailing punctuation).

Unlike the previous examples, this case places the emphasized line inside a block
quote, confirming that quoted content is also scanned.

```Markdown
> **Quoted section**
>
> Some quoted text.
```

> **Explanation**: The line `**Quoted section**` is a single line where the entirety
> of the text is bold and does not end with a configured punctuation character.
> The block-quote marker (`>`) is stripped before the rule evaluates the line, so
> the same single-line, entirely-emphasized, no-configured-punctuation criteria
> apply. The rule flags it for the same reasons as the earlier examples.

Unlike the previous examples, this case demonstrates a **configuration-dependent**
failure: `punctuation` has been set to `.!`, so the trailing `?` no longer counts
as an exempting character.

```Markdown
**My section?**

Lorem ipsum dolor sit amet...
```

> **Explanation**: The line `**My section?**` is entirely emphasized on a single
> line. It ends with a question mark (`?`), which would normally exempt it under
> the default `punctuation` value (`.,;:!?。，；：？`). However, with `punctuation`
> set to `.!`, the trailing `?` no longer counts as a configured punctuation character.
> The line therefore fails on the same criteria as the earlier examples: single
> line, entirely emphasized, no configured trailing punctuation.

### Correct Scenarios

This rule does not trigger when the emphasized text spans multiple lines, since
the rule only applies to single-line paragraphs.

```Markdown
**My
document**

Lorem ipsum dolor sit amet...
```

> **Explanation**: The emphasized text spans two lines (a line break inside the
> `**…**` pair). The rule specifically targets single-line paragraphs where emphasis
> mimics a heading. Multi-line emphasis is not considered a heading substitute.

Unlike the previous example, this case includes non-emphasized text on the same
line, so the text is not entirely emphasized.

```Markdown
_Almost a section_ heading

Consectetur adipiscing elit, sed do eiusmod.
```

> **Explanation**: The line `_Almost a section_ heading` contains both emphasized
> (`_Almost a section_`) and plain (`heading`) text. Because the **entirety** of
> the line is not within an emphasis element, it does not meet the violation criteria.

Unlike the previous examples, this emphasized line ends with a configured punctuation
character, exempting it from the rule.

```Markdown
*But this is not a heading!*

Consectetur adipiscing elit, sed do eiusmod.
```

> **Explanation**: The line `*But this is not a heading!*` is entirely emphasized
> but ends with an exclamation mark (`!`), which is included in the default `punctuation`
> configuration (`.,;:!?。，；：？`). Lines ending with configured punctuation are excluded
> from this rule to avoid false positives on exclamations or questions.

Unlike the previous example, this case has emphasized text that contains a link,
which the rule correctly treats as non-heading content.

```Markdown
[**Click here**](https://example.com)

Consectetur adipiscing elit, sed do eiusmod.
```

> **Explanation**: The line `[**Click here**](https://example.com)` is a link whose
> visible text is bold. Because the emphasized text is part of a link rather than
> a standalone emphasized paragraph line, it does not meet the violation criteria.
> Links are a common, legitimate use of emphasis that this rule intentionally does
> not flag.

Unlike the previous example, this case has emphasized text that is part of a longer
sentence rather than a standalone line, which the rule correctly treats as inline
emphasis.

```Markdown
This is a paragraph with **important** text that continues after the emphasis.

Consectetur adipiscing elit, sed do eiusmod.
```

> **Explanation**: The first line contains emphasized text (`**important**`) embedded
> within a longer sentence. Because the **entirety** of the line is not within an
> emphasis element, it does not meet the violation criteria. Inline emphasis within
> running text is a normal, expected use of Markdown and is not confused with a
> heading.

## Fix Description

A line that is fully emphasized may be intentional emphasis rather than a misused
heading, so an automatic conversion to a heading could change the author's intended
meaning. For this reason, the rule only reports the case and does not modify the
content.

## Configuration

| Prefixes |
| --- |
| `plugins.md036.` |
| `plugins.no-emphasis-as-heading.` |
| `plugins.no-emphasis-as-header.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `punctuation` | `string` | `.,;:!?。，；：？` | Punctuation characters (ASCII and CJK full-width) that are considered sentence-ending characters. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD036](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md036---emphasis-used-instead-of-a-heading)
and
[Emphasis vs. Headers in Markdown](https://cirosantilli.com/markdown-style-guide#emphasis-vs-headers).

### Differences From MarkdownLint Rule

The original rule did not work inside Block Quote elements or List elements.
