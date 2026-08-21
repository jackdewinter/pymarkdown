# Rule - MD060

| Property | Value |
| --- | --- |
| Aliases | `md060`, `table-column-style` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Table column style.

## Reasoning

### Readability

One of the main keys to readability is to have consistent formatting applied
throughout a group of documents.  Extending the concept even further,
organizations often have specific rules on how documents should be authored throughout
that organization.  It follows that both concepts may extend to specifying
how tables are formatted for a given set of Markdown documents.

## Styles

There are three styles of tables that are supported: `tight`, `compact`, and `aligned`.
There
is an additional style `any` that picks the closest style and compares the table
against that style.

Note this rule makes every effort to account for each character in each row/column
text element.
This includes the characters required to specify Markdown elements, emojis, and
JKC characters.

### Style: Tight

The `tight` style presents the table as separators that do not have any leading
or trailing whitespace in any of the columns. In addition, the separator line
is composed of three `-` characters, with leading or trailing `:` characters to
specify alignment of the text within each row/column. This is largely due to some
older Markdown parsers that require three separator characters.

#### Correct Scenarios

The following is a correct example for the `tight` style.

````Markdown
|Character|Meaning|French|Spanish|
|---|:--|--:|:-:|
|Y|Yes|Oui|Si|
|N|No|Non|No|
````

### Failure Scenarios

For any of the columns in the table, any leading or trailing whitespace for a column
triggers
this rule. The following table has whitespace around the text in the title columns,
which
triggers this rule. Having leading or trailing whitespace for any of the other column
text
also triggers this rule.

````Markdown
| Character | Meaning | French | Spanish |
|---|:--|--:|:-:|
|  Y        |  Yes    |  Oui   |  Si     |
|  N        |  No     |  Non   |  No     |
````

In addition, if the number of characters in the separator columns are not equal
to 3, then this rule also triggers.

````Markdown
|Character|Meaning|French|Spanish|
|----|:-|---:|:-|
|Y|Yes|Oui|Si|
|N|No|Non|No|
````

### Style: Compact

The `compact` style is almost the same as the `compact` style, except that it mandates
a single space leading character and a single space trailing character for each column.

<!-- pyml disable-next-line no-duplicate-heading-->
#### Correct Scenarios

The following is a correct example for the `compact` style.

````Markdown
| Character | Meaning | French | Spanish |
| --- | :-- | --: | :-: |
| Y | Yes | Oui | Si |
| N | No | Non | No |
````

If the `aligned_delimiter` is `True`, then the delimiter row's separator characters
must match the separator characters of the title row. This configuration value can
be set to
make `compact` styled tables stand out because of their title and separator rows.

````Markdown
| Character | Meaning | French | Spanish |
| --------- |:------- | -----: | :-----: |
| Y | Yes | Oui | Si |
| N | No | Non | No |
````

<!-- pyml disable-next-line no-duplicate-heading-->
### Failure Scenarios

For any of the columns in the table, having zero or greater than one space
character at
the start of any column or at the end of any column will trigger this rule.

````Markdown
|Character|Meaning|French|Spanish|
| --- | :-- | --: | :-: |
| Y   | Yes | Oui | Si  |
| N   | No  | Non | No  |
````

### Style: Aligned

The `aligned` style departs from the previous two styles that focus on the leading
and trailing whitespace around each row/column text, and focuses on the separator
characters themsevles. Specifically, if there are eight characters between the
start `|` of a column and the end `|` of a column, then each of the rows of that
column must have eight characters.  If inline sequences such as `&amp;`, `\$`,
and `[Link](#link)` are used as column text, they will count as 5, 2, and 13 characters
respectively.

<!-- pyml disable-next-line no-duplicate-heading-->
#### Correct Scenarios

The following is a correct example for the `compact` style.

````Markdown
| Character | Meaning | French | Spanish |
| ---       | :------ | -----: | :-:     |
| Y         | Yes     | Oui    | Si      |
| N         | No      | Non    | No      |
````

<!-- pyml disable-next-line no-duplicate-heading-->
### Failure Scenarios

If the separators do not line up visually, then the rule triggers.

````Markdown
|Character| Meaning |French|Spanish|
| ---     | :--    | --:   | :-:   |
| Y       | Yes    | Oui   | Si    |
| N       | No     | Non   | No    |
````

Because of this, if the title row does not include a leading or trailing `|` character,
than each of the subsequent rows much also include the same leading and trailing
`|` characters or this rule will trigger.

````Markdown
Character | Meaning |French |Spanish|
| ---     | :--     | --:   | :-:
| Y       | Yes     | Oui   | Si
| N       | No      | Non   | No
````

### Style: Any

The `any` style is an outlier in that it adapts to all three of the above styles.
If the `any` style is specified, then all three of the above style are applied.
The rule then chooses the style that reported the *least* number of Rule Failures,
and reports those Rule Failures for the table.

This style resets for each table.

## Fix Description

Ths fix for this rule is under examination.

## Configuration

| Prefixes |
| --- |
| `plugins.md060.` |
| `plugins.table-column-style.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `style` | `str` | `"any"` | Style to check for against the table's format. One of `any`, `tight`, `compact`, `aligned`. |
| `aligned_delimiter` | `bool` | `False` | If the style is `tight` or `compact`, force the delimeter row to be aligned with the title row. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD060](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md060---table-column-style).
