# Rule - MD014

| Aliases |
| --- |
| `md014` |
| `commands-show-output` |

## Summary

Dollar signs used before commands without showing output.

## Reasoning

The primary reason for enabling this rule is that Bash-style script text
are more readable and ready for copy-and-paste when the `$` indicator for
a new script line is removed.  The exception to this rule is when the
script text includes both the input and the output for the script.

As long as one line without the leading indicator is present in the code
block, this rule will not fire.  This is present to take into account
that some commands do not produce any output.

## Examples

### Failure Scenarios

This rule triggers if every line within a Code Block element begins with
the `$` indicator, after any leading whitespace has been removed.

````Markdown
```shell
$ ls /my/dir
$ cat /my/dir/file
```
````

### Correct Scenarios

There are two ways in which to correct the above example.  If the writer
intends to show only the script input commands, then the example can be
corrected by removing the leading `$` indicator from each line.

````Markdown
```shell
ls /my/dir
cat /my/dir/file
```
````

Note that while technically only one leading `$` needs to be removed to
prevent this rule from triggering, that will leave some of the commands
with the leading character and some without.  It is recommended that
all leading `$` characters are removed.

However, if the writer's intent is to show both the script input and the
script output, the other alternative is to include the output of each
line following the line that generated the output:

````Markdown
```shell
$ ls /my/dir
file
file2
$ cat /my/dir/file
```
````

## Configuration

| Prefixes |
| --- |
| `plugins.md014.` |
| `plugins.commands-show-output.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the plugin rule is enabled by default. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD014](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md014---dollar-signs-used-before-commands-without-showing-output).

### Differences From MarkdownLint Rule

The only difference is that when this rule is triggered, it is triggered for
every line in the code block, instead of just the first line in the code block.
Because this rule only triggers if every line starts withe a dollar sign
character (`$`), it made more sense to only fire this rule once.
