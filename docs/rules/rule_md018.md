# Rule - MD018

| Aliases |
| --- |
| `md018` |
| `no-missing-space-atx` |

| Autofix Available |
| --- |
| No |

## Summary

No space present after the hash character on a possible Atx Heading.

## Reasoning

### Correctness

In most cases, one or more hash characters (`#`) followed by text was
probably meant to indicate an Atx Heading, with the space between the
hash characters and the text being omitted.  The triggering of this rule
will allow the document's author to decide on whether the o mission of
the space was accidental or not.

## Examples

### Failure Scenarios

This rule triggers when a sequence of characters occurs at the start of a line in
a paragraph after between 0 and 3 leading spaces are removed.  After those leading
spaces are removed, this rule then looks for between 1 and 6 hash characters (`#`)
followed by at least one non-space character.

```Markdown
#Heading 1
```

This rule triggers under these circumstances even if the text is at the start
of its own line within a block quote:

```Markdown
> #Heading 1
```

or an ordered or unordered list:

```Markdown
- #Heading 1
  ##Heading2
```

### Correct Scenarios

This rule does not trigger in five distinct scenarios.  The simplest scenario
where this rule does not fire is when there is correctly at least one
space character between the last hash character (`#`) and the first
non-space character:

```Markdown
# Heading 1
```

Assuming that there is no space character between the hash character and
the first non-space character, the next most common scenario where this rule
does not trigger is if that sequence is not in a Paragraph element.  This often
occurs when the text is inside of another element that looks like a Paragraph
element, such as the text inside of a SetExt Heading element:

```Markdown
#Heading 1
----
```

Within a Paragraph element, this rule does not trigger if there are more
than 3 space characters at the start of the line (making it an
Indented Code Block):

```Markdown
    #Heading 1
```

or if the text would not be a valid Atx Heading element due to excess hash characters:

```Markdown
#######Heading 7
```

or due to no text following the hash characters:

```Markdown
##
```

Another scenario in which this rule does not trigger is when the line
holding the otherwise eligible text has any inline elements
within that same line.

```Markdown
#Heading *1*
```

While this line would be a valid Atx Heading element if the proper spacing
was present, the presence of the inline Emphasis element prevents it from
triggering.  

Finally, this rule will not trigger if the Atx Heading element has closing
hash characters, such as `#Heading1#`.  The rule for effectively managing Atx
Heading Close elements is
[Rule md020](https://github.com/jackdewinter/pymarkdown/blob/main/docs/rule_md020.md).

## Configuration

| Prefixes |
| --- |
| `plugins.md018.` |
| `plugins.no-missing-space-atx.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD018](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md018---no-space-after-hash-on-atx-style-heading).

### Differences From MarkdownLint Rule

While this rule was inspired by the above MarkdownLint rule, improvements
were made to make the rule more complete.  The biggest change was that the
original rule did not trigger if the line was not in a block quote or a list.
As most of the researched parsers support Atx Heading elements within
Block Quote elements and List elements, this just made sense.

The next change was that the original rule triggered if the possibly
eligible text occurred within a SetExt Heading element. This did not make
sense as the presence of the SetExt Heading specifiers after the text
present an intention to have that text be part of a SetExt Heading element,
not an Atx Heading element.

Finally, the last change was that the original rule triggered regardless of
what extra text occurred on the possibly eligible line.  The decision to add
that change to the trigger conditions was arrived at after significant
deliberation.  It was decided that the "logical distance" to go from
text within a Paragraph element to text within an Atx Heading element
was too far once inline elements were included.

## Fix Description

The reason for not being able to auto-fix this rule is context.  As stated above,
the rule looks for:

> No space present after the hash character on a possible Atx Heading.

As there is only a possibilty that the Markdown:

```Markdown
#Heading 1
```

represents a heading, there is a lack of context surrounding the implied meaning
of that block of text.  It is better for this rule to trigger and have the author
of the document clarify the context than to assume that the above text will always
indicate a heading.
