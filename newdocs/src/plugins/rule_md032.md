# Rule - MD032

| Property | Value |
| --- | -- |
| Aliases | `md032`, `blanks-around-lists` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

List blocks should be surrounded by blank lines.

## Reasoning

### Readability

By separating
List elements from the other elements in a document, their
existence in the document is highlighted.  In addition, some parsers
may not properly recognize the List elements without the extra
blank lines on both sides.

## Examples

### Failure Scenarios

This rule triggers when the List element is either not
prefaced with Blank Lines:

````Markdown
This is text.
+ a list
````

or followed by Blank Lines:

````Markdown
1. a list
# This is any non-text block
````

### Correct Scenarios

This rule does not trigger when there is a single
Blank Line both before and after the List element:

````Markdown
This is text and a blank line.

+ a list

This is a blank line and some text.
````

This rule will also not trigger if the List element is at the
very start or the very end of the document.  

In addition, this rule will not trigger if a List element
is found directly within the scope of another List element. If
a List element is found directly within the scope of a Block
Quote element, then this rule behaves normally.

## Fix Description

The auto-fix feature for this rule is scheduled to be added soon after the v1.0.0
release.

## Configuration

| Prefixes |
| --- |
| `plugins.md032.` |
| `plugins.blanks-around-lists.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD032](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md032---lists-should-be-surrounded-by-blank-lines).
