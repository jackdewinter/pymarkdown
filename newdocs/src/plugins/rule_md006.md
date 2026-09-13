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

Starting unordered lists at column 1 produces a uniform, predictable layout
across documents, which improves reader scanning and lets accessibility tools
reliably associate each item with its parent list.

## Examples

### Failure Scenarios

This rule triggers when an Unordered List element does not start at the
beginning of the line:

```Markdown
 * Item 1
 * Item 2
```

> **Explanation**: The list above is indented by one space, which violates the
> requirement that unordered list markers begin at column 1.

Unlike the previous example of a simple root-level indent, this case involves an
unordered list intended as a child of an ordered list but lacking the correct indentation:

```Markdown
1. Ordered List
  - Item 1
  - Item 2
```

> **Explanation**: The unordered list markers are indented by two spaces,
> placing them inside the ordered list item rather than aligned with the
> ordered list's content column (which is 3 spaces here). Because the
> markers are not aligned with the parent's content column, the rule
> triggers. See the matching correct-scenario example for the valid
> indentation.

Unlike the previous example involving list nesting, this case shows an unordered
list indented within a blockquote:

```Markdown
> Quoted text
> * Item 1
> * Item 2
```

> **Explanation**: The `*` markers are preceded by a leading space (after the
> blockquote marker), so they do not begin at column 1 of the blockquote's
> content. That single leading space is sufficient to trigger the rule, even
> though the list is correctly scoped to the blockquote.

Unlike the previous example, this case involves a nested unordered list where the
parent marker is indented:

```Markdown
  * Parent Item
    * Child Item 1
    * Child Item 2
```

> **Explanation**: The parent unordered list marker is indented by two spaces.
> Even though the child items are properly indented relative to the parent,
> the parent itself does not start at column 1, which violates the rule.

Unlike the previous example, which involved plain unordered list items, this
case shows an indented task list, where the markers carry a checkbox:

```Markdown
 * [ ] Task 1
 * [x] Task 2
```

> **Explanation**: The leading space before the `*` marker still places the
> task-list items away from column 1, so the rule triggers. The presence of
> the checkbox does not exempt the markers from the start-of-line
> requirement.

### Correct Scenarios

This rule does not trigger when every top-level item for an Unordered List
element starts at the beginning of each line.

```Markdown
* Item 1
* Item 2
```

> **Explanation**: The list markers begin at column 1, satisfying the rule.

Unlike the previous example, this list contains multi-line items, but the next
list marker still starts at column 1:

```Markdown
* Item 1
  more of Item 1
  even more of Item 1
* Item 2
```

> **Explanation**: Even though list content spans multiple lines, the next list
> marker starts at column 1, which is valid.

Unlike the previous example, which showed only a flat top-level list, this
case shows a correctly indented nested list: the parent is at column 1 and
the children are indented relative to the parent:

```Markdown
* Parent Item
  * Child Item 1
  * Child Item 2
```

> **Explanation**: The parent marker begins at column 1, and the child
> markers are indented relative to the parent, which is the expected
> structure for a nested list. Because the rule only requires that the
> top-level markers start at the beginning of the line, this example
> satisfies the rule.

Unlike the previous example, which used only unordered items, this case
shows an unordered list that is the child of an ordered list item. The
unordered markers are indented to match the ordered list's content column:

```Markdown
1. Ordered List
   - Child Item 1
   - Child Item 2
```

> **Explanation**: The unordered markers are indented to align with the
> content of the ordered list item, which is the conventional nesting
> structure. The rule is satisfied because the *top-level* markers of the
> document (the ordered list) begin at column 1; the unordered list is
> correctly nested inside it.

Unlike the previous example, which uses spaces, this case uses a literal tab character
in column 1 (shown below as `→`, representing a literal tab that renders as 4 spaces
of indentation) to indent the list markers:

```Markdown
<!-- The first character of each line is a literal TAB in the source file -->
→* Item 1
→* Item 2
```

> **Explanation**: The leading character in the source is a literal **tab**
> (shown here as `→`). A tab advances to the next tab stop, and when that
> results in four or more columns of indentation, it is parsed
> as an **indented code block** rather than a list item. Because the parser
> sees no unordered list marker on that line, the rule has nothing to
> evaluate and does not trigger.

Unlike the previous example, which was a plain nested list, this case shows
an unordered list inside a blockquote, where the markers begin at the start
of the blockquote's content:

```Markdown
> * Item 1
> * Item 2
```

> **Explanation**: Within the blockquote, the list markers begin at the
> first content column of the quoted text, which is the conventional way to
> place a list inside a blockquote. The rule is satisfied because the
> markers are at the start of the line *within their own context*.

## Fix Description

The autofix removes leading whitespace from unordered list markers so that
they begin at column 1 (the start of the line).

> **Note**: Because nested and blockquote contexts made the start-of-line
> definition ambiguous, this rule is deprecated in favor of
> [Rule MD007](./rule_md007.md), which provides precise indentation
> control for lists.

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

The original MarkdownLint rule MD006 only checked that bulleted lists
start at the beginning of the line. This rule extends that behavior to
nested list blocks and block quotes, and it has been superseded by
[Rule MD007](./rule_md007.md), which provides more precise indentation
control for lists.
