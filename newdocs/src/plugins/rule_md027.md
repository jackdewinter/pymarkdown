# Rule - MD027

| Property | Value |
| --- | --- |
| Aliases | `md027`, `no-multiple-space-blockquote` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Do not use multiple spaces after the blockquote symbol.

## Reasoning

### Consistency

Consistent formatting improves readability across documents. This rule ensures that only zero or one space follows the blockquote symbol (`>`), helping maintain a uniform appearance.

## Examples

### Failure Scenarios

This rule triggers when multiple spaces follow a blockquote symbol.

```Markdown
>  This is text
```

> **Explanation**: This example violates the rule because there are two space characters after the blockquote symbol `>` on the first line. The rule requires zero or one space after the blockquote symbol.

Unlike the previous example, this case shows a blank line within a blockquote where extra spaces precede a pipe character used for visibility:

```Markdown
>  |
```

> **Explanation**: This example violates the rule because there are two spaces after the blockquote symbol `>`. The pipe character `|` is not part of the Markdown syntax but is included for visibility. The rule triggers because the extra spaces are not justified by any exempt element.

Unlike the previous examples, this case shows a list item inside a blockquote with extra spaces after the blockquote symbol:

```Markdown
>  - This is a list item
```

> **Explanation**: This example violates the rule because there are two spaces after the blockquote symbol `>`. The extra space before the list marker `-` is not justified by any exempt element, and the rule requires zero or one space after the blockquote symbol.

Unlike the previous example, this case demonstrates Setext headings with extra spaces after the blockquote symbol:

```Markdown
>   this is one Setext
> =====

> this is another Setext
>   =====
```

> **Explanation**: This example violates the rule because the first and fifth lines have extra spaces after the blockquote symbol `>`. The Setext heading underline lines (lines 1 and 5) also trigger the rule because extra spaces are present after `>`, even though they are part of a Setext heading.

Unlike the previous example, this case shows a thematic break with extra spaces after the blockquote symbol:

```Markdown
>  ----
```

> **Explanation**: This example violates the rule because there are two spaces after the blockquote symbol `>`. The thematic break line triggers the rule because the extra spaces are not justified by any exempt element.

Unlike the previous example, this case shows a Link Reference Definition element with extra spaces in the non-Label and non-Title parts of the element:

```Markdown
>  [lab
>  el]:
>  /url
>  "tit
>  le"
```

> **Explanation**: This example violates the rule on lines 1, 3, and 4 because each has two spaces after the blockquote symbol. The Link Label part (`el]:`) and Link Title part (`"tit`) are excluded from the rule because they require the extra space for proper formatting, but the other lines do not have this exception and thus trigger the rule.

Unlike the previous example, this case shows a Fenced Code Block where the content inside is safe, but the opening and closing lines still trigger the rule due to extra spaces after the blockquote symbol:

````Markdown
>  ```Python
>  a = a + 1
>  ```
````

> **Explanation**: This example triggers because the start and end lines of the Fenced Code Block are not immune to triggering, even though the content inside is exempt.

### Correct Scenarios

This rule does not trigger when the start of any line in a block quote has
zero or one space characters:

```Markdown
> This is text
>This is still text.
```

> **Explanation**: This example satisfies the rule because the first line has exactly one space after the blockquote symbol, and the second line has zero spaces. Both are within the allowed range of zero or one spaces.

Unlike the previous example, this case shows text inside an Indented Code Block element:

```Markdown
>     indented code block
```

> **Explanation**: This example satisfies the rule because the extra spaces after the blockquote symbol are part of an Indented Code Block (four or more spaces), which is exempt from the rule. The spaces are required for the code block syntax, not a formatting error.

Unlike the previous example showing an Indented Code Block, this case demonstrates an entire HTML Block element:

```Markdown
>  <!-- some comment -->
```

> **Explanation**: This example satisfies the rule because the content is part of an HTML Block element (an HTML comment). The rule does not apply to HTML Block elements, so the extra space after the blockquote symbol is ignored.

Unlike the previous example, this case shows a Fenced Code Block where the start and end lines have proper indentation, even if the FCB contents are indented extra.

````Markdown
> ```Python
>   a = a + 1
> ```
````

> **Explanation**: Start and end of code block adhere to indentation, and anything within the block has its indentation controlled by the FCB, meaning it does not trigger.

## Fix Description

After a block quote character and an optional space character, any spaces that
are not used for a list container are removed. Therefore, this example

```Markdown
>  # This is a header
```

and this example:

```Markdown
>  - This is a list item
```

will have the number of spaces at the start of the line reduced by 1.  However, this
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
spaces on Blank Lines within a Block Quote element.  Blank Lines within block quotes often contain extra whitespace due to editing errors:

To improve visibility in the following example, the pipe character (`|`) marks line endings for visibility and is not evaluated by the rule.

```Markdown
>  |
```

That example will trigger with this rule, but not with the original
rule.

The rest of the differences are small, but meaningful.

As explained
in the [above section](#correct-scenarios), only the characters inside of a
Fenced Code Block are not scanned by this rule.  This is a change
from the original rule which triggers on any part of a Fenced Code
Block element.

Also, as explained in the [above section](#failure-scenarios), only
certain parts of the Link Reference Definition are scanned by this
rule.  Like the Fenced Code Block element, this is a change from the
original rule which triggers on any part of a Link Reference Definition
element.

Finally, the original rule does not trigger on the final line or
heading line for a Setext Heading element or on the Thematic Break
element.  This implementation triggers when extra spaces are present in
either element.
