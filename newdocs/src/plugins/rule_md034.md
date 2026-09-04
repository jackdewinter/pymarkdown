# Rule - MD034

| Property | Value |
| --- | --- |
| Aliases | `md034`, `no-bare-urls` |
| Autofix Available | No |
| Enabled By Default | Yes |

## Summary

Bare URL used.

## Reasoning

### Correctness

Bare URLs (e.g., `http://www.google.com`) resemble clickable links but are plain text, causing user confusion when readers attempt to interact with them. This rule enforces proper URL formatting as autolinks or hyperlinks to improve clarity.

## Examples

### Failure Scenarios

This rule triggers when a bare URL appears in paragraph text without surrounding delimiters.

```Markdown
This link http://www.google.com should not exist without extra markers.
```

> **Explanation**: This example fails because the URL `http://www.google.com` is presented as bare text within a paragraph. The rule detects the schemes `http:`, `https:`, `ftp:`, and `ftps:` followed by `//` and non-whitespace characters, identifying it as an unformatted link which can cause confusion for readers who may attempt to click on non-clickable text.

This scenario differs by showing a bare URL within an Atx heading.

```Markdown
# Visit http://www.google.com for more information
```

> **Explanation**: This example fails because the URL `http://www.google.com` is presented as bare text within an Atx heading. The rule detects schemes such as `http:` followed by `//` and non-whitespace characters even within heading structures, identifying it as an unformatted link. Readers may expect the heading text to be clickable, leading to confusion when it is not.

This scenario differs by showing a bare URL within a Setext heading.

```Markdown
Visit http://www.google.com for more information
===
```

> **Explanation**: This example fails because the URL `http://www.google.com` is presented as bare text within a Setext heading (indicated by the `===` underline). Similar to Atx headings and paragraphs, Setext headings are checked for bare URLs to ensure that all prominent text in the document adheres to proper linking standards.

### Correct Scenarios

This rule does not trigger when a non-whitespace character directly precedes the URL, as this indicates the URL is part of a larger token.

```Markdown
"http://www.google.com" is the name of the movie.

$http://www.google.com is the name of the command.
```

> **Explanation**: These examples pass because the URL is immediately preceded by a quote mark (`"`) or a dollar sign (`$`). The rule ignores URLs that are not preceded by whitespace, assuming they are part of a larger textual element or command, thus not constituting a "bare" URL that would confuse readers expecting a clickable link.

Unlike the previous example which showed text prefixes, this case demonstrates that URLs within a Fenced Code Block are also ignored.

````Markdown
```Python
s = "http://www.google.com"
```
````

> **Explanation**: This example passes because the URL appears inside a fenced code block (indicated by the triple backticks). Code blocks are treated as literal text environments where URL parsing is suspended, preventing false positives for code snippets containing URLs.

This scenario differs by showing an Indented Code Block, which is another context where URLs are ignored.

````Markdown
    s = "http://www.google.com"
````

> **Explanation**: This example passes because the URL is inside an indented code block (indicated by the leading spaces). Similar to fenced code blocks, indented code blocks are treated as literal text, so URLs within them are not flagged as bare URLs.

This scenario demonstrates that URLs within HTML comments (HTML Blocks) are also ignored.

````Markdown
<!--
This code was copied from "http://www.google.com".
-->
````

> **Explanation**: This example passes because the URL is contained within an HTML comment block. HTML blocks are excluded from URL checking, as they are not part of the rendered Markdown text flow where bare URLs would cause confusion.

This final scenario shows that URLs used as link labels are also ignored.

````Markdown
[a http://www.google.com link](/url)
````

> **Explanation**: This example passes because the URL is part of a Markdown link's label text. Since the entire construct is a clickable link, the URL itself is not "bare" in the context of the rendered document, and thus does not trigger the rule.

## Fix Description

This rule can often be disabled in favor of enabling the
[Extended Autolink](../extensions/extended-autolinks.md) extension. While that
extension does not provide support for the `ftp` and `ftps` schemes, it does support
both the `http` and `https` schemes. Given the declining use of FTP services, a fix was not implemented, as the Extended Autolink extension addresses HTTP/HTTPS schemes effectively.

However, even if we assume that the extension is not enabled, there is still a question
of context. While we have the link destination for a link, there is not enough
context to determine what the link's label should contain. As with the fix option
on other rules, the author is the best entity to determine the link label's context.

## Configuration

| Prefixes |
| --- |
| `plugins.md034.` |
| `plugins.no-bare-urls.` |

| Value Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enabled` | `boolean` | `True` | Whether the Rule Plugin is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD034](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md034---bare-url-used).

### Differences From MarkdownLint Rule

There are two main differences between the original rule and this rule.

The first difference is in the requirements for finding an eligible URL to trigger
on. In the description for the original rule, significant time is spent describing
the various bounding characters that negate the firing of that rule. To supply
a similar effect but in a simpler manner, this rule just checks for a single non-whitespace
character preceding the found URL.

The second difference is in this documentation. The original rule's documentation
focused mostly on what would not trigger the rule. In this description of the rule,
effort has been made to clearly specify when this rule triggers and simplify the
description of when this rule will not trigger.
