# Rule - MD007

| Aliases |
| --- |
| `md007` |
| `ul-indent` |

| Autofix Available |
| --- |
| Yes |

## Summary

Unordered list indentation.

## Reasoning

### Readability/Consistency

While existing specifications for Markdown specify that multiple spaces
are allowed, using those extra spaces will confuse readers.  Instead,
it is recommended that all unordered list markers start at the first column
where they are allowed, without any extra indentation.

In addition, there are
[various Markdown parsers](https://babelmark.github.io/?text=%2B+sublist%0A++%2B+sublist%0A)
that do not acknowledge a sublist without a non-standard amount of indentation
before the sublist.  This rule supplies configuration for those situations to
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

To correct the above example, simply enforce the required indentation using space
characters:

```Markdown
* indented with extra space

* indented properly
  * but sublist is not
```

If required, the amount of indentation at each level can be set using
the `indent` configuration value.  This may be needed for certain parsers
that require four space characters for indentation instead of the normal
two characters.  For those parsers, the following example specifies a
valid list with a sublist:

```Markdown
* indented properly
    * but sublist is not
```

In addition, to start the first level of lists with the specified amount
of indentation, the `start_indented` configuration value can be set to
`True`.

### Notes

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

## Configuration

| Prefixes |
| --- |
| `plugins.md007.` |
| `plugins.ul-indent.` |

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

## Fix Description

Any unordered list item elements and their new list item elements are examined
to make sure that they start with a multiple of the specified `indent`.  If an
unordered list is started within a block quote or ordered list item, the base indent
within that element is calculated.  If not in either of those two elements, the
base indent is `0`.  The number of containing unordered list item elements or list
depth is calculated.

A simple calculation is made to determine the ideal ident: the base indent plus
the `indent` value multiplied by the list depth minus `1`.  If that value
differs from the actual indent, the list item start element or the new list item
element is adjusted to start at that calculated location.

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
