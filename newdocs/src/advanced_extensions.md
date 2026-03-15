---
summary: More information on extensions and which extensions are currently available.
authors:
  - Jack De Winter
---

# Advanced Extensions

In the [Advanced Configuration](./advanced_configuration.md#extensions) document,
we briefly introduced PyMarkdown extensions and their impact on PyMarkdown.
This guide covers the extensions that PyMarkdown adds on top of
[GitHub Flavored Markdown](https://github.github.com/gfm/) specification: what they
do, how they affect parsing, and how to enable or configure them.

PyMarkdown uses its own parser as the foundation for linting, so our extensions
must behave consistently with extensions in popular Markdown parsers.

When the upstream documentation is clear, we infer the intended behavior and configuration
by matching the rendered HTML and, where possible, the tokenization rules of reference
parsers.

We do not aim for perfect parity with every Markdown parser. Instead, we focus on
predictable, well‑documented behavior that is easy to configure.

When we intentionally diverge from other parsers, especially in ways that could
break existing Rule Plugins, we document that behavior and its rationale. That
lets you see exactly where PyMarkdown differs.

## Skipping Ahead

To help you either explore extension concepts or look up specific topics, here is
a roadmap of what this page covers:

- [Rule Plugins vs Extensions](#rule-plugins-vs-extensions)
- [Categories of Extensions](#categories-of-extensions)
    - [Specification Extensions](#specification-extensions)
        - [Tables](#markdown-tables)
        - [Task List Items](#task-list-items)
        - [Strikethrough](#strikethrough)
        - [Autolinks (Extended)](#autolinks-extended)
        - [Disallowed Raw HTML](#disallowed-raw-html)
    - [Requested Extensions](#requested-extensions)
        - [Front-Matter](#front-matter-extension)
        - [Pragmas](#pragmas-extension)
- [Configuring Extensions](#configuring-extensions)

If a topic isn't listed explicitly, look for nearby categories &mdash; for example,
the Front-Matter Extension documentation is under "Categories of Extensions". Your
browser's page search can also help you find specific keys or terms.

## Rule Plugins vs Extensions

This section explains the relationship between Rule Plugins, extensions, and the
parser's Markdown token stream.

In particular, it covers:

- why only rules are called "Rule Plugins"
- how extensions interact with the parser differently than rules
- how changes to the Markdown token stream can affect existing Rule Plugins

In PyMarkdown, both rules and extensions use a plugin architecture, but only rules
are called "Rule Plugins".
We reserve that term for user‑extensible linting rules.

From the outset, we designed Rule Plugins with a true plugin mindset: adding a new
Rule Plugin should be straightforward, and that flexibility is one of PyMarkdown's
strengths.

For you as a user, this means:

- you can add or customize Rule Plugins without changing how Markdown is parsed
- extensions are fewer and more "core"; they change parsing behavior rather than
just linting policy

Because PyMarkdown is a linter, not just an HTML generator, the rules within the
Rule Plugins depend
directly on the Markdown token stream produced by the parser. If we introduce new
token types,
we can accidentally change how those rules see the document, which can cause:

- rules to start failing on documents that previously passed
- rules to silently miss issues they used to detect

To avoid that, we add extensions cautiously and run our full test suite with
each extension both enabled and disabled, so the Markdown token stream stays compatible
for
existing Rule Plugins and you rarely need to change your plugins or configuration.

## Categories of Extensions

Extensions fall into two types: Specification Extensions that follow the GitHub
Flavored Markdown spec, and Requested Extensions that are driven by real‑world
usage and may go beyond the spec's narrow focus on grammar. Specification
Extensions help with GitHub compatibility; Requested Extensions help with
workflow features such as metadata or fine‑grained lint control.

The GitHub Flavored Markdown specification labels certain features with an `(extension)`
suffix. These are optional for
parsers, but if a parser supports them, it should follow the behavior defined in
the specification. PyMarkdown implements all of these as Specification Extensions.

Other extensions are classified as Requested Extensions. They may change how PyMarkdown
processes documents in ways not described by the GFM specification and are not limited
to pure syntax or grammar changes. You typically use these for workflow and tooling
features &mdash; such as metadata for site generators or fine‑grained lint control
&mdash; rather than strict compatibility. For GitHub‑style behavior, you instead
enable the Specification Extensions.

> GitHub Flavored Markdown, often shortened as GFM, is the dialect of Markdown
> that is currently supported for user content on GitHub.com and GitHub Enterprise.
>
> This formal specification, based on the CommonMark Spec, defines the syntax and
> semantics of this dialect.

The specification authors deliberately kept the GitHub Flavored Markdown specification
narrow and grammar‑focused. They included only Markdown elements they expected most
implementors to agree on. Requested Extensions cover practical behaviors that fall
outside this scope. In practice, you enable Specification Extensions when you want
spec‑pure behavior, and Requested Extensions when you need higher‑level workflow
features that the GitHub Flavored Markdown specification intentionally leaves out.

### Specification Extensions

There are a limited number of elements in the [GitHub Flavored Markdown](https://github.github.com/gfm/)
specification that are marked as extensions. These are:

- [Markdown Tables](./extensions/markdown-tables.md)
- [Task List Items](./extensions/task-list-items.md)
- [Strikethrough](./extensions/strikethrough.md)
- [Autolinks (Extended)](./extensions/extended-autolinks.md)
- [Disallowed Raw HTML](./extensions/disallowed-raw-html.md)

These five extensions complete the requirements for full compliance with the GitHub
Flavored Markdown specification. PyMarkdown supports all of these extensions.

#### Markdown Tables

[This extension](./extensions/markdown-tables.md), configured as `markdown-tables`,
follows the GitHub Flavored Markdown specification to provide simple tables in Markdown
documents.

The [Markdown Tables Extension](./extensions/markdown-tables.md#specifics) describes
what constitutes
a table and where tables are valid. With this extension disabled, the following
Markdown is just text. With it enabled, PyMarkdown recognizes it as a table:

```markdown
| foo | bar |
| --- | --- |
| baz | bim |
```

rendering it as:

| foo | bar |
| --- | --- |
| baz | bim |

and a more comprehensive example looks like:

```Markdown
| normal | right | left | center |
| ---    | --: | :-- | :--: |
| baz    | bim | bam | bom |
```

rendering as:

| normal | right | left | center |
| ---    | --: | :-- | :--: |
| baz    | bim | bam | bom |

#### Task List Items

[This extension](./extensions/task-list-items.md), configured as `task-list-items`,
follows the GitHub Flavored Markdown specification to turn certain list items into
checkboxes.
Use it when your documents include GitHub-style checklists. It lets PyMarkdown treat
those items as structured content instead of plain text. Any list item whose text
begins with `[ ]`, `[x]`, or `[X]` and then a space is rendered as a task list item.

With this extension enabled, the following Markdown text:

- [ ] something
- [x] something
- [a] something

is parsed so that the first two bullets are task list items, but the third remains
a normal list item because `[a]` does not match the task list pattern. This produces
this HTML:

<!-- pyml disable-num-lines 5 no-inline-html-->
<ul>
<li><input type="checkbox"> something</li>
<li><input checked="" type="checkbox"> something</li>
<li>[a] something</li>
</ul>

#### Strikethrough

[This extension](./extensions/strikethrough.md), configured as `markdown-strikethrough`,
follows the GitHub Flavored Markdown specification to add a new type of emphasis,
strikethrough
emphasis. Like how the `*` and `_` emphasis characters provide `<em>`/`</em>` and
`<strong>`/`</strong>` emphasis blocks in text, the ~ character provides for
`<del>`/`</del>` emphasis blocks.

The specifics for this extension are simple. For example, with this extension enabled,
this Markdown:

```Markdown
~abc~
```

produces this HTML:

<!-- pyml disable-next-line no-inline-html-->
<del>abc</del>

#### Autolinks (Extended)

[This extension](./extensions/extended-autolinks.md), configured as `markdown-extended-autolinks`,
allows plain text that looks like a URL or email address to be treated as a link,
even without `<` and `>` around it. For example, `www.example.com` and `user@example.com`
become clickable links.

It implements the GitHub Flavored Markdown specification for extended autolinks.
The
[extension specifics](./extensions/extended-autolinks.md#specifics) describe the
exact patterns, including `www` domains, `http`/`https` URLs, email addresses, and
`mailto:` or `xmpp:` links.

For example, with this extension enabled, the following Markdown:

```Markdown
Visit www.commonmark.org/help for more information.
```

renders as:

<!-- pyml disable-num-lines 5 no-inline-html,line-length -->
<p>Visit <a href="http://www.commonmark.org/help">www.commonmark.org/help</a> for more information.</p>

#### Disallowed Raw HTML

[This extension](./extensions/disallowed-raw-html.md), configured as `markdown-disallow-raw-html`,
follows the GitHub Flavored Markdown specification to prevent certain HTML tags
from being
rendered. It does this by replacing the leading `<` of those tags with `&lt;`, which
forces them to render as text instead of HTML.

The `markdown-disallow-raw-html.change_tag_names` configuration item allows for
the set of HTML tags that will undergo this transformation to be changed using a
simple [comma-separated string](./extensions/disallowed-raw-html.md#configuring-tags-to-disallow).
By default, the HTML items that are treated this way are:

- `title`
- `textarea`
- `style`
- `xmp`
- `iframe`
- `noembed`
- `noframes`
- `script`
- `plaintext`

### Requested Extensions

These are the Requested Extensions:

- [Front-Matter](./extensions/front-matter.md)
- [Pragmas](./extensions/pragmas.md)

We highlighted GitHub Flavored Markdown specification's focus on grammar because
our two most common requested extensions &mdash; the Front-Matter Extension and
the Pragmas Extension &mdash; operate outside that scope. They do not change how
Markdown is interpreted, so they fall outside that specification, but they are still
widely useful in real-world workflows.
In practice, you use them to attach metadata (Front‑Matter) and to control lint
behavior around generated or exceptional content (Pragmas) without changing the
underlying Markdown semantics.

#### Front-Matter Extension

[This extension](./extensions/front-matter.md), configured as `front-matter`, allows
PyMarkdown to recognize Markdown "Front-Matter" blocks at the start of a document.
Disabled, Front-Matter blocks are treated as normal content and can trigger Rule
Failures; enabled, they are treated as metadata and excluded from normal Markdown
parsing.

The Front-Matter Extension runs before normal Markdown parsing. It scans for a Front-Matter
block at the very start of the document and, if present, records it as metadata
and excludes it from the Markdown token stream. Rule Plugins only
see it as a single token.

In the Markdown token stream, that token is represented as a `FrontMatterMarkdownToken`,
for example:

- token type: `front-matter`
- boundaries: `start_boundary_line` and `end_boundary_line`
- payload: `collected_lines` for the raw lines, and `matter_map` as a convenient
  dictionary mapping each Front-Matter key to its value

**NOTE:** As a `MarkdownToken` class, the `FrontMatterMarkdownToken` does have a
position. Because it must always exist at the start of the document, that position
is always line 1, column 1.

Front-Matter carries metadata for tools that consume the document but does not change
how the Markdown body is parsed. Static site generators and other aggregators use
this metadata to classify documents and control how they are rendered.

As an example, this page on Advanced Extensions has a Front-Matter block at
the very top that is:

```yaml
---
summary: More information on extensions and which extensions are currently available.
authors:
  - Jack De Winter
---

# Advanced Extensions
...
```

This `Front-Matter` block does not affect how the above Markdown is parsed. However,
aggregators such as [MkDocs](https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data)
rely heavily on the metadata it provides.

For example, with this extension enabled, the internal Markdown token stream will
conceptually look like:

- lines 1-5: Front-Matter token
- line 6: blank line token
- line 7: ATX heading token + text token

Without this extension enabled, the same text is interpreted as:

- line 1: thematic break token
- lines 2-5: SetExt heading token
- line 6: blank line token
- line 7: ATX heading token + text token

#### Pragmas Extension

[This extension](./extensions/pragmas.md), configured as `linter-pragmas`, allows
PyMarkdown to interpret "Pragma" comments that control how Rule Failures are processed.
Use it when you need to suppress or re-enable specific Rule Plugin around generated
content.
It also helps with intentional style deviations that you do not want to fix or flag.

The Pragmas extension does not change how Markdown is parsed. It runs alongside
parsing. When the PyMarkdown linter processes each line, it checks for Pragmas.
If a line contains a Pragma, the Pragma is recorded and the line is removed before
normal processing. As a result, Pragmas are invisible to Rule Plugins because they
never appear in the Markdown token stream.

The full details are in the [Specifics section](./extensions/pragmas.md#specifics);
but, the key behaviors are:

- Disable a Rule Plugin for the next line only:

  ```markdown
  <!-- pyml disable-next-line no-multiple-space-atx -->
  #  My Special Heading
  ```

- Disable and then re-enable a Rule Plugin over a region:

  ```markdown
  <!-- pyml disable no-multiple-space-atx -->
  #  Heading generated by a tool
  #  Another generated heading
  <!-- pyml enable no-multiple-space-atx -->
  ```

If your Markdown generator uses two spaces between `#` and the heading text to
mark a special kind of heading, you may not want to disable `no-multiple-space-atx`
globally. In that case, you can use the following Pragma:

```Markdown
some paragraph

<!-- pyml disable no-multiple-space-atx-->
#  My Bad Atx Heading

some other paragraph
<!-- pyml enable no-multiple-space-atx-->
```

## Configuring Extensions

In configuration, each extension is identified by a short name. For example, the
"Front-Matter Extension" uses the key `front-matter`, and the "Disallowed Raw HTML"
extension uses `markdown-disallow-raw-html`. These names appear under the `extensions`
section in each configuration format.

This section explains how to enable extensions and configure them using command‑line
flags or JSON, YAML, and TOML configuration files.
Currently, only two extensions have extra configuration items &mdash; the
[Disallowed Raw HTML Extension](./extensions/disallowed-raw-html.md) and the
[Front-Matter Extension](./extensions/front-matter.md) &mdash; and their configuration
items are set exactly like [Rule Plugins](./advanced_configuration.md#specific-plugin-settings)
configuration items.

For example, if your documents use Front-Matter blocks and you want to forbid blank
lines
inside that block, while also disallowing the `style` tag and adding a custom `something`
tag, you could use one of the following configurations:

<!-- pyml disable code-block-style-->
=== "Command Line"
    ```sh
    # Extensions can be enabled, but without --set, cannot be configured.
    --enable-extensions front-matter,markdown-tables
    ```
=== "--set Argument"
    ```sh
    --set 'extensions.front-matter.enabled=$!True' \
    --set 'extensions.front-matter.allow_blank_lines=$!False' \
    --set 'extensions.markdown-disallow-raw-html.enabled=$!True' \
    --set 'extensions.markdown-disallow-raw-html.change_tag_names=-style,+something'
    ```
=== "JSON"
    ```json
    {
      "extensions": {
        "front-matter": {
          "enabled": true,
          "allow_blank_lines": false
        },
        "markdown-disallow-raw-html": {
          "enabled": true,
          "change_tag_names" : "-style,+something"
        }
      }
    }
    ```
=== "YAML"
    ```yaml
    extensions:
      front-matter:
        enabled: true
        allow_blank_lines: false
      markdown-disallow-raw-html:
        enabled: true
        change_tag_names : "-style,+something"
    ```
=== "TOML"
    ```toml
    [tool.pymarkdown]
    extensions.front-matter.enabled = true
    extensions.front-matter.allow_blank_lines = false
    extensions.markdown-disallow-raw-html.enabled = true
    extensions.markdown-disallow-raw-html.change_tag_names = "-style,+something"
    ```
<!-- pyml enable code-block-style-->
