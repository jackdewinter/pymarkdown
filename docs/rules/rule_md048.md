# # Rule - MD048

| Aliases |
| --- |
| `md048` |
| `code-fence-style` |

## Summary

Images should have alternate text (alt text).

## Reasoning

One of the main keys to readability is to have consistent formatting applied
throughout a group of documents.  Extending the concept even further, many
organizations have specific rules on how documents should be authored throughout
that organization.  It follows that both concepts may extend to specifying
which element should be used for specifying the fence character for fenced
code blocks in a Markdown document.

## Examples

### Failure Scenarios

This rule triggers when there is inconsistent use of fence characters for
Fenced Code Blocks:

````Markdown
```Python
a=b
```

~~~Python
a=b
~~~
````

With default configuration settings, the `consistent` style is used.  This
style sets the current configuration type to either `tilde` or `backticks`
based on the first fenced code block encountered in the document.

### Correct Scenarios

This rule does not trigger if the fence character for Fenced Code Blocks are
consistently specified within the document:

````Markdown
```Python
a=b
```

```Python
b=c
```
````

Note that setting the `style` configuration value explicitly to `tilde`
will cause the above Markdown document to trigger this rule, while a
value of `backtick` or `consistent` will not cause this rule to trigger.

## Configuration

| Prefixes |
| --- |
| `plugins.md048.` |
| `plugins.code-fence-style.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled by default. |
| `style` | string (see below) | `"consistent"` | Style of fenced code block fence characters expected in the document. |

Valid heading styles:

| Style | Description |
| -- | -- |
| `"consistent"` | The first heading in the document specifies the style for the rest of the document. |
| `"backtick"` | Only backticks are to be used for Fenced Code Block elements. |
| `"indented"` | Only tildes are to be used for Fenced Code Block elements. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD048](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md048---code-fence-style).
