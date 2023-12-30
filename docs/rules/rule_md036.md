# Rule - MD036

| Aliases |
| --- |
| `md036` |
| `no-emphasis-as-heading` |
| `no-emphasis-as-header` |

| Autofix Available |
| --- |
| No |

## Summary

Emphasis possibly used instead of a heading element.

## Reasoning

To people that are new to Markdown, there may be an old habit of
using various forms of emphasis to create a heading, instead of using
Markdown's Atx Heading element or SetExt Heading element.  The heading
elements are present to allow a higher semantic meaning to be associated
with the text, rather than the more simplistic emphasis meaning associated
with text that is emphasized.

## Examples

### Failure Scenarios

This rule triggers when a single line of text is present in a Paragraph
element, the entirety of the text is within an Emphasis element, and
that text does not end with any of the configured punctuation characters.

```Markdown
**My document**

Lorem ipsum dolor sit amet...

_Another section_

Consectetur adipiscing elit, sed do eiusmod.
```

### Correct Scenarios

This rule does not trigger when all constraints have not been met:

```Markdown
**My
document**

Lorem ipsum dolor sit amet...

_Almost a section_ heading

Consectetur adipiscing elit, sed do eiusmod.

*But this is not a heading!*

Consectetur adipiscing elit, sed do eiusmod.
```

## Configuration

| Prefixes |
| --- |
| `plugins.md036.` |
| `plugins.no-emphasis-as-heading.` |
| `plugins.no-emphasis-as-header.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `punctuation` | `string` | `.,;:!?。，；：？` | Punctuation characters that are considered sentence ending characters. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD036](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md036---emphasis-used-instead-of-a-heading).
and
[this article](https://cirosantilli.com/markdown-style-guide#emphasis-vs-headers).

### Differences From MarkdownLint Rule

The original rule did not work inside of Block Quote elements or List elements.

## Fix Description

The reason for not being able to auto-fix this rule is certainty.  The summary for
this rule specifically states:

> Emphasis possibly used instead of a heading element.

As this rule simply advises that it found cases that only appear to be headings
that are created with emphasis, it does not attempt to fix them.
