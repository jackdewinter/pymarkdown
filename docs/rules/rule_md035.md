# Rule - MD035

| Aliases |
| --- |
| `md035` |
| `hr-style` |

## Summary

Horizontal rule style.

## Reasoning

### Readability

The primary reason for enabling this rule is to force the document
writer to not use a single representation for a horizontal rule to
enhance readability.

## Examples

### Failure Scenarios

This rule triggers if the horizontal rule marker style is not consistent
throughout the document.  Note that with default configuration, the first
marker sets the style used throughout the document.

```Markdown
---

-  -  -

***

***********
```

If the configuration specifies a specific style that is not present in
the document, such as `* * *`, then this rule will trigger on every
marker.

### Correct Scenarios

This rule does not trigger if every horizontal rule marker is the
same throughout the document:

```Markdown
---

---
```

Note that any leading whitespace is discarded before the comparison
is made, so that the following example will not trigger this rule:

```Markdown
---

  ---
```

## Configuration

| Prefixes |
| --- |
| `plugins.md035.` |
| `plugins.hr-style.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `style` | `string` | `consistent` | `consistent` for consistent, or a specific marker** |

** If a specific marker is configured, it must be valid multiples (three or more) of either the
`-` character, the `_` character, or the `*` character, with optional whitespace between them.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD035](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md035---horizontal-rule-style).
