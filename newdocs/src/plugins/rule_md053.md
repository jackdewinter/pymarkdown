# Rule - MD053

| Property | Value |
| --- | --- |
| Aliases | `md053`, `link-image-reference-definitions` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Link and image reference definitions should be needed.

## Reasoning

### Readability

Link reference definitions allow documents to keep links organized in one place. However, two situations can arise that affect readability:

- **Unused definitions**: A definition exists but is never referenced, creating clutter.
- **Duplicate definitions**: Multiple definitions share the same label (case-insensitive), causing confusion about which URL is intended.

> **Note**: Labels are compared after Unicode case-folding, stripping leading/trailing whitespace, and collapsing internal whitespace. For example, `some-link`, `Some-Link`, and `some   link` are treated as identical.

## Examples

### Failure Scenarios

This rule triggers when a link reference definition is defined but not used anywhere in the document.

```Markdown
Go to [this link][some-link].

[some-link]: /url
[some-other-link]: /url
```

> **Explanation**: The definition `[some-other-link]` is present but never referenced by any link or image in the document. This violates the rule because link reference definitions should be needed.

Unlike the previous example, this case uses a link reference label that is defined multiple times.

```Markdown
Go to [this link][some-link].

[some-link]: /url
[Some-Link]: /other-url
```

> **Explanation**: The label `some-link` (case-insensitive match to `Some-Link`) is defined twice. According to the GFM spec, the first definition takes precedence, rendering the second definition unused and redundant, which violates the rule.

### Correct Scenarios

This rule does not trigger when all link reference definitions are used and have unique labels.

```Markdown
Go to [this link][some-link].
Show ![this image][some-other-link].

[some-link]: /url
[some-other-link]: /image-url
```

> **Explanation**: Both `[some-link]` and `[some-other-link]` are defined exactly once and referenced in the document. This satisfies the rule requirement that definitions must be needed and unique.

Unlike the previous example, this case uses link reference definitions with labels that are configured to be ignored, effectively acting as comments.

```Markdown
[//]: /u (This behaves like a comment)
```

> **Explanation**: The definition `[//]` is present but never referenced by any link or image. However, because `//` is included in the `ignored-definitions` configuration item (default value `"//"`), this definition is excluded from triggering the rule. This satisfies the rule by being an explicitly allowed exception.

## Fix Description

The reason for not being able to auto-fix this rule is certainty. Removing unused definitions is generally safe, but determining whether a duplicate definition should be removed or merged requires understanding the author's intent. Additionally, some definitions may be intentionally ignored (via `ignored-definitions`), and auto-removal could delete definitions that the user considers valid comments or placeholders. Therefore, manual review is required to ensure no intended definitions are incorrectly removed.

## Configuration

| Prefixes |
| --- |
| `plugins.md053.` |
| `plugins.link-image-reference-definitions.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `ignored-definitions` | `str` | `"//"` | Comma-separated list of link texts that do not trigger this rule. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD053](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md053---link-and-image-reference-definitions-should-be-needed).
