# Rule - MD026

| Aliases |
| --- |
| `md026` |
| `no-trailing-punctuation` |

## Summary

Trailing punctuation present in heading text.

## Reasoning

Headings are meant to be the titles for separate sections of the document,
not complete sentences.  Except for the question mark character (`?`), often
used for a section title that contains a question, no other sentence ending
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
| `enabled` | `boolean` | `False` | Whether the plugin rule is enabled by default. |
| `punctuation` | `string` | `".,;:!。，；：！"` | Punctuation characters that are considered sentence ending characters. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD026](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md026---trailing-punctuation-in-heading).
and
[this article](https://cirosantilli.com/markdown-style-guide#punctuation-at-the-end-of-headers).

### Differences From MarkdownLint Rule

The main difference encountered was that the original rule did not handle
anything to do with multiple line SetExt Heading elements.
