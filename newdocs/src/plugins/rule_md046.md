# Rule - MD046

| Property | Value |
| --- | -- |
| Aliases | `md046`, `code-block-style` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Code block style.

## Reasoning

### Readability

One of the main keys to readability is to have consistent formatting applied
throughout a group of documents. It therefore follows that setting consistent
guidelines for code block usage within a document or within an organization
will enhance the readability of any such Markdown documents.

## Examples

### Failure Scenarios

This rule triggers when there is inconsistent use of code block elements within
the same document:

````Markdown
```Python
a=b
```

    indented
````

With default configuration settings, the `consistent` style is used.  This
style sets the current configuration type to either `indented` or `fenced`
based on the first code block encountered in the document.

### Correct Scenarios

This rule does not trigger if the code blocks are consistently specified
within the document:

````Markdown
```Python
a=b
```

```Python
b=c
```
````

Note that setting the `style` configuration item value to `indented`
will cause the above Markdown document to trigger this rule, while a
value of `fenced` or `consistent` will not cause this rule to trigger.

## Fix Description

Setting the `style` configuration item value to either `indented`
or `fenced` will cause all code blocks to be transformed into the specified
value.  If set to `consistent`, the first code block in the document will
set the style for the rest of the document.

Note that the translation from fenced-to-indented code block and the
translation from indented-to-fenced code block have their issues.

- For both translations, any whitespace before the code block is removed during
  the transition.
- When translating to a fenced code block, there is no guaranteed way to properly
  set the language for the fenced code block.  As such, it is left blank and will
  cause Rule Md040 to be triggered when next scanned.
- When translating to an indented code block, there are parsing issues with an
  indented code block that immediately follows a paragraph.  As indented code blocks
  cannot interrupt a paragraph block, an extra blank line is inserted between the
  paragraph and the new indented code block to allow the indented code block to
  be properly recognized.

## Configuration

| Prefixes |
| --- |
| `plugins.md046.` |
| `plugins.code-block-style.` |

<!--- pyml disable-num-lines 4 line-length-->
| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `style` | string (see below) | `consistent` | Style of code blocks expected in the document. |

Valid heading styles:

<!--- pyml disable-num-lines 5 line-length-->
| Style | Description |
| -- | -- |
| `consistent` | The first heading in the document specifies the style for the rest of the document. |
| `fenced` | Only fenced code blocks are to be used. |
| `indented` | Only indented code blocks are to be used. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD046](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md046---code-block-style).
