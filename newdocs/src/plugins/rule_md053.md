# Rule - MD053

| Property | Value |
| --- | --- |
| Aliases | `md053`, `link-image-reference-definitions` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Link and image reference definitions should be needed.

## Reasoning

### Readability

Link reference definitions are used in conjunction with full links, collapsed
links, and shortcut links. Their use allows the main body of the document
to stay uncluttered, allowing their definition at a later part in the
document where they can be organized together.

But because of this split between where a link reference is declared
and where a link reference is used, two situations can arise that affect
readability:

- unused definitions: a link reference definition is specified but is not
  referenced
- multiple definitions: multiple link reference definitions that contain
  the same link label text

Both of these situations can easily occur as a Markdown document evolves
and its content are changed.

## Examples

### Failure Scenarios

This rule triggers under the two main situations defined in the above section
on readability.

In the first case, unused definitions are orphaned link reference definitions
that are no longer referenced by links in the document. In the following
Markdown fragment, the `some-other-link` text is used to register a link
reference definition, but is not referenced anywhere.

````Markdown
Go to [this link][some-link].

[some-link]: /url
[some-other-link]: /url
````

In the second case, the link reference definition is specified with the
same link text in multiple places in the document. The
[GitHub Flavored Markdown specification](https://github.github.com/gfm/#example-173)
clearly spells out that if there are several matching definitions, the first
one takes precedence. That means that in the following example, the information
provided by the second `some-link` link reference definition is ignored.
While this example
shows both link reference definitions together, the more common case
is that they are defined at the end of each section and multiple
sections unintentionally refer to a definition with the same link text.

````Markdown
Go to [this link][some-link].

[some-link]: /url
[Some-Link]: /other-url
````

### Correct Scenarios

This rule does not trigger if a link reference definition is used by
at least one link and does not have semantically equal link text to another
link reference definition. A simple example of this is the Markdown fragment:

````Markdown
Go to [this link][some-link].
Show ![this image][some-other-link].

[some-link]: /url
[some-other-link]: /image-url
````

Please keep in mind that "semantically equal" in the above paragraph
means that the two values being compared are equal after applying the
following process to the link text:

- perform a Unicode case fold (fully documented [in this specification](https://www.unicode.org/reports/tr21/tr21-5.html))
- strip leading and trailing whitespace
- collapse consecutive internal whitespace to a single space

#### Skipping Reference Checks

There are some cases where the link reference definitions are present without
a need for a link to reference them. A common use of this is to allow for a
link reference definition to act like a comment by using the following format:

```Markdown
[//]: /u (This behaves like a comment)
```

The `//` sequence in the above Markdown fragment is allowed without triggering
this rule as the value of the `ignored-definitions` configuration item is defined
as `"//"`. That configuration item is a comma-separated string of link texts
for this rule to ignore.  Therefore, if you want to allow link texts values of
both `//` and `#` to act as a comment, you can set the value of `ignored-definitions`
to `"//,#"`.

## Fix Description

The reason for not being able to auto-fix this rule is certainty.

## Configuration

| Prefixes |
| --- |
| `plugins.md053.` |
| `plugins.link-image-reference-definitions.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `ignored-definitions` | `str` | `"//"` | Comma-separated list of link texts that do not trigger this rule. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD053](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md053---link-and-image-reference-definitions-should-be-needed).
