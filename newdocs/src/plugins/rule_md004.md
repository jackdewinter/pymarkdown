# Rule - MD004

| Property | Value |
| --- | --- |
| Aliases | `md004`, `ul-style` |
| Autofix Available | Yes |
| Enabled By Default | Yes |

## Summary

Use a consistent style for unordered list characters.

## Reasoning

### Readability

Inconsistent unordered list markers (`*`, `-`, `+`) create visual noise that distracts
readers. Enforcing a consistent style improves document clarity and scannability.

## Examples

### Failure Scenarios

This rule triggers when unordered list markers are inconsistent across the document. Using different characters like `+`, `-`, and `*` violates the default `consistent` style.

```Markdown
+ First Item
- Second Item
* Third Item
```

> **Explanation**: This example fails because the first list item uses `+`, setting the expected style. The subsequent items use `-` and `*`, which differ from the established marker, violating the consistent rule requirement.

Unlike the previous example which used the default `consistent` style, this scenario fails because the `style` is explicitly set to `dash`, requiring all items to use `-`.

```Markdown
- First Item
* Second Item
+ Third Item
```

> **Explanation**: This example fails because the configuration requires `dash` as the only valid marker. The use of `*` and `+` violates this explicit style setting, even though the first item is correct.

Unlike the previous examples which tested `consistent` and explicit single-marker styles, this scenario demonstrates a failure under the `sublist` style where different nesting levels use inconsistent markers within the same level across multiple lists.

```Markdown
+ First Level
  - Second Level
    * Third Level

* First Level
  * Second Level
    * Third Level
```

> **Explanation**: This example fails under the `sublist` style because the first list establishes Level 1 uses `+`, Level 2 uses `-`, and Level 3 uses `*`. The second list violates this by using `*` for Level 1 (should be `+`) and `*` for Level 2 (should be `-`). Each nesting level must maintain its established marker across all lists in the document.

### Correct Scenarios

This rule does not trigger when all unordered list items in the document use the same marker, satisfying the `consistent` style.

```Markdown
+ First Item
+ Second Item
+ Third Item
```

> **Explanation**: This example passes because every unordered list item uses the `+` marker. Since all markers are identical, the `consistent` style requirement is fully met.

Unlike the previous flat list example, this scenario demonstrates compliance with the `sublist` style, where each nesting level maintains its own consistent marker.

```Markdown
+ First Level
  - Second Level
    * Third Level
```

> **Explanation**: This example passes under `sublist` style because Level 1 uses `+`, Level 2 uses `-`, and Level 3 uses `*`. Each level is internally consistent with its respective marker.

This scenario differs from the previous one by introducing a **new, distinct unordered list** in the document, rather than continuing the same list, showing that marker consistency applies across all lists.

```Markdown
+ New List
  - New Sublist
```

> **Explanation**: This example passes because the unordered list and its sublist use the same markers (`+` and `-`) as established in the previous correct scenario. Under the `sublist` style (or `consistent` style), each list level maintains its marker consistency, and subsequent lists in the document must adhere to the same pattern to avoid triggering the rule.

## Fix Description

The autofix replaces non-conforming unordered list markers to match the configured style. For `consistent` style, the first marker in the document sets the standard for all items. For `sublist` style, the first marker at each nesting level sets the standard for that level. For fixed styles (`asterisk`, `dash`, `plus`), all markers are replaced with the specified character.

## Configuration

| Prefixes |
| --- |
| `plugins.md004.` |
| `plugins.ul-style.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Determines if this rule is active. |
| `style` | `string` | `consistent` | Style for unordered lists in the document. |

### Valid Styles

| Style | Description |
| --- | --- |
| `consistent` | The first unordered list in the document specifies the style for the rest of the document. |
| `asterisk` | Only unordered lists with asterisks are used. |
| `dash` | Only unordered lists with dashes are used. |
| `plus` | Only unordered lists with pluses are used. |
| `sublist` | The first unordered list in the document for that level of sublist specifies the style for that level of sublist for the rest of the document. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD004](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md004---unordered-List-style).
