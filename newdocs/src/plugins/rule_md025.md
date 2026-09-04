# Rule - MD025

| Property | Value |
| --- | --- |
| Aliases | `md025`, `single-title`, `single-h1` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Use only one top-level heading per document.

## Reasoning

### Correctness

Most Markdown parsers treat the first Heading 1 element as the document title. Allowing multiple Heading 1 elements creates ambiguity regarding which heading serves as the official title, harming document structure and accessibility.

## Examples

### Failure Scenarios

This rule triggers when multiple top-level headings exist in the same document, violating the principle that a document should have only one title.

```Markdown
# Top Level

# Another Top Level
```

> **Explanation**: This example fails because it contains two Heading 1 elements (`# Top Level` and `# Another Top Level`). The rule requires only one top-level heading per document to serve as the document title.

Unlike the first example, this case uses a mix of Atx and Setext heading styles for the top-level headings.

```Markdown
# Top Level

Another Top Level
===
```

> **Explanation**: This example fails because the rule treats both Atx headings (`# Top Level`) and Setext headings (`Another Top Level` with `===`) as top-level headings. Having both violates the single-title requirement.

Unlike the previous examples, this case combines [front-matter parsing](../extensions/front-matter.md) with a top-level heading, which also triggers the rule when Front-Matter doesn't provide a title.

```Markdown
---
title: this is a title
---

# Top Level
```

> **Explanation**: This example fails because even though Front-Matter is present, it contains a top-level heading (`# Top Level`) in addition to the title in Front-Matter. The rule counts this as multiple titles.

### Correct Scenarios

This rule does not trigger when the document contains only a single top-level heading, satisfying the single-title requirement.

```Markdown
# Top Level

## Used To Be Another Top Level
```

> **Explanation**: This example passes because there is only one Heading 1 element (`# Top Level`). The second heading is level 2 (`##`), which is acceptable.

Unlike the previous example, this case uses [front-matter parsing](../extensions/front-matter.md) with a configured `front_matter_title` field of `subject`, allowing all document headings to be level 2 or below.

```Markdown
---
subject: This is a title
---

## Used To Be Another Top Level
```

> **Explanation**: This example passes because the `front_matter_title` configuration is set to `subject`, and the Front-Matter contains `subject: This is a title`. Since the title is provided in Front-Matter, all headings in the document are level 2 or below, satisfying the rule.

## Fix Description

This rule cannot be auto-fixed due to context dependency and cascading effects.
Although some parsers default to honoring only the first top-level heading, this behavior is not universal enough to justify an automatic fix.
On the context front, while there is precedent that only the first top-level heading of a document should be honored, we do not currently consider it to be a solid enough precedent to base a fix on.
Additionally, changing multiple top-level headings to level 2 could require recursive adjustments to nested headings, creating unpredictable cascading changes.
If those offending headings are changed to
a level 2 heading, should any other headings within those headings be similarly
increased?
Due to these ambiguities, no automatic fix is provided.

## Configuration

| Prefixes |
| --- |
| `plugins.md025.` |
| `plugins.single-title.` |
| `plugins.single-h1.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |
| `front_matter_title` | `string` | `title` | Name of the Front-Matter field that has the title associated with the document.** |
| `level` | `integer` | `1` | Heading level to be considered as the top-level. |

** Any leading or trailing space characters are removed from the `front_matter_title`
during processing.  This value is expected not to have the `:` at the end. Therefore,
a header value of `subject:` would be entered as `subject`.

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD025](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md025---multiple-top-level-headings-in-the-same-document).

### Differences From MarkdownLint Rule

Unlike the original MarkdownLint rule, which used a regular expression to identify title fields in Front-Matter, this rule simply looks for the value of the Front-Matter key `title` by default.
