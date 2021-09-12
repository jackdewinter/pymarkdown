# Rule - MD020

| Aliases |
| --- |
| `md020` |
| `no-missing-space-closed-atx` |

## Summary

No space present inside of the hashes on a possible Atx Closed Heading.

## Reasoning

In most cases, one or more hash characters (`#`) followed by text and closing
hash characters were meant to indicate an Atx Closed Heading, with the
space between the hash characters and the text being omitted.

## Examples

### Failure Scenarios

This rule triggers when a sequence of characters occurs at the start of a line in
a paragraph after between 0 and 3 leading spaces are removed.  After those leading
spaces are removed, this rule then looks for between 1 and 6 hash characters (`#`),
0 or more space characters, 1 or more non-space characters, 0 or more space
characters, and 1 or more hash characters.  This rule specifically triggers
if the number of space characters at the start of the Atx Closed Heading is zero:

```Markdown
#Heading 1 #
```

if the number of space character at the end of the Atx Closed Heading is zero:

```Markdown
# Heading 1#
```

or if both counts of space characters are zero:

```Markdown
#Heading 1#
```

### Correct Scenarios

This rule does not trigger when there are 1 or more spaces on either
side of the Atx Closed Heading:

```Markdown
## Heading 2 ##
```

or if a closing hash character is not present:

```Markdown
##Heading 2
```

This failure scenario is handled by
[Rule md018](https://github.com/jackdewinter/pymarkdown/blob/main/docs/rule_md018.md).

## Configuration

| Prefixes |
| --- |
| `plugins.md020.` |
| `plugins.no-missing-space-closed-atx.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD020](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md020---no-space-inside-hashes-on-closed-atx-style-heading).

### Differences From MarkdownLint Rule

Similar to
[Rule md018](https://github.com/jackdewinter/pymarkdown/blob/main/docs/rule_md018.md),
the original rule did not trigger in Block Quote elements or
List elements, but did fire within SetExt Heading elements.  These
changes were also made in this rule to keep it consistent with
Rule md018.
