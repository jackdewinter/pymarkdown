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

Link labels with leading or trailing spaces (e.g., `[ label ]`) are visually indistinct from those without (e.g., `[label]`). Enforcing consistent spacing prevents accidental mismatches in link reference resolution and improves source readability.

## Examples

### Failure Scenarios

This rule triggers when the link label for any link or image includes leading whitespace or trailing whitespace.

```Markdown
this is not
[ a proper](https://www.example.com)
link
```

> **Explanation**: The link label containing `a proper` has leading whitespace. The rule requires that link labels do not have spaces immediately inside the square brackets.

Unlike the previous example which had leading whitespace, this case demonstrates trailing whitespace inside the link label.

```Markdown
this is not
[label ](https://www.example.com)
link
```

> **Explanation**: The link label containing `label` has trailing whitespace. The rule requires that link labels do not have spaces immediately inside the square brackets, whether leading or trailing.

Unlike the previous examples which had only leading or only trailing whitespace, this case demonstrates both leading and trailing whitespace inside the link label.

```Markdown
this is not
[ label ](https://www.example.com)
link
```

> **Explanation**: The link label containing `label` has both leading and trailing whitespace. The rule requires that link labels do not have spaces immediately inside the square brackets.

Unlike the previous examples which used standard links, this case demonstrates leading whitespace in an image's alt-text label.

```Markdown
![ alt text](https://www.example.com/image.png)
```

> **Explanation**: The image alt-text label containing `alt text` has leading whitespace. The rule applies to both links and images, requiring that neither have spaces immediately inside the square brackets.

Unlike the previous examples which used inline links or images, this case demonstrates leading whitespace in a link reference definition label.

```Markdown
[ label ]: https://www.example.com
```

> **Explanation**: The link reference definition label `label` has leading whitespace. The rule applies to link reference definitions as well, requiring that labels do not have spaces immediately inside the square brackets.

### Correct Scenarios

This rule does not trigger when the link label for any link or image does not start with leading whitespace or end with trailing whitespace.

```Markdown
this is a
[proper](https://www.example.com)
link
```

> **Explanation**: The link label `a proper` does not contain any leading or trailing whitespace. It adheres to the rule's requirement for clean link labels.

Unlike the previous example which used a single-word label, this case demonstrates a multi-word label with an internal space, which is permitted as long as there are no leading or trailing spaces.

```Markdown
this is
[a proper](https://www.example.com)
link
```

> **Explanation**: The link label `a proper` does not contain any leading or trailing whitespace. It adheres to the rule's requirement for clean link labels. Internal spaces within the label are allowed.

Unlike the previous example which used a standard link, this case demonstrates an image with a clean alt-text label without leading or trailing whitespace.

```Markdown
![alt text](https://www.example.com/image.png)
```

> **Explanation**: The image alt-text label `alt text` does not contain any leading or trailing whitespace. It adheres to the rule's requirement for clean labels in both links and images.

Unlike the previous examples which used inline links or images, this case demonstrates a link reference definition label without leading or trailing whitespace.

```Markdown
[label]: https://www.example.com
```

> **Explanation**: The link reference definition label `label` does not contain any leading or trailing whitespace. It adheres to the rule's requirement for clean labels in link reference definitions.

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
