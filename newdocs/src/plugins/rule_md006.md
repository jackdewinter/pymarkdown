# Rule - MD006

| Property | Value |
| --- | --- |
| Aliases | `md006`, `ul-start-left` |
| Autofix Available | Yes |
| Enabled By Default | No |

## Deprecation

This rule has been deprecated in favor of [Rule MD007](./rule_md007.md).

## Summary

Ensure unordered lists start at the beginning of the line.

## Reasoning

### Consistency

Unordered lists should start at the beginning of the line to ensure
predictable document structure and consistent rendering across
Markdown parsers. Proper alignment helps readers quickly identify
list boundaries and improves accessibility for screen readers that
rely on consistent indentation patterns.

## Examples

### Failure Scenarios

This rule triggers when an Unordered List element does not start at the
beginning of the line:

```Markdown
 * Item 1
 * Item 2
```

> **Explanation**: The list above is indented by one space, which violates the
> requirement that unordered list markers begin at column 0.

Unlike the previous example of a simple root-level indent, this case involves an unordered list intended as a child of an ordered list but lacking the correct indentation:

```Markdown
1. Ordered List
  - Item 1
  - Item 2
```

> **Explanation**: The unordered list markers are indented by two spaces, placing them inside the ordered list item rather than at column 0. This violates the requirement that unordered list markers begin at the start of the line.

Unlike the previous example involving list nesting, this case shows an unordered list indented within a blockquote:

```Markdown
> Quoted text
> * Item 1
> * Item 2
```

> **Explanation**: The unordered list markers inside the blockquote are not
> at the start of the line within the blockquote context, causing the rule
> to trigger.

Unlike the previous example, this case involves a nested unordered list where the parent marker is indented:


```Markdown
  * Parent Item
    * Child Item 1
    * Child Item 2
```

> **Explanation**: The parent unordered list marker is indented by two spaces.
> Even though the child items are properly indented relative to the parent,
> the parent itself does not start at column 0, which violates the rule.

### Correct Scenarios

This rule does not trigger when every top-level item for an Unordered List
element starts at the beginning of each line.

```Markdown
* Item 1
* Item 2
```

> **Explanation**: The list markers begin at column 0, satisfying the rule.

Unlike the previous example, this list contains multi-line items, but the next list marker still starts at column 0:

```Markdown
* Item 1
  more of Item 1
  even more of Item 1
* Item 2
```

> **Explanation**: Even though list content spans multiple lines, the next list marker starts at column 0, which is valid.

## Fix Description

The autofix removes leading whitespace from unordered list markers so that
they begin at column 0 (the start of the line).

Note: Because the definition of "start of the line" was ambiguous in nested
contexts, this rule has been deprecated in favor of [Rule MD007](./rule_md007.md),
which provides more precise indentation control for lists.

## Configuration

| Prefixes |
| --- |
| `plugins.md006.` |
| `plugins.ul-start-left.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `False` | Determines if this rule is active. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD006](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md006---consider-starting-bulleted-lists-at-the-beginning-of-the-line).

### Differences From MarkdownLint Rule

It is not clear how this rule, which is disabled by default, differs from
Rule MD007. To make sure this rule is well-rounded, it has been changed
to work with nested list blocks and block quotes.
