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

This rule triggers when there is a link with a local fragment specified, but
the document does not contain any targets with that name.

````Markdown
# Heading Name

[Local Link](#local-fragment)
````

### Correct Scenarios

This rule does not trigger when there is a link with a local fragment specified, with
the document containing a target with that name.

````Markdown
# Heading Name

[Local Link](#heading-name)
````

### Link Targets

While these is no official [Github Flavored Markdown](https://github.github.com/gfm/) specification
for what consistutes a valid link target, the [GitHub heading algorithm](https://github.com/gjtorikian/html-pipeline/blob/f13a1534cb650ba17af400d1acd3a22c28004c09/lib/html/pipeline/toc_filter.rb) can be used to generate the expected link fragment itself. To do that, the text is collected from one of the following Markdown elements:

- **ATX heading:** any text on the same line, excluding any trailing `#` characters that are part of an ATX heading close
- **SetExt heading:** any text that is part of the paragraph before the SetExt heading characters
- **HTML Blocks and Raw HTML:** the `name` attribute for an `a` start tag (i.e. `<a name="bookmark">`) or any start tag's `id` parameter (i.e. `<a id="bookmark">`)

### Translation From Heading to Fragment

The HTML Block and Raw HTML option above provide clear targets, specified by the tag's attribute value.
For the ATX heading and SetExt heading target information, the text contained within the heading must
be processed to determine the appropriate fragment for that heading.
While section links are not part of the CommonMark specification; this rule enforces the historic [GitHub heading algorithm](https://github.com/gjtorikian/html-pipeline/blob/f13a1534cb650ba17af400d1acd3a22c28004c09/lib/html/pipeline/toc_filter.rb) to generate those fragments by:

- Converting the text to lowercase
- Removing any punctuation characters
- Converting any spaces to dashes
- Append an incrementing integer (as needed for uniqueness)
- URI-encode the result

## Heading Ã name

c3

- Simple text
    - Example: `# Heading Name` --> `#heading-name`
- Simple text with punctuation characters
    - Example: `# Heading & Name !` --> `#heading--name-`
- Unicode text
    - Example: `# Heading Name` --> `#heading-name`
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

[Link](#top)

### Not Supported

[Link](#L89)
[Link](#L19C5-L21C11)

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

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD051](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md051---strong-style).
