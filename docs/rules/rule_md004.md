# Rule - MD004

| Aliases |
| --- |
| `md004` |
| `ul-style` |

## Summary

Inconsistent Unordered List Start style.

## Reasoning

While the parsing engines do not usually have any problems with inconsistent
Unordered List Start styles, a human reader of the same document will encounter difficulty.
By enforcing a rule to make the Unordered List Start style consistent, the human reader
will be able to read the document with less issues.

## Examples

### Failure Scenarios

This rule triggers when the starting character for any Unordered List Start
within the document does not match the configurated style:

```Markdown
+ First Item
- Second Item
* Third Item
```

### Correct Scenarios

This rule does not trigger under two groups of scenarios.  The first
group of scenarios occur when every Unordered List Start in the
document is the same, regardless of whether they are lists or sublists:

```Markdown
+ First Item
+ Second Item
+ Third Item
```

By default, the [configured style](#configuration) is set to `consistent`.
This means that as long as every Unordered List Start in the document
is the same as the first in the document, the rule will not fire.
If more precision is required, one of the values `plus`, `dash`, or `asterisk` can
be specified to lock down the Unordered List Start, instead of
relying on the first Unordered List Start in the document to be the correct style.

The second group of scenarios occur when the [configured style](#configuration)
is set to `sublist`.  That style specifies that each level of Unordered List Starts
behaves as if the style `consistent` was specified for that level.
For example, if this Markdown was present near the start of the document:

```Markdown
+ First Level
  - Second Level
    * Third Level
```

then another Unordered List, later in the document, needs to keep to those start
characters to avoid triggering the rule:

```Markdown
+ New List
```

```Markdown
+ Another List
  - With Sublist Items
    * At each level
```

Note that while these examples contain three level of Unordered Lists for
illustration purposes, there is no limit to the number of sublist levels
that are tracked.

## Configuration

| Prefixes |
| --- |
| `plugins.md004.` |
| `plugins.ul-style.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `style` | string (see below) | `consistent` | Style for Unordered List Starts in the document. |

Valid heading styles:

| Style | Description |
| -- | -- |
| `"consistent"` | The first Unordered List Start in the document specifies the style for the rest of the document. |
| `"asterisk"` | Only Unordered List Starts with asterisks are to be used. |
| `"dash"` | Only Unordered List Starts with dashes are to be used. |
| `"plus"` | Only Unordered List Starts with pluses are to be used. |
| `"sublist"` | The first Unordered List Start in the document for that level of sublist specifies the style for that level of sublist for the rest of the document. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD004](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md004---unordered-List-style).
