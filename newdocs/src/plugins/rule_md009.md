# Rule - MD009

| Property | Value |
| --- | --- |
| Aliases | `md009`, `no-trailing-spaces` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Trailing spaces are not allowed.

## Reasoning

### Simplicity

Trailing spaces serve no visible purpose in rendered HTML unless they constitute a hard line break (default: two spaces). Allowing arbitrary trailing spaces adds unnecessary complexity and whitespace clutter.

## Examples

To improve visibility in the following examples, the pipe character (`|`) marks line endings for visibility and is not evaluated by the rule.

### Failure Scenarios

This rule triggers when a line ends with a single trailing space, which differs from the default `br_spaces` value of 2.

```Markdown
this line ends with one space character |
```

> **Explanation**: This line ends with one trailing space. Since the default for `br_spaces` is `2`, a single space is not a valid hard line break indicator and is considered trailing whitespace, thus triggering the rule.

Unlike the previous example, this scenario sets `strict` to `True`, causing any trailing spaces (including those matching `br_spaces`) to trigger the rule.

```Markdown
This line does not end with any spaces.|
This line ends with one space. |
This line ends with two spaces.  |
This line ends with three spaces.   |
```

> **Explanation**: With `strict` set to `True`, all lines ending with any number of spaces are flagged, regardless of the `br_spaces` setting. The first line passes only because it has zero spaces. The subsequent lines fail because they contain trailing spaces, which are prohibited in strict mode.

Unlike the previous examples, this scenario demonstrates that by default, trailing spaces on empty lines within list items trigger the rule because `list_item_empty_lines` is set to `False`.

```Markdown
1. a list item
   |
   still the same item, different paragraph
```

> **Explanation**: By default, `list_item_empty_lines` is `False`, meaning trailing spaces on empty lines inside list items are flagged as violations. The space on the empty line serves no rendering purpose and is considered trailing whitespace, thus triggering the rule.

Unlike the previous example, this scenario shows that even when `list_item_empty_lines` is set to `True`, trailing spaces beyond the required indentation on empty lines within list items still trigger the rule.

```Markdown
1. a list item
    |
   still the same item, different paragraph
```

> **Explanation**: With `list_item_empty_lines` set to `True`, empty lines are exempt only if they contain exactly the spaces needed to maintain list structure. Here, the list item's content is indented by three spaces, so the empty line should also have three spaces. Because it has four, the extra space is treated as trailing whitespace and triggers the rule.

Unlike the previous examples, this scenario demonstrates that trailing spaces within HTML blocks trigger the rule, since HTML blocks are not exempt like code blocks.

```Markdown
<!--
this is a |
HTML block |
-->

<abc>  |
</abc>  |
```

> **Explanation**: Unlike fenced code blocks and indented code blocks, HTML blocks are evaluated by this rule. A single trailing space within the `<!--` and `-->` lines triggers the rule because it does not match the default `br_spaces` value of `2`. The lines with two trailing spaces (`<abc>  |` and `</abc>  |`) do not trigger because two spaces match the default `br_spaces` setting and are treated as valid hard line break indicators.

### Correct Scenarios

This rule does not trigger when lines have no trailing spaces or exactly the number of spaces specified by `br_spaces`.

```Markdown
This line does not end with any spaces.|
This line ends with two spaces, which is okay.  |
```

> **Explanation**: The first line has no trailing spaces, so it passes. The second line has exactly two trailing spaces, which matches the default `br_spaces` value of `2`, so it is treated as a valid hard line break indicator and does not trigger the rule.

Unlike the previous examples, this scenario demonstrates that lines within fenced code blocks do not trigger this rule, even if they contain trailing spaces.

````Markdown
```python
def my_function():
  print("""  |
""")
```
````

> **Explanation**: Fenced code blocks are excluded from this rule's evaluation to preserve syntax validity in programming languages that may require or allow trailing whitespace. Therefore, the trailing spaces on the `print` line do not trigger the rule.

Unlike the previous examples, this scenario shows that list item empty lines are exempt from the rule when the `list_item_empty_lines` configuration is set to `True`.

```Markdown
1. a list item
   |
   still the same item, different paragraph
```

> **Explanation**: By default, trailing spaces on blank lines inside list items would trigger the rule. However, with `list_item_empty_lines` set to `True`, trailing spaces on empty lines that serve only to maintain the list structure are ignored, so the rule does not trigger.

## Fix Description

When fixed, each eligible line will either have 0 whitespace characters or `br_spaces`
whitespace characters at the end of that line.

## Configuration

| Prefixes |
| --- |
| `plugins.md009.` |
| `plugins.no-trailing-spaces.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `br_spaces` | `integer` | `2` | Specifies the exact number of spaces allowed at the end of the line. |
| `strict` | `boolean` | `False` | Whether strict mode is enabled for the plugin. |
| `list_item_empty_lines` | `boolean` | `False` | Whether empty list item lines are exempt from this rule. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD009](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md009---trailing-spaces).

### Differences From MarkdownLint Rule

The main difference from the original rule is in how an HTML block is
managed. According to the original rule:

> Trailing space is allowed in indented and fenced code blocks because some languages
> require it.

However, in tests against the original rule, HTML blocks seemed to be
immune to triggering this rule. This rule adheres to the text in the
original specification by not triggering on indented code blocks and
fenced code blocks but triggering on HTML blocks.

In addition, the original implementation used the `br_spaces` value
when using the `list_item_empty_lines` configuration value to decide
if that List Item Empty Line triggered the rule. That algorithm has
been changed in this rule to instead use the number of spaces
required to satisfy the indentation requirements of the List element.
