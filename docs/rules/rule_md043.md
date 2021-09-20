# Rule - MD043

| Aliases |
| --- |
| `md043` |
| `required-headings` |
| `required-headers` |

## Summary

Required heading structure.

## Reasoning

### Consistency

In certain situations, there may be a need to enforce a heading structure
on one or more documents.  This rule uses configuration to specify
what heading elements are expected in the document, and in which order
they must show up.

## Examples

For these examples, Atx Heading elements are used.  The SetExt Heading
element equivalents of those Atx Heading elements support an identical
behavior.

### Failure Scenarios

This rule is triggered when the required heading structure constraints
are not met by the actual heading structure.

Given a configuration value of `# Level 1,## Level 2`, those two Heading elements
must be present in the document and in that order to satisfy the requirements.
Any change in the level of the elements:

```Markdown
## Level 1
## Level 2
```

the text of the elements:

```Markdown
# Level 1
## Level Two
```

or the order of the elements:

```Markdown
## Level 2
# Level 1
```

will cause this rule to trigger.

### Correct Scenarios

This rule is not triggered when the required heading structure constraints
are met by the actual heading structure.  Using the default configuration
value of an empty string, every actual heading structure meets those criteria.

Given a configuration value of `# Level 1,## Level 2`, those two Heading elements
must be present in the document and in that order to satisfy the requirements:

```Markdown
# Level 1
## Level 2
```

In addition to a valid Atx Heading Text element, a single `*` character may
be used.  This character specifies that any number of lines (zero or more)
can be matched to satisfy the criteria.  For example, the configuration value
of `## Header,*,## Footer` can be used to specify a header and footer section for the document:

```Markdown
## Header
...
## Footer
```

Note that specifically in this case, because of the `*` that follows the
`## Header` sequence in the configuration value, the `Header` section may have
any number of subheadings underneath it.  However, since the `## Footer`
sequence is not followed by anything; it cannot be followed by any headings.

## Configuration

| Prefixes |
| --- |
| `plugins.md043.` |
| `plugins.required-headings.` |
| `plugins.required-headers.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `required_headings` | `string` | `""` | Comma separated list of headings to require the document to have. |

For the `required_headings` list, each element is expected to be in one
of two forms.  The first form is that of a uncomplicated text Atx Heading, such as
`# Heading 1`.  Regardless of whether the heading in the document is an
Atx Heading element or a SetExt Heading element, this form must be used.
The second form is that of a single wildcard character.  Currently, only
the `*` character is allowed, specifying that zero or more non-matching
rows may occur.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD043](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md043---required-heading-structure).
