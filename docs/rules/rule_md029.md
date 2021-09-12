# Rule - MD029

| Aliases |
| --- |
| `md028` |
| `ol-prefix` |

## Summary

Ordered list item prefix.

## Reasoning

The main reasons for this rule are readability and consistency.  While
it may not seem important, keeping the Ordered List Item prefix in a
common form enhances the readability of the document by providing
consistency.  This consistency can also be set to take advantage of
the strengths and weaknesses of the Markdown parser, to ensure the
correct HTML is output.

## Examples

### Failure Scenarios

This rule triggers when an Ordered List Item element does not
start with the number `1` or if any subsequent List Item elements
are not in a numerically increasing order.

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

## Configuration

| Prefixes |
| --- |
| `plugins.md029.` |
| `plugins.ol-prefix.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled by default. |
| `style` | string (see below) | `one_or_ordered` | Style for Ordered List Starts in the document. |

Valid heading styles:

| Style | Description |
| -- | -- |
| `"one_or_ordered"` | Either of the `one` or `ordered` styles below. |
| `"one"` | All Ordered List Items must start with `1`. |
| `"ordered"` | Starting with `0` or `1`, each subsequent item must be one greater than its predecessor. |
| `"zero"` | All Ordered List Items must start with `0`. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD029](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md029---ordered-list-item-prefix).

### Differences From MarkdownLint Rule

This rule differs from the original implementation in that it only
fires for the first non-matching item.  As that first item will most
likely indicate the pattern for any other items that follow, it should
be enough to call out the first item and let the user fix the rest of
the list.
