# Rule - MD045

| Property | Value |
| --- | --- |
| Aliases | `md045`, `no-alt-text` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Images should have alternate text (alt text).

## Reasoning

### Accessibility

The `alt` attribute of an image is used by screen readers to provide an audio description of the image to people with visual impairments. Without meaningful alt text, these users cannot understand the content or purpose of the image.

Note that for the shortcut and collapsed types of image links, it is impossible
to create an example that triggers this rule. For more information,
consult the [GitHub Flavored Markdown](https://github.github.com/gfm/#example-559)
specification.

## Examples

### Failure Scenarios

This rule triggers when the link label for an image has no characters or only
whitespace characters. As the focus of this rule is to provide text to help
identify the image, the whitespace characters compared against are the set
of Unicode whitespace characters.

```Markdown
[](/url)

![][link]

[link]: /url "a title"
```

> **Explanation**: The above examples show image links where the alternate text (alt text) is either completely empty (`[](/url)`) or referenced via a link definition that provides no alt text (`![][link]`). In both cases, the `alt` attribute in the resulting HTML will be empty, violating the rule that images must have descriptive alt text for accessibility.

Unlike the first example, this case shows two link labels containing only whitespace characters before the link reference.

```Markdown
[  ][link]

[
][link]
```

> **Explanation**: The alt text consists only of whitespace characters. Since the rule requires at least one non-whitespace character for meaningful alt text, this example fails the accessibility criterion. Screen readers may interpret this as empty alt text, failing to convey the image's purpose to users with visual impairments.

### Correct Scenarios

This rule does not trigger when the link label for an image has
at least one non-whitespace character:

```Markdown
![link](/url)
```

> **Explanation**: This example demonstrates an image link with valid alternate text (`link`). Since the alt text contains non-whitespace characters, it satisfies the rule's requirement for descriptive image text, ensuring that screen readers can convey meaningful information to users with visual impairments.

Unlike the previous minimal example, this scenario demonstrates real-world descriptive alt text for common images, showing how meaningful descriptions enhance accessibility.

```Markdown
![A cat sitting on a mat.](/cat.jpg)

![Cover of the book "C++ & Python Examples".](/book-examples.jpg)
```

> **Explanation**: These examples demonstrate proper alt text that provides meaningful descriptions of the images. The alt text clearly identifies the content ("A cat sitting on a mat" and "Cover of the book..."), enabling screen readers to convey specific information to users with visual impairments. This satisfies the rule's requirement for descriptive, non-empty alt text.

Unlike the previous descriptive examples, this scenario demonstrates a valid reference-style image link with meaningful alt text.

```Markdown
![A diagram of the system architecture.][arch-diagram]

[arch-diagram]: /images/arch.png
```

> **Explanation**: This example shows a reference-style image link with descriptive alt text ("A diagram of the system architecture."). The alt text is non-empty and meaningful, satisfying the rule. This mirrors the failure case for reference images, demonstrating the correct usage.

## Fix Description

The reason for not being able to auto-fix this rule is context. While it is easy
to detect that no alternate text has been provided for an image, the summarization of
the intended content of the link exceeds the scope of the project's context.
Any generated context would require scanning the destination link and
providing a summary of that image that was relevant to the current document.

## Configuration

| Prefixes |
| --- |
| `plugins.md045.` |
| `plugins.no-alt-text.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD045](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md045---images-should-have-alternate-text-alt-text).
