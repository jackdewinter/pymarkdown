---
summary: Base information about the PyMarkdown Linter2
authors:
  - Jack De Winter
---

# Advanced Rules

In the [User Guide](./user-guide.md#basic-scanning) document, we touched
briefly on how scanning works, followed by a section devoted specifically
to the [Rule Plugins](./user-guide.md/#plugin-rules) which implement our rules.
Then we took a quick look at PyMarkdown's [Fix Mode](./user-guide.md/#fix-mode-failure-correction),
a feature that leverages those same rules to automatically fix any failures.

But what are these rules? A rule is simply code that looks at the stream of information
provided by the [PyMarkdown parser](./user-guide.md/#markdown-parser) and decides
if it will trigger a failure based on behavior it observes in the data stream that
the parser generates.  At a high level, that is what a rule is: an analyzer written
in code that is looking for something that it does not like from the PyMarkdown
parser's output. It is just that simple.

Other than that, one useful piece of information to know is that each rule has
an id associated with it.  To keep things simple, each id is a 2-3 letter prefix
followed by a 3-digit suffix.  Each rule can also have one or more names.  Each
name can contain alphabetic characters and the `-` character.  Combined, this set
of information is known as the rule's identifiers.  These identifiers are guaranteed
to be unique within an instance of PyMarkdown and can be used interchangeably in
most cases.

## History

A fair number of our rules have close parallels with David Anson's
[MarkdownLint](https://github.com/DavidAnson/markdownlint) project. As that project
is used worldwide in editors such as VSCode, we would be silly not to.  However,
as detailed
in our [README.md](https://github.com/jackdewinter/pymarkdown#what-linting-checks-does-pymarkdown-release-with)
document, our team wanted to provide rules that were clear with a singular focus.
Instead of writing one rule with side-effects, we decided that we wanted to be able
to write two rules, each with their own distinct focus.  If a rule is supposed to
work outside of any containers, it should also work just as well within any group
of containers.  We realize that this means more work on our part, but that we accepted
that responsibility from the moment we made our decision.

## Listing

At the root of our support for rule plugins is the [Plugin Command](./user-guide.md#plugin-command)
available at the command line.  The command is well documented in our user guide,
and we believe it does not require any embellishments in this document.  Between
the `list` subcommand and the `info` subcommand, we have designed the command to
relay useful information intended to help users to locate any rule-based information
that they are looking for.

## Enabling and Disabling Rules

Keeping in mind the [configuration layering](https://application-properties.readthedocs.io/en/latest/getting-started/#configuration-ordering-layering)
that occurs, the most direct way of enabling and disabling plugins is through
the `--enable-rules` and `--disable-rules` command line options.  As these
are [specific command line settings](https://application-properties.readthedocs.io/en/latest/command-line/#specific-command-line-settings),
these settings override every other enable/disable configuration for the rules
specified by the command line arguments.

After that comes the `--set` argument which is detailed in the Advanced Configuration
document under [General Command Line Settings](https://application-properties.readthedocs.io/en/latest/command-line/#general-command-line-settings).
Using the format `--set=plugins.{id}.enabled=$!True` (with the escaping of
[certain characters](https://application-properties.readthedocs.io/en/latest/command-line/#special-characters-and-shells)
being required), a single plugin may be enabled.  Disabling a plugin is as simple
as replacing the `True` with a `False`.

Finally, there are the [configuration files](./advanced_configuration.md/#configuration-files).
The configuration files provide a more compact and easier way to set configuration
item values. The configuration files are available in JSON, YAML, and TOML formats,
with configuration files specified on the command line as well as implicit configuration
files that are searched for in the current directory when the application starts.
These tend to be used for more static configuration settings and can easily be shared
between projects.

## Configuration In Practice

Note that this is contrived example for demonstration purposes with all three
active layers of configuration.  In the common uses of PyMarkdown's configuration
manager that we have observed, our users rarely use more than 2 configuration layers.
However, how would configuration look like if we utilized all three configuration
layers? Let us start with a configuration file called `config.json` with contents:

```json
{
    "plugins": {
        "md011": {
            "enabled": true,
        },
        "md012": {
            "enabled": true,
        },
        "md013": {
            "enabled": false
        }
    }
}
```

and a command line of (newlines inserted for readability):

```text
pipenv run pymarkdown --disable-rules Md011
                      --set 'plugins.md011.enabled=$!True'
                      --set 'plugins.md012.enabled=$!False'
                      --config config.json
                      scan -r .
```

The `--disable-rules` argument takes precedence over any other setting as it is
at the topmost configuration layer.  This forces Rule Md011 to be disabled, even
though it is set to `true` in two other locations. The next layer we look at includes
the `--set` arguments, with one setting Rule Md011 to `True` and the other setting
Rule Md012 to `False`.  Because of the `--disable-rules` argument, the first setting
does not take effect, but the second setting does as there was no `--enable-rules`
or `--disable-rules` argument that specifies Rule Md012.  In a similar fashion,
the Rule Md011 and Rule Md012 configuration item values in the configuration file
are overridden, leaving only the `"md013": { "enabled": false }` setting intact
to disable Rule Md013.

Therefore, after applying all configuration layers, Rule Md011 is disabled by `--disable-rules`,
Rule Md012 is disabled by `--set 'plugins.md012.enabled=$!False'`, and Rule Md013
is disabled by the `config.json` configfuration item.

## Rule Configuration

If you have tackled the examples from the last two sections and understand how
the layers interact with each other, you should have no trouble understanding rule
configuration items. That comprehension is made easier because arguments like `--disable-rules`
and `--enable-rules` do not exist for rule configuration items.  For rule
configuration items, only the `--set` argument and the configuration file
layers are considered.

For this example, we are going to set a configuration item that is commonly
changed: the `line_length` configuration item. Similar to the above example,
we may start with a YAML configuration file `config.yaml` with contents:

```YAML
plugins:
  line-length:
    enabled: false
```

To add the setting of the new configuration item, we just add the `line_length`
configuration item at the right level of hierarchy, and set its value to `100` to
denote 100 characters:

```YAML
plugins:
  line-length:
    enabled: false
    line_length: 100
```

As another option, instead we could add this argument to the command line:

```text
--set 'plugins.line-length.line_length=$#100'
```

Both are equally correct and would result in the `line_length` value for the
`line-length` rule, otherwise known as Rule Md013, being set to the integer value
of `100`.

### Which Format is Better?

Why would you prefer one form over the other?  That largely depends on your team's
preference.  How does our team use these two formats?  If we need to share something
between projects or need to put a configuration item into "long term storage", then
we use configuration files.  If we need to set a configuration item temporarily,
then we use the command line arguments.  For any other cases, we try and figure
out what makes the most sense to us.

There is no right answer for everyone.  The best answer is always to determine
guidelines that make sense to you and your team.

## Suppressing Rule Failures

[Failures](./user-guide.md#failure) are generated in response to a rule
triggering. As we mentioned at the start of [this document](./advanced_plugins.md),
rules are written to look for a given pattern in the Markdown document.
Therefore any failure that is reported is the direct response of a rule finding
something that it does not think is correct in the Markdown document being
scanned.

In the majority of cases, that generated failure is accurate and needs to be
responded to by the author or the Markdown document.  However, there are occurrences
where a failure is generated in a situation where the author meant the Markdown
document to be written exactly as they wrote it.  That is where
[pragmas](./extensions/pragmas.md) come in.

This example for pragmas clearly indicates how you suppress a single failure.  In
the example below, the Atx Heading characters are followed by two space characters,
where only one is required.  This normally causes the `no-multiple-space-atx` rule,
otherwise known as Rule Md019 to trigger. However, in this case, the pragma line
above it suppressed this failure.

```Markdown
some paragraph

<!--- pyml disable-next-line no-multiple-space-atx-->
#  My Bad Atx Heading

some other paragraph
```

While that example was contrived, here is a realistic suppression issue that
we run into on our PyMarkdown project: our [changelog](./changelog.md).
We started off the file with a simple format that allows us to add in
what we have been working on for each release.  Anything new that we
work on goes in the "Unversioned" section at the top.  When we build
a release, we change the "Unversioned" name and date and add this template to
the top of the file.

```Markdown
## Unversioned - In Main, Not Released

### Added

- None

### Fixed

- None

### Changed

- None
```

Before we switched our changelog from its old location
[changelog](https://github.com/jackdewinter/pymarkdown/blob/main/changelog.md)
to its [new location](./changelog.md), we just disabled the
`no-duplicate-heading` rule for the entire project.  A better option would have
been to have a scan that excluded the `changelog.md` file with that rule
enabled and another configuration file specifically for the `changelog.md` file
with that rule disabled. We did not do the right thing and just disabled the rule
completely for the entire project. That never sat right with our team.

When we moved the changelog over to the new documentation format, we decided to
make a small change to the format:

```Markdown
## Unversioned - In Main, Not Released

<!--- pyml disable-next-line no-duplicate-heading-->
### Added

- None

<!--- pyml disable-next-line no-duplicate-heading-->
### Fixed

- None

<!--- pyml disable-next-line no-duplicate-heading-->
### Changed

- None
```

By adding these pragmas to the headings, we can now run PyMarkdown against the
new changelog file.  Since we are aware that it is a duplicate heading and
accept that, we can add the pragma to the file without impacting the scan of any
other Markdown document.

## List of Rule Plugins

The [rules document](./rules.md) provides for a single place to look for
information on any of the rules that are released with the PyMarkdown application.
To make things easier for our users, we have tried to follow this pattern in creating
the documentation for each rule.  Our hope is that this standardized format will
help our users locate information about specific rules more efficiently.

- Introduction (implicit)
    - Details aliases, whether autofix is available, and whether the rule is enabled
      by default.
- Deprecation (optional)
    - Present if the rule was removed.  If removed because another rule was implemented
      that was better, a link to that new rule is provided.
- Summary
    - Text line presented by the rule when a failure occurs.
- Reasoning
    - A defined basis for implementing this rule: Consistency, Readability, Simplicity,
      Correctness, or Portability
- Examples
    - Examples that demonstrate when a failure occurs and when failures do not occur.
- Fix Description
    - If a fix is available, a description of how the rule will fix the failure.
      If not, why a fix was not implemented.
- Configuration
    - The collection of settings that are present for this rule.
- Origination of Rule
    - Details of what prompted this rule to initially be created.
- Differences From MarkdownLint Rule (optional)
    - If this rule is based on a MarkdownLint rule, how PyMarkdown's implementation
      differs, and why that decision was made.

## Specific Parser Configuration

While most parsers follow the GFM specification and do not require any configuration
items to be specially set for them, there are exceptions.

### Python-Markdown

As the PyMarkdown project is Python based, one of the first Markdown-to-HTML generators
that we looked at was [Python-Markdown](https://python-markdown.github.io/).  That
generator is used as part of [MkDocs](https://www.mkdocs.org/) which is used to
generate the documentation you are reading right now.
But while Python-Markdown is compliant in many other areas, there are a handful
of differences noted on their [home page](https://python-markdown.github.io/#differences).
The biggest difference is that the Python-Markdown team passionately believes that
all Unordered List Indents should be 4 characters.

This forced us as a team to decide how we will treat any "slightly" non-compliant
Markdown parsers and their differences.  In this case, as the differences are small,
we decided to write [Rule Pml101](./plugins/rule_pml101.md) or the `list-anchored-indent`
rule to handle these scenarios.  As detailed in its documentation, the `list-anchored-indent`
rule is an adjusted [`ul-indent` rule](./plugins/rule_md007.md) that tunes the list
indentation to the specific needs of Python-Markdown.

Therefore, to accommodate Python-Markdown, the following configuration is suggested:

```json
"plugins" : {
    "ul-indent" : {
        "enabled": false
    },
    "list-anchored-indent" : {
        "enabled": true
    }
}
```

or :

```yaml
plugins:
  ul-indent:
    enabled: false
  list-anchored-indent:
    enabled: true
```
