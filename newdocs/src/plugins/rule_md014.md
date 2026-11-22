# Rule - MD014

| Property | Value |
| --- | --- |
| Aliases | `md014`, `commands-show-output` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Require that at least one line in a code block is not prefixed with `$`, indicating
that command output is visible.

## Reasoning

### Readability

Readers of terminal simulations in fenced code blocks rely on the `$` prompt to
distinguish commands from output. When every line is prefixed with `$`, output becomes
invisible, making it impossible to tell what a command produced.

## Examples

### Failure Scenarios

This rule triggers when every line within the code block contains the `$` indicator
alone on a line or contains the `$` indicator followed by a space character and
then one or more non-space characters.

````Markdown
```shell
$ ls /my/dir
$ cat /my/dir/file
```
````

> **Explanation**: This example fails because both lines start with `$`, and there
> are no lines without the `$` indicator to suggest command output. The rule requires
> that at least one line in the code block does not start with `$` to indicate that
> the block contains command output.

Unlike the first example, this case includes leading spaces before the `$` indicator
on each line.

````Markdown
```shell
  $ ls /my/dir
  $ cat /my/dir/file
```
````

> **Explanation**: This example fails because every line begins with `$` after optional
> leading whitespace. The rule ignores leading whitespace before `$`, so the presence
> of two leading spaces does not exempt the line. Because no line is free of a leading
> `$`, the rule's requirement — that at least one line in the block does not start
> with `$` — is not satisfied.

Unlike the previous example, this case mixes a `$`-prefixed command line with a
line that is just a lone `$` (no trailing characters).

````Markdown
```shell
$ ls /my/dir
$
```
````

> **Explanation**: This example fails because, after the bare `$` line, no line is
> present that shows command output. The lone `$` does not qualify as output; the
> rule still requires at least one line in the block to be free of a leading `$`.

### Correct Scenarios

This rule does not trigger when the leading `$` indicators are removed from all
lines in a code block containing only script input.

````Markdown
```shell
ls /my/dir
cat /my/dir/file
```
````

> **Explanation**: This example passes because no line begins with the `$` indicator,
> so the rule's trigger condition (every line prefixed with `$`) is not met.

Unlike the previous example, this case includes command output lines that do not
start with `$`, demonstrating a terminal session context.

````Markdown
```shell
$ ls /my/dir
file
file2
$ cat /my/dir/file
```
````

> **Explanation**: This example passes because not every line starts with `$`. The
> lines `file` and `file2` represent command output, satisfying the rule's exception
> that allows `$` prefixes when output is also shown. This distinguishes it from
> the first correct scenario where all prefixes were removed.

Unlike the previous example, this case shows a line where a non-space character
directly follows the `$` (a Bash variable expansion), which the rule does not
treat as a command prompt.

````Markdown
```shell
${some-bash-environment-variable}
```
````

> **Explanation**: This example passes because the `$` is immediately followed by
> a non-space character (`{`), which the rule does not interpret as the command
> prompt indicator. The block therefore does not meet the trigger condition that
> every line is a `$`-prefixed command.

Unlike the previous example, this case uses the PowerShell `$env:` syntax, where
a non-space character (`:`) directly follows the `$`.

````Markdown
```shell
$env:PYTHONUTF8 = "1"
```
````

> **Explanation**: This example passes for the same reason as the Bash case: the
> `$` is immediately followed by a non-space character (`:`), so the rule does
> not treat it as the command prompt indicator. The trigger condition is not met.

## Fix Description

The reason for not being able to auto-fix this rule is context. A developer can
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

The only difference is that when this rule is triggered by MarkdownLint,
it is triggered for every line in the code block, instead of just the
first line in the code block. Because this rule only triggers if every
line starts with a dollar-sign character (`$`), the implementation
reports the violation only once per code block.
