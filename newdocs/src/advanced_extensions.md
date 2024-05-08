---
summary: More information on extensions and which extensions are currently available.
authors:
  - Jack De Winter
---

# Advanced Extensions

In the [Advanced Configuration](./advanced_configuration.md#extensions)
document, we touched briefly on extensions and how they impact the PyMarkdown
application.  To reiterate, extensions are features that are implemented
in addition to the base [GitHub Flavored Markdown](https://github.github.com/gfm/)
specification, changing how the PyMarkdown parser interprets the Markdown document.

The GitHub Flavored Markdown is a relatively static document that provides
a solid foundation for parsing any Markdown document.  If the authors of a
given parser want to add any non-standard parsing of a Markdown document, they must
extend the specification and provide their own information on how their extension
impacts the parsing of a Markdown document.  While the quality of that information
may be decent, the quality of that information differs wildly between parsers
and their maturity.

As the PyMarkdown linter uses its own parser as the foundation for its linting
services, our application must also provide similar extensions to the ones that
those popular parsers provide.  If we are lucky, their documentation is good
enough that we can easily determine the features and settings for our own extension,
seeking to match as many popular parsers as possible.

However, no matter how hard we try, we cannot promise to match the functionality
of all Markdown parsers.  What is within our team's abilities is to promise to
try our best to clearly articulate how our extensions work, what parsers we have
tested it against, and what configuration works best.  We are confident that this
will allow our users to leverage PyMarkdown and its extensions to match their
parser's behavior as closely as possible.

## Categories

There are two categories of extensions: GitHub Flavored Markdown extensions and
community extensions.  The GitHub Flavored Markdown extensions are parts of
that specification that contain a `(extension)` suffix after their title.
The specification clearly notes each of the five extension elements, implying that
there is no requirement for a Markdown parser to implement these features
to be considered GitHub Flavored Markdown compliant. However, as these extensions
specify a useful feature for a Markdown parser to have, it is also implied that if
the parser team decides to implement the feature, they must adhere those extensions
to the specification to keep their GitHub Flavored Markdown compliant status.

Other extensions fall into the category of community extensions and may
stretch their impact on parsing Markdown a bit further than the GitHub Flavored Markdown
specification. In the GitHub Flavored Markdown specification's [Introduction](https://github.github.com/gfm/#introduction),
it states:

> GitHub Flavored Markdown, often shortened as GFM, is the dialect of Markdown
> that is currently supported for user content on GitHub.com and GitHub Enterprise.
>
> This formal specification, based on the CommonMark Spec, defines the syntax and
> semantics of this dialect.

After checking with the specification authors, we can confirm that their intention
was to only deal with concerns regarding the parsing of Markdown document.  They
specifically wanted to keep a narrow focus on the grammar of Markdown, the parts
of Markdown that they believed most implementors could come to common ground on.

### GitHub Flavored Markdown Extensions

There are a limited number of elements in the [GitHub Flavored Markdown](https://github.github.com/gfm/)
specification that are marked as extensions.  These are:

- Tables
- [Task List Items](./extensions/task-list-items.md)
- [Strikethrough](./extensions/strikethrough.md)
- [Autolinks (Extended)](./extensions/extended-autolinks.md)
- [Disallowed Raw HTML](./extensions/disallowed-raw-html.md)

These five extensions round out the requirements for full compliance to the entire
GitHub Flavored Markdown specification.  Except for the Table extension, the other
extensions are completed, tested, and part of current releases.

The reason that Tables is not yet implemented is a simple one: time.  The other
GFM extensions are all modifications on existing elements.  The Tables extension
adds a brand-new leaf block type to the document.  While the base parts of adding
that support are going to be relatively easy, our team knows that the sheer number
of test scenarios for a new leaf block element is going to be huge.  Rather than
rush and do a poor job, we want to make sure we start it and complete
it with the quality it deserves.

Work is slated to begin on the Tables extension as soon as
version 1.0.0 is complete.

### Community Extensions

These extensions are the community extensions:

- [Front-Matter](./extensions/front-matter.md)
- [Pragmas](./extensions/pragmas.md)

The reason that we mentioned the GFM specification's focus on grammar is that two
of our most common extensions work to process information that falls outside of
that focus.
Neither one of these extensions works on how the Markdown itself is interpreted,
therefore
falling outside of the purview of the GFM specification.  However, it should be
evident
that both extensions are useful.

The first example is the [front-matter](./extensions/front-matter.md)
extension, working with PyMarkdown's parser to allow for a block of YAML text
at the start of the document.  While this YAML block of text is not Markdown,
it is an important feature to have for supporting applications that aggregate
Markdown documents.  Aggregators, such as the [MkDocs](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data)
application used for our documentation, use this YAML front-matter block to provide
information on
the page itself.  Without an extension to process this YAML block, it would be
wrongly parsed as normal Markdown text, causing all sorts of issues.

Our second example is the [pragmas](./extensions/pragmas.md) extension, working
with the parser to allow
specialized inline comments that disable rules for a specific number of lines in
the Markdown document.
When writing Markdown documents, there are times that you have a good reason to
break a rule
for a small number of instances.  That is where this extension's usefulness comes
into play.  If not for this extension, the only options would be to 1) disable
the rule, and 2) fix the issue.  We acknowledge that there are times that neither
of those two options are the right choice, hence this extension.

Community extensions come into play in these two cases, as well as others yet to
be implemented.  The extensions will allow our team to grow PyMarkdown to handle
more scenarios and increase the accuracy of our linting rules.

## Enabling and Disabling

Each extension's documentation specifies whether it is enabled or disabled by default.
This information is also available on the command line by using the
[`extension` command](./user-guide.md#extension-command).

Examples of enabling an extension from configuration files are given in the
examples under the documentation for [Configuration File Types](./advanced_configuration.md/#configuration-file-types).
Similarly, examples of enabling an extension from the command line are
provided under the documentation for [Configuration Item Types](./advanced_configuration.md/#typing-examples).
The only difference between enabling and disabling an extension is whether
the `enabled` item is assigned a boolean value of `True` or `False`.

Note that for the command line, the assignment of a boolean value requires
special characters, as detailed in the documentation on [Special Characters and Shells](./advanced_configuration.md#special-characters-and-shells).

## Extension Configuration

Most extensions do not have configuration, as they are changing the way that the
Markdown document is parsed.  However, where configuration is required, please follow
the documentation for [rule plugins](./advanced_plugins.md),
as the only difference is the word `extensions`
in the configuration item name instead of the word `plugins`.

## Full List of Extensions

- [Front-Matter](./extensions/front-matter.md)
- [Pragmas](./extensions/pragmas.md)
- [Task List Items](./extensions/task-list-items.md)
- [Strikethrough](./extensions/strikethrough.md)
- [Autolinks (Extended)](./extensions/extended-autolinks.md)
- [Disallowed Raw HTML](./extensions/disallowed-raw-html.md)
