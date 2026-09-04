# Rule - MD026

| Property | Value |
| --- | --- |
| Aliases | `md026`, `no-trailing-punctuation` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Do not use trailing punctuation in heading text.

## Reasoning

### Readability

Headings serve as section titles, not complete sentences. Except for question marks (`?`), which are appropriate for question-style headings, trailing sentence-ending punctuation should be avoided to maintain readability and consistency.

## Examples

### Failure Scenarios

This rule triggers when a heading ends with a punctuation character that
makes it look like a sentence:

```Markdown
# This is a heading.
```

> **Explanation**: This heading ends with a period (`.`), which is one of the configured trailing punctuation characters. The rule triggers because trailing punctuation makes the heading look like a complete sentence rather than a section title.

Unlike the first scenario which used a period, this case uses an exclamation mark (`!`) as trailing punctuation.

```Markdown
# This is a cool heading!
```

> **Explanation**: This heading ends with an exclamation mark (`!`), which is one of the configured trailing punctuation characters. Unlike the first scenario which used a period, this example demonstrates that other sentence-ending punctuation like exclamation marks also trigger the rule.

Unlike the previous scenarios which used a period or exclamation mark, this heading ends with a trailing semicolon (`;`).

```Markdown
# This is a heading;
```

> **Explanation**: This heading ends with a semicolon (`;`), which is one of the configured trailing punctuation characters. The rule triggers because the semicolon serves no grammatical purpose at the end of a heading and makes it appear like an incomplete sentence.

Unlike the previous scenario which used a semicolon, this heading ends with a trailing colon (`:`).

```Markdown
# This is a heading:
```

> **Explanation**: This heading ends with a colon (`:`), which is one of the configured trailing punctuation characters. The rule triggers because a trailing colon suggests incomplete text and makes the heading look like a sentence fragment.

Unlike the previous scenarios which ended with periods, exclamation marks, semicolons, or colons, this heading ends with a trailing comma (`,`).

```Markdown
# This is a heading,
```

> **Explanation**: This heading ends with a comma (`,`), which is one of the configured trailing punctuation characters. The rule triggers because a trailing comma makes the heading appear like an incomplete sentence.

Unlike the previous scenarios which used ASCII punctuation, this heading ends with a full-width period (`。`), a CJK sentence-ending character.

```Markdown
# 这是一个标题。
```

> **Explanation**: This heading ends with a full-width period (`。`), which is one of the configured trailing punctuation characters. The rule triggers because full-width CJK punctuation is included in the default list of prohibited trailing punctuation, just like their ASCII counterparts.

### Correct Scenarios

This rule does not trigger when the heading does not end with one of the
configured punctuation characters.

```Markdown
# This is a heading
```

> **Explanation**: This heading does not end with any punctuation character. Therefore, the rule does not trigger.

Unlike the previous example, this case ends with a question mark, which is explicitly excluded from the list of prohibited trailing punctuation.

```Markdown
# Is this a heading?
```

> **Explanation**: This heading ends with a question mark (`?`), which is explicitly excluded from the list of prohibited trailing punctuation characters.

Unlike the previous example which tested question marks at the end, this heading contains a comma within the body of the heading text, not as trailing punctuation.

```Markdown
# This is a heading, isn't it?
```

> **Explanation**: This heading contains a comma in the middle of the text, but does not end with prohibited trailing punctuation. The question mark at the end is explicitly excluded from triggering the rule. Therefore, the rule does not trigger.

Unlike the previous scenario which tested commas within heading text, this heading contains quotation marks within the body of the text but does not end with prohibited trailing punctuation.

```Markdown
# Coining the term "mind flayer"
```

> **Explanation**: This heading contains quotation marks within the text, but does not end with any prohibited trailing punctuation characters. Since the heading ends with a closing quote followed by no sentence-ending punctuation, the rule does not trigger.

Unlike the previous example, this case uses semicolons as part of HTML entity references rather than as trailing punctuation.

```Markdown
# This is a heading &copy;
```

> **Explanation**: Although the semicolon (`;`) is in the default list of trailing punctuation characters, this heading uses a semicolon as part of an HTML entity reference (`&copy;`). The rule correctly identifies that this is not trailing punctuation and does not trigger.

## Fix Description

Auto-fixing this rule is not possible due to contextual ambiguity. 
Simply removing trailing punctuation could alter the author's intended meaning.
Without understanding the context and proper classification of each punctuation
mark, designing an algorithm that correctly handles all cases is not feasible.

## Configuration

| Prefixes |
| --- |
| `plugins.md026.` |
| `plugins.no-trailing-punctuation.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `punctuation` | `string` | `.,;:!。，；：！` | Punctuation characters that are considered sentence-ending characters. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD026](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md026---trailing-punctuation-in-heading)
and
[this article](https://cirosantilli.com/markdown-style-guide#punctuation-at-the-end-of-headers).

### Differences From MarkdownLint Rule

The main difference is that this rule also handles multi-line Setext heading elements, which the original MarkdownLint rule did not address.
