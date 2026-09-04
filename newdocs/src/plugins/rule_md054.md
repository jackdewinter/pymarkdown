# Rule - MD054

| Property | Value |
| --- | --- |
| Aliases | `md054`, `link-image-style` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Keep the style of links and images consistent within a Markdown document.

## Reasoning

### Consistency

Consistent link and image styles make a document easier to read and maintain.
Restricting a document to a chosen subset of the six supported styles
(autolink, inline link, full reference, collapsed reference, shortcut
reference, and inline URL) reduces stylistic drift across a repository and
helps readers recognize the same construct the same way.

## Examples

### Failure Scenarios

This rule triggers when an autolink (e.g., `<https://example.com>`) is used in a location where the `autolinks` configuration value is set to `False`.

```Markdown
<https://example.com>
```

> **Explanation**: The example uses an autolink. If the `autolinks` configuration
> value is set to `False`, this autolink violates the rule because that style is
> disabled.

Unlike the previous example, this case uses an inline link and is triggered only when `inline-links` is set to `False`.

```Markdown
[link](https://example.com)
```

> **Explanation**: The example uses an inline link. If the `inline-links` configuration value is set to `False`, this inline link violates the rule because the style is no longer permitted.

Unlike the previous example, this case uses a full reference link and is triggered only when `full-links` is set to `False`.

```Markdown
[link][url]

[url]: https://example.com
```

> **Explanation**: The example uses a full reference link (`[link][url]` with a corresponding `[url]:` definition). If the `full-links` configuration value is set to `False`, this full reference link violates the rule because that style is disabled.

Unlike the two preceding examples, this case uses a collapsed reference link and is triggered only when `collapsed-links` is set to `False`.

```Markdown
[url][]

[url]: https://example.com
```

> **Explanation**: The example uses a collapsed reference link (`[url][]`). If the `collapsed-links` configuration value is set to `False`, this collapsed reference link violates the rule because that style is disabled.

Unlike the preceding reference-link example, this case uses a shortcut reference link and is triggered only when `shortcut-links` is set to `False`.

```Markdown
[url]

[url]: https://example.com
```

> **Explanation**: The example uses a shortcut reference link (`[url]`). If the `shortcut-links` configuration value is set to `False`, this shortcut reference link violates the rule because that style is disabled.

Unlike the previous reference-link example, this case uses an inline link whose label
and URL are identical and is triggered only when `inline-urls` is set to `False`.

```Markdown
[https://example.com](https://example.com)
```

> **Explanation**: The example uses an inline link whose label and URL are identical. If the `inline-urls` configuration value is set to `False`, this self-referencing inline link violates the rule because that style is disabled.

### Correct Scenarios

This rule does not trigger when an autolink (e.g., `<https://example.com>`) is used in a location where the `autolinks` configuration value remains `True`.

```Markdown
<https://example.com>
```

> **Explanation**: The example uses an autolink. With the default configuration for `autolinks` set to `True`, autolinks are permitted, so the rule does not trigger on this construct.

Unlike the previous autolink example, this case uses an inline link and satisfies the rule as long as `inline-links` has not been disabled.

```Markdown
[link](https://example.com)
```

> **Explanation**: The example uses an inline link. With the default configuration for `inline-links` set to `True`, inline links are permitted, so the rule does not trigger on this construct.

Unlike the preceding inline-link example, this case uses a full reference link and satisfies the rule as long as `full-links` has not been disabled.

```Markdown
[link][url]

[url]: https://example.com
```

> **Explanation**: The example uses a full reference link with a matching link reference definition. With the default configuration of `full-links` set to `True`, full reference links are permitted, so the rule does not trigger.

Unlike the preceding full reference link, this case uses a collapsed reference link and satisfies the rule as long as `collapsed-links` has not been disabled.

```Markdown
[url][]

[url]: https://example.com
```

> **Explanation**: The example uses a collapsed reference link. With the default configuration for `collapsed-links` set to `True`, collapsed reference links are permitted, so the rule does not trigger.

Unlike the preceding collapsed reference link, this case uses a shortcut reference link and satisfies the rule as long as `shortcut-links` has not been disabled.

```Markdown
[url]

[url]: https://example.com
```

> **Explanation**: The example uses a shortcut reference link. With the default configuration of `shortcut-links` set to `True`, shortcut reference links are permitted, so the rule does not trigger.

Unlike the preceding shortcut reference link, this case uses an inline link whose
label and URL are identical and satisfies the rule as long as `inline-urls` has not
been disabled.

```Markdown
[https://example.com](https://example.com)
```

> **Explanation**: The example uses an inline link whose label and URL are identical.
> With the default configuration for `inline-urls` set to `True`, this style is
> permitted, so the rule does not trigger.

## Fix Description

The tool cannot autofix this, because a non-permitted link or image could be
rewritten into any of the other enabled styles (autolink, full reference,
collapsed reference, shortcut reference, or inline URL). Choosing one
replacement without author intent could change the meaning or emphasis of the
document.

## Configuration

| Prefixes |
| --- |
| `plugins.md054.` |
| `plugins.link-image-style.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `autolinks` | `boolean` | `True` | Whether autolinks are allowed. |
| `inline-links` | `boolean` | `True` | Whether inline links and images are allowed. |
| `full-links` | `boolean` | `True` | Whether full links and images are allowed. |
| `collapsed-links` | `boolean` | `True` | Whether collapsed links and images are allowed. |
| `shortcut-links` | `boolean` | `True` | Whether shortcut links and images are allowed. |
| `inline-urls` | `boolean` | `True` | Whether inline URLs for links and images are allowed. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD054](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md054---link-and-image-style).
