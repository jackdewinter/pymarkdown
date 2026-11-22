# Rule - MD011

| Property | Value |
| --- | --- |
| Aliases | `md011`, `no-reversed-links` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

Inline links should use correct syntax with link text in brackets preceding the
URL in parentheses.

## Reasoning

### Consistency

Reversed link syntax creates invalid Markdown that fails to render as clickable
links, confusing readers. Correct syntax ensures consistent rendering across
parsers and preserves document integrity.

## Examples

### Failure Scenarios

<!-- pyml disable-num-lines 3 no-reversed-links -->
This rule triggers when inline link syntax has the brackets and parentheses transposed,
such as `(text)[url]` instead of `[text](url)`.

```Markdown
This link (is)[/transposed].
```

> **Explanation**: The `[]` brackets and `()` parentheses are transposed, creating
> an invalid inline link syntax. The rule requires that link text be enclosed in
> `[]` followed by the URL in `()`.

Unlike the previous example, this case uses a full absolute URL inside the parentheses
rather than a relative path, which is the most common real-world form of a reversed
link.

```Markdown
For more information, (click here)[https://example.com/docs].
```

> **Explanation**: The link text is enclosed in `()` parentheses and the absolute
> URL is enclosed in `[]` brackets — the exact transposition the rule targets. The
> use of a full `https://` URL does not exempt the pattern; the rule fires on any
> inline link where `()` precedes `[]` in this adjacent, reversed arrangement.

Unlike the previous examples, this case wraps the transposed pattern inside a
code span, showing that the rule still fires even when the pattern appears
within inline code.

```Markdown
The syntax `(text)[url]` is sometimes seen in drafts.
```

> **Explanation**: Unlike the previous examples, where the transposed pattern
> appears directly in prose, this case wraps the pattern inside a code span
> (backticks). The rule performs its check at the inline/leaf level, so
> enclosing the pattern in a code span does not suppress detection — the
> reversed `()...[]` arrangement is still identified and the rule fires.

### Correct Scenarios

This rule does not trigger when inline links use the correct syntax with `[]` preceding
`()`.

```Markdown
This link [is not](/transposed).
```

> **Explanation**: The link text is correctly enclosed in `[]` brackets, followed
> by the URL in `()` parentheses, satisfying the required inline link syntax.

Unlike the previous examples, this case includes a space between the closing parenthesis
and opening bracket, which prevents the syntax from being recognized as an inline
link.

```Markdown
This link (is not) [/transposed].
```

> **Explanation**: The space between the parentheses `()` and brackets `[]`
> breaks the direct adjacency the rule requires, so the reversed-link pattern
> (which mandates `()` immediately followed by `[]`) is not matched and the
> rule does not trigger.

Unlike the previous examples, this case places reversed link syntax inside a fenced
code block, where Markdown parsing is suppressed.

````Markdown
```text
This (reversed)[link] is in a code block.
```
````

> **Explanation**: Content within fenced code blocks is treated as literal text,
> not as Markdown syntax, so the rule does not apply here.

Unlike the previous examples, this case embeds reversed link syntax inside an HTML
comment block, which is also excluded from rule evaluation.

```Markdown
<!--
This (reversed)[link] is in an HTML comment.
-->
```

> **Explanation**: HTML blocks and comments are excluded from inline Markdown parsing,
> so reversed link patterns within them do not trigger the rule.

## Fix Description

The implementation for this feature is tracked [with this issue](https://github.com/jackdewinter/pymarkdown/issues/807).

## Configuration

| Prefixes |
| --- |
| `plugins.md011.` |
| `plugins.no-reversed-links.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD011](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md011---reversed-link-syntax).
