# Rule - MD049

| Property | Value |
| --- | --- |
| Aliases | `md049`, `emphasis-style` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

Ensure consistent emphasis style throughout the document.

## Reasoning

### Readability

To maintain a uniform appearance and improve readability, the character sequence used for inline emphasis (e.g., asterisks vs. underscores) should remain consistent throughout a document or set of documents.

## Examples

### Failure Scenarios

This rule triggers when there is inconsistent use for inline emphasis blocks:

```Markdown
This is *one* emphasis.

This is _another_ emphasis.
```

> **Explanation**: This example fails because the first line uses asterisks (`*`) for emphasis while the second line uses underscores (`_`). With the default `consistent` style, the first emphasis block sets the expected style to asterisks. The subsequent use of underscores violates this consistency requirement.

Unlike the previous example, which relies on the default `consistent` style, this scenario violates the rule when the `style` configuration is explicitly set to `asterisk`. Even if all emphasis blocks use underscores consistently among themselves, they fail the rule because underscores are not permitted in this strict mode.

```Markdown
This is _one_ emphasis.

This is _another_ emphasis.
```

> **Explanation**: This example fails because the configuration `style` is set to `asterisk`, which mandates that only asterisks (`*`) may be used for emphasis. Although both blocks use underscores consistently, underscores are prohibited in this mode.

Unlike the previous example, which demonstrated a violation of the `asterisk` configuration, this scenario violates the rule when the `style` configuration is explicitly set to `underscore`. Even if all emphasis blocks use asterisks consistently among themselves, they fail the rule because asterisks are not permitted in this strict mode.

```Markdown
This is *one* emphasis.

This is *another* emphasis.
```

> **Explanation**: This example fails because the `style` configuration is set to `underscore`, which mandates that only underscores (`_`) may be used for emphasis. Although both blocks use asterisks consistently, asterisks are prohibited in this mode.

### Correct Scenarios

This rule does not trigger when the character sequence for emphasis blocks is
consistently specified within the document:

```Markdown
This is *one* emphasis.

This is the *same* emphasis.
```

> **Explanation**: This example passes because both emphasis blocks use asterisks (`*`). This is consistent with the default `consistent` style, which adopts the style of the first emphasis block encountered.

Unlike the previous example, which relied on the default `consistent` style, this scenario demonstrates compliance when the `style` configuration is explicitly set to `underscore`. All emphasis blocks use underscores, satisfying the strict configuration requirement.

```Markdown
This is _one_ emphasis.

This is _another_ emphasis.
```

> **Explanation**: This example passes because the configuration `style` is set to `underscore`, which mandates that only underscores (`_`) may be used for emphasis. Both blocks use underscores, satisfying this requirement.

Unlike the previous example, which satisfied the `underscore` style, this scenario demonstrates compliance when the style configuration is explicitly set to `asterisk`. All emphasis blocks use asterisks, satisfying the strict configuration requirement.

```Markdown
This is *one* emphasis.

This is *another* emphasis.
```

> **Explanation**: This example passes because the configuration `style` is set to `asterisk`, which mandates that only asterisks (`*`) may be used for emphasis. Both blocks use asterisks, satisfying this requirement.

## Fix Description

The implementation for this feature is tracked [with this issue](https://github.com/jackdewinter/pymarkdown/issues/1676).

## Configuration

| Prefixes |
| --- |
| `plugins.md049.` |
| `plugins.emphasis-style.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `style` | `string` | `consistent` | Style of emphasis block characters expected in the document. |

### Valid Styles

| Style | Description |
| --- | --- |
| `consistent` | The first emphasis block in the document specifies the style for the rest of the document. |
| `asterisk` | Only asterisks are to be used for inline emphasis block elements. |
| `underscore` | Only underscores are to be used for inline emphasis block elements. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD049](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md049---emphasis-style).
