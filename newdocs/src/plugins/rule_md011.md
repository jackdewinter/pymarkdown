# Rule - MD011

| Property | Value |
| --- | --- |
| Aliases | `md011`, `no-reversed-links` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

Inline links should use correct syntax with link text in brackets preceding the URL in parentheses.

## Reasoning

### Correctness

Reversed link syntax creates invalid Markdown that fails to render as clickable links, confusing readers. Correct syntax ensures consistent rendering across parsers and preserves document integrity.

## Examples

### Failure Scenarios

This rule triggers when inline link syntax has the brackets and parentheses transposed, such as `(text)[url]` instead of `[text](url)`.

<!-- pyml disable-num-lines 3 no-reversed-links -->
```Markdown
This link (is)[/transposed].
```

> **Explanation**: The `[]` brackets and `()` parentheses are transposed, creating an invalid inline link syntax. The rule requires that link text be enclosed in `[]` followed by the URL in `()`.

### Correct Scenarios

This rule does not trigger when inline links use the correct syntax with `[]` preceding `()`.

```Markdown
This link [is not](/transposed).
```

> **Explanation**: The link text is correctly enclosed in `[]` brackets, followed by the URL in `()` parentheses, satisfying the required inline link syntax.

Unlike the previous example, this case uses [Markdown Extra](https://en.wikipedia.org/wiki/Markdown_Extra) footnote syntax where `()` precedes `[]`, which intentionally resembles a reversed link but is excluded from the rule.

```Markdown
... to it (as an example)[^footnote]. Therefore...
```

> **Explanation**: The apparent URL section starts with a `^` character (indicating a footnote reference), so this rule does not trigger. This accommodation allows legal footnote sequences that would otherwise appear as reversed links.

Unlike the previous examples, this case includes a space between the closing parenthesis and opening bracket, which prevents the syntax from being recognized as an inline link.

```Markdown
This link (is not) [/transposed].
```

> **Explanation**: The space between the parentheses `()` and brackets `[]` breaks the potential reversed link pattern, so this rule does not trigger. The rule only applies to cases where the brackets and parentheses are directly adjacent in a reversed order without intervening whitespace.

Unlike the previous examples, this case places reversed link syntax inside a fenced code block, where Markdown parsing is suppressed.

````Markdown
```text
This (reversed)[link] is in a code block.
```
````

> **Explanation**: Content within fenced code blocks is treated as literal text, not as Markdown syntax, so the rule does not apply here.

Unlike the previous examples, this case embeds reversed link syntax inside an HTML comment block, which is also excluded from rule evaluation.

```Markdown
<!--
This (reversed)[link] is in an HTML comment.
-->
```

> **Explanation**: HTML blocks and comments are excluded from inline Markdown parsing, so reversed link patterns within them do not trigger the rule.

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
