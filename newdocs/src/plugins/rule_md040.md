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

Specifying a language identifier enables syntax highlighting, which significantly
improves code readability and maintainability for human readers.

## Examples

### Failure Scenarios

This rule triggers when no characters follow the fenced code block start character
sequence.

````Markdown
```
def func(arg1, arg2):
    return arg1 + arg2
```
````

> **Explanation**: The fenced code block above begins with the three-backtick
> start sequence followed immediately by a newline, with no language
> identifier specified. This violates the rule because the absence of a
> language string prevents syntax highlighting and reduces readability for
> the reader.

Unlike the previous example, this case has only a whitespace character after the
opening fence (the trailing `|` below is a display marker for that single space;
the parser sees only the space).

````Markdown
``` |
def func(arg1, arg2):
    return arg1 + arg2
```
````

> **Explanation**: Although a character appears after the opening fence here, it
> is only a whitespace character, so no meaningful language identifier is present.
> This still violates the rule because a whitespace-only string does not enable
> syntax highlighting and does not satisfy the requirement for a non-whitespace
> language identifier.

### Correct Scenarios

This rule does not trigger when a language identifier is present after the fenced
code block start character sequence.

````Markdown
```python
def func(arg1, arg2):
    return arg1 + arg2
```
````

> **Explanation**: The fenced code block above specifies `python` as the language
> identifier immediately after the opening fence. This satisfies the rule because
> the presence of a non-whitespace language string enables syntax highlighting and
> improves readability.

Unlike the previous example, which uses a well-known language (`python`),
this case uses a non-standard identifier to demonstrate that the rule only
requires a non-whitespace string after the opening fence.

````Markdown
```custom-identifier
def func(arg1, arg2):
    return arg1 + arg2
```
````

> **Explanation**: The fenced code block above specifies
> `custom-identifier` as the language identifier. This satisfies the rule
> because the presence of any non-whitespace character sequence immediately
> following the opening fence is sufficient, regardless of whether a
> renderer supports highlighting for that identifier.

## Fix Description

Auto-fix is not possible because identifying the language of an unknown
code block requires the author's intent. A heuristic guess (e.g., by file
extension or content sniffing) would be unreliable and could misclassify
the content.

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
