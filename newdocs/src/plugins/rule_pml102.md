# Rule - PML102

| Property | Value |
| --- | -- |
| Aliases | `pml102`, `disallow-lazy-list-indentation` |
| Autofix Available | In Queue |
| Enabled By Default | No |

## Summary

Disallow "lazy" paragraph continuations within lists.

## Enable This Rule If

This rule is disabled by default.  Enable this rule if you want to generate
Rule Failures when the Markdown documents contain multiple line paragraphs
where the indentation for each paragraph line does not match the indentation
for the list that contains it.

## Reasoning

### Readability

The example of a trivial list with two lines is as follows:

```Markdown
1. A paragraph
   with two lines.
```

From our point of view, when we look at those two lines, everything lines up and
most readers would agree that the second line is part of the list item started on
the first line.

The next example mutates that example by removing leading spaces on the second line:

```Markdown
1. A paragraph
 with two lines.
```

In this example, the second line starts at the left margin instead of being aligned
with the text in the list item. According to the GitHub Flavored Markdown (GFM)
specification, that second line is still part of the same paragraph because it does
not start another eligible Markdown element. The specification calls this kind of
misaligned paragraph line a [lazy continuation lines](https://github.github.com/gfm/#lazy-continuation-line).

One of our users filed [issue 979](https://github.com/jackdewinter/pymarkdown/issues/979)
describing this concern. We agreed with their request and implemented it as Rule
Plugin PML102. While we allow lazy continuation lines to remain compliant with the
specification, we believe it can reduce the readability of many Markdown documents.
This rule gives PyMarkdown users control over whether lazy continuation lines are
permitted in their documents.

## Examples

### Failure Scenarios

This rule triggers if any paragraph started directly within a list container utilizes
lazy continuation of the paragraph element on the second and later lines of the
paragraph. Whether that continuation line is missing one space of indentation, as
in this example:

```Markdown
1. A paragraph
  with two lines.
```

or multiple spaces of indentation, as in this example:

```Markdown
1. A paragraph
with two lines.
```

this rule will fire. Note that in the case where a new list item is added to the
list with a changed indentation, that indentation will be used to determine if this
rule will fire, not the original list item's indentation.

```Markdown
1. A paragraph
   with two lines.
 2. Another paragraph
   with two lines.
```

### Correct Scenarios

To correct the above examples, simply enforce the required indentation using space
characters to match the indentation of the list:

```Markdown
1. A paragraph
   with two lines.
```

### Note

This rule currently targets [List Item lazy continuation lines](https://github.github.com/gfm/#example-269)
and not [Block Quote lazy continuation lines](https://github.github.com/gfm/#example-210).
If you would like to see Block Quote lazy continuation lines supported by this rule,
please [open an issue](https://github.com/jackdewinter/pymarkdown/issues).

## Fix Description

The fix for this rule is currently in queue.

## Configuration

| Prefixes |
| --- |
| `plugins.pml102.` |
| `plugins.disallow-lazy-list-indentation.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule was developed in response to user [issue 979](https://github.com/jackdewinter/pymarkdown/issues/979).
