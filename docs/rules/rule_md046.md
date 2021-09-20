# Rule - MD046

| Aliases |
| --- |
| `md046` |
| `code-block-style` |

## Summary

Images should have alternate text (alt text).

## Reasoning

### Readability

One of the main keys to readability is to have consistent formatting applied
throughout a group of documents.  Extending the concept even further,
organizations may have specific rules on how documents should be authored throughout
that organization.  It follows that both concepts may extend to specifying
which element should be used for specifying code blocks in a Markdown document.

## Examples

### Failure Scenarios

This rule triggers when there is inconsistent use of code block elements within
the document:

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

Note that setting the `style` configuration value explicitly to `indented`
will cause the above Markdown document to trigger this rule, while a
value of `fenced` or `consistent` will not cause this rule to trigger.

## Configuration

| Prefixes |
| --- |
| `plugins.md046.` |
| `plugins.code-block-style.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `style` | string (see below) | `consistent` | Style of code blocks expected in the document. |

Valid heading styles:

| Style | Description |
| -- | -- |
| `consistent` | The first heading in the document specifies the style for the rest of the document. |
| `fenced` | Only fenced code blocks are to be used. |
| `indented` | Only indented code blocks are to be used. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD046](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md046---code-block-style).
