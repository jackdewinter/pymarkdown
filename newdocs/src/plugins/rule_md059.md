# Rule - MD059

| Property | Value |
| --- | --- |
| Aliases | `md059`, `descriptive-link-text` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Link text should be descriptive.

## Reasoning

### Accessibility

Placeholder link text such as `click here`, `here`, `link`, and `more` provides no context for screen reader users who navigate by links alone. Descriptive link text ensures that the purpose of the link is clear without surrounding context, improving accessibility.

## Examples

### Failure Scenarios

This rule triggers when the text associated with a link contains any of the specified placeholders, such as `click here`, `here`, `link`, or `more`.

```Markdown
To read more, [click here](#some-section).
```

> **Explanation**: This example fails because the link text `click here` is in the list of prohibited phrases. The rule checks the interpreted link text (case-insensitive, trimmed) against the `prohibited-phrases` configuration.

Unlike the previous example, this case demonstrates the rule triggering on a reference-style link.

```Markdown
Go to this [link][some-link].

[some-link]: /url
```

> **Explanation**: This example fails because the link text `link` is in the list of prohibited phrases. The rule applies to reference-style links as well as inline links.

This scenario shows a shortcut reference link using the prohibited word.

```Markdown
Go here for [more][] information.

[more]: /url
```

> **Explanation**: This example fails because the link text `more` is in the list of prohibited phrases. The rule detects prohibited text in shortcut reference links where the label matches the link definition.

This scenario shows a collapsed reference link using the prohibited word.

```Markdown
Go here for [more] information.

[more]: /url
```

> **Explanation**: This example fails because the link text `more` is in the list of prohibited phrases. The rule detects prohibited text in collapsed reference links.

Unlike the previous examples, this case shows that leading/trailing spaces and multiple internal spaces are ignored when evaluating the link text.

```Markdown
To read more, [ Click  Here ](#some-section).
```

> **Explanation**: This example also fails because, after trimming spaces and converting to lowercase, the link text becomes `click here`, which is a prohibited phrase. The rule normalizes the text before checking against the prohibited list.

Unlike the previous examples, this case demonstrates that customizing the `prohibited-phrases` configuration completely overrides the default list.

```Markdown
To read more, [click one here](#some-section).
```

> **Explanation**: This example fails because the custom `prohibited-phrases` list includes `click one here`. The default phrases (`click here`, `here`, `link`, `more`) are no longer checked unless explicitly included in the new configured custom list. If one of those phrases is no longer in the custom list, a link with just that phrase would not trigger this rule in this configuration.

### Correct Scenarios

This rule does not trigger when the interpreted link text is not one of the prohibited phrases, such as using a descriptive phrase.

```Markdown
Go to [this section](#some-section).
```

> **Explanation**: This example passes because the link text `this section` is not in the list of prohibited phrases (`click here`, `here`, `link`, `more`). The rule only flags link text that matches the prohibited list exactly (after normalization).

Unlike the previous example, this case shows that a link containing a prohibited word as part of a larger descriptive phrase does not trigger the rule.

```Markdown
[Click here to learn more](#some-section).
```

> **Explanation**: This example passes because the link text `Click here to learn more` does not exactly match any prohibited phrase (`click here`, `here`, `link`, `more`). The rule requires an exact match after normalization, not a substring match.

## Fix Description

Automatic fixing is not possible because determining appropriate, descriptive link text requires understanding the context and intent of the link, which is ambiguous without human judgment. Replacing generic text with specific content could result in incorrect or misleading descriptions.

## Configuration

| Prefixes |
| --- |
| `plugins.md059.` |
| `plugins.descriptive-link-text.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `prohibited-phrases` | `str` | `"click here,here,link,more"` | Comma-separated list of phrases that are prohibited. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD059](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md059---link-text-should-be-descriptive).
