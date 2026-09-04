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

Lines that are too long force readers to scroll horizontally or wrap text unpredictably, reducing readability. Enforcing a maximum line length ensures documents render consistently across different editors, terminals, and screen sizes, improving accessibility for all readers.

## Examples

### Failure Scenarios

This rule triggers when the length of any line exceeds the configured maximum character count.

```Markdown
This is a real sample line that's a grand total of 81 wonderful characters long.
```

> **Explanation**: The line above contains 81 characters, which exceeds the default maximum line length of 80 characters. This violates the rule's requirement to keep lines within the specified limit.

Unlike the previous example, this case demonstrates the rule triggering under the `strict` configuration, where even lines slightly over the limit with no break points are flagged.

```Markdown
This is a real sample line that's a grand total of 81-wonderful-characters-long.
```

> **Explanation**: Although this line is 81 characters long and has no whitespace after the 80-character limit, the `strict` mode (if enabled) does not allow lines to extend past the maximum length regardless of break points. Therefore, this line violates the strict line length constraint.

Unlike the previous examples, this case demonstrates a code block containing a line that exceeds the configured `code_block_line_length`, even though the line is syntactically valid code.

````Markdown
Some text before the code block.

```
This is a line inside a code block that is exactly eighty-five characters long here.
```

More text after the code block.
````

> **Explanation**: The line inside the fenced code block is 85 characters long, which exceeds the default `code_block_line_length` of 80. By default, MD013 checks code blocks unless `code_blocks` is set to `False`. This violates the rule's requirement to keep code block lines within the specified limit.

Unlike the previous examples, this case demonstrates a heading line that exceeds the configured `heading_line_length`.

```Markdown
# This is a heading that is way too long and exceeds eighty characters in total length here.
```

> **Explanation**: The heading line is over 80 characters long, which exceeds the default `heading_line_length` of 80. By default, MD013 checks headings unless `headings` is set to `False`. This violates the rule's requirement to keep heading lines within the specified limit.

Unlike the previous examples, this case demonstrates a table containing a line that exceeds the configured `table_line_length`.

```Markdown
| Column One | Column Two | Column Three | Column Four | Column Five |
| ---------- | ---------- | ------------ | ----------- | ----------- |
| cell data that is very long and exceeds eighty characters in the table row | short | short | short | short |
```

> **Explanation**: The second row of the table is over 80 characters long, which exceeds the default `table_line_length` of 80. By default, MD013 checks tables unless `tables` is set to `False`. This violates the rule's requirement to keep table lines within the specified limit.

### Correct Scenarios

This rule does not trigger when all lines are within the configured maximum character count.

```Markdown
This is a longish line that is 50 characters long.
```

> **Explanation**: The line above is 50 characters long, which is within the default maximum line length of 80 characters. Therefore, the rule does not trigger.

Unlike the previous example, this case has no whitespace beyond the character limit, relying on a continuous string.

```Markdown
This is a real sample line that's a grand total of 81-wonderful-characters-long.
```

> **Explanation**: Although this line is 81 characters long, there are no whitespace characters after the configured limit. By default, MD013 allows lines to continue if there's no whitespace to break at, unless strict or stern modes are enabled. This is a correct scenario under default settings.

Unlike the previous examples, this case demonstrates a code block containing a long line, but with `code_blocks` disabled so the rule does not trigger.

````Markdown
Some text before the code block.

```
This is a line inside a code block that is exactly eighty-five characters long here.
```

More text after the code block.
````

> **Explanation**: The line inside the fenced code block is 85 characters long, which exceeds the default `code_block_line_length` of 80. However, when `code_blocks` is set to `False`, the rule skips checking lines inside code blocks entirely. Therefore, this does not violate the rule.

Unlike the previous examples, this case demonstrates a long heading line, but with `headings` disabled so the rule does not trigger.

```Markdown
# This is a heading that is way too long and exceeds eighty characters in total length here.
```

> **Explanation**: The heading line is over 80 characters long, which exceeds the default `heading_line_length` of 80. However, when `headings` is set to `False`, the rule skips checking heading lines entirely. Therefore, this does not violate the rule.

Unlike the previous examples, this case demonstrates a table containing a long line, but with `tables` disabled so the rule does not trigger.

```Markdown
| Column One | Column Two | Column Three | Column Four | Column Five |
| ---------- | ---------- | ------------ | ----------- | ----------- |
| cell data that is very long and exceeds eighty characters in the table row | short | short | short | short |
```

> **Explanation**: The second row of the table is over 80 characters long, which exceeds the default `table_line_length` of 80. However, when `tables` is set to `False`, the rule skips checking table lines entirely. Therefore, this does not violate the rule.

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
| `code_blocks` | `boolean` | `True` | Whether the Rule Plugin triggers on lines in a code block. |
| `code_block_line_length` | `integer` | `80` | Maximum number of characters on a code block line. |
| `headings` | `boolean` | `True` | Whether the Rule Plugin triggers on lines in a heading. |
| `heading_line_length` | `integer` | `80` | Maximum number of characters on a heading line. |
| `tables` | `boolean` | `True` | Whether the Rule Plugin triggers on lines in a table. |
| `table_line_length` | `integer` | `80` | Maximum number of characters on a table line. |
| `stern` | `boolean` | `False` | Whether the 'stern' trigger rules are in effect. |
| `strict` | `boolean` | `False` | Whether the 'strict' trigger rules are in effect. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD013](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md013---line-length).
