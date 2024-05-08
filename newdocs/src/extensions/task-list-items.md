# Markdown Task List Items

| Item | Description |
| --- | --- |
| Extension Id | `markdown-task-list-items` |
| GFM Extension Status | Official |
| Configuration Item | `extensions.markdown-task-list-items.enabled` |
| Default Value | `False` |

## Configuration

| Prefixes |
| --- |
| `extensions.markdown-task-list-items.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the extension is enabled. |

## Summary

This extension follows the GitHub Flavored Markdown
[rules](https://github.github.com/gfm/#task-list-items-extension-)
to interpret certain list items as task list items.  If the specified sequence is
present at the start of the text for a list item, it is interpreted as a task
list item.  That sequence is a `[` character followed by one of `{space}`, `x`
or `X`, and ending with a `]` character and at least one whitespace character.

## Examples

With this extension enabled, the following Markdown text:

```Markdown
- [ ] something
- [x] something
- [a] something
```

produces the following html:

```HTML
<ul>
<li><input type="checkbox"> something</li>
<li><input checked="" type="checkbox"> something</li>
<li>[a] something</li>
</ul>
```

which renders as:

<!--- pyml disable-num-lines 5 no-inline-html-->
<ul>
<li><input type="checkbox"> something</li>
<li><input checked="" type="checkbox"> something</li>
<li>[a] something</li>
</ul>

## Specifics

There are times where having a list item that begins with a checkbox can be advantageous
to the document being created.  Especially if the document is being used in some
manner of interactive format, having a checkbox that the user can "click" to specify
they have completed some action is useful.

The basics are simple.  The sequence `[ ]` denotes a task list item that has not
been completed, and the sequences `[x]` and `[X]` denotes a task list item that has
been completed.  For these sequences to be valid, they must occur at the start of
a list item paragraph and they must be followed by at least one whitespace character.
Any other sequences, such as the third list item in the example, are interpreted
as normal Markdown.

Therefore, the following examples do not result in a task list item:

- `- [y] something` because the `y` character is not one of the valid "internal"
  characters
- `- x[x] something` because the valid sequence does not appear at the very beginning
- `- [x]something` because the valid sequence is not followed by a whitespace character

In addition, the following Markdown text:

```Markdown
- [x] task list item
  [x] not a task list item
```

will produce a task list item for the first line but not the second line. This
is because the first sequence appears at the start of the paragraph, while the
second sequence occurs in the middle of the paragraph.
