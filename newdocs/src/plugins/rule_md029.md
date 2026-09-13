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

Consistent ordered list item prefixes create a predictable pattern that enhances
readability for sighted readers and assistive-technology users alike. They also
ensure that lists render correctly across different Markdown parsers and tools.

## Examples

### Failure Scenarios

This rule triggers when an ordered list item prefix is not `1` or `0` (depending
on configuration) or does not follow the expected order.

```Markdown
2. second item
3. third item
```

> **Explanation**: This list starts with `2`, which is not the allowed start value
> (`0` or `1`) for the default `one_or_ordered` style. Therefore, the rule triggers.

Unlike the previous example, this list starts with `1` but the subsequent item skips
a number.

```Markdown
1. first item
3. third item
```

> **Explanation**: The list starts with `1`, which is valid. However, the next item
> is `3`, skipping `2`. This violates the `ordered` style requirement where each
> item must increment by one.

Unlike the previous example, this list starts with an invalid number and does not
increment correctly.

```Markdown
3. first item
3. second item
```

> **Explanation**: The list starts with `3`, which is invalid. Additionally, the
> second item is also `3`, failing to increment from the previous item.

Unlike the previous examples, this scenario demonstrates nested ordered lists, where
each inner list starts a new evaluation of the rule based on the configured style.

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

> **Explanation**: Assuming the default `one_or_ordered` style, the rule triggers
> in multiple places. The outer list's first item starts with `2` instead of `1`
> or `0`. In the first inner list, the third item is `2` even though the `one` style
> requires every item to be `1`. In the second inner list, the third item is `2`
> even though the `ordered` style requires it to be `3`. This highlights that nested
> lists are evaluated independently according to the rule's style criteria.

Unlike the previous examples, this scenario demonstrates the `one` style, where
every item must be `1`, and the rule triggers when an item deviates.

```Markdown
1. first item
2. second item
```

> **Explanation**: With `style` set to `one`, every ordered list item must start
> with `1`. The second item is `2`, which violates the `one` style requirement.
> Unlike the previous examples, which operated under the default `one_or_ordered`
> style, this rule is stricter because `one` does not allow incrementing.

Unlike the previous examples, this scenario demonstrates the `zero` style, where
every item must be `0`, and the rule triggers when an item deviates.

```Markdown
0. first item
1. second item
```

> **Explanation**: With `style` set to `zero`, every ordered list item must start
> with `0`. The second item is `1`, which violates the `zero` style requirement.
> Unlike the previous examples, which used `one` or `one_or_ordered` styles, the
> `zero` style requires all items to be `0` with no incrementing allowed.

Unlike the previous examples, this scenario demonstrates the `ordered` style, where
items must increment, and the rule triggers when an item does not increment from
its predecessor.

```Markdown
1. first item
1. second item
```

> **Explanation**: With `style` set to `ordered`, each item must be one greater
> than its predecessor. The first item is `1`, so the second item must be `2`. The
> second item is `1`, which violates the `ordered` style requirement. Unlike the
> previous examples, which used `one` or `one_or_ordered` styles, the `ordered`
> style requires strict incrementing even when the first item is valid.

Unlike the previous example, this scenario demonstrates the `ordered` style with
`allow_extended_start_values` enabled, where the list starts with a valid extended
value but fails to increment.

```Markdown
5. first item
5. second item
```

> **Explanation**: With `style` set to `ordered` and `allow_extended_start_values`
> enabled, starting with `5` is valid. However, the second item is `5`, which fails
> to increment from `5` to `6`. This violates the `ordered` style requirement that
> each item must be one greater than its predecessor, even when extended start values
> are allowed.

### Correct Scenarios

This rule does not trigger when all ordered list items start with `1`, which is
one of the allowed styles (`one`).

```Markdown
1. First Line
1. Second Line
```

> **Explanation**: All items start with `1`, satisfying the `one` style component
> of the default `one_or_ordered` configuration or an explicitly configured style
> of `one`.

Unlike the previous example, this list starts with `1` and increments steadily,
satisfying the `ordered` style.

```Markdown
1. First Item
2. Second Item
3. Third Item
```

> **Explanation**: The list starts with `1` and each subsequent item increments
> by one, satisfying the `ordered` style component of the default `one_or_ordered`
> style or an explicitly configured style of `ordered`.

Unlike the previous example, this list uses the `zero` style, where all items start
with `0`.

```Markdown
0. First Item
0. Second Item
0. Third Item
```

> **Explanation**: All items start with `0`, satisfying the `zero` style configuration.
> This is a valid alternative to `one` or `ordered` styles.

Unlike the previous example, this scenario shows `ordered` style with `allow_extended_start_values`
enabled, allowing non-standard start values.

```Markdown
2. second item
3. third item
```

> **Explanation**: With `style` set to `ordered` and `allow_extended_start_values`
> enabled, the `ordered` style permits starting with `2`. The subsequent item `3`
> correctly increments from `2`, satisfying the `ordered` criteria.

Unlike the previous example, this scenario shows two separate lists where each can
independently satisfy one of the different styles in the `one_or_ordered` style
(`one` vs `ordered`) because the style determination resets for each list.

```Markdown
1. First Line
1. Second Line

text to break up lists

1. First Item
2. Second Item
3. Third Item
```

> **Explanation**: The first list uses the `one` style (all items start with `1`).
> The second list uses the `ordered` style (starts with `1` and increments). Since
> the lists are separated by text, the style reset allows both patterns to exist
> without triggering the rule.

Unlike the previous example, this scenario shows the `ordered` style starting with
`0` and incrementing by one.

```Markdown
0. First Item
1. Second Item
2. Third Item
```

> **Explanation**: The `ordered` style allows starting with either `0` or `1`. This
> list starts with `0` and each subsequent item increments by one, satisfying the
`ordered` style criteria.

## Fix Description

With a `zero` or `one` style, all list items will be set to `0` or `1`
respectively. In `ordered` configuration, if the first item does not start with
`0` or `1`, it will be set to `1` with any other list items in that list increasing
from that base item in sequential order.

With the `one_or_ordered` style, behavior depends on whether the first item's start
is `1` or another number. If it is not `1`, it is set to `1` and the list's style
is treated as `ordered`. If it is `1`, the determination of the list's style
is delayed to the next list item, determining whether the `one` or `ordered` style
will be followed. If that second list item is `1`, the `one` style is adopted.
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
| `allow_extended_start_values` | `boolean` | `False` | With the `ordered` style, allows the list to begin with any integer. |

### Valid Styles

| Style Name | Description |
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
fires for the first non-matching item. Because that first item most
likely establishes the pattern for the items that follow, reporting the
first item is sufficient for a reader to correct the remainder of the
list.
