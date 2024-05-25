# Rule - PML101

| Property | Value |
| --- | -- |
| Aliases | `pml101`, `list-anchored-indent` |
| Autofix Available | Pending review |
| Enabled By Default | No |

## Summary

Anchored list indentation.

## Reasoning

### Compatibility

This rule is specifically for Markdown parsers like the
[Python-Markdown](https://python-markdown.github.io/) parser. In their homepage's
section detailing their implementation [differences](https://python-markdown.github.io/#differences),
the authors clearly state:

> Indentation/Tab Length
>
> The syntax rules clearly state that when a list item consists of multiple paragraphs,
> "each subsequent paragraph in a list item must be indented by either 4 spaces or
> one tab" (emphasis added). However, many implementations do not enforce this rule
> and allow less than 4 spaces of indentation. The implementers of Python-Markdown
> consider it a bug to not enforce this rule.

The rule that they refer to is the initial
[Markdown specification](https://daringfireball.net/projects/markdown/syntax),
not the more recent [GitHub Flavored Markdown](https://github.github.com/gfm/)
specification.

PyMarkdown's linter does not weigh
in on the benefits or costs of that decision but seeks to help support the parser
as it is.  To that extent, this rule provides an alternative implementation to
[rule Md007](./rule_md007.md) that supports the initial specification as implemented
by Python-Markdown.  We refer to these as "anchored list indentations".

From our point of view, the type of lists supported by Python-Markdown are anchored
either at the start of the line or after a block quote character (and its optional
space character).  Typically, the base list is anchored to column 1 (no block quote)
or a column that is an odd number above 1 (block quote with space character). Once
that anchor is established with the base list, any sublists may start at any column
that is a multiple of 4 (by default) added to the base list's column.  In the case
of a base list that anchors at the start of the line, its column number is 1, so
any sublists may start at columns 5 (1+4), 9 (1+8), and so on.

## Examples

### Failure Scenarios

This rule triggers if any initial list start sequence does not start with the correct
indentation:

```Markdown
 * poorly indented unordered list
 1. poorly indented ordered list
>  * poorly indented list within a block quote
```

Once that base list indentation has been established, this rule triggers if any
subsequent sublist does not start at indents that are a multiplier of 4 (default)
to the right of the base list's indentation.

```Markdown
* properly indented unordered list
  * indented according to Md007

1. properly indented ordered list
   1. indented according to Md007

> * properly indented list within a block quote
>   * indented according to Md007
```

### Correct Scenarios

To correct the above examples, simply enforce the required indentation using space
characters:

```Markdown
* properly indented unordered list
    * indented according to Md007

1. properly indented ordered list
    1. indented according to Md007

> * properly indented list within a block quote
>     * indented according to Md007
```

If required, the amount of indentation at each level can be set using
the `indent` configuration value.

### Notes

#### Enabling This Rule

This rule was developed as an alternative to [Rule Md007](./rule_md007.md), enabling
the project to better support parsers like the
[Python-Markdown](https://python-markdown.github.io/) parser. As such, it is strongly
advised to disable Rule Md007 when enabling Pml101.

## Fix Description

The fix for this rule is currently in review.

## Configuration

| Prefixes |
| --- |
| `plugins.pml101.` |
| `plugins.list-anchored-indent.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `indent` | `integer` | `4` | Number of spaces needed between sublists starts. |

## Origination of Rule

This rule was developed as an alternative to [Rule Md007](./rule_md007.md), enabling
the project to better support parsers like the
[Python-Markdown](https://python-markdown.github.io/) parser.
