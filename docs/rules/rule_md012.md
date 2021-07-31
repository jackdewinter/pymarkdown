# Rule - MD012

| Aliases |
| --- |
| `md012` |
| `no-multiple-blanks` |

## Summary

Multiple consecutive blank lines.

## Reasoning

The primary reason for enabling this rule is that, with the exception of an
Indented Code Block element or a Fenced Code Block element, blank lines in
the Markdown document do not alter the rendering of the document as HTML. Except
in Code Block elements, blank lines only serve as delimiters between one element
and any following element.  Therefore, replacing multiple blank lines with a
single blank line provides equivalent functionality in those non-Code Block scenarios.

## Examples

### Failure Scenarios

This rule triggers if there are blank lines in any Container Block elements, in
certain HTML Block elements, and between existing elements, and the count of
consequitve Blank Line elements exceeds the configured maximum.

```Markdown
this is a line


this is another line
```

### Correct Scenarios

To correct the above example, simply reduce the number of Blank Lines to
the configured maximum number of Blank Line elements.  Assuming the default
value of `1`, this change would stop the rule from triggering.

```Markdown
this is a line

this is another line
```

## Configuration

| Prefixes |
| --- |
| `plugins.md012.` |
| `plugins.no-multiple-blanks.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the plugin rule is enabled by default. |
| `maximum` | `integer` | `1` | Number of blank lines to exceed before this rule triggers |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD012](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md012---multiple-consecutive-blank-lines).

### Differences From MarkdownLint Rule

The first difference was that the original rule did not fire within Block Quote elements, such
as this example:

```Markdown
> block quote before
>
>
> block quote after
```

In addition, in scenarios where the 

```Markdown
first line



second line
```

# TBD

- same as inspiration except where n > max + m.  in case, max + 1 to max +m will be issued.
- did not report in bq
