# Rule - MD051

| Property | Value |
| --- | -- |
| Aliases | `md051`, `link-fragments` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Local link fragments should be valid.

## Reasoning

### Correctness

In our opinion, nothing annoys readers of documents more than trying to follow
a link only to find out that it does not go where it is supposed to. While
it is often outside of the scope of a single document to validate all link
targets, there is no reason why local link fragments (such as '#target') should
not be validated.

## Examples

### Failure Scenarios

This rule triggers when there is an inline link with a local fragment specified,
but the document does not contain any targets with that name.

````Markdown
# Heading Name

[Local Link](#local-fragment)
````

If non-inline links are used with a link reference definition, this rule triggers
on the link reference definition, not the link to that definition.

```Markdown
[Local Link][Local Link]

[Local Link]: #local-fragment
```

### Correct Scenarios

This rule does not trigger when there is a link with a local fragment specified,
with the document containing a target with that name.

````Markdown
# Heading Name

[Local Link](#heading-name)
````

### Link Targets

While these is no official [Github Flavored Markdown](https://github.github.com/gfm/)
specification
for what consistutes a valid link target, the [GitHub heading algorithm](https://github.com/gjtorikian/html-pipeline/blob/f13a1534cb650ba17af400d1acd3a22c28004c09/lib/html/pipeline/toc_filter.rb)
can be used to generate the expected link fragment itself. To do that, the text
is collected from one of the following Markdown elements:

- **ATX heading:** any text on the same line, excluding any trailing
  `#` characters that are part of an ATX heading close
- **SetExt heading:** any text that is part of the paragraph before the
  SetExt heading characters
- **HTML Blocks and Raw HTML:** the `name` attribute for an `a` start tag
  (i.e. `<a name="bookmark">`) or any start tag's `id` parameter (i.e. `<a id="bookmark">`)

### Translation From Heading to Fragment

The HTML Block and Raw HTML option above provide clear targets, specified by the
tag's `id` or `name` attribute value.
For the ATX heading and SetExt heading target information, the text contained within
the heading must
be processed to determine the appropriate fragment for that heading.
While section links are not part of the CommonMark specification; this rule enforces
the historic [GitHub heading algorithm](https://github.com/gjtorikian/html-pipeline/blob/f13a1534cb650ba17af400d1acd3a22c28004c09/lib/html/pipeline/toc_filter.rb)
to generate those fragments by:

- Converting the text to lowercase (if `ignore-case` is set to `True`)
- Removing any punctuation characters
- Converting any spaces to dashes
- Append an incrementing integer (as needed for uniqueness)
- URI-encode the result

Examples of this are:

- Simple text
    - Example: `# Heading Name` --> `#heading-name`
- Simple text with punctuation characters
    - Example: `# Heading & Name !` --> `#heading--name-`
- Unicode text (Ã = `\xC3` in unicode, when encoded in utf-8, becomes `\xC3\xA3`)
    - Example: `# Heading Ã name` --> `#heading-%C3%A3-name`
- [Backslash escapes](https://github.github.com/gfm/#backslash-escapes)
    - Example: `# Heading \* Name` --> `#heading--name`
- [Numeric character references](https://github.github.com/gfm/#entity-and-numeric-character-references)
    - Example: `# Heading &#x0041; Name` --> `#heading-a-name`
- [Entity character references](https://github.github.com/gfm/#entity-and-numeric-character-references)
    - Example: `# Heading &copy; Name` --> `#heading--name`
- [Emphasis](https://github.github.com/gfm/#emphasis-and-strong-emphasis)
    - Example: `# Heading *foo* Name` --> `#heading-foo-name`
- [Links](https://github.github.com/gfm/#links)
    - Example: `# Heading [Google](www.google.com) Name` --> `#heading-google-name`
- [Code spans](https://github.github.com/gfm/#code-spans)
    - Example: ``# Heading `foo` Name`` --> `#heading-foo-name`
- [URI Autolinks](https://github.github.com/gfm/#autolinks)
    - Example: `# Heading <http://foo.bar.baz> Name` --> `#heading-httpfoobarbaz-name`
- [Email Autolinks](https://github.github.com/gfm/#autolinks)
    - Example: `# Heading <foo@bar.example.com> Name` --> `#heading-foobarexamplecom-name`
- [Raw HTML](https://github.github.com/gfm/#raw-html)
    - Example: `# Heading <del>d</del> Name` --> `#heading-d-name`

### Special Targets

The sole special target that is universally supported is the `#top` target. This
target is used to return the reader to the top of the current page. An example of
this is [this link](#top).

### Excluding Targets

There are special cases where link fragments are automatically added during the
Markdown-to-HTML
generation process, to aid in navigation. The most obvious one is that some generators
will add
link anchors underneath references images, labelling those link anchors as `figure-1`,
`figure-2`
and so on.

The `ignore-pattern-regex` configuration item allows for a regular expression to
be specified
that is used to ignore any matching link fragments. For the above example with
the `figure-`
prefix for images, setting the `ignore-pattern-regex` configuration item value to
`^figure-`
will cause this rule not to trigger for any link fragment that starts with `figure-`.

### Not Supported

Supported by the inspiration of this rule, but not by this rule itself is the Line
and Line/Column link format. At its core, this format allows for link fragments
formatted
as `#l89` to specify that the 89th line of the current document should be highlights
and `#L19C5-L21C11` to specify that from
line 19 column 5 to line 21 column 11 of the current document should be highlighted.

However, during our testing of this format, two observations were repeated. The
first was that
pointing to a Markdown document on GitHub is not easy. To view the Markdown itself,
you
need to add `?plain=1` to the end of the url [like this](https://github.com/jackdewinter/pymarkdown/blob/main/README.md?plain=1)
just to point at the Markdown document itself. Then, to point to the correct line,
say line 40, you need to
add `?plain=1#L40` to the end of the URL, [like this](https://github.com/jackdewinter/pymarkdown/blob/main/README.md?plain=1#L40).
That makes it really unclear whether your are even adding a link fragment to the
document itself, or appending
some text to the value for the `plain` option of the URL.

The second observation was that GitHub's processing of these link fragment's is
iffy at best.  After reading [this page](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-a-permanent-link-to-a-code-snippet#linking-to-markdown),
our team tried over 10 trivial combinations to help us figure out how to test the
link fragment. They all worked. Simple ones, such as `#xL40-L41` that we expected
to fail did not. Because of this, we were
not sure how to properly test these formats, as we were unsure of what formats were
actually
allowed.

Because of these observations and the questions that they raised to our team, we
decided to not support these Line and Line/Column formats due to the ambiguity issues
raised by the first and second observations.

## Fix Description

The reason for not being able to auto-fix this rule is certainty.

## Configuration

| Prefixes |
| --- |
| `plugins.md051.` |
| `plugins.link-fragments.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `ignore-case` | `boolean` | `True` | Whether the Rule Plugin ignores case when matching local link fragments. |
| `ignore-pattern-regex` | `str` | `(empty string)` | If not empty, regular expression for link fragment text to ignore. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD051](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md051---link-fragments-should-be-valid).
