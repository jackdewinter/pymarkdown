# Rule - PML102

| Property | Value |
| --- | --- |
| Aliases | `pml102`, `disallow-lazy-list-indentation` |
| Autofix Available | Pending |
| Enabled By Default | No |

## Summary

Disallow "lazy" paragraph continuations within lists.

## Reasoning

> **Advisory**: Enable this rule if you want to generate Rule Failures when the
> Markdown documents use lazy continuation lines. That is, multiple line paragraphs
> where the indentation for each paragraph line does not match the indentation for
> the list that contains it.

### Readability

Lazy continuation lines, while valid per the GFM spec, make the visual indentation
of a document misleading — readers cannot tell at a glance whether a line belongs
to the list item above it or is a standalone paragraph. This rule gives authors
control over that ambiguity.

### History

The example of a trivial list with two lines is as follows:

```Markdown
1. A paragraph
   with two lines.
```

From our point of view, when we look at those two lines, everything lines up and
most readers would agree that the second line is part of the list item started on
the first line.

The next example mutates that example by removing leading spaces on the second line:

```Markdown
1. A paragraph
 with two lines.
```

In this example, the second line starts at the left margin instead of being aligned
with the text in the list item. According to the GitHub Flavored Markdown (GFM)
specification, that second line is still part of the same paragraph because it does
not start another eligible Markdown element. The specification calls this kind of
misaligned paragraph line a [lazy continuation line](https://github.github.com/gfm/#lazy-continuation-line).

One of our users filed [issue 979](https://github.com/jackdewinter/pymarkdown/issues/979)
describing this concern. We agreed with their request and implemented it as Rule
Plugin PML102. While we allow lazy continuation lines to remain compliant with the
specification, we believe it can reduce the readability of many Markdown documents.
This rule gives PyMarkdown users control over whether lazy continuation lines are
permitted in their documents.

## Examples

### Failure Scenarios

This rule triggers when a paragraph inside a list uses a lazy continuation line
that is indented less than the list item's content column.

```Markdown
1. A paragraph
  with two lines.
```

> **Explanation**: This example fails because the continuation line is indented
> by two spaces, while the list item's content column begins at column 4
> (after `1.` and a single space). The continuation line is therefore a lazy continuation
> line, which this rule disallows.

Unlike the previous example, which was short by one space of indentation, this
case omits all leading whitespace on the continuation line.

```Markdown
1. A paragraph
with two lines.
```

> **Explanation**: This example fails because the continuation line begins at
> column 0, far to the left of the list item's content column. Per the GFM
> specification this is still part of the same paragraph, but the misalignment
> is exactly the condition this rule flags.

Unlike the previous two single-item examples, this case uses a second list item
with a *different* marker width, so the active item's content column on the lazy
continuation line is wider than the indentation used.

```Markdown
1. A paragraph
   with two lines.
10. Another paragraph
   that has two lines.
```

> **Explanation**: The second list item uses a two-digit marker (`10.`), which shifts
> the content column for its item to column 6. The continuation line
> `that has two lines.` is indented by only three spaces — aligned with the single-digit
> item's content column but **not** with the double-digit item's content column
> — so the rule flags it as a lazy continuation line.

Unlike the previous examples, which all used ordered list markers (`1.`, `10.`),
this case uses a bulleted list marker (`-`) to show the rule applies to unordered
lists as well. The continuation line is again short of the content column by one
space.

```Markdown
- A paragraph
 with two lines.
```

> **Explanation**: This example fails for the same reason as the earlier single-item
> example: the bullet marker `-` is one character wide, so the content column begins
> at column 2. The continuation line `with two lines.` is indented by only one space,
> placing it to the left of the content column and making it a lazy continuation
> line.

Unlike the previous examples, which each involved a single flat list item, this
case nests one list item inside another. The inner item's continuation line is short
of the inner item's content column by one space.

```Markdown
- A paragraph
  - An inner paragraph
   with two lines.
```

> **Explanation**: This example fails because the inner item's content column begins
> after its own marker (the `-` at column 2), at column 4. The continuation line
> `with two lines.` is indented by only three spaces, placing it to the left of
> that content column and making it a lazy continuation line of the inner list item.

### Correct Scenarios

This rule does not trigger when every paragraph continuation line inside a list
is indented to align with the list item's content column.

```Markdown
1. A paragraph
   with two lines.
```

> **Explanation**: This example passes because the continuation line is indented
> by three spaces, exactly matching the content column of the list item (`1.`) and
> the single space that follows it. No lazy continuation line is present, so the
> rule does not fire.

Unlike the previous example, which used an ordered list marker (`1.`), this case
uses a bulleted list marker (`-`) to show the rule does not fire for unordered lists
either. The continuation line is indented exactly to the bullet's content column.

```Markdown
- A paragraph
  with two lines.
```

> **Explanation**: This example passes because the bullet marker `-` is one character
> wide, so the content column begins at column 2. The continuation line
> `with two lines.` is indented by two spaces, exactly matching that content column.
> No lazy continuation line is present, so the rule does not fire.

Unlike the previous examples, which each involved a single flat list item, this
case nests one list item inside another, and both continuation lines are correctly
aligned with their own respective items' content columns.

```Markdown
- A paragraph
  - An inner paragraph
    with two lines.
```

> **Explanation**: This example passes because each continuation line is aligned
> with the content column of the item it belongs to. The inner item's marker `-`
> sits at column 2, so its content column begins at column 4; the continuation line
> `with two lines.` is indented by four spaces, exactly matching that column. No
> lazy continuation line is present, so the rule does not fire.

### Note

This rule currently targets [List Item lazy continuation lines](https://github.github.com/gfm/#example-269)
and not [Block Quote lazy continuation lines](https://github.github.com/gfm/#example-210).
If you would like to see Block Quote lazy continuation lines supported by this rule,
please [open an issue](https://github.com/jackdewinter/pymarkdown/issues).

## Fix Description

The implementation for this feature is tracked [with this issue](https://github.com/jackdewinter/pymarkdown/issues/1618).

## Configuration

| Prefixes |
| --- |
| `plugins.pml102.` |
| `plugins.disallow-lazy-list-indentation.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `False` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule was developed in response to user [issue 979](https://github.com/jackdewinter/pymarkdown/issues/979).
