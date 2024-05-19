# Rule - MD047

| Property | Value |
| --- | -- |
| Aliases | `md047`, `single-trailing-newline` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Each file should end with a single newline character.

## Reasoning

### Consistency

Various parsers and operating system calls have trouble with files that
do not end with at least one newline character.
It is common on any POSIX operating systems to mandate that each text file
be ended with a single newline character.  To make the Markdown
documents compatible with these various systems, it just makes sense to
end documents with a newline character.

## Examples

As the space character is not normally visible, each occurrence of
the text `{space}` in the following example stands for a single
space character.

### Failure Scenarios

This rule triggers when the document does not end with a single
newline character.

```Markdown
# Heading

This file ends without a newline.
```

This includes triggering on a final line that has a newline
character followed by one or more whitespace characters.  To
properly illustrate this, the space characters at the end of the
following example have been replaced with the string `{space}`
to make those space characters visible.

```Markdown
# Heading

This file ends with a newline and two space characters.
{space}{space}  
```

### Correct Scenarios

This rule does not trigger when the document does end with a single
newline character.

```Markdown
# Heading

This file ends with a newline.

```

In most editors, if the current file ends with a single newline character,
it will appear to be a line with nothing on it.  The difficulty with using
this as the visual indicator is that most editors do not display a document
ending in a newline character any differently than a document ending with
a newline characters and one or more whitespace characters.

## Fix Description

If the document does not end with a blank line, a blank line is added to the
end of the document.

## Configuration

| Prefixes |
| --- |
| `plugins.md047.` |
| `plugins.single-trailing-newline.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD047](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md047---files-should-end-with-a-single-newline-character).
and various blogs and answers such as
[this answer](https://unix.stackexchange.com/questions/18743/whats-the-point-in-adding-a-new-line-to-the-end-of-a-file).
