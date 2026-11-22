# Rule - MD058

| Property | Value |
| --- | --- |
| Aliases | `md058`, `blanks-around-tables` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

Tables should be surrounded by blank lines.

## Reasoning

**Tables Extension**: As tables are only recognized when the
[Markdown Tables](../extensions/markdown-tables.md) extension is enabled, this
rule has no effect unless that extension is turned on.

### Correctness

For a [GFM table](https://github.github.com/gfm/#tables-extension-) to be
recognized, it generally needs to be separated from the surrounding content by
blank lines. When a blank line is missing, the text next to the table is often
absorbed into the table (or absorbs the table into a paragraph), producing
output the author did not intend. Requiring a blank line above and below each
table keeps the table distinct from its neighbors.

## Examples

### Failure Scenarios

This rule triggers when a table is not preceded by a blank line, so the line
immediately above the table is treated as part of the table's context rather
than as separate content.

```Markdown
# Heading
| abc | def |
| --- | --- |
| ghi | jkl |
```

> **Explanation**: There is no blank line between the `# Heading` line and the
> first table row. Because the heading is adjacent to the table, parsers may
> fold the heading into the table's surrounding paragraph, which violates the
> rule's requirement that each table be separated from the content above it by
> a blank line.

Unlike the previous example, which shows a missing blank line *above* the table,
this scenario shows a missing blank line *below* the table.

```Markdown
| abc | def |
| --- | --- |
| ghi | jkl |
# Heading
```

> **Explanation**: There is no blank line between the last table row and the
> `# Heading` line that follows. The heading is adjacent to the table, so
> parsers may absorb the heading into the table's paragraph, violating the
> rule's requirement that each table be separated from the content below it by
> a blank line.

### Correct Scenarios

This rule does not trigger when the table has a blank line both above and below
it, so the table is clearly separated from its neighbors.

```Markdown
# Heading

| abc | def |
| --- | --- |
| ghi | jkl |

More text.
```

> **Explanation**: A blank line separates the `# Heading` above from the
> first table row, and another blank line separates the last table row from
> `More text.` below. Because the table is isolated by blank lines on both
> sides, it satisfies the rule's requirement that tables be surrounded by blank
> lines.

Unlike the previous example, which shows a table in the middle of the document
with surrounding content, this case places the table at the very start of the
document, so there is no content above it to be separated by a blank line.

```Markdown
| abc | def |
| --- | --- |
| ghi | jkl |

More text.
```

> **Explanation**: Because the table is the first element of the document,
> there is no content above it that would require a separating blank line. The
> blank line below the table still satisfies the rule's requirement that the
> table be separated from the content that follows it.

Symmetric to the previous example, this case places the table at the very end
of the document, so there is no content below it to be separated by a blank line.

```Markdown
More text.

| abc | def |
| --- | --- |
| ghi | jkl |
```

> **Explanation**: Because the table is the last element of the document,
> there is no content below it that would require a separating blank line. The
> blank line above the table still satisfies the rule's requirement that the
> table be separated from the content that precedes it.

## Fix Description

The implementation for this feature is tracked [with this issue](https://github.com/jackdewinter/pymarkdown/issues/111).

## Configuration

| Prefixes |
| --- |
| `plugins.md058.` |
| `plugins.blanks-around-tables.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD058](https://github.com/DavidAnson/markdownlint/blob/main/doc/md058.md).

### Differences From MarkdownLint Rule

MarkdownLint treats a line containing only an HTML comment as a blank line when
deciding whether a table is surrounded by blank lines. This rule uses the
parsed document structure instead, so a table separated from adjacent content
only by an HTML-comment line is reported as not surrounded by blank lines.
