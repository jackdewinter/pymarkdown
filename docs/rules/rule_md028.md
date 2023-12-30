# Rule - MD028

| Aliases |
| --- |
| `md028` |
| `no-blanks-blockquote` |

| Autofix Available |
| --- |
| No |

## Summary

Blank line inside blockquote.

## Reasoning

### Consistency

Especially with *weird* cases, like the one this rule tries to protect
against, parsers can return surprisingly different results for how "failure"
scenarios below are interpreted into HTML.  To reduce the complexity needed
to determine which parser return which result, this rule attempts to
remove the single most divisive scenario between parsers: blank lines within
Block Quote elements.

## Examples

### Failure Scenarios

This rule triggers when there are one or more Blank Line elements between
a pair of Block Quote sections:

````Markdown
> This is one section of a block quote

> This is the other section.
````

Due to the Laziness requirements of Block Quote elements, it is possible
that a Paragraph element thought to be following a Block Quote element
may be included in the previous Block Quote section.

````Markdown
> This is one section of a block quote
This looks like its own paragraph but is really part of the above block quote.

> This is the other section.
````

### Correct Scenarios

This rule triggers if a Block Quote element is followed by one or
more Blank Lines and a new Block Quote section.  Therefore, the correct
way to address those issues is to ensure the first Block Quote section
is not followed by a Blank Line:

````Markdown
> This is one section of a block quote
# Not A Blank Line
> This is the other section.
````

or to have that Blank Line be followed by something that is not
another Block Quote element:

````Markdown
> This is one section of a block quote

This is its own paragraph.
> This is the other section.
````

To ensure that the above example is readable, it is suggested that the
Block Quote is prefaced with its own Blank Line:

````Markdown
> This is one section of a block quote

This is its own paragraph.

> This is the other section.
````

## Configuration

| Prefixes |
| --- |
| `plugins.md028.` |
| `plugins.no-blanks-blockquote.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD028](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md028---blank-line-inside-blockquote).

## Fix Description

The reason for not being able to auto-fix this rule is clarity.  Given the Markdown
example from above:

````Markdown
> This is one section of a block quote
This looks like its own paragraph but is really part of the above block quote.

> This is the other section.
````

it is unclear if the second line that starts with `This looks like` is part of
the block quote or if it is in its own paragraph following the block quote. As the
context of that line is not clear, any fix to that line would also be unclear.
