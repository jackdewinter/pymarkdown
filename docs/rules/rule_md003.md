# Rule - MD003

| Aliases |
| --- |
| `md003` |
| `heading-style` |
| `header-style` |

## Summary

Heading style should be consistent throughout the document.

## Reasoning

### Readability

One of the main keys to readability is to have consistent formatting applied
throughout a group of documents.  Extending the concept even further,
organizations often have specific rules on how documents should be authored throughout
that organization.  It follows that both concepts may extend to specifying
which elements are used to specify headings in a Markdown document.

## Examples

### Failure Scenarios

This rule triggers when more than one heading style is used within a given document:

```Markdown
## Atx Heading Without Closing Hashes

## Atx Heading With Closing Hashes ##

SetExt Heading
===============
```

### Correct Scenarios

This rule does not trigger when a consistent heading style is used within
the document.  The default style `consistent` decides the heading style upon
encountering the first heading element in the document.  In this example:

```Markdown
# ATX style H1

## ATX style H2
```

the heading style that would be decided on is `atx`.

Configuration may be used to specify a specific heading style to be used within
the document.  This is extremely useful for the `setext` style, which is limited
by Markdown to only 2 levels.  The `setext_with_atx` and `setext_with_atx_closed`
styles can be used to specify that for levels 3 and higher, the `atx` and
`atx_closed` styles are specified.

If the `style` value is `setext_with_atx`, then this example will not trigger
the rule:

```Markdown
Setext style H1
===============

Setext style H2
---------------

### ATX style H3
```

#### Allowing Auto-Detection of `setext_with_atx`

Using the default style of `consistent` to auto-detect the `setext_with_atx` style
is problematic, as it appears first as the `setext` style.  The `allow-setext-update`
configuration value was added to address this issue.  If this configuration setting
is enabled with the previous example, the rule will still detect the `setext` style
based on the first SetExt Heading element.  However, when a level 3 (or higher)
Atx Heading element is encounted and this configuration setting is enabled, it will
switch to the `setext_with_atx` style.

## Configuration

| Prefixes |
| --- |
| `plugins.md003.` |
| `plugins.heading-style.` |
| `plugins.header-style.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `style` | string (see below) | `consistent` | Style of headings expected in the document. |
| `allow-setext-update` | boolean | `False` | If `style` is `consistent` and the document started off as `setext`, allow an upgrade to `setext_with_atx` if a level 3 Atx Header or higher is observed. |

Valid heading styles:

| Style | Description |
| -- | -- |
| `consistent` | The first heading in the document specifies the style for the rest of the document. |
| `atx` | Only Atx Headings without any closing hashes are used. |
| `atx_closed` | Only Atx Headings with closing hashes are used. |
| `setext` | Only SetExt headings are used. |
| `setext_with_atx` | Only SetExt headings are used for levels 1 and 2, and Atx Headings without closing hashes used for levels 3 to 6.|
| `setext_with_atx_closed` |Only SetExt headings are used for levels 1 and 2, and Atx Headings with closing hashes are used for levels 3 to 6.|

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD003](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md003---heading-style).
The `allow-setext-update` configuration value was added due to a [user request](https://github.com/jackdewinter/pymarkdown/issues/154).
