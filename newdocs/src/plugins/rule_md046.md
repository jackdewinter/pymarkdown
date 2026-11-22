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

Mixing fenced and indented code blocks in the same document creates visual noise
and makes it harder for readers to tell code apart from prose.

## Examples

### Failure Scenarios

This rule triggers when there is inconsistent use of code block elements within
the same document.

````Markdown
```Python
a=b
```

    indented
````

> **Explanation**: This document contains both a fenced code block (using triple
> backticks) and an indented code block (using four leading spaces). With the default
> `consistent` style, the first code block sets the expected style (`fenced` in
> this case). The second code block uses `indented` style, which violates the consistency
> requirement.

Unlike the first scenario, this case also uses the default `consistent` style,
but the **first** code block is indented and the **second** is fenced. Because
the first block establishes the expected style, the fenced block is the one
that violates the rule — the reverse of the first scenario, where the indented
block was the violation.

````Markdown
    indented, no language tag

```Python
a=b
```
````

> **Explanation**: With the default `consistent` style, the **first** code
> block in the document sets the expected style for the rest of the document.
> Here, the first block is an **indented** code block (four leading spaces,
> no language tag), so `indented` becomes the expected style. The second block
> is a **fenced** code block (triple backticks with a `Python` language tag),
> which violates the `indented` requirement established by the first block.
> This is the mirror image of the first scenario: the same two block types
> appear, but in reversed order, and the violation now falls on the fenced
> block rather than the indented one. The takeaway is that under `consistent`,
> **order matters** — the first block always governs.

Unlike the previous example, this case explicitly sets `style` to `fenced`,
so the four-space indented code block shown below violates the enforced `fenced`
requirement even though the document contains only a single code block.

```Markdown
    indented
```

> **Explanation**: When the `style` configuration is explicitly set to
> `fenced`, **every** code block in the document must be a fenced code
> block. The four-space-indented line above is an **indented code block**, so
> it violates the enforced `fenced` style requirement.

Unlike the previous example, this case explicitly sets `style` to `indented` and
the document contains a fenced code block.

````Markdown
```Python
a=b
```
````

> **Explanation**: When the `style` configuration is explicitly set to
> `indented`, **every** code block in the document must be an indented code
> block. The triple-backtick block above is a `fenced` code block, so it
> violates the enforced `indented` style requirement. Like the first scenario,
> this
> failure occurs with a single code block because the `indented`
> requirement is absolute — it does not depend on what the first block in
> the document happens to be.

### Correct Scenarios

This rule does not trigger when all code blocks in the document use the same
style (both blocks are indented in this case).

```Markdown
    indented, without any ability to add a language tag

    another indented
```

> **Explanation**: Both code blocks in this document use the indented style
> (four leading spaces). Indented blocks cannot carry a language tag, so the
> example is intentionally tag-free. With the default `consistent` style, the
> first code block establishes `indented` as the expected style, and the
> second code block conforms to it. No inconsistency exists.

Unlike the previous example, this case uses fenced code blocks throughout the
document, so the default `consistent` style is satisfied by the `fenced` form
chosen for the first block.

````Markdown
```Python
a = b
```

```Python
c = d
```
````

> **Explanation**: Both code blocks in this document use the fenced style (triple-backtick
> delimiters).
> With the default `consistent` style, the first code block establishes `fenced`
> as the expected
> style, and the second code block conforms to it. No inconsistency exists, so the
> rule does not
> trigger. Unlike the previous (indented) scenario, the expected style here is `fenced`
> rather
> than `indented`, but the consistency logic is identical: the first block's style
> governs the
> rest of the document.

Unlike the previous example, this case explicitly sets `style` to `fenced`,
so a document containing only fenced code blocks satisfies the enforced requirement.

````Markdown
```Python
a = b
```

```JavaScript
console.log("hi")
```
````

> **Explanation**: With `style` explicitly set to `fenced`, every code block in
> the document must be fenced. Both blocks above are fenced, so the rule does
> not trigger.

Unlike the previous example, this case explicitly sets `style` to `indented`,
so a document containing only indented code blocks satisfies the enforced requirement.

```Markdown
    indented, block one

    indented, block two
```

> **Explanation**: With `style` explicitly set to `indented`, every code block in
> the document must be an indented code block. Both blocks above use four
> leading spaces, so the rule does not trigger.

## Fix Description

Setting the `style` configuration item value to either `indented`
or `fenced` will cause all code blocks to be transformed into the specified
value. If set to `consistent`, the first code block in the document will
set the style for the rest of the document.

Note that the translations between fenced and indented code blocks
introduce the following considerations:

- For both translations, any whitespace before the code block is removed during
  the transition.
- When translating to a fenced code block, there is no guaranteed way to properly
  set the language for the fenced code block. As such, it is left blank and will
  cause [Rule MD040](./rule_md040.md) to be triggered when next scanned.
- When translating to an indented code block, there are parsing issues with an
  indented code block that immediately follows a paragraph. As indented code blocks
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

### Valid Styles

| Style Name | Description |
| --- | --- |
| `consistent` | The first code block in the document specifies the style for the rest of the document. |
| `fenced` | Only fenced code blocks are to be used. |
| `indented` | Only indented code blocks are to be used. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD046](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md046---code-block-style).
