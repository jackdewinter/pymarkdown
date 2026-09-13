# Rule - MD048

| Property | Value |
| --- | --- |
| Aliases | `md048`, `code-fence-style` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Enforce a consistent code fence style throughout the document.

## Reasoning

### Readability

Consistent fence characters improve readability and enable organizations to enforce
uniform code block formatting standards across documents.

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

```Python
c=3
```
````

> **Explanation**: The document uses backticks (`` ``` ``) for the first and third
> code blocks, but tildes (`~~~`) for the second code block. This violates the rule
> because the fence style is not consistent throughout the document under the default
> consistent style — the first Fenced Code Block (backticks) sets the expectation,
> and the second block (tildes) breaks it.

Unlike the previous example, this scenario demonstrates a failure when the `style`
configuration is set to `backtick`, but tildes are used.

````Markdown
~~~Python
a=b
~~~
````

> **Explanation**: The code block uses tildes (`~~~`) as fence characters. This
> violates the rule because the configuration specifies that only backticks
> (`` ``` ``) should be used when `style` is set to `backtick`.

Unlike the previous example, this scenario demonstrates a failure when the `style`
configuration is set to `tilde`, but backticks are used.

````Markdown
```Python
a=b
```
````

> **Explanation**: The code block uses backticks (`` ``` ``) as fence characters.
> This violates the rule because the configuration specifies that only tildes (`~~~`)
> should be used when `style` is set to `tilde`.

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

> **Explanation**: Both code blocks use backticks (`` ``` ``) as fence characters.
> This satisfies the rule because the fence style is consistent throughout the document.

Unlike the previous example, this case demonstrates consistent use of tildes (`~`)
as fence characters.

````Markdown
~~~Python
a=b
~~~

~~~Python
b=c
~~~
````

> **Explanation**: Both code blocks use tildes (`~~~`) as fence characters. This
> satisfies the rule because the fence style is consistent throughout the document,
> and tildes are also explicitly permitted under the `tilde` style.

## Fix Description

Fenced code blocks will be fixed to use a single fence character style, as determined
by the `style` configuration. If `style` is `consistent`, all fences will match
the first fence encountered in the document. If `style` is `backtick`, all fences
will be converted to backticks (`` ``` ``). If `style` is `tilde`, all fences will
be converted to tildes (`` ~~~ ``).

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

| Style Name | Description |
| --- | --- |
| `consistent` | The first Fenced Code Block specifies the style for the rest of the document. |
| `backtick` | Only backticks are to be used for Fenced Code Block elements. |
| `tilde` | Only tildes are to be used for Fenced Code Block elements. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD048](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md048---code-fence-style).
