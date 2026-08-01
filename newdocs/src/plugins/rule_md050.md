# Rule - MD050

| Property | Value |
| --- | -- |
| Aliases | `md050`, `strong-style` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Strong emphasis style should be consistent throughout the document.

## Reasoning

### Readability

One of the main keys to readability is to have consistent formatting applied
throughout a group of documents.  Extending the concept even further,
organizations may have specific rules on how documents should be authored throughout
that organization.  It follows that both concepts may extend to specifying
which character sequence should be used for specifying the start of an inline strong
emphasis block in a Markdown document.

## Examples

### Failure Scenarios

This rule triggers when there is inconsistent use for inline strong emphasis blocks:

````Markdown
This is **one** emphasis.

This is the __another__ emphasis.
````

With default configuration settings, the `consistent` style is used.  This
style sets the current configuration type to either `asterisk` or `underscore`
based on the first inline strong emphasis block encountered in the document.

### Correct Scenarios

This rule does not trigger if the character sequence for inline strong emphasis
blocks is consistently specified within the document:

````Markdown
This is **one** emphasis.

This is the **same** emphasis.
````

Note that setting the `style` configuration value explicitly to `underscore`
will cause the above Markdown document to trigger this rule, while a
value of `asterisk` or `consistent` will not cause this rule to trigger.

## Fix Description

The fix for this rule is currently in queue.

## Configuration

| Prefixes |
| --- |
| `plugins.md050.` |
| `plugins.strong-style.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `style` | string (see below) | `consistent` | Style of inline strong emphasis block characters expected in the document. |

Valid styles:

| Style | Description |
| -- | -- |
| `consistent` | The first inline strong emphasis block in the document specifies the style for the rest of the document. |
| `asterisk` | Only asterisks are to be used for inline strong emphasis block elements. |
| `underscore` | Only underscores are to be used for inline strong emphasis block elements. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD050](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md050---strong-style).
