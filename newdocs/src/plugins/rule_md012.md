# Rule - MD012

| Property | Value |
| --- | -- |
| Aliases | `md012`, `no-multiple-blanks` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

Multiple consecutive blank lines.

## Reasoning

### Simplicity

The primary reason for enabling this rule is that, except for when they are present
within an Indented Code Block element or a Fenced Code Block element, multiple blank
lines in a Markdown document are ignored. Outside of Code Block elements, the only
purpose that blank lines have is to serve as delimiters between one element and
any following element.  Therefore, replacing multiple blank lines with a single
blank line supplies the equivalent functionality with no structural change to the
document.

## Examples

### Failure Scenarios

This rule triggers if there are blank lines in any Container Block elements, in
certain HTML Block elements, and between existing elements, and the count of
consecutive Blank Line elements exceeds the configured maximum.

```Markdown
this is a line


this is another line
```

### Correct Scenarios

To correct the above example, simply reduce the number of Blank Lines to
the configured maximum number of Blank Line elements.  Assuming the default
value of `1`, this change would stop the rule from being triggered.

```Markdown
this is a line

this is another line
```

## Fix Description

The auto-fix feature for this rule is scheduled to be added soon after the v1.0.0
release.

## Configuration

| Prefixes |
| --- |
| `plugins.md012.` |
| `plugins.no-multiple-blanks.` |

<!-- pyml disable-num-lines 4 line-length-->
| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `maximum` | `integer` | `1` | Number of blank lines to exceed before this rule triggers |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD012](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md012---multiple-consecutive-blank-lines).

### Differences From MarkdownLint Rule

The first difference was that the original rule did not fire with blank lines placed
within Block Quote elements, such as this example:

```Markdown
> block quote before
>
>
> block quote after
```
