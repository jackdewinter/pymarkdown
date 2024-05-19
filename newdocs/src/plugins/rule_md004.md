# Rule - MD004

| Property | Value |
| --- | -- |
| Aliases | `md004`, `ul-style` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Inconsistent Unordered List Start style.

## Reasoning

### Readability

While parsing engines do not usually have any problems with inconsistent
Unordered List Start styles, a human reader of the same document will typically
experience issues. A human reader will need to mentally keep track of which List
elements belong to which List Start characters, slowing down their reading of the
document in the process. By enforcing a rule to make the Unordered List Start style
consistent, the human reader will be presented with a document that is easier to
read.

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
This means that unless every Unordered List Start in the document
is the same as the first Unordered List Start in the document, the rule will not
fire. If more precision is needed, one of the values `plus`, `dash`, or `asterisk`
can be specified to lock down the Unordered List Start, instead of
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

Note that while these examples have three levels of Unordered Lists for
illustration purposes, there is no limit to the number of sublist levels
that are tracked.

## Fix Description

If the `style` configuration value is set to `consistent`, then the first unordered
list start character encountered will be used for the rest of the document. This
also applies to the `sublist` value, but on a list depth basis.  Once the style
has been determined, it will be replaced if not already used for any unordered
list start.

## Configuration

| Prefixes |
| --- |
| `plugins.md004.` |
| `plugins.ul-style.` |

<!--- pyml disable-num-lines 4 line-length-->
| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `style` | string (see below) | `consistent` | Style for Unordered List Starts in the document. |

Valid heading styles:

<!--- pyml disable-num-lines 7 line-length-->
| Style | Description |
| -- | -- |
| `consistent` | The first Unordered List Start in the document specifies the style for the rest of the document. |
| `asterisk` | Only Unordered List Starts with asterisks are used. |
| `dash` | Only Unordered List Starts with dashes are used. |
| `plus` | Only Unordered List Starts with pluses are used. |
| `sublist` | The first Unordered List Start in the document for that level of sublist specifies the style for that level of sublist for the rest of the document. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD004](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md004---unordered-List-style).
