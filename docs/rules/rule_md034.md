# Rule - MD035

| Aliases |
| --- |
| `md034` |
| `no-bare-urls` |

## Summary

Bare URL used.

## Reasoning

The primary reason for enabling this rule is correctness.  When text
that looks like the start of a formal URL is encountered by a reader,
that reader will try and click on the text, thinking it is a link unless
there is other formatting to convince them otherwise.

Note that as the various allowed forms of URLs and URIs is a very
[complex topic](https://stackoverflow.com/questions/30847/regex-to-validate-uris),
this rule only strives to handle the most mainstream cases.

## Examples

### Failure Scenarios

This rule triggers if any one of the strings `http:`, `https:`, `ftp:`, or
`ftps:` is encountered in the text and is followed by the string `\\` and at
least one non-whitespace character:

```Markdown
This link http://www.google.com should not exist without extra markers.
```

The text searched is any text belonging to a Paragraph element, an Atx Heading
element, or a SetExt Heading element, except for any text specifically belonging
to a Link element or an Image element.

### Correct Scenarios

This rule does not trigger if there is any non-whitespace character directly before the
formal URL:

```Markdown
"http://www.google.com" is the name of the movie.

$http://www.google.com is the name of the command.
```

In addition, this rule does not trigger if the text is present with a
Fenced Block element:

````Markdown
```Python
s = "http://www.google.com"
```
````

an Indented Code Block element:

````Markdown
    s = "http://www.google.com"
````

a HTML Block element:

````Markdown
<!--
This code was copied from "http://www.google.com".
-->
````

or a Link element:

````Markdown
[a http://www.google.com link](/url)
````

## Configuration

| Prefixes |
| --- |
| `plugins.md034.` |
| `plugins.no-bare-urls.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled by default. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD034](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md034---bare-url-used).

### Differences From MarkdownLint Rule

There are two main differences between the original rule and this rule.

The first difference is in the requirements for finding an eligible url to trigger
on.  In the description for the original rule, a lot of time is spent describing the
various bounding characters that negate the firing of that rule.  To provide a
similar effect but in a simpler manner, this rule just checks for a single non-whitespace
character preceding the found URL.

The second difference is in this documentation.  The original rule's documentation
focused mostly on what would not trigger the rule.  In this description of the rule,
effort has been made to clearly state when this rule triggers, and simplify the
description of when this rule will not trigger.
