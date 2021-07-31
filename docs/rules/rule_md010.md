# Rule - MD010

| Aliases |
| --- |
| `md010` |
| `no-hard-tabs` |

## Summary

Hard tabs.

## Reasoning

The primary reason for enabling this rule is to force Markdown writers to be
explicit about their intent with the document.  As different editors and different
parsers treat tab characters differently, the interpretation of a tab character's
effect on a line depends on what editor or parser is used to interpret the Markdown.
By enabling this rule, the Markdown writer is forced to explicitly state their
intentions for document indentation without any ambiguity.

## Examples

### Failure Scenarios

This rule triggers when any line of the document contains a hard tab character
instead of using space characters for indentation. A simple example is:

```Markdown
{tab}Indented Code Block
```

where the sequence `{tab}` is replaced with an actual tab character.  If multiple
tab characters are present, each occurrence of a tab character will trigger this
rule independently.

### Correct Scenarios

To correct the above example, simply enforce the required indentation using space
characters:

```Markdown
    Indented Code Block
```

## Configuration

| Prefixes |
| --- |
| `plugins.md010.` |
| `plugins.no-hard-tabs.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the plugin rule is enabled by default. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD010](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md010---hard-tabs).
