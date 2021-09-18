# Rule - MD037

| Aliases |
| --- |
| `md037` |
| `no-space-in-emphasis` |

## Summary

Spaces inside emphasis markers.

## Reasoning

The primary reason for enabling this rule is to try and detect cases
where the author probably meant to specify emphasis on a word or
series of words.  Most parsers will not detect emphasized text if
there is whitespace on both sides of the emphasis characters, so
this rule specifically looks for instances where that happens.

Note that this rule does not currently handle cases of nested emphasis,
such as `***` for combining an italics emphasis with a bold emphasis.

## Examples

### Failure Scenarios

This rule triggers if a pair of matching emphasis characters occur
within the same paragraph with space around either of the emphasis
characters.

```Markdown
this is ** not some ** bold text
```

### Correct Scenarios

This rule does not trigger if there is no whitespace present on the
inside of the emphasis.

```Markdown
this is **some** bold text
```

## Configuration

| Prefixes |
| --- |
| `plugins.md037.` |
| `plugins.no-space-in-emphasis.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD037](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md037---spaces-inside-emphasis-markers).

### Differences From MarkdownLint Rule

The original rule did not distinguish between probable emphasis situations
and emphasis sequences.  As such, text such as `this * is not * emphasis`
raised triggered on both the first and the second emphasis characters.
This rule looks for scenarios where there are a matched pair of emphasis
characters, instead of just looking for those individual characters.
