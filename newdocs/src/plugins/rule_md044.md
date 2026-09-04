# Rule - MD044

| Property | Value |
| --- | --- |
| Aliases | `md044`, `proper-names` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Proper names should have the correct capitalization.

## Reasoning

### Consistency

Proper nouns often have specific capitalization requirements (e.g., `PyMarkdown`, not `pymarkdown` or `PYMARKDOWN`). Enforcing consistent capitalization improves document professionalism and readability by ensuring brand names and technical terms are presented uniformly across all content.

## Examples

### Failure Scenarios

This rule triggers when this rule finds any standalone instance of a
word specified in the `names` configuration value that does not have
a correct capitalization. Assuming `names` is set to `ParaGraph`, then
the following example will trigger this rule:

```Markdown
this is a paragraph.
```

> **Explanation**: The word "paragraph" appears in the text, but the configuration `names` expects "ParaGraph". Since "paragraph" does not match the required capitalization "ParaGraph", the rule triggers.

Unlike the previous example with standalone text, this rule also triggers on matching text in inline link labels and link titles, but not the link URI:

```Markdown
this is a [paragraph](/paragraph "a paragraph item") link.
```

> **Explanation**: The word "paragraph" appears in the link label and the link title. The configuration `names` expects "ParaGraph". Since "paragraph" does not match the required capitalization "ParaGraph" in the label and title, the rule triggers. Note that the URI `/paragraph` is ignored as per rule criteria.

Unlike the inline link scenario, for reference-style links and images, this rule triggers on any occurrence in the link label.

```Markdown
![collapsed
paragraph][]
link

[collapsed
paragraph]: /url "a paragraph title"
```

> **Explanation**: The word "paragraph" appears in the image label and the link reference label. The configuration `names` expects "ParaGraph". Since "paragraph" does not match the required capitalization "ParaGraph" in these labels, the rule triggers.

### Correct Scenarios

This rule does not trigger when the proper name appears with the correct capitalization as specified in the `names` configuration. Assuming `names` is set to `ParaGraph`, then the following example will not trigger this rule:

```Markdown
this is a ParaGraph.
```

> **Explanation**: The word "ParaGraph" appears in the text. The configuration `names` expects "ParaGraph". Since the capitalization matches exactly, the rule does not trigger.

In addition, this rule does not trigger if the found text is not an
isolated word within the text. For example, even if `names` is set to
`ParaGraph`, the following lines of text will not trigger this rule:

```Markdown
this is a paragraphing
this is a reparagraph
```

> **Explanation**: The string "ParaGraph" is configured as a proper name. However, in this example, "paragraph" is part of the larger words "paragraphing" and "reparagraph". Since the rule only triggers on standalone instances of the word, and these are not standalone instances, the rule does not trigger.

## Fix Description

The specified word is replaced by the properly cased word presented in the
configuration item.

## Configuration

| Prefixes |
| --- |
| `plugins.md044.` |
| `plugins.proper-names.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `names` | `string` | None | Comma-separated list of proper nouns to preserve capitalization on.** |
| `code_blocks` | `boolean` | `True` | Search in Fenced Code Block elements and Indented Code Block elements. |
| `code_spans` | `boolean` | `True` | Search in Inline Code Span elements. |

** The comma-separated list of items is a string with a format of `{item},...,{item}`.
Any leading or trailing space characters surrounding the `{item}` are trimmed during
processing. Any empty `{item}` value left after this trimming has been applied
will generate a configuration error.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD044](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md044---proper-names-should-have-the-correct-capitalization).
