# Markdown Tables

| Item | Description |
| --- | --- |
| Extension Id | `markdown-tables` |
| GFM Extension Status | Official |
| Configuration Item | `extensions.markdown-tables.enabled` |
| Default Value | `False` |

## Configuration

| Prefixes |
| --- |
| `extensions.markdown-tables.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the extension is enabled. |

## Summary

This extension follows the GitHub Flavored Markdown
[rules](https://github.github.com/gfm/#tables-extension-)
to provide for simple tables in Markdown documents.

## Examples

With this extension enabled, the following Markdown text:

```Markdown
| foo | bar |
| --- | --- |
| baz | bim |
```

produces the following html:

```HTML
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
```

which renders as:

<!-- pyml disable-next-line no-inline-html-->
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>

## Specifics

This extension is one of the more complicated extensions, adding a new type of
leaf element to the Markdown document.

While described fully in the [Github Markdown Specification]((https://github.github.com/gfm/#tables-extension-)),
the basic rules for tables are:

1. Columns in the table are separated by the `|` character.
1. Each line of the table optionally starts with the `|` character and ends with
   the `|` character.

Adding a bit more depth, the first line of a table is the header title line which
must be present. The content of each column is the title associated with that column
in the table. If no title is desired for a column, leave it blank.

The second line of a table is the header separator line which must have the same
number of columns as the header title line. The contents of each column must
be a string of one or more `-` characters, optionally prefixed or suffixed with
a single `:` character.  Note that if the header separator line is not present
or the number of columns is different than the header title line, the table is
not recognized.

The `:` character in the header separator line is used to denote text justification
within the column.

- Only a leading `:` character (as in `:--`) denotes the default which is left
  justification.
- Only a trailing `:` character (as in `--:`) denotes right
  justification.
- Both a leading `:` character and a trailing `:` character (as in `:--:`)
  denotes center justification.

Each line that follows until another leaf element occurs is considered part of the
table, with its content being broken down into columns.  The content for each
column becomes a text element, with standard rules to parse that text
element for inline elements applying. If the count of columns
is less than the count in the header title line, empty columns are added at the
end.  If the count of columns is greater than the count in the header title line,
the extra columns are ignored.
