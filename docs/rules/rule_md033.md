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
| `allowed_elements` | `string` | `!--,![CDATA[,?` | Comma separated list of tag starts that are allowable. |
| `allow_first_image_element` | `boolean` | `True` | Whether to allow an image HTML block. |

To be clear, if using the `allowed_elements` configuration value, the supplied
value is a comma separated list of allowable element sequences.  Those
element names are derived by taking the start of the tag and skipping
over the start character `<`.
From that point, the parser collects the contents of the tag up to one of the
following:

- the first whitespace character
- the close HTML tag character (`/`)
- the end HTML tag character (`>`)

As tags either require a whitespace character, the end character, or
the closing characters, this supplies a straightforward way to represent each HTML
tag.  The only exceptions to this is when the rule encounters the
[CDATA](https://github.github.com/gfm/#cdata-section)
character sequence `![CDATA[` right after the start HTML tag character (`<`) or
the HTML comment sequence `!--`.
Because those sequences do not require any whitespace to follow it, they are managed
separately.

### Allowing For Image Headings

Looking at numerous GitHub project pages, there are a significant number of more established
projects that use an HTML Image for their initial heading.  This is already supported
through Rule Md041 which allows an `h1` tag at the very start of the document to satisfy
the requirements for the document starting with a level 1 Heading element:

```Markdown
<h1 align="center"><img src="/path/to/image"/></h1>
```

To round out that support in this rule, the `allow_first_image_element` was added
to provide an exception to the normal `allowed_elements` configuration value.  This
exception is specifically for the very first element in the document, and only
triggers if that HTML Block element starts and ends with a `h1` tag, with only an `img`
tag between them.

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
HTML start conditions, the
`allowed_elements` configuration default value is set to `!--,![CDATA[,?` to allow
for common HTML tags to not trigger this rule by default.

To provide better support for the "image as a heading" scenario, the
`allow_first_image_element` configuration value was added to specifically
allow that scenario to not trigger this rule.
