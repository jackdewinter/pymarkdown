# Rule - MD038

| Aliases |
| --- |
| `md038` |
| `no-space-in-code` |

## Summary

Spaces inside code span elements.

## Reasoning

The primary reason for enabling this rule is that different parsers
will interpret extra leading and trailing spaces in code spans differently.
To ensure that the author's intent for the code span is respected,
mismatched extra leading and trailing spaces trigger this rule.

## Examples

### Failure Scenarios

This rule triggers if there is unbalanced spaces at the start:

```Markdown
this is an ` invalid` code span
```

or the end:

```Markdown
this is an `invalid ` code span
```

of the code span text.

As a balanced pair of spaces at the start and the end of the code span
text are automatically removed, this rule will trigger on multiple
spaces at the start or end of the code span text:

```Markdown
this is an `  invalid  ` code span
```

### Correct Scenarios

This rule does not trigger if there are no spaces at the start and end
of the code span text:

```Markdown
this is a `valid` code span
```

or if there are single spaces at the start and the end of the code span text:

```Markdown
this is a ` valid ` code span
```

Because it is possible for a code span to contain the backtick character (`` ` ``)
itself under certain situations, a single space character is allowed before
that backtick character to distinguish it from the code span boundary itself.

```Markdown
this is a `` `valid `` code span
```

## Configuration

| Prefixes |
| --- |
| `plugins.md038.` |
| `plugins.no-space-in-code.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the plugin rule is enabled by default. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD038](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md038---spaces-inside-code-span-elements).
