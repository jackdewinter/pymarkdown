# Rule - MD007

| Property | Value |
| --- | --- |
| Aliases | `md007`, `ul-indent` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Ensure unordered list items use consistent indentation.

## Reasoning

### Readability

Markdown allows variable leading spaces before list markers, which can cause unexpected rendering and confuse readers. It is recommended that all unordered list markers start at the earliest allowed column.

### Consistency

Certain [Markdown parsers](https://babelmark.github.io/?text=%2B+sublist%0A++%2B+sublist%0A) require non-standard indentation to recognize sublists. This rule provides configuration options to accommodate these parsers and ensure consistent rendering across tools.

> **Note**: This rule only validates indentation for **unordered** list items.
> If you require indentation validation for **ordered** lists as well, disable
> this rule and enable the [PML101 rule](./rule_pml101.md) instead, which supports
> anchored indentation for both ordered and unordered lists.

## Examples

### Failure Scenarios

This rule triggers when an unordered list item has incorrect indentation relative to its parent or the base indent:

```Markdown
 * first item

* second item
   * sublist item
```

> **Explanation**: The first item has an extra leading space, violating the base indent of 0. The sublist item uses 3 spaces of indentation, which is not a multiple of the default indent value (2) relative to its parent, or exceeds the expected depth-based calculation depending on configuration.

Unlike the previous example, this case demonstrates a sublist item with insufficient indentation, using only 1 space instead of the required default of 2.

```Markdown
* parent item
 * sublist with only 1 space
```

> **Explanation**: The sublist item is indented by only 1 space, which does not match the configured `indent` value of 2. The rule requires that each level of nesting increases indentation by the configured amount. Because 1 is not a multiple of the configured indent relative to the parent, the rule triggers.

Unlike the previous examples, this case involves a deeply nested sublist (three levels deep) where the third level is indented by 3 spaces instead of the expected 4.

```Markdown
* level 1
  * level 2
   * level 3 with only 3 spaces
```

> **Explanation**: The third-level sublist item is indented by only 3 spaces from the start of the line. Given a base indent of 0 and an `indent` value of `2`, the expected indentation for the third level is `0 + (3-1)*2 = 4` spaces. The actual indentation of 3 spaces deviates from this calculation, causing the rule to trigger.

Unlike the previous examples, this case involves an unordered list nested inside a block quote, where the sublist indentation fails to align with the adjusted base indent.

```Markdown
> * item in block quote
>  * correct sublist indent
>   * incorrect sublist with extra space
```

> **Explanation**: Inside a block quote, the base indent is shifted. The first list item starts at the correct position relative to the block quote marker. The second sublist item uses the correct additional indentation (2 spaces). However, the third sublist item uses 3 additional spaces relative to its parent, exceeding the configured `indent` value of `2`. The rule validates that indentation increments match the configuration regardless of the container context.

### Correct Scenarios

This rule does not trigger when all unordered list items use consistent indentation matching the default indent value.

```Markdown
* first item

* second item
  * sublist item
```

> **Explanation**: All list markers start at the correct column. The sublist item is indented by `2` spaces relative to its parent, matching the default indent configuration.

Unlike the previous example, this case uses a custom indent value of `3`.

```Markdown
* first item
   * sublist item
```

> **Explanation**: When configured with `indent` equal to `3`, a 3-space indent for the sublist is valid. The rule checks that indentation aligns with the configured multiple.

Unlike the previous examples, this case involves a mixed list with an ordered list item breaking the unordered list chain.

```Markdown
* indented properly
  1. indented properly
     * indented properly
```

> **Explanation**: The ordered list item creates a new nesting context. The unordered list item that follows is treated as a sublist of the ordered item, with a base indent determined by the ordered list's content column. Its `2`-space indentation relative to this base matches the configured `indent` value, satisfying the rule.

Unlike the previous examples, this case demonstrates the `start_indented` configuration set to `True`.

```Markdown
  * indented at first level
    * sublist indented correctly
```

> **Explanation**: When `start_indented` is `True`, the first level of the
> unordered list is allowed to start with the configured indent value (default
> `2`). This accommodates parsers that expect all list levels to be indented
> uniformly. The sublist is indented by another `2` spaces relative to its
> parent, maintaining consistency.

If indentation support is also required for ordered lists,
refer to the selection below on [Python-Markdown Support](#python-markdown-support).

### Notes

#### Python-Markdown Support

If you are using [Python-Markdown](https://python-markdown.github.io/) or tools
that use it such as the popular [MkDocs](https://www.mkdocs.org/), this rule
should be disabled in favor of enabling the [PML101 rule](./rule_pml101.md). That
rule supports proper anchored list indentation, our name for the indentation method
that is required to support parsers like the Python-Markdown parser.

#### Unordered Lists Only

The indentation measured by this rule solely covers the indentation for any
unordered list items. Therefore, if the following Markdown is scanned under
normal circumstance:

```Markdown
1. ordered indent
   * unordered indent
```

this rule will not be triggered. However, the following Markdown:

```Markdown
1. ordered indent
    * unordered indent
```

will trigger the rule as it is expecting the unordered list to start at column
4, not column 5.

> **Note**: For comprehensive indentation checking that includes **ordered**
> lists, see the [PML101 rule](rule_pml101.md).

## Fix Description

Each unordered list item and its child items are examined
to make sure that they start with a multiple of the specified `indent`. If an
unordered list is started within a block quote or ordered list item, the base indent
within that element is calculated. If not in either of those two elements, the
base indent is `0`. The number of unordered list item elements (referred to as
the list depth) is calculated.

A simple calculation is made to determine the ideal indent: the base indent plus
the `indent` value multiplied by the list depth minus `1`. If that value
differs from the actual indent, the rule adjusts the list item start element or
the new list item element to start at that calculated location.

Therefore, for the above example:

```Markdown
1. ordered indent
    * unordered indent
```

the base indent is `3` and the list depth is `1`. Therefore `3 + (1-1)*2` equals
`3`, adjusting the unordered list start to have an indent of 3:

```Markdown
1. ordered indent
   * unordered indent
```

The same calculation happens for a new list item for that list, arriving at the same
list depth, and therefore the same calculated indent. For any nested lists, the
list depth is increased accordingly, resulting in indents of `5`, `7`, `9`, and
so on.

## Configuration

| Prefixes |
| --- |
| `plugins.md007.` |
| `plugins.ul-indent.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `indent` | `integer` | `2` | Number of spaces needed between unordered sublists starts. |
| `start_indented` | `boolean` | `False` | Whether the first unordered list should be indented. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD007](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md007---unordered-list-indentation).

### Differences From MarkdownLint Rule

The original rule did not work for Unordered List elements within
Ordered List elements. For example, the original rule does not fire
on the following sample:

```Markdown
1.  ordered list
    + sublist
       + sublist
```

while our version of this rule fires in those situations.
