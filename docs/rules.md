# Plugin Rules

Plugins are the manner in which rules are included into PyMarkdown.  While there
are a healthy set of rules shipped with PyMarkdown, there is also support for any
user to provide their own plugins.

Each shipped plugins comes completed with its own documentation.  This documentation
follows this format.

- Title and High Level Information
  - The name of the rule, any aliases for the rule, and whether the autofix option
    is available for this rule.
- Deprecation
  - If this plugin is deprecated in favor of another plugin, what that other plugin
    is.
- Summary
  - A quick one line summary of what the rule does.
- Reasoning
  - Why this rule was implemented.
  - Readability, Consistency, Simplicity, Correctness, Portability
- Examples
  - Both positive and negative examples to illustrate the rule.  Since the rule
    triggers on negative examples, the negative examples are usually first, often
    with the corrected positive for of the examples following them.
- Configuration
  - Two tables to present that configuration, even if the only configuration is
    the `enabled` value. The first table shows acceptable prefixes for any configuration
    value and the second table lists the value's name, its type, its default value,
    and a simple description of the configuration.
- Origination of Rule
  - A compliment to the `Reasoning` section, this section talks about the history
    of the rule.
- Fix Description
  - If autofix is available for the rule, what the effects of using autofix are.
  - If autofix is not available for the rule, why the decision to not autofix was
    made.
  - If this section is not present, it means that the rule is currently in queue
    for adding autofix support.

A big note on the Fix Description for any plugin that does not support autofix.
That section contains the reasons why the decision was made at the time.  Given
extra conversation and a solid, predictable algorithm to apply, it is possible to
change that decision.  If you believe that you have a solution, please file an
issue and present your case to our team!

## Implemented Rules

These are the rules that are currently implemented.

- [Rule Md001 - heading-increment](/docs/rules/rule_md001.md)
- [Rule Md002 - first-heading-h1](/docs/rules/rule_md002.md)
- [Rule Md003 - heading-style](/docs/rules/rule_md003.md)
- [Rule Md004 - ul-style](/docs/rules/rule_md004.md)
- [Rule Md005 - list-indent](/docs/rules/rule_md005.md)
- [Rule Md006 - ul-start-left](/docs/rules/rule_md006.md)
- [Rule Md007 - ul-indent](/docs/rules/rule_md007.md)
- [Rule Md009 - no-trailing-spaces](/docs/rules/rule_md009.md)
- [Rule Md010 - no-hard-tabs](/docs/rules/rule_md010.md)
- [Rule Md011 - no-reversed-links](/docs/rules/rule_md011.md)
- [Rule Md012 - no-multiple-blanks](/docs/rules/rule_md012.md)
- [Rule Md013 - line-length](/docs/rules/rule_md013.md)
- [Rule Md014 - commands-show-output](/docs/rules/rule_md014.md)
- [Rule Md018 - no-missing-space-atx](/docs/rules/rule_md018.md)
- [Rule Md019 - no-multiple-space-atx](/docs/rules/rule_md019.md)
- [Rule Md020 - no-missing-space-closed-atx](/docs/rules/rule_md020.md)
- [Rule Md021 - no-multiple-space-closed-atx](/docs/rules/rule_md021.md)
- [Rule Md022 - blanks-around-headings](/docs/rules/rule_md022.md)
- [Rule Md023 - heading-start-left](/docs/rules/rule_md023.md)
- [Rule Md024 - no-duplicate-heading](/docs/rules/rule_md024.md)
- [Rule Md025 - single-title](/docs/rules/rule_md025.md)
- [Rule Md026 - no-trailing-punctuation](/docs/rules/rule_md026.md)
- [Rule Md027 - no-multiple-space-blockquote](/docs/rules/rule_md027.md)
- [Rule Md028 - no-blanks-blockquote](/docs/rules/rule_md028.md)
- [Rule Md029 - ol-prefix](/docs/rules/rule_md029.md)
- [Rule Md030 - list-marker-space](/docs/rules/rule_md030.md)
- [Rule Md031 - blanks-around-fences](/docs/rules/rule_md031.md)
- [Rule Md032 - blanks-around-lists](/docs/rules/rule_md032.md)
- [Rule Md033 - no-inline-html](/docs/rules/rule_md033.md)
- [Rule Md034 - no-bare-urls](/docs/rules/rule_md034.md)
- [Rule Md035 - hr-style](/docs/rules/rule_md035.md)
- [Rule Md036 - no-emphasis-as-heading](/docs/rules/rule_md036.md)
- [Rule Md037 - no-space-in-emphasis](/docs/rules/rule_md037.md)
- [Rule Md038 - no-space-in-code](/docs/rules/rule_md038.md)
- [Rule Md039 - no-space-in-links](/docs/rules/rule_md039.md)
- [Rule Md040 - fenced-code-language](/docs/rules/rule_md040.md)
- [Rule Md041 - first-line-heading](/docs/rules/rule_md041.md)
- [Rule Md042 - no-empty-links](/docs/rules/rule_md042.md)
- [Rule Md043 - required-headings](/docs/rules/rule_md043.md)
- [Rule Md044 - proper-names](/docs/rules/rule_md044.md)
- [Rule Md045 - no-alt-text](/docs/rules/rule_md045.md)
- [Rule Md046 - code-block-style](/docs/rules/rule_md046.md)
- [Rule Md047 - single-trailing-newline](/docs/rules/rule_md047.md)
- [Rule Md048 - code-fence-style](/docs/rules/rule_md048.md)
- [Rule Pml101 - list-anchored-indent](/docs/rules/rule_pml101.md)
