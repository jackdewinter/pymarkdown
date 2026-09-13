# Rule - MD060

| Property | Value |
| --- | --- |
| Aliases | `md060`, `table-column-style` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Ensure table columns adhere to a consistent formatting style.

## Reasoning

### Readability

Inconsistent table formatting increases cognitive load and creates visual clutter.
A unified style ensures predictable rendering for all readers and tools.

## Examples

There are three styles of tables that are supported: `tight`, `compact`, and `aligned`.
There is an additional style `any` that picks the closest style and compares the
table against that style. As these styles are significantly different from each
other, they are presented in the following scenario sections in that order to provide
a guide.

**Note:** This rule makes every effort to account for each character in each row/column
text element.
This includes the characters required to specify Markdown elements, emojis, and
JKC characters.

### Failure Scenarios

This rule triggers when the table columns do not match the configured `style`. The
following examples assume `style` is set to `tight`.

```Markdown
|Character|Meaning|French|Spanish|
|---|:--|--:|:-:|
|  Y        |  Yes    |  Oui   |  Si     |
|  N        |  No     |  Non   |  No     |
```

> **Explanation**: For any column in the table, leading or trailing whitespace violates
> the `tight` style. In this example, the title columns and data cells contain extra
> whitespace around the text (e.g., the `Y` cell), which triggers the rule.

Unlike the previous example which focused on cell whitespace, this rule also triggers
when the separator columns do not have exactly three characters (including alignment
colons).

```Markdown
|Character|Meaning|French|Spanish|
|----|:-|---:|:-|
|Y|Yes|Oui|Si|
|N|No|Non|No|
```

> **Explanation**: The `tight` style requires separator lines to have exactly three
> characters (dashes or alignment colons). The first and third columns have four
> valid characters and the second and fourth columns have two valid characters,
> violating the length constraint.

Unlike the previous tight style examples, this case enables the `aligned_delimiter`
configuration. Although the header row (line 1) still violates the `tight` style
and therefore triggers the rule, the separator row (line 2) does *not* contribute
an additional failure: its extra padding is permitted because it aligns the separator
pipes with the header pipes.

```Markdown
| Character | Meaning | French | Spanish |
| --------- | :------ | -----: | :-----: |
|Y|Yes|Oui|Si|
|N|No|Non|No|
```

> **Explanation**: Line 1 (the header) contains leading and trailing whitespace
> in each cell (e.g., ` Character `), which violates the `tight` style and triggers
> the rule. Line 2 (the separator) has more than three characters per column, which
> would normally violate `tight` as well. However, because `aligned_delimiter` is
> enabled, the separator row is exempt from the `tight` length constraint as long
> as its pipes align with the header row's pipes. In this example they do (e.g.,
> `| --------- |` aligns with `| Character |`), so line 2 does not produce a separate
> failure. The overall rule trigger comes solely from line 1.

Unlike the previous tight style examples, this scenario uses the `compact` style,
which requires exactly one leading and one trailing space per cell. Here, the
data rows have varying whitespace, violating that constraint.

```Markdown
|Character|Meaning|French|Spanish|
| --- | :-- | --: | :-: |
| Y   | Yes | Oui | Si  |
| N   | No  | Non | No  |
```

> **Explanation**: The `compact` style requires exactly one leading and one trailing
> space per cell. The data rows have varying whitespace (e.g., the `Y` cell has
> multiple trailing spaces), violating the compact spacing rule.

Unlike the previous compact style example, this case uses the `aligned` style, which
requires all columns to have consistent width. The second column in the header differs
in width from its separator, violating this constraint.

```Markdown
|Character| Meaning |French|Spanish|
| ---     | :--    | --:   | :-:   |
| Y       | Yes    | Oui   | Si    |
| N       | No     | Non   | No    |
```

> **Explanation**: Under the `aligned` style, every cell in a given column must
> have the same total width (from the leading `|` to the trailing `|`). In the second
> column of this example, the header cell is 9 characters wide (` Meaning `), the
> data cells are 9 characters wide (` Yes `, ` No `), but the separator cell is
> only 3 characters wide (`:--`). This width mismatch across rows in the same column
> violates the `aligned` style.

Unlike the previous aligned example, this case mixes pipe presence: the header omits
the leading `|` while rows 2–4 omit the trailing `|`, so no two rows share the same
pipe layout.

```Markdown
Character | Meaning |French |Spanish|
| ---     | :--     | --:   | :-:
| Y       | Yes     | Oui   | Si
| N       | No      | Non   | No
```

> **Explanation**: Under the `aligned` style, the set of pipe delimiters present
> per row (leading and/or trailing) must be identical across all rows so that columns
> align vertically. In this example, row 1 has only a trailing pipe, while rows
> 2–4 have only a leading pipe. Because no consistent pipe layout exists, the columns
> cannot align, violating the `aligned` style.

Unlike the previous scenarios which tested specific styles, this case uses the `any`
style. The rule evaluates the table against all three styles and picks the closest
one, reporting on failures against the "best" choice.

```Markdown
Character | Meaning |French |Spanish|
| ---     | :--     | --:   | :-:   |
| Y       | Yes     | Oui   | Si    |
|N|No|Non| No
```

> **Explanation**: The `any` style fails if the table doesn't fit *any* defined
> style consistently. However, this table most closely matches the `aligned` style,
> with only the last row not adhering to that style. As this is the closest style,
> only the rule failures for the last line will be reported.

### Correct Scenarios

This rule does not trigger when the table adheres strictly to the configured `tight`
style, with no extra whitespace and correct separator lengths.

```Markdown
|Character|Meaning|French|Spanish|
|---|:--|--:|:-:|
|Y|Yes|Oui|Si|
|N|No|Non|No|
```

> **Explanation**: All columns have no leading or trailing whitespace within the
> cells. The separator row uses exactly three dashes (with alignment colons) for
> each column. This satisfies the `tight` style criteria.

Unlike the previous example, this case demonstrates the `tight` style with `aligned_delimiter`
enabled, where the separator pipes align with the header pipes.

```Markdown
|Character|Meaning|French|Spanish|
| ------- | :---- | ---: | :---: |
|Y|Yes|Oui|Si|
|N|No|Non|No|
```

> **Explanation**: With `aligned_delimiter` enabled for `tight` style, the pipe
> characters in the separator row must align with the pipes in the header row. In
> this example, the separator row expands to align correctly (e.g.,
> `| ------- |` under `|Character|`). The `tight` style forbids internal whitespace
> in cells. The header and data cells contain no leading or trailing whitespace
> (e.g., `Character`, `Y`). This satisfies both the `tight` style criteria and the
> `aligned_delimiter` requirement.

Unlike the previous examples, this case uses the `compact` style, requiring exactly
one leading and one trailing space per cell.

```Markdown
| Character | Meaning | French | Spanish |
| --- | :-- | --: | :-: |
| Y | Yes | Oui | Si |
| N | No | Non | No |
```

> **Explanation**: Each cell in the data rows has exactly one space before and one
> space after the text (e.g., ` Y `, ` Yes `). The separator row uses standard alignment
> markers. This satisfies the `compact` style criteria.

Unlike the previous compact example, this case enables `aligned_delimiter`, aligning
the separator pipes with the header pipes while maintaining compact data cells.

```Markdown
| Character | Meaning | French | Spanish |
| --------- |:------- | -----: | :-----: |
| Y | Yes | Oui | Si |
| N | No | Non | No |
```

> **Explanation**: The separator row is expanded to align pipes with the header,
> satisfying `aligned_delimiter`. The data cells retain single-space padding, satisfying
> `compact` style.

Unlike the previous compact style example with aligned delimiters, this case uses
the `aligned` style, which requires all columns to maintain consistent width across
all rows, rather than just single-space padding.

```Markdown
| Character | Meaning | French | Spanish |
| ---       | :------ | -----: | :-:     |
| Y         | Yes     | Oui    | Si      |
| N         | No      | Non    | No      |
```

> **Explanation**: All columns maintain consistent widths across header, separator,
> and data rows. The pipes align vertically, and the spacing within each column
> is uniform, satisfying the `aligned` style criteria.

Unlike the previous aligned example, this scenario demonstrates the `any` style
passing by relying on its closest-style selection. The table below is intentionally
*not* valid `tight` (cells have surrounding spaces) and *not* valid `aligned` (column
widths vary across rows), but it is valid `compact` — so only `compact` reports
zero failures.

```Markdown
| Character | Meaning | French | Spanish |
| ---       | :--     | --:    | :-:     |
| Y         | Yes     | Oui    | Si      |
| N         | No      | Non    | No      |
```

> **Explanation**: This table does not conform to the `tight` style (cells have
> surrounding whitespace) and does not conform to the `aligned` style (column widths
> vary across rows), but it does conform to the `compact` style. Under `any`, the
> rule evaluates all three styles, selects compact as the closest match, and reports
> zero failures — so the rule does not trigger. This demonstrates that `any` genuinely
> picks the closest style rather than trivially passing via `tight`.

## Fix Description

Automated fixing is not available because determining the "correct" table style
requires subjective judgment about readability and consistency preferences. Additionally,
preserving the author's intent in complex tables with mixed styles or ambiguous
alignment is difficult for an algorithm. Manual correction is recommended to ensure
the desired visual structure is maintained.

## Configuration

| Prefixes |
| --- |
| `plugins.md060.` |
| `plugins.table-column-style.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `bool` | `True` | Whether the Rule Plugin is enabled. |
| `style` | `str` | `"any"` | Expected formatting style for tables. One of `any`, `tight`, `compact`, `aligned`. |
| `aligned_delimiter` | `bool` | `False` | If the style is `tight` or `compact`, force the delimiter row to be aligned with the title row. |

### Valid Styles

#### Style: Tight

The `tight` style presents the table as separators that do not have any leading
or trailing whitespace in any of the columns. In addition, the separator line
is composed of three `-` characters, with leading or trailing `:` characters to
specify alignment of the text within each row/column. This is largely due to some
older Markdown parsers that require three separator characters.

#### Style: Compact

The `compact` style is almost the same as the `tight` style, except that it mandates
a single space leading character and a single space trailing character for each column.

#### Style: Aligned

The `aligned` style departs from the previous two styles that focus on the leading
and trailing whitespace around each row/column text, and focuses on the separator
characters themselves. Specifically, this style requires that all rows within a
given column maintain the same total character width, from the start `|` to the
end `|` of the cell. For example, if the first row of a column contains eight characters
between the pipes, every subsequent row in that column must also contain exactly
eight characters. If inline sequences such as `&amp;`, `\$`, and `[Link](#link)`
are used as column text, they will count as 5, 2, and 13 characters respectively.

#### Style: Any

If the `any` style is specified, then all three of the above styles are applied.
The rule then chooses the style that reported the *least* number of Rule Failures,
and reports those Rule Failures for the table.

The evaluation resets for each table.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD060](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md060---table-column-style).
