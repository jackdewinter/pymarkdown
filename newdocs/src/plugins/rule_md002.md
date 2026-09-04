# Rule - MD002

| Property | Value |
| --- | --- |
| Aliases | `md002`, `first-heading-h1`, `first-header-h1` |
| Autofix Available | No |
| Enabled By Default | No |

## Deprecation

This rule is disabled by default, as it has been deprecated in favor of
[Rule Md041](./rule_md041.md).

## Summary

The first heading must be a top-level heading.

## Reasoning

### Consistency

Using a level 1 heading (#) for the first heading ensures consistent document structure
and improves accessibility by clearly marking the document's primary title.

## Examples

### Failure Scenarios

This rule triggers when the first heading in the document is not a level 1 heading in Atx Heading format:

```Markdown
## This isn't an ATX level 1 heading, it is a level 2 heading
```

> **Explanation**: The first heading uses level 2 (`##`) instead of the required level 1 (`#`), violating the rule that the first heading must be a top-level heading.

This scenario differs from the previous Atx example by using Setext heading syntax, which also violates the rule:

```Markdown
This isn't a Setext level 1 heading, it is a level 2 heading
---
```

> **Explanation**: The first heading uses Setext syntax for a level 2 heading (underline with `---`) instead of level 1 (underline with `===`), violating the rule that the first heading must be a top-level heading.

### Correct Scenarios

This rule does not trigger when the first heading in the document is a level 1 heading in Atx Heading format:

```Markdown
# This is an Atx level 1 heading
```

> **Explanation**: The first heading uses level 1 (`#`), satisfying the rule that the first heading must be a top-level heading.

Unlike the previous Atx example, this case uses Setext heading syntax, which also satisfies the rule:

```Markdown
This is a Setext level 1 heading
===
```

> **Explanation**: The first heading uses Setext syntax for a level 1 heading (underline with `===`), satisfying the rule that the first heading must be a top-level heading.

Unlike the previous examples which use the default `level` of 1, this case sets the `level` configuration to 2, allowing a level 2 heading to pass:

```Markdown
## This is an Atx level 2 heading
```

> **Explanation**: With the `level` configuration set to `2`, a level 2 heading (`##`) satisfies the rule's requirement that the first heading must be at the specified level.

## Fix Description

The reason for not being able to auto-fix this rule is its deprecation in favor of
[Rule MD041](./rule_md041.md)

## Configuration

| Prefixes |
| --- |
| `plugins.md002.` |
| `plugins.first-heading-h1.` |
| `plugins.first-header-h1.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `False` | Determines if this rule is active. |
| `level` | `integer` | `1` | Level that is expected from the first heading (Atx or Setext) in the document. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[Md002](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md002---first-heading-should-be-a-top-level-heading),
which is in turn inspired by
[this article](https://cirosantilli.com/markdown-style-guide/#top-level-header).
