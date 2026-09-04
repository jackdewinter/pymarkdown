# Rule - MD003

| Property | Value |
| --- | --- |
| Aliases | `md003`, `heading-style`, `header-style` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

Use consistent heading styles throughout the document.

## Reasoning

### Readability

Consistent heading styles improve document readability and maintainability. Inconsistent
heading styles can cause confusion for readers and accessibility tools, making it
difficult to parse the document structure visually or programmatically.

## Examples

### Failure Scenarios

This rule triggers when more than one heading style is used within a given document
and the `consistent` style is used. In the following example, because the `consistent`
style is used by default, the first heading establishes the style as `atx`, causing
the rule to generate failures for the second and third headings.

```Markdown
## Atx Heading Without Closing Hashes

## Atx Heading With Closing Hashes ##

Setext Heading
==============
```

> **Explanation**: The first heading is an ATX heading without closing hashes, establishing the `atx` style. The second heading uses closing hashes (`atx_closed`), and the third is a Setext heading. Both deviate from the established `atx` style, triggering the rule.

Unlike the previous example using `consistent` style, this scenario specifies `atx_closed` as the required style. This causes failures for any heading not using closing hashes.

```Markdown
# ATX With No Closing Characters

## ATX With Closing Characters ##

Any Setext
----------
```

> **Explanation**: The configuration specifies `atx_closed`. The first heading (`# ATX With No Closing Characters`) lacks closing hashes, and the third heading (`Any Setext`) is a Setext heading. Both violate the `atx_closed` requirement, triggering the rule.

Similarly, if the `style` is configured to `atx`, any heading that is not an ATX
heading without closing hashes will trigger a failure. In the following example,
the second and third headings will generate a failure.

```Markdown
# ATX Heading

## ATX Closed Heading ##

Setext Heading
====
```

> **Explanation**: The configuration specifies `atx` (no closing hashes). The second heading uses closing hashes (`atx_closed`), and the third is a Setext heading. Both deviate from the strict `atx` style, triggering the rule.

### Correct Scenarios

This rule does not trigger when a consistent heading style is used within
the document. The default style `consistent` decides the heading style upon
encountering the first heading element in the document.

```Markdown
# ATX style H1

## ATX style H2
```

> **Explanation**: Both headings use ATX style without closing hashes. Since the default `consistent` style is used, the first heading establishes `atx` as the expected style, and the second heading conforms to it, so the rule does not trigger.

If a specific style such as `atx_closed` is specified, then all headings must
adhere to that style. Therefore, the following example would not trigger the
rule with a style of `atx_closed`:

```Markdown
# ATX style H1 #

## ATX style H2 ##
```

> **Explanation**: The configuration specifies `atx_closed`. Both headings include closing hashes. Therefore, they both satisfy the configured style, and the rule does not trigger.

Unlike the previous scenario using `atx_closed`, this example configures `setext_with_atx`, which allows Setext headings for levels 1–2 and ATX headings for levels 3+.

```Markdown
Setext style H1
===============

Setext style H2
---------------

### ATX style H3
```

> **Explanation**: The configuration specifies `setext_with_atx`. Headings 1 and 2 use Setext style, and Heading 3 uses ATX style without closing hashes. This matches the defined hybrid style for levels 1-2 (Setext) and 3-6 (ATX), so the rule does not trigger.

This scenario uses `consistent` style with `allow-setext-update` set to `True`, differing from the previous explicit `setext_with_atx` config.

```Markdown
Setext style H1
===============

Setext style H2
---------------

### ATX style H3
```

> **Explanation**: Without `allow-setext-update`, this would fail because the initial style detected is `setext`, and the H3 ATX heading violates it. With `allow-setext-update` set to `True`, the style auto-upgrades to `setext_with_atx` upon encountering the H3 heading. Thus, H1 and H2 satisfy the Setext part, and H3 satisfies the ATX part for level 3+, so the rule does not trigger.

## Fix Description

The implementation for this feature is tracked [with this issue](https://github.com/jackdewinter/pymarkdown/issues/807).

## Configuration

| Prefixes |
| --- |
| `plugins.md003.` |
| `plugins.heading-style.` |
| `plugins.header-style.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Determines if this rule is active. |
| `style` | `string` | `consistent` | The heading style expected in the document. |
| `allow-setext-update` | `boolean` | `False` | Auto-upgrades `consistent` style from `setext` to `setext_with_atx` if a level 3+ ATX heading is found in an otherwise Setext-style document. |

### Valid Styles

| Style | Description |
| --- | --- |
| `consistent` | The first heading in the document specifies the style for the rest of the document. |
| `atx` | Only Atx Headings without any closing hashes are used. |
| `atx_closed` | Only Atx Headings with closing hashes are used. |
| `setext` | Only Setext headings are used. |
| `setext_with_atx` | Only Setext headings are used for levels 1 and 2, and Atx Headings without closing hashes are used for levels 3 to 6. |
| `setext_with_atx_closed` | Only Setext headings are used for levels 1 and 2, and Atx Headings with closing hashes are used for levels 3 to 6. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD003](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md003---heading-style).
The `allow-setext-update` configuration value was added due to a [user request](https://github.com/jackdewinter/pymarkdown/issues/154).
