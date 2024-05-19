# Rule - MD028

| Property | Value |
| --- | -- |
| Aliases | `md028`, `no-blanks-blockquote` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Blank line inside blockquote.

## Reasoning

### Consistency

While most parsers agree on the core rules for parsing, there are boundary
scenarios that parsers cannot agree on.  A blank line within a block quote is
one of those scenarios.  To be consistent and support parsers that
are not fully Markdown compliant, this rule attempts to resolve any
issues with this boundary conditions before they happen.

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
