# Rule - MD055

| Property | Value |
| --- | -- |
| Aliases | `md055`, `table-pipe-style` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Table pipe style.

## Reasoning

### Consistency

The [GFM table](https://github.github.com/gfm/#tables-extension-) syntax allows
the leading and trailing pipe (`|`) characters on each row to be present or
omitted independently.  While every combination renders the same, mixing styles
within a document is harder to read and to maintain.  This rule enforces a
single, consistent leading/trailing pipe style across every row of every table,
including the header row and the delimiter row.

## Examples

### Failure Scenarios

This rule triggers when a row's use of leading and trailing pipe characters does
not match the expected style.  With the default `consistent` style, the first
row of the first table sets the expected style, and any row that deviates is
reported.  Here the body row is missing its trailing pipe:

```Markdown
| abc | def |
| --- | --- |
| ghi | jkl
```

### Correct Scenarios

This rule does not trigger when every row uses the same leading and trailing
pipe style:

```Markdown
| abc | def |
| --- | --- |
| ghi | jkl |
```

## Configuration

| Prefixes |
| --- |
| `plugins.md055.` |
| `plugins.table-pipe-style.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `style` | `string` | `consistent` | Required leading/trailing pipe style. |

The allowable values for the `style` value are:

| Value | Description |
| -- | -- |
| `consistent` | The first table row sets the expected style for the rest of the document. |
| `leading_and_trailing` | Each row must have both a leading and a trailing pipe. |
| `leading_only` | Each row must have a leading pipe but no trailing pipe. |
| `trailing_only` | Each row must have a trailing pipe but no leading pipe. |
| `no_leading_or_trailing` | Each row must have neither a leading nor a trailing pipe. |

As tables are only recognized when the
[Markdown Tables](../extensions/markdown-tables.md) extension is enabled, this
rule has no effect unless that extension is turned on.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD055](https://github.com/DavidAnson/markdownlint/blob/main/doc/md055.md).
