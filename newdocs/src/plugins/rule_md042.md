# Rule - MD042

| Property | Value |
| --- | --- |
| Aliases | `md042`, `no-empty-links` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

No empty links.

## Reasoning

### Correctness

Links require a valid URI to function. Empty URIs break navigation and may indicate unfinished documentation. This rule ensures all links contain non-whitespace content, improving document reliability and accessibility for readers who rely on functional navigation.

## Examples

### Failure Scenarios

This rule triggers when the link is empty and has no characters or only
whitespace characters:

```Markdown
[empty link]()
```

> **Explanation**: This link fails because the URI part `()` is completely empty, containing no characters or whitespace. The rule requires at least one non-whitespace character in the URI.

Unlike the previous example with a fully empty URI, this shows that URIs containing only a hash (`#`) are also treated as empty, applying to both regular links and image links:

```Markdown
[empty fragment link](#)
![empty fragment image](#)
```

> **Explanation**: Both links fail because the URI fragment `#` contains no text after the hash. The rule requires non-whitespace content in the URI, even for fragments, and applies equally to standard links and image links.

Unlike the previous examples which had empty or hash-only URIs, this scenario demonstrates a URI containing only whitespace characters, which the rule also treats as empty:

```Markdown
[link with spaces](   )
```

> **Explanation**: This link fails because the URI contains only whitespace characters (spaces). The rule requires at least one non-whitespace character in the URI to be considered valid.

### Correct Scenarios

This rule does not trigger when any non-whitespace text is present within the URI part of the link:

```Markdown
[link](a)
```

> **Explanation**: This link passes because the URI contains the character `a`, which is non-whitespace. The rule only checks for the presence of at least one non-whitespace character, not the validity of the URL.

Unlike the previous example which had a simple URI, this scenario demonstrates a fragment link with text after the hash character:

```Markdown
![fragment](#in-same-document)
```

> **Explanation**: This image link passes because the URI contains `#in-same-document`, which has non-whitespace text (`in-same-document`) after the hash. This satisfies the rule's requirement for content in the URI.

## Fix Description

The reason for not being able to auto-fix this rule is context. Without context
provided by the author, adding the proper link destination to the link is almost
impossible.

## Configuration

| Prefixes |
| --- |
| `plugins.md042.` |
| `plugins.no-empty-links.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD042](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md042---no-empty-links).

### Differences From MarkdownLint Rule

The difference between this rule and the original rule is that the original
rule only fired on links, not image links. As the only difference between
a link:

```Markdown
[fragment](#in-same-document)
```

and an image:

```Markdown
![fragment](#in-same-document)
```

is the `!` character, it made sense for the implementation to respect both elements.
