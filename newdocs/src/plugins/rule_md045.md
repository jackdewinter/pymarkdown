# Rule - MD045

| Property | Value |
| --- | -- |
| Aliases | `md045`, `no-alt-text` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Images should have alternate text (alt text).

## Reasoning

### Accessibility

All four types of the Image Markdown element transfer the text in the
label text part of the element into the `img` tag's `alt` parameter.
That parameter is used by screen
readers to render an audio description of that image to
sight impaired people.

## Examples

### Failure Scenarios

This rule triggers when the link label for an image has no characters or only
whitespace characters.  As the focus of this rule is to provide text to help
identify the image, the whitespace characters compared against are the set
of Unicode whitespace characters.

````Markdown
[](/url)

![][link]

[link]: /url "a title"```
````

Note that for the shortcut and collapsed types of image links, it is impossible
to create an example that triggers this rule.  For more information,
consult the [GitHub Flavored Markdown](https://github.github.com/gfm/#example-559)
specification.

### Correct Scenarios

This rule does not trigger if the link label for an image has
at least one non-whitespace character:

````Markdown
![link](/url)
````

## Fix Description

The reason for not being able to auto-fix this rule is context.  While it is easy
to detect that no alternate text has been provided for an image, the summation of
the indented content of the link exceeds the scope of the project's context.
Basically, any generated context would require scanning the destination link and
providing a summary of that image that was relevant to the current document.

## Configuration

| Prefixes |
| --- |
| `plugins.md045.` |
| `plugins.no-alt-text.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD045](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md045---images-should-have-alternate-text-alt-text).
