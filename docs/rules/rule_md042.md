# Rule - MD042

| Aliases |
| --- |
| `md042` |
| `no-empty-links` |

## Summary

Fenced code blocks should have a language specified.

## Reasoning

The main reason for this rule is correctness.  By definition, both
normal links and image links present an URI that determines what they
link to.  If the URI that they refer to is not present, then is
goes against their very nature.

Also, during the creation of documents, authors often leave the
links blank to remind them to find and insert the correct URI later in the
creative process.  This rule also helps enforce that practice.

## Examples

### Failure Scenarios

This rule triggers when the link is empty and contains no characters or only
whitespace characters:

````Markdown
[empty link]()
````

This rule also triggers on URI fragments that are also similarly empty:

```Markdown
![empty fragment](#)
```

### Correct Scenarios

This rule does not trigger if any non-whitespace text is present within
the URI portion of the link:

````Markdown
[link](a)
````

Note that the link is not checked to see if it is validly formed or
present, just that at least one non-whitespace character is present.

Similarly, this rule does not trigger if any non-whitespace text is
present after the leading hash character (`#`) for the URI:

```Markdown
![fragment](#in-same-document)
```

## Configuration

| Prefixes |
| --- |
| `plugins.md042.` |
| `plugins.no-empty-links.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD042](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md042---no-empty-links).

### Differences From MarkdownLint Rule

The difference between this rule and the original rule is that the original
rule only fired on links, not image links.  As the only difference between
a link:

```Markdown
[fragment](#in-same-document)
```

and an image:

```Markdown
![fragment](#in-same-document)
```

is the `!` character, it made sense for the implementation to respect both elements.
