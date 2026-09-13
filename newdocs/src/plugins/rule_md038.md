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

Different parsers interpret leading and trailing spaces in code spans inconsistently.
This rule triggers on unbalanced spaces to ensure the author's intent is preserved
across renderers.

## Examples

### Failure Scenarios

This rule triggers when there are unbalanced spaces at the start:

```Markdown
this is an ` invalid` code span
```

> **Explanation**: This example violates the rule because there is a leading space
> inside the code span that is not matched by a trailing space. The rule requires
> that leading and trailing spaces be balanced or absent.

Unlike the first example, this case has an unbalanced trailing space instead of
a leading space:

```Markdown
this is an `invalid ` code span
```

> **Explanation**: This example violates the rule because there is a trailing space
> inside the code span that is not matched by a leading space. The rule requires
> that leading and trailing spaces be balanced or absent.

Unlike the previous examples, this case uses multiple balanced spaces at the start
and end of the code span:

```Markdown
this is an `  invalid  ` code span
```

> **Explanation**: This example violates the rule because the code span has two
> leading spaces and two trailing spaces. The rule permits at most a single balanced
> pair of spaces; any additional leading or trailing space triggers the failure.

Unlike the previous examples, this case has more leading spaces than trailing spaces,
making the pair unbalanced:

```Markdown
this is an `  invalid ` code span
```

> **Explanation**: This example violates the rule because the code span has two
> leading spaces but only one trailing space. The rule requires that any leading
> and trailing spaces form exactly one balanced pair; an uneven count on either
> side is not permitted, even though both sides contain a space.

### Correct Scenarios

This rule does not trigger when there are no spaces at the start and end of the
code span text:

```Markdown
this is a `valid` code span
```

> **Explanation**: This example satisfies the rule because there are no leading
> or trailing spaces within the code span. The content is clean and unambiguous
> for all parsers.

Unlike the first example, this case includes a single balanced space at both the
start and end of the code span:

```Markdown
this is a ` valid ` code span
```

> **Explanation**: This example satisfies the rule because there is exactly one
> leading and one trailing space. Standard Markdown parsers automatically strip
> this single pair of spaces, ensuring consistent rendering.

Unlike the previous examples, this case uses a doubled-backtick code span whose
inner text contains a literal backtick, where the surrounding spaces are required
to keep the span from terminating early:

```Markdown
this is a `` `valid` `` code span
```

> **Explanation**: This example satisfies the rule because the code span uses a
> doubled-backtick fence and contains a literal backtick in its inner text. The
> spaces adjacent to the inner backtick are required to disambiguate the span's
> content, and the rule preserves them rather than treating them as removable "extra"
> spaces.

## Fix Description

A single leading and/or trailing space is removed from the code span text when it
is balanced (i.e., present at both ends). The exception is when the character adjacent
to that space is a backtick (`` ` ``), because in that case the space is required
to keep the code span from terminating early (e.g., `` `code` `` ). In that case,
the autofix preserves the space.

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
