# Rule - MD056

| Aliases |
| --- |
| `md056` |
| `table-column-count` |

| Autofix Available |
| --- |
| No |

## Summary

Table column count.

## Reasoning

### Correctness

A [GFM table](https://github.github.com/gfm/#tables-extension-) is defined by
its header row, and every other row in the table is expected to have the same
number of cells as that header row.  When a row has fewer cells than the header
row, the renderer pads the row with empty cells, so data the author intended to
provide is missing.  When a row has more cells than the header row, the extra
cells are silently dropped, so data the author provided is lost.  In both cases
the mismatch is almost always an accidental missing or extra pipe (`|`)
character, making it worth flagging.

## Examples

### Failure Scenarios

This rule triggers when a table row does not have the same number of cells as
the table's header row.  This can be because the row has too few cells:

```Markdown
| Heading | Heading |
| ------- | ------- |
| Cell |
```

or because the row has too many cells:

```Markdown
| Heading | Heading |
| ------- | ------- |
| Cell | Cell | Cell |
```

### Correct Scenarios

This rule does not trigger when every row in the table has the same number of
cells as the header row:

```Markdown
| Heading | Heading |
| ------- | ------- |
| Cell | Cell |
```

Note that a table's header row and its delimiter row must already have the same
number of cells, or the block is not recognized as a table at all.  In that
case there is no table for this rule to examine.

## Configuration

| Prefixes |
| --- |
| `plugins.md056.` |
| `plugins.table-column-count.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

As tables are only recognized when the
[Markdown Tables](/docs/extensions.md) extension is enabled, this rule has no
effect unless that extension is turned on.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD056](https://github.com/DavidAnson/markdownlint/blob/main/doc/md056.md).
