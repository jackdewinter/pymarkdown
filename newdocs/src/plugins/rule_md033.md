# Rule - MD033

| Property | Value |
| --- | --- |
| Aliases | `md033`, `no-inline-html` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Avoid using inline HTML elements in Markdown documents.

## Reasoning

### Portability

This rule encourages authors to avoid inline HTML elements to improve:

- **Security**: preventing injection vulnerabilities and rendering pipeline issues in applications that restrict arbitrary HTML
- **Portability**: ensuring compatibility with Markdown parsers that target non-HTML outputs (e.g., PDF, plain text, or reStructuredText), where inline HTML may not render correctly for end readers

## Examples

### Failure Scenarios

This rule triggers when an inline HTML element or an HTML block is present in the document.

```Markdown
This is <b>bold</b> text.
```

> **Explanation**: The example contains an inline `<b>` HTML element which is raw HTML not allowed by this rule. The rule detects any HTML elements that are not on the `allowed_elements` list.

Unlike the previous example, this case demonstrates self-closing HTML tags, which are also detected by this rule even though they do not have a separate closing tag.

```Markdown
Add a line break<br/>here.
And an image<img src="/logo.png"/>here too.
```

> **Explanation**: The example contains self-closing HTML elements (`<br/>` and `<img>`). The rule detects these because `br` and `img` are not on the default `allowed_elements` list (`!--,![CDATA[,!DOCTYPE`). Any HTML tag not explicitly allowed will trigger this rule, regardless of whether it is self-closing or uses a separate closing tag.

Unlike the previous examples, this case demonstrates HTML blocks as defined by [GFM HTML block rules](https://github.github.com/gfm/#html-blocks), specifically cases 2–5 (e.g., blocks starting with `<script`, `<style`, `<pre`, or comment-style blocks) and closing tag case 7. These are multi-line HTML structures that span multiple lines and are not merely inline elements.

```Markdown
<script>alert('test');</script>

<style>
  body { color: red; }
</style>

<div>
This is a div block.
</div>
```

> **Explanation**: The example contains HTML blocks: a `<script>` block, a `<style>` block, and a `<div>` block. These trigger the rule because `script`, `style`, and `div` are not on the default `allowed_elements` list. This demonstrates that the rule detects not only inline HTML but also multi-line HTML blocks, including GFM HTML block cases 2–5 and closing tag case 7, which were not detected by the original MarkdownLint rule.

Unlike the previous examples, this case demonstrates HTML tags that include attributes, such as inline styles or class names. The presence of attributes does not prevent the rule from detecting the element.

```Markdown
<span style="color: red;">This text is red.</span>

<div class="container">This is a styled div.</div>
```

> **Explanation**: The example contains HTML elements with attributes: a `<span>` with an inline `style` attribute and a `<div>` with a `class` attribute. The rule detects these because `span` and `div` are not on the default `allowed_elements` list. Adding attributes to an HTML tag does not exempt it from triggering the rule; any HTML tag not explicitly allowed will be flagged regardless of whether it contains attributes.

Unlike the previous examples, this case demonstrates an HTML comment that triggers the rule when it is removed from the `allowed_elements` configuration. By default, `!--` is in the allowed list, but if a user explicitly clears or restricts `allowed_elements`, comments will also be flagged.

```Markdown
<!-- This is an HTML comment -->

Normal text follows.
```

> **Explanation**: The example contains an HTML comment (`<!-- -->`). If the `allowed_elements` configuration does not include `!--`, this comment will trigger the rule because the sequence `!--` is treated as an HTML element start. By default, `!--` is included in `allowed_elements`, so comments do not trigger the rule. However, if a user sets `allowed_elements` to an empty list or excludes `!--`, this comment will be flagged as a violation.

### Correct Scenarios

This rule does not trigger when inline HTML is replaced with equivalent Markdown syntax.

```Markdown
This is *Raw* HTML.

![image](/foo.jpg)
```

> **Explanation**: This example passes because italics are expressed using Markdown emphasis (`*Raw*`) and the image is expressed using Markdown image syntax (`![image](/foo.jpg)`). No raw HTML elements are present, so the rule does not trigger.

Unlike the previous example, this case demonstrates using the `allowed_elements` configuration to permit specific HTML tags. Here, `<i>` and `<image>` are added to the allowed list, so their presence does not trigger the rule.

```Markdown
This is <i>Raw</i> HTML.

<image src="/foo.jpg">
```

> **Explanation**: This example passes because the `allowed_elements` configuration has been set to include `i` and `image`. The rule only triggers on HTML elements not on the allowed list, so these tags are permitted.

Unlike the previous examples, this case demonstrates the `allow_first_image_element` configuration, which permits an `<img>` tag wrapped in an `<h1>` tag at the very start of the document. This exception supports the common pattern of using an HTML image as a project heading on platforms like GitHub.

```Markdown
<h1 align="center"><img src="/path/to/logo.png" alt="Logo"/></h1>

Normal document content follows.
```

> **Explanation**: This example passes because the `allow_first_image_element` configuration is enabled by default (`True`). The rule recognizes that the document begins with an HTML block consisting of an `<h1>` tag containing only an `<img>` tag, and permits this specific structure as an exception to the normal `allowed_elements` restrictions. This exception applies only to the first element in the document and does not affect HTML elements appearing elsewhere.

## Fix Description

This rule cannot be auto-fixed because the appropriate correction depends on user intent. If the goal is to disallow all HTML, the [Disallow HTML](../extensions/disallowed-raw-html.md) extension should be used instead, which escapes `<` characters. If the goal is to flag specific HTML tags, users should review and correct the flagged elements manually or configure `allowed_elements` to permit known-safe tags.

## Configuration

| Prefixes |
| --- |
| `plugins.md033.` |
| `plugins.no-inline-html.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `allowed_elements` | `string` | `!--,![CDATA[,!DOCTYPE` | Comma separated list of tag starts that are allowable. |
| `allow_first_image_element` | `boolean` | `True` | Whether to allow an image HTML block. |

The `allowed_elements` value is a comma-separated list of items. Each item is a string with a format of `{item}`, and the full list follows the format `{item},...,{item}`.

Each item in the list is derived by taking the start of the tag and skipping
over the start character `<`. From that point, the parser collects the contents
of the tag up to one of the following:

- the first whitespace character
- the close HTML tag character (`/`)
- the end HTML tag character (`>`)

Since tags either require a whitespace character, the end character, or
the closing characters, this supplies a straightforward way to represent each HTML
tag. The only exceptions to this are when the rule encounters the
[CDATA](https://github.github.com/gfm/#cdata-section)
character sequence `![CDATA[` right after the start HTML tag character (`<`) or
the HTML comment sequence `!--`.
Because those sequences do not require any whitespace to follow them, they are managed
separately.

### Allowing For Image Headings

Numerous established GitHub projects use an HTML image for their initial heading. This is
already supported through [Rule MD041](./rule_md041.md) which allows an `h1` tag at the very start
of the document to satisfy the requirements for the document starting with a level
1 Heading element:

```Markdown
<h1 align="center"><img src="/path/to/image"/></h1>
```

To round out that support in this rule, the `allow_first_image_element` was added
to provide an exception to the normal `allowed_elements` configuration value. This
exception is specifically for the very first element in the document, and only
triggers if that HTML Block element starts and ends with a `h1` tag, with only an
`img` tag between them.

### Special Sequences - Processing Instructions and the DOCTYPE Directive

In earlier versions of the Rule Plugin, support for identifying a generic Processing
Instruction starting with the `?` character was supported. After doing some needed
research, it was determined that Processing Instructions are supported in XML documents,
[but not in HTML documents](https://www.tutorialspoint.com/xml/xml_processing.htm).
After confirming that information at other sources, the Processing Instruction sequence
was removed from the default for the `allowed_elements` configuration value.

At the same time, research was performed on Declarations that start with the `!`
character. Related to Processing Instructions, these elements are also used in XML
documents for special instructions, but do not appear in HTML documents. The one
exception is the `!DOCTYPE` declaration. The [DOCTYPE declaration](https://en.wikipedia.org/wiki/Document_type_declaration)
is included in HTML documents to ensure that the browser interprets the HTML document
in the manner that it was intended to be parsed.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD033](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md033---inline-html).

### Differences From MarkdownLint Rule

The substantial difference from the original rule is that the original rule only
triggers if an alphabetic character follows the starting `<` character. While
that worked in most cases, it precluded the detection of
[HTML start conditions](https://github.github.com/gfm/#html-blocks)
number 2 to number 5 and the closing tag case for number 7.

In creating this rule to work with all HTML tags, including previously undetected HTML start conditions,
the `allowed_elements` configuration default value is set to `!--,![CDATA[` to allow
for common HTML tags to not trigger this rule by default.

To provide better support for the "image as a heading" scenario, the
`allow_first_image_element` configuration value was added to specifically
allow that scenario to not trigger this rule.
