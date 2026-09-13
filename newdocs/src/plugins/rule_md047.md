# Rule - MD047

| Property | Value |
| --- | --- |
| Aliases | `md047`, `single-trailing-newline` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

End each file with a single newline character.

## Reasoning

### Consistency

POSIX systems, and many parsers and tools, expect text files to end with a single
newline character. Ending Markdown documents with a single newline preserves compatibility
across these systems.

## Examples

> **Note on Invisible Characters**: In the following examples, invisible characters
> are represented visually to aid understanding:
>
> - `↵` represents a newline character (`\n`).
> - `⎵` represents a space character.
> - `⇥` represents a tab character.

### Failure Scenarios

This rule triggers when the document does not end with a single newline character.

```Markdown
# Heading↵
↵
This file ends without a newline.
```

> **Explanation**: The file ends immediately after the period in "newline." with
> no newline character (`↵`) following. The rule requires exactly one newline as
> the final character in the file, ensuring POSIX compatibility.

Unlike the previous example, this case ends with a newline but includes additional
blank lines (multiple newlines) at the end of the file.

```Markdown
# Heading↵
↵
This file ends with multiple newlines.↵
↵
↵
```

> **Explanation**: The file ends with three newline characters (`↵↵↵`). The rule
> requires **exactly one** newline character as the final character. Extra trailing
> newlines constitute a failure because the file does not end with a *single* newline.

Unlike the previous example, this case has the required trailing newline, but
**two space characters follow that newline**, so the file's final bytes are whitespace
rather than the newline itself — a different failure mode than the excess-newline
case above.

```Markdown
# Heading↵
↵
This file ends with a newline followed by two spaces.↵
⎵⎵
```

> **Explanation**: Although a newline character (`↵`) exists, it is followed by
> two space characters (`⎵`). The rule requires the newline to be the **final**
> character in the file. Any trailing whitespace after the newline causes a failure.

### Correct Scenarios

This rule does not trigger when the document ends with a single newline character.

```Markdown
# Heading↵
↵
This file ends with a single trailing newline.↵
```

> **Explanation**: The file ends with exactly one newline character after the last
> line of content (`newline.`). No trailing whitespace follows the newline, satisfying
> the rule's requirement.

Unlike the previous example, this case ends with a single trailing newline even
though the last line of content is a heading.

```Markdown
# Heading↵
```

> **Explanation**: The file's only line is a heading, and exactly one newline character
> (`↵`) follows it. The rule does not require any particular *kind* of content —
> only that the file terminate with a single newline. This satisfies the rule.

Unlike the previous example, this case ends with a blockquote rather than a paragraph
or heading, yet still terminates with exactly one newline.

```Markdown
# Heading↵
↵
> A quoted line of text.↵
```

> **Explanation**: The last line of content is a blockquote
> (`> A quoted line of text.`), and exactly one newline character (`↵`) follows
> it. Because the rule only inspects the final bytes of the file, the content type
> is irrelevant — what matters is the single trailing newline, which is satisfied
> here.

Unlike the previous example, this case ends with a list item rather than a paragraph
or heading, yet still terminates with exactly one newline.

```Markdown
# Heading↵
↵
- First item↵
- Second item↵
```

> **Explanation**: The last line of content is a list item (`- Second item`), and
> exactly one newline character (`↵`) follows it. The rule's criterion — exactly
> one newline as the file's final character, with no trailing whitespace — is met,
> independent of the list-item structure.

## Fix Description

If the document does not end with a single newline character, a newline character
is added to the end of the document. If the document ends with multiple newline
characters or with trailing whitespace after the final newline, those extra characters
are trimmed so that exactly one newline remains as the final character of the file.

## Configuration

| Prefixes |
| --- |
| `plugins.md047.` |
| `plugins.single-trailing-newline.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD047](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md047---files-should-end-with-a-single-newline-character).
and various blogs and answers such as
[this answer](https://unix.stackexchange.com/questions/18743/whats-the-point-in-adding-a-new-line-to-the-end-of-a-file).
