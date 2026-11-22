# Rule - MD002

| Property | Value |
| --- | --- |
| Aliases | `md002`, `first-heading-h1`, `first-header-h1` |
| Autofix Available | No |
| Enabled By Default | No |

## Deprecation

This rule is disabled by default, as it has been deprecated in favor of
[Rule MD041](./rule_md041.md).

## Summary

Use a top-level heading for the first heading in the document.

## Reasoning

### Consistency

Using a level 1 heading (`#`) for the first heading ensures consistent document
structure
and improves accessibility by clearly marking the document's primary title.

## Examples

### Failure Scenarios

This rule triggers when the first heading in the document is not at the level required
by the rule (by default, a level 1 heading):

```Markdown
## This isn't an ATX level 1 heading; it is a level 2 heading
```

> **Explanation**: The first heading uses level 2 (`##`) instead of the required
> level 1 (`#`), violating the rule that the first heading must be a top-level heading.

Unlike the previous example, which used Atx syntax, this case uses Setext heading
syntax at level 2, which also violates the rule:

```Markdown
This isn't a Setext level 1 heading; it is a level 2 heading
---
```

> **Explanation**: The first heading uses Setext syntax for a level 2 heading (underline
> with `---`) instead of level 1 (underline with `===`), violating the rule that
> the first heading must be a top-level heading.

Unlike the previous examples which show a level 2 heading, this case uses a
level 3 heading, which equally violates the rule:

```Markdown
### This is a level 3 heading, not the required level 1
```

> **Explanation**: The first heading uses level 3 (`###`), which is further from
> the required level 1 (`#`). The rule checks that the first heading matches the
> configured `level`; any mismatch triggers a failure.

### Correct Scenarios

This rule does not trigger when the first heading in the document is a
level 1 heading in Atx Heading format:

```Markdown
# This is an Atx level 1 heading
```

> **Explanation**: The first heading uses level 1 (`#`), satisfying the rule that
> the first heading must be a top-level heading.

Unlike the previous Atx example, this case uses Setext heading syntax, which also
satisfies the rule:

```Markdown
This is a Setext level 1 heading
===
```

> **Explanation**: The first heading uses Setext syntax for a level 1 heading
> (underline with `===`), satisfying the rule that the first heading must be a
> top-level heading.

Unlike the previous examples, which rely on the default `level` of 1, this case
changes the `level` configuration to 2, allowing a level 2 heading to satisfy
the rule:

```Markdown
## This is an Atx level 2 heading
```

> **Explanation**: The `level` configuration parameter defines the expected heading
> level. With `level` set to `2`, a level 2 heading (`##`) meets the rule's requirement,
so no failure is reported.

## Fix Description

The reason for not being able to auto-fix this rule is that the rule is
deprecated in favor of [Rule MD041](./rule_md041.md). Because the rule is
disabled by default and is intended to be replaced by Rule MD041, no
auto-fix is provided for it.

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
[MD002](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md002---first-heading-should-be-a-top-level-heading),
which is in turn inspired by
[this article](https://cirosantilli.com/markdown-style-guide/#top-level-header).

### Differences From MarkdownLint Rule

PyMarkdown's `MD002` extends MarkdownLint's `MD002` by exposing the expected heading
level through the `level` configuration parameter. MarkdownLint's `MD002` always
expects a level 1 heading; here, `level` may be set to any positive integer, so
a
document whose first heading is `## ...` can still satisfy the rule when `level`
is `2`.
