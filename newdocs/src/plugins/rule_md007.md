# Rule - MD007

| Property | Value |
| --- | -- |
| Aliases | `md007`, `ul-indent` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Unordered list indentation.

## Reasoning

### Readability/Consistency

Existing specifications for Markdown specify that multiple spaces are allowed
before a list start item. As the use of those existing spaces typically
causes the list items to start in unexpected locations, there is a good chance
that the use of those "extra" spaces will just confuse readers. It is instead
recommended that all unordered list markers start at the first column
where they are allowed, without any unrequired indentation.

In addition, there are
[various Markdown parsers](https://babelmark.github.io/?text=%2B+sublist%0A++%2B+sublist%0A)
that do not acknowledge the start of a sublist without a non-standard amount of indentation
before the sublist item.  This rule supplies configuration for those situations to
allow consistent rendering between parsers.

## Examples

### Failure Scenarios

This rule triggers if any Unordered List element or new List Item element
does not start with the correct indentation:

```Markdown
 * indented with extra space

* indented properly
   * but sublist is not
```

### Correct Scenarios

To correct the above example, simply enforce the required indentation using the
proper number of space characters:

```Markdown
* indented with extra space

* indented properly
  * but sublist is not
```

If required, the amount of indentation at each level can be set using the `indent`
configuration value.  Note that an `indent` value of `3` will make the following
example correct:

```Markdown
* indented properly
   * but sublist is not
```

but it will also not trigger in the case of a list like this one:

```Markdown
* indented properly
  1. indented properly
     * indented properly
```

The reason for this is that the ordered list breaks up the "chain" of unordered
lists into two distinct unordered lists, as this rule does not apply to ordered
list indentations.  If indentation support is also required for ordered lists,
refer to the selection below on [Python-Markdown Support](#python-markdown-support).

In addition, there are occasions where parsers expect to start the first level of
lists with the specified amount of indentation.  For those situations, the `start_indented`
configuration value can be set to `True` to accommodate these parsers.

### Notes

#### Python-Markdown Support

If you are using [Python-Markdown](https://python-markdown.github.io/) or tools
that use it such as the popular [MkDocs](https://www.mkdocs.org/), this rule
should be disabled in favor of enabling the [Pml101 rule](rule_pml101.md).  That
rule supports proper anchored list indentation, our name for the indentation method
that is required to support parsers like the Python-Markdown parser.

#### Unordered Lists Only

The indentation measured by this rule solely covers the indentation for any
unordered list items.  Therefore, if the following Markdown is scanned under
normal circumstance:

```Markdown
1. ordered indent
   * unordered indent
```

this rule will not be triggered.  However, the following Markdown:

```Markdown
1. ordered indent
    * unordered indent
```

will trigger the rule as it is expecting the unordered list to start at column
4, not column 5.

## Fix Description

Any unordered list item elements and their new list item elements are examined
to make sure that they start with a multiple of the specified `indent`.  If an
unordered list is started within a block quote or ordered list item, the base indent
within that element is calculated.  If not in either of those two elements, the
base indent is `0`.  The number of unordered list item elements (referred to as
the list depth) is calculated.

A simple calculation is made to determine the ideal ident: the base indent plus
the `indent` value multiplied by the list depth minus `1`.  If that value
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
list depth, and therefore the same calculated indent.  For any nested lists, the
list depth is increased accordingly, resulting in indents of `5`, `7`, `9`, and
so on.

## Configuration

| Prefixes |
| --- |
| `plugins.md007.` |
| `plugins.ul-indent.` |

<!-- pyml disable-num-lines 5 line-length-->
| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `indent` | `integer` | `2` | Number of spaces needed between unordered sublists starts. |
| `start_indented` | `boolean` | `False` | Whether the first unordered list should be indented. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD007](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md007---unordered-list-indentation).

### Differences From MarkdownLint Rule

The original rule did not work for Unordered List elements within
Ordered List elements.  For example, the original rule does not fire
on the following sample:

```Markdown
1.  ordered list
    + sublist
       + sublist
```

while our version of this rule fires in those situations.
