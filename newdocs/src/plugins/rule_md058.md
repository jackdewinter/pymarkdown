# Rule - MD058

| Property | Value |
| --- | -- |
| Aliases | `md058`, `blanks-around-tables` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Tables should be surrounded by blank lines.

## Reasoning

### Correctness

For a [GFM table](https://github.github.com/gfm/#tables-extension-) to be
recognized, it generally needs to be separated from the surrounding content by
blank lines.  When a blank line is missing, the text next to the table is often
absorbed into the table (or absorbs the table into a paragraph), producing
output the author did not intend.  Requiring a blank line above and below each
table keeps the table distinct from its neighbors.

## Examples

### Failure Scenarios

This rule triggers when a table is not preceded by a blank line:

```Markdown
# Heading
| abc | def |
| --- | --- |
| ghi | jkl |
```

or not followed by a blank line:

```Markdown
| abc | def |
| --- | --- |
| ghi | jkl |
# Heading
```

### Correct Scenarios

This rule does not trigger when the table has a blank line both above and below
it:

```Markdown
# Heading

| abc | def |
| --- | --- |
| ghi | jkl |

More text.
```

A table at the very start or very end of the document does not require a blank
line on the missing side.

## Configuration

| Prefixes |
| --- |
| `plugins.md058.` |
| `plugins.blanks-around-tables.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

As tables are only recognized when the
[Markdown Tables](../extensions/markdown-tables.md) extension is enabled, this
rule has no effect unless that extension is turned on.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD058](https://github.com/DavidAnson/markdownlint/blob/main/doc/md058.md).

### Differences From MarkdownLint Rule

MarkdownLint treats a line containing only an HTML comment as a blank line when
deciding whether a table is surrounded by blank lines.  This rule uses the
parsed document structure instead, so a table separated from adjacent content
only by an HTML-comment line is reported as not surrounded by blank lines.
