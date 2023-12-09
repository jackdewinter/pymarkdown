# Markdown Strikethrough

| Item | Description |
| --- | --- |
| Extension Id | `markdown-strikethrough` |
| GFM Extension Status | Official |
| Configuration Item | `extensions.markdown-strikethrough.enabled` |
| Default Value | `False` |

## Summary

This extension follows the GitHub Flavored Markdown
[rules](https://github.github.com/gfm/#strikethrough-extension-) for the ability
to add a new type of emphasis, strikethrough emphasis.  Similar to how the `*`
and `_` emphasis characters provide `<em>`/`</em>` and `<strong>`/`</strong>`
emphasis blocks in text, the `~` character provides `<del>`/`</del>`

## Extension Specifics

This extension is a pretty simple extension.  In the handling of the emphasis
markers, in addition to the `*` and `_` characters providing simple emphasis
(usually italics) and `**` and `__` providing strong emphasis (usually bold),
one or two `~` characters provide strikethrough emphasis.

The decision to only allow 1 or 2 `~` characters is to ensure that there is
no confusion between this emphasis and the use of 3 `~` characters to start
a fenced block.
