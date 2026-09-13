# Rule - PML100

| Property | Value |
| --- | --- |
| Aliases | `pml100`, `disallowed-html` |
| Autofix Available | No |
| Enabled By Default | No |

## Summary

Ensure that disallowed HTML elements (such as `script`, `iframe`, and `style`) do
not appear in the Markdown document.

## Reasoning

### Simplicity

This rule specifically provides an alternative to the [Disallowed HTML](../extensions/disallowed-raw-html.md)
extension of the [GitHub Flavored Markdown](https://github.github.com/gfm/) specification.
The benefit
is that it produces a linting failure for disallowed HTML, whereas the extension
silently strips the HTML at render time.

### Note

Alternative to disallow-html extension. benefit here is that it triggers a failure
instead of blindly ignoring the HTML.

Like its related extension, the initial set of (case insensitive) tag names are:

- title
- textarea
- style
- xmp
- iframe
- noembed
- noframes
- script
- plaintext

Just like the extension, this list can be configured by setting the `change_tag_names`
configuration value, as outlined in the [Configuration](#configuration) section
below.

## Examples

### Failure Scenarios

This rule triggers when a configured disallowed HTML tag (such as `script`)
appears in the start-end form (`<script>…</script>`).

```Markdown
<script src=./foo.js>
  <!-- some script stuff -->
</script>
```

> **Explanation**: This example fails because the `script` tag appears in the
> start-end form, which matches the disallowed tag list.

Unlike the previous example, this case uses the self-closing start-only form
(`<script/>`) instead of a paired start-end pair.

```Markdown
<script/>
```

> **Explanation**: This example fails because the self-closing `script` tag
> matches the disallowed tag list — the rule explicitly matches both the
> start-end form and the self-closing start-only form.

Unlike the previous examples, which both use the `script` tag, this case
uses the `iframe` tag, which is also on the default disallowed list.

```Markdown
<iframe src="./evil.html" width="100%" height="200"></iframe>
```

> **Explanation**: The `iframe` tag is included in the default disallowed tag
> list, and it appears in the start-end form, so the rule fails the document
> exactly as it would for `<script>`.

Unlike the previous examples, which use a single disallowed tag, this case
shows that **every** tag on the default disallowed list is matched:
`title`, `textarea`, `style`, `xmp`, `noembed`, `noframes`, `plaintext`,
and `script` (in addition to `iframe`).

```Markdown
<title>hidden</title>
<textarea>hidden</textarea>
<style>body { display: none; }</style>
<xmp>hidden</xmp>
<noembed>hidden</noembed>
<noframes>hidden</noframes>
<plaintext>hidden</plaintext>
<script>hidden</script>
```

> **Explanation**: Each opening tag in this document — `title`, `textarea`,
> `style`, `xmp`, `noembed`, `noframes`, `plaintext`, and `script` — is a
> parsed opening-tag token whose name (case-insensitively) is on the default
> disallowed list, so the rule reports a failure for each one.

Unlike the previous examples, which all use lowercase tag names, this case
uses an **uppercase** variant (`<SCRIPT>`) to demonstrate that the rule's
tag-name matching is case-insensitive.

```Markdown
<SCRIPT src="./evil.js"></SCRIPT>
```

> **Explanation**: The default disallowed list contains `script` in
> lowercase, but the rule compares tag names case-insensitively, so the
> uppercase `<SCRIPT>` opening tag is still matched and the rule fails the
> document.

Unlike the previous examples, which use a single all-lowercase or
all-uppercase tag name, this case uses a **mixed-case** variant
(`<Script>`) to confirm that any casing of a disallowed tag is matched.

```Markdown
<Script src="./evil.js"></Script>
```

> **Explanation**: Case-insensitive matching means `<Script>`, `<SCRIPT>`,
> `<sCrIpT>`, and `<script>` are all equivalent to the rule; the mixed-case
> `<Script>` opening tag is therefore matched against the lowercase `script`
> entry on the disallowed list, and the rule fails the document.

Unlike the previous examples, which each contain a single disallowed tag,
this case places **multiple** disallowed tags (a `script` start-end pair and
a self-closing `iframe`) in the same document to show that the rule
independently flags each occurrence.

```Markdown
<script src="./evil.js"></script>
<iframe src="./evil.html"/>
```

> **Explanation**: The rule scans the document for every parsed
> opening-tag token and checks it against the disallowed list. Both the
> `<script>` start-end form and the `<iframe>` self-closing form are on the
> default disallowed list, so the rule reports a failure for **each** of
> them, not just the first.

Unlike the previous examples, which all use tags from the default disallowed list,
this case shows that a **custom** tag added to the list via the `change_tag_names`
configuration value (e.g., `+embed`) is also matched and reported as a failure.

```Markdown
<embed src="./malicious.swf" type="application/x-shockwave-flash"/>
```

> **Explanation**: With `change_tag_names` set to `+embed`, the `embed` tag is appended
> to the default disallowed list. The `<embed/>` self-closing opening-tag token
> above is therefore matched case-insensitively against that extended list, and
> the rule fails the document — exactly as it would for a default-list tag such
> as `<script>`.

Unlike the previous examples, which each use a minimal disallowed tag with no
(or only one) attribute, this case shows that the rule still fires when the disallowed
tag carries attributes and irregular whitespace between the tag name and the attribute
list.

```Markdown
<script   src="./evil.js"  type="text/javascript"></script>
```

> **Explanation**: The opening-tag token begins with `<script` followed by whitespace
> and an attribute list, which is a normal HTML opening-tag form. The rule matches
> on the tag *name* (the token text starting with `<script`), not on the exact spacing
> or the presence/absence of attributes, so the irregular whitespace in
> `<script src=…` does not prevent the match and the rule fails the document.

Unlike the previous examples, where each disallowed tag appears at the top level
of the document, this case nests a `script` start-end pair inside another HTML element
(`<html> … </html>`) to confirm that the rule still reports the inner disallowed
tag.

```Markdown
<html>
  <body>
    <script src="./evil.js"></script>
  </body>
</html>
```

> **Explanation**: The rule does not stop at the first opening tag it sees. It scans
> every parsed opening-tag token in the document, and the inner `<script>` opening
> tag — even though it is nested two levels inside `<html>` and `<body>` — still
> begins with `<script` and therefore matches the default disallowed list, so the
> rule fails the document at the position of the inner tag.

### Correct Scenarios

This rule does not trigger when the disallowed tag is escaped using the HTML entity
`&lt;`.

```Markdown
&lt;script src=./foo.js>
  <!-- some script stuff -->
&lt;/script>
```

> **Explanation**: The opening angle bracket of `<script` is written as the entity
> `&lt;`, so no parsed opening-tag token beginning with `<script` exists. The
> `</script>` close tag is a different token kind and is not matched by the rule.

Unlike the previous example, this case escapes the self-closing form (`&lt;script/>`).

```Markdown
&lt;script/>
```

> **Explanation**: The self-closing `script` token is also avoided because its
> opening angle bracket is the entity `&lt;`; the rule's matching logic looks for
> a parsed opening-tag token whose text starts with `<script`, and none is present.

Unlike the previous examples, which show that escaping the angle bracket
prevents the rule from matching, this case uses tags that are **not** on
the disallowed list at all (`div`, `span`, `a`).

```Markdown
<div class="wrapper">
  <span>Hello</span>
  <a href="./page.html">link</a>
</div>
```

> **Explanation**: The tags `div`, `span`, and `a` do not appear on the default
> disallowed tag list (`title`, `textarea`, `style`, `xmp`, `iframe`, `noembed`,
> `noframes`, `script`, `plaintext`), so the rule does not report a failure for
> any of them, regardless of their form or attributes.

Unlike the previous examples, which contain complete start-end tag pairs, this
case contains only a closing tag (`</script>`) with no corresponding opening tag.

```Markdown
</script>
```

> **Explanation**: The rule matches parsed **opening**-tag tokens whose text begins
> with a disallowed tag name. The token `</script>` is a closing-tag token, not
> an opening-tag token, so it is not matched and the rule does not fire.

Unlike the previous examples, which place the disallowed tag in regular Markdown
prose, this case places a `<script>` tag inside a fenced code block, where the text
is treated as a code sample rather than as raw HTML.

````Markdown
```html
<script>
```
````

> **Explanation**: Content inside a fenced code block is not parsed as raw HTML
> by the Markdown processor; it is emitted verbatim as a `<code>` element. Because
> no opening-tag token for script is produced during parsing, the rule does
> not fire.

Unlike the previous examples, which involve actual HTML tag syntax, this case uses
the word "script" as plain text in a sentence, with no angle brackets or tag structure.

```Markdown
This document describes how to write a script in JavaScript.
```

> **Explanation**: The word "script" here is ordinary prose, not an opening-tag
> token. The rule only matches parsed opening-tag tokens whose text starts with
> `<` followed by a disallowed tag name, so plain-text occurrences of the word
> "script" do not trigger a failure.

## Fix Description

Automated fixes are not performed because removing or rewriting disallowed HTML
would alter what the author wrote, and the correct replacement (if any) depends on
the author's intent for how the document is ultimately rendered.

## Configuration

| Prefixes |
| --- |
| `plugins.pml100.` |
| `plugins.disallowed-html.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `False` | Whether the Rule Plugin is enabled. |
| `change_tag_names` | `string` | [See above list](#note). | Comma-separated list of HTML tag names to disallow. Items prefixed with `+` are added to the default list; items prefixed with `-` are removed from it. |

** The comma-separated list of items is a string with a format of `{item},...,{item}`.
Any leading or trailing space characters surrounding the `{item}` are trimmed during
processing.  Empty `{item}` values after this trimming has been applied will generate
a configuration error.

In addition, each item in the list must start with either the `+` character
to add the item to the list, or the `-` character to remove the item from the list.

## Origination of Rule

This rule was developed as an alternative to the
[Disallowed HTML](../extensions/disallowed-raw-html.md) extension.
