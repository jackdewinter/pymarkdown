# Rule - MD029

| Aliases |
| --- |
| `md029` |
| `ol-prefix` |

| Autofix Available |
| --- |
| Yes |

## Summary

Ordered list item prefix.

## Reasoning

### Readability

Writing the Ordered List Item prefix using a consistent form enhances the readability
of the document by supplying consistency.  This consistency can also be set to take
advantage of the strengths and weaknesses of the Markdown parser, to ensure the
correct HTML is output.

## Examples

### Failure Scenarios

By default, this rule uses the `one_or_ordered` configuration.  This triggers when
an Ordered List Item element does not start with the number `0` or `1` or if any
subsequent List Item elements are not in a numerically increasing order.

````Markdown
2. second item
3. third item
````

````Markdown
1. first item
3. third item
````

````Markdown
3. first item
3. second item
````

### Correct Scenarios

This rule does not trigger if all Ordered List Item elements
start with `1`:

````Markdown
1. First Line
1. Second Line
````

or if the first item starts with `0` or `1` and steadily increasing by
one:

````Markdown
1. First Item
2. Second Item
3. Third Item
````

Instead of the default `one_or_ordered` configuration, the `one` configuration
will trigger is any Ordered List Item element does not start with `1` and the
`zero` configuration will trigger instead if not a `0`.

Note that enabling the `allow_extended_start_values` configuration allows any
non-negative integer to start an `ordered` list. If the default `one_or_ordered`
configuration is in effect, any other integer other than `0` or `1` will force
the `ordered` configuration to be chosen.  Therefore, given the above failure
scenario:

````Markdown
2. second item
3. third item
````

and enabling the configuration `allow_extended_start_values` will cause this
scenario to become a correct scenario.

### Clarifications

The determination of whether the `one` part or the `ordered` part of the configuration
is used for the `one_or_ordered` configuration is done on a list by list basis.
Therefore, the following Markdown will not cause the rule to be triggered:

````Markdown
1. First Line
1. Second Line

text to break up lists

1. First Item
2. Second Item
3. Third Item
````

as there are two lists, each with their own style.

This is also true of nested lists, but with a twist.  Given the following:

```Markdown
2. first
   1. first-first
   1. first-second
   2. first-third
3. second
   1. second-first
   2. second-second
   2. second-third
```

this rule triggers on lines 1, 4, and 8.  It triggers on line 1 because the list
starts with `2`, line 4 because that inner list's style is `one` and line 8 because
that inner list's style is `ordered`.  Note that as a Commonmark compatible parser,
PyMarkdown will only accept an inner list that starts with a `1` to keep alignment
with Commonmark.

## Configuration

| Prefixes |
| --- |
| `plugins.md029.` |
| `plugins.ol-prefix.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `style` | string (see below) | `one_or_ordered` | Style for Ordered List Starts in the document. |
| `allow_extended_start_values` | `boolean` | `False` | Using the `ordered` style, allows for any integer to start the list. |

Valid heading styles:

| Style | Description |
| -- | -- |
| `one_or_ordered` | Either of the `one` or `ordered` styles below. |
| `one` | All Ordered List Items must start with `1`. |
| `ordered` | Starting with `0` or `1`, each List Item must be one greater than its predecessor. |
| `zero` | All Ordered List Items must start with `0`. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD029](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md029---ordered-list-item-prefix).

### Differences From MarkdownLint Rule

This rule differs from the original implementation in that it only
fires for the first non-matching item.  As that first item will most
likely provide the pattern for any other items that follow, it should
be enough to call out the first item and let the user fix the rest of
the list.

## Fix Description

In `zero` or `one` configuration, all list item starts will be set to `0` or `1`
respectively.  In `ordered` configuration, if the first item does not start with
`0` or `1` it will be set to `1` with any other list items in that list increasing
from that base item in ordered fashion.

With the `one_or_ordered` style, behavior depends on whether the first item's start
is `1` or another number.  If it is not `1`, it is set to `1` and the list's style
is considered to be `ordered`. If it is `1`, the determination of the list's style
is delayed to the next list item, determining whether the `one` or `ordered` style
will be followed.  If that second list item is `1`, the `one` style is adopted.
Any other number for the second list item causes the `ordered` style to be adopted,
changing that second item's list start to `2`.
