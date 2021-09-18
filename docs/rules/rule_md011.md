# Rule - MD011

| Aliases |
| --- |
| `md011` |
| `no-reversed-links` |

## Summary

Reversed link syntax.

## Reasoning

The primary reason for enabling this rule is correctness.  It is
possible to transpose the `[]` characters and the `()` characters
while typing, resulting in something that is not a link.  This pattern
has probably happened enough times that the original rule was authored
to correct this transposition.

## Examples

### Failure Scenarios

This rule triggers when any non code block, non HTML block line
contains an Inline Link that appears to have the `[]` characters and
the `()` characters transposed:

```Markdown
This link (is)[/tranposed].
```

### Correct Scenarios

To correct the above example, transpose the `[]` characters and
the `()` characters to their correct order:

```Markdown
This link [is not](/tranposed).
```

Note that some parsers implement the
[Markdown Extra](https://en.wikipedia.org/wiki/Markdown_Extra)
footnotes, and it is possible to construct a legal footnote
that may look like a reversed link:

```Markdown
... to it (as an example)[^footnote].  Therefore...
```

To accomodate these footnotes, if the apparent URL section
starts with a `^` character, this rule will not trigger.

## Configuration

| Prefixes |
| --- |
| `plugins.md011.` |
| `plugins.no-reversed-links.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the plugin rule is enabled by default. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD011](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md011---reversed-link-syntax).
