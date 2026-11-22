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

Horizontal rules visually separate content sections. Using a consistent style (such
as `---`, `***`, or `___`) improves document uniformity and makes it easier for
readers to scan and distinguish structural breaks from other content.

## Examples

### Failure Scenarios

This rule triggers when the horizontal rule marker style is not consistent throughout
the document. With the default configuration, the first marker sets the style used
throughout the document.

```Markdown
---

-  -  -

***

***********
```

> **Explanation**: The first horizontal rule uses `---`, establishing `---` as the
> expected style. The subsequent rules use `-  -  -` (dashed with extra spacing),
> `***` (asterisk style), and `***********` (longer asterisk run), none of which
> match the established `---` style, causing violations.

Unlike the previous example, this scenario uses a configured style (`* * *`) that
the second marker does not match.

```Markdown
* * *

---
```

> **Explanation**: The configuration explicitly requires the `style` set to
> `* * *`. The first marker matches this style. The second marker `---` does not
> match the configured style `* * *`, causing a violation.

Unlike the previous examples, this scenario demonstrates a mismatch between dash
and underscore horizontal rule styles.

```Markdown
---

___
```

> **Explanation**: The first horizontal rule uses `---`, establishing `---` as the
> expected style (under the default `consistent` configuration). The second rule
> uses `___`, which is a valid horizontal rule marker but does not match the established
> dash style, causing a violation.

Unlike the previous examples, this scenario demonstrates a mismatch caused by inconsistent
spacing within the same character type.

```Markdown
***

* * *
```

> **Explanation**: The first horizontal rule uses `***` (no spaces), establishing
> `***` as the expected style. The second rule uses `* * *` (with spaces), which
> is a valid horizontal rule marker but does not match the established no-space
style, causing a violation.

### Correct Scenarios

This rule does not trigger when every horizontal rule marker is the same throughout
the document.

```Markdown
---

---
```

> **Explanation**: Both horizontal rules use the `---` style. Since the style is
> consistent throughout the document, no violations occur.

Unlike the previous example, this scenario includes leading whitespace before the
markers.

```Markdown
---

  ---
```

> **Explanation**: Indentation is not part of the horizontal-rule style; only the
> marker characters define the style. Both markers are `---`, so the document remains
> stylistically consistent and the rule does not trigger.

Unlike the previous examples, this scenario demonstrates consistent use of the underscore
horizontal rule style.

```Markdown
___

___
```

> **Explanation**: Both horizontal rules use the `___` style. Since the style is
> consistent throughout the document, no violations occur. This confirms that any
> consistent style (not just `---`) is acceptable.

Unlike the previous examples, this scenario includes a two-character sequence (`--`)
that is too short to be a valid horizontal rule.

```Markdown
--
```

> **Explanation**: A horizontal rule requires three or more consecutive delimiter
> characters (`-`, `_`, or `*`). The sequence `--` has only two characters and therefore
> is not recognized as a horizontal rule at all. Since no horizontal rule is present,
> the rule has nothing to compare and does not trigger.

## Fix Description

All horizontal rules are replaced with the configured thematic break text. If the
configuration is the default `consistent`, the first horizontal rule establishes
the style text used throughout the document.

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
