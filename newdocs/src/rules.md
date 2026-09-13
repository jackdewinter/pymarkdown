# Rules

## Rule - MD001

[Full Documentation](./plugins/rule_md001.md)

| Property | Value |
| --- | --- |
| Aliases | `md001`, `heading-increment`, `header-increment` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Increment headings by one level at a time.

## Rule - MD002

[Full Documentation](./plugins/rule_md002.md)

| Property | Value |
| --- | --- |
| Aliases | `md002`, `first-heading-h1`, `first-header-h1` |
| Autofix Available | No |
| Enabled By Default | No |

<!-- pyml disable-next-line no-duplicate-heading-->
### Deprecation

This rule is disabled by default, as it has been deprecated in favor of
[Rule MD041](./plugins/rule_md041.md).

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Use a top-level heading for the first heading in the document.

## Rule - MD003

[Full Documentation](./plugins/rule_md003.md)

| Property | Value |
| --- | --- |
| Aliases | `md003`, `heading-style`, `header-style` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Use consistent heading styles throughout the document.

## Rule - MD004

[Full Documentation](./plugins/rule_md004.md)

| Property | Value |
| --- | --- |
| Aliases | `md004`, `ul-style` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Use a consistent style for unordered list characters.

## Rule - MD005

[Full Documentation](./plugins/rule_md005.md)

| Property | Value |
| --- | --- |
| Aliases | `md005`, `list-indent` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

List items at the same nesting level must share consistent indentation.

## Rule - MD006

[Full Documentation](./plugins/rule_md006.md)

| Property | Value |
| --- | --- |
| Aliases | `md006`, `ul-start-left` |
| Autofix Available | Yes |
| Enabled By Default | No |

<!-- pyml disable-next-line no-duplicate-heading-->
### Deprecation

This rule has been deprecated in favor of [Rule MD007](./plugins/rule_md007.md).

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure unordered lists start at the beginning of the line.

## Rule - MD007

[Full Documentation](./plugins/rule_md007.md)

| Property | Value |
| --- | --- |
| Aliases | `md007`, `ul-indent` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure unordered list items use consistent indentation.

## Rule - MD009

[Full Documentation](./plugins/rule_md009.md)

| Property | Value |
| --- | --- |
| Aliases | `md009`, `no-trailing-spaces` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Prohibit trailing whitespace on every line, except where it is an intentional hard
line break.

## Rule - MD010

[Full Documentation](./plugins/rule_md010.md)

| Property | Value |
| --- | --- |
| Aliases | `md010`, `no-hard-tabs` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Disallow hard tabs in Markdown files so that indentation renders consistently across
editors, viewers, and terminals.

## Rule - MD011

[Full Documentation](./plugins/rule_md011.md)

| Property | Value |
| --- | --- |
| Aliases | `md011`, `no-reversed-links` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Inline links should use correct syntax with link text in brackets preceding the
URL in parentheses.

## Rule - MD012

[Full Documentation](./plugins/rule_md012.md)

| Property | Value |
| --- | --- |
| Aliases | `md012`, `no-multiple-blanks` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure that at most one blank line separates consecutive paragraphs or block-level
elements.

## Rule - MD013

[Full Documentation](./plugins/rule_md013.md)

| Property | Value |
| --- | --- |
| Aliases | `md013`, `line-length` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

This rule enforces a maximum line length to improve document readability.

## Rule - MD014

[Full Documentation](./plugins/rule_md014.md)

| Property | Value |
| --- | --- |
| Aliases | `md014`, `commands-show-output` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Require that at least one line in a code block is not prefixed with `$`, indicating
that command output is visible.

## Rule - MD018

[Full Documentation](./plugins/rule_md018.md)

| Property | Value |
| --- | --- |
| Aliases | `md018`, `no-missing-space-atx` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure at least one space exists between hash marks and text in Atx Open Headings.

## Rule - MD019

[Full Documentation](./plugins/rule_md019.md)

| Property | Value |
| --- | --- |
| Aliases | `md019`, `no-multiple-space-atx` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure only one space follows the hash character in open-style Atx headings (headings
without trailing closing hash characters).

## Rule - MD020

[Full Documentation](./plugins/rule_md020.md)

| Property | Value |
| --- | --- |
| Aliases | `md020`, `no-missing-space-closed-atx` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure at least one space exists between hash marks and text in Atx Closed Headings.

## Rule - MD021

[Full Documentation](./plugins/rule_md021.md)

| Property | Value |
| --- | --- |
| Aliases | `md021`, `no-multiple-space-closed-atx` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Multiple spaces are present inside the hash characters of a closed Atx heading.

## Rule - MD022

[Full Documentation](./plugins/rule_md022.md)

| Property | Value |
| --- | --- |
| Aliases | `md022`, `blanks-around-headings`, `blanks-around-headers` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Headings should be surrounded by blank lines.

## Rule - MD023

[Full Documentation](./plugins/rule_md023.md)

| Property | Value |
| --- | --- |
| Aliases | `md023`, `heading-start-left`, `header-start-left` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Start every heading at the beginning of the line.

## Rule - MD024

[Full Documentation](./plugins/rule_md024.md)

| Property | Value |
| --- | --- |
| Aliases | `md024`, `no-duplicate-heading`, `no-duplicate-header` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Each heading in the document must contain unique content.

## Rule - MD025

[Full Documentation](./plugins/rule_md025.md)

| Property | Value |
| --- | --- |
| Aliases | `md025`, `single-title`, `single-h1` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Use only one top-level heading per document.

## Rule - MD026

[Full Documentation](./plugins/rule_md026.md)

| Property | Value |
| --- | --- |
| Aliases | `md026`, `no-trailing-punctuation` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Do not use trailing punctuation in heading text.

## Rule - MD027

[Full Documentation](./plugins/rule_md027.md)

| Property | Value |
| --- | --- |
| Aliases | `md027`, `no-multiple-space-blockquote` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Use zero or one space after a block quote symbol so block quotes render with consistent
spacing.

## Rule - MD028

[Full Documentation](./plugins/rule_md028.md)

| Property | Value |
| --- | --- |
| Aliases | `md028`, `no-blanks-blockquote` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Do not include blank lines inside block quotes.

## Rule - MD029

[Full Documentation](./plugins/rule_md029.md)

| Property | Value |
| --- | --- |
| Aliases | `md029`, `ol-prefix` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ordered list item prefixes must be consistent.

## Rule - MD030

[Full Documentation](./plugins/rule_md030.md)

| Property | Value |
| --- | --- |
| Aliases | `md030`, `list-marker-space` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure consistent spacing after list markers.

## Rule - MD031

[Full Documentation](./plugins/rule_md031.md)

| Property | Value |
| --- | --- |
| Aliases | `md031`, `blanks-around-fences` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Fenced code blocks should be surrounded by blank lines.

## Rule - MD032

[Full Documentation](./plugins/rule_md032.md)

| Property | Value |
| --- | --- |
| Aliases | `md032`, `blanks-around-lists` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

List blocks must be surrounded by blank lines.

## Rule - MD033

[Full Documentation](./plugins/rule_md033.md)

| Property | Value |
| --- | --- |
| Aliases | `md033`, `no-inline-html` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Avoid using inline HTML elements in Markdown documents.

## Rule - MD034

[Full Documentation](./plugins/rule_md034.md)

| Property | Value |
| --- | --- |
| Aliases | `md034`, `no-bare-urls` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure that all URLs are formatted as autolinks or hyperlinks rather than appearing
as bare text.

## Rule - MD035

[Full Documentation](./plugins/rule_md035.md)

| Property | Value |
| --- | --- |
| Aliases | `md035`, `hr-style` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Enforce a consistent style for horizontal rules.

## Rule - MD036

[Full Documentation](./plugins/rule_md036.md)

| Property | Value |
| --- | --- |
| Aliases | `md036`, `no-emphasis-as-heading`, `no-emphasis-as-header` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Avoid using emphasis elements as headings.

## Rule - MD037

[Full Documentation](./plugins/rule_md037.md)

| Property | Value |
| --- | --- |
| Aliases | `md037`, `no-space-in-emphasis` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Do not use spaces inside emphasis markers.

## Rule - MD038

[Full Documentation](./plugins/rule_md038.md)

| Property | Value |
| --- | --- |
| Aliases | `md038`, `no-space-in-code` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Remove extra leading and trailing spaces from code span elements.

## Rule - MD039

[Full Documentation](./plugins/rule_md039.md)

| Property | Value |
| --- | --- |
| Aliases | `md039`, `no-space-in-links` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Do not include spaces inside link text labels.

## Rule - MD040

[Full Documentation](./plugins/rule_md040.md)

| Property | Value |
| --- | --- |
| Aliases | `md040`, `fenced-code-language` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Fenced code blocks should have a language specified.

## Rule - MD041

[Full Documentation](./plugins/rule_md041.md)

| Property | Value |
| --- | --- |
| Aliases | `md041`, `first-line-heading`, `first-line-h1` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure the first line of a Markdown file is a top-level heading.

## Rule - MD042

[Full Documentation](./plugins/rule_md042.md)

| Property | Value |
| --- | --- |
| Aliases | `md042`, `no-empty-links` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

No empty links.

## Rule - MD043

[Full Documentation](./plugins/rule_md043.md)

| Property | Value |
| --- | --- |
| Aliases | `md043`, `required-headings`, `required-headers` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Require the document to contain a specific, configuration-defined heading structure.

## Rule - MD044

[Full Documentation](./plugins/rule_md044.md)

| Property | Value |
| --- | --- |
| Aliases | `md044`, `proper-names` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure proper names use the correct capitalization.

## Rule - MD045

[Full Documentation](./plugins/rule_md045.md)

| Property | Value |
| --- | --- |
| Aliases | `md045`, `no-alt-text` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Provide alternate text for every image.

## Rule - MD046

[Full Documentation](./plugins/rule_md046.md)

| Property | Value |
| --- | --- |
| Aliases | `md046`, `code-block-style` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure consistent code block styles within a document.

## Rule - MD047

[Full Documentation](./plugins/rule_md047.md)

| Property | Value |
| --- | --- |
| Aliases | `md047`, `single-trailing-newline` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

End each file with a single newline character.

## Rule - MD048

[Full Documentation](./plugins/rule_md048.md)

| Property | Value |
| --- | --- |
| Aliases | `md048`, `code-fence-style` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Enforce a consistent code fence style throughout the document.

## Rule - MD049

[Full Documentation](./plugins/rule_md049.md)

| Property | Value |
| --- | --- |
| Aliases | `md049`, `emphasis-style` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure consistent emphasis style across the document.

## Rule - MD050

[Full Documentation](./plugins/rule_md050.md)

| Property | Value |
| --- | --- |
| Aliases | `md050`, `strong-style` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure consistent strong emphasis style throughout the document.

## Rule - MD051

[Full Documentation](./plugins/rule_md051.md)

| Property | Value |
| --- | --- |
| Aliases | `md051`, `link-fragments` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Local link fragments should be valid.

## Rule - MD053

[Full Documentation](./plugins/rule_md053.md)

| Property | Value |
| --- | --- |
| Aliases | `md053`, `link-image-reference-definitions` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Link and image reference definitions should be needed by at least one link or image
in the document, and each label should be defined only once.

## Rule - MD054

[Full Documentation](./plugins/rule_md054.md)

| Property | Value |
| --- | --- |
| Aliases | `md054`, `link-image-style` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Keep the style of links and images consistent within a Markdown document.

## Rule - MD059

[Full Documentation](./plugins/rule_md059.md)

| Property | Value |
| --- | --- |
| Aliases | `md059`, `descriptive-link-text` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Link text must be descriptive.

## Rule - MD060

[Full Documentation](./plugins/rule_md060.md)

| Property | Value |
| --- | --- |
| Aliases | `md060`, `table-column-style` |
| Autofix Available | No |
| Enabled By Default | Yes |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure table columns adhere to a consistent formatting style.

## Rule - PML100

[Full Documentation](./plugins/rule_pml100.md)

| Property | Value |
| --- | --- |
| Aliases | `pml100`, `disallowed-html` |
| Autofix Available | No |
| Enabled By Default | No |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Ensure that disallowed HTML elements (such as `script`, `iframe`, and `style`) do
not appear in the Markdown document.

## Rule - PML101

[Full Documentation](./plugins/rule_pml101.md)

| Property | Value |
| --- | --- |
| Aliases | `pml101`, `list-anchored-indent` |
| Autofix Available | No |
| Enabled By Default | No |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Enforce that base lists are anchored at an allowed column and that every sub-list
is indented by a multiple of the configured indent width.

## Rule - PML102

[Full Documentation](./plugins/rule_pml102.md)

| Property | Value |
| --- | --- |
| Aliases | `pml102`, `disallow-lazy-list-indentation` |
| Autofix Available | Pending |
| Enabled By Default | No |

<!-- pyml disable-next-line no-duplicate-heading-->
### Summary

Disallow "lazy" paragraph continuations within lists.
