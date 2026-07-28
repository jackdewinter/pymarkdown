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

## Heading \* Name

## Heading \< Name

## Heading \& Name

https://github.com/jackdewinter/pymarkdown/blob/352dd88480c58a25252ccdfb045a6bcaa81ca035/newdocs/src/plugins/rule_md051.md#heading--name

## Heading &#x0041; Name

https://github.com/jackdewinter/pymarkdown/blob/c2a0ad8210e12cf52261e48343d5bbcec003b858/newdocs/src/plugins/rule_md051.md#heading-a-name

## Heading &copy; Name

https://github.com/jackdewinter/pymarkdown/blob/352dd88480c58a25252ccdfb045a6bcaa81ca035/newdocs/src/plugins/rule_md051.md#heading--name-1

## Heading *foo* Name

https://github.com/jackdewinter/pymarkdown/blob/352dd88480c58a25252ccdfb045a6bcaa81ca035/newdocs/src/plugins/rule_md051.md#heading-foo-name

## Heading `foo` Name

https://github.com/jackdewinter/pymarkdown/blob/352dd88480c58a25252ccdfb045a6bcaa81ca035/newdocs/src/plugins/rule_md051.md#heading-foo-name

## Heading [Google](www.google.com) Name

https://github.com/jackdewinter/pymarkdown/blob/352dd88480c58a25252ccdfb045a6bcaa81ca035/newdocs/src/plugins/rule_md051.md#heading-google-name

## Heading <foo@bar.example.com> Name

## A <http://foo.bar.baz> target

https://github.com/jackdewinter/pymarkdown/blob/352dd88480c58a25252ccdfb045a6bcaa81ca035/newdocs/src/plugins/rule_md051.md#a-httpfoobarbaz-target

## A <del>d</del> <a name="d">target</a>

https://github.com/jackdewinter/pymarkdown/blob/352dd88480c58a25252ccdfb045a6bcaa81ca035/newdocs/src/plugins/rule_md051.md#a-d-target

### Link Targets

While these is no official [Github Flavored Markdown](https://github.github.com/gfm/) specification
for what consistutes a valid link target, the [GitHub heading algorithm](https://github.com/gjtorikian/html-pipeline/blob/f13a1534cb650ba17af400d1acd3a22c28004c09/lib/html/pipeline/toc_filter.rb) can be used to generate the link text itself. To do that, the text is collected from one of the following Markdown elements:

- **ATX heading:** any text on the same line, excluding any trailing `#` characters that are part of an ATX heading close
- **SetExt heading:** any text that is part of the paragraph before the SetExt heading characters
- **HTML Blocks and Raw HTML:** the `name` attribute for an `a` start tag (i.e. `<a name="bookmark">`) or any start tag's `id` parameter (i.e. `<a id="bookmark">`)

### Special Targets

[Link](#top)
[Link](#L89)
[Link](#L19C5-L21C11)

### XXX

Note: Section links are not part of the CommonMark specification; this rule enforces the historic [GitHub heading algorithm](https://github.com/gjtorikian/html-pipeline/blob/f13a1534cb650ba17af400d1acd3a22c28004c09/lib/html/pipeline/toc_filter.rb):

- Convert text to lowercase
- Remove punctuation characters
- Convert spaces to dashes
- Append an incrementing integer (as needed for uniqueness)
- URI-encode the result

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
