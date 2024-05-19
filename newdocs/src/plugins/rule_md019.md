# Rule - MD019

| Property | Value |
| --- | -- |
| Aliases | `md019`, `no-multiple-space-atx` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Multiple spaces are present after hash character on Atx Heading.

## Reasoning

### Simplicity

All the Markdown parsers that we researched treat one space character after
the hash character (`#`) the same as multiple space characters after the
hash character.  As such, the extra space characters have no purpose as they do
not affect the rendering of the Atx Heading element.

## Examples

### Failure Scenarios

This rule triggers when the start of an Atx Heading element has more
than one space character between the last hash character (`#`) and
the first non-space character.

```Markdown
#  Heading 1
```

### Correct Scenarios

This rule does not trigger with exactly one space character occurring
between the last hash character and the first non-space character.

```Markdown
# Heading 1
```

This rule is specifically targeted to the space between the hash character
and the first non-space character.  Between one and three leading space
characters do not trigger this rule:

```Markdown
   # Heading 1
```

## Fix Description

Any instances of 1+ space characters within a normal Atx Heading are replaced with
a single space character.

## Configuration

| Prefixes |
| --- |
| `plugins.md019.` |
| `plugins.no-multiple-space-atx.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD019](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md019---multiple-spaces-after-hash-on-atx-style-heading).

### Differences From MarkdownLint Rule

The original rule did not take any leading spaces into consideration,
declaring that any leading spaces were a violation of this rule.  As
[Rule Md023](./rule_md023.md)
addresses the number of leading spaces preceding an Atx Heading element,
this rule was developed to ignore any leading spaces.  The rationale is
that if leading spaces before Atx Heading elements are not desired, there
should only be one rule's configuration that needs to be set to
enforce that.
