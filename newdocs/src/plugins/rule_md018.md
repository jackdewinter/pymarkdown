# Rule - MD018

| Property | Value |
| --- | --- |
| Aliases | `md018`, `no-missing-space-atx` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Ensure at least one space exists between hash marks and text in Atx Open Headings.

## Reasoning

**Scope Boundary**: This rule checks open-style headings only. [Rule MD020](./rule_md020.md)
checks closed-style headings. A heading is "closed" if it ends with one or more
hash characters (e.g., `# Heading #`).

### Correctness

In most Markdown parsers, hash characters (`#`) followed immediately by text (without
a space) are still interpreted as Atx Headings. This rule alerts authors when the
required space after the hash character(s) is missing, helping them determine whether
the omission was accidental.

## Examples

### Failure Scenarios

This rule triggers when a line starts with 1-6 hash characters followed immediately
by non-space text, indicating a missing space in an Atx Heading.

```Markdown
#Heading 1
```

> **Explanation**: The line `#Heading 1` starts with a single `#` followed immediately
> by `Heading` without a space. This violates the requirement for a space after
> the hash character(s) in an Atx Heading.

Unlike the previous example, this case shows the rule triggering inside a block
quote, ensuring the rule checks headings within nested block structures.

```Markdown
> #Heading 1
```

> **Explanation**: Even though the heading is inside a block quote (`>`), the content
> `#Heading 1` still lacks the required space after the `#`. The rule applies to
> headings in block quotes as well.

Unlike the previous example, this case shows the rule triggering inside a list
item, ensuring the rule checks headings within list structures.

```Markdown
- #Heading 1
  ##Heading2
```

> **Explanation**: The lines `#Heading 1` and `##Heading2` are inside a list item.
> Despite the indentation and list context, the hash characters are immediately
> followed by text without a space. The rule applies to headings within list items,
> just as it does for block quotes.

### Correct Scenarios

This rule does not trigger when there is at least one space character between the
last hash character and the first non-space character, satisfying the Atx Heading
syntax.

```Markdown
# Heading 1
```

> **Explanation**: The line `# Heading 1` includes a space between `#` and `Heading`,
> conforming to the correct Atx Heading format. Thus, the rule does not fire.

Unlike the previous example, this case shows text that looks like a heading but
is part of a Setext Heading, where the hash characters are not interpreted as
Atx delimiters.

```Markdown
#Heading 1
----
```

> **Explanation**: Here, `#Heading 1` is the title of a Setext Heading (indicated
> by the `----` below). Since the parser identifies this as a Setext element,
> the Atx heading rule does not apply to the hash characters.

This scenario differs by showing that lines with more than 3 leading spaces are
treated as Indented Code Blocks, not headings, so the rule ignores them.

```Markdown
    #Heading 1
```

> **Explanation**: The four leading spaces convert the line into an Indented Code
> Block. Atx Heading parsing does not apply to code blocks, so the missing space
> is ignored.

This case shows that more than 6 hash characters at the start of a line prevent
Atx Heading parsing, as valid Atx Headings allow only 1-6 hashes.

```Markdown
#######Heading 7
```

> **Explanation**: Seven hash characters exceed the maximum allowed for an Atx Heading.
> Therefore, this is not parsed as a heading, and the rule does not trigger.

This scenario shows that if there is no text following the hash characters, it is
not considered a heading with missing space, but potentially an empty heading or
invalid syntax.

```Markdown
##
```

> **Explanation**: The line contains only hash characters with no following text.
> Since there is no "heading text" to have a space before, the specific "missing
> space" violation does not apply.

Unlike the previous cases, this example includes inline elements (emphasis),
which prevents the line from being parsed as a simple Atx Heading.

```Markdown
#Heading *1*
```

> **Explanation**: Although the line begins with `#Heading`, the presence of inline
> markup (`*1*`) places this candidate outside the trigger conditions for this rule.
> This rule targets lines where the entire remainder after the hash is plain heading
> text with a missing space; lines containing inline elements are treated as paragraphs
> for this rule's purposes, so the missing-space check does not apply.

This final scenario shows that headings with closing hash characters are handled
by a different rule (MD020), so this rule does not trigger for missing spaces when
closing hashes are present.

```Markdown
#Heading1#
```

> **Explanation**: The line `#Heading1#` contains a closing hash character. The
> management of possible closed-style Atx headings is covered by [Rule MD020](./rule_md020.md).
> This rule does not trigger here because the handling of possible closed-style
> Atx headings falls outside its scope.

## Fix Description

The reason for not being able to auto-fix this rule is context. As stated above,
the rule looks for:

> No space present after the hash character on a possible Atx Heading.

As there is only a possibility that the Markdown:

```Markdown
#Heading 1
```

represents a heading, there is a lack of context surrounding the implied meaning
of that block of text. It is better for this rule to trigger and have the author
of the document clarify the context than to assume that the above text will always
indicate a heading.

## Configuration

| Prefixes |
| --- |
| `plugins.md018.` |
| `plugins.no-missing-space-atx.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD018](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md018---no-space-after-hash-on-atx-style-heading).

### Differences From MarkdownLint Rule

This rule was inspired by the above MarkdownLint rule, with refinements to address
areas where the previous implementation was incomplete. The most significant change
is that the original rule did not trigger when the candidate line was inside a block
quote or a list. Because the parsers reviewed for this project support Atx Heading
elements inside Block Quote and List elements, the rule was extended to cover those
contexts as well.

The next change is that the original rule triggered when the candidate text appeared
within a Setext Heading element. This was removed: the presence of Setext Heading
delimiters after the text indicates author intent to treat the line as a Setext
Heading, not an Atx Heading, so the rule no longer fires in that case.

Finally, the original rule triggered regardless of what other text appeared on the
candidate line. After deliberation, this behavior was removed: the structural distance
from a Paragraph element to an Atx Heading element is too great when inline elements
(such as emphasis) are involved, so the rule now ignores such lines.
