# Markdown Extended Autolinks

| Item | Description |
| --- | --- |
| Extension Id | `markdown-extended-autolinks` |
| GFM Extension Status | Official |
| Configuration Item | `extensions.markdown-extended-autolinks.enabled` |
| Default Value | `False` |

## Configuration

| Prefixes |
| --- |
| `extensions.markdown-extended-autolinks.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the extension is enabled. |

## Summary

This extension follows the GitHub Flavored Markdown
[rules](https://github.github.com/gfm/#autolinks-extension-) to extend the
set of text sequences that the parser considers as a link and an autolink element
generated for it.  While the normal [autolinks](https://github.github.com/gfm/#autolinks)
deal with text enclosed within the `<` and `>` characters, this extension
introduces autolinks that the parser will recognize without any enclosing characters.

## Examples

### WWW Autolinks

With this extension enabled, the following Markdown text:

```Markdown
Visit www.commonmark.org/help for more information.

Or www.commonmark.org/help.

Or (www.google.com/search?q=Markup+(business)).
```

produces the following html:

```HTML
<p>Visit <a href="http://www.commonmark.org/help">www.commonmark.org/help</a> for more information.</p>

<p>Visit <a href="http://www.commonmark.org/help">www.commonmark.org/help</a>.</p>

<p>(<a href="http://www.google.com/search?q=Markup+(business)">www.google.com/search?q=Markup+(business)</a>)</p>
```

which renders as:

<!--- pyml disable-num-lines 5 no-inline-html,line-length -->
<p>Visit <a href="http://www.commonmark.org/help">www.commonmark.org/help</a> for more information.</p>

<p>Visit <a href="http://www.commonmark.org/help">www.commonmark.org/help</a>.</p>

<p>(<a href="http://www.google.com/search?q=Markup+(business)">www.google.com/search?q=Markup+(business)</a>)</p>

### Url Autolinks

With this extension enabled, the following Markdown text:

```Markdown
http://commonmark.org

(Visit https://encrypted.google.com/search?q=Markup+(business))
```

will produce the following html:

```HTML
<p><a href="http://commonmark.org">http://commonmark.org</a></p>
<p>(Visit <a href="https://encrypted.google.com/search?q=Markup+(business)">https://encrypted.google.com/search?q=Markup+(business)</a>)</p>
```

which renders as:

<!--- pyml disable-num-lines 2 no-inline-html-->
<p><a href="http://commonmark.org">http://commonmark.org</a></p>
<p>(Visit <a href="https://encrypted.google.com/search?q=Markup+(business)">https://encrypted.google.com/search?q=Markup+(business)</a>)</p>

### Email Autolinks

With this extension enabled, the following Markdown text:

```Markdown
foo@bar.baz

hello@mail+xyz.example isn't valid, but hello+xyz@mail.example is.
```

will produce the following html:

```HTML
<p><a href="mailto:foo@bar.baz">foo@bar.baz</a></p>
<p>hello@mail+xyz.example isn't valid, but <a href="mailto:hello+xyz@mail.example">hello+xyz@mail.example</a> is.</p>
```

which renders as:

<!--- pyml disable-num-lines 2 no-inline-html,line-length -->
<p><a href="mailto:foo@bar.baz">foo@bar.baz</a></p>
<p>hello@mail+xyz.example isn't valid, but <a href="mailto:hello+xyz@mail.example">hello+xyz@mail.example</a> is.</p>

### Protocol Autolinks

With this extension enabled, the following Markdown text:

```Markdown
mailto:foo@bar.baz

xmpp:foo@bar.baz/txt
```

will produce the following html:

```HTML
<p><a href="mailto:foo@bar.baz">mailto:foo@bar.baz</a></p>
<p><a href="xmpp:foo@bar.baz/txt">xmpp:foo@bar.baz/txt</a></p>
```

which renders as:

<!--- pyml disable-num-lines 2 no-inline-html-->
<p><a href="mailto:foo@bar.baz">mailto:foo@bar.baz</a></p>
<p><a href="xmpp:foo@bar.baz/txt">xmpp:foo@bar.baz/txt</a></p>

## Specifics

The base specification for [autolinks](https://github.github.com/gfm/#autolinks)
specifies the conditions under which parsers treat certain urls enclosed within
the `<` and `>` characters as a link specification.  This extension allows the
parser to recognize a more focused group of sequences without the enclosed characters.

While the specification itself is [more explicit](https://github.github.com/gfm/#autolinks-extension-)
as to the allowable conditions, here are the highlights.  In the following circumstances,
the parser will consider the text as an Autolink without any `<` and `>` enclosing
characters, if:

- the text `www` followed by a valid domain name and optional path information
- the text `http://` or `https://` followed by a valid domain name and optional
  path information
- the text for a valid email address, including a `+` character before the `@` character
- the text `mailto:` or `xmpp:` followed by a valid email address

As the parser applies these rules to all text, and not just those enclosed with
the `<` and `>` characters, the rules for recognizing these extended autolinks
are narrowly focused on validly constructed sequences.  This decision is reflected
in the above list with the word `valid` appearing in each item.

Our team would be remiss to not point
out one small flaw of this extension: opting out of the enhanced autolinks.  If
you enter the text `www.something.com` and do not want it to be an autolink, you
have few options. One is to enclose the text in `` ` `` characters, rendering it
as a code span.  Another is to use the sequence `&#119;` in place of one of the
`w` characters, breaking up the text sequence with a character reference.

Our team remains neutral on the usage of this extension, as we do not have windows
into the scenarios of our users.  We hope we have provided enough information
about this extension to allow you and your team to make an educated decision
on whether to enable this extension for your team.
