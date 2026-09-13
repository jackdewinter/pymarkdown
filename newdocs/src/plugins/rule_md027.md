# Rule - MD027

| Property | Value |
| --- | --- |
| Aliases | `md027`, `no-multiple-space-blockquote` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Use zero or one space after a block quote symbol so block quotes render with consistent
spacing.

## Reasoning

### Consistency

Inconsistent spacing after the block quote symbol `>` causes visual misalignment.
Because whitespace is invisible in rendered output, extra spaces are often accidental
artifacts. Restricting this to zero or one space keeps the block quote's left edge
predictable and consistent.

## Examples

### Failure Scenarios

This rule triggers when multiple spaces follow a block quote symbol.

```Markdown
>  This is text
```

> **Explanation**: This example violates the rule because there are two space characters
> after the block quote symbol `>` on the first line. The rule requires zero or
> one space after the block quote symbol.

Unlike the previous example, this case shows a block quote line whose only
content is a pipe character, with two spaces after the block quote symbol. The
pipe character (`|`) is used for visibility and is not part of the Markdown syntax:

```Markdown
>  |
```

> **Explanation**: This example violates the rule because there are two spaces after
> the block quote symbol `>`. The pipe character `|` is not part of the Markdown
> syntax but is included for visibility. The rule triggers because the extra spaces
> are not justified by any exempt element.

Unlike the previous example, this case shows a list item inside a block quote with
extra spaces after the block quote symbol:

```Markdown
>  - This is a list item
```

> **Explanation**: This example violates the rule because there are two spaces after
> the block quote symbol `>`. The extra space before the list marker `-` is not
> justified by any exempt element, and the rule requires zero or one space after
> the block quote symbol.

Unlike the previous example, this case demonstrates Setext headings with extra spaces
after the block quote symbol:

```Markdown
>   this is one Setext
> =====

> this is another Setext
>   =====
```

> **Explanation**: This example violates the rule on lines 1 and 5 (the code block
> contains 5 lines total). Line 1 is the text of the first Setext heading and line
> 5 is the underline of the second Setext heading; both have three spaces after
> the block quote symbol `>`. The rule applies to the text line and the underline
> line of a Setext heading equally — extra spaces after `>` are not permitted on
> either line.

Unlike the previous example, this case shows a thematic break with extra spaces
after the block quote symbol:

```Markdown
>  ----
```

> **Explanation**: This example violates the rule because there are two spaces after
> the block quote symbol `>`. The thematic break line triggers the rule because
> the extra spaces are not justified by any exempt element.

Unlike the previous example, this case shows a Link Reference Definition element
with extra spaces in the non-Label and non-Title parts of the element:

```Markdown
>  [lab
>  el]:
>  /url
>  "tit
>  le"
```

> **Explanation**: This example violates the rule on lines 1, 3, and 4 because each
> has two spaces after the block quote symbol `>`. The Link Label part (line 2:
> `el]:`) and Link Title part (line 5: `"tit"`) are **not** evaluated by the rule
> because the space within those tokens is part of the Label/Title syntax required
> for validity; only the non-Label, non-Title lines (1, 3, and 4) are subject to
> the zero-or-one-space restriction and therefore trigger the rule.

Unlike the previous example, this case shows a Fenced Code Block where the content
inside is safe, but the opening and closing lines still trigger the rule due to
extra spaces after the block quote symbol:

````Markdown
>  ```Python
>  a = a + 1
>  ```
````

> **Explanation**: This example triggers because the start and end lines of the
> Fenced Code Block are not immune to triggering, even though the content inside
> is exempt.

Unlike the previous example, this case shows an Atx Heading with extra spaces after
the block quote symbol:

```Markdown
>  # This is a heading
```

> **Explanation**: This example violates the rule because there are two spaces after
> the block quote symbol `>`. The Atx Heading line triggers the rule because the
> extra spaces are not part of an exempt element.

Unlike the previous example, this case shows an ordered list item with extra spaces
after the block quote symbol:

```Markdown
>  1. This is an ordered list item
```

> **Explanation**: This example violates the rule because there are two spaces after
> the block quote symbol `>`. The ordered list marker `1.` does not create an exemption
> for the extra space before it.

Unlike the previous example, this case shows a nested block quote where the inner
block quote symbol is followed by extra spaces:

```Markdown
> >  This is nested
```

> **Explanation**: This example violates the rule because the inner block quote
> symbol `>` is followed by two spaces. The rule evaluates each block quote marker
> independently: while the outer `>` is followed by a single space (within the allowed
> range), the inner `>` has an extra space that exceeds the zero-or-one limit and
> therefore triggers the rule.

Unlike the previous example, this case shows a blank line within a block quote that
has trailing spaces after the block quote symbol:

```Markdown
> This is a non-blank line
>  |
> This is another non-blank line
```

> **Explanation**: This example violates the rule because the middle line (shown
> with the pipe character `|` for visibility, representing a blank line) has two
> spaces after the block quote symbol. This triggers on blank lines with extra
> whitespace, as they are frequently the result of copy-and-paste artifacts.

### Correct Scenarios

This rule does not trigger when the start of any line in a block quote has zero
or one space character after the block quote symbol.

```Markdown
> This is text
>This is still text.
```

> **Explanation**: This example satisfies the rule because the first line has exactly
> one space after the block quote symbol, and the second line has zero spaces. Both
> are within the allowed range of zero or one spaces.

Unlike the previous example, this case shows text inside an Indented Code Block
element:

```Markdown
>     indented code block
```

> **Explanation**: This example satisfies the rule because the extra spaces after
> the block quote symbol are part of an Indented Code Block (four or more spaces),
> which is exempt from the rule. The spaces are required for the code block syntax,
> not a formatting error.

Unlike the previous example showing an Indented Code Block, this case demonstrates
an entire HTML Block element:

```Markdown
>  <!-- some comment -->
```

> **Explanation**: This example satisfies the rule because the content is part of
> an HTML Block element (an HTML comment). The rule does not apply to HTML Block
> elements, so the extra spaces after the block quote symbol are ignored.

Unlike the previous example, this case shows a Fenced Code Block where the
start and end lines have proper indentation, while the inner code lines
carry additional indentation.

````Markdown
> ```Python
>   a = a + 1
> ```
````

> **Explanation**: This example satisfies the rule because the start and end lines
> of
> the Fenced Code Block contain at most one space after the block quote symbol `>`.
> The extra indentation on the inner `a = a + 1` line is
> controlled by the Fenced Code Block itself and is therefore not evaluated by the
> rule.

Unlike the previous example, this case shows a list item and an Atx heading
inside a block quote where each has exactly one space after the block quote symbol:

```Markdown
> - This is a list item
> # This is a heading
```

> **Explanation**: This example satisfies the rule because both lines have exactly
> one space after the block quote symbol `>`. Unlike the failure cases, the single
> space is within the allowed zero-or-one range, so no violation occurs.

Unlike the previous example, this case shows a nested block quote where both
block quote symbols are followed by a single space:

```Markdown
> > This is nested
```

> **Explanation**: This example satisfies the rule because both the outer and inner
> block quote symbols are each followed by exactly one space. Since the rule evaluates
> each marker independently, neither exceeds the zero-or-one limit.

## Fix Description

After a block quote character and an optional space character, any spaces that
are not used to support an ongoing list container are removed. This keeps block
quotes visually
consistent across documents. For example:

```Markdown
>  # This is a header
```

and this example:

```Markdown
>  - This is a list item
```

will have the number of spaces at the start of the line reduced by 1. However, this
example:

```Markdown
> - This is a list item
>   and still the same item
```

will not reduce the spaces, as they are used to maintain the list.

## Configuration

| Prefixes |
| --- |
| `plugins.md027.` |
| `plugins.no-multiple-space-blockquote.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD027](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md027---multiple-spaces-after-blockquote-symbol).

### Differences From MarkdownLint Rule

The most obvious difference between implementations is in the treatment of extra
spaces on Blank Lines within a Block Quote element. Blank Lines within block quotes
often contain extra whitespace due to editing errors:

To improve visibility in the following example, the pipe character (`|`) marks line
endings for visibility and is not evaluated by the rule.

```Markdown
>  |
```

That example will trigger with this rule, but not with the original
rule.

The remaining differences are minor but have observable effects on rule triggering.

As explained
in the [above section](#correct-scenarios), only the characters inside a
Fenced Code Block are not scanned by this rule. This is a change
from the original rule which triggers on any part of a Fenced Code
Block element.

Also, as explained in the [above section](#failure-scenarios), only
certain parts of the Link Reference Definition are scanned by this
rule. Like the Fenced Code Block element, this is a change from the
original rule which triggers on any part of a Link Reference Definition
element.

Finally, the original rule does not trigger on the final line or
heading line for a Setext Heading element or on the Thematic Break
element. This implementation triggers when extra spaces are present in
either element.
