# Rule - MD011

| Aliases |
| --- |
| `md011` |
| `no-reversed-links` |

## Summary

Reversed link syntax.

## Reasoning

### Correctness

It is possible to transpose the `[]` characters and the `()` characters
while typing, resulting in text that does not represent the intended link.
This pattern has probably happened enough times that the original rule was
authored to correct for situations like this.

## Examples

### Failure Scenarios

This rule triggers when any non code block, non HTML block line
contains an Inline Link that appears to have the `[]` characters and
the `()` characters transposed:

```Markdown
This link (is)[/transposed].
```

### Correct Scenarios

To correct the above example, transpose the `[]` characters and
the `()` characters to their correct order:

```Markdown
This link [is not](/transposed).
```

Note that some parsers implement the
[Markdown Extra](https://en.wikipedia.org/wiki/Markdown_Extra)
footnotes, and it is possible to construct a legal footnote
that may look like a reversed link:

```Markdown
... to it (as an example)[^footnote].  Therefore...
```

To accommodate those footnotes sequences, if the apparent URL section
starts with a `^` character, this rule will not trigger.

## Configuration

| Prefixes |
| --- |
| `plugins.md011.` |
| `plugins.no-reversed-links.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD011](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md011---reversed-link-syntax).
