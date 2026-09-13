# Rule - PML101

| Property | Value |
| --- | --- |
| Aliases | `pml101`, `list-anchored-indent` |
| Autofix Available | No |
| Enabled By Default | No |

## Summary

Enforce that base lists are anchored at an allowed column and that every sub-list
is indented by a multiple of the configured indent width.

## Reasoning

### Compatibility

Some Markdown parsers, such as [Python-Markdown](https://python-markdown.github.io/),
enforce the original Markdown specification's requirement that sub-list items be
indented by exactly 4 spaces (or one tab stop). This rule supports that stricter
behavior, which differs from the relaxed indentation that GitHub Flavored Markdown
allows.

> **Advisory**: This rule was developed as an alternative to
> [Rule MD007](./rule_md007.md). See the Origination of Rule section for details.
> It is strongly advised to disable Rule MD007 when enabling Rule PML101.

## Examples

### Failure Scenarios

This rule triggers when an initial (base) list is not anchored at an allowed column
(column 1, or an odd column greater than 1 when inside a block quote).

```Markdown
 * poorly indented unordered list
1. poorly indented ordered list
>  * poorly indented list within a block quote
```

> **Explanation**: Each base list in the example begins at an indentation
> that is neither column 1 nor an allowed odd column inside a block quote.
> Because PML101 requires base lists to be anchored at one of those columns
> (see the `enabled` and `indent` keys in the Configuration section), all
> three base lists above violate the rule.

Unlike the previous example, this scenario shows a properly anchored base list whose
*sublists* fail to sit at a multiple-of-4 (default) offset to the right of the base
list's column.

```Markdown
* properly indented unordered list
  * indented according to MD007

1. properly indented ordered list
   1. indented according to MD007

> * properly indented list within a block quote
>   * indented according to MD007
```

> **Explanation**: The base lists above are correctly anchored, but each sub-list
> starts 1 or 3 spaces in from the base list instead of 4, 8, 12, … spaces in. This
> rule requires every sub-list to start at `base_column + N*indent` (with the default
> `indent = 4`), so each sub-list in this example violates the rule.

Unlike the previous example, this scenario uses the `indent` value set to `2`.
Here the base list is anchored correctly, but the sub-list is offset by 3 spaces
(1 + 3), which is not a multiple of 2 relative to the base column.

```Markdown
* base list anchored at column 1
   * sub-list offset by 3 spaces (not a multiple of indent=2)
```

> **Explanation**: With `indent` set to `2`, sub-lists must start at base + 2,
> base + 4, base + 6, … The sub-list above starts 3 spaces past the base, which
> is not in that set, so it violates the rule.

Unlike the previous examples, this scenario places a *deeper* (level-2) sub-list
at an offset that is not a multiple of `indent` from the base list's column, even
though the level-1 sub-list is correctly indented.

```Markdown
* base list anchored at column 1
    * level-1 sub-list offset by 4 spaces (valid)
       * level-2 sub-list offset by only 2 more spaces (total 6, not a multiple of 4)
```

> **Explanation**: With the default `indent` of 4, every sub-list at any depth must
> start at `base_column + N*4` (column 5, 9, 13, …). The level-1 sub-list sits at
> column 5, which is valid. The level-2 sub-list sits at column 7 (1 + 4 + 2),
> which is not in that set, so it violates the rule even though its *parent*
> is correctly indented. The rule is measured against the base list's anchor,
> not against the immediate parent.

Unlike the previous examples, this scenario combines *both* violations in a single
snippet: the base list is not anchored at an allowed column **and** the sub-list
offset is not a multiple of `indent`.

```Markdown
  * base list not anchored at column 1
     * sub-list offset by 2 spaces from the (mis-anchored) base
```

> **Explanation**: Two independent violations occur here. First, the base list
> begins at column 3, which is neither column 1 nor an allowed odd column inside
> a block quote, so the anchoring requirement fails. Second, even if the anchor
> were accepted, the sub-list begins 2 spaces to the right of the base (column 5),
> which is not a multiple of the default `indent` of 4, so the sub-list
> indentation requirement also fails.

### Correct Scenarios

This rule does not trigger when both the base list is anchored at an allowed column
and every sub-list sits at a multiple-of-4 (default) offset to the right of that
anchor.

```Markdown
* properly indented unordered list
    * indented according to MD007

1. properly indented ordered list
    1. indented according to MD007

> * properly indented list within a block quote
>     * indented according to MD007
```

> **Explanation**: Each base list above is anchored at an allowed column
> (column 1, or an odd column inside the block quote), and each sub-list
> starts exactly 4 spaces to the right of its base list's column. This satisfies
> both anchoring and sub-list indentation requirements of PML101 with the default
> `indent` of 4.

Unlike the previous example, this scenario uses a non-default `indent` value
(`indent: 2`). The base list is still anchored at an allowed column, but the
valid sub-list offsets are now 2, 4, 6, … spaces to the right of the anchor
rather than 4, 8, 12, ….

```Markdown
* base list anchored at column 1
  * sub-list offset by 2 spaces (valid when indent = 2)
    * sub-list offset by 4 spaces (valid when indent = 2)

1. base list anchored at column 1
   1. sub-list offset by 2 spaces (valid when indent = 2)
      1. sub-list offset by 4 spaces (valid when indent = 2)

> * base list anchored inside a block quote
>   * sub-list offset by 2 spaces (valid when indent = 2)
>     * sub-list offset by 4 spaces (valid when indent = 2)
```

> **Explanation**: With `indent: 2`, the rule requires each sub-list to start at
> `base_column + N*2` for some positive integer `N`. The first sub-list in each
> list is offset by 2 (`N = 1`) and the second by 4 (`N = 2`), both of which
> are valid multiples of the configured `indent`. The base lists remain anchored
> at allowed columns (column 1, or an odd column inside the block quote), so
> neither the anchoring requirement nor the sub-list indentation requirement is
> violated.

Unlike the previous examples, this scenario shows a 3-level-deep list at the
default `indent` of 4. Each level is anchored 4, 8, and 12 spaces to the right
of the base list's column (columns 5, 9, and 13), all valid multiples of 4.

```Markdown
* base list anchored at column 1
    * level-1 sub-list at column 5 (1 + 4)
        * level-2 sub-list at column 9 (1 + 8)
            * level-3 sub-list at column 13 (1 + 12)

1. base list anchored at column 1
    1. level-1 sub-list at column 5 (1 + 4)
        1. level-2 sub-list at column 9 (1 + 8)
            1. level-3 sub-list at column 13 (1 + 12)
```

> **Explanation**: With the default `indent` of 4, the rule requires every
> sub-list at any depth to start at `base_column + N*4` for some positive
> integer `N`. Here `N = 1` (column 5), `N = 2` (column 9), and `N = 3`
> (column 13), all of which are valid. The base list remains anchored at
> column 1, so neither the anchoring requirement nor the sub-list indentation
> requirement is violated.

### Notes

On the [Python-Markdown](https://python-markdown.github.io/) page detailing
their implementation [differences](https://python-markdown.github.io/#differences),
the authors clearly state:

> Indentation/Tab Length
>
> The syntax rules clearly state that when a list item consists of multiple paragraphs,
> "each subsequent paragraph in a list item must be indented by either 4 spaces or
> one tab" (emphasis added). However, many implementations do not enforce this rule
> and allow less than 4 spaces of indentation. The implementers of Python-Markdown
> consider it a bug to not enforce this rule.

The rule that they refer to is the initial
[Markdown specification](https://daringfireball.net/projects/markdown/syntax),
not the more recent [GitHub Flavored Markdown](https://github.github.com/gfm/)
specification.

PyMarkdown's linter does not weigh
in on the benefits or costs of that decision but seeks to help support the parser
as it is.  To that extent, this rule provides an alternative implementation to
[rule MD007](./rule_md007.md) that supports the initial specification as implemented
by Python-Markdown.  We refer to these as "anchored list indentations".

From our point of view, the type of lists supported by Python-Markdown is anchored
either at the start of the line or after a block quote character (and its optional
space character).  Typically, the base list is anchored to column 1 (no block quote)
or a column that is an odd number above 1 (block quote with space character). Once
that anchor is established with the base list, any sublists may start at any column
that is a multiple of 4 (by default) added to the base list's column.  In the case
of a base list that anchors at the start of the line, its column number is 1, so
any sublists may start at columns 5 (1+4), 9 (1+8), and so on.

## Fix Description

Automatic correction is not provided because determining the correct anchor
column and the intended indent size for a multi-paragraph list item requires
understanding the author's intended list structure, which the linter cannot
infer from syntax alone. Users can correct these violations by re-indenting
sub-list items so that their column offset from the base list is a multiple of
the configured `indent` value.

## Configuration

| Prefixes |
| --- |
| `plugins.pml101.` |
| `plugins.list-anchored-indent.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `False` | Whether the Rule Plugin is enabled. |
| `indent` | `integer` | `4` | Number of spaces between the start of a base list item and the start of each sub-list item. |

## Origination of Rule

This rule was developed as an alternative to [Rule MD007](./rule_md007.md), enabling
the project to better support parsers like the
[Python-Markdown](https://python-markdown.github.io/) parser.
