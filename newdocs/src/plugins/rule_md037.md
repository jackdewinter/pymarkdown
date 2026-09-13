# Rule - MD037

| Property | Value |
| --- | --- |
| Aliases | `md037`, `no-space-in-emphasis` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Do not use spaces inside emphasis markers.

## Reasoning

### Readability

Emphasis is a core readability cue: bold and italic signal emphasis, tone, and definition
to human readers. When a parser fails to render emphasis because of internal whitespace,
readers see literal * or ** characters instead of formatted text, which breaks visual
scanning and can hide meaning. This rule keeps emphasis visually reliable by requiring
the markers to adjoin their text directly.

Note: This rule does not currently handle nested emphasis cases (e.g., `***` for
bold italics).

## Examples

### Failure Scenarios

This rule triggers when whitespace appears immediately inside the opening or closing
emphasis markers.

```Markdown
this is ** not some ** bold text
```

> **Explanation**: This example fails because there are spaces immediately inside
> both the opening (`**`) and closing (`**`) emphasis markers. The rule requires
> that emphasis characters directly adjoin the text being emphasized.

Unlike the previous example, this case has whitespace only after the first emphasis
marker.

```Markdown
this is ** not some** bold text
```

> **Explanation**: This example fails because there is a space immediately inside
> the opening emphasis marker (`**`). Even though the closing marker is correct,
> the presence of internal whitespace on one side is sufficient to trigger the rule.

Unlike the previous example, this case has whitespace only after the closing emphasis
marker.

```Markdown
this is **not some ** bold text
```

> **Explanation**: This example fails because there is a space immediately inside
> the closing emphasis marker (`**`). Even though the opening marker is correct,
> the presence of internal whitespace on one side is sufficient to trigger the rule.

Unlike the previous examples, this case uses single asterisks (`*`) for italics
instead of double asterisks (`**`) for bold.

```Markdown
this is * not some * italic text
```

> **Explanation**: This example fails because there are spaces immediately inside
> both the opening (`*`) and closing (`*`) emphasis markers. The rule applies to
> both single and double emphasis markers, requiring that they directly adjoin the
> emphasized text.

Unlike the previous examples, this case uses underscores (`_`) instead of asterisks
(`*`) to mark italics.

```Markdown
this is _ not some _ italic text
```

> **Explanation**: This example fails because there are spaces immediately inside
> both the opening (`_`) and closing (`_`) emphasis markers. The rule applies equally
> to underscore and asterisk emphasis, requiring that each marker directly adjoin
> the emphasized text.

Unlike the previous examples, this case uses double underscores (`__`) to mark bold
text.

```Markdown
this is __ not some __ bold text
```

> **Explanation**: This example fails because there are spaces immediately inside
> both the opening (`__`) and closing (`__`) emphasis markers. The rule treats `__`
> bold emphasis the same as `**` bold emphasis, requiring the markers to adjoin
> the text directly.

### Correct Scenarios

This rule does not trigger when there is no whitespace present on the inside of
the emphasis markers.

```Markdown
this is **some** bold text
```

> **Explanation**: This example passes because the emphasis markers (`**`) directly
> adjoin the text "some" without any internal whitespace. This is the correct format
> for emphasis.

Unlike the previous example, this case uses single asterisks (`*`) for italics instead
of double asterisks (`**`) for bold.

```Markdown
this is *some* italic text
```

> **Explanation**: This example passes because the emphasis markers (`*`) directly
> adjoin the text "some" without any internal whitespace. This is the correct format
> for italics, and the rule does not trigger when emphasis is properly formatted.

Unlike the previous examples, this case contains multiple emphasized sections within
the same paragraph.

```Markdown
this is **bold** and *italic* text in one line
```

> **Explanation**: This example passes because both emphasis pairs (`**` and `*`)
> directly adjoin their respective text without any internal whitespace. The rule
> evaluates each pair independently, and both are correctly formatted.

Unlike the previous examples, this case places the emphasis at the very beginning
of a paragraph, a position where some parsers are most finicky about marker adjacency.

```Markdown
**Bold** leads the paragraph.
```

> **Explanation**: This example passes because the opening `**` marker is the first
> character of the paragraph and directly adjoins the word "Bold", with no internal
> whitespace. Parsers commonly mishandle emphasis that begins a line, so confirming
> the rule does not misfire here is important.

Unlike the previous example, this case places the emphasized span immediately after
a sentence-ending period.

```Markdown
Note this.**bold**
```

> **Explanation**: This example passes because the opening `**` marker directly
> adjoins
> the word "bold" and the closing `**` marker directly adjoins it on the right,
> with no internal whitespace on either side. The preceding period is *outside*
> the emphasis span, and the rule correctly treats this as valid emphasis.

Unlike the previous examples, this case uses underscores (`_`) instead of asterisks
(`*`) to mark italics.

```Markdown
this is _some_ italic text
```

> **Explanation**: This example passes because the underscore markers (`_`) directly
> adjoin the text "some" with no internal whitespace. The rule applies the same
> adjacency requirement to underscores as it does to asterisks, so correctly formatted
> underscore emphasis does not trigger the rule.

Unlike the previous examples, this case uses backslash-escaped asterisks (`\*`)
to represent literal asterisk characters rather than emphasis markers.

```Markdown
this \* is not \* emphasis
```

> **Explanation**: This example passes because the backslashes escape the asterisks,
> making them literal characters rather than emphasis markers. Since no emphasis
> is being formed, there are no emphasis markers with internal whitespace to evaluate,
> and the rule correctly does not trigger.

## Fix Description

The spaces immediately inside the opening or closing emphasis markers are removed,
so that the emphasis characters directly adjoin the emphasized text.

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
