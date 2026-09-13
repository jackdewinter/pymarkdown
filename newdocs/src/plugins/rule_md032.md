# Rule - MD032

| Property | Value |
| --- | --- |
| Aliases | `md032`, `blanks-around-lists` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

List blocks must be surrounded by blank lines.

## Reasoning

### Readability

Separating list elements from surrounding content highlights their structure and
improves readability. Additionally, blank lines ensure that parsers consistently
recognize list boundaries.

## Examples

### Failure Scenarios

This rule triggers when a list is not prefaced by a blank line, causing it to be
adjacent to preceding text.

```Markdown
This is text.
+ a list
```

> **Explanation**: The list item `+ a list` immediately follows the paragraph
> `This is text.` without an intervening blank line. This violates the rule requirement
> that list blocks must be surrounded by blank lines to ensure distinct separation
> and proper parser recognition.

Unlike the previous example, this case shows a list that is not followed by a blank
line, appearing directly before a non-text block element.

```Markdown
1. a list
# This is any non-text block
```

> **Explanation**: The list item `1. a list` is immediately followed by a heading
> `# This is any non-text block` without an intervening blank line. The rule requires
> a blank line after the list to separate it from subsequent block elements.

Unlike the previous examples which involved text or headings adjacent to lists,
this case shows a list immediately following a heading without an intervening blank
line.

```Markdown
## Some Heading
+ some list
```

> **Explanation**: The list item `+ some list` immediately follows the heading
> `## Some Heading` without an intervening blank line. The rule requires a blank
> line after block elements (including headings) before a list begins to ensure
> proper separation and parser recognition.

Unlike the previous examples which show a list adjacent to a paragraph or heading,
this case shows a list immediately followed by a paragraph without an intervening
blank line.

```Markdown
+ a list
This is text.
```

> **Explanation**: The paragraph `This is text.` immediately follows the list item
> `+ a list` without an intervening blank line. The rule requires a blank line after
> a list block to separate it from subsequent paragraphs, just as it requires one
> before the list to separate it from preceding paragraphs.

### Correct Scenarios

This rule does not trigger when a list is properly surrounded by blank lines on
both sides, which is the expected base case.

```Markdown
This is text and a blank line.

+ a list

This is a blank line and some text.
```

> **Explanation**: The list item `+ a list` is separated from the preceding paragraph
> and the following paragraph by single blank lines. This satisfies the rule's requirement
> for lists to be surrounded by blank lines.

Unlike the previous example, this scenario demonstrates that a list at the very
beginning of a document does not require a preceding blank line.

```Markdown
+ a list at the start

text
```

> **Explanation**: The list is at the start of the document, so no preceding blank
> line is possible or required by the rule. Since the GFM parser recognizes it as
> the first block element, the rule does not trigger.

Unlike the previous example where the list is at the start of the document, this
scenario shows a list at the very end of a document, where no following content
exists to require a trailing blank line.

```Markdown
This is text and a blank line.

+ a list
```

> **Explanation**: The list is the final block element in the document. Because
> there is no following block element, no trailing blank line is required. The preceding
> blank line already separates the list from the prior paragraph, satisfying the
> rule's requirement that lists be surrounded by blank lines where adjacent blocks
> exist.

Unlike lists at the document start, this scenario shows a list nested within another
list.

```Markdown
- nested list
  - item inside
```

> **Explanation**: The second list item `- item inside` is parsed as a *child* of
> the first list item (a nested list), so it is part of the same list block rather
> than a separate top-level list. Because the rule only requires blank lines around
> distinct top-level list blocks, no blank line is needed between the parent and
> child items.

Unlike standard lists, this scenario shows a list directly within a block quote
element.

```Markdown
> + a list in a quote
```

> **Explanation**: A list inside a block quote is contained within the quote block.
> The rule applies to the outer block (the block quote), not to internal lists,
> so the rule does not trigger.

Unlike previous structural examples, this scenario involves "Lazy Continuation Lines"
as defined in the GFM specification.

```Markdown
This is text and a blank line.

+ a list
This is some text.
```

> **Explanation**: Due to Lazy Continuation Lines, the fourth line
> (`This is some text.`) is parsed as part of the list item started on line three.
> Since it is part of the same list item, no blank line is required between them.
> The rule does not trigger because the list block is effectively followed by nothing
> (end of document or next block) after the continuation is resolved.

Unlike lazy continuation text, this scenario demonstrates that indented text following
a list item may be parsed as a continuation of the list item rather than an indented
code block.

```Markdown
This is text and a blank line.

+ a list
    This is some text.
```

> **Explanation**: Parsers often interpret the indented text on line four as a continuation
> of the list item on line three, potentially with extra indentation. Because it
> is treated as part of the list item, the rule does not trigger for a missing blank
> line after the list.

Unlike simple continuations, this scenario shows a list followed by a link reference
definition with a blank line, which is clearly separate.

```Markdown
+ a list

[lrd]:
/url
```

> **Explanation**: This is a list element followed by a link reference definition
> with a blank line between them. The list is properly terminated by the blank line,
> so the rule does not trigger.

Unlike the previous example with a blank line, this scenario shows a list immediately
followed by a link reference definition without a blank line, which parsers may
treat as ambiguous or part of the list.

```Markdown
+ a list
[lrd]:
/url
```

> **Explanation**: Without a blank line, the GFM specification's lenient list parsing
> treats the link reference definition (`[lrd]:` / `/url`) as continuation of the
> list item rather than as a separate block element. Since no distinct block element
> follows the list, the rule does not trigger.

Unlike the previous LRD example, this scenario shows a list immediately followed
by a fenced code block with no intervening blank line.

````Markdown
+ a list
```python
print("hello")
```
````

> **Explanation**: Because a fenced code block that directly follows a list item
> (without a blank line) is parsed as part of the list item's lazy continuation,
> no distinct block element follows the list at the parser level. The rule therefore
> does not trigger, since there is no adjacent top-level block element requiring
> separation by a blank line.

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
