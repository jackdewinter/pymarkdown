# Rule - MD049

| Property | Value |
| --- | -- |
| Aliases | `md049`, `emphasis-style` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Emphasis style should be consistent throughout the document.

## Reasoning

### Readability

One of the main keys to readability is to have consistent formatting applied
throughout a group of documents.  Extending the concept even further,
organizations may have specific rules on how documents should be authored throughout
that organization.  It follows that both concepts may extend to specifying
which character sequence should be used for specifying the start of an inline emphasis
block in a Markdown document.

## Examples

### Failure Scenarios

This rule triggers when there is inconsistent use for inline emphasis blocks:

````Markdown
This is *one* emphasis.

This is the _another_ emphasis.
````

With default configuration settings, the `consistent` style is used.  This
style sets the current configuration type to either `asterisk` or `underscore`
based on the first inline emphasis block encountered in the document.

### Correct Scenarios

This rule does not trigger if the character sequence for emphasis blocks is
consistently specified within the document:

````Markdown
This is *one* emphasis.

This is the *same* emphasis.
````

Note that setting the `style` configuration value explicitly to `underscore`
will cause the above Markdown document to trigger this rule, while a
value of `asterisk` or `consistent` will not cause this rule to trigger.

## Fix Description

The fix for this rule is currently in queue.

## Configuration

| Prefixes |
| --- |
| `plugins.md049.` |
| `plugins.emphasis-style.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `style` | string (see below) | `consistent` | Style of emphasis block characters expected in the document. |

Valid styles:

| Style | Description |
| -- | -- |
| `consistent` | The first emphasis block in the document specifies the style for the rest of the document. |
| `asterisk` | Only asterisks are to be used for inline emphasis block elements. |
| `underscore` | Only underscores are to be used for inline emphasis block elements. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD049](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md049---emphasis-style).
