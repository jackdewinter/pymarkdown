# Rule - MD040

| Aliases |
| --- |
| `md040` |
| `fenced-code-language` |

| Autofix Available |
| --- |
| No |

## Summary

Fenced code blocks should have a language specified.

## Reasoning

### Readability

When a language is specified, the rendering engine has the choice to
apply syntax highlighting to the code block if the language is recognized.

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

## Fix Description

The reason for not being able to auto-fix this rule is context.  While a guess can
be made as to the type of content within a fenced code block, it typically requires
the author's context to properly classify the content.
