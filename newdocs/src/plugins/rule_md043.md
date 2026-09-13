# Rule - MD043

| Property | Value |
| --- | --- |
| Aliases | `md043`, `required-headings`, `required-headers` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Require the document to contain a specific, configuration-defined heading structure.

## Reasoning

### Consistency

Documents that share a common outline (e.g., templates, API reference pages, or
generated reports) are easier to read when their heading structure is predictable.
This rule lets authors encode that expected outline in configuration and flags
any document that deviates from it.

## Examples

### Failure Scenarios

This rule triggers when the document headings do not match the configured required
structure. In this example, the configuration `# Level 1,## Level 2` expects a Level
1 heading followed by a Level 2 heading, but the document starts with a Level 2
heading.

```Markdown
## Level 1
## Level 2
```

> **Explanation**: The rule fails because the first heading is `## Level 1` (Level
> 2), but the configuration requires the first heading to be `# Level 1` (Level
> 1). The heading level does not match the required structure.

Unlike the previous example, this case uses the correct heading levels but incorrect
heading text. The configuration expects `Level 2`, but the document contains
`Level Two`.

```Markdown
# Level 1
## Level Two
```

> **Explanation**: The rule fails because the second heading text is `Level Two`,
> but the configuration requires the text to be `Level 2`. The heading text does
> not match the required structure.

Unlike the previous examples, this case uses the correct heading levels and text
but in the wrong order. The configuration expects Level 1 before Level 2, but the
document has Level 2 before Level 1.

```Markdown
## Level 2
# Level 1
```

> **Explanation**: The rule fails because the headings appear in the order
> `## Level 2` then `# Level 1`, but the configuration requires `# Level 1` to
> appear before `## Level 2`. The heading order does not match the required structure.

Unlike the previous examples, this case demonstrates a missing required heading.
The configuration expects `# Level 1` followed by `## Level 2`, but the document
only contains `# Level 1`.

```Markdown
# Level 1
```

> **Explanation**: The rule fails because the document is missing the required
> `## Level 2` heading. The configuration requires both headings to be present,
> but only the first one exists.

Unlike the previous examples, this case demonstrates that extra headings present
in the document cause a failure when the configuration does not include a wildcard
to allow them. The configuration `# Level 1,## Level 2` expects exactly those two
headings, but the document contains an additional `### Level 3` heading.

```Markdown
# Level 1
## Level 2
### Level 3
```

> **Explanation**: The rule fails because the document contains `### Level 3`, which
> is not included in the configuration `# Level 1,## Level 2`. Since the configuration
> does not use a wildcard (`*`) to allow additional headings, any extra headings
> violate the required structure.

Unlike the previous examples, this case demonstrates that the rule inspects the
**level** of a Setext heading, not just its text. The configuration
`# Level 1,## Level 2` requires a Level 1 heading followed by a Level 2
heading. The document uses Setext syntax, but the first heading is a Level 2
Setext heading (single-dash underline) where a Level 1 heading is required, and
the second heading is a Level 3 Setext heading (triple-dash underline) where a
Level 2 heading is required.

```Markdown
Level 1
-------
Level 2
---------
```

> **Explanation**: The rule fails because the **levels** of the Setext
> headings do not match the configuration. The first Setext heading
> (`Level 1` underlined with a single `-`) is a **Level 2** heading, but the
> configuration requires a **Level 1** heading (`# Level 1`). The second Setext
> heading (`Level 2` underlined with three `-` characters) is a **Level 3**
> heading, but the configuration requires a **Level 2** heading (`## Level 2`).
> The text of both headings is correct, but the underline length determines the
> level, and both levels are wrong.

### Correct Scenarios

This rule does not trigger when the document headings exactly match the configured
required structure. In this example, the configuration `# Level 1,## Level 2` is
satisfied by the document having a Level 1 heading followed by a Level 2 heading
with the correct text.

```Markdown
# Level 1
## Level 2
```

> **Explanation**: The rule passes because the document headings `# Level 1` and
> `## Level 2` match the required structure specified in the configuration
> `# Level 1,## Level 2` in both level, text, and order.

Unlike the previous example, this case demonstrates the use of a wildcard (`*`)
in the configuration to allow for flexible content between required headings. The
configuration `## Header,*,## Footer` requires a "Header" section and a "Footer"
section, with any number of headings (or none) allowed in between.

```Markdown
## Header
### Subheading 1
### Subheading 2
## Footer
```

> **Explanation**: The rule passes because the document starts with `## Header`
> and ends with `## Footer`, satisfying the configuration `## Header,*,## Footer`.
> The wildcard `*` allows for the intermediate `### Subheading 1` and
> `### Subheading 2` headings to exist without violating the rule.

Unlike the previous example, this case demonstrates the use of multiple wildcards
(`*`) in the configuration to allow flexible content in separate sections of the
document. The configuration `## Header,*,## Middle,*,## Footer` requires "Header",
"Middle", and "Footer" sections, with any number of headings allowed between each
pair.

```Markdown
## Header
### Introduction
### Background
## Middle
### Data
## Footer
### Conclusion
```

> **Explanation**: The rule passes because the document contains `## Header`,
> `## Middle`, and `## Footer` in the correct order. The configuration
> `## Header,*,## Middle,*,## Footer` uses two wildcards, allowing `### Introduction`
> and `### Background` between the first two required headings, and `### Data` between
> the next pair, without violating the rule.

Unlike the previous example, this case demonstrates that a Setext heading in the
document satisfies a configuration entry written in Atx form. The configuration
`# Level 1,## Level 2` requires a Level 1 and a Level 2 heading, but the
document expresses both as Setext headings (underline-style) rather than Atx
headings (`#`-style).

```Markdown
Level 1
=======
Level 2
-------
```

> **Explanation**: The rule passes because the configuration specifies heading
> **levels and text**, not the syntactic form. The first line `Level 1` followed
> by `=======` is a Setext Level 1 heading, and `Level 2` followed by `-------`
> is a Setext Level 2 heading. Both match the required `# Level 1` and
> `## Level 2` entries in the configuration `# Level 1,## Level 2`, confirming
> that Setext headings in the document are accepted regardless of the Atx form
> used in the configuration.

Unlike the previous example, this case demonstrates that a wildcard (`*`) may
match **zero** intermediate headings, not only one or more. The configuration
`## Header,*,## Footer` requires a `## Header` heading followed by a
`## Footer` heading, with any number of headings (including none) allowed
between them. This document contains only the two required headings, with no
headings in between.

```Markdown
## Header
## Footer
```

> **Explanation**: The rule passes because the document begins with `## Header`
> and ends with `## Footer`, satisfying the configuration
> `## Header,*,## Footer`. The wildcard `*` matches zero intermediate headings
> in this case, which is permitted by its semantics ("zero or more non-matching
> headings"). The absence of any heading between `## Header` and `## Footer`
> does not violate the rule.

## Fix Description

Auto-fixing is not available due to combinatorial explosion. While simple configurations
(e.g., `## Header, ## Footer`) could be fixed, the use of the `*` wildcard creates
a large number of possible heading structures, making it computationally infeasible
to determine the correct fix automatically.

## Configuration

| Prefixes |
| --- |
| `plugins.md043.` |
| `plugins.required-headings.` |
| `plugins.required-headers.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `required_headings` | `string` | `""` | Comma-separated list of headings to require the document to have. |

The comma-separated list of items is a string with a format of `{item},...,{item}`.
Any leading or trailing space characters surrounding the `{item}` are trimmed during
processing. Any empty `{item}` value left after this trimming has been applied will
generate a configuration error.

Each element must be in one of two forms. The first form is that of an uncomplicated
text Atx Heading,
such as `# Heading 1`. Regardless of whether the heading in the document is an
Atx Heading element or a Setext Heading element, this form must be used.
The second form is that of a single wildcard character. Currently, only
the `*` character is allowed, specifying that zero or more non-matching
headings may occur.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD043](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md043---required-heading-structure).
