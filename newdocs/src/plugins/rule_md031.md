# Rule - MD031

| Property | Value |
| --- | -- |
| Aliases | `md031`, `blanks-around-fences` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

Fenced code blocks should be surrounded by blank lines.

## Reasoning

### Readability

By separating
Fenced Code Block elements from the other elements in a document, their
existence in the document is highlighted.  In addition, a select few parsers
may not properly recognize the Fenced Code Block without the extra
blank lines on both sides.

## Examples

### Failure Scenarios

This rule triggers when the Fenced Code Block element is either not
prefaced with Blank Lines:

````Markdown
This is text.
```block
A code block
```

This is a blank line and some text.
````

or followed by Blank Lines:

````Markdown
This is text and a blank line.

```block
A code block
```
This is some text.
````

### Correct Scenarios

This rule does not trigger when there is a single
Blank Line both before and after the Fenced Code Block
element:

````Markdown
This is text and a blank line.

```block
A code block
```

This is a blank line and some text.
````

This rule will also not trigger if the Fenced Code Block element
is at the very start or the very end of the document.  In addition,
if the Fenced Code Block element is either the first element or
last element within a Block Quote element or a List Item element,
the check for a Blank Line in that direction extends beyond the
border of the container element.

#### Within List Items

Within a single List Item, there may be a need to create a List Item
that is [loose](https://github.github.com/gfm/#loose).  If this is
required, the `list_items` configuration value can be set to `False`.
With that configuration value set, this rule will not trigger for
lack of whitespace around Fenced Code Blocks, such as:

````Markdown
- This is an item
  ```block
  A code block
  ```
  Still the same item, and loose.
````

## Fix Description

The auto-fix feature for this rule is scheduled to be added soon after the v1.0.0
release.

## Configuration

| Prefixes |
| --- |
| `plugins.md031.` |
| `plugins.blanks-around-fences.` |

<!--- pyml disable-num-lines 4 line-length-->
| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `list_items` | `boolean` | `True` | Whether this plugin rule triggers directly within a list item. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD031](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md031---fenced-code-blocks-should-be-surrounded-by-blank-lines).
