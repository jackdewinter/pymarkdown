# Rule - MD003

| Aliases |
| --- |
| `md003` |
| `heading-style` |
| `header-style` |

## Summary

Heading style should be consistent throughout the document.

## Reasoning

One of the main keys to readability is to have consistent formatting applied
throughout a group of documents.  Extending the concept even further, many
organizations have specific rules on how documents should be authored throughout
that organization.  It follows that both concepts may extend to specifying
which elements should be used for specifying headings in a Markdown document.

## Examples

### Failure Scenarios

This rule triggers by default when more than one heading style is used within
a given document:

```Markdown
## Atx Heading Without Closing Hashes

## Atx Heading With Closing Hashes ##

SetExt Heading
===============
```

### Correct Scenarios

This rule does not trigger when a consistent heading style is used within
the document.  By default, the heading style is determined by the first
heading element encountered in the document:

```Markdown
# ATX style H1

## ATX style H2
```

Configuration may be used to specify an exact heading style to be used within
the document.  This is extremely useful for the `setext` style, which is limited
by Markdown to only 2 levels.  The `setext_with_atx` and `setext_with_atx_closed`
styles can be used to specify that for levels 3 and higher, the `atx` and
`atx_closed` styles are specified.

If the `style` value is `"setext_with_atx"`, then this example will not trigger
the rule:

```Markdown
Setext style H1
===============

Setext style H2
---------------

### ATX style H3
```

## Configuration

| Prefixes |
| --- |
| `plugins.md003.` |
| `plugins.heading-style-h1.` |
| `plugins.header-style-h1.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled by default. |
| `style` | string (see below) | `"consistent"` | Style of headings expected in the document. |

Valid heading styles:

| Style | Description |
| -- | -- |
| `"consistent"` | The first heading in the document specifies the style for the rest of the document. |
| `"atx"` | Only Atx Headings without any closing hashes are to be used. |
| `"atx_closed"` | Only Atx Headings with closing hashes are to be used. |
| `"setext"` | Only SetExt headings are to be used. |
| `"setext_with_atx"` | Only SetExt headings are to be used for levels 1 and 2, and Atx Headings without closing hashes to be used for levels 3 to 6.|
| `"setext_with_atx_closed"` |Only SetExt headings are to be used for levels 1 and 2, and Atx Headings with closing hashes to be used for levels 3 to 6.|

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD003](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md003---heading-style).
