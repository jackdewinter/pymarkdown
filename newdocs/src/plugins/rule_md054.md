# Rule - MD054

| Property | Value |
| --- | -- |
| Aliases | `md054`, `link-image-style` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Link and image style.

## Reasoning

### Consistency

Whether it is within a single document or across multiple documents in a repository,
the style of those documents matter. Depending on you team

Consistent formatting makes it easier to understand a document. Autolinks are concise,
but appear as URLs which can be long and confusing. Inline links and images can
include descriptive text, but take up more space in Markdown form. Reference links
and images can be easier to read and manipulate in Markdown form, but require a
separate link reference definition.

## Examples

### Scenarios

This rule triggers whenever a link type is turned off and that link or image type
is encountered in the document. By default, all link types are enabled, and it is
only through configuration that they can be turned off. Normally, we would present
a section on failed scenarios and correct scenarios, outlining what Markdown
triggers each rule and what an acceptable form of that Markdown is.

However,
since the only difference is configuration, we will present this table instead.
As noted above, without any configuration changes, each of the configuration items
listed below defaults to `True`, and the Markdown specified in the "Example Markdown"
column **will not** trigger the rule.  However, if the configuration item's value
is
changed to `False`, the Markdown specified in the "Example Markdown"
column **will** trigger the rule.

<!-- pyml disable-num-lines 8 no-inline-html-->
| Configuration Item Name | Example Markdown |
| -- | -- |
| `autolinks` | `<https://example.com>`<br>`<someone@somewhere.com>` |
| `inline-links` | `[link](https://example.com)`<br>`![image](https://example.com)` |
| `full-links` | `[link][url]`<br>`![image][url]`|
| `collapsed-links` | `[url][]`<br>`![url][]` |
| `shortcut-links` | `[url]`<br>`![url]` |
| `inline-urls` | `[https://example.com](https://example.com)`<br>`![https://example.com](https://example.com)` |

For experienced users of Markdown, the only scenario above that needs explaining
is the `inline-urls` example. As a shortcut when writing documents, some users will
use this as a "to-do" item, setting the link label and link url to the same value
to remind them to come up with a decent name for the link. This explicitly checks
for the link text and the link URL to have the same value, without any link title
being present.

## Fix Description

The reason for not being able to auto-fix this rule is that it is unclear what one
of the link formats should be changed to if it is not enabled.

## Configuration

| Prefixes |
| --- |
| `plugins.md054.` |
| `plugins.link-image-style.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `autolinks` | `boolean` | `True` | Whether autolinks are allowed. |
| `inline-links` | `boolean` | `True` | Whether inline links and images are allowed. |
| `full-links` | `boolean` | `True` | Whether full links and images are allowed. |
| `collapsed-links` | `boolean` | `True` | Whether collapsed links and images are allowed. |
| `shortcut-links` | `boolean` | `True` | Whether shortcut links and images are allowed. |
| `inline-urls` | `boolean` | `True` | Whether inline URL for links and image are allowed. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD054](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md054---link-and-image-style).
