# Rule - MD031

| Property | Value |
| --- | --- |
| Aliases | `md031`, `blanks-around-fences` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

Fenced code blocks should be surrounded by blank lines.

## Reasoning

### Readability

By separating fenced code blocks from surrounding content, their presence in a document is more easily visible to human readers. Additionally, some Markdown parsers require blank lines before and after fenced code blocks to properly recognize them.

## Examples

### Failure Scenarios

This rule triggers when the Fenced Code Block element is not prefaced with a blank line.

````Markdown
This is text.
```block
A code block
```

This is a blank line and some text.
````

> **Explanation**: The Fenced Code Block immediately follows "This is text." without an intervening blank line. The rule requires a blank line before any Fenced Code Block to ensure readability and parser compatibility.

Unlike the previous example, this case shows a Fenced Code Block not followed by a blank line.

````Markdown
This is text and a blank line.

```block
A code block
```
This is some text.
````

> **Explanation**: The Fenced Code Block is immediately followed by "This is some text." without an intervening blank line. The rule requires a blank line after any Fenced Code Block to ensure readability and parser compatibility.

### Correct Scenarios

This rule does not trigger when there is a single
Blank Line both before and after the Fenced Code Block
element:

````Markdown
This is some text.

```block
A code block
```

This is some text.
````

> **Explanation**: This rule does not trigger because the Fenced Code Block is properly surrounded by blank lines, satisfying the requirement for readability and parser compatibility.

This rule does not trigger when the Fenced Code Block appears at the very start of the document, as there is no preceding content that requires separation.

````Markdown
```block
A code block
```

This is some text.
````

> **Explanation**: This rule does not trigger because the Fenced Code Block is at the start of the document. There is no preceding content, so a blank line before the code block is not required. A blank line follows the code block, separating it from the subsequent text.

Unlike the previous example, this case shows a Fenced Code Block at the very end of the document.

````Markdown
This is some text.

```block
A code block
```
````

> **Explanation**: This rule does not trigger because the Fenced Code Block is at the end of the document. There is no following content, so a blank line after the code block is not required. A blank line precedes the code block, separating it from the preceding text.

Unlike the previous examples, this case shows a Fenced Code Block nested within a blockquote.

````Markdown
> ```block
> A code block
> ```
>
> This is some text.
````

> **Explanation**: This rule does not trigger because the Fenced Code Block is within a blockquote. The blank lines before and after the code block (within the blockquote context) satisfy the requirement for separation. The rule evaluates content within blockquotes independently.

Unlike the previous example which used a blockquote, this case shows a Fenced Code Block nested within a list item.

````Markdown
+ ```block
  A code block
  ```

  This is some text.
````

> **Explanation**: This rule does not trigger because the Fenced Code Block is within a list item. The blank lines before and after the code block (within the list item context) satisfy the requirement for separation. By default, the rule checks for proper spacing within list items.

Unlike the previous example, this case demonstrates a [loose list item](https://github.github.com/gfm/#loose) where the `list_items` configuration is set to `False`, disabling the rule within list items.

````Markdown
- This is an item
  ```block
  A code block
  ```
  Still the same item, and loose.
````

> **Explanation**: This rule does not trigger because the `list_items` configuration value is set to `False`. When this configuration is disabled, the rule does not check for blank lines around Fenced Code Blocks within list items, allowing tight formatting within loose list items.

## Fix Description

The implementation for this feature is tracked [with this issue](https://github.com/jackdewinter/pymarkdown/issues/818).

## Configuration

| Prefixes |
| --- |
| `plugins.md031.` |
| `plugins.blanks-around-fences.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `list_items` | `boolean` | `True` | Whether this Rule Plugin triggers directly within a list item. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD031](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md031---fenced-code-blocks-should-be-surrounded-by-blank-lines).
