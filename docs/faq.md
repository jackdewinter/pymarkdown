# Frequently Asked Questions

## Is Markdown Front-Matter supported?

Yes, mostly.  Current support for Markdown front-matter is limited to
interpreting the front-matter as simple key-value pairs.  Indenting
any following lines with 4 or more spaces causes the parser to interpret
that line as a continuation of the previous value.

To enable this behavior in the parser, please see
[Enabling Front-Matter](/docs/advanced_configuration.md#front-matter).

## Why are my configuration changes not working?

That is a large can of worms to attack in one document.  But from my own experience,
it usually falls into a handful of items that I check in turn.  Remember that most
settings have a default value that they will use.

- Typing errors.
  - This is the one that plagues me the most.
  - No really good way to find these other than double checking the configuration
    item name against the documentation.
- Not using `--strict-config` on the command line.
  - With strict mode enabled, if the configuration item's name is correct but the
    value type is not correct, PyMarkdown will error.  Otherwise, it will only
    error if there is no default value, and almost everything has values.
  - This catches problems with values that are the wrong type.
  - If specifying values on the command line or with a configuration file that does
    not natively support typing, need to provide type hints.
  - For more, [see this section](./advanced_configuration.md#specifying-configuration-types).
- Not saving the new configuration changes.
  - Yup.  Done this more times than I wish to admit.  Sometimes I just get ahead
    of myself and think I have saved the changes, when I didn't.
