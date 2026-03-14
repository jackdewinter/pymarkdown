---
summary: Quick-Start documentation on how to use PyMarkdown Extensions.
authors:
  - Jack De Winter
---

# Quick Start: Enabling PyMarkdown Extensions

This page helps you control which extensions PyMarkdown will use when scanning
your Markdown file for Rule Failures. A **Rule Failure** is one reported issue that
PyMarkdown's Rule Plugins find in your Markdown. For example, PyMarkdown might show
an error like "missing heading at top of file" when it detects a Rule Failure.

Extensions do not turn Rule Plugins on or off. Instead, they change how PyMarkdown
interprets
your Markdown file before calling any enabled Rule Plugins. For example, an extension
can tell PyMarkdown that a YAML block
is "Front-Matter" or that a set of `|` characters form a table. With that extra
context, Rule Plugins can analyze the document in a way that matches your intent.
**The same rules still run either way;** what changes is how your Markdown is parsed
before those Rule Plugins see it.

This page focuses on the practical side: how to enable the built‑in extensions that
ship with PyMarkdown so they recognize content like Front-Matter blocks and Markdown
tables in your own files.

If that explanation feels a bit abstract, that is okay.
In the next sections we use concrete examples &mdash; Front-Matter and tables &mdash;
to show how extensions change how PyMarkdown parses your Markdown and why that matters.

For a complete list of extensions and a brief explanation of what they do, consult
the User Guide's [Extensions](../user-guide.md#extensions) section.  For the purposes
of this Quick Start guide, we will only focus on two of those extensions: the Tables
Extension
and the Front-Matter Extension.

## What You Will Learn

> **Quick Start Guide Single Line Summary**
> This page teaches the basic information that you need to know about PyMarkdown's
> extensions, the two most frequently used extensions, and how to enable them.

PyMarkdown supports several extensions. In this Quick Start guide, we will mention
all of them briefly, but we will focus only on two: the Tables Extension and
the Front-Matter Extension. This page will teach you:

- what PyMarkdown extensions are
- the two most frequently enabled extensions:
    - Front-Matter Extension
    - Tables Extension
- how to enable these extensions from the command line

## Prerequisites

The following sections assume that you have already [installed PyMarkdown](./installation.md)
and are reasonably comfortable with [command line usage](./general.md). If you are
not, please refer to the links above to help you get started.

## Why Is This Important?

PyMarkdown's Markdown parser is based on the [GitHub Flavored Markdown](https://github.github.com/gfm/)
(GFM) specification. That specification includes five capabilities that are considered
optional. In addition, our team has implemented two other capabilities that enhance
PyMarkdown's ability to handle Markdown that is commonly seen by our users.

In total, PyMarkdown supports seven extensions.
Most of them are disabled by default, including the [Front-Matter Extension](../advanced_extensions.md#front-matter-extension)
and the [Tables Extension](../advanced_extensions.md#markdown-tables), to avoid
surprising behavior when you first run PyMarkdown on existing Markdown files. Therefore,
you turn them on only when you need their behavior for your own Markdown files.
You are most likely to enable these two first, so this Quick Start guide focuses
on them.

All seven extensions are briefly introduced in the following sections. For more
information on extensions and details on all extensions, refer to the [User Guide](../user-guide.md#extensions).

### Front-Matter Extension

If you use Markdown with a static-site generator or transformation tool, it likely
supports Front-Matter. Front-Matter carries metadata for the file without changing
the Markdown body of that file. The tools use the Front-Matter to classify and annotate
documents, sometimes providing configuration that alters how each document is rendered.

Many of the pages that are part of our PyMarkdown documentation are created with
Front-Matter located at the top of the file. This file contains a Front-Matter
block of text with the content:

```YAML
---
summary: Quick-Start documentation on how to use PyMarkdown Extensions.
authors:
  - Jack De Winter
---
```

This Front-Matter block of YAML provides two useful pieces of information: a summary
of the document itself and who the authors of the document are. This information
is hidden from the reader of the rendered Markdown document, but provides important
information to our static-site generator [MkDocs](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data).

If you do not enable the Front-Matter Extension, PyMarkdown treats this block as
regular content. That can cause Rule Plugins whose rules require a heading or paragraph
at the top of the file to complain. When the extension is enabled, that same block
is classified as metadata, so those Rule Plugins no longer see it as content and
stop
reporting problems.

### Tables Extension

Paragraphs and lists work for many documents, but tables can make some information
much clearer and easier to read. A good example of this is data concerning the fictitious
Bedrock Bowling League and its two inaugural members:

```markdown
| User   | Best Score | Average Score |
| ------ | ---------- | ------------- |
| Fred   | 200        | 185           |
| Barney | 250        | 182           |
```

which renders as:

| User   | Best Score | Average Score |
| ------ | ---------- | ------------- |
| Fred   | 200        | 185           |
| Barney | 250        | 182           |

While you could present this information in a paragraph, the number would be hidden
between all the words. You could put the information in a list to make it stand out
more, but putting that information in a table really helps us see the data clearly.

With the Tables Extension enabled, PyMarkdown understands this structure as a table,
so Rule Plugins that check alignment, header presence, or cell content operate on
each
column and row instead of treating it as a long paragraph of text and punctuation.

## What Happens If You Do Not Enable These Extensions?

If you scan either of the examples above without enabling extensions, PyMarkdown
sees only plain text. The Front-Matter looks like two thematic breaks with text
between them, and the table looks like a paragraph filled with `|` and `-` characters.
Because PyMarkdown does not recognize them as Front-Matter or a table, any Rule Plugins
that rely on that structure will not behave as you expect.

For example, without the Front-Matter Extension, a Rule Plugin that checks for
"too many
thematic breaks" might treat the `---` lines in your Front-Matter as regular content
and
report extra Rule Failures such as "too many thematic breaks in a row." Once you
enable
the Front-Matter Extension, those same `---` lines are correctly treated as metadata,
so
that Rule Plugin no longer reports those failures. The Rule Plugin stays enabled
in both
cases; enabling the extension only changes how PyMarkdown interprets the content.

## Enabling These Two Extensions

While there are more complex ways of [enabling these extensions](../advanced_configuration.md#enable-extensions),
the simplest way to enable them is from the command line. Assuming we are
starting with a simple example, such as the [Scan A Simple File](./scanning.md#scan-a-single-file)
from our "Quick Start: Scanning Markdown Files" guide, we can modify it to enable
both extensions by
doing the following.

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown --enable-extensions markdown-tables,front-matter scan sample.md
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown --enable-extensions markdown-tables,front-matter scan sample.md
    ```

<!-- pyml enable code-block-style-->

We simply use the `--enable-extensions` command-line argument and follow it with
a comma-separated list of extension identifiers. The identifier for the Tables Extension
is `markdown-tables` and the identifier for the Front-Matter extension is `front-matter`.

You may not see an obvious difference at first, but Rule Plugins that rely on Front-Matter
or tables will either start producing results or change how they report issues once
these extensions are enabled,
**even though you have not changed which Rule Plugins are enabled.**

## Where to Go From Here?

On this page, you have learned:

- what PyMarkdown extensions are and why they matter
- how the Front-Matter and Tables extensions affect how PyMarkdown interprets your
  files
- how to enable these extensions from the command line

**If** you need some review:

- Select [Quick Start: Introduction](./index.md) for an overview of all Quick Start
  guides.
