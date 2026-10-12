# Rule - MD056

| Property | Value |
| --- | --- |
| Aliases | `md056`, `table-column-count` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Table rows must contain the same number of cells as the table's header row.

## Reasoning

**Tables Extension**: As tables are only recognized when the
[Markdown Tables](../extensions/markdown-tables.md) extension is enabled, this
rule has no effect unless that extension is turned on.

### Correctness

A [GFM table](https://github.github.com/gfm/#tables-extension-) is defined by
its header row, and every other row in the table is expected to have the same
number of cells as that header row. When a row has fewer cells than the header
row, the renderer pads the row with empty cells, so any data the author intended
to provide for those columns is lost. When a row has more cells than the header
row, the renderer silently drops the extra cells, so data the author provided
in those cells is lost. In both cases
the mismatch is almost always an accidental missing or extra pipe (`|`)
character, making it worth flagging.

## Examples

### Failure Scenarios

This rule triggers when a table row does not have the same number of cells as
the table's header row. In the example below, the data row has only one cell
while the header row has two.

```Markdown
| Heading | Heading |
| ------- | ------- |
| Cell |
```

> **Explanation**: The header row defines two columns, but the data row
> supplies only one cell. Renderers will pad the missing cell with an empty
> value, so any data the author intended to place in the second column is
> silently lost. This violates the rule's requirement that every row match
> the header row's column count.

Unlike the previous example, which was missing a cell, this case has *too many*
cells in the data row relative to the header.

```Markdown
| Heading | Heading |
| ------- | ------- |
| Cell | Cell | Cell |
```

> **Explanation**: The header row declares two columns, but the data row
> supplies three cells. Renderers silently drop the third cell, so the
> author's extra data is lost. This violates the rule's requirement that
> every row match the header row's column count.

### Correct Scenarios

This rule does not trigger when every row in the table has the same number of
cells as the header row.

```Markdown
| Heading | Heading |
| ------- | ------- |
| Cell | Cell |
```

> **Explanation**: The header row defines two columns, and the data row also
> contains exactly two cells. Because the column counts match, no data is
> padded in or dropped out, so the rule is satisfied.

Unlike the previous two-column example, this table has three columns and two
data rows, each of which matches the header row's three-cell count.

```Markdown
| Heading A | Heading B | Heading C |
| --------- | --------- | --------- |
| Cell 1    | Cell 2    | Cell 3    |
| Cell 4    | Cell 5    | Cell 6    |
```

> **Explanation**: The header row declares three columns, and **both** data rows
> supply exactly three cells each. Because every row's column count matches the
> header row's, no cell is padded in or dropped out, so the rule is satisfied
> for every row in the table.

## Fix Description

This rule cannot be auto-fixed because the correct fix depends on the
author's intent: a short row may need an unknown cell inserted, while a
long row may need an unknown cell removed. The tool therefore reports the
mismatch and leaves the table unchanged so the author can resolve it.

## Configuration

| Prefixes |
| --- |
| `plugins.md056.` |
| `plugins.table-column-count.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD056](https://github.com/DavidAnson/markdownlint/blob/main/doc/md056.md).
