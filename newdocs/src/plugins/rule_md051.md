# Rule - MD051

| Property | Value |
| --- | --- |
| Aliases | `md051`, `link-fragments` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Local link fragments should be valid.

## Reasoning

### Correctness

Broken internal links degrade the reader's experience: a reader who clicks a
link expecting to land on a specific section, only to find the fragment does not
resolve to any target, is left with a confusing, unhelpful result. Unlike
external targets, local link fragments (such as `#target`) are defined entirely
within the same document, so there is no reason not to validate them.

### Spec Basis

There is no official [GitHub Flavored Markdown](https://github.github.com/gfm/)
specification for what constitutes a valid link target.
This rule collects the target text from one of the following Markdown
elements:

- **ATX heading:** any text on the same line, excluding any trailing
  `#` characters that are part of an ATX heading close.
- **Setext heading:** any text that is part of the paragraph before the
  Setext heading characters.
- **HTML Blocks and Raw HTML:** the `name` attribute for an `a` start tag
  (i.e. `<a name="bookmark">`) or any start tag's `id` parameter (i.e. `<a id="bookmark">`).

For the ATX and Setext heading cases, the collected text is transformed into a
fragment using the historic [GitHub heading algorithm](https://github.com/gjtorikian/html-pipeline/blob/f13a1534cb650ba17af400d1acd3a22c28004c09/lib/html/pipeline/toc_filter.rb).
The transformation steps, and how they are affected by configuration, are
documented in the [Configuration](#configuration) section.

## Examples

### Failure Scenarios

This rule triggers when there is an inline link with a local fragment specified,
but the document does not contain any targets with that name.

```Markdown
# Heading Name

[Local Link](#local-fragment)
```

> **Explanation**: This example fails because the inline link points to the local fragment `#local-fragment`, but the document contains no heading (or other target) that generates that fragment. The only heading, `# Heading Name`, produces the fragment `#heading-name` (lowercased, with spaces converted to dashes). Because the referenced fragment does not resolve to any real target, the unresolved fragment is invalid.

Unlike the previous example, which used an inline link, this scenario places the invalid fragment inside a **link reference definition**. The rule triggers on the definition itself rather than on the shorter reference that uses it.

```Markdown
[Local Link][Local Link]

[Local Link]: #local-fragment
```

> **Explanation**: This example fails for the same underlying reason as the previous one, but the invalid fragment is defined in a **link reference definition** rather than written inline. The definition `[Local Link]: #local-fragment` points to a fragment that no target in the document generates. Because the rule evaluates the destination of the link regardless of how it is written, it triggers on the link reference definition itself — not on the shorter `[Local Link]` reference that uses it — since that definition is where the unresolvable fragment actually lives.

Unlike the previous examples, which used ATX headings, this scenario uses a
**Setext heading**. The heading text still generates a fragment, but the
referenced fragment does not match it.

```Markdown
Heading Name
============

[Local Link](#heading-name-xyz)
```

> **Explanation**: This example fails because the Setext heading `Heading Name` generates the fragment `#heading-name` (text lowercased, spaces converted to dashes), but the link points to `#heading-name-xyz`, which no heading or target produces. The fragment is therefore unresolved and invalid, even though the heading is a Setext heading rather than an ATX heading.

Unlike the previous examples, which relied on headings, this scenario uses an
**HTML `id` attribute** as the only target in the document. The referenced
fragment does not match the `id`.

```Markdown
<a id="real-bookmark"></a>

[Local Link](#wrong-bookmark)
```

> **Explanation**: This example fails because the only target in the document is the HTML element with `id="real-bookmark"`, which provides the fragment `#real-bookmark`. The link points to `#wrong-bookmark`, which matches neither the HTML `id`/`name` target nor any heading, so the fragment does not resolve to any target in the document.

Unlike the previous examples, this scenario shows that the referenced fragment
matches the heading **only in case**. With the default `ignore-case` setting of
`True`, a case-only difference is ignored, so this specific form is the one that
*would* fail if `ignore-case` were `False`.

```Markdown
# Heading Name

[Local Link](#HEADING-NAME)
```

> **Explanation**: This example shows the case-sensitivity behavior controlled by `ignore-case`. The heading `# Heading Name` generates the lowercase fragment `#heading-name`. The link uses the fragment `#HEADING-NAME`, which differs only in case. With `ignore-case` set to `True` (the default) the rule treats these as matching and does not flag this; with `ignore-case` set to `False` the case difference is not ignored, so the fragment no longer resolves and the rule triggers. This scenario demonstrates that case-mismatched fragments are a distinct failure mode governed by the `ignore-case` setting.

### Correct Scenarios

This rule does not trigger when there is a link with a local fragment specified,
with the document containing a target with that name.

```Markdown
# Heading Name

[Local Link](#heading-name)
```

> **Explanation**: This example passes because the local fragment `#heading-name` matches the fragment generated by the heading `# Heading Name`. The heading text is converted to lowercase, punctuation is removed, and the space is converted to a dash, producing exactly `#heading-name`. Since that target exists in the document, the link resolves to a real section and a reader clicking it is taken to the expected place. Because the fragment is valid, the rule does not trigger.

Unlike the previous correct scenario, where a fragment must match a generated heading, this scenario uses the special target `#top`, which the rule recognizes without requiring a corresponding heading or element in the document.

```Markdown
[Top Of Page](#top)
```

> **Explanation**: This example passes because `#top` is a universally recognized special target that does not require a corresponding heading or element in the document. The rule exempts this well-known fragment from validation, so the link resolves to the top of the page without needing a matching target.

Unlike the previous correct scenario, this example's link fragment (`#figure-1a`) would normally be invalid because no heading generates that fragment. It is allowed here because it matches the `ignore-pattern-regex` pattern.

```Markdown
The above [figure](#figure-1a).
```

> **Explanation**: This example passes because the configuration `ignore-pattern-regex` is set to `^figure-`. The rule consults this pattern before evaluating the fragment, and because `figure-1a` matches the `^figure-` prefix, the rule skips validation of that fragment. This is the intended mechanism for tolerating generator-added anchors (e.g., image captions labelled `figure-1`, `figure-2`, …) that do not correspond to any author-defined heading.

Unlike the previous examples, this scenario involves a **repeated heading**, so the
heading the link intends is the second occurrence. Because the rule appends an
incrementing integer to repeated headings, the second one resolves to
`#heading-name-2`, not the bare `#heading-name`.

```Markdown
# Heading Name

some text

# Heading Name

[Local Link](#heading-name-2)
```

> **Explanation**: This example passes because the document contains two occurrences of the heading `Heading Name`. The rule appends an incrementing integer to duplicate headings to ensure unique fragments: the first occurrence generates `#heading-name` and the second generates `#heading-name-2`. The link `[Local Link](#heading-name-2)` correctly targets the second occurrence's fragment, which is a valid, resolvable target in the document.

## Fix Description

This rule cannot be auto-fixed because the only valid correction is to change the fragment to point at a target the author actually intended. PyMarkdown cannot reliably infer that intent from an invalid fragment alone (for example, `#local-fragment` could be a typo for `#heading-name`, `#local-fragments`, or a new heading the author plans to add). Because any auto-correction could silently redirect the reader to the wrong section, the rule reports the failure and leaves the correction to the author.

## Configuration

| Prefixes |
| --- |
| `plugins.md051.` |
| `plugins.link-fragments.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `ignore-case` | `boolean` | `True` | Whether the Rule Plugin ignores case when matching local link fragments. |
| `ignore-pattern-regex` | `string` | `(empty string)` | If not empty, regular expression for link fragment text to ignore. |

### Fragment Computation

The HTML Block and Raw HTML targets are used directly, specified by the tag's
`id` or `name` attribute value.
For the ATX heading and Setext heading target information, the text contained
within the heading must be processed to determine the appropriate fragment.
While section links are not part of the CommonMark specification, this rule
enforces the historic [GitHub heading algorithm](https://github.com/gjtorikian/html-pipeline/blob/f13a1534cb650ba17af400d1acd3a22c28004c09/lib/html/pipeline/toc_filter.rb)
to generate those fragments by:

- Converting the text to lowercase (if `ignore-case` is set to `True`)
- Removing any punctuation characters
- Converting any spaces to dashes
- Appending an incrementing integer (as needed for uniqueness)
- URI-encoding the result

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

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD051](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md051---link-fragments-should-be-valid).

### Differences From MarkdownLint Rule

Supported by the inspiration of this rule, but not by this rule itself, is the Line and Line/Column link format. At its core, this format allows for link fragments
formatted
as `#l89` to specify that the 89th line of the current document should be highlighted
and `#L19C5-L21C11` to specify that from
line 19 column 5 to line 21 column 11 of the current document should be highlighted.

However, during our testing of this format, two observations kept coming up. The
first was that
pointing to a Markdown document on GitHub is not easy. To view the Markdown itself,
you
need to add `?plain=1` to the end of the URL [like this](https://github.com/jackdewinter/pymarkdown/blob/main/README.md?plain=1)
just to point at the Markdown document itself. Then, to point to the correct line,
say line 40, you need to
add `?plain=1#L40` to the end of the URL, [like this](https://github.com/jackdewinter/pymarkdown/blob/main/README.md?plain=1#L40).
That makes it really unclear whether you are even adding a link fragment to the
document itself, or appending
some text to the value for the `plain` option of the URL.

The second observation was that GitHub's processing of these link fragments is
spotty at best.  After reading [this page](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-a-permanent-link-to-a-code-snippet#linking-to-markdown),
our team tried over 10 combinations to help us figure out how to test the link fragment. Every one was accepted by GitHub — even malformed ones such as `#xL40-L41` that we expected to be rejected. Because of this, we were not sure how to properly test these formats, as we could not determine which fragments were actually valid.


Because of these observations and the questions that they raised to our team, we
decided to not support these Line and Line/Column formats due to the ambiguity issues
raised by the first and second observations.
