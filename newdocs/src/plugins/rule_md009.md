# Rule - MD009

| Property | Value |
| --- | -- |
| Aliases | `md009`, `no-trailing-spaces` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Trailing spaces.

## Reasoning

### Simplicity

The primary reason for enabling this rule is simplicity.  Two spaces at
the end of a line within a paragraph produces a Hard Line Break element.
Other than that, there is no other reason for trailing spaces on any line.
Any other form of trailing spaces is ignored, with no effect on the final HTML document.

## Examples

As the space character is not normally visible, each occurrence of
the text `{space}` in the following example represents a single
space character.

### Failure Scenarios

This rule triggers when any line of the document ends with more than one
space, except for the number of spaces specified by the `br_spaces`
configuration value:

```Markdown
this line ends with one space character{space}
```

This rule can be triggered on any eligible line (non code block line)
with trailing spaces, ignoring the `br_spaces` configuration value,
by setting the `strict` configuration value to `True`.  With the default
value for `br_spaces` of `2` and `strict` set to `True`, all these lines
will trigger the rule:

```Markdown
This line does not end with any spaces.
This line ends with one space.{space}
This line ends with two spaces.{space}{space}
This line ends with three spaces.{space}{space}{space}
```

### Correct Scenarios

This rule does not trigger if a line does not end with any spaces
or if the line ends with the exact number of spaces specified by the
`br_spaces` configuration value:

```Markdown
This line does not end with any spaces.
This line ends with two spaces, which is okay.{space}{space}
```

As various programming languages allow spaces at the end of their lines,
the Indented Code Blocks and Fenced Code Blocks do not trigger this rule
for any of their lines.

In addition, various parsers may require spaces on blank lines within
List elements to keep that List element open.  Enabling the `list_item_empty_lines`
configuration value will cause this sample to not trigger the rule:

```Markdown
- a list item
{space}{space}
  still the same item, different paragraph
```

Note that the number of spaces needed to recognize the Blank Line
within the List element is decided by the current List Item element
that has the Blank Line.

## Fix Description

When fixed, each eligible line will either have 0 whitespace characters or `br_spaces`
whitespace characters at the end of that line.

## Configuration

| Prefixes |
| --- |
| `plugins.md009.` |
| `plugins.no-trailing-spaces.` |

<!-- pyml disable-num-lines 6 line-length-->
| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `br_spaces` | `integer` | `2` | Specifies the exact number of spaces allowed at the end of the line. |
| `strict` | `boolean` | `False` | Whether strict mode is enabled for the plugin. |
| `list_item_empty_lines` | `boolean` | `False` | Whether empty list item lines are exempt from this rule. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD009](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md009---trailing-spaces).

### Differences From MarkdownLint Rule

The main difference from the original rule is in how a HTML block is
managed. According to the original rule:

> Trailing space is allowed in indented and fenced code blocks because some languages
> require it.

However, in tests against the original rule, HTML blocks seemed to be
immune to triggering this rule.  This rule adheres to the text in the
original specification by not triggering on indented code blocks and
fenced code blocks but triggering on HTML blocks.

In addition, the original implementation used the `br_spaces` value
when using the `list_item_empty_lines` configuration value to decide
if that List Item Empty Line triggered the rule.  That algorithm has
been changed in this rule to instead use the number of spaces
required to satisfy the indentation requirements of the List element.
