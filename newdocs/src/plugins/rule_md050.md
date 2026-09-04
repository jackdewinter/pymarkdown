# Rule - MD050

| Property | Value |
| --- | --- |
| Aliases | `md050`, `strong-style` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Ensure consistent strong emphasis style throughout the document.

## Reasoning

### Readability

To maintain a uniform appearance and improve readability, the character sequence used for strong inline emphasis (e.g., asterisks vs. underscores) should remain consistent throughout a document or set of documents.

## Examples

### Failure Scenarios

This rule triggers when there is inconsistent use of inline strong emphasis blocks:

```Markdown
This is **one** strong emphasis.

This is __another__ strong emphasis.
```

> **Explanation**: This example fails because the first line uses asterisks (`**`) for strong emphasis while the second line uses underscores (`__`). With the default `consistent` style, the first strong emphasis block sets the expected style to asterisks. The subsequent use of underscores violates this consistency requirement.

Unlike the previous example, which relies on the default `consistent` style, this scenario violates the rule when the `style` configuration is explicitly set to `asterisk`. Even if all strong emphasis blocks use underscores consistently among themselves, they fail the rule because underscores are not permitted in this strict mode.

```Markdown
This is __one__ strong emphasis.

This is __another__ strong emphasis.
```

> **Explanation**: This example fails because the configuration `style` is set to `asterisk`, which mandates that only asterisks (`*`) may be used for strong emphasis. Although both blocks use underscores consistently, underscores are prohibited in this mode.

Unlike the previous example, which demonstrated a violation of the `asterisk` configuration, this scenario violates the rule when the `style` configuration is explicitly set to `underscore`. Even if all strong emphasis blocks use asterisks consistently among themselves, they fail the rule because asterisks are not permitted in this strict mode.

```Markdown
This is **one** strong emphasis.

This is **another** strong emphasis.
```

> **Explanation**: This example fails because the `style` configuration is set to `underscore`, which mandates that only underscores (`_`) may be used for strong emphasis. Although both blocks use asterisks consistently, asterisks are prohibited in this mode.

### Correct Scenarios

This rule does not trigger when the character sequence for strong emphasis blocks is
consistently specified within the document:

```Markdown
This is **one** strong emphasis.

This is the **same** strong emphasis.
```

> **Explanation**: This example passes because both strong emphasis blocks use asterisks (`*`). This is consistent with the default `consistent` style, which adopts the style of the first strong emphasis block encountered.

Unlike the previous example, which relied on the default `consistent` style, this scenario demonstrates compliance when the `style` configuration is explicitly set to `underscore`. All strong emphasis blocks use underscores, satisfying the strict configuration requirement.

```Markdown
This is __one__ strong emphasis.

This is __another__ strong emphasis.
```

> **Explanation**: This example passes because the configuration `style` is set to `underscore`, which mandates that only underscores (`_`) may be used for strong emphasis. Both blocks use underscores, satisfying this requirement.

Unlike the previous example, which demonstrated compliance with `style` set to `underscore`, this scenario shows compliance when `style` is explicitly set to `asterisk`. All strong emphasis blocks use asterisks, satisfying the strict configuration requirement.

```Markdown
This is **one** strong emphasis.

This is **another** strong emphasis.
```

> **Explanation**: This example passes because the configuration `style` is set to `asterisk`, which mandates that only asterisks (`*`) may be used for strong emphasis. Both blocks use asterisks, satisfying this requirement.

## Fix Description

Because the rule is style-sensitive, the tool cannot safely determine which emphasis marker (`**` or `__`) the author intends when only a single type is present. Automatically choosing one could change the document's intended formatting, so no autofix is applied.

## Configuration

| Prefixes |
| --- |
| `plugins.md050.` |
| `plugins.strong-style.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `style` | `string` | `consistent` | Style of inline strong emphasis block characters expected in the document. |

### Valid Styles

| Style | Description |
| --- | --- |
| `consistent` | The first inline strong emphasis block in the document specifies the style for the rest of the document. |
| `asterisk` | Only asterisks are to be used for inline strong emphasis block elements. |
| `underscore` | Only underscores are to be used for inline strong emphasis block elements. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD050](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md050---strong-style).
