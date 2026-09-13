# Rule - MD009

| Property | Value |
| --- | --- |
| Aliases | `md009`, `no-trailing-spaces` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Prohibit trailing whitespace on every line, except where it is an intentional hard
line break.

## Reasoning

### Simplicity

Trailing spaces serve no visible purpose in rendered HTML unless they constitute
a hard line break (default: two spaces). Allowing arbitrary trailing spaces adds
unnecessary complexity and whitespace clutter.

## Examples

> **Note**: A trailing pipe (`|`) for an example line is a visual marker used
> to make trailing spaces visible. The pipe itself is **not** part of the example
> and is not evaluated by the rule.

### Failure Scenarios

This rule triggers when a line ends with a single trailing space, which differs
from the default `br_spaces` value of 2.

```Markdown
this line ends with one space character |
```

> **Explanation**: This line ends with one trailing space. Since the default for
> `br_spaces` is `2`, a single space is not a valid hard line break indicator and
> is considered trailing whitespace, thus triggering the rule.

Unlike the previous example, this scenario sets `strict` to `True`, causing any
trailing spaces (including those matching `br_spaces`) to trigger the rule.

```Markdown
This line does not end with any spaces.|
This line ends with one space. |
This line ends with two spaces.  |
This line ends with three spaces.   |
```

> **Explanation**: With `strict` set to `True`, all lines ending with any number
> of spaces are flagged, regardless of the `br_spaces` setting. The first line does
> not trigger only because it has zero spaces. The subsequent lines fail because
> they contain trailing spaces, which are prohibited in strict mode.

Unlike the previous example, this scenario shows that when `list_item_empty_lines`
is at its default value (`False`), trailing spaces on empty lines within list items
trigger the rule.

```Markdown
1. a list item
   |
   still the same item, different paragraph
```

> **Explanation**: By default, `list_item_empty_lines` is `False`, meaning trailing
> spaces on empty lines inside list items are flagged as violations. The space on
> the empty line serves no rendering purpose and is considered trailing whitespace,
> thus triggering the rule.

Unlike the previous example, this scenario shows that even when `list_item_empty_lines`
is set to `True`, trailing spaces beyond the required indentation on empty lines
within list items still trigger the rule.

```Markdown
1. a list item
    |
   still the same item, different paragraph
```

> **Explanation**: With `list_item_empty_lines` set to `True`, an empty line inside
> a list item is exempt only for the spaces required to preserve the list indentation
> (three spaces here, matching the indent of `still the same item`). Any spaces
> beyond that allowance are still trailing whitespace. Because the example line
> contains four spaces, the fourth space is treated as trailing whitespace and triggers
> the rule.

Unlike the previous examples, this scenario demonstrates that trailing spaces within
HTML blocks trigger the rule, since HTML blocks are not exempt like code blocks.

```Markdown
<!--
this is a |
HTML block |
-->
```

> **Explanation**: Unlike fenced code blocks and indented code blocks, HTML blocks
> are evaluated by this rule. The inner content line starting with `this is a` ends
> with a single trailing space, which does not match the default `br_spaces` value
> of `2`, so the rule triggers.

### Correct Scenarios

This rule does not trigger when lines have no trailing spaces or exactly the number
of spaces specified by `br_spaces`.

```Markdown
This line does not end with any spaces.|
This line ends with two spaces, which is okay.  |
```

> **Explanation**: The first line has no trailing spaces, so it passes. The second
> line has exactly two trailing spaces, which matches the default `br_spaces` value
> of `2`, so it is treated as a valid hard line break indicator and does not trigger
> the rule.

Unlike the previous examples, this scenario demonstrates that lines within fenced
code blocks do not trigger this rule, even if they contain trailing spaces.

````Markdown
```python
def my_function():
  print("""  |
""")
```
````

> **Explanation**: Fenced code blocks are excluded from this rule's evaluation because
> code content is governed by the programming language, not by Markdown structural
> rules. Trailing whitespace within code is the author's responsibility and is not
> considered trailing whitespace in the Markdown sense.

Unlike the previous examples, this scenario shows that list item empty lines are
exempt from the rule when the `list_item_empty_lines` configuration is set to `True`.

```Markdown
1. a list item
   |
   still the same item, different paragraph
```

> **Explanation**: By default, trailing spaces on blank lines inside list items
> trigger the rule. However, with `list_item_empty_lines` set to `True`, trailing
> spaces on empty lines that serve only to maintain the list structure are ignored,
> so the rule does not trigger.

Unlike the previous correct examples, this case shows an HTML block whose lines
end with exactly `br_spaces` (the default `2`) trailing spaces, in contrast with
the HTML-block failure example that used a single trailing space.

```Markdown
<abc>  |
</abc>  |
```

> **Explanation**: Both HTML lines end with exactly two spaces, matching the default
> `br_spaces` value of `2`. Two trailing spaces constitute a valid hard line break
> indicator, so they are not classified as trailing whitespace and the rule does
> not fire. (Contrast with the earlier HTML-block failure example, where the HTML
> block's lines ended with a *single* space that did not match `br_spaces`.)

Unlike the previous examples, this scenario shows that lines within an indented
code block are also exempt from this rule, even if they contain trailing spaces.

```Markdown
    def my_function():
      print("hello world  |")
```

> **Explanation**: Indented code blocks are excluded from this rule's evaluation
> for the same reason as fenced code blocks: the content is governed by the programming
> language, not by Markdown structural rules. The four-space indentation that establishes
> the code block, as well as any trailing spaces within the code, are the author's
> responsibility and are not considered trailing whitespace in the Markdown sense.

## Fix Description

When fixed, the trailing whitespace on each eligible line is removed or normalized
so that the line ends with either 0 whitespace characters or exactly `br_spaces`
whitespace characters. Lines that already end with exactly `br_spaces` whitespace
characters are preserved as-is, since they represent an intentional hard line break.

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
immune to triggering this rule. This rule follows the text of the
original specification: it does not trigger on indented or fenced code
blocks, but it does trigger on HTML blocks.

In addition, the original implementation used the `br_spaces` value
together with the `list_item_empty_lines` configuration value to decide
whether a list item empty line triggered the rule. That algorithm has
been changed in this rule to instead use the number of spaces
required to satisfy the indentation requirements of the list element.
