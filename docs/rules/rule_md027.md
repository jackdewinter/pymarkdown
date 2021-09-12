# Rule - MD027

| Aliases |
| --- |
| `md027` |
| `no-multiple-space-blockquote` |

## Summary

Multiple spaces after blockquote symbol.

## Reasoning

One of the main keys to readability is to have consistent formatting applied
throughout a group of documents.  Extending the concept even further, many
organizations have specific rules on how documents should be authored throughout
that organization.  It follows that both concepts may extend to specifying
that only zero or one space characters can follow the block quote character
(`>`).

The exceptions to this rule are the

## Examples

### Failure Scenarios

This rule triggers when the start of any line in a block quote has more than
one space character:

```Markdown
>  This is text
```

Most of the exceptions for triggering this rule are detailed in the following section
on Correct Scenarios.  One that bears special mention is the Link Reference Definition
element.  A Link Reference Definition element that has extra spaces in the non-Label
and non-Title parts of the element will trigger this rule:

```Markdown
>  [lab
>  el]:
>  /url
>  "tit
>  le"
```

The above example will trigger the rule three times.  Once for the first line,
once for the third line, and once for the fourth line.  Because the Link Label
part and the Link Title part of the element may require that extra space to be
present for some reason, they are excluded from the trigger conditions for this
rule.

### Correct Scenarios

This rule does not trigger when the start of any line in a block quote has
zero or one space characters:

```Markdown
> This is text
>This is still text.
```

This rule does not trigger at any text inside of a Fenced Code Block element,
any text in an Indented Code Block element, or any text in a HTML Block element.
Similar to the reasons for excluding certain parts of the Link Reference
Definition element from triggering this rule (see last section), the text in
these areas have special meaning which may include the presence of any
space characters.  Note that while an entire Indented Code Block element
will not trigger this rule:

```Markdown
>     indented code block
```

and an entire HTML Block element will not trigger this rule:

```Markdown
>  <!-- some comment -->
```

only the *inside* parts of a Fenced Code Block element will trigger
this rule:

````Markdown
>  ```Python
>   a = a + 1
>  ```
````

For the Fenced Code Block element example, the extra spaces for the
first line (opening the Fenced Code Block element) and the last line
(closing the Fenced Code Block element) will trigger this rule, while
the second line (inside the Fenced Code Block element) will not trigger
this rule.

### Future

For reasons similar to the ones already expressed above, the
Link element and the Raw HTML element should not trigger this rule.
Currently, these two elements are not treated any differently than
any of the other text within a Paragraph element.

This will be changed in a future release.

## Configuration

| Prefixes |
| --- |
| `plugins.md027.` |
| `plugins.no-multiple-space-blockquote.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled by default. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD027](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md027---multiple-spaces-after-blockquote-symbol).

### Differences From MarkdownLint Rule

The most obvious difference between is in the treatment of extra
spaces on Blank Lines within a Block Quote element.  A frequent
victim of cut-and-paste accidents, there are often times when a
Blank Line is followed by extra whitespace characters, as such:

```Markdown
>{space}{space}
```

That example will trigger with this rule, but not with the original
rule.

The rest of the differences are small, but meaningful.

As explained
in the [above section](#correct-scenarios), only the inside of a
Fenced Code Block are not scanned by this rule.  This is a change
from the original rule which triggers on any part of a Fenced Code
Block element.

Also, as explained in the [above section](#failure-scenarios), only
certain parts of the Link Reference Definition are scanned by this
rule.  Like the Fenced Code Block element, this is a change from the
original rule which triggers on any part of a Link Referenced Definition
element.

Finally, the original rule does not trigger on the final line or
heading line for a SetExt Heading element or on the Thematic Break
element.  This implementation triggers on extra spaces present in
either element.
