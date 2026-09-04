# Rule - MD019

| Property | Value |
| --- | --- |
| Aliases | `md019`, `no-multiple-space-atx` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Ensure only one space follows the hash character in open-style Atx headings (headings without trailing closing hash characters).

**Scope Boundary**: This rule checks open-style headings only. [Rule MD021](./rule_md021.md) checks closed-style headings. A heading is "closed" if it ends with one or more hash characters (e.g., `# Heading #`).

## Reasoning

### Simplicity

All tested Markdown parsers treat one space after the hash character (`#`) identically to multiple spaces. The extra spaces serve no purpose and do not affect how an open-style Atx heading renders.

## Examples

### Failure Scenarios

This rule triggers when the start of an Atx Heading element has more
than one space character between the last hash character (`#`) and
the first non-space character.

```Markdown
#  Heading 1
```

> **Explanation**: This example violates the rule because there are two space characters between the hash character (`#`) and the first non-space character (`H`). The rule requires only a single space in this position.

This scenario differs from the first by using a level-2 heading instead of level-1, demonstrating that the rule applies regardless of heading depth.

```Markdown
##  Heading 2
```

> **Explanation**: This example violates the rule because there are two space characters between the last hash character (`#`) and the first non-space character (`H`). The rule requires only a single space in this position, regardless of the heading level.

Unlike the previous examples, this case includes leading spaces before the hash character, in addition to multiple spaces after the hash.

```Markdown
  ##  heading 2
```

> **Explanation**: This example violates the rule because there are two space characters between the last hash character (`#`) and the first non-space character (`h`). Although leading spaces are ignored by this rule, the multiple spaces between the hash and the heading text still trigger the violation.

### Correct Scenarios

This rule does not trigger with exactly one space character occurring
between the last hash character and the first non-space character.

```Markdown
# Heading 1
```

> **Explanation**: This example satisfies the rule because there is exactly one space character between the hash character (`#`) and the first non-space character (`H`), which is the required format.

Unlike the previous example, this case includes leading space characters before the hash symbol. The rule only checks the space between the hash and the heading text, ignoring leading spaces.

```Markdown
   # Heading 2
```

> **Explanation**: This example satisfies the rule because, despite having leading spaces, there is only one space character between the hash character (`#`) and the first non-space character of the heading text (`H`). Leading spaces are ignored by this rule.

Unlike the previous examples, this case includes trailing hash characters, which is handled by [Rule MD021](./rule_md021.md) instead.

```Markdown
##  Heading 2  ##
```

> **Explanation**: This example does not trigger Rule MD019 because it is a "closed" style Atx heading (it has trailing closing hash characters). Rule MD019 applies only to open-style Atx headings (those without trailing hashes). Closed-style headings are validated by [Rule MD021](./rule_md021.md) instead. Note that this example *will* trigger MD021 for the multiple spaces between the hashes and the text.

## Fix Description

Any instances of two or more space characters after the hash character(s) within a normal Atx Heading are replaced with
a single space character.

## Configuration

| Prefixes |
| --- |
| `plugins.md019.` |
| `plugins.no-multiple-space-atx.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

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
