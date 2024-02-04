# Markdown Front Matter

| Item | Description |
| --- | --- |
| Extension Id | `front-matter` |
| GFM Extension Status | Unofficial |
| Configuration Item | `extensions.front-matter.enabled` |
| Default Value | `False` |

## Configuration

| Prefixes |
| --- |
| `extensions.front-matter.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the extension is enabled. |
| `allow_blank_lines` | `string` | `False` | Whether blank lines are allowed within the front-matter block. |

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

### Specifics

For clarity in the following sections, any mention of the word "whitespace"
refers to ascii whitespace characters `"\x20\x09\x0a\x0b\x0c\x0d"`. Specifically,
these characters are the space character `\x20`, the tab character `\x09`,
the newline character `\x0a`, the line tabulation character `\x0b`, the form feed
character `\x0c`, and the carriage return character `\x0d`.

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

#### Previous Format

This previous format was mostly compatible with the
[Python Markdown](https://python-markdown.github.io/extensions/meta_data/)
metadata format, except for a couple of small issues.  The problems with
that format were that they were specified for Python Markdown, with little
room for change.  That was the more complete of two specifications, the
other being the [Jekyll specification](https://jekyllrb.com/docs/front-matter/)
which was lean on specifics.

To be more compatible with how other parsers seem to use front-matter in the
field, we decided to keep things simple, forgoing the old format for a simple
YAML format.

#### YAML format

Being the predominant format, we decided that it was best to let the Python YAML
package any issues with the validity of the YAML information contained within
the document.  To that extent, a start boundary of `---` and an end boundary
of `---` are now required to delimit the front-matter from the rest of the
document.  In addition, if the `allow_blank_lines` configuration is set to its
default of `False`, a blank line will also terminate the front-matter.  If that
configuration is set to `True`, any blank lines are preserved and are passed
on to the PyYAML processor.

Once the lines in the front-matter have been determined, they are passed to
the [PyYAML](https://pypi.org/project/PyYAML/) processor in safe mode.  It is
left up to that package to determine whether the YAML is valid, including the
presence of any blank lines allowed when the `allow_blank_lines` setting is `True`.
If the YAML is valid, it is returned as a dictionary for parsing. Otherwisem the
lines are fed back to the normal processor and are interpretted as normal lines.

### Common Fields

#### Subject or Title

Many document processors prefer to have the subject or title (depending
on the document processor) specified in the front matter using either
the `Subject` or `Title` field name.  This allows the processor to
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
