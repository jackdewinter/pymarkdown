# Rule - MD032

| Property | Value |
| --- | --- |
| Aliases | `md032`, `blanks-around-lists` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

List blocks should be surrounded by blank lines.

## Reasoning

### Readability

Separating list elements from surrounding content highlights their structure and improves readability. Additionally, blank lines ensure that parsers consistently recognize list boundaries.

## Examples

### Failure Scenarios

This rule triggers when a list is not prefaced by a blank line, causing it to be adjacent to preceding text.

```Markdown
This is text.
+ a list
```

> **Explanation**: The list item `+ a list` immediately follows the paragraph `This is text.` without an intervening blank line. This violates the rule requirement that list blocks must be surrounded by blank lines to ensure distinct separation and proper parser recognition.

Unlike the previous example, this case shows a list that is not followed by a blank line, appearing directly before a non-text block element.

```Markdown
1. a list
# This is any non-text block
```

> **Explanation**: The list item `1. a list` is immediately followed by a heading `# This is any non-text block` without an intervening blank line. The rule requires a blank line after the list to separate it from subsequent block elements.

Unlike the previous examples which involved text or headings adjacent to lists, this case shows a list immediately following a heading without an intervening blank line.

```Markdown
## Some Heading
+ some list
```

> **Explanation**: The list item `+ some list` immediately follows the heading `## Some Heading` without an intervening blank line. The rule requires a blank line after block elements (including headings) before a list begins to ensure proper separation and parser recognition.

### Correct Scenarios

This rule does not trigger when a list is properly surrounded by blank lines on both sides.

```Markdown
This is text and a blank line.

+ a list

This is a blank line and some text.
```

> **Explanation**: The list item `+ a list` is separated from the preceding paragraph and the following paragraph by single blank lines. This satisfies the rule's requirement for lists to be surrounded by blank lines.

Unlike the previous example which showed separated lists, this scenario demonstrates that lists at the very beginning or end of a document, or lists nested within other lists, do not require surrounding blank lines in the same way.

```Markdown
+ a list at the start

text
```

> **Explanation**: The list is at the start of the document, so no preceding blank line is possible or required. The rule does not trigger for this valid structural position.

Unlike lists at the document start, this scenario shows a list nested within another list.

```Markdown
- nested list
  - item inside
```

> **Explanation**: The nested list is part of the parent list structure, so the blank line requirement applies to the parent list block as a whole, not internal nesting. The rule does not trigger for this valid structural position.

Unlike standard lists, this scenario shows a list directly within a block quote element.

```Markdown
> + a list in a quote
```

> **Explanation**: A list inside a block quote is contained within the quote element. The blank line requirement applies to the block quote as a whole, not to the internal list. Since the list is properly contained, the rule does not trigger.

Unlike previous structural examples, this scenario involves "Lazy Continuation Lines" as defined in the GFM specification.

```Markdown
This is text and a blank line.

+ a list
This is some text.
```

> **Explanation**: Due to Lazy Continuation Lines, the fourth line (`This is some text.`) is parsed as part of the list item started on line three. Since it is part of the same list item, no blank line is required between them. The rule does not trigger because the list block is effectively followed by nothing (end of document or next block) after the continuation is resolved.

Unlike lazy continuation text, this scenario demonstrates that indented text following a list item may be parsed as a continuation of the list item rather than an indented code block.

```Markdown
This is text and a blank line.

+ a list
    This is some text.
```

> **Explanation**: Parsers often interpret the indented text on line four as a continuation of the list item on line three, potentially with extra indentation. Because it is treated as part of the list item, the rule does not trigger for a missing blank line after the list.

Unlike simple continuations, this scenario shows a list followed by a link reference definition with a blank line, which is clearly separate.

```Markdown
+ a list

[lrd]:
/url
```

> **Explanation**: This is a list element followed by a link reference definition with a blank line between them. The list is properly terminated by the blank line, so the rule does not trigger.

Unlike the previous example with a blank line, this scenario shows a list immediately followed by a link reference definition without a blank line, which parsers may treat as ambiguous or part of the list.

```Markdown
+ a list
[lrd]:
/url
```

> **Explanation**: Without a blank line, the parser may treat the link reference definition as part of the list item due to parsing ambiguity. Because the lines are grouped into a single list item, there is no separate block element after the list, so the rule does not trigger.

## Fix Description

The implementation for this feature is tracked [with this issue](https://github.com/jackdewinter/pymarkdown/issues/819).

## Configuration

| Prefixes |
| --- |
| `plugins.md032.` |
| `plugins.blanks-around-lists.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD032](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md032---lists-should-be-surrounded-by-blank-lines).
