# Rule - MD026

| Aliases |
| --- |
| `md026` |
| `no-trailing-punctuation` |

| Autofix Available |
| --- |
| No |

## Summary

Trailing punctuation present in heading text.

## Reasoning

### Readability

Headings are meant to be the titles for separate sections of the document,
not complete sentences.  Except for the question mark character (`?`), often
used for a section title that asks a question, no other sentence ending
punctuation characters should be used.

## Examples

### Failure Scenarios

This rule triggers when a heading ends with a punctuation character that
makes it look like a sentence:

```Markdown
# This is a heading.
```

### Correct Scenarios

This rule does not trigger when the heading does not end with one of the
configured punctuation characters.

```Markdown
# This is a heading

# Is this is a heading?
```

Even though the semicolon character (`;`) is in the default list of punctuation
characters, this rule does not trigger when that character is used as part of
one of the entities:

```Markdown
# This is a heading &copy;

# This is a heading &#169;

# This is a heading &#x000A9;
```

## Configuration

| Prefixes |
| --- |
| `plugins.md026.` |
| `plugins.no-trailing-punctuation.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |
| `punctuation` | `string` | `.,;:!。，；：！` | Punctuation characters that are considered sentence ending characters. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD026](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md026---trailing-punctuation-in-heading).
and
[this article](https://cirosantilli.com/markdown-style-guide#punctuation-at-the-end-of-headers).

### Differences From MarkdownLint Rule

The main difference met was that the original rule did not manage
anything to do with multiple line SetExt Heading elements.

## Fix Description

The reason for not being able to auto-fix this rule is context.  While our team
considered simply removing any offending punctuation, the author of the document
put it there for a reason.  Without understanding the intended context of that punctuation
and the proper classification of that punctuation, designing an algorithm that
properly handles the punctuation is not currently possible.
