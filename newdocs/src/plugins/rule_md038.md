# Rule - MD038

| Property | Value |
| --- | --- |
| Aliases | `md038`, `no-space-in-code` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Remove extra leading and trailing spaces from code span elements.

## Reasoning

### Correctness

Different parsers interpret leading and trailing spaces in code spans inconsistently. This rule triggers on unbalanced spaces to ensure the author's intent is preserved across renderers.

## Examples

### Failure Scenarios

This rule triggers when there are unbalanced spaces at the start:

```Markdown
this is an ` invalid` code span
```

> **Explanation**: This example violates the rule because there is a leading space inside the code span that is not matched by a trailing space. The rule requires that leading and trailing spaces be balanced or absent.

Unlike the first example, this case has an unbalanced trailing space instead of a leading space:

```Markdown
this is an `invalid ` code span
```

> **Explanation**: This example violates the rule because there is a trailing space inside the code span that is not matched by a leading space. The rule requires that leading and trailing spaces be balanced or absent.

Unlike the previous examples, this case uses multiple unbalanced spaces at the start and end of the code span:

```Markdown
this is an `  invalid  ` code span
```

> **Explanation**: While single balanced spaces are removed automatically, multiple spaces at the start and end are not fully stripped by standard parsers. This example has two spaces at both ends, which creates ambiguity in rendering. The rule triggers because the spaces are not a single balanced pair.

### Correct Scenarios

This rule does not trigger when there are no spaces at the start and end of the code span text:

```Markdown
this is a `valid` code span
```

> **Explanation**: This example satisfies the rule because there are no leading or trailing spaces within the code span. The content is clean and unambiguous for all parsers.

Unlike the first example, this case includes a single balanced space at both the start and end of the code span:

```Markdown
this is a ` valid ` code span
```

> **Explanation**: This example satisfies the rule because there is exactly one leading and one trailing space. Standard Markdown parsers automatically strip this single pair of spaces, ensuring consistent rendering.

Unlike the previous examples, this case uses a space before an inner backtick to prevent it from closing the code span prematurely:

```Markdown
this is a `` `valid `` code span
```

> **Explanation**: This example satisfies the rule because the space before the inner backtick is necessary to prevent it from closing the code span prematurely. The rule allows this specific case to ensure valid code spans containing backticks can be written.

## Fix Description

Generally, a single space character will be removed from both the start of the
code span text and from the end of the code span text. The one exception to that
rule is if the character following (or preceding) the space character is the
`` ` `` character.

## Configuration

| Prefixes |
| --- |
| `plugins.md038.` |
| `plugins.no-space-in-code.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD038](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md038---spaces-inside-code-span-elements).
