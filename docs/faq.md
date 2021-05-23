# Frequently Asked Questions

## Is Markdown Front-Matter supported?

Yes, mostly.  Current support for Markdown front-matter is limited to
interpreting the front-matter as simple key-value pairs.  Indenting
any following lines with 4 or more spaces causes the parser to interpret
that line as a continuation of the previous value.

To enable this behavior in the parser, please see
[Enabling Front-Matter](/docs/advanced_configuration.md#front-matter).
