# Rule - MD013

| Property | Value |
| --- | -- |
| Aliases | `md013`, `line-length` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Line length.

## Reasoning

### Readability/Consistency

For every user, there is a specific number of columns that can be displayed
on their screen before the user feels that data on their screen becomes unreadable.
To provide consistency across application or organizations, a specific maximum
line length may be put in place to establish an expectation of console window
and editor window width.  That established line length, used across a set of documents,
helps to promote a consistent line length, setting expectations in the reader's mind
that improve the readability of those documents.

## Examples

### Failure Scenarios

This rule triggers if the length of any line exceeds a given character count.
Assuming that the configuration values are set to a maximum line length of
50 characters, the following example will trigger this rule:

```Markdown
This is a sample line that is a total of 60 characters long.
```

### Correct Scenarios

This rule does not trigger if the length of any line is less than or
equal to a given character count. If the configuration values
are set to a maximum line length of 50 characters, the following
example will not trigger this rule:

```Markdown
This is a sample line  that is 50 characters long.
```

#### Long Last Words

To allow for longer, continuous constructs, such as URLs, a check
is performed to see if there is any whitespace beyond the specified
character count.  If there are no whitespace characters, then this
rule will not trigger.  An example of this is:

```Markdown
This is a sample line that is a total of 60-characters-long.
```

where the boundary is at the second `c` character in `60-characters-long`.

If this is not the desired behavior, there are two options.  The first option,
the `strict` configuration value, forces this rule to trigger if any character
is present past the specified line length. The `stern` configuration is another
option, allowing lines without any spaces past the specified line length
while triggering on lines that are too long.

#### Special Elements

For line lengths, two types of elements stick out as
needing special attention: headings and code blocks.  To that extent,
the `heading_line_length` configuration value specifies the line length
for headings and `headings` configuration value specifies whether this
rule triggers at all for headings.  Similarly, the `code_block_line_length`
and `code_blocks` configuration values perform the same action for
code blocks.

## Fix Description

The auto-fix feature for this rule is scheduled to be added soon after the v1.0.0
release.

## Configuration

| Prefixes |
| --- |
| `plugins.md013.` |
| `plugins.line-length.` |

<!--- pyml disable-num-lines 10 line-length-->
| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `line_length` | `integer` | `80` | Maximum number of characters on a normal line. |
| `heading_line_length` | `integer` | `80` | Maximum number of characters on a heading line. |
| `code_block_line_length` | `integer` | `80` | Maximum number of characters on a code block line. |
| `headings` | `boolean` | `True` | Whether the plugin rule triggers on lines in a heading. |
| `code_blocks` | `boolean` | `True` | Whether the plugin rule triggers on lines in a code block. |
| `stern` | `boolean` | `False` | Whether the 'stern' trigger rules are in effect. |
| `strict` | `boolean` | `False` | Whether the 'strict' trigger rules are in effect. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD013](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md013---line-length).

### Differences From MarkdownLint Rule

The substantial difference from the original rule is that the `table` configuration
value is not present as the PyMarkdown parser does not currently support tables.
