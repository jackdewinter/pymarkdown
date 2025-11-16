---
summary: More information on configuration and how to apply it.
authors:
  - Jack De Winter
---

# Advanced Configuration

Configuration is a fundamental aspect that every application must address. Whether
it's handling simple command-line options, enabling features, or setting values
for those features, applications require a robust configuration management system
to manage these variables effectively.

Early in the development of the PyMarkdown application, we recognized the importance
of having a reliable and flexible configuration system of our own.

## A Note To Begin With

The base documentation for the [`application_properties`](https://application-properties.readthedocs.io/en/latest/getting-started/)
project was originally adapted from this document to serve as the main documentation
for that project. To avoid unnecessary repetition, we now provide links to the relevant
sections of that documentation rather than duplicating content here. We believe
that moving the documentation to its new home gave us an opportunity to further
refine and improve it for the `application_properties` project. We hope that this
effort also enhances the experience for users of the `pymarkdown` project.

## Skipping Ahead

As this is the Advanced Configuration document, we focus on explaining the configuration
manager and how it resolves configuration items. We strongly recommend taking the
time to understand the configuration manager before making changes to configuration
values, but ultimately, the choice is yours.

If you prefer to jump directly to specific topics, here are some sections you may
find useful:

- [Configuration Files](#configuration-files)
    - Learn about the types of configuration files we support and how to access
      them.
- [Command Line Configuration](#command-line)
    - How to specify configuration items from the command line.
    - If you are working with boolean or integer values, see the
      [Configuration Item Types](https://application-properties.readthedocs.io/en/latest/command-line/#configuration-item-types)
      section.
- [Enabling or Disabling Rules](#how-to-enable-or-disable-rules)
    - How to turn rules on and off
- [Available Configuration Items](#available-configuration-items)
    - A complete list of configuration items and options for changing their values.

## Nomenclature

See the [Nomenclature section](https://application-properties.readthedocs.io/en/latest/getting-started/#nomenclature)
of the `application_properties` project documentation.

## Configuration Files

See the [Configuration Files section](https://application-properties.readthedocs.io/en/latest/file-types/)
of the `application_properties` project documentation.

### Which One Is Best - Addendum for PyMarkdown

In the original documentation, we made the following observation:

> If comments are important to you, then JSON is out.

However, starting with version 0.9.32 of PyMarkdown (and version 0.9.0 of `application_properties`),
we now support the JSON5 parser, which allows comments in JSON files. This feature
is enabled by default. (See [this section](./user-guide.md#-no-json5-configuration)
for more details.)

When discussing the pros and cons of JSON5 versus YAML with friends and colleagues,
we found that the best answer is: it depends.

From these conversations, it became clear that both background and personal preference
play a significant role in choosing one file type over another. Our team’s advice
is that JSON tends to be stricter and more explicit, while YAML is more flexible
and forgiving. When we shared these observations, only a small percentage of people
disagreed—and those who did were typically strong advocates for either JSON or YAML.

Ultimately, choose the format that works best for you and your team. And remember,
if you ever change your mind, there are easy-to-use format converters available.

### Command Line

See the [Configuration Files section](https://application-properties.readthedocs.io/en/latest/file-types/)
of the `application_properties` project documentation.

## Available Configuration Items

The available configuration items are broken down into the following areas:

- [General - `mode.*` + command line](#general) - Global settings.
- [Logs - `log.*`](#logs) - Settings that affect how logging works.
- [System - `system.*`](#logs) - Settings that affect the entire system.
- [Rules - `plugins.*` + command line](#rule-plugins) - Settings that affect the
  various plugins.
- [Extensions - `extensions.*`](#extensions) - Settings that affect the various
  extensions.
- [Other - command line](#other) - Settings that do not fit into other categories.

### General

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

These configuration values control how the application logs information. The `*file`
and `*level` options are straightforward: they determine the log level for the application
and whether log messages are written to a file instead of standard output (stdout).

The `log.stack-trace` configuration item (and its `--stack-trace` command line flag)
has a more nuanced role. At its core, enabling this setting causes the application
to print a debugging stack trace whenever an error occurs. While this information
can be overwhelming for typical users, it is invaluable for diagnosing application
errors.

There is an additional subtlety regarding when this flag takes effect. Since the
configuration manager must be initialized before the `log.stack-trace` setting can
be accessed, there is a brief period during startup when log settings and stack
trace output cannot be controlled. Because the primary use case for the `--stack-trace`
flag is debugging application errors, we chose to enable debug-level logging from
startup until the configuration manager is fully initialized.

Although we usually follow a "one configuration item, one result" principle, this
was a case where making an exception provided a better user experience for debugging.

### System

These items affect various aspects of the application:

<!-- pyml disable-num-lines 2 line-length-->
| Key | Command Line | Type | Description |
| system.exclude_path | --exclude | string | Comma separated list of relative glob paths to exclude. |

The `system.exclude_path` configuration item (and its command line equivalent)
allows you to instruct the application to scan a path while excluding one or more
globbed paths. This feature was introduced in response to
[issue 1462](https://github.com/jackdewinter/pymarkdown/issues/1462),
which highlighted the need for both command line and configuration-based methods
to specify excluded glob paths.

There is a key difference between the two approaches:

- On the command line, you can specify multiple glob paths to exclude by repeating
  the argument (e.g., `--exclude 1.md --exclude 2.md`).
- In the configuration file, the item can only be specified once, so you provide
  a comma-separated list of paths (e.g., `-s system.exclude_path=1.md,2.md`).

This flexibility allows you to choose the method that best fits your workflow.

### Rule Plugins

These affect the collection of rule plugins and whether they are called.

<!-- pyml disable-num-lines 5 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| *special* | --enable-rules,-e   | string    | Comma separated list of rules to enable. |
| *special* | --disable-rules,-d  | string    | Comma separated list of rules to disable. |
| plugins.additional_paths | --add-plugin     | string    | Path to a plugin containing a new rule to apply. |

Plugins can be enabled or disabled either through the command line or by using
a configuration file. On the command line, you can use the `--enable-rules` and
`--disable-rules` arguments to specify a comma-separated list of rule identifiers
to enable or disable. If you prefer to manage plugin settings through a configuration
file, you can enable rule plugins as described in the following section.

You can add additional rule plugins either temporarily or permanently. For temporary
evaluation, the recommended approach is to use the `--add-plugin` command line argument
for each plugin you want to add, with each argument followed by the path to the
plugin file. If you want a more permanent setup, you can use the `plugins.additional_paths`
configuration value, specifying one or more plugin paths as a comma-separated list.
This allows you to tailor plugin management to your workflow, whether you need a
quick test or a lasting configuration.

#### General Plugin Settings

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Available: Version 0.9.30**

<!-- pyml disable-num-lines 4 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| `plugins.selectively_enable_rules` | -- | Boolean | Specify whether to enable selective enable mode. |

In some situations, you may want to apply only a minimal set of rules to your Markdown
documents. The selectively_enable_rules configuration setting enables this selective
mode. When set to True, all rules are disabled by default, and you can then explicitly
enable only the rules you want to use. This option is available through both the
[command line](#exception-selective-enabling-of-rules) and configuration settings.

For instance, if you want the PyMarkdown linter to apply only rule Md007 to a group
of documents, you would use the following configuration:

```text
plugins.selectively_enable_rules: True
plugins.Md007.enabled: True
```

With this configuration, all rules are disabled except for Md007, regardless of
the system's default rule settings. For more details, see the section on
[Selective Enabling of Rules](#exception-selective-enabling-of-rules).

#### Specific Plugin Settings

<!-- pyml disable-num-lines 4 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| `plugins.{id}.enabled` | -- | Boolean | Specify whether the plugin rule is enabled. |
| `plugins.{id}.other` | -- | Various | Specify other configuration properties specific to the rule. |

The configuration values for rule plugins differ somewhat from those used elsewhere
in the system. Each rule plugin has a primary boolean configuration value, written
as `plugins.{id}.enabled`, which determines whether that rule is enabled. Here,
`{id}` represents any valid identifier for a plugin rule.

After a rule plugin is enabled, it manages its own configuration properties, all
of which are organized under the `plugins.{id}.` hierarchy. This structure allows
each plugin to define and control its specific settings independently from the
rest of the system. The full list of configuration values available for each standard
plugin rule is shown in the `Configuration` section for
each [standard rule plugin](./advanced_plugins.md).

### Extensions

Extensions are configured in much the same way as rule plugins, but unlike plugins,
there are no general command line options available for enabling or configuring
extensions. In our experience, extensions are typically enabled through configuration
files and applied at the project level. For this reason, we have found that providing
general command line options for extensions does not offer significant value to
users.

As with rule plugins, the configuration options for each extension are detailed
in the `Configuration` section of their respective
[extension documentation](./advanced_extensions.md).

### Other

These items do not fit nicely into any other category.

<!-- pyml disable-num-lines 4 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| -- | --continue-on-error | Boolean | Enable PyMarkdown to continue after application errors. |
| -- | --return-code-scheme | String | Specify a scheme to use when formulating the return code. |

These two arguments are not associated with any configuration items and are handled
directly from the command line. The `--continue-on-error` option allows the application
to keep running after an error occurs, while still returning a code that indicates
an error was encountered. The `--return-code-scheme` option changes the return code
values according to a specified mapping of outcomes to return codes. For more details,
see the User Guide section on
[General Command Line Arguments](./user-guide.md#general-command-line-arguments).

## Common Topics

### How To Enable or Disable Rules

The simplest way to enable or disable rules is by using the command line. For example:

```text
pymarkdown -d MD041,md013 scan .
```

Whether you specify these settings in a configuration file or on the command line,
the enable and disable options follow the standard rules of
[Configuration Ordering](https://application-properties.readthedocs.io/en/latest/getting-started/#configuration-ordering-layering).
This means that command line arguments, such as the example above, will override
any enable or disable settings provided via the `--set` option or within a configuration
file.

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
pymarkdown -e Md041 -d "*" scan .
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

A rule plugin can have multiple identifiers: a primary ID and one or more aliases.
When separate configuration hierarchies use different identifiers for the same plugin
rule, there must be a clear and predictable order to determine which configuration
takes precedence. The rule is as follows: the plugin's primary ID is considered
first, followed by each alias in the order they are defined within the plugin. This
ordering applies to the entire group of configuration values for that plugin.

For example, consider the following configuration file:

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

According to the documentation for [Rule Md003](./plugins/rule_md003.md), the primary
ID for this rule is `md003`, and it has an alias heading-style-h1. In this case,
the `plugins.md003` configuration takes precedence over the `plugins.heading-style-h1`
configuration, regardless of their order in the file. If the `"enabled": false`
value under `md003` were instead `"enabled": true`, the property `plugins.heading-style-h1.style`
would still not be used by the configuration manager unless the entire `plugins.md003`
hierarchy was removed. This is because precedence is determined at the hierarchy
level, not for individual configuration properties.

### Command Line Vs Configuration File

A common question, both for PyMarkdown and other projects, is whether to use a
configuration file or command line arguments. The answer depends on your specific
context and needs.

In our experience, configuration files are often preferred for several reasons.
They allow you to keep all configuration values in a single, organized location,
making it easier to manage and review settings. Configuration files also promote
reusability, as you can reference the same settings in different scripts or environments.
They simplify complex configurations by reducing the need for lengthy or repetitive
command line options. If you want to separate concerns, you can dedicate configuration
files to specific purposes, such as pre-commit hooks, while keeping other settings
elsewhere. And sometimes, the choice simply comes down to personal or team preference.

Ultimately, the decision between configuration files and command line arguments
should be based on what works best for your workflow and team. Consider your project's
requirements, how often settings change, and how you want to manage and share configuration
information.

If you are only using PyMarkdown in a single part of your project and not invoking
it elsewhere, the reasons for choosing configuration files over command line arguments
may not be as relevant or influential. Other factors, such as team guidelines or
project conventions, might also play a role in your decision. Ultimately, the choice
comes down to what works best for your team.

In our experience, we prefer to keep configuration items in dedicated configuration
files. This approach offers greater reusability and readability. Our team’s guideline
is to maintain one configuration file per tool whenever possible, and to be as precise
as possible with configuration items. As a result, we use a JSON configuration file
that we explicitly specify on the command line each time we run the tool. This deliberate
approach works well for us and makes it easy to explain our rationale to each other.

We also use the command line for experimenting with new configuration items. For
us, the configuration file serves as "well-tested cold storage," while the command
line acts as a test platform. When we see a configuration option on the command
line, we know it’s being evaluated and hasn’t yet been fully adopted. These are
our team’s practices, and they suit our workflow.

Whatever you decide, make sure to discuss and document your team’s approach. Having
clear documentation will help you revisit and understand your decisions later,
especially as team members and project requirements change over time.
