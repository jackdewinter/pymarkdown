# Markdown Strikethrough

| Item | Description |
| --- | --- |
| Extension Id | `markdown-strikethrough` |
| GFM Extension Status | Official |
| Configuration Item | `extensions.markdown-strikethrough.enabled` |
| Default Value | `False` |

## Configuration

| Prefixes |
| --- |
| `extensions.markdown-strikethrough.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the extension is enabled. |

## Summary

This extension follows the GitHub Flavored Markdown
[rules](https://github.github.com/gfm/#strikethrough-extension-)
to add a new type of emphasis, strikethrough emphasis.  Like how the `*`
and `_` emphasis characters provide `<em>`/`</em>` and `<strong>`/`</strong>`
emphasis blocks in text, the `~` character provides  for `<del>`/`</del>`
emphasis blocks.

## Examples

With this extension enabled, the following Markdown text:

```Markdown
~abc~
```

produces the following html:

```HTML
<del>abc</del>
```

which renders as:

<!--- pyml disable-next-line no-inline-html-->
<del>abc</del>

## Specifics

This extension is a simple extension, extending the types of emphasis that an author
may apply to inline text.  In the same way that the `*`/`**` characters provide
`<em>`/`</em>` emphasis and `_`/`__` characters provide `<strong>`/`</strong>`
emphasis, the strikethrough extension provides `<del>`/`</del>` emphasis.

Other than the adding of the `~` character to the set of emphasis characters,
this extension does not alter any of the other rules about applying emphasis
to inline text.
