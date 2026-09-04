# Rule - MD021

| Property | Value |
| --- | --- |
| Aliases | `md021`, `no-multiple-space-closed-atx` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Multiple spaces are present inside the hash characters of a closed Atx heading.

## Reasoning

### Simplicity

All researched Markdown parsers treat a single space after the opening `#` and before the closing `#` the same as multiple spaces. Extra spaces serve no purpose, as they do not affect the rendered Atx Heading element.

## Examples

### Failure Scenarios

This rule triggers when there are multiple spaces between the opening `#` and the heading text:

```Markdown
#  Heading 1 #
```

> **Explanation**: This example fails because there are two spaces between the starting `#` and the heading text `Heading 1`. The rule requires exactly one space.

Unlike the previous example, this case has multiple spaces before the closing `#`:

```Markdown
# Heading 1  #
```

> **Explanation**: This example fails because there are two spaces between the heading text `Heading 1` and the ending `#`. The rule requires exactly one space.

This scenario combines both previous violations, having multiple spaces at both the start and end:

```Markdown
#  Heading 1  #
```

> **Explanation**: This example fails because it has multiple spaces at both the start (after the opening `#`) and the end (before the closing `#`). Both violations trigger this rule.

### Correct Scenarios

This rule does not trigger when there is exactly one space character
between the hash characters at the start and end of the heading and
the text between the two sets of hash characters.

```Markdown
# Heading 1 #
```

> **Explanation**: This example passes because there is exactly one space after the opening `#` and one space before the closing `#`, satisfying the rule's requirement.

Unlike the previous example, this case includes leading spaces before the heading:

```Markdown
   # Heading 1 #
```

> **Explanation**: This example passes because the rule only checks spaces between the hash characters and the heading text, not leading spaces before the opening `#`. The single spaces around the text remain compliant.

## Fix Description

Any instances of 1+ space characters within a closed Atx Heading are replaced with
a single space character.

## Configuration

| Prefixes |
| --- |
| `plugins.md021.` |
| `plugins.no-multiple-space-closed-atx.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

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
