# Rule - MD007

| Aliases |
| --- |
| `md007` |
| `ul-indent` |

## Summary

Unordered list indentation.

## Reasoning

The primary reason for this rule is consistency.  While existing specifications
for Markdown specify that multiple spaces are allowed, using those extra spaces
will confused the reader.  Instead, it is recommended that all unordered list
markers start at the first column where they are allowed, without any extra
indentation.

In addition, there are
[various Markdown parsers](https://babelmark.github.io/?text=%2B+sublist%0A++%2B+sublist%0A)
that do not acknowledge a sublist without a non-standard amount of indentation
before the sublist.  This rule provides configuration for those situations.

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
the `indent` configuration value.  This may be required for certain parsers
that require four space characters for indentation instead of the normal
two characters.  For thost parsers, the following example specifies a
valid list with a sublist:

```Markdown
* indented properly
    * but sublist is not
```

In addition, to start the first level of lists with the specified amount
of indentation, the `start_indented` configuration value can be set to
`True`.

## Configuration

| Prefixes |
| --- |
| `plugins.md007.` |
| `plugins.ul-indent.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the plugin rule is enabled by default. |
| `indent` | `integer` | `2` | Number of spaces required between unordered sublists. |
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
