# Rule - MD040

| Aliases |
| --- |
| `md040` |
| `fenced-code-language` |

## Summary

Fenced code blocks should have a language specified.

## Reasoning

The main reason for this rule is readability.  When a language is specified,
the rendering engine has the option to apply syntax highlighting to the code
block, if the language is recognized.

## Examples

### Failure Scenarios

This rule triggers when no characters or only whitespace characters follow
the fenced code block start character sequence.  In this example, that
sequence is `` ``` ``:

````Markdown
```
def func(arg1, arg2):
    return arg1 + arg2
```
````

### Correct Scenarios

This rule does not trigger if any non-whitespace text is present after the fenced
code block start character sequence.  In this example, that sequence is `` ``` ``:

````Markdown
```python
def func(arg1, arg2):
    return arg1 + arg2
```
````

## Configuration

| Prefixes |
| --- |
| `plugins.md040.` |
| `plugins.fenced-code-language.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD040](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md040---fenced-code-blocks-should-have-a-language-specified).
