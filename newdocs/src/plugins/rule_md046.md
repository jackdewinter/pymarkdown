# Rule - MD046

| Property | Value |
| --- | --- |
| Aliases | `md046`, `code-block-style` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Ensure consistent code block styles within a document.

## Reasoning

### Readability

Consistent code block formatting within a document enhances readability by reducing visual noise and helping readers quickly distinguish between code and prose.

## Examples

### Failure Scenarios

This rule triggers when there is inconsistent use of code block elements within the same document.

````Markdown
```Python
a=b
```

    indented
````

> **Explanation**: This document contains both a fenced code block (using triple backticks) and an indented code block (using four leading spaces). With the default `consistent` style, the first code block sets the expected style (`fenced` in this case). The second code block uses `indented` style, which violates the consistency requirement.

Unlike the previous example, this case explicitly configures the style to `fenced` rather than relying on the default `consistent` setting.

```Markdown
    indented
```

> **Explanation**: When the `style` configuration is explicitly set to `fenced`, any indented code block in the document violates the rule. This example uses an indented code block, which conflicts with the enforced `fenced` style requirement.

### Correct Scenarios

This rule does not trigger when all code blocks use the same style throughout the document.

````Markdown
```Python
a=b
```

```Python
b=c
```
````

> **Explanation**: Both code blocks in this document use the fenced style (triple backticks). With the default `consistent` style, the first code block establishes `fenced` as the expected style, and the second code block conforms to it. No inconsistency exists.

Unlike the previous example, this case uses only indented code blocks.

````Markdown
    indented, without any ability to add a language tag

    another indented
````

> **Explanation**: Both code blocks in this document use the indented style (four leading spaces). With the default `consistent` style, the first code block establishes `indented` as the expected style, and the second code block conforms to it. No inconsistency exists.

## Fix Description

Setting the `style` configuration item value to either `indented`
or `fenced` will cause all code blocks to be transformed into the specified
value.  If set to `consistent`, the first code block in the document will
set the style for the rest of the document.

Note that the translation from fenced-to-indented code block and the
translation from indented-to-fenced code block have their issues.

- For both translations, any whitespace before the code block is removed during
  the transition.
- When translating to a fenced code block, there is no guaranteed way to properly
  set the language for the fenced code block.  As such, it is left blank and will
  cause [Rule Md040](./rule_md040.md) to be triggered when next scanned.
- When translating to an indented code block, there are parsing issues with an
  indented code block that immediately follows a paragraph.  As indented code blocks
  cannot interrupt a paragraph block, an extra blank line is inserted between the
  paragraph and the new indented code block to allow the indented code block to
  be properly recognized.

## Configuration

| Prefixes |
| --- |
| `plugins.md046.` |
| `plugins.code-block-style.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `style` | `string` | `consistent` | Style of code blocks expected in the document. |

Valid styles:

| Style | Description |
| --- | --- |
| `consistent` | The first code block in the document specifies the style for the rest of the document. |
| `fenced` | Only fenced code blocks are to be used. |
| `indented` | Only indented code blocks are to be used. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD046](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md046---code-block-style).
