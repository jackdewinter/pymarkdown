# Rule - MD029

| Property | Value |
| --- | --- |
| Aliases | `md029`, `ol-prefix` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Ordered list item prefixes must be consistent.

## Reasoning

### Readability

Consistent ordered list item prefixes create a predictable pattern that enhances readability. They also ensure that lists render correctly across different Markdown parsers and tools.

## Examples

### Failure Scenarios

This rule triggers when an ordered list item prefix is not `1` or `0` (depending on configuration) or does not follow the expected order.

```Markdown
2. second item
3. third item
```

> **Explanation**: This list starts with `2`, which is not the allowed start value (`0` or `1`) for the default `one_or_ordered` style. Therefore, the rule triggers.

Unlike the previous example, this list starts with `1` but the subsequent item skips a number.

```Markdown
1. first item
3. third item
```

> **Explanation**: The list starts with `1`, which is valid. However, the next item is `3`, skipping `2`. This violates the `ordered` style requirement where each item must increment by one.

Unlike the previous example, this list starts with an invalid number and does not increment correctly.

```Markdown
3. first item
3. second item
```

> **Explanation**: The list starts with `3`, which is invalid. Additionally, the second item is also `3`, failing to increment from the previous item.

Unlike the previous examples, this scenario demonstrates nested ordered lists, where each inner list starts a new evaluation of the rule based on the configured style.

```Markdown
2. first
   1. first-first
   1. first-second
   2. first-third
3. second
   1. second-first
   2. second-second
   2. second-third
```

> **Explanation**: Assuming the default `one_or_ordered` style, the rule triggers on multiple lines. Line 1 triggers because the outer list starts with `2` instead of `1` or `0`. Line 4 triggers because the first inner list uses the `one` style (items should all be `1`), but the third item is `2`. Line 8 triggers because the second inner list uses the `ordered` style (items should increment), but the third item is `2` instead of `3`. This highlights that nested lists are evaluated independently according to the rule's style criteria.

### Correct Scenarios

This rule does not trigger when all ordered list items start with `1`, which is one of the allowed styles (`one`).

```Markdown
1. First Line
1. Second Line
```

> **Explanation**: All items start with `1`, satisfying the `one` style component of the default `one_or_ordered` configuration or an explicitly configured style of `one`.

Unlike the previous example, this list starts with `1` and increments steadily, satisfying the `ordered` style.

```Markdown
1. First Item
2. Second Item
3. Third Item
```

> **Explanation**: The list starts with `1` and each subsequent item increments by one, satisfying the `ordered` style component of the default `one_or_ordered` style or an explicitly configured style of `ordered`.

Unlike the previous example, this list uses the `zero` style, where all items start with `0`.

```Markdown
0. First Item
0. Second Item
0. Third Item
```

> **Explanation**: All items start with `0`, satisfying the `zero` style configuration. This is a valid alternative to `one` or `ordered` styles.

Unlike the previous example, this scenario demonstrates that enabling the `allow_extended_start_values` configuration allows non-standard start values when using the `ordered` style.

```Markdown
2. second item
3. third item
```

> **Explanation**: With `allow_extended_start_values` enabled, the `ordered` style permits starting with `2`. The subsequent item `3` correctly increments from `2`, satisfying the `ordered` criteria.

Unlike the previous example, this scenario shows two separate lists where each can independently satisfy one of the different styles in the `one_or_ordered` style (`one` vs `ordered`) because the style determination resets for each list.

```Markdown
1. First Line
1. Second Line

text to break up lists

1. First Item
2. Second Item
3. Third Item
```

> **Explanation**: The first list uses the `one` style (all items start with `1`). The second list uses the `ordered` style (starts with `1` and increments). Since the lists are separated by text, the style reset allows both patterns to exist without triggering the rule.

## Fix Description

In `zero` or `one` configuration, all list items will be set to `0` or `1`
respectively.  In `ordered` configuration, if the first item does not start with
`0` or `1` it will be set to `1` with any other list items in that list increasing
from that base item in ordered fashion.

With the `one_or_ordered` style, behavior depends on whether the first item's start
is `1` or another number.  If it is not `1`, it is set to `1` and the list's style
is considered to be `ordered`. If it is `1`, the determination of the list's style
is delayed to the next list item, determining whether the `one` or `ordered` style
will be followed.  If that second list item is `1`, the `one` style is adopted.
Any other number for the second list item causes the `ordered` style to be adopted,
changing that second item's list start to `2`.

## Configuration

| Prefixes |
| --- |
| `plugins.md029.` |
| `plugins.ol-prefix.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `style` | `string` | `one_or_ordered` | Style for Ordered List Starts in the document. |
| `allow_extended_start_values` | `boolean` | `False` | Using the `ordered` style, allows for any integer to start the list. |

Valid styles:

| Style | Description |
| --- | --- |
| `one_or_ordered` | Either of the `one` or `ordered` styles below. |
| `one` | All Ordered List Items must start with `1`. |
| `ordered` | Starting with `0` or `1`, each List Item must be one greater than its predecessor. |
| `zero` | All Ordered List Items must start with `0`. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD029](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md029---ordered-list-item-prefix).

### Differences From MarkdownLint Rule

This rule differs from the original implementation in that it only
fires for the first non-matching item.  As that first item will most
likely provide the pattern for any other items that follow, it should
be enough to call out the first item and let the user fix the rest of
the list.
