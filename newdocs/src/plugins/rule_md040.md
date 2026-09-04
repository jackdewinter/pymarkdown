# Rule - MD040

| Property | Value |
| --- | --- |
| Aliases | `md040`, `fenced-code-language` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Fenced code blocks should have a language specified.

## Reasoning

### Readability

Specifying a language identifier enables syntax highlighting, which significantly improves code readability and maintainability for human readers.

## Examples

### Failure Scenarios

This rule triggers when no characters or only whitespace characters follow the fenced code block start character sequence.
The trailing `|` character in the second example is used to show a single trailing whitespace characters for display purposes only, and would not be presented to the parser.

````Markdown
```
def func(arg1, arg2):
    return arg1 + arg2
```

``` |
def func(arg1, arg2):
    return arg1 + arg2
```
````

> **Explanation**: The fenced code block above begins with `` ``` `` followed immediately by a newline, with no language identifier specified. This violates the rule because the absence of a language string prevents syntax highlighting and reduces readability for the reader.

### Correct Scenarios

This rule does not trigger when a language identifier is present after the fenced code block start character sequence.

````Markdown
```python
def func(arg1, arg2):
    return arg1 + arg2
```
````

> **Explanation**: The fenced code block above specifies `python` as the language identifier immediately after the opening fence. This satisfies the rule because the presence of a non-whitespace language string enables syntax highlighting and improves readability.

This scenario demonstrates that any non-whitespace string after the opening fence satisfies the rule, even if it is not a recognized programming language.

````Markdown
```custom-identifier
def func(arg1, arg2):
    return arg1 + arg2
```
````

> **Explanation**: The fenced code block above specifies `custom-identifier` as the language identifier. This satisfies the rule because the presence of any non-whitespace character sequence immediately following the opening fence is sufficient, regardless of whether the rendering engine recognizes or supports syntax highlighting for that particular identifier.

## Fix Description

The reason for not being able to auto-fix this rule is context. While a guess can
be made as to the type of content within a fenced code block, it typically requires
the author's insight to properly classify the content's language.

## Configuration

| Prefixes |
| --- |
| `plugins.md040.` |
| `plugins.fenced-code-language.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD040](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md040---fenced-code-blocks-should-have-a-language-specified).
