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

Some older parsers do not handle varying numbers of spaces after list markers well. Consistent spacing also improves visual alignment and readability for human readers.

## Examples

### Failure Scenarios

This rule triggers when a list marker is followed by more than the configured number of spaces before the text begins, with the default being 1 space.

````Markdown
1.  first item
````

> **Explanation**: This ordered list item has two spaces after the `1.` marker. By default, `ol_single` is set to `1`, so only one space is expected. The extra space violates the rule.

Unlike the previous example, this case uses an unordered list marker with multiple trailing spaces.

````Markdown
+  first item
````

> **Explanation**: This unordered list item has two spaces after the `+` marker. By default, `ul_single` is set to `1`, so only one space is expected. The extra space violates the rule.

Unlike the previous single-line examples, this case demonstrates a multi-paragraph unordered list item where the spacing after the list marker exceeds the configured `ul_multi` value.

```Markdown
+ first item

   second paragraph
```

> **Explanation**: This unordered list item spans multiple paragraphs. By default, `ul_multi` is set to `2`, meaning **two spaces** are expected after the list marker for multi-line items. The second paragraph here has **three spaces**, exceeding the configured value. This violates the rule.

### Correct Scenarios

This rule does not trigger when all list items have the configured number of spaces after the marker, with the default being 1 space.

```Markdown
1. first item
```

> **Explanation**: This ordered list item has exactly one space after the `1.` marker, matching the default `ol_single` value of `1`. The rule is satisfied.

Unlike the previous example, this case uses an unordered list marker with the correct spacing.

```Markdown
+ first item
```

> **Explanation**: This unordered list item has exactly one space after the `+` marker, matching the default `ul_single` value of `1`. The rule is satisfied.

Unlike the previous simple examples, this scenario demonstrates a nested unordered list with mixed single-line and multi-line items, where configuration values `ul_single` and `ul_multi` control the expected spacing differently.

```Markdown
+ first item
+ second item
  +  inner item

     inner item
```

> **Explanation**: This nested list uses `ul_single` = `1` for simple items (e.g., `first item`, `second item`) and `ul_multi` = `2` for multi-paragraph items (e.g., the nested `inner item` with a blank line). Each item respects the configured spacing for its type, so the rule is not triggered.

## Fix Description

When fixed, the number of spaces between a list start and the following text is
set to the configured amount of spacing.  By default, this means ordered and unordered
list markers will be set to have 1 space before the text.

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
