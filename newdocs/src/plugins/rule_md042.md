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

Empty URIs produce broken links that fail navigation for readers, including screen-reader
users who rely on functional link targets.

## Examples

### Failure Scenarios

This rule triggers when the URI part of the link is empty or contains only whitespace
characters:

```Markdown
[empty link]()
![empty image]()
```

> **Explanation**: Both elements fail because the URI part `()` is completely empty
> — it contains no characters at all. The rule requires at least one non-whitespace
> character in the URI, and this applies equally to standard links and image links.

Unlike the previous example with a fully empty URI, this shows that URIs containing
only a hash (`#`) are also treated as empty, applying to both regular links and
image links:

```Markdown
[empty fragment link](#)
![empty fragment image](#)
```

> **Explanation**: Both links fail because the URI fragment `#` contains no text
> after the hash. The rule requires non-whitespace content in the URI, even for
> fragments, and applies equally to standard links and image links.

Unlike the previous examples which had empty or hash-only URIs, this scenario demonstrates
a URI containing only whitespace characters, which the rule also treats as empty:

```Markdown
[link with spaces](   )
```

> **Explanation**: This link fails because the URI contains only whitespace characters
> (three spaces). The rule requires at least one non-whitespace character in the
URI to be considered valid.

### Correct Scenarios

This rule does not trigger when any non-whitespace text is present within the URI
part of the link:

```Markdown
[link](a)
![image](image.png)
```

> **Explanation**: Both elements pass because each URI (`a` and `image.png`) contains
> non-whitespace content. The rule only checks for the presence of at least one
> non-whitespace character, not the validity of the URL, and this applies equally
> to standard links and image links.

Unlike the previous example which had a simple URI, this scenario demonstrates a
fragment link with text after the hash character:

```Markdown
[fragment](#in-same-document)
```

> **Explanation**: This link passes because the URI contains `#in-same-document`,
> which has non-whitespace text (`in-same-document`) after the hash. This satisfies
> the rule's requirement for content in the URI.

Unlike the previous example which used a relative path, this scenario shows an absolute
external URL, the other common real-world destination:

```Markdown
[Python documentation](https://docs.python.org/3/)
![Python logo](https://www.python.org/static/img/python-logo.png)
```

> **Explanation**: Both elements pass because their URIs contain non-whitespace
> content (full `https://` URLs). The rule does not validate the URL — it only requires
> that the URI is not empty or whitespace-only — so any syntactically non-empty
> destination satisfies it.

## Fix Description

An empty link does not indicate a single correct destination. Without additional
context from the author, choosing an appropriate replacement target is not
reliably possible, so this rule is not auto-fixable.

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
