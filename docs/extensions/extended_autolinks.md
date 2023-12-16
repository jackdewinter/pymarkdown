# Markdown Disallowed Raw HTML

| Item | Description |
| --- | --- |
| Extension Id | `markdown-extended-autolinks` |
| GFM Extension Status | Official |
| Configuration Item | `extensions.markdown-extended-autolinks.enabled` |
| Default Value | `False` |

## Summary

This extension follows the GitHub Flavored Markdown
[rules](https://github.github.com/gfm/#autolinks-extension-) for the extension
of cases where text may be considered a link and an autolink element generated
for it.

## Extension Specifics

For the most part, the base specification for
[autolinks](https://github.github.com/gfm/#autolinks) specifies conditions in which
parsers should conisder certain urls within the `<` and `>` characters to be link
specifications.  This primarly focuses on any URL-like construct that begins
with a valid scheme or text that matches the specification's definition for a valid
email address.

This extension allows for a small set of these scenarios to be recognized without
the need for `<` and `>` characters to encapsulate them.  For URL autolinks, those
scenarios are the text `www.` followed by a valid domain and extra characters as
well as the text sequences `http://` or `https://` followed by a valid domain and
extra characters.  A similar pattern is followed for valid email addresses centered
around the `@` character and the `mailto:` and `xmpp:` text sequences.

With the default state of this extension being disabled, it allows for a decision
to be made to stick with strict autolinks with very few false positives or to enable
this extension and possibly see an increase in false positives.  From our experience,
the restrictions on the extra scenarios that will be recognized have not produced
any extra false positives.  Your mileage may vary.
