# Rule - MD013

| Property | Value |
| --- | --- |
| Aliases | `md013`, `line-length` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

This rule enforces a maximum line length to improve document readability.

## Reasoning

### Readability

Lines that are too long force readers to scroll horizontally or see text wrap unpredictably.
A maximum line length keeps documents rendering consistently across editors, terminals,
and screen sizes, which aids readability and accessibility.

## Examples

### Failure Scenarios

This rule triggers when the length of any line exceeds the configured maximum character
count.

```Markdown
This is a real sample line that's a grand total of 88 wonderful characters long ya'know.
```

> **Explanation**: The line above contains 88 characters, which exceeds the default
> maximum line length of 80 characters. This violates the rule's requirement to
> keep lines within the specified limit.

Unlike the previous example, this case demonstrates the rule triggering under the
`strict` configuration, where the no-break-point exception is overridden.

```Markdown
This is a real sample line that is a grand total of 81-wonderful-characters-long.
```

> **Explanation**: By default, this rule does not flag a line when the only character
> beyond the 80-character limit is part of a continuous token with no whitespace
> to break at. However, when `strict` is set to `True`, that exception is removed:
> the line is flagged purely on exceeding the configured `line_length`, regardless
> of break-point availability.

Unlike the previous example, which demonstrates `strict` mode (a line is flagged
even when no whitespace break point exists), this case demonstrates `stern` mode:
a line is flagged when it exceeds the configured `line_length` **and** it contains
at least one whitespace break point.

```Markdown
This is a real sample line that is a grand total of 81 wonderful characters long.
```

> **Explanation**: The line above is 81 characters long and contains whitespace
> characters (i.e., break points). Under default settings this rule would not trigger
> because there is no whitespace break point after the configured limit. When `stern`
> is set to `True`, the rule triggers on any over-limit line
> **that has a break point**, which this line does. This violates the rule's requirement
> under `stern` mode.

Unlike the previous examples, this case demonstrates a code block containing a line
that exceeds the configured `code_block_line_length`, even though the line is syntactically
valid code.

````Markdown
Some text before the code block.

```text
This is a line inside a code block that is exactly eighty-five characters long here.
```

More text after the code block.
````

> **Explanation**: The line inside the fenced code block is 85 characters long,
> which exceeds the default `code_block_line_length` of 80. By default, this rule
> checks code blocks unless `code_blocks` is set to `False`. This violates the rule's
> requirement to keep code block lines within the specified limit.

Unlike the previous examples, this case demonstrates a heading line that exceeds
the configured `heading_line_length`.

```Markdown
# This is a heading that is way too long and exceeds eighty characters in total length here.
```

> **Explanation**: The heading line is over 80 characters long, which exceeds the
> default `heading_line_length` of 80. By default, this rule checks headings unless
> `headings` is set to `False`. This violates the rule's requirement to keep heading
> lines within the specified limit.

Unlike the previous examples, this case demonstrates a table containing a line that
exceeds the configured `table_line_length`.

```Markdown
| Column One | Column Two | Column Three | Column Four | Column Five |
| ---------- | ---------- | ------------ | ----------- | ----------- |
| cell data that is very long and exceeds eighty characters in the table row | short | short | short | short |
```

> **Explanation**: The second row of the table is over 80 characters long, which
> exceeds the default `table_line_length` of 80. By default, this rule checks tables
> unless `tables` is set to `False`. This violates the rule's requirement to keep
> table lines within the specified limit.

### Correct Scenarios

This rule does not trigger when all lines are within the configured maximum character
count.

```Markdown
This is a longish line that is 50 characters long.
```

> **Explanation**: The line above is 50 characters long, which is within the default
> maximum line length of 80 characters. Therefore, the rule does not trigger, even
> under `stern` and `strict` modes.

Unlike the previous example (which flags a no-break-point line under `strict`),
this case shows the default behavior: a line that exceeds the limit by one character
but has no whitespace break point after the 80th character does not trigger this
rule.

```Markdown
This is a real sample line that's a grand total of 81-wonderful-characters-long.
```

> **Explanation**: Although this line is 81 characters long, there are no whitespace
> characters after the configured limit. By default, this rule allows lines to continue
> if there's no whitespace to break at, unless `strict` or `stern` modes are enabled.
> This is a correct scenario under default settings.

Unlike the previous examples, this case demonstrates `stern` mode where the line
exceeds the character limit but contains no whitespace break points, so `stern`
mode does not trigger.

```Markdown
This-is-a-real-sample-line-that's-a-total-of-101-characters-long-without-any-whitespace--like-an-URL.
```

> **Explanation**: Although this line (at 101 characters) exceeds the 80-character
> limit, it contains no whitespace characters at all, meaning there are no break
> points anywhere in the line. Under `stern` mode, the rule only triggers on over-limit
> lines that contain at least one break point. Since this line has none, the rule
> does not trigger, even under `stern`.

Unlike the previous examples, this case demonstrates a code block containing a long
line, but with `code_blocks` disabled so the rule does not trigger.

````Markdown
Some text before the code block.

```text
This is a line inside a code block that is exactly eighty-five characters long here.
```

More text after the code block.
````

> **Explanation**: The line inside the fenced code block is 85 characters long,
> which exceeds the default `code_block_line_length` of 80. However, when `code_blocks`
> is set to `False`, the rule skips checking lines inside code blocks entirely.
> Therefore, this does not violate the rule.

Unlike the previous examples, this case demonstrates a long heading line, but with
`headings` disabled so the rule does not trigger.

```Markdown
# This is a heading that is way too long and exceeds eighty characters in total length here.
```

> **Explanation**: The heading line is over 80 characters long, which exceeds the
> default `heading_line_length` of 80. However, when `headings` is set to `False`,
> the rule skips checking heading lines entirely. Therefore, this does not violate
> the rule.

Unlike the previous examples, this case demonstrates a table containing a long line,
but with `tables` disabled so the rule does not trigger.

```Markdown
| Column One | Column Two | Column Three | Column Four | Column Five |
| ---------- | ---------- | ------------ | ----------- | ----------- |
| cell data that is very long and exceeds eighty characters in the table row | short | short | short | short |
```

> **Explanation**: The second row of the table is over 80 characters long, which
> exceeds the default `table_line_length` of 80. However, when `tables` is set to
> `False`, the rule skips checking table lines entirely. Therefore, this does not
> violate the rule.

## Fix Description

The implementation for this feature is tracked [with this issue](https://github.com/jackdewinter/pymarkdown/issues/811).

## Configuration

| Prefixes |
| --- |
| `plugins.md013.` |
| `plugins.line-length.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `line_length` | `integer` | `80` | Maximum number of characters on a normal line. |
| `code_blocks` | `boolean` | `True` | Whether lines inside code blocks are checked against `code_block_line_length`. |
| `code_block_line_length` | `integer` | `80` | Maximum number of characters on a code block line. |
| `headings` | `boolean` | `True` | Whether heading lines are checked against `heading_line_length`. |
| `heading_line_length` | `integer` | `80` | Maximum number of characters on a heading line. |
| `tables` | `boolean` | `True` | Whether table rows are checked against `table_line_length`. |
| `table_line_length` | `integer` | `80` | Maximum number of characters on a table line. |
| `stern` | `boolean` | `False` | Whether the `stern` trigger rules are in effect. |
| `strict` | `boolean` | `False` | Whether the `strict` trigger rules are in effect. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD013](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md013---line-length).

### Differences From MarkdownLint Rule

This implementation extends the original rule with configurable sub-limits
(`code_blocks`/`code_block_line_length`, `headings`/`heading_line_length`, and
`tables`/`table_line_length`) that are not present
in the upstream MarkdownLint rule.
