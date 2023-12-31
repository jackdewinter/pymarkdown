# Rule - MD006

| Aliases |
| --- |
| `md006` |
| `ul-start-left` |

| Autofix Available |
| --- |
| Yes |

## Summary

Consider starting bulleted lists at the beginning of the line.

## Reasoning

### Consistency

The primary reason for enabling this rule is to force any Unordered List
to start at the beginning of the line.  While there are ancillary scenarios
that this rule can help, the main focus is to allow for predictability
in how Unordered List elements are constructed.

When creating lists with an editor, it is common to use the Tab key to create
lists that are properly indented.  If an Unordered List element does not start
at the beginning of the line, using the Tab key can cause the number of
spaces inserted to not be an even number.  As the normal indent for an Unordered
List element is 2, this may cause issues with other parts of the list.

## Examples

### Failure Scenarios

This rule triggers when an Unordered List element does not start at the
beginning of the line:

```Markdown
 * Item 1
 * Item 2
```

A more practical example is when an Unordered List element is supposed to
be created as a child of an Ordered List element, but lacks the correct
indentation:

```Markdown
1. Ordered List
  - Item 1
  - Item 2
```

In this case, an Ordered List element will be created with one item,
followed by an Unordered List element with two items.  Enabling this
rule will help prevent circumstances like this.

### Correct Scenarios

This rule will not trigger if every top-level item for an Unordered List
element starts at the beginning of each line.

```Markdown
* Item 1
* Item 2
```

Note that having items that span multiple lines is also acceptable, as long
as the next Unordered List element starts is at the beginning of the line.

```Markdown
* Item 1
  more of Item 1
  even more of Item 1
* Item 2
```

## Configuration

| Prefixes |
| --- |
| `plugins.md006.` |
| `plugins.ul-start-left.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD006](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md006---consider-starting-bulleted-lists-at-the-beginning-of-the-line).

### Differences From MarkdownLint Rule

It is not clear how this rule, which is disabled by default, differs from
Rule Md007.  To make sure this rule is well-rounded, it has been changed
to work with nested list blocks and block quotes.

## Fix Description

The containers will be altered so that they start at the beginning of "the line".
As that definition was not clearly understood [Rule MD007](./rule_md007.md) was
created to more clearly handle the issue.
