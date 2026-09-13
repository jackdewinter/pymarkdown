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

Inconsistent heading styles make a document harder for human readers and assistive-technology
users to scan and navigate; a single, consistent heading style keeps the structure
visually and programmatically predictable.

## Examples

### Failure Scenarios

This rule triggers when a document mixes more than one heading style under the default
`consistent` style — for example, combining `atx`, `atx_closed`, and `setext` headings
in the same document.

```Markdown
## Atx Heading Without Closing Hashes

## Atx Heading With Closing Hashes ##

Setext Heading
==============
```

> **Explanation**: The first heading is an ATX heading without closing hashes, establishing
> the `atx` style. The second heading uses closing hashes (`atx_closed`), and the
> third is a Setext heading. Both deviate from the established `atx` style, triggering
> the rule.

Unlike the preceding scenario, which relied on the default `consistent` style, this
scenario explicitly configures `style` to `atx_closed`. Any heading that does not
use closing hashes (including Setext headings) fails the rule.

```Markdown
# ATX With No Closing Characters

Any Setext
----------
```

> **Explanation**: The configuration specifies `atx_closed`. The first heading
> (`# ATX With No Closing Characters`) lacks closing hashes, and the second heading
> (`Any Setext`) is a Setext heading. Both violate the `atx_closed` requirement,
> triggering the rule.

Unlike the previous scenario that required `atx_closed`, this scenario explicitly
configures `style` to `atx` (no closing hashes). Any heading that uses closing hashes
or is a Setext heading triggers a failure.

```Markdown
## ATX Closed Heading ##

Setext Heading
==============
```

> **Explanation**: The configuration specifies `atx` (no closing hashes). The second
> heading uses closing hashes (`atx_closed`), and the third is a Setext heading.
> Both deviate from the strict `atx` style, triggering the rule.

### Correct Scenarios

This rule does not trigger when a consistent heading style is used throughout the
document under the default `consistent` style.

```Markdown
# ATX style H1

## ATX style H2
```

> **Explanation**: Both headings use ATX style without closing hashes. Since the
> default `consistent` style is used, the first heading establishes `atx` as the
> expected style, and the second heading conforms to it, so the rule does not trigger.

Unlike the previous scenario, where the default `consistent` style determined
`atx` from the first heading, this scenario explicitly configures
`atx_closed`. All headings in the document use closing hashes, so the
rule does not trigger.

```Markdown
# ATX style H1 #

## ATX style H2 ##
```

> **Explanation**: The configuration specifies `atx_closed`. Both headings include
> closing hashes. Therefore, both satisfy the configured style, and the rule does
> not trigger.

Unlike the previous uniform `atx_closed` scenario, this scenario uses the hybrid
`setext_with_atx` style: levels 1–2 are Setext and level 3+ is ATX without closing
hashes. The code block itself shows both halves of the hybrid style.

```Markdown
Setext style H1
===============

Setext style H2
---------------

### ATX style H3

#### ATX style H4
```

> **Explanation**: Levels 1 and 2 are Setext headings and levels 3–4 are ATX headings
> without closing hashes, which is exactly what `setext_with_atx` requires. Because
> every heading matches its level's mandated style, the rule does not trigger.

Unlike the previous `setext_with_atx` scenario, this scenario uses the default
`consistent` style together with `allow-setext-update` set to `True`. A level-3
ATX heading in an otherwise Setext document triggers the auto-upgrade to `setext_with_atx`,
so the rule does not trigger.

```Markdown
Setext style H1
===============

Setext style H2
---------------

### ATX style H3
```

> **Explanation**: Under plain `consistent`, the first heading would lock the document
> into `setext`, and the level-3 ATX heading would violate that style. With `allow-setext-update`
> set to `True`, the style auto-upgrades to `setext_with_atx` as soon as a level-3+
> ATX heading is seen. Because the ATX heading here is at level 3 (an ATX-mandated
> level under `setext_with_atx`), the rule does not trigger.

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

| Style Name | Description |
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

### Differences From MarkdownLint Rule

The `allow-setext-update` configuration value was added due to a
[user request](https://github.com/jackdewinter/pymarkdown/issues/154) and is not
present in the upstream MarkdownLint rule. Otherwise, the rule's behavior and supported
styles are equivalent to the MarkdownLint rule.
