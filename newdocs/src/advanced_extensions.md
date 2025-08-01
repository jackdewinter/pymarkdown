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

## Enabling and Disabling Extensions

Keeping in mind the [configuration layering](https://application-properties.readthedocs.io/en/latest/getting-started/#configuration-ordering-layering)
that occurs, the most direct way of enabling extensions is through the `--enable-extensions`
command line option.  Because almost every extension is disabled by default (except
for `linter-pragmas`), the `--disable-extensions` command line option was dropped
to reduce command line option clutter.  Note that the `--enable-extensions` option
is a [specific command line setting](https://application-properties.readthedocs.io/en/latest/command-line/#specific-command-line-settings),
overriding every other enable/disable configuration for the extensions
specified by other command line arguments.

After the specific command line setting comes the `--set` argument which is detailed
in the Advanced Configuration document under
[General Command Line Settings](https://application-properties.readthedocs.io/en/latest/command-line/#general-command-line-settings).
Using the format `--set=extensions.{id}.enabled=$!True` (with the escaping of
[certain characters](https://application-properties.readthedocs.io/en/latest/command-line/#special-characters-and-shells)
being required), a single extension may be enabled.  Disabling an extension is
as simple as replacing the `True` with a `False`.

Finally, there are the [configuration files](./advanced_configuration.md/#configuration-files).
The configuration files provide a more compact and easier way to set configuration
item values. The configuration files are available in JSON, YAML, and TOML formats,
with configuration files specified on the command line as well as implicit configuration
files that are searched for in the current directory when the application starts.
These tend to be used for more static configuration settings and can easily be shared
between projects.

## Extension Configuration

Most extensions do not have configuration, as they are changing the way that the
Markdown document is parsed.  However, where configuration is required, please follow
the documentation for [rule plugins](./advanced_plugins.md),
as the only difference is the word `extensions`
in the configuration item name instead of the word `plugins`.

## List of Extensions

For a full list of extensions, check out the [extensions list](./extensions.md).
