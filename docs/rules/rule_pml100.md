# Rule - PML100

| Aliases |
| --- |
| `pml100` |
| `disallowed-html` |

## Summary

Disallowed HTML elements.

## Reasoning

### Compatibility

This rule is specially crafted to be the rule version of the
[GitHub Flavored Markdown](https://github.github.com/gfm/) extension
[Disallowed HTML](../extensions/disallowed-raw_html.md). As that extension only
changes the HTML text of the specified HTML sequences upon rendering of the Markdown
document into HTML, it does not provide any benefit for someone who only wants
to lint the Markdown document. Implemented as a rule, this limit can be overcome.

Like the extension that this rule is related to, the initial set of (case insensitive)
tag names is:

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

This rule triggers if any of the configured HTML tags are encountered in either
the start only form (such as `<script`) or the start-end form (such as `<script/>`).

```Markdown
<script src=./foo.js>
  <!-- some script stuff -->
</script>

<script/>
```

### Correct Scenarios

To correct the above examples, like the simply replace the starting tag character
`<` with the character sequence `&lt;`.

```Markdown
`&lt;`script src=./foo.js>
  <!-- some script stuff -->
</script>

`&lt;`script/>
```

The effect of replacing that one character is that the web browser no longer interprets
that HTML tag as an HTML tag. That prevents the author's action, such as to include
a JavaScript file, from happening.

## Configuration

| Prefixes |
| --- |
| `plugins.pml101.` |
| `plugins.disallowed-html.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `change_tag_names` | `string` | [See above list](#compatibility). | Comma-separated list of proper nouns to preserve capitalization on.** |

** The comma-separated list of items is a string with a format of `{item},...,{item}`.
Any leading or trailing space characters surrounding the `{item}` are trimmed during
processing.  Empty `{item}` values after this trimming has been applied will generate
a configuration error.

In addition, each item in the list must start with either the `+` character
to add the item to the list, or the `-` character to remove the item from the list.

## Origination of Rule

This rule was developed as an alternative to the
[Disallowed HTML](../extensions/disallowed-raw_html.md) extension.
