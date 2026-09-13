# Rule - MD030

| Property | Value |
| --- | --- |
| Aliases | `md030`, `list-marker-space` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Ensure consistent spacing after list markers.

## Reasoning

### Consistency

Consistent spacing after list markers improves visual alignment and readability
for human readers, and helps ensure predictable rendering across parsers and screen
readers.

## Examples

### Failure Scenarios

This rule triggers when a list marker is followed by more than the configured number
of spaces before the text begins, with the default being 1 space.

```Markdown
1.  first item
```

> **Explanation**: This ordered list item has two spaces after the `1.` marker.
> By default, `ol_single` is set to `1`, so only one space is expected. The extra
> space violates the rule.

Unlike the previous example, this case uses an unordered list marker with multiple
trailing spaces.

```Markdown
+  first item
```

> **Explanation**: This unordered list item has two spaces after the `+` marker.
> By default, `ul_single` is set to `1`, so only one space is expected. The extra
> space violates the rule.

Unlike the previous single-line examples, this case demonstrates a multi-paragraph
unordered list item where the indentation of the continuation paragraph exceeds
the configured `ul_multi` value (configured to `2` in this example).

```Markdown
+ first item

   second paragraph
```

> **Explanation**: In a multi-paragraph list item, the continuation line must be
> indented according to the `ul_multi` setting. In this example, `ul_multi` is configured
> to `2`, but the continuation paragraph is indented with **three spaces**, exceeding
> the configured value. This violates the rule.

Unlike the previous unordered multi-paragraph example, this case uses an ordered
list marker where both the single-line spacing (`ol_single`) and the multi-paragraph
continuation spacing (`ol_multi`) are violated.

```Markdown
1.  First
1.  Second - 1

    Second - 2
1.  Third
```

> **Explanation**: All three `1.` markers are followed by **two spaces** instead
> of the configured `ol_single` value of `1`, violating the single-line spacing
> rule on lines 1, 2, and 5. Additionally, the continuation paragraph on line 4
> is indented with **four spaces** (two for the list structure + two for the continuation
> indent) instead of the configured `ol_multi` value of `1` (which would be two
> spaces total: two for structure + one for continuation). This violates the multi-paragraph
> spacing rule.

Unlike the previous unordered nested example, this case shows a nested ordered list
where every level's `1.` marker is followed by more spaces than the configured `ol_single`
value.

```Markdown
1.  First
    1.  Second
1.  Third
```

> **Explanation**: All three `1.` markers — the two outer items on lines 1 and 3,
> and the nested item on line 2 — are followed by **two spaces** instead of the
> configured `ol_single` value of `1`. The rule applies to every list marker at
> every nesting level, so all three violate the rule.

Unlike the previous `+` marker example, this case uses the hyphen/minus sign (`-`),
which is the most commonly used unordered list marker in practice.

```Markdown
-  first item
-  second item
```

> **Explanation**: The rule is marker-agnostic — it applies equally to `-`, `*`,
> and `+` markers. Both `-` markers here are followed by two spaces instead of the
> configured `ul_single` value of `1`. The extra space after each marker violates
> the rule.

Unlike the previous standalone list examples, this case shows a list nested inside
a blockquote, where the list marker spacing is still checked by this rule.

```Markdown
>  *  Heading 1
>  *  Heading 2
```

> **Explanation**: The rule applies to list markers at any nesting level, including
> those inside blockquotes. Both `*` markers are followed by **two spaces** instead
> of the configured `ul_single` value of `1`. The blockquote's `>` prefix and its
> spacing are governed by a different rule ([MD027](./rule_md027.md)), but the space
> after the list marker itself is still validated by this rule.

Unlike the previous examples, this case shows a nested unordered list where the
inner list marker is followed by more spaces than the configured `ul_single` value.

```Markdown
+ first item
  +  inner item
```

> **Explanation**: The outer `+` marker is followed by exactly one space (correct
> for `ul_single` = `1`), but the nested `+` marker is followed by **two spaces**.
> Because `ul_single` is `1`, the nested marker is also expected to have one space
> before its text. The extra space after the nested marker violates the rule, even
> though the outer list item itself is formatted correctly.

### Correct Scenarios

This rule does not trigger when all list items have the configured number of spaces
after the marker, with the default being 1 space.

```Markdown
1. first item
```

> **Explanation**: This ordered list item has exactly one space after the `1.` marker,
> matching the default `ol_single` value of `1`. The rule is satisfied.

Unlike the previous example, this case uses an unordered list marker with the correct
spacing.

```Markdown
+ first item
```

> **Explanation**: This unordered list item has exactly one space after the `+`
> marker, matching the default `ul_single` value of `1`. The rule is satisfied.

Unlike the previous simple examples, this scenario demonstrates a nested unordered
list with mixed single-line and multi-line items, where the configuration values
`ul_single` and `ul_multi` control the expected spacing differently. In this example,
the user has set `ul_multi` to `2`.

```Markdown
+ first item
+ second item
  +  inner item

     inner item
```

> **Explanation**: This nested list uses `ul_single` set to `1` for single-line
> items (e.g., "first item", "second item"). The nested "inner item" spans a blank
> line, making it a multi-paragraph item subject to `ul_multi`, which the user has
> set to `2` for this example. Each line respects the configured spacing for its
> item type, so the rule is not triggered.

## Fix Description

When fixed, the number of spaces between a list marker and the following text is
set to the configured amount of spacing. By default, this means ordered and unordered
list markers will be set to have 1 space after the text.

## Configuration

| Prefixes |
| --- |
| `plugins.md030.` |
| `plugins.list-marker-space.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `ul_single` | `integer` | `1` | Spaces after an Unordered List Item and any following text for a single line item. |
| `ol_single` | `integer` | `1` | Spaces after an Ordered List Item and any following text for a single line item. |
| `ul_multi` | `integer` | `1` | Spaces after an Unordered List Item and any following text for a multiple line item. |
| `ol_multi` | `integer` | `1` | Spaces after an Ordered List Item and any following text for a multiple line item. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD030](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md030---spaces-after-list-markers).
