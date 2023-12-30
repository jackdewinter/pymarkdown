# Rule - MD045

| Aliases |
| --- |
| `md045` |
| `no-alt-text` |

| Autofix Available |
| --- |
| No |

## Summary

Images should have alternate text (alt text).

## Reasoning

### Accessibility

The label text part
of all four types of Image element is translated in HTML to the `alt`
parameter of the `img` tag.  That parameter is often used by screen
readers to render an auto description of what that image is to
sight impaired people.

## Examples

### Failure Scenarios

This rule triggers when the link label for an image has no characters or only
whitespace characters:

````Markdown
[](/url)

![][link]

[link]: /url "a title"```
````

Note that for shortcut and collapsed types of image links, it is impossible
to create an example that triggers this rule.  For more information,
consult the [GitHub Flavored Markdown](https://github.github.com/gfm/#example-559)
specification.

### Correct Scenarios

This rule does not trigger if the link label for an image has
at least one non-whitespace character:

````Markdown
![link](/url)
````

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

## Fix Description

The reason for not being able to auto-fix this rule is context.  While it is easy
to detect that no alternate text has been provided for an image, the summation of
the indented content of the link exceeds the scope of the project's context.
Basically, any generated context would require scanning the destination link and
providing a summary of that image that was relevant to the current document.
