# Rule - MD014

| Property | Value |
| --- | --- |
| Aliases | `md014`, `commands-show-output` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Require output lines in code blocks prefixed with `$`.

## Reasoning

### Readability

Terminal simulations should distinguish between commands and output to aid reader comprehension. When every line starts with $, it falsely implies a command was issued with no visible result; requiring at least one non-prefixed line ensures output is shown or prompts are removed entirely, improving clarity.

## Examples

### Failure Scenarios

This rule triggers when every line within a code block begins with the `$` indicator.

````Markdown
```shell
$ ls /my/dir
$ cat /my/dir/file
```
````

> **Explanation**: This example fails because both lines start with `$`, and there are no lines without the `$` indicator to suggest command output. The rule requires that at least one line in the code block does not start with `$` to indicate output is present or commands are not prefixed.

Unlike the first example, this case includes leading spaces before the `$` indicator on each line.

````Markdown
```shell
  $ ls /my/dir
  $ cat /my/dir/file
```
````

> **Explanation**: This example fails because every line starts with `$` after optional leading whitespace. The rule considers leading spaces before the `$` indicator, and since all lines begin with `$` (ignoring leading spaces), there are no lines without the `$` indicator to suggest command output. The rule requires that at least one line in the code block does not start with `$` to indicate output is present or commands are not prefixed.

### Correct Scenarios

This rule does not trigger when the leading `$` indicators are removed from all lines in a code block containing only script input.

````Markdown
```shell
ls /my/dir
cat /my/dir/file
```
````

> **Explanation**: This example passes because none of the lines start with the `$` indicator. By removing the prefixes, the code block represents plain commands without implying a terminal session context, satisfying the rule's requirement for visibility.

Unlike the previous example, this case includes command output lines that do not start with `$`, demonstrating a terminal session context.

````Markdown
```shell
$ ls /my/dir
file
file2
$ cat /my/dir/file
```
````

> **Explanation**: This example passes because not every line starts with `$`. The lines `file` and `file2` represent command output, satisfying the rule's exception that allows `$` prefixes when output is also shown. This distinguishes it from the first correct scenario where all prefixes were removed.

## Fix Description

The reason for not being able to auto-fix this rule is context.  A developer can
reasonably be expected to look at this sample:

````Markdown
```shell
$ ls /my/dir
$ cat /my/dir/file
```
````

and this sample:

````Markdown
```shell
$ ls /my/dir
$ my_file
$ cat /my/dir/file
```
````

and make a reasonable guess that the output for both samples is from Linux systems
and that the second line of the second sample should not start with a `$` character.
While the algorithm for detecting when to trigger this rule is clear, a similar
algorithm to fix instances of this rule lacks the context to be clear.

## Configuration

| Prefixes |
| --- |
| `plugins.md014.` |
| `plugins.commands-show-output.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD014](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md014---dollar-signs-used-before-commands-without-showing-output).

### Differences From MarkdownLint Rule

The only difference is that when this rule is triggered by MarkdownLint, it is triggered
for every line in the code block, instead of just the first line in the code block.
Because this rule only triggers if every line starts with a dollar sign
character (`$`), it made more sense to only fire this rule once.
