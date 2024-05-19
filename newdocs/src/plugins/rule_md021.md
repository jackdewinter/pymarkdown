# Rule - MD021

| Property | Value |
| --- | -- |
| Aliases | `md021`, `no-multiple-space-closed-atx` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Multiple spaces are present inside hash characters on Atx Closed Heading.

## Reasoning

### Simplicity

All the Markdown parsers that we researched treat one space character after
the start hash character (`#`) and one space before the end hash
character the same as multiple space characters.  As such, the extra space
characters have no purpose as they do not affect
the rendering of the Atx Heading element.

## Examples

### Failure Scenarios

This rule triggers when the start of an Atx Heading element has more
than one space character between the last start hash character (`#`) and
the first non-space character:

```Markdown
#  Heading 1 #
```

between the first end hash character and the last non-space character:

```Markdown
# Heading 1  #
```

or both.

### Correct Scenarios

This rule does not trigger when there is exactly one space character
between the hash characters at the start and end of the heading and
the text between the two sets of hash characters.

```Markdown
# Heading 1 #
```

This rule is specifically targeted to the spaces between the hash characters
and the contained text.  Between one and three leading space
characters do not trigger this rule:

```Markdown
   # Heading 1 #
```

## Fix Description

Any instances of 1+ space characters within a closed Atx Heading are replaced with
a single space character.

## Configuration

| Prefixes |
| --- |
| `plugins.md021.` |
| `plugins.no-multiple-space-closed-atx.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD021](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md021---multiple-spaces-inside-hashes-on-closed-atx-style-heading).

### Differences From MarkdownLint Rule

The original rule did not take any leading spaces into consideration,
declaring that any leading spaces were a violation of this rule.  As
[Rule md023](./rule_md023.md)
addresses the number of leading spaces preceding an Atx Heading element,
this rule was developed to ignore any leading spaces.  The rationale is
that if leading spaces before Atx Heading elements are not desired, there
should only be one rule's configuration that needs to be set to
enforce that.
