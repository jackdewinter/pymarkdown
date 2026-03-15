# Development Documentation

**NOTE:** The Development Documentation page is still being worked on as part of
our documentation overhaul.

This document will be the new home of the content currently located
[here](https://github.com/jackdewinter/pymarkdown/blob/main/docs/developer.md).

Other things that will be added:

- how to create a plugin
- how to add it

## Extending PyMarkdown

### Adding Extensions

One of our goals is to extend the Markdown parser to support commonly used Markdown
features that are not yet covered by the core specifications. These extensions might
introduce new syntaxes, like additional block types or link formats.

Building and testing each extension properly takes time. For most extensions, we:

- Design and prototype the new syntax.
- Publish one or more sub‑releases over 1–3 months so you can try the new behavior.
- Finalize the extension once it has been used and refined in real documents.

### Adding Rule Plugins

Because the Rule Engine is plugin‑based, adding new rules does not require
changing the core application. In many cases, we can add or refine rules without
disrupting other features.

Adding or refining Rule Plugins is often straightforward, but requires precise
tests:

- Start by defining the single condition the rule enforces.  
  *Example: "Heading levels must not skip levels (H1 → H3)."*
- Write basic scenario tests that describe when the rule should and should not
  trigger under normal conditions.
- Implement the Rule Plugin to satisfy those tests.
- Extend the tests to include container token types (Block Quotes and Lists),
  then update the implementation to handle those contexts as well.

Following this pattern keeps each rule focused and predictable, even as documents
become more complex.

Adding support for **fix** mode is more involved. To add a safe **autofix**, we:

- Define what a "safe" fix looks like for that rule, if applicable.
- Implement the fix so it only changes what is necessary.
- Test it against a wide range of documents to avoid breaking valid content.

This extra work is why new fix‑mode features can take longer to ship than the rules
themselves.
