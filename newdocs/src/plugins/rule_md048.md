# Rule - MD048

| Property | Value |
| --- | --- |
| Aliases | `md048`, `code-fence-style` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Code fence style should be consistent throughout the document.

## Reasoning

### Readability

Consistent fence characters improve readability and enable organizations to enforce uniform code block formatting standards across documents.

## Examples

### Failure Scenarios

This rule triggers when there is inconsistent use of fence characters for
Fenced Code Blocks:

````Markdown
```Python
a=b
```

~~~Python
a=b
~~~
````

> **Explanation**: The first code block uses backticks (`` ``` ``) as fence characters, while the second uses tildes (`` ~~~ ``). This violates the rule because the fence style is not consistent throughout the document with the default configuration of `consistent`.

Unlike the previous example, this scenario demonstrates a failure when the `style` configuration is set to `backtick`, but tildes are used.

````Markdown
~~~Python
a=b
~~~
````

> **Explanation**: The code block uses tildes (`~~~`) as fence characters. This violates the rule because the configuration specifies that only backticks (`` ``` ``) should be used (`style: backtick`).

Unlike the previous example, this scenario demonstrates a failure when the `style` configuration is set to `tilde`, but backticks are used.

````Markdown
```Python
a=b
```
````

> **Explanation**: The code block uses backticks (`` ``` ``) as fence characters. This violates the rule because the configuration specifies that only tildes (`~~~`) should be used (`style: tilde`).

### Correct Scenarios

This rule does not trigger when the fence character for Fenced Code Blocks is
consistently specified within the document:

````Markdown
```Python
a=b
```

```Python
b=c
```
````

> **Explanation**: Both code blocks use backticks (`` ``` ``) as fence characters. This satisfies the rule because the fence style is consistent throughout the document.

Unlike the previous example, this case demonstrates consistent use of tildes (`~`) as fence characters.

````Markdown
~~~Python
a=b
~~~

~~~Python
b=c
~~~
````

> **Explanation**: Both code blocks use tildes (`~~~`) as fence characters. This satisfies the rule because the fence style is consistent throughout the document. Under the `consistent` style, this is valid because tildes are used exclusively. Under the `tilde` style, this is also valid.

## Fix Description

Fenced code blocks will be fixed to use a single fence character style, as determined by the `style` configuration. If `style` is `consistent`, all fences will match the first fence encountered in the document.

## Configuration

| Prefixes |
| --- |
| `plugins.md048.` |
| `plugins.code-fence-style.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `style` | `string` | `consistent` | Style of fenced code block fence characters expected in the document. |

### Valid Styles

| Style | Description |
| --- | --- |
| `consistent` | The first Fenced Code Block specifies the style for the rest of the document. |
| `backtick` | Only backticks are to be used for Fenced Code Block elements. |
| `tilde` | Only tildes are to be used for Fenced Code Block elements. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD048](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md048---code-fence-style).
