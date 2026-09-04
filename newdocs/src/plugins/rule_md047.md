# Rule - MD047

| Property | Value |
| --- | --- |
| Aliases | `md047`, `single-trailing-newline` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Each file should end with a single newline character.

## Reasoning

### Consistency

Various parsers and operating systems expect text files to end with a single newline character. POSIX systems, in particular, mandate this convention. Ending Markdown documents with a single newline ensures compatibility across these systems.

## Examples

> **Note on Invisible Characters**: In the following examples, invisible characters are represented visually to aid understanding:
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

> **Explanation**: The file ends immediately after the period in "newline." with no newline character (`↵`) following. The rule requires exactly one newline as the final character in the file, ensuring POSIX compatibility.

Unlike the previous example, this case ends with a newline but includes additional blank lines (multiple newlines) at the end of the file.

```Markdown
# Heading↵
↵
This file ends with multiple newlines.↵
↵
↵
```

> **Explanation**: The file ends with three newline characters (`↵↵↵`). The rule requires **exactly one** newline character as the final character. Extra trailing newlines constitute a failure because the file does not end with a *single* newline.

Unlike the previous example, this case includes a newline character but is followed by trailing whitespace.

```Markdown
# Heading↵
↵
This file ends with a newline followed by two spaces.↵
⎵⎵
```

> **Explanation**: Although a newline character (`↵`) exists, it is followed by two space characters (`⎵`). The rule requires the newline to be the **final** character in the file. Any trailing whitespace after the newline causes a failure.

### Correct Scenarios

This rule does not trigger when the document ends with a single newline character.

```Markdown
# Heading↵
↵
This file ends with a single trailing newline.↵
↵
```

> **Explanation**: The file ends with exactly one newline character after the last line of content (`newline.`). No trailing whitespace follows the newline, satisfying the rule's requirement.

## Fix Description

If the document does not end with a single newline character, a newline character is added to the end of the document.

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
