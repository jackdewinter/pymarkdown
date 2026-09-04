# Rule - MD001

| Property | Value |
| --- | --- |
| Aliases | `md001`, `heading-increment`, `header-increment` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Heading levels should only increment by one level at a time.

## Reasoning

### Readability

Skipping heading levels disrupts the document outline that readers and assistive technologies, such as screen readers, rely on for navigation ([Web Accessibility Initiative](https://www.w3.org/WAI/tutorials/page-structure/headings/)).

## Examples

### Failure Scenarios

This rule triggers when a heading level is increased by more than one level, such as from level 1 directly to level 3.

```Markdown
# Heading 1

### Heading 3
```

> **Explanation**: This example fails because the heading level increments from 1 to 3, skipping level 2. The rule requires that heading levels increment by only one level at a time.

Unlike the previous example, this case involves a document with the [Front-Matter Extension](../extensions/front-matter.md) enabled where the `title` field acts as an implicit level-1 heading. The next explicit heading is level 3, skipping level 2.

```Markdown
---
title: my title
---

### Heading 3
```

> **Explanation**: This example fails because the implicit heading from Front-Matter is treated as level 1. The next heading is level 3, which skips level 2. The rule requires incrementing by only one level.

Unlike the previous examples, this case involves skipping heading levels between two explicit headings that are not the initial heading.

```Markdown
## Heading 2

#### Heading 4
```

> **Explanation**: This example fails because the heading level increments from 2 to 4, skipping level 3. The rule applies to all heading transitions, not just those involving the first heading.

### Correct Scenarios

This rule does not trigger when there is a single level increase or any decrease between consecutive headings.

```Markdown
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

## Another Heading 2

### Another Heading 3
```

> **Explanation**: This example passes because each consecutive heading differs by exactly one level (increasing or decreasing). No levels are skipped.

Unlike the previous example, this case involves a document with Front-Matter where the `title` field acts as an implicit level-1 heading. The next explicit heading is level 2, which is a valid increment.

```Markdown
---
title: my title
---

## Heading 2
```

> **Explanation**: This example passes because the implicit heading from Front-Matter is level 1, and the next heading is level 2. This is a valid increment of one level.

Unlike the previous examples, this case demonstrates that the very first heading in a document is ignored by this rule, regardless of its level. The rule only enforces increment rules starting from the second heading.

```Markdown
### Heading 3

## Heading 2
```

> **Explanation**: This example passes because the first heading (level 3) is ignored by the rule. The rule only evaluates transitions starting from the second heading. The transition from level 3 to level 2 is a decrease, which is allowed.

## Fix Description

The heading count (number of `#` characters) is adjusted to match what is expected.

## Configuration

| Prefixes |
| --- |
| `plugins.md001.` |
| `plugins.heading-increment.` |
| `plugins.header-increment.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Determines if this rule is active. |
| `front_matter_title` | `string` | `title` | Name of the Front-Matter field that contains the title associated with the document. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD001](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md001---heading-levels-should-only-increment-by-one-level-at-a-time)
and the
[W3C standards](https://www.w3.org/WAI/tutorials/page-structure/headings/).

### Differences From MarkdownLint Rule

The difference between this rule and the original rule is that the
original rule specified a regular expression used to look for the
specific element within a raw Front-Matter element. By default, this
was ``"^\s*"?title"?\s*[:=]"``. To support simplicity, this rule
simply looks for the value of the Front-Matter key `title` by default,
as the PyMarkdown parser loads the YAML Front-Matter and retains its
values.
