# Extensions

## Markdown Disallowed Raw HTML

[Full Documentation](./extensions/disallowed-raw-html.md)

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

This extension follows the GitHub Flavored Markdown
[specifications](https://github.github.com/gfm/#disallowed-raw-html-extension-)
for the
marking of certain HTML tag names as disallowed.  Once marked as disallowed, the
HTML tag will have the leading character `<` changed to `&lt;` to prevent it from
being rendered as a HTML tag by browsers.

## Markdown Extended Autolinks

[Full Documentation](./extensions/extended-autolinks.md)

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

This extension follows the GitHub Flavored Markdown
[specifications](https://github.github.com/gfm/#autolinks-extension-) to extend the
set of text sequences that the parser considers as a link and an autolink element
generated for it.  While the normal [autolinks](https://github.github.com/gfm/#autolinks)
deal with text enclosed within the `<` and `>` characters, this extension
introduces autolinks that the parser will recognize without any enclosing characters.

## Markdown Front-Matter

[Full Documentation](./extensions/front-matter.md)

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

This extension allows for the parsing of Markdown "Front-Matter" at
the start of a Markdown document.  Markdown Front-Matter is used by
various Markdown parsers to communicate extra metadata to the document
processor, metadata that alters the presentation of that document.

The most common use case for Front-Matter is in Markdown aggregators,
such as static website generators.  The Front-Matter is used to supply metadata
about each Markdown document, metadata used to classify, annotate, and
augment the Markdown document.

## Markdown Tables

[Full Documentation](./extensions/markdown-tables.md)

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

This extension follows the GitHub Flavored Markdown
[specification](https://github.github.com/gfm/#tables-extension-)
to provide for simple tables in Markdown documents.

## Pragmas

[Full Documentation](./extensions/pragmas.md)

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

This extension allows the PyMarkdown parser to look for "Pragmas" that provide
metadata about a Markdown document.  This information is then used by the Rule
Engine to alter how Rule Failures are processed.

The most common use case for Pragmas is to disable Rule Failures for a specific
Rule Plugin on the line that follows the Pragma.  As a logical extension of this,
there
is also a form of the Pragmas that disables Rule Failures for a specified number
of lines after the Pragma.

## Markdown Strikethrough

[Full Documentation](./extensions/strikethrough.md)

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

This extension follows the GitHub Flavored Markdown
[specification](https://github.github.com/gfm/#strikethrough-extension-)
to add a new type of emphasis, strikethrough emphasis.  Like how the `*`
and `_` emphasis characters provide `<em>`/`</em>` and `<strong>`/`</strong>`
emphasis blocks in text, the `~` character provides  for `<del>`/`</del>`
emphasis blocks.

## Markdown Task List Items

[Full Documentation](./extensions/task-list-items.md)

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

This extension follows the GitHub Flavored Markdown
[specification](https://github.github.com/gfm/#task-list-items-extension-)
to interpret certain list items as task list items.  If the specified sequence is
present at the start of the text for a list item, it is interpreted as a task
list item.  That sequence is a `[` character followed by one of `{space}`, `x`
or `X`, and ending with a `]` character and at least one whitespace character.
