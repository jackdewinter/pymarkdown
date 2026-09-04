# Rule - MD010

| Property | Value |
| --- | --- |
| Aliases | `md010`, `no-hard-tabs` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Disallow hard tabs in Markdown files.

## Reasoning

### Consistency

Different editors and parsers interpret tab characters inconsistently, leading to unpredictable rendering. This rule requires spaces instead of tabs to ensure uniform appearance.

## Examples

### Failure Scenarios

This rule triggers when a line contains a hard tab character.

```Markdown
→Indented Code Block
```

> **Explanation**: This line begins with a hard tab character (shown as `→`) instead of spaces. MD010 requires all indentation to use spaces for consistent rendering. The `→` symbol visually represents the tab character (`\t`, Unicode U+0009).

Unlike the previous example, this case includes hard tab characters both at the beginning of the line and within the content.

```Markdown
→Indented→Code→Block
```

> **Explanation**: This line fails MD010 because it contains hard tab characters (shown as `→`) for both leading indentation and within the text. The rule requires all tabs to be replaced with spaces to ensure consistent rendering across different parsers and editors.

Unlike the previous examples, this case contains a hard tab character only within the inline text, with no leading indentation.

```Markdown
Some text→with a tab
```

> **Explanation**: This line fails MD010 because it contains a hard tab character (shown as `→`) within the inline content. Even though there is no leading indentation tab, any tab character anywhere in the document triggers this rule. The rule requires all tabs to be replaced with spaces to ensure consistent rendering.

### Correct Scenarios

This rule does not trigger when indentation is performed using space characters.

```Markdown
    Indented Code Block
```

> **Explanation**: This line passes MD010 because it uses four space characters for indentation rather than a hard tab. Since no tab characters are present, the rule is satisfied.

## Fix Description

Except for within code blocks, any tab characters will be replaced with the appropriate
count of space characters. Note that tab characters within Markdown documents are
treated as [Tab Stops](https://github.github.com/gfm/#tabs) and not blindly replaced
with 4 space characters per tab character. For more clarity, please read the
specification at the above link.

## Configuration

| Prefixes |
| --- |
| `plugins.md010.` |
| `plugins.no-hard-tabs.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `code_blocks` | `boolean` | `True` | Whether hard tabs are searched for within code blocks. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD010](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md010---hard-tabs).
