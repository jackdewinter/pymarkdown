# Rule - MD059

| Property | Value |
| --- | -- |
| Aliases | `md059`, `descriptive-link-text` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Link text should be descriptive.

## Reasoning

### Correctness

There are certain words and phrases that are attached to links as placeholders
for more descriptive phrases. The most common of these placeholders are the
phrases `click here`, `here`, `link`, and `more`.  This rule treats these
phrases as placeholders that were left in the Markdown document, to be replaced.

## Examples

### Failure Scenarios

This rule triggers when the text associated with a link contains any of the
specified placeholders.

````Markdown
To read more, [click here](#some-section).
Go to [here](#some-section).
Go to this [link][some-link].
Go here for [more][] information.
Go here for [more] information.

[some-link]: /url
[more]: /url
````

Note that when the text for the link is interpretted, any spaces are stripped
from the start and end of the link text, multiple spaces are replaced with a
single space, and the link text is shifted to lower case.

That means each of the following examples will trigger this rule:

````Markdown
To read more, [Click Here](#some-section).
To read more, [ Click  Here ](#some-section).
````

### Correct Scenarios

This rule does not trigger when the interpretted link text is not one of
the above phrases, such as:

````Markdown
Go to [this section](#some-section).
````

The list of prohibited phrases are:

- `click here`
- `here`
- `link`
- `more`

and are controlled by the `prohibited-phrases` configuration item. The value
for this configuration item is a comma-separated string that defaults to the
representation for the above list. Note that if a new value for the `prohibited-phrases`
configuration item is used, it replaces all of the above values with its contents.

## Fix Description

The reason for not being able to auto-fix this rule is certainty.

## Configuration

| Prefixes |
| --- |
| `plugins.md059.` |
| `plugins.prohibited-phrases.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `prohibited-phrases` | `str` | `"click here,here,link,more"` | Comma-separated list of phrases that are prohibited. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD059](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md059---link-text-should-be-descriptive).
