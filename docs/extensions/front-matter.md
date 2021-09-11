# Markdown Front Matter

| Item | Description |
| --- | --- |
| Extension Id | `front-matter` |
| GFM Extension Status | Unofficial |
| Configuration Item | `extensions.front-matter.enabled` |
| Default Value | `False` |

## Summary

This extension allows for the parsing of Markdown "front matter" at
the start of a Markdown document.  Markdown front-matter is used by
various document processors to communicate extra metadata to the document
processor, metadata that usually alters the presentation of that document.

The most common use case for front-matter is in static website
generators that use the information to figure out where to put the
rendered document, how to classify it, and whether it is a published
document or a draft document.

## Extension Specifics

The [GitHub Flavored Markdown](https://github.github.com/gfm/) specification
focuses on the parsing of Markdown and the uniform generation of HTML based on
that parsing.  As Markdown Front Matter is not Markdown, but one of a
handful of other formats, the authors of that document justifiably did not
provide anything to deal with Markdown front matter.

### History

There is not a lot of information documented about Front Matter, even
though most static website generators use it.  The bulk of the information
we found was contained in these documents:

- [Markdown Lint](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md041---first-line-in-a-file-should-be-a-top-level-heading)
- [Python Markdown](https://python-markdown.github.io/extensions/meta_data/)
- [Jekyll Static Site Generator](https://jekyllrb.com/docs/front-matter/)

### Front Matter Blocks

The Front Matter Block start character sequence of `---` must be by itself
on the first line of the document with no whitespace before that
character sequence.  As some editors may not display trailing whitespace
properly, trailing whitespace is allowed after the above character sequence.

The Front Matter Block end character sequence `---` concludes the front
matter section. It also must be by itself on a subsequent line of
the document with no whitespace before that character sequence. As with
the start sequence, trailing whitespace after the end character sequence
is allowed.

Everything on the line after the start character sequence to the line
before the end character sequence is considered the content of the
Front Matter Block.  The normally recognized Markdown document starts
with the line after the end character sequence.

### Front Matter Token

A singular `FrontMatterToken` instance can occur at the very start of
the Markdown token stream.  As with all other tokens, this token contains
the necessary information to successfully rebuild the Front Matter
Block from that data.  This may be used by rules that need to examine
the Front Matter Block Data and need an accurate character-by-character record
of what was in the Front Matter Block element.

For more casual use, the `matter_map` property contains a dictionary
with a fully parsed set of field names and values.  This parsing is
accomplished using one of the data formats specified in the next section.

### Data Formats

The following section describe the various data formats that are allowed
for the Front Matter Block Data.  In both cases, at least one field must
be parsed according to the Front Matter Data Format for the data to be
considered valid.

#### Normal Format

This format is mostly compatible with the
[Python Markdown](https://python-markdown.github.io/extensions/meta_data/)
metadata format, except as mentioned in the next paragraph.
A valid field name line starts with a field comprised of one or more characters
in the regular expression group `([a-z][A-Z][0-9]_-)+` followed by the
colon character ':'.  Optionally, any character data may follow the colon
character up to the end of the line and is called the field value.

A continuation line is any line that follows a field name line or another
continuation line that starts with 4 or more whitespace characters.  As
the name suggests, the data in a continuation line is the
continuation of the data presented in the last field name.  The data that
is appended to the field value is the newline character followed by any
data following the leading whitespace.  The interpretation of that data
as a single value or as a set of separated values is totally dependent
on the needs of the function requesting the field value.

Any blank lines in the Front Matter Block invalidate the entire front
matter block.  The only exception to that is if the blank line starts
with 4 or more whitespace characters, in which case it is interpreted
as a continuation line, as documented in the last paragraph.

#### Changes from Python Markdown

The two major changes from the Python Markdown format concerns validation
and blank lines.

##### Invalid Front Matter Data Format

As the documentation is sparse at best, there is no mention of how to
handle invalid cases, such as a line that begins with an invalid keyword.
When the Front Matter Data Format is shown to be invalid, the Front Matter
Block is discarded, and the parser then parses those same lines as
straight Markdown.

The supported cases of invalidating the Front Matter Block Data for
this data format are:

- "Continuation line encountered before a keyword line."
- "Blank line encountered before end of metadata."
- "Newline did not start with `keyword:`."

##### New Lines

The second change is the support for newlines.  In the Python Markdown
documentation, any blank line will terminate the Front Matter Block Data at
that point.  Instead of that approach, we decided that to be more
predictable, except for a continuation blank line (see above), any
blank line will invalidate the entire Front Matter Block Data format.
If that happens, the process outlined in the previous section for
an invalidate Front Matter Block Data Format takes effect.

#### YAML format

TBD

### Common Fields

#### Subject or Title

Many document processors prefer to have the subject or title (depending
on the document processor) specified in the front matter using either
the `subject` or `title` field name.  This allows the processor to
easily use that metadata field value, not only for the top-level header
of the document, but for things such as the name of the generated HTML
document and other generated elements.

For example, the Pelican static site generator use the `Title` field name
in this manner:

```Markdown
---
Title: My Markdown document
Date: 2021-06-14
---

This is my Markdown document.

```

One of the common settings for blog-oriented static sites is to set
the file name of the article to be a combination of the `Date`
metadata field and the `Title` metadata field.  In this case, the
article would be published to the relative path
`content/2021/06/14/my-markdown-document/index.html`.

### Date

There are many cases where a document needs to be fixed to a current
date.  For example, say a document was initially created on June 14th
and published to a website, but includes a link to another document.
If anything in that document changes, say the page that link points to,
that new change would reset the document's date to the current date.
If anything is counting on the document's "date" to remain constant,
that change would invalidate that assumption.  The `Date` metadata
field provides a manner to specify the date of the document as a
constant.

For a good example of how this is used, see the above section
on [Subject or Title](#subject-or-title).
