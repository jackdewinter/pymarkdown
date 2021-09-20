# Rule - MD033

| Aliases |
| --- |
| `md033` |
| `no-inline-html` |

## Summary

Inline HTML.

## Reasoning

### Portability

The primary reason for enabling this rule is to force the document
writer to not use any HTML elements, or only a small subset of HTML
elements,  in their documents.  The two main reasons for this are:

- for specific reasons, such as security, where allowing HTML to be added to a document is not desirable
- for use with Markdown parsers that render their output as something other than HTML

## Examples

### Failure Scenarios

This rule triggers if either a HTML block or an inline Raw HTML element is detected.

```Markdown
This is <i>Raw</i> HTML.

<image src="/foo.jpg">
```

### Correct Scenarios

This rule only triggers on HTML elements that are present and not on the
`allowed_elements` list.  Therefore, one solution to correct the above
example is to express both concepts as Markdown elements instead of HTML
elements:

```Markdown
This is *Raw* HTML.

![](/foo.jpg)
```

Depending on the reasons for enabling this rule, the other approach is
to add any required elements to the `allowed_elements` list.  Added
through configuration, setting the `allowed_elements` to `image,i` will
also suppress the triggering of this rule.
However, as this rule is generally used for a sincere and overwhelming
reason to not allow inline HTML, the use of this approach for any other
image tags than the default `!--` (HTML comment) are strongly discouraged.

## Configuration

| Prefixes |
| --- |
| `plugins.md033.` |
| `plugins.no-inline-html.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `allowed_elements` | `string` | `!--` | Comma separated list of tag starts that are allowable. |

To be clear, if using the `allowed_elements` configuration value, the supplied
value is a comma separated list of allowable element sequences.  Those
element names are derived by taking the start of the tag and skipping
over the start character `<` or the start and close characters `</`.
From that point, the parser collects the contents of the tag up to one of the
following:

- the first whitespace character
- the close HTML tag character (`/`)
- the end HTML tag character (`>`)

As tags either require a whitespace character, the end character, or
the closing characters, this supplies a straightforward way to represent each HTML
tag.  The only exception to this is when the rule encounters the
[CDATA](https://github.github.com/gfm/#cdata-section)
character sequence `![CDATA[` right after the start HTML tag character (`<`).
Because that sequence does not require any whitespace to follow it, it is managed
separately.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD033](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md033---inline-html).

### Differences From MarkdownLint Rule

The substantial difference from the original rule is that the original rule only
triggers if an alphabetic character followed the starting `<` character. While
that worked in most cases, it precluded the detection of
[HTML start conditions](https://github.github.com/gfm/#html-blocks)
number 2 to number 5 and the closing tag case for number 7.

In creating this rule to work with all HTML tags, including the missing
HTML start conditions and the close HTML tag character (`/`), the
`allowed_elements` configuration default value is set to `!--` to allow
for HTML comment tags to not trigger this rule by default.
