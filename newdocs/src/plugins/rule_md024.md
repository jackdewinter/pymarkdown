# Rule - MD024

| Property | Value |
| --- | -- |
| Aliases | `md024`, `no-duplicate-heading`, `no-duplicate-header` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Multiple headings cannot contain the same content.

## Reasoning

### Correctness

While not common to the default installation of most parsers, a common extension
to those parsers is to generate an `id` attribute for the heading element and/or
an anchor tag based on the content of the heading element.  Therefore, having
two or more headings with the same text may confuse those generators, producing
non-unique results for those anchors.

## Examples

### Failure Scenarios

This rule triggers when there are multiple headings that have the same text:

```Markdown
# Heading Text

## Heading Text
```

### Correct Scenarios

This rule does not trigger when each heading has distinct text:

```Markdown
# Heading 1

## Heading 2
```

A strict comparison is performed, so even an extra space character:

```Markdown
# Heading  Text

## Heading Text
```

or a change in capitalization is enough to avoid this rule triggering:

```Markdown
# Heading TEXT

## Heading Text
```

### Siblings

In certain Markdown documents, such as `changelog.md` files, non-sibling
headings may purposefully have the same text.  As this is the desired
behavior, the `siblings_only` or `allow_different_nesting` configuration value
can be set to `True` to allow this Markdown document to not trigger this rule:

```Markdown
# Change log

## 1.0.0

### Features

## 2.0.0

### Features
```

Continuing the use of the family analogy, the way to view a sibling
relationship is as follows.  If the same heading occurs at the same
level, it is considered a *twin* heading.  This mirrors a real-life
twin that has the same parents, in this case the heading before
the twin headings.  And while it might more properly be called
a *cousin* heading, a *sibling* heading is a heading with the same
name at the same depth in the heading hierarchy.

Using the change log example above, this relationship is true as
both occurrences of the heading text `Features` occurs in a level
3 heading under a level 2 heading.

## Fix Description

The reason for not being able to auto-fix this rule is context. Using any of the
above trigger examples, it is simple to determine when this rule should be triggered.
It would be relatively easy to devise an algorithm that would perform some action
(such as appending an increasing number to the end of the heading text) to make each
heading unique.  While that would fix the triggering of the rule, it would deprive
the author of the chance to change any triggered headings to text that was unique
and made sense within the scope of the document.

## Configuration

| Prefixes |
| --- |
| `plugins.md024.` |
| `plugins.no-duplicate-heading.` |
| `plugins.no-duplicate-header.` |

<!--- pyml disable-num-lines 5 line-length-->
| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `siblings_only` | `boolean` | `False` | Whether the plugin rule allows the same text on sibling headings. |
| `allow_different_nesting` | `boolean` | `False` | Whether the plugin rule allows the same text within different nesting hierarchies. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD024](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md024---multiple-headings-with-the-same-content).
