# Extensions

## Markdown Disallowed Raw HTML

[Full Documentation](./extensions/disallowed-raw-html.md)

<!--- pyml disable-next-line no-duplicate-heading-->
### Summary

This extension follows the GitHub Flavored Markdown
[rules](https://github.github.com/gfm/#disallowed-raw-html-extension-) for the
marking of certain HTML tag names as disallowed.  Once marked as disallowed, the
HTML tag will have the leading character `<` changed to `&lt;` to prevent it from
being rendered as a HTML tag by browsers.

## Markdown Extended Autolinks

[Full Documentation](./extensions/extended-autolinks.md)

<!--- pyml disable-next-line no-duplicate-heading-->
### Summary

This extension follows the GitHub Flavored Markdown
[rules](https://github.github.com/gfm/#autolinks-extension-) to extend the
set of text sequences that the parser considers as a link and an autolink element
generated for it.  While the normal [autolinks](https://github.github.com/gfm/#autolinks)
deal with text enclosed within the `<` and `>` characters, this extension
introduces autolinks that the parser will recognize without any enclosing characters.

## Markdown Front-Matter

[Full Documentation](./extensions/front-matter.md)

<!--- pyml disable-next-line no-duplicate-heading-->
### Summary

This extension allows for the parsing of Markdown "front-matter" at
the start of a Markdown document.  Markdown front-matter is used by
various Markdown parsers to communicate extra metadata to the document
processor, metadata that alters the presentation of that document.

The most common use case for front-matter is in Markdown aggregators,
such as static website generators.  The front-matter is used to supply metadata
about each Markdown document, metadata used to classify, annotate, and
augment the Markdown document.

## Pragmas

[Full Documentation](./extensions/pragmas.md)

<!--- pyml disable-next-line no-duplicate-heading-->
### Summary

This extension allows the PyMarkdown parser to look for "pragmas" that provide
metadata about a Markdown document.  This information is then used by the rule
engine to alter how failures are processed.

The most common use case for pragmas is to disable rule violations for a specific
rule on the line that follows the pragma.  As a logical extension of this, there
is also a form of the pragmas that disables rule violations for a specified number
of lines after the pragma.

## Markdown Strikethrough

[Full Documentation](./extensions/strikethrough.md)

<!--- pyml disable-next-line no-duplicate-heading-->
### Summary

This extension follows the GitHub Flavored Markdown
[rules](https://github.github.com/gfm/#strikethrough-extension-)
to add a new type of emphasis, strikethrough emphasis.  Like how the `*`
and `_` emphasis characters provide `<em>`/`</em>` and `<strong>`/`</strong>`
emphasis blocks in text, the `~` character provides  for `<del>`/`</del>`
emphasis blocks.

## Markdown Task List Items

[Full Documentation](./extensions/task-list-items.md)

<!--- pyml disable-next-line no-duplicate-heading-->
### Summary

This extension follows the GitHub Flavored Markdown
[rules](https://github.github.com/gfm/#task-list-items-extension-)
to interpret certain list items as task list items.  If the specified sequence is
present at the start of the text for a list item, it is interpreted as a task
list item.  That sequence is a `[` character followed by one of `{space}`, `x`
or `X`, and ending with a `]` character and at least one whitespace character.
