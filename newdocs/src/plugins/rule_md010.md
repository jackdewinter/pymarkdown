# Rule - MD010

| Property | Value |
| --- | --- |
| Aliases | `md010`, `no-hard-tabs` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Disallow hard tabs in Markdown files so that indentation renders consistently across
editors, viewers, and terminals.

## Reasoning

### Consistency

Hard tab characters render at variable widths depending on the editor, viewer,
and terminal, so the same source displays with different indentation to
different readers and produces inconsistent diffs and line lengths. Requiring
spaces instead of tabs keeps both rendered output and source text deterministic
regardless of the tool used to open the file.

## Examples

### Failure Scenarios

This rule triggers when a line contains a hard tab character.

```Markdown
→Just some text
```

> **Explanation**: This line begins with a hard tab character (shown as `→`) instead
> of spaces. MD010 requires all indentation to use spaces for consistent rendering.
> The `→` symbol visually represents the tab character (`\t`, Unicode U+0009).

Unlike the previous example, this case includes hard tab characters both at the
beginning of the line and within the content.

```Markdown
→Indented→Code→Block
```

> **Explanation**: This line fails because it contains hard tab characters (shown
> as `→`) for both leading indentation and within the text.

Unlike the previous examples, this case contains a hard tab character only within
the inline text, with no leading indentation.

```Markdown
Some text→with a tab
```

> **Explanation**: This line fails because it contains a hard tab character (shown
> as `→`) within the inline content. Even though there is no leading indentation
> tab, any tab character anywhere in the document triggers this rule. The rule requires
> all tabs to be replaced with spaces to guarantee deterministic rendering.

Unlike the previous three examples, which placed hard tab characters directly in
the document flow, this case contains a hard tab character inside a fenced code
block. With the default setting `code_blocks` set to `True`, tabs inside fenced
code blocks are also flagged by this rule.

````Markdown
```Markdown
→Tab inside a code block is flagged
```
````

> **Explanation**: This example fails because the tab character (shown as `→`) appears
> inside a fenced code block, and the `code_blocks` default setting is `True`. With
> that setting, this rule treats tabs inside code blocks the same as tabs in prose
> and flags them for replacement with spaces.

### Correct Scenarios

This rule does not trigger when indentation is performed using space characters.

```Markdown
    Just some text
```

> **Explanation**: This line passes because it uses four space characters for indentation
> rather than a hard tab. Since no tab characters are present, the rule is satisfied.

Unlike the previous example, which only demonstrated space-based indentation, this
case uses spaces for inline word separation instead of a tab character.

```Markdown
Some text    with extra spaces
```

> **Explanation**: This line passes because the visual spacing between text fragments
> is achieved with space characters rather than a tab. The rule forbids tab characters
> anywhere in the document, but spaces (regardless of count) are always acceptable,
> so the document remains compliant.

Unlike the previous two examples, which used spaces directly in the document flow,
this case contains a hard tab character inside a fenced code block. It passes only
because the `code_blocks` setting is `False`, which exempts code blocks from this
rule.

````Markdown
```Markdown
→Tab inside a code block is allowed
```
````

> **Explanation**: This example passes because the tab character (shown as `→`)
> appears only inside a fenced code block, and the `code_blocks` setting is `False`.
> With that setting, tabs inside code blocks are excluded from MD010, so the rule
> does not trigger.

## Fix Description

Any tab characters, except those inside code blocks, will be replaced with the appropriate
number of spaces. Note that tab characters within Markdown documents are
treated as [Tab Stops](https://github.github.com/gfm/#tabs) and are not replaced
with 4 space characters per tab character.

## Configuration

| Prefixes |
| --- |
| `plugins.md010.` |
| `plugins.no-hard-tabs.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `code_blocks` | `boolean` | `True` | When `True`, hard tab characters inside fenced code blocks are also flagged and autofixed. Set to `False` to allow tabs inside code blocks. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD010](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md010---hard-tabs).

### Differences From MarkdownLint Rule

PyMarkdown's MD010 adds a `code_blocks` configuration option that controls
whether hard tabs inside fenced code blocks are also flagged and autofixed,
giving users a single knob to permit tabs in code while still enforcing spaces
in prose.
