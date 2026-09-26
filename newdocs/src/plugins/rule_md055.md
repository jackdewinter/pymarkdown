# Rule - MD055

| Property | Value |
| --- | --- |
| Aliases | `md055`, `table-pipe-style` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

Table rows must use a consistent leading and trailing pipe style.

## Reasoning

**Tables Extension**: As tables are only recognized when the
[Markdown Tables](../extensions/markdown-tables.md) extension is enabled, this
rule has no effect unless that extension is turned on.

### Consistency

The [GFM table](https://github.github.com/gfm/#tables-extension-) syntax allows
the leading and trailing pipe (`|`) characters on each row to be present or
omitted independently. While every combination renders the same, mixing styles
within a document is harder to read and to maintain. This rule enforces a
single, consistent leading/trailing pipe style across every row of every table,
including the header row and the delimiter row.

### Readability

For human readers scanning long documents with many tables, uniform pipe
style reduces visual noise at the row edges and makes it easier to track the
start and end of each cell, particularly in wide tables or in side-by-side
diff views.

## Examples

### Failure Scenarios

This rule triggers when a row's leading/trailing pipe style deviates from
the style established by the first row of the table.

```Markdown
| abc | def |
| --- | --- |
| ghi | jkl
```

> **Explanation**: Under the `consistent` style, the header row (`| abc | def |`)
> establishes a leading-and-trailing pipe pattern. The body row `| ghi | jkl`
> omits the trailing pipe, deviating from that established pattern, so the rule
> fires on that row.

Unlike the previous scenario, which shows a body row deviating from the
header's style, this scenario shows a delimiter row deviating from the
style established by the header and body rows.

```Markdown
| abc | def |
--- | ---
| ghi | jkl |
```

> **Explanation**: The header row and the body row both use a
> leading-and-trailing pipe style, but the delimiter row (`--- | ---`)
> omits the leading and trailing pipes. Because the Summary of the rule
> explicitly requires the delimiter row to follow the same style as the
> rest of the table, this row is a violation even though the data rows
> themselves are internally consistent.

### Correct Scenarios

This rule does not trigger when every row uses the same leading and trailing
pipe style.

```Markdown
| abc | def |
| --- | --- |
| ghi | jkl |
```

> **Explanation**: All three rows (header, delimiter, and body) use the same
> leading-and-trailing pipe style, so the `consistent` requirement is satisfied
> and the rule does not trigger.

Unlike the preceding examples that include leading pipes, this scenario shows a
table where no row contains either a leading or a trailing pipe.

```Markdown
abc | def
--- | ---
ghi | jkl
```

> **Explanation**: The first row of the table does not include leading or trailing
> pipes. As long as all subsequent rows match this style, the rule is satisfied
> because the entire table is consistent with the style established by the first
> row.

Unlike the preceding example that omits both pipes, this table includes a leading
pipe on every row while omitting the trailing pipe.

```Markdown
| abc | def
| --- | ---
| ghi | jkl
```

> **Explanation**: All rows in this table consistently use a leading pipe and
> omit the trailing pipe. Under the default `consistent` style, the first row
> establishes the expected pattern (leading pipe present, trailing pipe absent),
> and every subsequent row matches that pattern, so the rule does not trigger.

## Fix Description

The implementation for this feature is tracked [with this issue](https://github.com/jackdewinter/pymarkdown/issues/111).

## Configuration

| Prefixes |
| --- |
| `plugins.md055.` |
| `plugins.table-pipe-style.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `style` | `string` | `consistent` | Required leading/trailing pipe style. |

The allowable values for the `style` value are:

| Value Name | Description |
| --- | --- |
| `consistent` | The first table row sets the expected style for the rest of the document. |
| `leading_and_trailing` | Each row must have both a leading and a trailing pipe. |
| `leading_only` | Each row must have a leading pipe but no trailing pipe. |
| `trailing_only` | Each row must have a trailing pipe but no leading pipe. |
| `no_leading_or_trailing` | Each row must have neither a leading nor a trailing pipe. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD055](https://github.com/DavidAnson/markdownlint/blob/main/doc/md055.md).

### Differences From MarkdownLint Rule

PyMarkdown's MD055 applies the consistency check across **all** tables in the
document (the first table row sets the style), whereas MarkdownLint's MD055
defaults to requiring leading and trailing pipes on every row and offers a
`style` option with a different set of values.
