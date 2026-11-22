# Rule - MD044

| Property | Value |
| --- | --- |
| Aliases | `md044`, `proper-names` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Ensure proper names use the correct capitalization.

## Reasoning

### Consistency

Proper nouns often have specific capitalization requirements (e.g., `PyMarkdown`,
not `pymarkdown` or `PYMARKDOWN`). Consistent capitalization of brand names and
technical terms reduces reader confusion and keeps documents consistent across the
project.

## Examples

### Failure Scenarios

This rule triggers when a standalone word in the body text does not match the capitalization
configured in `names` (e.g., `names` is set to `ParaGraph`):

```Markdown
this is a paragraph.
```

> **Explanation**: The word "paragraph" appears in the text, but the configuration
> `names` expects "ParaGraph". Since "paragraph" does not match the required capitalization
> "ParaGraph", the rule triggers.

Unlike the previous example with standalone text, this rule also triggers on matching
text in inline link labels and link titles, but not the link URI:

```Markdown
this is a [paragraph](/paragraph "a paragraph item") link.
```

> **Explanation**: The word "paragraph" appears in the link label and the link title.
> The configuration `names` expects "ParaGraph". Since "paragraph" does not match
> the required capitalization "ParaGraph" in the label and title, the rule triggers.
> Note that the URI `/paragraph` is ignored as per rule criteria.

Unlike the inline link scenario, for reference-style links and images, this rule
triggers on any occurrence in the link label.

```Markdown
![collapsed
paragraph][]
link

[collapsed
paragraph]: /url "a paragraph title"
```

> **Explanation**: The word "paragraph" appears in the image label and the link
> reference label. The configuration `names` expects "ParaGraph". Since "paragraph"
> does not match the required capitalization "ParaGraph" in these labels, the rule
> triggers.

Unlike the previous scenarios, which all operate on visible Markdown body text,
this rule also triggers on matches inside fenced code blocks when the `code_blocks`
configuration value is `True` (the default).

```Markdown
# A fenced code block
print("paragraph")
```

> **Explanation**: The word "paragraph" appears inside the fenced code block. With
> `code_blocks` set to `True`, the rule scans code block content, so the rule triggers.

Unlike the prior code-block scenario, this case shows that matches inside an inline
code span also trigger the rule when `code_spans` is `True` (the default).

```Markdown
Use the `paragraph` element here.
```

> **Explanation**: The word "paragraph" appears inside the inline code span. With
> `code_spans` set to `True`, the rule scans inline code span content, so the rule
> triggers.

Unlike the previous example that used a lowercase word, this case shows that an
all-uppercase variant is also a failure when it does not exactly match the configured
proper name.

```Markdown
this is a PARAGRAPH.
```

> **Explanation**: The configuration `names` expects exactly `ParaGraph`. The text
> contains `PARAGRAPH`, which differs in capitalization from the configured value.
> Because the comparison is case-sensitive and `PARAGRAPH` is not an exact match
> for `ParaGraph`, the rule triggers.

Unlike the previous fenced code block scenario, this case shows that the same match
inside an **indented** code block also triggers the rule when `code_blocks` is `True`
(the default).

```Markdown
Some text before the block.

    print("paragraph")

Some text after the block.
```

> **Explanation**: The word "paragraph" appears inside an indented code block (four
> leading spaces on the code line). Because `code_blocks` is `True`, the rule scans
> **both** fenced and indented code block content, so the rule triggers. This confirms
> that the `code_blocks` setting is not limited to fenced blocks.

### Correct Scenarios

This rule does not trigger when the proper name appears with the correct capitalization
as specified in the `names` configuration. Assuming `names` is set to `ParaGraph`,
then the following example will not trigger this rule:

```Markdown
this is a ParaGraph.
```

> **Explanation**: The word "ParaGraph" appears in the text. The configuration `names`
> expects "ParaGraph". Since the capitalization matches exactly, the rule does not
> trigger.

Unlike the prior example where the word exactly matched the configured proper name,
this case shows that a proper-name substring embedded inside a larger word does
not
count as a standalone occurrence and therefore does not trigger the rule.

```Markdown
this is a paragraphing
this is a reparagraph
```

> **Explanation**: The string "ParaGraph" is configured as a proper name. However,
> in this example, "paragraph" is part of the larger words "paragraphing" and "reparagraph".
> Since the rule only triggers on standalone instances of the word, and these are
> not standalone instances, the rule does not trigger.

Unlike the prior failure scenario that showed a match inside a fenced code block,
this case shows that the same content does not trigger the rule when code_blocks
is set to False, because the rule no longer scans code block content.

````Markdown
```Python
print("paragraph")
```
````

> **Explanation**: The word "paragraph" appears inside the fenced code block, but
> with `code_blocks` set to `False`, the rule does not scan fenced or indented code
> block content. Since the only occurrence is inside a code block, the rule does
> not trigger.

Unlike the prior failure scenario that showed a match inside an inline code span,
this case shows that the same content does not trigger the rule when `code_spans`
is set to `False`, because the rule no longer scans inline code span content.

```Markdown
Use the `paragraph` element here.
```

> **Explanation**: The word "paragraph" appears inside the inline code span, but
> with `code_spans` set to `False`, the rule does not scan inline code span content.
> Since the only occurrence is inside a code span, the rule does not trigger.

Unlike the prior scenarios that operated on visible Markdown body text, labels,
or code content, this case shows that a match inside a link URI does not trigger
the rule, since the rule explicitly excludes link URIs from its evaluation and only
considers the label and title portions of links.

```Markdown
this is a [ParaGraph](/paragraph "a proper name") link.
```

> **Explanation**: The word "paragraph" appears only in the link URI. The label
> (`ParaGraph`) is correctly capitalized, and the title (a proper name) does not
> contain the configured proper name. Since the rule explicitly excludes link URIs
> from its evaluation, the rule does not trigger.

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
