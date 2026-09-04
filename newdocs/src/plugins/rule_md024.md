# Rule - MD024

| Property | Value |
| --- | --- |
| Aliases | `md024`, `no-duplicate-heading`, `no-duplicate-header` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Multiple headings cannot contain the same content.

## Reasoning

### Correctness

Many Markdown parsers generate `id` attributes or anchor tags based on heading content. Having multiple headings with the same text produces non-unique anchors, which can break navigation and cause accessibility issues for readers relying on those links.

## Examples

### Failure Scenarios

This rule triggers when there are multiple headings that have the same text:

```Markdown
# Heading Text

## Heading Text
```

> **Explanation**: This example fails because both headings contain the exact same text (`Heading Text`), which violates the rule that prohibits multiple headings with identical content. This could cause issues with parsers that generate unique IDs or anchor tags based on heading content.

Unlike the previous example which showed headings at different nesting levels, this case demonstrates duplicate headings that are direct siblings at the same level:

```Markdown
## Heading Text

## Heading Text
```

> **Explanation**: This example fails because both headings are sibling elements at the same nesting level (`##`) with identical text, which violates the rule that prohibits duplicate heading content among siblings.

Building on the previous sibling example, this scenario shows that leading whitespace in a heading does not make it distinct from another heading without leading whitespace:

```Markdown
  ## Heading Text

## Heading Text
```

> **Explanation**: This example fails because the rule ignores leading whitespace when comparing heading content. Both headings are considered to have the same text (`Heading Text`), violating the duplicate heading prohibition.

### Correct Scenarios

This rule does not trigger when each heading has distinct text:

```Markdown
# Heading 1

## Heading 2
```
> **Explanation**: This example passes because each heading has distinct text (`Heading 1` and `Heading 2`), satisfying the rule requirement that all headings must have unique content.

Unlike the previous example where headings were clearly different, this case shows that even a single extra space character makes headings distinct under strict comparison:

```Markdown
# Heading  Text

## Heading Text
```

> **Explanation**: This example passes because the strict comparison detects that `Heading  Text` (with two spaces) differs from `Heading Text` (with one space), making them unique despite appearing similar visually.

Building on the prior example, this case demonstrates that capitalization changes alone are sufficient to differentiate headings:

```Markdown
# Heading TEXT

## Heading Text
```

> **Explanation**: This example passes because the strict comparison treats `Heading TEXT` and `Heading Text` as different strings due to the capitalization difference, satisfying the uniqueness requirement.

Unlike the earlier examples involving simple uniqueness, this scenario involves non-sibling headings that share text within different nesting hierarchies, which is allowed when `siblings_only` or `allow_different_nesting` is enabled:

```Markdown
# Change log

## 1.0.0

### Features

## 2.0.0

### Features
```

> **Explanation**: This example passes when the siblings_only configuration is set to True because the "Features" headings are not siblings (they are under different parent headings), so they are allowed to have the same text. This is useful for documents like changelogs where repeated section names are intentional and desired.

## Fix Description

Auto-fixing this rule is not feasible due to contextual considerations. Using any of the
above trigger examples, it is simple to determine when this rule should be triggered.
It would be relatively easy to devise an algorithm that would perform some action
(such as appending an increasing number to the end of the heading text) to make each
heading unique.  While that would fix the triggering of the rule, it would deprive
the author of the chance to change any triggered headings to text that was unique
and made sense within the scope of the document.

## Configuration

| Prefixes |
| --- |
| `plugins.md024.` |
| `plugins.no-duplicate-heading.` |
| `plugins.no-duplicate-header.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `siblings_only` | `boolean` | `False` | Whether the Rule Plugin allows the same text on sibling headings. |
| `allow_different_nesting` | `boolean` | `False` | Whether the Rule Plugin allows the same text within different nesting hierarchies. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD024](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md024---multiple-headings-with-the-same-content).
