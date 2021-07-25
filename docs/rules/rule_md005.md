# Rule - MD005

| Aliases |
| --- |
| `md005` |
| `list-indent` |

## Summary

Inconsistent indentation for list items at the same level.

## Reasoning

While the parsing engines do not usually have any problems with inconsistent
starting indentation for List elements, a human reader of the same document will
encounter difficulty.  By enforcing the items within a List element to start at
predictable locations, the human reader will be able to read the document with
less difficulty.

## Examples

### Failure Scenarios

This rule triggers when there is a misalignment with the list indentation for the
items within a list.  An Unordered List element is the easiest failure to see as
the indentation either matches up or not:

```Markdown
* Item 1
* Item 2
 * Misaligned item
```

A failure for this rule for Ordered List elements is a bit more nuanced as this
rule supports both left aligned and right aligned.  That means that either the
first character must match the identation of the list or the list delimiter
character (`.` or `)`) must match.  Therefore

```Markdown
1. First item
 2. Second Item
```

fails because neither the first character's indentation nor the delimiter
character's indentation matches.

### Correct Scenarios

This rule does not trigger under two groups of scenarios.  The first
group of scenarios occur when every Unordered List Start in the
document is the same, regardless of whether they are lists or sublists:

```Markdown
* Item 1
  * Item 1a
* Item 2
  * Item 2a
```

As mentioned above, the indentation of Ordered List elements supports
both left alignment and right alignment.  This means that either of
these two formats is acceptable:

```Markdown
1. Item
10. Item
100. Item
```

or

```Markdown
  1. Item
 10. Item
100. Item
```

Note that in the right aligment format, having an Ordered List item
starts with more than 4 characters is impossible without switching
aligmnent.

```Markdown
    1. Item
   10. Item
  100. Item
 1000. Item
10000. Item
```

In this case, the Ordered List starts with the "second" item as
the 4 spaces at before `1.` makes it an Indented Code Block instead
of the start of an Ordered List.

## Configuration

| Prefixes |
| --- |
| `plugins.md005.` |
| `plugins.list-indent.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled by default. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD005](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md005---inconsistent-indentation-for-list-items-at-the-same-level).
