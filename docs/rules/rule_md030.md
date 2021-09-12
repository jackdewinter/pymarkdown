# Rule - MD030

| Aliases |
| --- |
| `md030` |
| `list-marker-space` |

## Summary

Spaces after list markers.

## Reasoning

The main reason for this rule is consistency.  Some older parsers
do not handle varying amount of spaces after the list marksers properly.

## Examples

### Failure Scenarios

This rule triggers when a List Item element is not followed by 1 space
character before the text starts:

````Markdown
1.  first item
````

````Markdown
+  first item
````

### Correct Scenarios

This rule does not trigger if all List Item elements are followed by
1 space before any text starts:

````Markdown
1. first item
````

````Markdown
+ first item
````

The `ol_single` and `ol_multi` configuration values specify the number of space
before text for Ordered List elements, and the `ul_single` and `ul_multi` configuration
values specify the number of space before text for Unordered List elements.
For the purpose of this rule, a `single` line List Item is one that contains text
only on the line on which that given List Item is started.

Therefore, setting `ul_single` to 2 and `ul_multi` to 1 will cause this list not
to trigger this rule:

```Markdown
+ first item
+ second item
  +  inner item
```

## Configuration

| Prefixes |
| --- |
| `plugins.md030.` |
| `plugins.list-marker-space.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled by default. |
| `ul_single` | integer | `1` | Spaces after an Unordered List Item and any following text for a single line item. |
| `ol_single` | integer | `1` | Spaces after an Ordered List Item and any following text for a single line item. |
| `ul_multi` | integer | `1` | Spaces after an Unordered List Item and any following text for a multiple line item. |
| `ol_multi` | integer | `1` | Spaces after an Ordered List Item and any following text for a multiple line item. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD030](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md030---spaces-after-list-markers).
