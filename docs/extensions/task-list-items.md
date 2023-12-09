# Markdown Task List Items

| Item | Description |
| --- | --- |
| Extension Id | `markdown-task-list-items` |
| GFM Extension Status | Official |
| Configuration Item | `extensions.markdown-task-list-items.enabled` |
| Default Value | `False` |

## Summary

This extension follows the GitHub Flavored Markdown
[rules](https://github.github.com/gfm/#task-list-items-extension-) for the ability
to mark certain list items as task list items.  While there is a more precise definition
at the GFM site, if present at the start of a paragraph that starts a list tiem,
a `[` followed by one of `{space}`, `x` or `X`, followed by a `]` and at least one
whitespace is translated into a checkbox that appears in the destination Markdown.

## Extension Specifics

There are times where having a list item that begins with a checkbox can be advantageous
to the document being created.  Especially if the document is being used in some
manner of interactive format, having a checkbox that the user can "click" to specify
they have completed some action is useful.

The basics are simple.  The sequence `[ ]` denotes off and the sequences `[x]` and
`[X]` denotes on.  Every other combination does not trigger the task lists. Besides
those simple rules, the task list sequence must occur at the start of a paragraph
that is at the start of a list item. In addition, the task list must be followed
by at least one whitespace character.  Therefore:

- `- [y] something` is not a task list as the inner character is not correct
- `- [x]something` is not a task list as the sequence is not followed by whitespace
- `- [x] something` is valid, but the same thing on any subsequent line of that
  list item is not a task list.  More precisely:

  ```text
  - [x] task list item
    [x] not a task list item
  ```

  and

  ```text
  - [x] task list item
  
    [x] not a task list item
  ```
