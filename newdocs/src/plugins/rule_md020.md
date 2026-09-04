# Rule - MD020

| Property | Value |
| --- | --- |
| Aliases | `md020`, `no-missing-space-closed-atx` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Ensure at least one space exists between hash marks and text in Atx Closed Headings.

**Scope Boundary**: This rule checks closed-style headings only. [Rule MD018](./rule_md018.md) checks open-style headings. A heading is "open" if it does not end with one or more hash characters (e.g., `# Heading`).

## Reasoning

### Correctness

Missing spaces between hash marks and heading text in Atx Closed Headings can make headings harder to read and may confuse parsers. Consistent spacing improves both readability and document correctness.

## Examples

### Failure Scenarios

This rule triggers when there is no space between the opening hash marks and the heading text in an Atx Closed Heading.

```Markdown
#Heading 1 #
```

> **Explanation**: This example violates the rule because there is no space between the opening `#` and the heading text `Heading 1`. An Atx Closed Heading requires at least one space after the opening hash marks.

Unlike the previous example, this case has a space after the opening hash but no space before the closing hash.

```Markdown
# Heading 1#
```

> **Explanation**: This example violates the rule because there is no space between the heading text `Heading 1` and the closing `#`. An Atx Closed Heading requires at least one space before the closing hash marks.

This case lacks spaces on both sides of the heading text.

```Markdown
#Heading 1#
```

> **Explanation**: This example violates the rule because there are no spaces between the hash marks and the heading text `Heading 1`. An Atx Closed Heading requires at least one space after the opening hash marks and before the closing hash marks.

### Correct Scenarios

This rule does not trigger when there are 1 or more spaces on either side of the Atx Closed Heading:

```Markdown
## Heading 2 ##
```

> **Explanation**: This example satisfies the rule because there is at least one space after the opening `##` and before the closing `##`. The heading text `Heading 2` is properly padded.

This final scenario shows that headings without closing hash characters are handled by a different rule (MD018), so MD020 does not trigger for missing spaces when closing hashes are present.

```Markdown
#Heading1
```

> **Explanation**: The line `#Heading1` does not contain a closing hash character. The management of closing hashes is covered by [Rule MD018](./rule_md018.md). This rule does not trigger here because the handling of possible open-style Atx headings falls outside its scope.

## Fix Description

The reason for not being able to auto-fix this rule is context.  As stated above,
the rule looks for:

> No space present inside of the hashes on a possible Atx Closed Heading.

As there is only a possibility that the Markdown:

```Markdown
#Heading 1#
```

represents a heading, there is a lack of context surrounding the implied meaning
of that block of text.  It is better for this rule to trigger and have the author
of the document clarify the context than to assume that the above text will always
indicate a heading.

## Configuration

| Prefixes |
| --- |
| `plugins.md020.` |
| `plugins.no-missing-space-closed-atx.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD020](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md020---no-space-inside-hashes-on-closed-atx-style-heading).

### Differences From MarkdownLint Rule

Like the PyMarkdown version of
[Rule MD018](./rule_md018.md), the original version of this rule did not trigger in Block Quote elements or
List elements but did fire within Setext Heading elements.  These
changes were also made to this rule to keep it consistent with
Rule MD018.
