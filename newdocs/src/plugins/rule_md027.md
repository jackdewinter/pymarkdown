# Rule - MD027

| Property | Value |
| --- | -- |
| Aliases | `md027`, `no-multiple-space-blockquote` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Multiple spaces after blockquote symbol.

## Reasoning

### Consistency

One of the main keys to readability is to have consistent formatting applied
throughout a group of documents.  Extending the concept even further,
organizations may have specific rules on how documents should be authored throughout
that organization.  It follows that both concepts may extend to specifying
that only zero or one space characters can follow the block quote character
(`>`).

## Examples

As the space character is not normally visible, each occurrence of
the text `{space}` in the following example stands for a single
space character.

### Failure Scenarios

This rule triggers when the start of any line in a block quote has more than
one space character:

```Markdown
>  This is text
```

The exceptions for triggering this rule are detailed in the following section
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
present, they are excluded from the trigger conditions for this rule.

### Correct Scenarios

This rule does not trigger when the start of any line in a block quote has
zero or one space characters:

```Markdown
> This is text
>This is still text.
```

This rule does not trigger on any text inside of a Fenced Code Block element,
any text inside of an Indented Code Block element, or any text inside of a HTML
Block element. Like the reasons for excluding certain parts of the Link Reference
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

For reasons like the ones already expressed above, the
Link element and the Raw HTML element should not trigger this rule.
Currently, these two elements are not treated any differently than
any of the other text within a Paragraph element.

This is slated to be changed in a future release.

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
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD027](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md027---multiple-spaces-after-blockquote-symbol).

### Differences From MarkdownLint Rule

The most obvious difference between implementations is in the treatment of extra
spaces on Blank Lines within a Block Quote element.  A frequent
victim of cut-and-paste accidents, it is not unusual to have a
Blank Line that is followed by extra whitespace characters:

```Markdown
>{space}{space}
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
original rule which triggers on any part of a Link Referenced Definition
element.

Finally, the original rule does not trigger on the final line or
heading line for a SetExt Heading element or on the Thematic Break
element.  This implementation triggers when extra spaces are present in
either element.
