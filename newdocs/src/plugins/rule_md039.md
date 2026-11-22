# Rule - MD039

| Property | Value |
| --- | --- |
| Aliases | `md039`, `no-space-in-links` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Do not include spaces inside link text labels.

## Reasoning

### Readability

Link labels with leading or trailing spaces (e.g., `[ label ]`) are visually indistinct
from those without (e.g., `[label]`). Enforcing consistent spacing prevents accidental
mismatches in link reference resolution and improves source readability.

## Examples

### Failure Scenarios

This rule triggers when the link label for any link or image includes leading whitespace
or trailing whitespace.

```Markdown
this is not
[ a proper](https://www.example.com)
link
```

> **Explanation**: The link label `a proper` has a leading space. The rule requires
> that link labels do not have a space at the very beginning or the very end of
> the label, while spaces *between* words remain allowed.

Unlike the previous example which had leading whitespace, this case demonstrates
trailing whitespace inside the link label.

```Markdown
this is not
[label ](https://www.example.com)
link
```

> **Explanation**: The link label `label` has a trailing space. The rule requires
> that link labels do not have a space at the very beginning or the very end of
> the label, while spaces *between* words remain allowed.

Unlike the previous examples which had only leading or only trailing whitespace,
this case demonstrates both leading and trailing whitespace inside the link label.

```Markdown
this is not
[ label ](https://www.example.com)
link
```

> **Explanation**: The link label `label` has both a leading space and a trailing
> space. The rule requires that link labels do not have a space at the very beginning
> or the very end of the label, while spaces *between* words remain allowed.

Unlike the previous examples which used standard links, this case demonstrates leading
whitespace in an image's alt-text label.

```Markdown
![ alt text](https://www.example.com/image.png)
```

> **Explanation**: The image alt-text label `alt text` has a leading space. The
> rule applies to both links and images, and neither may have a space at the very
> beginning or the very end of the label, while spaces *between* words remain allowed.

Unlike the previous examples which used inline links or images, this case demonstrates
leading and trailing whitespace in a link reference definition label.

```Markdown
[ label ]: https://www.example.com
```

> **Explanation**: The link reference definition label `label` has both a leading
> space and a trailing space. The rule applies to link reference definitions as
> well, and neither may have a space at the very beginning or the very end of the
> label, while spaces *between* words remain allowed.

### Correct Scenarios

This rule does not trigger when the link label for any link or image does not start
with leading whitespace or end with trailing whitespace.

```Markdown
this is a
[proper](https://www.example.com)
link
```

> **Explanation**: The link label `proper` does not contain any leading or trailing
> whitespace. It adheres to the rule's requirement for clean link labels.

Unlike the previous example which used a single-word label, this case demonstrates
a multi-word label with an internal space, which is permitted as long as there are
no leading or trailing spaces.

```Markdown
this is
[a proper](https://www.example.com)
link
```

> **Explanation**: The link label `a proper` does not contain any leading or trailing
> whitespace. It adheres to the rule's requirement for clean link labels. Internal
> spaces within the label are allowed.

Unlike the previous example which used a standard link, this case demonstrates an
image with a clean alt-text label without leading or trailing whitespace.

```Markdown
![alt text](https://www.example.com/image.png)
```

> **Explanation**: The image alt-text label `alt text` does not contain any leading
> or trailing whitespace. It adheres to the rule's requirement for clean labels
> in both links and images.

Unlike the previous examples which used inline links or images, this case demonstrates
a link reference definition label without leading or trailing whitespace.

```Markdown
[label]: https://www.example.com
```

> **Explanation**: The link reference definition label `label` does not contain
> any leading or trailing whitespace. It adheres to the rule's requirement for clean
> labels in link reference definitions.

## Fix Description

The fix for this rule strips leading and trailing spaces from the link label.

## Configuration

| Prefixes |
| --- |
| `plugins.md039.` |
| `plugins.no-space-in-links.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD039](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md039---spaces-inside-link-text).

### Differences From MarkdownLint Rule

The difference between this rule and the original rule is that the original
rule only fired on links, not image links or link definitions. As the only difference
between a link:

```Markdown
[a link](https://www.example.com)
```

and an image:

```Markdown
![an image](https://www.example.com)
```

is the `!` character, it made sense for the implementation to respect both elements.
