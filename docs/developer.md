# Developer Documentation

This document is provided to help developers extend the PyMarkdown project to
solve their immediate needs.  This is meant to be an evolving document, growing
with the needs of any developers who want to help out with the project or
develop plugins to work with the project.

In general, we need your help to allow these documents to grow and encompass
your needs.  If there is something that you would like to see in this
documentation, please look for
[an existing issue](https://github.com/jackdewinter/pymarkdown/issues)
or create one if one that does not exist.

## Introduction

From a development point of view, the project itself is broken down into three
aspects: token parsing, document generation, and rule plugins.

## Token Parsing and the Markdown Token Stream

The PyMarkdown project is built on the GitHub Flavored Markdown specification,
[available here](https://github.github.com/gfm/).  Where there are gaps in
that specification, there is a strong inclination to follow the CommonMark
Spec, [available here](https://spec.commonmark.org/).  To achieve this goal,
the parsing tests generate tokens and then use the HTML Generator (described
in the following section), to generated compliant HTML.  This HTML is then
compared against the output from
[BabelMark 2](https://johnmacfarlane.net/babelmark2/), specifically against
the output for the CommonMark parser.

When it comes down to it, the parsing of most tokens follow their logical
appearance in the Markdown document.  On the outside are container tokens,
processed and handled before anything else.  Once that processing is done,
the remainder of the line is processed for the start of or continuation of
any leaf blocks.  Once all that processing has been completed, a second full
pass is done on given Text tokens to look for any Inline tokens.

This may seem like the parser was written by someone who was overly pedantic,
but this was done on purpose.  By organizing the parser in this manner, there
are three independent concerns, each based on a single group of tokens. While
care must be maintained going across a boundary, once that boundary is crossed,
the previous concern does not have (mostly) any bearing on what is being done
by the new processor.  That means the code for each processor can be written
with that single responsibility in mind.

### A Small Deviation

Because of the way that the parser evolved, there is a slight deviation to
these rules.  Specifically, the order of the Blank Line token and the end
List token are backwards.  When reading a Markdown document such as:

```Markdown
- this is a line

```

it is natural to think that the tokens are: start List token, start Paragraph
token, Text token, end Paragraph token, end List token, and Blank Line token.
However, for historical reasons, the order of the last two tokens is inverted.

There are some plans to order these two tokens properly. But as there are rules
that now depend on that order, extra throught has to be placed on how to
achieve that goal without disrupting any of the rules.

### Container Block Processor

TBD

### Leaf Block Processor

TBD

### Inline Processor

TBD

### Extensions

TBD

## Document Generation and Parsing Validation

TBD

## Rule Plugins and Analyzing Markdown Documents

Before going to our document on
[Writing Rule Plugins](writing_rule_plugins.md),
it is useful to understand how these plugins work at a high level.

With the PyMarkdown parser providing a stream of tokens that have been
validated by the HTML Generator and the Markdown Generator, rules can be
developed that analyze the stream of tokens.  By providing that stream of
valid tokens to developers, rules developers can have confidence that the
basis for their rules is based on solid, well-tested code.  After all, before
those tokens get to their rules, they have passed tests against the definitive
specification HTML as well as against their own reconstitution of the Markdown
that created them.  This has been woven into the fabric of the project to
provide rule developers with just that confidence.

From a design point of view, a rule is just a subclass of the `Plugin`
class that is contained within its own module.  It is referred by some of the
documentation as a "rule plugin" because the rule is loaded dynamically at
run-time and is independeant of the main program execpt for the interface
provided by the `Plugin` class.  This design allows for external rules to be
developed and added without requiring any changes on behalf of the PyMarkdown
project itself.

When the PyMarkdown application is started, it reads its configuration to
determine where to look for rule plugins and which ones are enabled. With that
list, all available rule plugins are loaded and verified for their integrity
to the interface.  But once that has been accomplished, that rule plugin
remains in memory for the entire duration that the PyMarkdown application is
active.  The `PluginManager` class is responsible for maintaing access to
every plugin during the lifetime of the application.

Upon initialization of each rule plugin, the `get_details` function is called
for each rule plugin, returning a populated instance of the `PluginDetails`
class.  This provides clear information to the `PluginManager` class and to the
PyMarkdown application on what the rule plugin does and how to related
information about the rule plugin.

After the `get_details` function is called, the optional `initialize_from_config`
function is called.  If provided by the rule plugin, this function is used to
fetch configuration from the PyMarkdown configuration system upon initialization.
[describe - facade only for rule's config]

Once initialization is complete, a life-cycle takes over for the scanning
of each Markdown document.

starting_new_file

next_token
report_next_token_error

next_line
report_next_line_error

completed_file

possible -> MD005, Md007
possible -> MD019/MD021, MD023

Md001 Atx/SetExt hash_count
MD004 UnorderedListStartMarkdownToken list_start_sequence
Md005 NewListItemMarkdownToken indent_level, extracted_whitespace
      UnorderedListStartMarkdownToken indent_level, extracted_whitespace, column_number
      OrderedListStartMarkdownToken indent_level, extracted_whitespace, column_number
MD007 NewListItemMarkdownToken indent_level, extracted_whitespace
      UnorderedListStartMarkdownToken indent_level, extracted_whitespace
MD009 line -> no trailing spaces
MD010 line -> detabify
MD019 AtxHeadingMarkdownToken extracted_whitespace
MD021 AtxHeadingMarkdownToken extracted_whitespace, extra_end_data
MD023 AtxHeadingMarkdownToken extracted_whitespace
MD029 OrderedListStartMarkdownToken list_start_content
MD035 ThematicBreakMarkdownToken start_character,rest_of_line
MD037 TextMarkdownToken (within emphasis) token_text
MD038 InlineCodeSpanMarkdownToken span_text
MD039 LinkStartMarkdownToken text_from_blocks
MD047 line -> adds newline to end
MD048 FencedCodeBlockMarkdownToken fence_character
