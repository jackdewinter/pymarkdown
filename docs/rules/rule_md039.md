# Rule - MD039

| Aliases |
| --- |
| `md039` |
| `no-space-in-links` |

## Summary

Spaces inside link text.

## Reasoning

The main reasons for this rule is readability and correctness.  When
creating a document or reading that same document, it is easy to confuse
the link labels `[ label ]`, `[label ]`, `[ label]` with the link label
`[label]`.  Being consistent with the leading spaces and trailing spaces
for a link label addresses this specific issue.

## Examples

### Failure Scenarios

This rule triggers when the link label for any link or image includes leading
whitespace or trailing whitespace.  This is true for all four forms of links and
for all four forms of images.

```Markdown
this is not
[ a proper](https://www.example.com)
link
```

### Correct Scenarios

This rule does not trigger if the link label for any link or image does not
start with leading whitespace or end with trailing whitespace.
This is true for all four forms of links and
for all four forms of images.

```Markdown
this is
[a proper](https://www.example.com)
link
```

## Configuration

| Prefixes |
| --- |
| `plugins.md039.` |
| `plugins.no-space-in-links.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled by default. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD039](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md039---spaces-inside-link-text).

### Differences From MarkdownLint Rule

The differnece between this rule and the original rule is that the original
rule only fired on links, not image links.  As the only difference between
a link:

```Markdown
[a link](https://www.example.com)
```

and an image:

```Markdown
![an image](https://www.example.com)
```

is the `!` character, it made sense for the implementation to respect both elements.
