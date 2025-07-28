# Markdown Front-Matter

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

<!-- pyml disable-num-lines 4 line-length-->
| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the extension is enabled. |
| `allow_blank_lines` | `string` | `False` | Whether blank lines are allowed within the front-matter block. |

## Summary

This extension allows for the parsing of Markdown "front-matter" at
the start of a Markdown document.  Markdown front-matter is used by
various Markdown parsers to communicate extra metadata to the document
processor, metadata that alters the presentation of that document.

The most common use case for front-matter is in Markdown aggregators,
such as static website generators.  The front-matter is used to supply metadata
about each Markdown document, metadata used to classify, annotate, and
augment the Markdown document.

## Examples

The raw Markdown for the [Advanced Extensions](../advanced_extensions.md) page
starts with the text:

```Markdown
---
summary: More information on extensions and which extensions are currently available.
authors:
  - Jack De Winter
---

# Advanced Extensions
```

While you cannot see it in the link above, it is present in the [raw form](https://raw.githubusercontent.com/jackdewinter/pymarkdown/main/newdocs/src/advanced_extensions.md)
of the web page.  When the MkDocs aggregator/documentation application that we
use for our documentation reads
in that file, it is presented with the above metadata.  While the metadata
for that specific page is purely informational, it could also include the `title`
or `template` fields that MkDocs uses to affect the rendering of the page.

## Specifics

The [GitHub Flavored Markdown](https://github.github.com/gfm/) specification
focuses on the parsing of Markdown and the uniform generation of HTML based on
that parsing.  As such, the authors of that document did not provide any guidance
in the specification that addresses the needs of the Markdown parsers that may
require additional metadata to properly render a Markdown document.

### History

There is only bits of information documented about Front-Matter, even
though most static website generators use it.  The bulk of the information
we found was contained in these documents:

- [Markdown Lint](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md041---first-line-in-a-file-should-be-a-top-level-heading)
- [Python Markdown](https://python-markdown.github.io/extensions/meta_data/)
- [Jekyll Static Site Generator](https://jekyllrb.com/docs/front-matter/)

### Clarifications

For clarity in the following sections, any mention of the word "whitespace"
refers to ascii whitespace characters `"\x20\x09\x0a\x0b\x0c\x0d"`. Specifically,
these characters are the space character `\x20`, the tab character `\x09`,
the newline character `\x0a`, the line tabulation character `\x0b`, the form feed
character `\x0c`, and the carriage return character `\x0d`.

### Front-Matter Blocks

The Front-Matter Block start character sequence of `---` must be by itself
on the first line of the document with no whitespace before that
character sequence.  As some editors may not display trailing whitespace
properly, trailing whitespace is allowed after the above character sequence.

The Front-Matter Block end character sequence `---` concludes the front-matter
section. It also must be by itself on a subsequent line of
the document with no whitespace before that character sequence. As with
the start sequence, trailing whitespace after the end character sequence
is allowed.

Everything on the line after the start character sequence to the line
before the end character sequence is considered the content of the
Front-Matter Block.  The normally recognized Markdown document starts
with the line after the end character sequence.

#### YAML format

Based on experience, our team decided that it was best to let the Python YAML
package deal with any issues regarding the validity of the YAML front-matter.
To that extent, anything within a start boundary of `---` and an end boundary
of `---` are passed to the Python YAML package for validation.  If the `allow_blank_lines`
configuration item has a value of `True`, a blank line will also terminate the
front-matter.  If that configuration item's value is its default of `False`,
any blank lines are preserved and are passed on to the YAML processor.

Once the lines in the front-matter block have been determined, they are passed to
the [PyYAML](https://pypi.org/project/PyYAML/) processor in safe mode.  It is
left up to that package to determine whether the YAML is valid.
If the YAML is valid, it is returned to PyMarkdown as a dictionary for possible
parsing by another extension or one of the rules.
If the YAML is not valid, the lines are fed back to the normal processor and
are then interpreted as normal lines.

### Common Fields

Note that the use of these fields varies wildly between different Markdown parsers
and aggregators.  Before making any assumptions on how a given application interprets
YAML front-matter, please consult that application's documentation.

#### Subject or Title

Many document processors prefer to have the subject or title (depending
on the document processor) specified in the front-matter using either
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

There are specific cases where a document needs to be fixed to a current
date.  For example, say a document was initially created on June 14th
and published on a website, but includes a link to another document.
If anything in that document changes, say the page that link points to,
that new change would reset the document's date to the current date.
If anything is counting on the document's "date" to remain constant,
that change would invalidate that assumption.  The `Date` metadata
field provides a manner to specify the date of the document as a
constant.
