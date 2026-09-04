# Rule - MD005

| Property | Value |
| --- | --- |
| Aliases | `md005`, `list-indent` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Use consistent indentation for list items at the same level.

## Reasoning

### Readability

Inconsistent indentation in lists doesn't affect parsing engines, but it makes source documents harder for humans to scan. Enforcing consistent indentation ensures list structure is visually clear and predictable.

## Examples

### Failure Scenarios

This rule triggers when list items at the same level have inconsistent indentation, such as an unordered list item that is indented more than its siblings.

```Markdown
* Item 1
* Item 2
 * Misaligned item
```

> **Explanation**: The third item is indented by one space more than the first two items. This violates the rule because all items at the same nesting level should start at the same horizontal position.

Unlike the previous unordered list example, this ordered list fails because the second item's indentation does not align with the first item's start or delimiter.

```Markdown
1. First item
 2. Second Item
```

> **Explanation**: The first item starts at column 0. The second item starts at column 1, which misaligns both the text content and the delimiter (`.`) relative to the first item. This violates the rule's requirement for consistent indentation or alignment.

Unlike the previous single-list examples, this scenario involves sublists with mixed alignment styles, causing a violation when the overall list alignment is inconsistent.

```Markdown
1. Item 1
   1. Item 1a
   10. Item 1b
2. Item 2
    1. Item 2a
   10. Item 2b
```

> **Explanation**: The sublist under `Item 1` is left-aligned (delimiter `1.` and `10.` align), while the sublist under `Item 2` is right-aligned (`1.` is indented more than `10.`). The rule enforces consistent alignment across the entire list structure, so this mixture triggers the failure.

### Correct Scenarios

This rule does not trigger when all unordered list items at the same level share consistent indentation, including proper indentation for nested sublists.

```Markdown
* Item 1
  * Item 1a
* Item 2
  * Item 2a
```

> **Explanation**: All top-level items (`Item 1`, `Item 2`) start at column 0. All nested items (`Item 1a`, `Item 2a`) are indented consistently by 2 spaces. This satisfies the rule's requirement for uniform indentation at each nesting level.

Unlike unordered lists, this ordered list example shows left-aligned items where the delimiter characters are vertically aligned.

```Markdown
1. Item
10. Item
100. Item
```

> **Explanation**: The delimiter characters (`1.`, `10.`, `100.`) are left-aligned at column 0. This is a valid format supported by the rule for ordered lists.

Unlike the previous left-aligned example, this ordered list shows right-aligned items where the end of the delimiter characters is vertically aligned.

```Markdown
  1. Item
 10. Item
100. Item
```

> **Explanation**: The delimiter characters are right-aligned, meaning the periods (`.`) are in the same column. This is also a valid format supported by the rule for ordered lists.

Unlike the previous right-aligned example, this case demonstrates how excessive indentation can cause an ordered list to be interpreted as an indented code block, which is not subject to this rule.

```Markdown
    1. Item
   10. Item
  100. Item
 1000. Item
10000. Item
```

> **Explanation**: The first item is indented by 4 spaces, which Markdown parsers interpret as an indented code block rather than an ordered list. Since this is not a list, the rule does not apply. This is an edge case that does not trigger the rule because the content is not recognized as a list.

## Fix Description

The autofix collects all list items within a contiguous list block. For ordered lists,
it determines whether right-alignment is intended. If so, it aligns the delimiters
to the right. Otherwise, it aligns all items at the same nesting level to start at
the same column as the first item. This ensures consistent indentation across the
entire list structure.

## Configuration

| Prefixes |
| --- |
| `plugins.md005.` |
| `plugins.list-indent.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Determines if this rule is active. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD005](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md005---inconsistent-indentation-for-list-items-at-the-same-level).

### Differences From MarkdownLint Rule

The original rule did not consider alignment consistency across sublists within a parent list. As such, it was possible to
have a list containing sublists that mixed left-aligned lists with right-aligned lists. This rule resets its notion of the proper alignment for
Ordered Lists when the base List element is closed.
