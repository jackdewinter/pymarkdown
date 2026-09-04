# Rule - MD035

| Property | Value |
| --- | --- |
| Aliases | `md035`, `hr-style` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Enforce a consistent style for horizontal rules.

## Reasoning

### Readability

Horizontal rules visually separate content sections. Using a consistent style (such as `---`, `***`, or `___`) improves document uniformity and makes it easier for readers to scan and distinguish structural breaks from other content.

## Examples

### Failure Scenarios

This rule triggers when the horizontal rule marker style is not consistent throughout the document. With the default configuration, the first marker sets the style used throughout the document.

```Markdown
---

-  -  -

***

***********
```

> **Explanation**: The first horizontal rule uses `---`, establishing `---` as the expected style. The subsequent rules use `- - -`, `***`, and `**` variants, which do not match the established style, causing violations.

Unlike the previous example, this scenario uses a specific configured style that differs from the markers in the document.

```Markdown
* * *

---
```

> **Explanation**: The configuration explicitly requires the style `* * *`. The first marker matches this style. The second marker `---` does not match the configured style `* * *`, causing a violation.

Unlike the previous examples, this scenario demonstrates a mismatch between dash and underscore horizontal rule styles.

```Markdown
---

___
```

> **Explanation**: The first horizontal rule uses `---`, establishing `---` as the expected style (under the default `consistent` configuration). The second rule uses `___`, which is a valid horizontal rule marker but does not match the established dash style, causing a violation.

Unlike the previous examples, this scenario demonstrates a mismatch caused by inconsistent spacing within the same character type.

```Markdown
***

* * *
```

> **Explanation**: The first horizontal rule uses `***` (no spaces), establishing `***` as the expected style. The second rule uses `* * *` (with spaces), which is a valid horizontal rule marker but does not match the established no-space style, causing a violation.

### Correct Scenarios

This rule does not trigger when every horizontal rule marker is the same throughout the document.

```Markdown
---

---
```

> **Explanation**: Both horizontal rules use the `---` style. Since the style is consistent throughout the document, no violations occur.

Unlike the previous example, this scenario includes leading whitespace before the markers.

```Markdown
---

  ---
```

> **Explanation**: Leading whitespace is discarded before comparison. Both markers are effectively `---` after whitespace removal. Since the styles match, no violations occur.

Unlike the previous examples, this scenario demonstrates consistent use of the underscore horizontal rule style.

```Markdown
___

___
```

> **Explanation**: Both horizontal rules use the `___` style. Since the style is consistent throughout the document, no violations occur. This confirms that any consistent style (not just `---`) is acceptable.

## Fix Description

All horizontal rules are replaced with the configured thematic break text. If the
configuration is the default `consistent`, the first horizontal rule establishes the style text used throughout the document.

## Configuration

| Prefixes |
| --- |
| `plugins.md035.` |
| `plugins.hr-style.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `style` | `string` | `consistent` | `consistent` for consistent style, or a specific marker (three or more `-`, `_`, or `*` characters with optional whitespace; cannot start or end with a space) |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD035](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md035---horizontal-rule-style).
