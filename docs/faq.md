# Frequently Asked Questions

## Is Markdown Front-Matter supported?

Yes, mostly.  Current support for Markdown front-matter is limited to
interpreting the front-matter as simple key-value pairs.  Indenting
any following lines with 4 or more spaces causes the parser to interpret
that line as a continuation of the previous value.

To enable this behavior in the parser, please see
[Enabling Front-Matter](/docs/advanced_configuration.md#front-matter).

## How do I specify more than one plugin to enable or disable on the command line?

While it is buried in the [Advanced Configuration](./advanced_configuration.md#plugins)
documentation, both the enable (`--enable-rules` or `-e`) and the disable
(`--disable-rules` or `-d`) options take a comma separated list of rules. As such,
instead of a list of arguments like:

```bash
        "--disable-rules",
        "md029"
        "--disable-rules",
        "md030",
        "scan",
        "<filename>"
```

the arguments can be condensed into:

```bash
        "--disable-rules",
        "md029,md030",
        "scan",
        "<filename>"
```

Note that this example was explicitly taken from the scenario test
`test_md005_good_ordered_list_separate_single_level_short_widths` within the scenario
tests for [Rule Md005](../test/rules/test_md005.py), so we are confident that
this works!
