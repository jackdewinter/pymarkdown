---
summary: More information on configuration and how to apply it.
authors:
  - Jack De Winter
---

# Advanced Configuration

Configuration is one of those topics that every application must deal with.
From simple command lines, to invoking features, to setting values for those features,
applications need a form of configuration management to provide variables for
those tasks.
And early in the development phase of the PyMarkdown application, we knew
we needed a solid one ourselves.

## A Note To Begin With

The base documentation for the [`application_properties`](https://application-properties.readthedocs.io/en/latest/getting-started/)
project was initially copied from this document to become the main documentation
for that project.  To avoid repetition where possible, we will provide links
to the equivalent section of that documentation instead of repeating them
here.  We strongly believe that moving the documentation over to its new
home gave us an extra chance to edit the documents and make them more
relevant to the `application_properties` project.  Our hope is that  effort
will also enhance the documents for users of the `pymarkdown` project.

## Skipping Ahead

As this is the Advanced Configuration document, we spend a significant amount
of time describing the configuration manager and how it resolves configuration
items. While we highly recommend you take the time to understand the configuration
manager before you try and change configuration values, whether to do that is your
decision to make.

If you intend to skip ahead, here are sections that we believe you may find
relevant:

- [Configuration Files](#configuration-files)
    - the types of configuration files that we support, and how to access them
- [Command Line Configuration](#command-line)
    - how to specify configuration items from the command line.
    - If dealing with boolean values
      or integer values, pay attention to the [Configuration Item Types](https://application-properties.readthedocs.io/en/latest/command-line/#configuration-item-types)
      section
- [Enabling or Disabling Rules](#how-to-enable-or-disable-rules)
    - turning a set of rules on and off
- [Available Configuration Items](#available-configuration-items)
    - a full list of configuration items and options for how to change their values

## Nomenclature

See the [Nomenclature section](https://application-properties.readthedocs.io/en/latest/getting-started/#nomenclature)
of the `application_properties` project documentation.

## Configuration Files

See the [Configuration Files section](https://application-properties.readthedocs.io/en/latest/file-types/)
of the `application_properties` project documentation.

### Which One Is Best - Addendum for PyMarkdown

In the original documentation, we had the following observation:

> If comments are important to you, then JSON is out.

New in version 0.9.32 of PyMarkdown (and in version 0.9.0 of `application_properties`)
is support
for the JSON5 parser which includes support for comments in JSON files and is enabled
by default. (See [this section](./user-guide.md#-no-json5-configuration) for more
details.)

In talking back and forth about the benefits of JSON5 versus YAML with
friends and colleagues, our team decided that the best answer is: it depends.

Based on the conversations, both background and personal style seemed to play
an important part in people's decisions for one file type over another. The
best advice we feel confident in giving you is that our team feels that JSON
is stricter and more obvious and YAML is more fluid and forgiving.  When going
back to those people and mentioning those observations, only a small percentage
of the people disagreed with our observations, and those people seemed to
be die-hard JSON or die-hard YAML people.

Please pick something that works for you and your team and know that there
are easy to use format converters out there if you change your mind.

### Command Line

See the [Configuration Files section](https://application-properties.readthedocs.io/en/latest/file-types/)
of the `application_properties` project documentation.

## Available Configuration Items

### Configuration

These items directly affect the collection of configuration values and how they
are interpreted.

<!-- pyml disable-num-lines 5 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| --                    | --config {file}           | string    | Path to the configuration file to use. |
| --                    | --set {key}={value}       | string    | Manually set an individual configuration property. |
| mode.strict-config    | --strict-config           | boolean   | Throw an error if the configuration is bad, instead of assuming default values. (Default: `false`) |

### Logs

These items affect the logging for the application.

<!-- pyml disable-num-lines 5 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| log.file          | --log-file        | string  | Destination file for log messages. |
| log.level         | --log-level       | string* | Minimum level required to log messages. Valid values are: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, or `DEBUG`. (Default: `WARNING`)  |
| log.stack-trace | --stack-trace | boolean | if an error occurs, print out the stack trace for debug purposes.  Also sets the initial logging (config processing) to debug. (Default: `false`) |

These configuration values affect how the application logs information.  The two
easiest to explain are the `*file` and `*level` values.  These configuration values
specify what the log level is for the application and whether to redirect any logged
information away from the standard output (stdout) to the specified log file.

The `log.stack-trace` configuration item (and its `--stack-trace` command line flag)
are
a bit more nuanced in its behavior. The simple part of this setting's behavior is
to generate a debugging stack trace when an application error occurs.  From our
experience, this information is confusing to the typical users but that information
is critical to the diagnosis of any application error.

The nuanced part of this flag has to do with the application's initialization
process.  Because the configuration manager must be initialized to access the
`log.stack-trace` configuration item, there is a narrow window where there is
no control over log settings and whether to emit a stack trace for an application
error. As one of the only reasons to use the command line flag is to debug an
application error, it seems fitting to also enable debug debugging until the
configuration manager is properly initialized.
Normally we typically stick to a "one configuration item, one result" guideline,
but this seemed to be the right time to make an exception.

### Rule Plugins

These affect the collection of rule plugins and whether they are called.

<!-- pyml disable-num-lines 5 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| *special* | --enable-rules,-e   | string    | Comma separated list of rules to enable. |
| *special* | --disable-rules,-d  | string    | Comma separated list of rules to disable. |
| plugins.additional_paths | --add-plugin     | string    | Path to a plugin containing a new rule to apply. |

The enabling and disabling of plugins can be accomplished in two ways.  From the
command line, the `--enable-rules` and `--disable-rules` arguments allow for the
user to specify a comma-separated
set of rule identifiers in the next argument.  If a configuration file option
is required, the rule plugin can be enabled as specified in the next section.

Additional rule plugins can be added to the configuration in one of two ways.  To
evaluate new rule plugins,
the recommended way to add a rule plugin is to use the `--add-plugin` command line
argument once for each rule plugin to add.
Each `--add-plugin` argument is followed by another argument that specifies a file
to load as a new plugin.  For a more permanent solution, the `plugins.additional_paths`
configuration value
can be used in a comparable manner, specifying one or more paths using a comma-separated
string containing the paths.

### General Plugin Settings

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Available: Version 0.9.30**

<!-- pyml disable-num-lines 4 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| `plugins.selectively_enable_rules` | -- | Boolean | Specify whether to enable selective enable mode. |

In certain cases, it is necessary or desired to produce a minimal set of rules to
be applied against a set of Markdown documents.  That is where the `selectively_enable_rules`
configuration setting and the selective enable mode for rules is required.  Available
through both [command line](#exception-selective-enabling-of-rules) and configuration
settings, setting this value to `True` disables all rules while allowing for rules
to be selectively enabled.

For example, to instruct the PyMardown linter to only apply rule Md007 to a series
of documents, specify the following configuration:

```text
plugins.selectively_enable_rules: True
plugins.Md007.enabled: True
```

Regardless of the default settings for the available rules in the system, that configuration
will disabled all of them, except for Rule Md007 which will be enabled.
For more information on this, refer to the section on the
[Selective Enabling of Rules](#exception-selective-enabling-of-rules).

### Rule Plugin Settings

<!-- pyml disable-num-lines 4 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| `plugins.{id}.enabled` | -- | Boolean | Specify whether the plugin rule is enabled. |
| `plugins.{id}.other` | -- | Various | Specify other configuration properties specific to the rule. |

The list of configuration values for rule plugins is slightly
different than the configuration for the rest of the system.
For each rule plugin, there is a main boolean configuration
value, in the form `plugins.{id}.enabled`, that specifies the rule
plugin's enabled state.  In that string, the sequence `{id}`
can be any one of the valid identifiers for a plugin rule.

Once enabled, each rule plugin is responsible for its own
properties located under the hierarchy of `plugins.{id}.`.
The list of configuration values available for each standard
plugin rule is shown in the `Configuration` section for
each [standard rule plugin](./advanced_plugins.md).

### Extensions

Extensions follow the same pattern as rule plugins, except that no general
command line settings are available.  From our experience, enabling extensions
is usually done from configuration files, and applied to an entire project.
As such, we do not believe having a general command line setting provides
any benefit to the user.

Like the rule plugins, the list of configuration items for each
extension is shown in the `Configuration` section for
each [extension](./advanced_extensions.md).

### Other

These items do not fit nicely into any other category.

<!-- pyml disable-num-lines 4 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| -- | --continue-on-error | Boolean | Enable PyMarkdown to continue after application errors. |
| -- | --return-code-scheme | String | Specify a scheme to use when formulating the return code. |

These two arguments do not match any configuration items and instead are interpreted
right from the command line. The argument `--continue-on-error` specifies that the
application can continue after an application error, while still emitting a return
code that indicates that application error.  The argument `--return-code-scheme`
alters the return code values based on a selected map of outcomes to return codes.
Both are better documented in the User Guide section on
[General Command Line Arguments](./user-guide.md#general-command-line-arguments).

## Common Topics

### How To Enable or Disable Rules

The easiest way to enable or disable rules is with the command line.

```text
pymarkdown -d MD041,md013 scan .
```

Whether specified by a configuration file or through the command line, the
enable and disable settings follow the normal rules of [Configuration Ordering](https://application-properties.readthedocs.io/en/latest/getting-started/#configuration-ordering-layering).
That is to say that the above command line will override any enable/disable
setting using the `--set` command line or through a configuration file.

#### Exception: Enabling/Disabling Rules From The Command Line

One tenet that we strive to follow is to have a clearly defined behavior for
our application.  And for observant readers, there was a bit of undefined behavior
talked about in the last section.  Consider the following example:

```text
pymarkdown -e Md041 -d Md041 scan .
```

As PyMarkdown allows for both enabling and disabling of a plugin to occur on
the command line and assigns it to its highest layer, what happens if both
are specified for the same rule?

Encountering this rule during our own testing, we did some more research to
determine the scope of this issue.  With every other layer of the configuration
manager, there is a combined enable and disable setting, instead of having a
split setting.  As such, the scope of this issue was solely focused on the
command line.  Since we believe that users will disabling plugins more often
than enabling plugins, we decided that command line disables would have
priority over command line enables.

#### Exception: Selective Enabling of Rules

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Available: Version 0.9.30**

Suggested by a user in [Issue 1396](https://github.com/jackdewinter/pymarkdown/issues/1396),
the PyMarkdown linter now supports the blanket disabling of all rules.  As mentioned
above, the disabling of a specific rule at a given level will cause that rule to
be forcibly disabled for that level and any lower levels, regardless of any enabling
done at the same level or lower.  Selectively enabling rules presents an interesting
twist to that pattern.

When selectively enabling items with any system, the enabling mechanism disables
every instance of the specific thing while presenting the user the ability to enable
a specified subset of those things. A popular example is an internet firewall, where
any incoming communication into a system is disabled unless someone has specifically
opened a way through the firewall. If you do not follow the proscribed method to
cross the firewall, your traffic bounces off the firewall.

Previously exposed for testing purposes, the PyMarkdown linter now provides the
ability to selectively enable rules using a command line like:

```bash
pymarkdown -e Md041 -d * scan .
```

This command line instructs the application to disable all rules, enabling only
Rule Md041. There are various uses for this mechanism, but the simplest one to
explain is the onboarding of a team to using the PyMarkdown linter.  Enabling the
full scanning of a set of Markdown documents without using a measured approach
can be daunting and overwhelming to a team. By using the selective enablement of
rules, that team can iteratively go onboard sets of rules until the complete
set of desired rules is in place.

##### Configuration Layers Matter

Selective enablement of rules is implemented at both the command line and general
configuration levels [(see General Plugin Settings)](#general-plugin-settings).
At the command line level, only command line enable arguments can activate a rule.
At the general configuration level, rules can be enabled either through the configuration
file or command line arguments.

Command line enablement takes precedence over general configuration, meaning if
a rule is enabled at the command line, it overrides any conflicting settings in
the general configuration. This precedence can be visualized as a layered approach:
if the command line layer provides a definitive setting, the general configuration
layer is not consulted.

### Multiple Identifiers For The Same Rule Plugin

A rule plugin can have two or more identifiers, one id plus
multiple aliases. If multiple identifiers belonging to a
single plugin rule are used for separate configuration
hierarchies, there must be a predictable ordering used
to resolve which hierarchy is used.  In order, the rule
plugin's id comes first, followed by each alias in the
order that they are entered in the plugin rule itself.
This rule applies to the group of configuration values
as a group.

For example, suppose there is a configuration file with
the contents of:

```json
{
"plugins" : {
    "heading-style-h1" : { 
        "enabled" : true,
        "style" : "consistent"
    },
    "md003" : { 
        "enabled" : false
    }
}
```

According to the documentation on [Rule Md003](./plugins/rule_md003.md),
the id for that rule is `md003` and it has one alias `heading-style-h1`.
This means that the `plugins.md003` configuration takes
precedence over the `plugins.heading-style-h1` configuration,
due to the rules specified above, regardless of its position in
the configuration file. Also, if instead
the `"enabled" : false` configuration value was `"enabled" : true`, the `plugins.heading-style-h1.style`
configuration value is set but it will not be used by the configuration manager.
For that configuration value to be used, the `plugins.md003` configuration
hierarchy must be removed completely as the entire hierarchy
has precedence, not just individual configuration properties.

### Command Line Vs Configuration File

One question that comes up repeatedly, for PyMarkdown or for other projects,
is whether to use a configuration file or command line arguments. And that answer
relies on your context.  

From our experience, there are typically five reasons for using configuration files
over command line arguments:

- conciseness: you prefer to keep any configuration values in a single file for
  that application
- reusability: you want to reuse those values in other locations, such as scripts
- simplicity: you want to do more complicated configuration without specifying "extra"
  command line options
- single responsibility: you only want pre-commit hook configuration in the file,
  everything else goes elsewhere
- catch-all: because... personal taste

If you are only leveraging PyMarkdown from one part of your project and are not executing
it from anywhere else, the above reasons either may not apply or may not be
as impactful to your decision.  There may also be other reasons
not listed here, such as team guidelines, which sway the decision one way or the
other. It really does come down to a team choice.

For our team, we typically
prefer to have our configuration items in their own specific configuration file.
The main reasons
for this are reusability and readability.  Our team's guidelines are to have one
configuration file per tool (where possible) and to be as precise about the configuration
items as possible.  Therefore, we use a JSON configuration file that we specifically
invoke from the command line each time.  For us, that pedantic act of specifying
a configuration file explicitly works for us, and we can easily explain what
our rationale is to each other.

Following that decision is our use of the command line for new configuration
items.  The best way to explain it is that we view our configuration file as
"well-tested cold storage" and the command line as a test platform.  If we see
configuration on a command line, we know that it is a new setting that is being
evaluated, not something that has been battle tested.  But those are our guidelines,
ones that work for our team.

This is a decision that you need to make with your project team.  And
when you make the decisions, please document them somewhere with enough information
so that you can revisit the decision later.  Team members and
reasons change over time, so it is good to remember the reasons behind your
decision.
